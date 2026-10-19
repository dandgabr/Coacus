#!/usr/bin/env python3
"""Coacus installer: activate rendered artifacts into a harness.

The repository GENERATES the per-harness artifacts (session-start-bootstrap); this script
INSTALLS them into a harness's own discovery locations. It is explicit and
idempotent — nothing runs at session start, and it never rewrites a harness
config file wholesale.

Mechanisms (verified against vendor docs, see docs/install.md):

- opencode    plugin -> <config_dir>/plugins/coacus.js  (`__COACUS_ROOT__`
              substituted) + governor gate, plus skill trees under
              <config_dir>/skills/ and agents under <config_dir>/agent/.
- claude-code skills   -> <config_dir>/skills/<skill>/  (documented personal path;
              real files land once in the shared ~/.agents/skills tree and a
              symlink per skill is placed here, unless --skills-mode copy)
              agents   -> <config_dir>/agents/<name>.md
              hook     -> plugin staged at <config_dir>/plugins/coacus/ with the
              JSON payload at bootstrap/session-start.json (matching hooks.json).
- antigravity plugin (manifest + compact rule + native agent selectors +
              on-demand catalog MCP by default; full native profile optional) ->
              <config_dir>/config/plugins/coacus/; activation is by directory,
              so no registry edit is needed.
- codex       skills   -> ~/.agents/skills/<skill>/  (Codex scans .agents/skills,
              not ~/.codex/skills); agents -> <config_dir>/agents/<name>.toml;
              plus the SessionStart hook at <config_dir>/hooks.json.
- cursor      skills   -> ~/.agents/skills/<skill>/; agents ->
              <config_dir>/agents/<name>.md; plus the sessionStart hook at
              <config_dir>/hooks.json (snake_case `additional_context`).
- command-code skills   -> ~/.agents/skills/<skill>/ (a Command Code user scan
              root); agents -> <config_dir>/agents/<name>.md; the SessionStart
              bootstrap is merged into <config_dir>/settings.json under the
              'hooks' key (Command Code has no separate hooks.json); the context7
              MCP is merged into <config_dir>/mcp.json under 'mcpServers'; and
              the Coacus user rules are written to <config_dir>/AGENTS.md when
              that file does not already exist.

Usage:
    python3 scripts/coacus_install.py <harness|all> [--dry-run] [--uninstall]
    python3 scripts/coacus_install.py opencode --config-dir /tmp/oc

A manifest (`coacus-install.json`) is written next to each target so re-runs
are idempotent and `--uninstall` removes exactly what was installed.

Partial installs keep the session-start skills budget small: a harness that
indexes every skill pays for every description. Filter with `--only` (top-level
category, applied to skills and agents), `--skills` (skill name glob) and/or
`--agents` (agent name glob); `--list` prints what is available.

    python3 scripts/coacus_install.py codex --only security,engineering
    python3 scripts/coacus_install.py codex --skills 'lang-python,framework-*'
    python3 scripts/coacus_install.py codex --agents 'qa-*,*-architect'
    python3 scripts/coacus_install.py codex --list
"""

from __future__ import annotations

import argparse
import ast
import base64
import fnmatch
import hashlib
import json
import os
import re
import shlex
import shutil
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path

try:  # tomllib entered the standard library in Python 3.11.
    import tomllib
except ModuleNotFoundError:  # Keep the Coacus Python 3.10 floor.
    tomllib = None  # type: ignore[assignment]

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

MANIFEST_NAME = "coacus-install.json"
NOTICE_NAME = "THIRD-PARTY-NOTICES.md"

@dataclass(frozen=True)
class Symlink:
    """An installed path that is a symbolic link to ``target`` (absolute).

    A harness that scans its OWN skill home (Claude Code's ``~/.claude/skills``)
    but shares the canonical ``~/.agents/skills`` tree gets a symlink per skill
    instead of a second real copy. Single source of truth, and Orca's skill list
    (which scans both homes) collapses the duplicate to one entry.
    """

    target: str


# A planned file's content: text normally, bytes for a binary companion, or a
# symlink to an absolute target.
FileContent = str | bytes | Symlink
SKILL_ROOTS = ("methodology/workflows", "knowledge/skills")
CODEX_PROFILE_START = "# BEGIN COACUS CODEX SKILL PROFILE"
CODEX_PROFILE_END = "# END COACUS CODEX SKILL PROFILE"


def _codex_profile_visible(root: Path) -> set[str]:
    """Load the small Codex-native allowlist, checking canonical identities."""
    path = root / "harnesses/codex/skills-profile.json"
    try:
        names = json.loads(path.read_text(encoding="utf-8"))["visible"]
    except (OSError, ValueError, KeyError, TypeError) as exc:
        raise ValueError(f"invalid Codex skill profile: {exc}") from exc
    if not isinstance(names, list) or not names or any(not isinstance(n, str) for n in names):
        raise ValueError("invalid Codex skill profile: visible must be a nonempty name list")
    if len(set(names)) != len(names):
        raise ValueError("invalid Codex skill profile: duplicate visible name")
    available = [skill.name for skill in discover_skills(root)]
    if len(set(available)) != len(available) or not set(names) <= set(available):
        raise ValueError("invalid Codex skill profile: names missing or ambiguous")
    return set(names)


def _strip_codex_profile(text: str) -> tuple[str, str]:
    """Remove the skill profile, preserving user tables inside its markers.

    Codex can insert UI tables before the closing comment. Only the leading
    skill tables belong to Coacus; retain the entire suffix from the first
    other table without scanning its values (which may be multiline strings).
    """
    start_token = "\n" + CODEX_PROFILE_START + "\n"
    start = text.find(start_token)
    end_token = CODEX_PROFILE_END + "\n"
    if start < 0:
        if CODEX_PROFILE_START in text or CODEX_PROFILE_END in text:
            raise ValueError("Codex config has a damaged Coacus profile block")
        return text, ""
    end = text.find(end_token, start)
    if end < 0 or text.find(start_token, start + 1) >= 0:
        raise ValueError("Codex config has a damaged Coacus profile block")
    body_start = start + len(start_token)
    offset = body_start
    for line in text[body_start:end].splitlines(keepends=True):
        stripped = line.strip()
        if stripped.startswith("[") and not re.fullmatch(r"\[\[skills\.config\]\]\s*(?:#.*)?", stripped):
            # Treat all subsequent bytes as user-owned, including any skill
            # overrides they contain. The updater already respects overrides.
            return (
                text[:start] + "\n" + text[offset:end] + text[end + len(end_token) :],
                text[start:offset] + end_token,
            )
        offset += len(line)
    return text[:start] + text[end + len(end_token) :], text[start : end + len(end_token)]


def _toml_statement_lines(text: str):
    """Yield lines starting outside multiline strings for the fallback scanner."""
    quote = ""
    for line in text.splitlines():
        is_statement = not quote
        pos = 0
        while pos < len(line):
            if quote:
                if quote.startswith('"') and line[pos] == "\\":
                    pos += 2
                elif line.startswith(quote, pos):
                    pos += len(quote)
                    quote = ""
                else:
                    pos += 1
            elif line[pos] == "#":
                break
            elif line[pos] in "\"'":
                quote = line[pos] * (3 if line.startswith(line[pos] * 3, pos) else 1)
                pos += len(quote)
            else:
                pos += 1
        # Single-line strings do not carry lexical state into the next line.
        if len(quote) == 1:
            quote = ""
        if is_statement:
            yield line


def _codex_user_skill_entries(text: str) -> list[dict[str, object]]:
    """Read user skill overrides, with a small Python 3.10 fallback scanner."""
    if tomllib is not None:
        try:
            parsed = tomllib.loads(text)
        except tomllib.TOMLDecodeError as exc:
            raise ValueError(f"Codex config is invalid TOML: {exc}") from exc
        skills_table = parsed.get("skills", {})
        if not isinstance(skills_table, dict):
            raise ValueError("Codex config skills must be a table")
        entries = skills_table.get("config", [])
        if not isinstance(entries, list):
            raise ValueError("Codex config skills.config must be an array")
        return entries

    # Python 3.10 has no standard TOML parser. Read only the array entries this
    # installer must preserve; leave all other config bytes untouched for Codex.
    entries: list[dict[str, object]] = []
    in_skill = False
    for raw_line in _toml_statement_lines(text):
        line = raw_line.strip()
        if line == "[[skills.config]]":
            entries.append({})
            in_skill = True
            continue
        if line.startswith("[") and line.endswith("]"):
            in_skill = False
            continue
        if not in_skill or "=" not in line:
            continue
        key, value = (part.strip() for part in line.split("=", 1))
        if key == "path":
            try:
                path = ast.literal_eval(value)
            except (SyntaxError, ValueError) as exc:
                raise ValueError("Codex config has an invalid skills.config path") from exc
            if not isinstance(path, str):
                raise ValueError("Codex config has a non-string skills.config path")
            entries[-1]["path"] = path
        elif key == "enabled":
            if value not in ("true", "false"):
                raise ValueError("Codex config has an invalid skills.config enabled value")
            entries[-1]["enabled"] = value == "true"
    return entries


def _codex_config_update(
    root: Path, config_dir: Path, profile: str
) -> tuple[str, str, list[str], bool]:
    """Return new TOML, owned block, user conflicts and whether file existed."""
    if profile not in ("compact", "full"):
        raise ValueError(f"unknown Codex skill profile: {profile}")
    config_path = config_dir / "config.toml"
    existed = config_path.is_file()
    current = config_path.read_text(encoding="utf-8") if existed else ""
    base, _ = _strip_codex_profile(current)
    user_entries = _codex_user_skill_entries(base)
    user_paths: dict[str, bool] = {}
    for item in user_entries:
        if isinstance(item, dict) and isinstance(item.get("path"), str):
            key = item["path"]
            user_paths[key] = user_paths.get(key, False) or bool(item.get("enabled", True))
    visible = _codex_profile_visible(root) if profile == "compact" else set()
    block_lines = ["", CODEX_PROFILE_START]
    conflicts: list[str] = []
    if profile == "compact":
        for source in discover_skills(root):
            if source.name in visible:
                continue
            installed = (config_dir.parent / ".agents" / "skills" / source.name / "SKILL.md").resolve()
            key = installed.as_posix()
            if key in user_paths:
                if user_paths[key]:
                    conflicts.append(key)
                continue
            block_lines.extend(("[[skills.config]]", f"path = {json.dumps(key)}", "enabled = false", ""))
    block = "\n".join(block_lines + [CODEX_PROFILE_END, ""]) if len(block_lines) > 2 else ""
    updated = base + block
    if tomllib is not None:
        try:
            tomllib.loads(updated)
        except tomllib.TOMLDecodeError as exc:
            raise ValueError(f"Codex config profile would be invalid TOML: {exc}") from exc
    return updated, block, conflicts, existed


