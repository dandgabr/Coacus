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
- claude-code skills   -> <config_dir>/skills/<skill>/  (documented personal path)
              agents   -> <config_dir>/agents/<name>.md
              hook     -> plugin staged at <config_dir>/plugins/coacus/ with the
              script at bootstrap/session-start.sh (matching hooks.json).
- antigravity plugin (manifest + rule + skills + agents) ->
              <config_dir>/config/plugins/coacus/; activation is by directory,
              so no registry edit is needed.
- codex       skills   -> ~/.agents/skills/<skill>/  (Codex scans .agents/skills,
              not ~/.codex/skills); agents -> <config_dir>/agents/<name>.toml;
              plus the SessionStart hook at <config_dir>/hooks.json.
- cursor      skills   -> ~/.agents/skills/<skill>/; agents ->
              <config_dir>/agents/<name>.md; plus the sessionStart hook at
              <config_dir>/hooks.json (snake_case `additional_context`).

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
import fnmatch
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

MANIFEST_NAME = "coacus-install.json"
NOTICE_NAME = "THIRD-PARTY-NOTICES.md"
SKILL_ROOTS = ("methodology/workflows", "knowledge/skills")


def _home() -> Path:
    return Path.home()


def default_config_dir(harness: str, home: Path) -> Path:
    return {
        "opencode": home / ".config" / "opencode",
        "claude-code": home / ".claude",
        "antigravity": home / ".gemini",
        "codex": home / ".codex",
        "cursor": home / ".cursor",
    }[harness]


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


def _render_agent_opencode(source: Path, root: Path) -> str:
    """OpenCode agent markdown: frontmatter description + mode, body as prompt."""
    meta = _agent_meta(source)
    try:
        rel = source.relative_to(root).as_posix()
    except ValueError:
        rel = source.as_posix()
    return (
        "---\n"
        f"description: {meta['description']}\n"
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
        f"description: {meta['description']}\n"
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
) -> list[tuple[Path, str]]:
    plan: list[tuple[Path, str]] = []
    for source in discover_agents(root, only=only, agents=agents):
        name = str(_agent_meta(source)["name"])
        plan.append((agents_dir / f"{name}.md", _render_agent_opencode(source, root)))
    return plan


def _plan_agents_antigravity(
    root: Path, agents_dir: Path, only: list[str] | None = None, agents: list[str] | None = None
) -> list[tuple[Path, str]]:
    plan: list[tuple[Path, str]] = []
    for source in discover_agents(root, only=only, agents=agents):
        name = str(_agent_meta(source)["name"])
        plan.append((agents_dir / name / "agent.md", _render_agent_named(source)))
    return plan


def _plan_agents_codex(
    root: Path, agents_dir: Path, only: list[str] | None = None, agents: list[str] | None = None
) -> list[tuple[Path, str]]:
    plan: list[tuple[Path, str]] = []
    for source in discover_agents(root, only=only, agents=agents):
        name = str(_agent_meta(source)["name"])
        plan.append((agents_dir / f"{name}.toml", _render_agent_codex(source)))
    return plan


def _plan_agents_named(
    root: Path, agents_dir: Path, only: list[str] | None = None, agents: list[str] | None = None
) -> list[tuple[Path, str]]:
    """Agent markdown (name+description) for Claude Code and Cursor."""
    plan: list[tuple[Path, str]] = []
    for source in discover_agents(root, only=only, agents=agents):
        name = str(_agent_meta(source)["name"])
        plan.append((agents_dir / f"{name}.md", _render_agent_named(source)))
    return plan


def _skill_files(skill_dir: Path) -> list[Path]:
    """Every file belonging to a skill, so companions (references/) travel too."""
    return sorted(p for p in skill_dir.rglob("*") if p.is_file())