def _write_codex_config(config_dir: Path, text: str, existed: bool) -> None:
    """Atomically update Codex config, preserving existing file permissions."""
    target = config_dir / "config.toml"
    if not text and not existed:
        return
    target.parent.mkdir(parents=True, exist_ok=True)
    mode = target.stat().st_mode & 0o777 if target.exists() else 0o600
    fd, temporary = tempfile.mkstemp(prefix=".config.toml.", dir=target.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as stream:
            stream.write(text)
        os.chmod(temporary, mode)
        os.replace(temporary, target)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def _home() -> Path:
    return Path.home()


def default_config_dir(harness: str, home: Path) -> Path:
    """Return the default config directory for ``harness`` under ``home``."""
    return {
        "opencode": home / ".config" / "opencode",
        "claude-code": home / ".claude",
        "antigravity": home / ".gemini",
        "codex": home / ".codex",
        "cursor": home / ".cursor",
        "command-code": home / ".commandcode",
    }[harness]


# Per-harness detection facts: the environment variables the harness sets and/or
# the executables it installs. A harness is "present" when any of them resolves.
# This is the DATA half; `harness_present` is the consumer. Without this guard the
# installer writes a full corpus into a config dir for a harness that is not
# installed (the bug this closes).
HARNESS_DETECTION: dict[str, dict[str, list[str]]] = {
    "opencode": {"env": ["OPENCODE_CONFIG_DIR", "OPENCODE"], "bins": ["opencode"]},
    "claude-code": {"env": ["CLAUDE_PLUGIN_ROOT"], "bins": ["claude"]},
    "antigravity": {"env": ["GEMINI_DIR", "ANTIGRAVITY"], "bins": ["agy", "antigravity"]},
    "codex": {"env": ["CODEX_HOME"], "bins": ["codex"]},
    "cursor": {"env": ["CURSOR_TRACE_ID", "CURSOR_PLUGIN_ROOT"], "bins": ["cursor", "cursor-agent"]},
    "command-code": {"env": ["COMMANDCODE_PROJECT_DIR"], "bins": ["command-code", "cmd"]},
}


def harness_present(harness: str, home: Path | None = None) -> bool:
    """True when ``harness`` appears installed on this machine.

    Detection is by the harness's own environment variable or its executable on
    PATH — never by the mere existence of the config directory, which Coacus
    itself may have created. This is what prevents installing into an absent
    harness.
    """
    import os

    facts = HARNESS_DETECTION.get(harness)
    if facts is None:
        return True  # unknown harness: do not block a custom adapter
    if any(os.environ.get(var) for var in facts.get("env", [])):
        return True
    return any(shutil.which(binary) for binary in facts.get("bins", []))


def _split_filter(value: str | None) -> list[str]:
    """Parse a comma-separated filter into clean tokens (`None` -> no filter)."""
    if not value:
        return []
    return [token.strip() for token in value.split(",") if token.strip()]


def _skill_groups(root: Path) -> dict[str, list[Path]]:
    """Every skill keyed by its top-level root, with the path segments under it.

    Returns ``{skill_dir: segments}`` where ``segments`` is the relative path
    from the skill root down to (but excluding) the skill directory. For
    ``knowledge/skills/domains/academic/foo/SKILL.md`` that is
    ``("domains", "academic")``; for ``methodology/workflows/using-coacus`` it is
    ``("workflows",)`` so the workflows collection has a stable category name.
    """
    groups: dict[str, list[str]] = {}
    for top in SKILL_ROOTS:
        base = root / top
        if not base.is_dir():
            continue
        default = "workflows" if top == "methodology/workflows" else ""
        for skill_md in sorted(base.rglob("SKILL.md")):
            skill = skill_md.parent
            rel = skill.relative_to(base)
            segments = list(rel.parts[:-1])
            if default and not segments:
                segments = [default]
            groups[str(skill)] = segments
    return groups


def discover_skills(
    root: Path, only: list[str] | None = None, skills: list[str] | None = None
) -> list[Path]:
    """All skill directories (the parent of a SKILL.md) in the repository.

    ``only`` keeps skills whose path under its root contains one of the given
    category tokens (matched against every path segment, so both ``domains`` and
    ``academic`` select the academic skills). ``skills`` keeps skills whose
    directory name matches one of the given fnmatch globs. Both filters are
    OR-ed within their own list and AND-ed with each other; an empty filter is
    no filter.
    """
    groups = _skill_groups(root)
    found: list[Path] = []
    for skill_str, segments in groups.items():
        skill = Path(skill_str)
        if only and not any(token in segments for token in only):
            continue
        if skills and not any(fnmatch.fnmatch(skill.name, pat) for pat in skills):
            continue
        found.append(skill)
    return found


def list_skills(root: Path) -> dict[str, object]:
    """Inventory for `--list`: categories and skill names, no harness needed."""
    groups = _skill_groups(root)
    categories: dict[str, list[str]] = {}
    for skill_str, segments in groups.items():
        name = Path(skill_str).name
        for segment in segments or ["(root)"]:
            categories.setdefault(segment, []).append(name)
    return {
        "skills": sorted(Path(s).name for s in groups),
        "categories": {k: sorted(v) for k, v in sorted(categories.items())},
        "count": len(groups),
    }


AGENT_SOURCE_NAME = "agent.source.md"


def _agent_groups(root: Path) -> dict[str, list[str]]:
    """Every canonical agent keyed by its source path, with its path segments.

    Returns ``{agent_source: segments}`` where ``segments`` is the relative path
    from ``knowledge/agents`` down to (but excluding) the agent directory. For
    ``knowledge/agents/core-orchestration/antigravity-agent/agent.source.md``
    that is ``("core-orchestration",)``.
    """
    agents_dir = root / "knowledge" / "agents"
    groups: dict[str, list[str]] = {}
    if not agents_dir.is_dir():
        return groups
    for source in sorted(agents_dir.glob("*/*/" + AGENT_SOURCE_NAME)):
        rel = source.parent.relative_to(agents_dir)
        groups[str(source)] = list(rel.parts[:-1])
    return groups


def discover_agents(
    root: Path, only: list[str] | None = None, agents: list[str] | None = None
) -> list[Path]:
    """All canonical agent sources: knowledge/agents/<category>/<name>/.

    ``only`` keeps agents whose path under ``knowledge/agents`` contains one of
    the given category tokens (matched against every path segment). ``agents``
    keeps agents whose directory name matches one of the given fnmatch globs.
    Both filters are OR-ed within their own list and AND-ed with each other; an
    empty filter is no filter. ``--skills`` never narrows agents.
    """
    groups = _agent_groups(root)
    found: list[Path] = []
    for source_str, segments in groups.items():
        if only and not any(token in segments for token in only):
            continue
        if agents and not any(
            fnmatch.fnmatch(Path(source_str).parent.name, pat) for pat in agents
        ):
            continue
        found.append(Path(source_str))
    return found


def _agent_meta(source: Path) -> dict[str, object]:
    """Parse name/description/body from a canonical agent source."""
    from engine.frontmatter import parse

    doc = parse(source.read_text(encoding="utf-8"))
    return {
        "name": str(doc.meta.get("name", "")).strip(),
        "description": str(doc.meta.get("description", "")).strip(),
        "body": doc.body.strip(),
    }


SAFE_NAME = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


def _safe_agent_name(source: Path) -> str:
    """The agent name, guaranteed usable as a filename (defense in depth).

    The validator rejects non-kebab names, but the installer must not trust a
    source it may be pointed at directly: a name like ``../../x`` would escape
    ``agents_dir``. Raise rather than write outside the plan.
    """
    name = str(_agent_meta(source)["name"])
    if not SAFE_NAME.match(name):
        raise ValueError(
            f"{source}: agent name {name!r} is not kebab-case; refusing to install"
        )
    return name


def _allowed_roots(config_dir: Path) -> list[Path]:
    """Roots the installer legitimately writes under.

    ``config_dir`` for the harness's own files, plus ``<config_dir>/../.agents``
    for the shared ``~/.agents/skills`` tree Codex and Cursor scan.
    """
    return [config_dir, config_dir.parent / ".agents"]


def _assert_contained(targets: list[tuple[Path, FileContent]], config_dir: Path) -> None:
    """Refuse to write anywhere outside the allowed roots (traversal guard)."""
    roots = [r.resolve() for r in _allowed_roots(config_dir)]
    for target, _ in targets:
        resolved = target.resolve()
        if not any(_is_within(resolved, r) for r in roots):
            raise ValueError(
                f"refusing to install outside {config_dir}: {target} resolves to {resolved}"
            )


def _is_within(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
    except ValueError:
        return False
    return True


def _yaml_scalar(text: str) -> str:
    """Render ``text`` as a YAML scalar safe for arbitrary content.

    A plain (unquoted) scalar is only valid while it contains no indicator
    characters: a description such as ``frames ... data products: dual`` breaks
    the mapping at the internal ``": "``. Emit a double-quoted JSON string
    instead — JSON string syntax is a valid subset of YAML double-quoted
    scalars, so the value round-trips whatever it contains.
    """
    return json.dumps(text)


def _render_agent_opencode(source: Path, root: Path) -> str:
    """OpenCode agent markdown: frontmatter description + mode, body as prompt."""
    meta = _agent_meta(source)
    try:
        rel = source.relative_to(root).as_posix()
    except ValueError:
        rel = source.as_posix()
    return (
        "---\n"
        f"description: {_yaml_scalar(str(meta['description']))}\n"
        "mode: subagent\n"
        "---\n\n"
        f"<!-- Generated from {rel} (Coacus) -->\n\n"
        f"{meta['body']}\n"
    )


def _render_agent_named(source: Path) -> str:
    """Agent markdown with name+description frontmatter and an H1 body.

    Shared by antigravity, Claude Code and Cursor, whose agent files carry the
    name in frontmatter (OpenCode derives it from the filename instead).
    """
    meta = _agent_meta(source)
    body = meta["body"]
    first = body.lstrip().splitlines()[:1]
    if not first or not first[0].startswith("# "):
        body = f"# {meta['name']}\n\n{body}"
    return (
        "---\n"
        f"name: {meta['name']}\n"
        f"description: {_yaml_scalar(str(meta['description']))}\n"
        "---\n\n"
        f"{body}\n"
    )


def _render_agent_codex(source: Path) -> str:
    """Codex agent role TOML: name/description + developer_instructions."""
    meta = _agent_meta(source)
    # TOML basic multiline string: escape backslashes and triple quotes.
    body = meta["body"].replace("\\", "\\\\").replace('"""', '\\"\\"\\"')
    description = str(meta["description"]).replace("\\", "\\\\").replace('"', '\\"')
    return (
        f'name = "{meta["name"]}"\n'
        f'description = "{description}"\n'
        'developer_instructions = """\n'
        f"{body}\n"
        '"""\n'
    )


def _plan_agents_opencode(
    root: Path, agents_dir: Path, only: list[str] | None = None, agents: list[str] | None = None
) -> list[tuple[Path, FileContent]]:
    plan: list[tuple[Path, FileContent]] = []
    for source in discover_agents(root, only=only, agents=agents):
        name = _safe_agent_name(source)
        plan.append((agents_dir / f"{name}.md", _render_agent_opencode(source, root)))
    return plan


def _plan_agents_antigravity(
    root: Path, agents_dir: Path, only: list[str] | None = None, agents: list[str] | None = None
) -> list[tuple[Path, FileContent]]:
    plan: list[tuple[Path, FileContent]] = []
    for source in discover_agents(root, only=only, agents=agents):
        name = _safe_agent_name(source)
        plan.append((agents_dir / name / "agent.md", _render_agent_named(source)))
    return plan


def _render_antigravity_agent_stub(source: Path) -> str:
    """Render a native agent selector whose full canonical prompt loads by MCP."""
    meta = _agent_meta(source)
    return (
        "---\n"
        f"name: {meta['name']}\n"
        f"description: {_yaml_scalar(str(meta['description']))}\n"
        "---\n\n"
        f"# {meta['name']}\n\n"
        "Load this role's complete canonical instructions with the `get` tool "
        "from the `coacus-catalog` MCP server, using `kind: agent` and this "
        f"name: `{meta['name']}`. Load each name in the returned "
        "`associated_skills` list with the same tool and `kind: skill`. Follow "
        "those instructions and use the host's native tools for the task.\n"
    )


def _antigravity_catalog_files(
    root: Path,
    plugin: Path,
    only: list[str] | None,
    skills: list[str] | None,
    agents: list[str] | None,
) -> list[tuple[Path, FileContent]]:
    """Install all selected canonical sources as data, outside native scan roots."""
    from engine.frontmatter import parse

    plan: list[tuple[Path, FileContent]] = []
    entries: dict[str, list[dict[str, object]]] = {"skills": [], "agents": []}
    skill_names_by_source: dict[str, str] = {}

    selected_skills = discover_skills(root, only=only, skills=skills)
    for skill in selected_skills:
        source = skill / "SKILL.md"
        doc = parse(source.read_text(encoding="utf-8"))
        meta = doc.meta
        name = str(meta.get("name") or skill.name)
        source_rel = source.relative_to(root).as_posix()
        if source_rel.startswith("knowledge/skills/"):
            category = "/".join(source.relative_to(root / "knowledge/skills").parts[:-2])
        else:
            category = "workflows"
        payload_rel = f"catalog/corpus/{source_rel}"
        entries["skills"].append(
            {
                "name": name,
                "kind": "skill",
                "category": category,
                "description": str(meta.get("description") or ""),
                "source": source_rel,
                "payload": payload_rel,
                "fingerprint": hashlib.sha256(source.read_bytes()).hexdigest(),
            }
        )
        skill_names_by_source[source_rel] = name
        for companion in _skill_files(skill):
            relative = companion.relative_to(root).as_posix()
            plan.append((plugin / "catalog" / "corpus" / relative, _read_source(companion)))

    selected_agents = discover_agents(root, only=only, agents=agents)
    for source in selected_agents:
        meta = _agent_meta(source)
        name = str(meta["name"])
        source_rel = source.relative_to(root).as_posix()
        skill_paths = meta.get("skills", [])
        if not isinstance(skill_paths, list):
            skill_paths = []
        associated_skills = sorted(
            {
                skill_names_by_source[str(path)]
                for path in skill_paths
                if str(path) in skill_names_by_source
            }
        )
        payload_rel = f"catalog/corpus/{source_rel}"
        entries["agents"].append(
            {
                "name": name,
                "kind": "agent",
                "category": str(source.relative_to(root / "knowledge/agents").parts[0]),
                "description": str(meta["description"]),
                "source": source_rel,
                "payload": payload_rel,
                "fingerprint": hashlib.sha256(source.read_bytes()).hexdigest(),
                "skills": associated_skills,
            }
        )
        agent_root = source.parent
        for companion in sorted(agent_root.rglob("*")):
            if (
                companion.is_file()
                and not companion.is_symlink()
                and "__pycache__" not in companion.relative_to(agent_root).parts
                and "dist" not in companion.relative_to(agent_root).parts
                and companion.suffix not in {".pyc", ".pyo"}
            ):
                relative = companion.relative_to(root).as_posix()
                plan.append((plugin / "catalog" / "corpus" / relative, _read_source(companion)))
        plan.append(
            (plugin / "agents" / name / "agent.md", _render_antigravity_agent_stub(source))
        )

    index = {"schema": 1, "skills": entries["skills"], "agents": entries["agents"]}
    plan.append((plugin / "catalog" / "index.json", json.dumps(index, indent=2) + "\n"))
    return plan


def _antigravity_catalog_mcp_config(root: Path, plugin: Path) -> str:
    """Render Antigravity's official MCP schema with installed paths resolved."""
    from engine.frontmatter import parse

    source = root / "knowledge" / "mcps" / "coacus-catalog" / "MCP.md"
    if not source.is_file():
        raise FileNotFoundError(f"canonical MCP source is missing: {source}")
    meta = parse(source.read_text(encoding="utf-8")).meta
    name = str(meta.get("name") or "coacus-catalog")
    executable = getattr(sys, "_base_executable", None) or sys.executable
    server = plugin / "coacus_catalog_mcp.py"
    return json.dumps(
        {"mcpServers": {name: {"command": executable, "args": [str(server.resolve())]}}},
        indent=2,
    ) + "\n"


def _plan_agents_codex(
    root: Path, agents_dir: Path, only: list[str] | None = None, agents: list[str] | None = None
) -> list[tuple[Path, FileContent]]:
    plan: list[tuple[Path, FileContent]] = []
    for source in discover_agents(root, only=only, agents=agents):
        name = _safe_agent_name(source)
        plan.append((agents_dir / f"{name}.toml", _render_agent_codex(source)))
    return plan


def _plan_agents_named(
    root: Path, agents_dir: Path, only: list[str] | None = None, agents: list[str] | None = None
) -> list[tuple[Path, FileContent]]:
    """Agent markdown (name+description) for Claude Code and Cursor."""
    plan: list[tuple[Path, FileContent]] = []
    for source in discover_agents(root, only=only, agents=agents):
        name = _safe_agent_name(source)
        plan.append((agents_dir / f"{name}.md", _render_agent_named(source)))
    return plan


def _render_agent_command_code(source: Path) -> str:
    """Command Code agent markdown: name + description + tools, body as prompt.

    Command Code reads ``name`` and ``description`` from the frontmatter (it does
    not derive the name from the filename), and matching is done against the
    description. An omitted ``tools`` grants the agent **no** tools at all, so
    ``tools: "*"`` is required for an installed agent to be usable; the ``agent``
    tool is never grantable, which keeps delegation one level deep.
    """
    meta = _agent_meta(source)
    body = meta["body"]
    first = body.lstrip().splitlines()[:1]
    if not first or not first[0].startswith("# "):
        body = f"# {meta['name']}\n\n{body}"
    return (
        "---\n"
        f"name: {meta['name']}\n"
        f"description: {_yaml_scalar(str(meta['description']))}\n"
        'tools: "*"\n'
        "---\n\n"
        f"{body}\n"
    )


# Command Code ignores a custom agent file whose name is one of its reserved
# built-ins, so writing those would be a silent no-op.
COMMAND_CODE_RESERVED = frozenset({"explore", "plan", "review", "general"})


def _plan_agents_command_code(
    root: Path, agents_dir: Path, only: list[str] | None = None, agents: list[str] | None = None
) -> list[tuple[Path, FileContent]]:
    """Agent markdown for Command Code, skipping names the harness reserves."""
    plan: list[tuple[Path, FileContent]] = []
    for source in discover_agents(root, only=only, agents=agents):
        name = _safe_agent_name(source)
        if name in COMMAND_CODE_RESERVED:
            continue
        plan.append((agents_dir / f"{name}.md", _render_agent_command_code(source)))
    return plan


def _skill_files(skill_dir: Path) -> list[Path]:
    """Every file belonging to a skill, so companions (references/) travel too.

    Symlinks are skipped: a link inside a skill tree must not point the installer
    at an arbitrary file outside the repository.
    """
    return sorted(
        p for p in skill_dir.rglob("*")
        if p.is_file() and not p.is_symlink()
        and "__pycache__" not in p.relative_to(skill_dir).parts
        and p.suffix not in {".pyc", ".pyo"}
    )


def _substitute_json(text: str, placeholder: str, value: str) -> str:
    """Replace ``placeholder`` inside every string of a JSON document.

    A naive ``str.replace`` corrupts the JSON (and can inject) when the value
    contains a quote or backslash. Parse, substitute, re-serialize instead.
    """
    def walk(node: object) -> object:
        if isinstance(node, str):
            return node.replace(placeholder, value)
        if isinstance(node, dict):
            return {k: walk(v) for k, v in node.items()}
        if isinstance(node, list):
            return [walk(item) for item in node]
        return node

    return json.dumps(walk(json.loads(text)), indent=2) + "\n"


def _hook_owner_markers(root: Path, harness: str) -> set[str]:
    """Substrings identifying Coacus-owned hook entries in a shared hooks.json.

    A SET, not one marker: the installer now owns two kinds of hook entry (the
    SessionStart bootstrap and the guardrail). One marker would let a re-install
    of one subsystem delete the other's entry, and ``--uninstall`` would leave a
    stale guardrail behind.
    """
    base = f"{root.as_posix()}/harnesses/{harness}/bootstrap"
    return {
        f"{base}/session-start.sh", f"{base}/coacus-guard.sh",
        # Legacy wrappers may refer to a retired checkout. Their harness
        # namespace identifies ownership independently of that checkout root.
        f"/harnesses/{harness}/bootstrap/session-start.sh",
        f"/harnesses/{harness}/bootstrap/coacus-guard.sh",
        f"{base}/session-start.json", f"{base}/coacus-guardrails.js",
        "/scripts/coacus_session_start.py",
        "/coacus/coacus-guard.sh", "${CLAUDE_PLUGIN_ROOT:-.}/bootstrap/session-start.sh",
        f"--harness {harness} --event tool.pre",
    }


def _command(argv: list[str]) -> str:
    """Quote arguments for the host's command parser, including the interpreter."""
    if os.name != "nt":
        return shlex.join(argv)
    # cmd.exe expands %VAR% even inside quotes, and CRT quoting alone leaves
    # ampersands unquoted. Keep dynamic script paths/arguments out of the shell.
    interpreter = argv[0]
    if any(char in interpreter for char in '%!"\r\n'):
        raise ValueError("Windows hook interpreter path contains unsupported shell expansion characters")
    encoded = base64.b64encode(json.dumps(argv[1:]).encode("utf-8")).decode("ascii")
    shim = ("import base64,json,runpy,sys;"
            f"sys.argv=json.loads(base64.b64decode('{encoded}'));"
            "runpy.run_path(sys.argv[0],run_name='__main__')")
    return f'"{interpreter}" -c "{shim}"'


def _hook_substitute(text: str, root: Path, plugin: Path | None = None) -> str:
    """Resolve templates as arguments before quoting the installed command."""
    replacements = {
        "__COACUS_ROOT__": root.as_posix(),
        "__COACUS_PYTHON__": sys.executable,
    }
    if plugin is not None:
        replacements["__COACUS_PLUGIN_ROOT__"] = plugin.as_posix()
        # Existing plugin manifests used POSIX variable expansion.
        replacements["${CLAUDE_PLUGIN_ROOT:-.}"] = plugin.as_posix()

    def replace(value: str) -> str:
        for key, replacement in replacements.items():
            value = value.replace(key, replacement)
        return value

    def walk(value, key: str = ""):
        if isinstance(value, dict):
            return {k: walk(v, k) for k, v in value.items()}
        if isinstance(value, list):
            return [walk(v) for v in value]
        if isinstance(value, str):
            if key == "command":
                return _command([replace(arg) for arg in shlex.split(value)])
            return replace(value)
        return value

    return json.dumps(walk(json.loads(text)), indent=2) + "\n"


def _plugin_substitute(text: str, root: Path) -> str:
    """Embed paths as JavaScript string literals without shell interpolation."""
    for placeholder, value in (("__COACUS_ROOT__", root.as_posix()),
                               ("__COACUS_PYTHON__", sys.executable)):
        text = text.replace(json.dumps(placeholder), json.dumps(value))
        text = text.replace("'" + placeholder + "'", json.dumps(value))
        text = text.replace(placeholder, value)
    return text


def _entry_owned(entry: object, markers: set[str]) -> bool:
    """True if a hook entry references any Coacus script (by our markers)."""
    blob = json.dumps(entry)
    for encoded in re.findall(r"b64decode\('([A-Za-z0-9+/=]+)'\)", blob):
        try:
            decoded = json.loads(base64.b64decode(encoded, validate=True))
            if isinstance(decoded, list) and all(isinstance(arg, str) for arg in decoded):
                blob += " ".join(decoded)
        except (ValueError, UnicodeDecodeError):
            continue
    for marker in markers:
        if marker not in blob:
            continue
        if marker.startswith("/harnesses/") and marker.endswith("/session-start.sh"):
            # This generic filename also exists in other products. A retired
            # checkout must retain a Coacus-named path component as evidence.
            owner = r'/[^/"\\]*\bcoacus\b[^/"\\]*' + re.escape(marker)
            if re.search(owner, blob, flags=re.IGNORECASE):
                return True
        else:
            return True
    return False


def _hook_owner_marker(root: Path, harness: str) -> str:
    """Back-compat single marker for legacy callers."""
    return f"{root.as_posix()}/harnesses/{harness}/bootstrap/session-start.json"


def _load_existing_json(path: Path) -> dict:
    """Read an existing JSON object, or {} when absent/unreadable."""
    if not path.is_file():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return data if isinstance(data, dict) else {}


def _merge_hooks(existing: dict, fragment: dict, markers: set[str]) -> dict:
    """Merge our hook entries into the user's hooks.json, preserving theirs.

    For each event we drop any prior Coacus entry (identified by ANY marker in
    ``markers``) and append ours. Every other key and event is left untouched, so
    installing does not rewrite a harness config file wholesale, and a re-install
    of one Coacus subsystem does not clobber the other.
    """
    merged = dict(existing) if isinstance(existing, dict) else {}
    merged_hooks = dict(merged.get("hooks", {})) if isinstance(merged.get("hooks"), dict) else {}
    for event, entries in (fragment.get("hooks") or {}).items():
        kept = [e for e in merged_hooks.get(event, []) if not _entry_owned(e, markers)]
        merged_hooks[event] = kept + list(entries)
    merged["hooks"] = merged_hooks
    return merged


def _strip_hooks(existing: dict, markers: set[str]) -> dict | None:
    """Remove Coacus hook entries from the user's hooks.json.

    Returns the trimmed document, or None when nothing but Coacus remained (the
    file may then be deleted). Other keys and events are preserved.
    """
    if not isinstance(existing, dict) or not isinstance(existing.get("hooks"), dict):
        return existing if existing else None
    hooks = {}
    for event, entries in existing["hooks"].items():
        if not isinstance(entries, list):
            hooks[event] = entries
            continue
        kept = [e for e in entries if not _entry_owned(e, markers)]
        if kept:
            hooks[event] = kept
    trimmed = {k: v for k, v in existing.items() if k != "hooks"}
    if hooks:
        trimmed["hooks"] = hooks
    else:
        trimmed.pop("hooks", None)
    return trimmed or None


def _guardrail_artifacts(
    root: Path, harness: str, config_dir: Path
) -> tuple[list[tuple[Path, FileContent]], dict | None]:
    """Stage the guardrail script/plugin and return a hook fragment to merge.

    Returns ``(files, fragment)`` where ``fragment`` is the container-shaped hook
    config to merge into the user's file, or None for an in-process harness
    (opencode) whose guard is a plugin. A harness with no guardrail plugin or an
    unsupported lifecycle stages nothing.
    """
    manifest = root / "harnesses" / harness / "harness.json"
    if not manifest.is_file():
        return [], None
    try:
        data = json.loads(manifest.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return [], None
    if not any(p.get("kind") == "guardrail" for p in data.get("plugins", [])):
        return [], None
    if not data.get("lifecycle", {}).get("supported"):
        return [], None
    subst = lambda text: _hook_substitute(text, root)  # noqa: E731

    files: list[tuple[Path, FileContent]] = []
    if harness == "opencode":
        src = root / "harnesses/opencode/bootstrap/coacus-guardrails.js"
        if src.is_file():
            files.append((config_dir / "plugins" / "coacus-guardrails.js", _plugin_substitute(src.read_text(encoding="utf-8"), root)))
        return files, None

    frag_path = root / f"harnesses/{harness}/bootstrap/guardrail-hooks.json"
    fragment = None
    if frag_path.is_file():
        text = subst(frag_path.read_text(encoding="utf-8"))
        try:
            fragment = json.loads(text)
        except json.JSONDecodeError:
            fragment = None
    return files, fragment


def _refuse_unenforceable(
    root: Path, harness: str, extra_docs: list[dict] | None = None
) -> list[str]:
    """Return reasons the guardrail policy cannot be enforced on this harness.

    A ``deny`` policy bound to an event the harness cannot block would install as
    advisory while looking successful. Enforcement is refused, not degraded (D3).
    ``extra_docs`` are policy documents generated during this run (the browser
    policy) that are not on disk under the repository yet.
    """
    policy_dir = root / "methodology" / "lifecycle" / "policies"
    docs: list[dict] = list(extra_docs or [])
    if policy_dir.is_dir():
        for path in sorted(policy_dir.glob("*.policy.json")):
            try:
                docs.append(json.loads(path.read_text(encoding="utf-8")))
            except (OSError, json.JSONDecodeError):
                continue
    if not docs:
        return []
    manifest = root / "harnesses" / harness / "harness.json"
    try:
        data = json.loads(manifest.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return []
    lifecycle = data.get("lifecycle", {})
    reasons: list[str] = []
    for doc in docs:
        if doc.get("enabled") is not True:
            continue
        for policy in doc.get("policies", []):
            if policy.get("decision") != "deny":
                continue
            event = str(policy.get("event", "tool.pre"))
            cap = (lifecycle.get("events", {}) or {}).get(event)
            if not cap or not cap.get("can_block"):
                reasons.append(
                    f"policy {policy.get('id')!r} denies {event!r} but {harness} "
                    f"cannot block it (can_block=false)"
                )
    return reasons


def _mcp_servers(root: Path) -> dict[str, dict]:
    """Coacus MCP servers as ``{name: config}`` for a harness MCP config.

    Read from the generated ``knowledge/mcps/*/dist/mcp.json`` manifests. The
    transport is normalized to the values a harness config accepts: ``stdio``
    stays ``stdio``; every HTTP flavor (``http``, ``streamable-http``, ``sse``)
    maps to ``http``.
    """
    servers: dict[str, dict] = {}
    mcp_root = root / "knowledge" / "mcps"
    if not mcp_root.is_dir():
        return servers
    for manifest in sorted(mcp_root.glob("*/dist/mcp.json")):
        data = _load_existing_json(manifest)
        name = str(data.get("name") or manifest.parent.parent.name)
        if str(data.get("transport") or "").lower() == "stdio":
            entry: dict = {"transport": "stdio", "enabled": True}
            if data.get("command"):
                entry["command"] = data["command"]
            if data.get("args"):
                entry["args"] = data["args"]
        else:
            entry = {"transport": "http", "enabled": True}
            if data.get("url"):
                entry["url"] = data["url"]
        servers[name] = entry
    return servers


def _merge_mcp(existing: dict, servers: dict[str, dict]) -> dict:
    """Merge Coacus MCP servers into the user's MCP config, preserving theirs.

    Each Coacus server name is replaced wholesale; every other server and every
    top-level key is left untouched, so installing never rewrites a shared MCP
    config file (the same contract as the hook merge).
    """
    merged = dict(existing) if isinstance(existing, dict) else {}
    current = merged.get("mcpServers")
    current = dict(current) if isinstance(current, dict) else {}
    current.update(servers)
    if current:
        merged["mcpServers"] = current
    return merged


def _strip_mcp(existing: dict, names: set[str]) -> dict | None:
    """Remove the given Coacus MCP servers; return the trimmed document or None.

    Returns None when nothing but Coacus servers remained (the file may then be
    deleted). Other servers and every top-level key are preserved.
    """
    if not isinstance(existing, dict) or not isinstance(existing.get("mcpServers"), dict):
        return existing if existing else None
    servers = {
        key: value
        for key, value in existing["mcpServers"].items()
        if key not in names
    }
    trimmed = {key: value for key, value in existing.items() if key != "mcpServers"}
    if servers:
        trimmed["mcpServers"] = servers
    return trimmed or None


def _plan_skills(
    root: Path,
    skills_dir: Path,
    only: list[str] | None = None,
    skills: list[str] | None = None,
) -> list[tuple[Path, FileContent]]:
    """Mirror every selected skill tree (SKILL.md + references/examples/scripts)."""
    plan: list[tuple[Path, FileContent]] = []
    for skill in discover_skills(root, only=only, skills=skills):
        for source in _skill_files(skill):
            relative = source.relative_to(skill)
            target = skills_dir / skill.name / relative
            plan.append((target, _read_source(source)))
    notice = root / NOTICE_NAME
    if notice.is_file():
        plan.append((skills_dir / NOTICE_NAME, _read_source(notice)))
    return plan


def _plan_skills_links(
    root: Path,
    link_dir: Path,
    canonical_dir: Path,
    only: list[str] | None = None,
    skills: list[str] | None = None,
) -> list[tuple[Path, FileContent]]:
    """Symlink each selected skill from ``link_dir`` to the canonical copy.

    The real skill files are installed once under ``canonical_dir`` (the shared
    ``~/.agents/skills`` tree). A harness with its OWN skill home receives a
    symlink per skill here, so there is a single source of truth.
    """
    plan: list[tuple[Path, FileContent]] = []
    for skill in discover_skills(root, only=only, skills=skills):
        plan.append(
            (link_dir / skill.name, Symlink((canonical_dir / skill.name).as_posix()))
        )
    return plan


def _install_symlink(target: Path, destination: str) -> None:
    """Create ``target`` as a symlink to ``destination``, replacing a stale copy.

    A prior (copy-mode) install may have left a real skill directory in the way;
    it is removed so the link can take its place. Only a planned skill path is
    ever passed here, and containment was checked before writing.
    """
    if target.is_symlink() or target.exists():
        if target.is_dir() and not target.is_symlink():
            shutil.rmtree(target)
        else:
            target.unlink()
    os.symlink(destination, target)


# Harnesses that write the canonical shared skills tree (directly or via links).
CANONICAL_SKILLS_WRITERS = frozenset({"codex", "cursor", "command-code", "claude-code"})


def _canonical_skills_dir(config_dir: Path) -> Path:
    """The shared ``~/.agents/skills`` tree that holds the single real copy."""
    return config_dir.parent / ".agents" / "skills"


def _walk_chmod(path: Path, writable: bool) -> None:
    """Best-effort add/remove write bits on a tree, never following symlinks.

    Read-only skill directories make a consumer's own delete/update fail (it
    cannot empty a directory it cannot write), while this installer restores
    write access just before it needs to rewrite them.
    """
    if not path.exists():
        return
    targets = [path, *(p for p in path.rglob("*") if not p.is_symlink())] if path.is_dir() else [path]
    for item in targets:
        if item.is_symlink():
            continue
        try:
            mode = item.lstat().st_mode & 0o777
            new_mode = (mode | 0o222) if writable else (mode & ~0o222)
            if new_mode != mode:
                os.chmod(item, new_mode)
        except OSError:
            pass


def _lock_canonical_skills(files: list[tuple[Path, FileContent]], config_dir: Path) -> None:
    """Mark the canonical Coacus skill directories read-only after an install."""
    canonical = _canonical_skills_dir(config_dir)
    try:
        canonical_resolved = canonical.resolve()
    except OSError:
        return
    for target, content in files:
        if isinstance(content, Symlink) or target.name != "SKILL.md":
            continue
        try:
            if target.parent.resolve().is_relative_to(canonical_resolved):
                _walk_chmod(target.parent, writable=False)
        except OSError:
            pass


def _read_source(path: Path) -> FileContent:
    """Text for a UTF-8 file, raw bytes for a binary companion (e.g. an image)."""
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_bytes()


def _read_installed(path: Path, expected: FileContent) -> FileContent:
    """Read an installed file the same way its plan content was produced."""
    if isinstance(expected, bytes):
        return path.read_bytes()
    return path.read_text(encoding="utf-8")


def _plan_opencode(
    root: Path,
    config_dir: Path,
    only: list[str] | None = None,
    skills: list[str] | None = None,
    agents: list[str] | None = None,
) -> list[tuple[Path, FileContent]]:
    """Plugin + governor gate + mirrored skill trees for opencode."""
    source = root / "harnesses/opencode/bootstrap/coacus.js"
    content = _plugin_substitute(source.read_text(encoding="utf-8"), root)
    plan: list[tuple[Path, FileContent]] = [(config_dir / "plugins" / "coacus.js", content)]
    gate = root / "harnesses/opencode/bootstrap/governor-gate.js"
    if gate.is_file():
        plan.append(
            (
                config_dir / "plugins" / "coacus-governor.js",
                _plugin_substitute(gate.read_text(encoding="utf-8"), root),
            )
        )
    plan += _plan_skills(root, config_dir / "skills", only, skills)
    plan += _plan_agents_opencode(root, config_dir / "agent", only, agents)
    guard_files, _ = _guardrail_artifacts(root, "opencode", config_dir)
    plan += guard_files
    return plan


def _plan_claude(
    root: Path,
    config_dir: Path,
    only: list[str] | None = None,
    skills: list[str] | None = None,
    agents: list[str] | None = None,
    skills_mode: str = "link",
) -> list[tuple[Path, FileContent]]:
    """Skills + subagents + a hook plugin whose script matches hooks.json.

    ``skills_mode="link"`` (default) installs the real skill files once under the
    shared ``~/.agents/skills`` tree and symlinks them into ``~/.claude/skills``,
    so a consumer that scans both homes (Orca's skill list) sees a single copy.
    ``"copy"`` restores the previous per-harness copies.
    """
    if skills_mode == "link":
        canonical_skills = config_dir.parent / ".agents" / "skills"
        plan = _plan_skills(root, canonical_skills, only, skills)
        plan += _plan_skills_links(
            root, config_dir / "skills", canonical_skills, only, skills
        )
    else:
        plan = _plan_skills(root, config_dir / "skills", only, skills)
    # Claude Code subagents load from ~/.claude/agents/<name>.md.
    plan += _plan_agents_named(root, config_dir / "agents", only, agents)
    plugin = config_dir / "plugins" / "coacus"
    plan.append(
        (
            plugin / ".claude-plugin" / "plugin.json",
            json.dumps(
                {
                    "name": "coacus",
                    "description": "Coacus agentic framework bootstrap",
                    "version": "0.1.0",
                    "hooks": "./hooks/hooks.json",
                },
                indent=2,
            )
            + "\n",
        )
    )
    # hooks.json reads the payload from the staged bootstrap directory. The guardrail
    # fragment merges into the SAME plugin hooks.json.
    hooks_path = plugin / "hooks" / "hooks.json"
    bootstrap_fragment = json.loads(
        _hook_substitute((root / "harnesses/claude-code/bootstrap/hooks.json").read_text(encoding="utf-8"), root, plugin)
    )
    guard_files, guard_fragment = _guardrail_artifacts(root, "claude-code", config_dir)
    plan += guard_files
    markers = _hook_owner_markers(root, "claude-code")
    merged = _merge_hooks(bootstrap_fragment, {}, markers)
    if guard_fragment:
        merged = _merge_hooks(merged, guard_fragment, markers)
    plan.append((hooks_path, json.dumps(merged, indent=2) + "\n"))
    plan.append(
        (
            plugin / "bootstrap" / "session-start.json",
            (root / "harnesses/claude-code/bootstrap/session-start.json").read_text(
                encoding="utf-8"
            ),
        )
    )
    return plan


def _plan_antigravity(
    root: Path,
    config_dir: Path,
    only: list[str] | None = None,
    skills: list[str] | None = None,
    agents: list[str] | None = None,
    profile: str = "on-demand",
) -> list[tuple[Path, FileContent]]:
    """Plugin (manifest + rule + skills) under the global plugins dir.

    Antigravity activates plugins by directory placement (``~/.gemini/config/plugins/``
    globally or ``.agents/plugins/`` per workspace). Rules load from the plugin's
    ``rules/`` dir with ``activation: always_on``; no registry edit is required.
    """
    plugin = config_dir / "config" / "plugins" / "coacus"
    if profile not in {"full", "on-demand"}:
        raise ValueError("Antigravity profile must be 'full' or 'on-demand'")
    if profile == "on-demand":
        plan = _antigravity_catalog_files(root, plugin, only, skills, agents)
        plan.append((plugin / "coacus_catalog_mcp.py", _read_source(root / "scripts/coacus_catalog_mcp.py")))
        rule_source = root / "harnesses/antigravity/coacus-on-demand-rule.md"
        if not rule_source.is_file():
            raise FileNotFoundError(f"on-demand Antigravity rule is missing: {rule_source}")
        plan.append((plugin / "rules" / "coacus.md", _read_source(rule_source)))
        plan.append((plugin / "mcp_config.json", _antigravity_catalog_mcp_config(root, plugin)))
    else:
        plan = _plan_skills(root, plugin / "skills", only, skills)
        plan += _plan_agents_antigravity(root, plugin / "agents", only, agents)
        plan.append((plugin / "rules" / "coacus.md", _read_source(root / "harnesses/antigravity/bootstrap/coacus-rule.md")))
    for name in ("plugin.json",):
        source = root / "harnesses/antigravity/bootstrap" / name
        plan.append((plugin / name, _read_source(source)))
    # Merge the governor wiring and the guardrail fragment into ONE plugin
    # hooks.json (the file the harness reads), keyed by hook-set name.
    hooks_doc = json.loads(_antigravity_hooks_json(root))
    guard_files, guard_fragment = _guardrail_artifacts(root, "antigravity", config_dir)
    plan += guard_files
    if guard_fragment:
        hooks_doc.update(guard_fragment)
    if hooks_doc:
        plan.append((plugin / "hooks.json", json.dumps(hooks_doc, indent=2) + "\n"))
    return plan


def _antigravity_hooks_json(root: Path) -> str:
    """Antigravity plugin hooks.json wiring the governor hook to lifecycle events."""
    argv = [sys.executable, (root / "scripts/coacus_governor_hook.py").as_posix()]
    matcher = "invoke_subagent|manage_subagents|task"
    return (
        json.dumps(
            {
                "coacus-governor": {
                    "PreToolUse": [
                        {
                            "matcher": matcher,
                            "hooks": [{"type": "command", "command": _command(argv + ["pretool"])}],
                        }
                    ],
                    "PostToolUse": [
                        {
                            "matcher": matcher,
                            "hooks": [{"type": "command", "command": _command(argv + ["posttool"])}],
                        }
                    ],
                    "PreInvocation": [
                        {"type": "command", "command": _command(argv + ["preinv"])}
                    ],
                }
            },
            indent=2,
        )
        + "\n"
    )


def _plan_codex(
    root: Path,
    config_dir: Path,
    only: list[str] | None = None,
    skills: list[str] | None = None,
    agents: list[str] | None = None,
) -> list[tuple[Path, FileContent]]:
    """Skills to the documented scan root + the SessionStart hook.

    Codex scans ``.agents/skills`` (not ``~/.codex/skills``), and its hooks load
    from ``~/.codex/hooks.json``. The hook invokes the Python runner and generated
    payload in the repository; the runner resolves paths in the emitted context.
    """
    plan: list[tuple[Path, FileContent]] = []
    # Codex scans $HOME/.agents/skills, not $config_dir/.codex/skills.
    plan += _plan_skills(root, config_dir.parent / ".agents" / "skills", only, skills)
    # Codex agent roles live in $CODEX_HOME/agents/*.toml.
    plan += _plan_agents_codex(root, config_dir / "agents", only, agents)
    hooks = (root / "harnesses/codex/bootstrap/hooks.json").read_text(encoding="utf-8")
    fragment = json.loads(_hook_substitute(hooks, root))
    existing = _load_existing_json(config_dir / "hooks.json")
    guard_files, guard_fragment = _guardrail_artifacts(root, "codex", config_dir)
    plan += guard_files
    markers = _hook_owner_markers(root, "codex")
    merged = _merge_hooks(existing, fragment, markers)
    if guard_fragment:
        merged = _merge_hooks(merged, guard_fragment, markers)
    plan.append(
        (
            config_dir / "hooks.json",
            json.dumps(merged, indent=2) + "\n",
        )
    )
    return plan


def _plan_cursor(
    root: Path,
    config_dir: Path,
    only: list[str] | None = None,
    skills: list[str] | None = None,
    agents: list[str] | None = None,
) -> list[tuple[Path, FileContent]]:
    """Skills to a Cursor scan root + subagents + the sessionStart hook.

    Cursor hooks live at ``~/.cursor/hooks.json`` (user) or
    ``<project>/.cursor/hooks.json``; the output key is snake_case
    ``additional_context``. Subagents load from ``~/.cursor/agents/<name>.md``.
    Commands are repo-absolute.
    """
    plan: list[tuple[Path, FileContent]] = []
    plan += _plan_skills(root, config_dir.parent / ".agents" / "skills", only, skills)
    plan += _plan_agents_named(root, config_dir / "agents", only, agents)
    hooks = (root / "harnesses/cursor/bootstrap/hooks.json").read_text(encoding="utf-8")
    fragment = json.loads(_hook_substitute(hooks, root))
    existing = _load_existing_json(config_dir / "hooks.json")
    guard_files, guard_fragment = _guardrail_artifacts(root, "cursor", config_dir)
    plan += guard_files
    markers = _hook_owner_markers(root, "cursor")
    merged = _merge_hooks(existing, fragment, markers)
    if guard_fragment:
        merged = _merge_hooks(merged, guard_fragment, markers)
    plan.append(
        (
            config_dir / "hooks.json",
            json.dumps(merged, indent=2) + "\n",
        )
    )
    return plan


COMMAND_CODE_HOOKS_FILE = "settings.json"
COMMAND_CODE_MCP_FILE = "mcp.json"
COMMAND_CODE_RULES_FILE = "AGENTS.md"


def _plan_command_code(
    root: Path,
    config_dir: Path,
    only: list[str] | None = None,
    skills: list[str] | None = None,
    agents: list[str] | None = None,
) -> list[tuple[Path, FileContent]]:
    """Skills (shared tree) + agents + SessionStart hook + MCP for Command Code.

    Command Code discovers skills from ``~/.agents/skills/`` (a user scan root,
    shared with Codex and Cursor), agents from ``<config>/agents/<name>.md``,
    hooks from ``<config>/settings.json`` under the ``hooks`` key — it has no
    separate hooks.json — and MCP servers from ``<config>/mcp.json`` under
    ``mcpServers``. Both config files are MERGED into the user's file, never
    rewritten wholesale. The Coacus user rules (``<config>/AGENTS.md``) are
    provisioned separately by ``install`` because that file is user memory.
    """
    plan: list[tuple[Path, FileContent]] = []
    plan += _plan_skills(root, config_dir.parent / ".agents" / "skills", only, skills)
    plan += _plan_agents_command_code(root, config_dir / "agents", only, agents)
    hooks = (root / "harnesses/command-code/bootstrap/hooks.json").read_text(encoding="utf-8")
    fragment = json.loads(_hook_substitute(hooks, root))
    existing = _load_existing_json(config_dir / COMMAND_CODE_HOOKS_FILE)
    guard_files, guard_fragment = _guardrail_artifacts(root, "command-code", config_dir)
    plan += guard_files
    markers = _hook_owner_markers(root, "command-code")
    merged = _merge_hooks(existing, fragment, markers)
    if guard_fragment:
        merged = _merge_hooks(merged, guard_fragment, markers)
    plan.append(
        (
            config_dir / COMMAND_CODE_HOOKS_FILE,
            json.dumps(merged, indent=2) + "\n",
        )
    )
    servers = _mcp_servers(root)
    if servers:
        mcp_existing = _load_existing_json(config_dir / COMMAND_CODE_MCP_FILE)
        plan.append(
            (
                config_dir / COMMAND_CODE_MCP_FILE,
                json.dumps(_merge_mcp(mcp_existing, servers), indent=2) + "\n",
            )
        )
    return plan


def _provision_rules(harness: str, root: Path, config_dir: Path) -> Path | None:
    """Write the Coacus user rules for ``harness`` when the file is absent.

    The rules are user memory (``<config>/AGENTS.md``), so they are written only
    when the file does not already exist and are never overwritten or removed —
    a pre-existing memory file is the user's. Returns the path written, or None.
    """
    if harness != "command-code":
        return None
    source = root / "harnesses" / "command-code" / COMMAND_CODE_RULES_FILE
    target = config_dir / COMMAND_CODE_RULES_FILE
    if not source.is_file() or target.exists():
        return None
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(
        source.read_text(encoding="utf-8").replace("__COACUS_ROOT__", root.as_posix()),
        encoding="utf-8",
    )
    return target


def plan(
    harness: str,
    root: Path,
    config_dir: Path,
    only: list[str] | None = None,
    skills: list[str] | None = None,
    agents: list[str] | None = None,
    skills_mode: str = "link",
    antigravity_profile: str = "on-demand",
) -> list[tuple[Path, FileContent]]:
    """Compute the files to install for ``harness`` under the given filters.

    Returns ``(target, content)`` pairs; nothing is written. ``only`` selects by
    category across skills and agents; ``skills``/``agents`` narrow each tree by
    name glob. Shared by ``install``, ``verify`` and ``uninstall``.
    """
    if harness == "opencode":
        return _plan_opencode(root, config_dir, only, skills, agents)
    if harness == "claude-code":
        return _plan_claude(root, config_dir, only, skills, agents, skills_mode)
    if harness == "antigravity":
        return _plan_antigravity(root, config_dir, only, skills, agents, antigravity_profile)
    if harness == "codex":
        return _plan_codex(root, config_dir, only, skills, agents)
    if harness == "cursor":
        return _plan_cursor(root, config_dir, only, skills, agents)
    if harness == "command-code":
        return _plan_command_code(root, config_dir, only, skills, agents)
    return []


def _is_default_target(harness: str, config_dir: Path) -> bool:
    """True when ``config_dir`` is the harness's real default config location.

    An explicit ``--config-dir`` (or a test target) is an intentional choice and
    bypasses the presence gate; the default location does not.
    """
    try:
        return config_dir.resolve() == default_config_dir(harness, _home()).resolve()
    except OSError:
        return config_dir == default_config_dir(harness, _home())


def install(
    harness: str,
    root: Path,
    config_dir: Path,
    dry_run: bool,
    only: list[str] | None = None,
    skills: list[str] | None = None,
    agents: list[str] | None = None,
    allow_advisory: bool = False,
    force: bool = False,
    codex_skill_profile: str = "compact",
    skills_mode: str = "link",
    lock_skills: bool | None = None,
    extra_policy_docs: list[dict] | None = None,
    antigravity_profile: str = "on-demand",
) -> dict[str, object]:
    """Install a harness and write its manifest; report files written.

    With ``dry_run``, returns the plan without touching disk. Every target is
    containment-checked first, so an install never writes outside the allowed
    roots (see ``_assert_contained``). For ``command-code`` the user rules
    (``<config>/AGENTS.md``) are written only when absent and are not part of the
    manifest — a pre-existing memory file is left untouched.

    Enforcement is refused, not degraded (D3): a ``deny`` policy the harness
    cannot block aborts the install unless ``allow_advisory`` records the
    downgrade explicitly.

    Detection is a gate (D13): a harness that is not present on this machine is
    SKIPPED, never populated — unless ``force`` is set to provision ahead of the
    harness's own installation.
    """
    if not force and _is_default_target(harness, config_dir) and not harness_present(harness):
        return {
            "harness": harness,
            "skipped": True,
            "reason": "harness not detected on this machine (use --force to override)",
            "config_dir": config_dir.as_posix(),
            "files": [],
        }
    refusals = _refuse_unenforceable(root, harness, extra_policy_docs)
    if refusals and not allow_advisory:
        return {
            "harness": harness,
            "error": "guardrail enforcement refused; use --allow-advisory to downgrade",
            "refusals": refusals,
            "files": [],
        }
    files = plan(
        harness, root, config_dir, only, skills, agents, skills_mode, antigravity_profile
    )
    _assert_contained(files, config_dir)
    if lock_skills is None:
        # Default: protect the shared tree only at a harness's real install
        # location, never an explicit custom target (tests, staging).
        lock_skills = _is_default_target(harness, config_dir)
    codex_update = (
        _codex_config_update(root, config_dir, codex_skill_profile)
        if harness == "codex"
        else None
    )
    previous_manifest = config_dir / MANIFEST_NAME
    previous_files: list[str] = []
    if previous_manifest.is_file():
        try:
            previous_files = _parse_manifest(previous_manifest).get("files", [])
        except ValueError:
            pass
    rules_target = config_dir / COMMAND_CODE_RULES_FILE
    rules_source = root / "harnesses" / "command-code" / COMMAND_CODE_RULES_FILE
    rules_pending = (
        rules_source.is_file() and not rules_target.exists()
        if harness == "command-code"
        else False
    )
    if dry_run:
        return {
            "harness": harness,
            "files": [str(t) for t, _ in files],
            "rules": rules_target.as_posix() if rules_pending else None,
            "dry_run": True,
            "only": only or [],
            "skills": skills or [],
            "agents": agents or [],
            **({"codex_skill_profile": codex_skill_profile} if harness == "codex" else {}),
            **({"antigravity_profile": antigravity_profile} if harness == "antigravity" else {}),
        }
    if harness in CANONICAL_SKILLS_WRITERS:
        # A prior install may have left the shared tree read-only (see
        # _lock_canonical_skills); restore write access before rewriting it.
        _walk_chmod(_canonical_skills_dir(config_dir), writable=True)
    written: list[str] = []
    for target, content in files:
        target.parent.mkdir(parents=True, exist_ok=True)
        if isinstance(content, Symlink):
            _install_symlink(target, content.target)
        elif isinstance(content, bytes):
            target.write_bytes(content)
        else:
            target.write_text(content, encoding="utf-8")
        written.append(target.as_posix())
    if lock_skills and harness in CANONICAL_SKILLS_WRITERS:
        _lock_canonical_skills(files, config_dir)
    if codex_update is not None:
        updated_config, owned_block, conflicts, config_existed = codex_update
        _write_codex_config(config_dir, updated_config, config_existed)
    # A manifest proves ownership of these legacy wrappers. Remove only files
    # retired by this migration, never a similarly named unowned user file.
    planned = set(written)
    retired = {"session-start.sh", "coacus-guard.sh", "governor-hook.sh"}
    allowed = [directory.resolve() for directory in _allowed_roots(config_dir)]
    for old in previous_files:
        target = Path(old)
        canonical = target.as_posix()
        replacement = canonical + ".py" in planned
        if ((target.name in retired or replacement) and canonical not in planned
                and any(_is_within(target.resolve(), directory) for directory in allowed)
                and target.is_file()):
            target.unlink()
    # Antigravity profiles can replace hundreds of manifest-owned native
    # customization files with opaque catalog data. Remove only paths recorded
    # by the previous manifest and no longer planned; never sweep plugin dirs.
    if harness == "antigravity":
        for old in previous_files:
            target = Path(old)
            if (
                target.as_posix() not in planned
                and any(_is_within(target.resolve(), directory) for directory in allowed)
                and target.is_file()
            ):
                target.unlink()
                parent = target.parent
                while parent != config_dir and _is_within(parent.resolve(), config_dir.resolve()):
                    try:
                        parent.rmdir()
                    except OSError:
                        break
                    parent = parent.parent
    rules = _provision_rules(harness, root, config_dir)
    manifest = config_dir / MANIFEST_NAME
    manifest.write_text(
        json.dumps(
            {
                "harness": harness,
                "files": written,
                "only": only or [],
                "skills": skills or [],
                "agents": agents or [],
                "skills_mode": skills_mode,
                **(
                    {
                        "codex_skill_profile": codex_skill_profile,
                        "codex_profile_block": owned_block,
                        "codex_config_existed": config_existed,
                    }
                    if codex_update is not None
                    else {}
                ),
                **(
                    {"antigravity_profile": antigravity_profile}
                    if harness == "antigravity"
                    else {}
                ),
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    return {
        "harness": harness,
        "files": written,
        "rules": rules.as_posix() if rules else None,
        "manifest": manifest.as_posix(),
        "advisory_downgrades": refusals if (refusals and allow_advisory) else [],
        **(
            {"codex_skill_profile": codex_skill_profile,
             "codex_skill_conflicts": conflicts}
            if codex_update is not None else {}
        ),
        **({"antigravity_profile": antigravity_profile} if harness == "antigravity" else {}),
    }


def _classify(target: Path) -> str:
    """Bucket an installed file: skill, agent, hook or other.

    Classifies by the path the installer produces, so the counts reflect what
    actually landed on disk rather than a number inferred elsewhere.
    """
    name = target.name
    parent = target.parent.name
    if name == "SKILL.md":
        return "skill"
    if name == "agent.md" or parent in ("agent", "agents"):
        return "agent"
    if name in ("hooks.json", "settings.json", "guardrail-hooks.json",
                "coacus-guardrails.js",
                "coacus-governor.js"):
        return "hook"
    return "other"


def _agent_key(target: Path) -> str:
    """Stable identity for an installed agent file across both layouts.

    Antigravity nests ``<agents>/<name>/agent.md`` (identity = the directory);
    OpenCode, Claude Code, Cursor and Codex write flat ``<agents>/<name>.md``
    or ``.toml`` (identity = the file itself). Using ``parent`` for both would
    collapse every flat agent in one directory into a single count.
    """
    if target.name == "agent.md":
        return target.parent.as_posix()
    return target.as_posix()


def _component_counts(files: list[tuple[Path, FileContent]]) -> dict[str, int]:
    """Distinct skills/agents plus hook/other file counts, from a plan.

    Symlink entries are excluded: they point at a canonical copy already counted
    once, so including them would double-count every shared skill.
    """
    real = [(t, c) for t, c in files if not isinstance(c, Symlink)]
    skills = {t.parent.as_posix() for t, _ in real if t.name == "SKILL.md"}
    agents = {_agent_key(t) for t, _ in real if _classify(t) == "agent"}
    hooks = [t for t, _ in real if _classify(t) == "hook"]
    other = [t for t, _ in real if _classify(t) == "other"]
    catalog_skills = 0
    catalog_agents = 0
    for target, content in real:
        if target.name != "index.json" or target.parent.name != "catalog" or not isinstance(content, str):
            continue
        try:
            index = json.loads(content)
        except json.JSONDecodeError:
            continue
        catalog_skills = len(index.get("skills", []))
        catalog_agents = len(index.get("agents", []))
    return {
        "skills": len(skills),
        "agents": len(agents),
        "hook_files": len(hooks),
        "other_files": len(other),
        "catalog_skills": catalog_skills,
        "catalog_agents": catalog_agents,
    }


def _installed_state(
    files: list[tuple[Path, FileContent]], harness: str, root: Path, config_dir: Path
) -> tuple[list[str], list[str]]:
    """Compute ``(missing, drifted)`` for a plan, honoring merged user files.

    A file Coacus MERGES into (a harness's ``hooks.json``/``settings.json``, an
    MCP config) is user-owned: the harness or the user may add keys after the
    install, so drift there means the Coacus entry is gone — not that the bytes
    differ. Every other file is compared verbatim.
    """
    hooks_path = _merged_config_path(harness, config_dir)
    markers = _hook_owner_markers(root, harness)
    mcp_path = _merged_mcp_path(harness, config_dir)
    mcp_names = set(_mcp_servers(root)) if mcp_path else set()
    missing: list[str] = []
    drift: list[str] = []
    for target, content in files:
        if isinstance(content, Symlink):
            if not target.is_symlink() or os.readlink(target) != content.target:
                drift.append(target.as_posix())
            continue
        if not target.is_file():
            missing.append(target.as_posix())
            continue
        if target == hooks_path:
            expected_hooks = json.loads(content).get("hooks", {})
            actual_hooks = _load_existing_json(target).get("hooks", {})
            expected_entries = [
                (event, entry) for event, entries in expected_hooks.items()
                for entry in entries if _entry_owned(entry, markers)
            ]
            if not expected_entries or any(
                entry not in actual_hooks.get(event, []) for event, entry in expected_entries
            ):
                drift.append(target.as_posix())
            continue
        if mcp_path is not None and target == mcp_path:
            servers = _load_existing_json(target).get("mcpServers") or {}
            if not any(name in servers for name in mcp_names):
                drift.append(target.as_posix())
            continue
        if _read_installed(target, content) != content:
            drift.append(target.as_posix())
    return missing, drift


def verify(harness: str, root: Path, config_dir: Path) -> dict[str, object]:
    """Compare an installed harness against the repository, read-only.

    Reports canonical component counts, the install root, and any file that is
    missing or has drifted from the repository. Exits non-zero (via the caller)
    when the harness is not installed or drift is found. The counts come from
    the plan the installer would write — never inferred — so a report can quote
    this output verbatim.
    """
    manifest = config_dir / MANIFEST_NAME
    result: dict[str, object] = {
        "harness": harness,
        "manifest": manifest.as_posix(),
        "installed": manifest.is_file(),
        "harness_present": harness_present(harness),
        "ok": False,
    }
    if not manifest.is_file():
        result["error"] = "no manifest — harness not installed (run install first)"
        return result
    try:
        data = _parse_manifest(manifest)
    except ValueError as exc:
        result["error"] = str(exc)
        return result
    only = data.get("only") or None
    skills = data.get("skills") or None
    agents = data.get("agents") or None
    antigravity_profile = data.get("antigravity_profile", "full")
    files = plan(
        harness, root, config_dir, only, skills, agents, data.get("skills_mode", "link"),
        antigravity_profile,
    )
    missing, drift = _installed_state(files, harness, root, config_dir)
    recorded = set(data.get("files", []))
    planned = {t.as_posix() for t, _ in files}
    result.update(
        {
            "install_root": config_dir.as_posix(),
            "only": only or [],
            "skills_filter": skills or [],
            "agents_filter": agents or [],
            "counts": _component_counts(files),
            "planned_files": len(files),
            "recorded_files": len(recorded),
            "missing": missing,
            "drifted": drift,
            "extra_in_manifest": sorted(recorded - planned),
        }
    )
    if harness == "antigravity":
        result["antigravity_profile"] = antigravity_profile
    result["ok"] = not missing and not drift and recorded == planned
    if harness == "codex":
        profile = data.get("codex_skill_profile", "legacy-full")
        result["codex_skill_profile"] = profile
        result["codex_config_drifted"] = False
        result["codex_skill_conflicts"] = []
        if profile != "legacy-full":
            try:
                config_path = config_dir / "config.toml"
                current = config_path.read_text(encoding="utf-8") if config_path.is_file() else ""
                _, actual_block = _strip_codex_profile(current)
                _, expected_block, conflicts, _ = _codex_config_update(root, config_dir, profile)
                result["codex_skill_conflicts"] = conflicts
                result["codex_config_drifted"] = (
                    actual_block != expected_block
                    or actual_block != data.get("codex_profile_block", "")
                )
            except (OSError, ValueError) as exc:
                result["codex_config_drifted"] = True
                result["codex_config_error"] = str(exc)
            result["ok"] = result["ok"] and not result["codex_config_drifted"]
    return result


def _parse_manifest(path: Path) -> dict:
    """Read an install manifest, raising a readable ValueError when malformed."""
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"{path}: unreadable install manifest ({exc})") from exc
    if not isinstance(data, dict):
        raise ValueError(f"{path}: install manifest must be a JSON object")
    return data


def _claimed_elsewhere(config_dir: Path, own_manifest: Path) -> set[str]:
    """Files another Coacus install manifest still claims.

    Codex and Cursor both mirror skills to ``<home>/.agents/skills``, so their
    manifests overlap. Uninstalling one must not delete files the other still
    needs. We scan sibling config dirs for other manifests.
    """
    claimed: set[str] = set()
    parent = config_dir.parent
    for manifest in parent.glob("*/coacus-install.json"):
        if manifest.resolve() == own_manifest.resolve():
            continue
        try:
            data = _parse_manifest(manifest)
        except ValueError:
            continue
        claimed.update(str(p) for p in data.get("files", []))
    return claimed


def _merged_config_path(harness: str, config_dir: Path) -> Path:
    """The user config file Coacus merges its hook entry into for ``harness``.

    Most harnesses keep hooks in ``hooks.json``; Command Code keeps them in its
    ``settings.json`` (key ``hooks``), so the uninstall strip must target that.
    """
    if harness == "command-code":
        return config_dir / COMMAND_CODE_HOOKS_FILE
    return config_dir / "hooks.json"


def _merged_mcp_path(harness: str, config_dir: Path) -> Path | None:
    """The user MCP config Coacus merges into, or None when it installs none."""
    if harness == "command-code":
        return config_dir / COMMAND_CODE_MCP_FILE
    return None


def uninstall(
    harness: str,
    root: Path,
    config_dir: Path,
    dry_run: bool = False,
) -> dict[str, object]:
    """Remove the recorded install, staying inside the allowed roots.

    Deletion is gated on containment under ``config_dir`` or the shared
    ``<config_dir>/../.agents`` tree — not on membership in a freshly re-derived
    plan, which would orphan a file whose repository source was deleted after
    install. Files still claimed by another harness's manifest (the shared
    ``.agents/skills`` tree) are skipped, so uninstalling Codex does not break
    Cursor. A path recorded by a doctored manifest but outside the allowed roots
    is skipped, so the manifest cannot delete arbitrary files.
    """
    manifest = config_dir / MANIFEST_NAME
    if not manifest.is_file():
        return {"harness": harness, "removed": [], "skipped": [], "note": "no manifest"}
    try:
        data = _parse_manifest(manifest)
    except ValueError as exc:
        return {"harness": harness, "removed": [], "skipped": [], "error": str(exc)}

    roots = [r.resolve() for r in _allowed_roots(config_dir)]
    if not dry_run and harness in CANONICAL_SKILLS_WRITERS:
        # Restore write access so the shared tree can be emptied on uninstall.
        _walk_chmod(_canonical_skills_dir(config_dir), writable=True)
    if harness == "codex" and not dry_run and "codex_skill_profile" in data:
        config_path = config_dir / "config.toml"
        if config_path.is_file():
            base, _ = _strip_codex_profile(config_path.read_text(encoding="utf-8"))
            if not base and not data.get("codex_config_existed", True):
                config_path.unlink()
            else:
                _write_codex_config(config_dir, base, True)
    shared = _claimed_elsewhere(config_dir, manifest)
    planned: list[str] = []
    skipped: list[str] = []
    hooks_path = _merged_config_path(harness, config_dir)
    markers = _hook_owner_markers(root, harness)
    existing_hooks = _load_existing_json(hooks_path) if hooks_path.is_file() else {}
    had_hooks_entry = any(marker in json.dumps(existing_hooks) for marker in markers)
    mcp_path = _merged_mcp_path(harness, config_dir)
    mcp_names = set(_mcp_servers(root)) if mcp_path else set()
    mcp_existing = (
        _load_existing_json(mcp_path) if (mcp_path and mcp_path.is_file()) else {}
    )
    had_mcp_entry = bool(mcp_names) and any(
        name in (mcp_existing.get("mcpServers") or {}) for name in mcp_names
    )
    for path in data.get("files", []):
        target = Path(path)
        if not any(_is_within(target.resolve(), r) for r in roots):
            skipped.append(path)
            continue
        if path in shared:
            skipped.append(path)
            continue
        if target.is_symlink():
            # A linked skill lives once in the canonical tree; removing our link
            # here leaves the real copy (claimed by the shared tree) intact.
            if not dry_run:
                target.unlink()
            planned.append(path)
            continue
        if not dry_run and target == hooks_path and had_hooks_entry:
            # hooks.json / settings.json is a user file we merged into; strip only
            # our entries and never delete the user's other keys.
            trimmed = _strip_hooks(_load_existing_json(hooks_path), markers)
            if trimmed is None:
                target.unlink()
            else:
                target.write_text(json.dumps(trimmed, indent=2) + "\n", encoding="utf-8")
            planned.append(path)
            continue
        if not dry_run and mcp_path and target == mcp_path and had_mcp_entry:
            # mcp.json is a user file we merged into; strip only our servers.
            trimmed_mcp = _strip_mcp(_load_existing_json(mcp_path), mcp_names)
            if trimmed_mcp is None:
                target.unlink()
            else:
                target.write_text(json.dumps(trimmed_mcp, indent=2) + "\n", encoding="utf-8")
            planned.append(path)
            continue
        if target.is_file():
            if not dry_run:
                target.unlink()
            planned.append(path)
    if not dry_run:
        _prune_empty_dirs([str(p) for p in data.get("files", [])], roots)
        manifest.unlink()
    return {"harness": harness, "removed": planned, "skipped": skipped, "dry_run": dry_run}


def _prune_empty_dirs(paths: list[str], roots: list[Path]) -> None:
    """Remove now-empty directories created for ``paths``, deepest first.

    Every ancestor of a recorded file that lies STRICTLY BELOW an allowed root is
    a candidate (the root itself is never removed). Only empty directories are
    removed, so unrelated user directories and anything still holding a file are
    left untouched.

    The earlier stop condition treated the config dir as the boundary, but a
    skill lives several levels below it (``<config>/skills/<skill>/``), so every
    ancestor was already "within the root" and nothing was ever pruned — leaving
    empty companion directories behind on uninstall.
    """
    candidates: set[Path] = set()
    for raw in paths:
        parent = Path(raw).parent
        while parent != parent.parent:
            if any(parent == r for r in roots):
                break  # never remove an allowed root itself
            if not any(_is_within(parent, r) for r in roots):
                break  # outside every root: stop
            candidates.add(parent)
            parent = parent.parent
    for directory in sorted(candidates, key=lambda p: len(p.parts), reverse=True):
        try:
            directory.rmdir()
        except OSError:
            pass  # not empty or already gone


def _browser_policy_dir(config_dir_arg: str | None, explicit: str | None) -> Path:
    """Where the generated browser policy lives.

    An explicit ``--browser-policy-dir`` wins; a custom ``--config-dir`` (staging,
    tests) keeps the policy beside it instead of touching the real user config;
    otherwise the runtime guard's user policy directory is used.
    """
    from engine.guardrail import evaluate

    if explicit:
        return Path(explicit).expanduser()
    if config_dir_arg:
        return Path(config_dir_arg) / "coacus-policies"
    return evaluate.user_policy_dir()


def browser_policy_step(
    root: Path,
    mode: str,
    policy_dir: Path,
    primary: str | None = None,
    fallback: str | None = None,
    dry_run: bool = False,
    ask=input,
    say=print,
) -> dict[str, object]:
    """Detect installed browsers, choose primary/fallback and write the policy.

    ``mode`` is ``off`` (do nothing), ``auto`` (preference order, no fallback),
    ``prompt`` (interactive) or ``select`` (explicit ``primary``/``fallback``).
    The generated policy is machine-local (D2: opt-in, never changes behaviour
    unasked) and is returned alongside a summary so the installer can check it
    can be enforced on each harness before writing anything.
    """
    from engine.guardrail import browsers

    summary: dict[str, object] = {"mode": mode, "status": "off", "policy_dir": policy_dir.as_posix()}
    if mode == "off":
        return summary
    catalog = browsers.load_catalog(root)
    detected = browsers.detect(catalog)
    summary["detected"] = [entry["id"] for entry in detected]
    try:
        if mode == "prompt":
            selection = browsers.prompt_selection(catalog, detected, ask=ask, say=say)
            if selection is None:
                summary["status"] = "skipped"
                return summary
        else:
            selection = browsers.choose(catalog, detected, primary=primary, fallback=fallback)
    except ValueError as exc:
        summary.update(status="error", error=str(exc))
        return summary
    document = browsers.build_policy(catalog, selection)
    summary.update(selection=selection, policies=len(document["policies"]), document=document)
    if dry_run:
        summary["status"] = "dry-run"
        return summary
    summary["policy_file"] = browsers.write_policy(policy_dir, document).as_posix()
    summary["status"] = "written"
    return summary


def main(argv: list[str] | None = None, root: Path | None = None) -> int:
    """Parse arguments and run install, uninstall, verify or list."""
    parser = argparse.ArgumentParser(prog="coacus-install", description=__doc__)
    parser.add_argument(
        "harness",
        nargs="?",
        choices=["opencode", "claude-code", "antigravity", "codex", "cursor", "command-code", "all"],
        help="harness to install into (omit with --list)",
    )
    parser.add_argument("--config-dir", help="override the harness config directory")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--uninstall", action="store_true")
    parser.add_argument(
        "--only",
        help="comma-separated categories to install (e.g. security,engineering)",
    )
    parser.add_argument(
        "--skills",
        help="comma-separated skill name globs to install (e.g. 'lang-*,framework-*')",
    )
    parser.add_argument(
        "--agents",
        help="comma-separated agent name globs to install (e.g. 'qa-*,*-architect')",
    )
    parser.add_argument(
        "--codex-skill-profile",
        choices=["compact", "full"],
        help="Codex native skill visibility (default: compact; full restores legacy behavior)",
    )
    parser.add_argument(
        "--antigravity-profile",
        choices=["on-demand", "full"],
        default="on-demand",
        help="Antigravity catalog activation (default: on-demand; full installs all native entries)",
    )
    parser.add_argument(
        "--skills-mode",
        choices=["link", "copy"],
        default=None,
        help="Skills strategy for harnesses with their own skill home (default: link — "
        "install once in ~/.agents/skills and symlink; copy restores per-harness copies)",
    )
    parser.add_argument(
        "--lock-skills",
        dest="lock_skills",
        action="store_true",
        default=None,
        help="force the shared ~/.agents/skills tree read-only after install (default: "
        "on at a harness's real install location, off for --config-dir)",
    )
    parser.add_argument(
        "--no-lock-skills",
        dest="lock_skills",
        action="store_false",
        help="leave the shared ~/.agents/skills tree writable after install",
    )
    parser.add_argument(
        "--list",
        dest="list_",
        action="store_true",
        help="print available categories and skill names, then exit",
    )
    parser.add_argument(
        "--verify",
        action="store_true",
        help="read-only: compare an installed harness against the repository, then exit non-zero on drift",
    )
    parser.add_argument(
        "--verify-after-install", action="store_true",
        help="install, then verify each installed harness (skip undetected harnesses)",
    )
    parser.add_argument(
        "--allow-advisory",
        dest="allow_advisory",
        action="store_true",
        help="record a guardrail downgrade instead of refusing to install an unenforceable deny",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="install even when the harness is not detected on this machine (provision ahead of it)",
    )
    parser.add_argument(
        "--browser-policy",
        choices=["off", "auto", "prompt"],
        default=None,
        help="detect installed browsers and restrict agents to the ones you select "
        "(default: prompt on an interactive terminal, off otherwise; auto picks by "
        "catalogue preference)",
    )
    parser.add_argument(
        "--browser-primary",
        help="browser id agents may drive (see methodology/lifecycle/browsers.json); implies a policy",
    )
    parser.add_argument(
        "--browser-fallback",
        help="optional second browser id agents may drive if the primary is unavailable",
    )
    parser.add_argument(
        "--browser-policy-dir",
        help="directory for the generated browser policy (default: the user policy directory)",
    )
    args = parser.parse_args(argv)
    if args.verify_after_install and (args.verify or args.uninstall or args.dry_run or args.list_):
        parser.error("--verify-after-install requires a real installation")

    only = _split_filter(args.only)
    skills = _split_filter(args.skills)
    agents = _split_filter(args.agents)

    if args.list_:
        print(json.dumps(list_skills(root or ROOT), indent=2))
        return 0

    if not args.harness:
        parser.error("a harness is required unless --list is used")

    # A filter that matches nothing silently installs only the harness files;
    # surface the typo instead (categories come from --list). `--only` spans
    # both trees, so agent categories are valid tokens too.
    if only:
        known = {
            segment
            for segments in _skill_groups(root or ROOT).values()
            for segment in (segments or ["(root)"])
        }
        known.update(
            segment
            for segments in _agent_groups(root or ROOT).values()
            for segment in segments
        )
        unknown = [token for token in only if token not in known]
        if unknown:
            parser.error(
                f"unknown category token(s): {', '.join(unknown)} "
                f"(run --list for the available categories)"
            )

    harnesses = (
        ["opencode", "claude-code", "antigravity", "codex", "cursor", "command-code"]
        if args.harness == "all"
        else [args.harness]
    )
    if args.codex_skill_profile and "codex" not in harnesses:
        parser.error("--codex-skill-profile applies only to codex or all")
    if args.antigravity_profile != "on-demand" and "antigravity" not in harnesses:
        parser.error("--antigravity-profile applies only to antigravity or all")
    if args.verify:
        results = []
        ok = True
        for harness in harnesses:
            config_dir = Path(args.config_dir) if args.config_dir else default_config_dir(
                harness, _home()
            )
            report = verify(harness, root or ROOT, config_dir)
            results.append(report)
            ok = ok and bool(report.get("ok"))
        if results:
            from engine.guardrail import browsers

            # Opt-in feature: absence is informational, never a verification failure.
            results[0]["browser_policy"] = {
                "selection": browsers.read_selection(
                    _browser_policy_dir(args.config_dir, args.browser_policy_dir)
                )
            }
        print(json.dumps(results, indent=2))
        return 0 if ok else 1

    policy_dir = _browser_policy_dir(args.config_dir, args.browser_policy_dir)
    browser: dict[str, object] = {"mode": "off", "status": "off"}
    extra_docs: list[dict] | None = None
    if not args.uninstall:
        if args.browser_primary or args.browser_fallback:
            browser_mode = "select"
        elif args.browser_policy:
            browser_mode = args.browser_policy
        elif sys.stdin.isatty() and sys.stdout.isatty() and not args.dry_run:
            browser_mode = "prompt"
        else:
            browser_mode = "off"
        browser = browser_policy_step(
            root or ROOT, browser_mode, policy_dir,
            primary=args.browser_primary, fallback=args.browser_fallback,
            dry_run=args.dry_run,
        )
        if browser.get("status") == "error":
            print(json.dumps([{"harness": args.harness, "error": browser.get("error"),
                               "browser_policy": {k: v for k, v in browser.items() if k != "document"}}],
                             indent=2))
            return 2
        document = browser.get("document")
        extra_docs = [document] if isinstance(document, dict) else None
        browser = {k: v for k, v in browser.items() if k != "document"}

    results = []
    for harness in harnesses:
        config_dir = Path(args.config_dir) if args.config_dir else default_config_dir(
            harness, _home()
        )
        if args.uninstall:
            results.append(uninstall(harness, root or ROOT, config_dir, dry_run=args.dry_run))
        else:
            results.append(
                install(harness, root or ROOT, config_dir, args.dry_run, only, skills, agents,
                        allow_advisory=args.allow_advisory, force=args.force,
                        codex_skill_profile=args.codex_skill_profile or "compact",
                        skills_mode=args.skills_mode or "link",
                        lock_skills=args.lock_skills,
                        extra_policy_docs=extra_docs,
                        antigravity_profile=args.antigravity_profile)
            )
    if args.uninstall and args.harness == "all" and not args.dry_run:
        from engine.guardrail import browsers

        # The policy is machine-wide: only a full uninstall removes it.
        browser = {"mode": "off", "status": "removed" if browsers.remove_policy(policy_dir) else "absent"}
    if results:
        results[0]["browser_policy"] = browser
    if args.verify_after_install:
        for result in results:
            if result.get("skipped") or result.get("error"):
                continue
            harness = str(result["harness"])
            config_dir = Path(args.config_dir) if args.config_dir else default_config_dir(harness, _home())
            report = verify(harness, root or ROOT, config_dir)
            result["verification"] = report
            if not report.get("ok"):
                result["error"] = "post-install verification failed"
    print(json.dumps(results, indent=2))
    exit_code = 0 if all(not r.get("error") for r in results) else 1
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