def _plan_skills(
    root: Path,
    skills_dir: Path,
    only: list[str] | None = None,
    skills: list[str] | None = None,
) -> list[tuple[Path, str]]:
    """Mirror every selected skill tree (SKILL.md + references/examples/scripts)."""
    plan: list[tuple[Path, str]] = []
    for skill in discover_skills(root, only=only, skills=skills):
        for source in _skill_files(skill):
            relative = source.relative_to(skill)
            target = skills_dir / skill.name / relative
            plan.append((target, source.read_text(encoding="utf-8")))
    notice = root / NOTICE_NAME
    if notice.is_file():
        plan.append((skills_dir / NOTICE_NAME, notice.read_text(encoding="utf-8")))
    return plan


def _plan_opencode(
    root: Path,
    config_dir: Path,
    only: list[str] | None = None,
    skills: list[str] | None = None,
    agents: list[str] | None = None,
) -> list[tuple[Path, str]]:
    """Plugin + governor gate + mirrored skill trees for opencode."""
    source = root / "harnesses/opencode/bootstrap/coacus.js"
    content = source.read_text(encoding="utf-8").replace(
        "__COACUS_ROOT__", root.as_posix()
    )
    plan: list[tuple[Path, str]] = [(config_dir / "plugins" / "coacus.js", content)]
    gate = root / "harnesses/opencode/bootstrap/governor-gate.js"
    if gate.is_file():
        plan.append(
            (
                config_dir / "plugins" / "coacus-governor.js",
                gate.read_text(encoding="utf-8").replace(
                    "__COACUS_ROOT__", root.as_posix()
                ),
            )
        )
    plan += _plan_skills(root, config_dir / "skills", only, skills)
    plan += _plan_agents_opencode(root, config_dir / "agent", only, agents)
    return plan


def _plan_claude(
    root: Path,
    config_dir: Path,
    only: list[str] | None = None,
    skills: list[str] | None = None,
    agents: list[str] | None = None,
) -> list[tuple[Path, str]]:
    """Skills + subagents + a hook plugin whose script matches hooks.json."""
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
    # hooks.json commands "${CLAUDE_PLUGIN_ROOT}/bootstrap/session-start.sh",
    # so the script MUST land under bootstrap/ (not hooks/).
    plan.append(
        (
            plugin / "hooks" / "hooks.json",
            (root / "harnesses/claude-code/bootstrap/hooks.json").read_text(encoding="utf-8"),
        )
    )
    plan.append(
        (
            plugin / "bootstrap" / "session-start.sh",
            (root / "harnesses/claude-code/bootstrap/session-start.sh").read_text(
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
) -> list[tuple[Path, str]]:
    """Plugin (manifest + rule + skills) under the global plugins dir.

    Antigravity activates plugins by directory placement (``~/.gemini/config/plugins/``
    globally or ``.agents/plugins/`` per workspace). Rules load from the plugin's
    ``rules/`` dir with ``activation: always_on``; no registry edit is required.
    """
    plugin = config_dir / "config" / "plugins" / "coacus"
    plan = _plan_skills(root, plugin / "skills", only, skills)
    plan += _plan_agents_antigravity(root, plugin / "agents", only, agents)
    for name in ("plugin.json", "coacus-rule.md"):
        source = root / "harnesses/antigravity/bootstrap" / name
        plan.append((plugin / name, source.read_text(encoding="utf-8")))
    # Governor hook (governance-executable) + its plugin hooks.json root file.
    hook = root / "harnesses/antigravity/bootstrap/governor-hook.sh"
    if hook.is_file():
        plan.append(
            (
                plugin / "governor-hook.sh",
                hook.read_text(encoding="utf-8").replace(
                    "__COACUS_ROOT__", root.as_posix()
                ),
            )
        )
        plan.append((plugin / "hooks.json", _antigravity_hooks_json(plugin)))
    return plan


def _antigravity_hooks_json(plugin_dir: Path) -> str:
    """Antigravity plugin hooks.json wiring the governor hook to lifecycle events."""
    command = f"{plugin_dir.as_posix()}/governor-hook.sh"
    matcher = "invoke_subagent|manage_subagents|task"
    return (
        json.dumps(
            {
                "coacus-governor": {
                    "PreToolUse": [
                        {
                            "matcher": matcher,
                            "hooks": [{"type": "command", "command": f"{command} pretool"}],
                        }
                    ],
                    "PostToolUse": [
                        {
                            "matcher": matcher,
                            "hooks": [{"type": "command", "command": f"{command} posttool"}],
                        }
                    ],
                    "PreInvocation": [
                        {"type": "command", "command": f"{command} preinv"}
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
) -> list[tuple[Path, str]]:
    """Skills to the documented scan root + the SessionStart hook.

    Codex scans ``.agents/skills`` (not ``~/.codex/skills``), and its hooks load
    from ``~/.codex/hooks.json``. The hook command needs an absolute script
    path, so we stage the script beside the hook and substitute the repo root.
    """
    plan: list[tuple[Path, str]] = []
    # Codex scans $HOME/.agents/skills, not $config_dir/.codex/skills.
    plan += _plan_skills(root, config_dir.parent / ".agents" / "skills", only, skills)
    # Codex agent roles live in $CODEX_HOME/agents/*.toml.
    plan += _plan_agents_codex(root, config_dir / "agents", only, agents)
    script = (root / "harnesses/codex/bootstrap/session-start.sh").read_text(encoding="utf-8")
    plan.append((config_dir / "coacus" / "session-start.sh", script))
    hooks = (root / "harnesses/codex/bootstrap/hooks.json").read_text(encoding="utf-8")
    plan.append(
        (
            config_dir / "hooks.json",
            hooks.replace("__COACUS_ROOT__", root.as_posix()),
        )
    )
    return plan


def _plan_cursor(
    root: Path,
    config_dir: Path,
    only: list[str] | None = None,
    skills: list[str] | None = None,
    agents: list[str] | None = None,
) -> list[tuple[Path, str]]:
    """Skills to a Cursor scan root + subagents + the sessionStart hook.

    Cursor hooks live at ``~/.cursor/hooks.json`` (user) or
    ``<project>/.cursor/hooks.json``; the output key is snake_case
    ``additional_context``. Subagents load from ``~/.cursor/agents/<name>.md``.
    Commands are repo-absolute.
    """
    plan: list[tuple[Path, str]] = []
    plan += _plan_skills(root, config_dir.parent / ".agents" / "skills", only, skills)
    plan += _plan_agents_named(root, config_dir / "agents", only, agents)
    script = (root / "harnesses/cursor/bootstrap/session-start.sh").read_text(encoding="utf-8")
    plan.append((config_dir / "coacus" / "session-start.sh", script))
    hooks = (root / "harnesses/cursor/bootstrap/hooks.json").read_text(encoding="utf-8")
    plan.append(
        (
            config_dir / "hooks.json",
            hooks.replace("__COACUS_ROOT__", root.as_posix()),
        )
    )
    return plan


def plan(
    harness: str,
    root: Path,
    config_dir: Path,
    only: list[str] | None = None,
    skills: list[str] | None = None,
    agents: list[str] | None = None,
) -> list[tuple[Path, str]]:
    if harness == "opencode":
        return _plan_opencode(root, config_dir, only, skills, agents)
    if harness == "claude-code":
        return _plan_claude(root, config_dir, only, skills, agents)
    if harness == "antigravity":
        return _plan_antigravity(root, config_dir, only, skills, agents)
    if harness == "codex":
        return _plan_codex(root, config_dir, only, skills, agents)
    if harness == "cursor":
        return _plan_cursor(root, config_dir, only, skills, agents)
    return []


def install(
    harness: str,
    root: Path,
    config_dir: Path,
    dry_run: bool,
    only: list[str] | None = None,
    skills: list[str] | None = None,
    agents: list[str] | None = None,
) -> dict[str, object]:
    files = plan(harness, root, config_dir, only, skills, agents)
    if dry_run:
        return {
            "harness": harness,
            "files": [str(t) for t, _ in files],
            "dry_run": True,
            "only": only or [],
            "skills": skills or [],
            "agents": agents or [],
        }
    written: list[str] = []
    for target, content in files:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        written.append(target.as_posix())
    manifest = config_dir / MANIFEST_NAME
    manifest.write_text(
        json.dumps(
            {
                "harness": harness,
                "files": written,
                "only": only or [],
                "skills": skills or [],
                "agents": agents or [],
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    return {"harness": harness, "files": written, "manifest": manifest.as_posix()}


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
    if name in ("hooks.json", "governor-hook.sh", "coacus-governor.js"):
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


def _component_counts(files: list[tuple[Path, str]]) -> dict[str, int]:
    """Distinct skills/agents plus hook/other file counts, from a plan."""
    skills = {t.parent.as_posix() for t, _ in files if t.name == "SKILL.md"}
    agents = {_agent_key(t) for t, _ in files if _classify(t) == "agent"}
    hooks = [t for t, _ in files if _classify(t) == "hook"]
    other = [t for t, _ in files if _classify(t) == "other"]
    return {
        "skills": len(skills),
        "agents": len(agents),
        "hook_files": len(hooks),
        "other_files": len(other),
    }


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
        "ok": False,
    }
    if not manifest.is_file():
        result["error"] = "no manifest — harness not installed (run install first)"
        return result
    data = json.loads(manifest.read_text(encoding="utf-8"))
    only = data.get("only") or None
    skills = data.get("skills") or None
    agents = data.get("agents") or None
    files = plan(harness, root, config_dir, only, skills, agents)
    missing = [
        t.as_posix() for t, _ in files if not t.is_file()
    ]
    drift = [
        t.as_posix()
        for t, content in files
        if t.is_file() and t.read_text(encoding="utf-8") != content
    ]
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
    result["ok"] = not missing and not drift and recorded == planned
    return result


def _contained(path: Path, root: Path) -> bool:
    """True only if ``path`` resolves inside ``root`` (blocks manifest tampering)."""
    try:
        path.resolve().relative_to(root.resolve())
    except ValueError:
        return False
    return True


def uninstall(harness: str, config_dir: Path, dry_run: bool = False) -> dict[str, object]:
    manifest = config_dir / MANIFEST_NAME
    if not manifest.is_file():
        return {"harness": harness, "removed": [], "note": "no manifest"}
    data = json.loads(manifest.read_text(encoding="utf-8"))
    planned: list[str] = []
    skipped: list[str] = []
    for path in data.get("files", []):
        target = Path(path)
        if not _contained(target, config_dir):
            skipped.append(path)
            continue
        if target.is_file():
            if not dry_run:
                target.unlink()
            planned.append(path)
    if not dry_run:
        manifest.unlink()
    return {"harness": harness, "removed": planned, "skipped": skipped, "dry_run": dry_run}


def main(argv: list[str] | None = None, root: Path | None = None) -> int:
    parser = argparse.ArgumentParser(prog="coacus-install", description=__doc__)
    parser.add_argument(
        "harness",
        nargs="?",
        choices=["opencode", "claude-code", "antigravity", "codex", "cursor", "all"],
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
    args = parser.parse_args(argv)

    only = _split_filter(args.only)
    skills = _split_filter(args.skills)
    agents = _split_filter(args.agents)

    if args.list_:
        print(json.dumps(list_skills(root or ROOT), indent=2))
        return 0

    if not args.harness:
        parser.error("a harness is required unless --list is used")

    harnesses = (
        ["opencode", "claude-code", "antigravity", "codex", "cursor"]
        if args.harness == "all"
        else [args.harness]
    )
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
        print(json.dumps(results, indent=2))
        return 0 if ok else 1

    results = []
    for harness in harnesses:
        config_dir = Path(args.config_dir) if args.config_dir else default_config_dir(
            harness, _home()
        )
        if args.uninstall:
            results.append(uninstall(harness, config_dir, dry_run=args.dry_run))
        else:
            results.append(
                install(harness, root or ROOT, config_dir, args.dry_run, only, skills, agents)
            )
    print(json.dumps(results, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
