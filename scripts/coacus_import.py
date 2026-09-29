#!/usr/bin/env python3
"""Coacus corpus importer (F6).

Imports the source corpora into the repository per `templates/import/import-manifest.json`,
recording provenance in `sources.lock.json` (provenance) and leaving content in
its original language with `transform: [..., "pending-translation"]` (english-only:
PT-BR imports are translated in tracked batches).

    python3 scripts/coacus_import.py plan      [--source skills|superpowers|agents]
    python3 scripts/coacus_import.py apply     [--source ...]
    python3 scripts/coacus_import.py normalize

`plan` writes nothing and prints the actions; `apply` performs the copy and
updates `sources.lock.json`. The import is idempotent: re-running refreshes the
target and the provenance entry (dedup keyed on source repo/commit/path).

`normalize` adapts an already-imported corpus in place — it needs no source
checkout. It rewrites the imported Superpowers workflows to Coacus conventions
(namespace refs, output paths, attribution) and records the change in
`sources.lock.json`; `apply` runs the same pass after copying.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from engine import provenance  # noqa: E402
from engine.frontmatter import parse  # noqa: E402

MANIFEST = ROOT / "templates/import/import-manifest.json"

# Provenance transform tag for the Coacus adaptation of an imported workflow.
ADAPTED_TAG = "adapted:coacus-workflows"
# Marker that makes the attribution footer insertion idempotent.
_ATTRIBUTION_MARK = "Coacus adaptation of a Superpowers workflow"
# Upstream colon namespace (`superpowers:test-driven-development`) -> flat name.
# The lookbehind leaves a URL path (`host/superpowers:x`) untouched.
_COLON_NAMESPACE = re.compile(r"(?<![\w/])superpowers:(?=[a-z0-9])")
# Upstream output root (`docs/superpowers/`), with or without a trailing segment.
_UPSTREAM_OUTPUT = re.compile(r"docs/superpowers(?![A-Za-z0-9_])")
# Sibling workflow dirs addressed by their bare upstream name (links, code spans,
# mermaid labels and shell/JS paths alike; trailing slash optional).
_BARE_SIBLING = re.compile(
    r"\.\./(brainstorming|writing-plans|executing-plans|"
    r"subagent-driven-development|test-driven-development|systematic-debugging|"
    r"requesting-code-review|receiving-code-review|verification-before-completion|"
    r"using-git-worktrees|finishing-a-development-branch|writing-skills|"
    r"dispatching-parallel-agents|diagnosing-superpowers)(?![\w-])"
)
# `using-superpowers` is not imported; its reference points at the local mappings.
_USING_SUPERPOWERS = re.compile(r"\.\./using-superpowers/references/")
# The brainstorming skill names upstream implementation skills it must not invoke.
_FRONTEND_PROHIBITION = re.compile(
    r"never[^.]*?\b(?:frontend-design|mcp-builder)\b[^.]*?implementation skill"
)
# A phrase the markdown-link fixup left duplicated in writing-skills.
_DUPLICATED_PHRASE = re.compile(
    r"(the per-harness tool mappings under references/) or \1"
)
# The attribution block already present in a SKILL.md (replaced, never skipped).
_FOOTER_BLOCK = re.compile(
    r"<!--\nCoacus adaptation of a Superpowers workflow.*?-->\n?", re.DOTALL
)
# Text extensions the pass may rewrite (imported shell and JS/TS included).
_TEXT_SUFFIXES = frozenset(
    {".md", ".sh", ".js", ".cjs", ".mjs", ".ts", ".tsx", ".jsx", ".txt", ".dot", ".html"}
)


def _workspace() -> Path:
    """The parent directory holding the sibling source repositories.

    Defaults to the parent of this repository (Coacus lives beside `skills`,
    `superpowers`, `agente-arquitetura-si`). Override with ``COACUS_WORKSPACE``.
    """
    override = os.environ.get("COACUS_WORKSPACE")
    if override:
        return Path(override)
    return ROOT.parent


def _resolve(value: str) -> str:
    """Resolve the portable ``{workspace}`` token in a manifest path."""
    return value.replace("{workspace}", _workspace().as_posix())


def _load_manifest() -> dict:
    """Load the import manifest and resolve portable ``{workspace}`` tokens."""
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    data["source_repos"] = {
        key: _resolve(str(value)) for key, value in data.get("source_repos", {}).items()
    }
    data["exclude_import_from"] = [
        _resolve(str(value)) for value in data.get("exclude_import_from", [])
    ]
    return data


def _git_commit(repo: Path) -> str:
    try:
        out = subprocess.run(
            ["git", "-C", str(repo), "rev-parse", "HEAD"],
            capture_output=True, text=True, check=False,
        )
        return out.stdout.strip() or "unknown"
    except OSError:
        return "unknown"


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _source_dir(manifest: dict, repo_key: str) -> Path:
    return Path(manifest["source_repos"][repo_key])


def _origin_license(manifest: dict, repo_key: str) -> str:
    """The license declared for a source repo in the import manifest.

    Falls back to a pointer at the source repo when none is declared, so the
    provenance entry never claims a license that was not verified.
    """
    return manifest.get("licenses", {}).get(repo_key, "see source repo")


def _skill_dirs(source_root: Path) -> list[Path]:
    base = source_root / "skills"
    if not base.is_dir():
        return []
    return sorted(p.parent for p in base.rglob("SKILL.md"))


def _target_category(manifest: dict, source_cat: str, subcat: str | None, name: str) -> str:
    """Map a source skill to its target directory under knowledge/skills."""
    if source_cat == "security":
        mapping = manifest["security_map"].get(subcat or "", f"security/{subcat}")
        if isinstance(mapping, dict):
            return mapping.get("override", {}).get(name, mapping["default"])
        return mapping
    if source_cat == "programs":
        return manifest["programs_map"].get(name, manifest["programs_map"]["default"])
    if source_cat == "domains":
        if name.startswith("academic-"):
            return manifest["domains_map"]["academic-prefix"]
        return manifest["domains_map"]["industry"].get(name, "domains/industry")
    return manifest["category_map"].get(source_cat, f"misc/{source_cat}")


def _skill_name(source_dir: Path, manifest: dict) -> str:
    return manifest["name_dir_fixes"].get(source_dir.name, source_dir.name)


def _iter_skill_files(skill_dir: Path) -> list[Path]:
    return sorted(p for p in skill_dir.rglob("*") if p.is_file())


def plan_skills(manifest: dict) -> list[dict]:
    """Plan the import (or exclusion) of every source skill into the taxonomy."""
    source_root = _source_dir(manifest, "skills")
    actions: list[dict] = []
    for skill_dir in _skill_dirs(source_root):
        rel = skill_dir.relative_to(source_root / "skills")
        parts = rel.parts
        source_cat = parts[0]
        subcat = parts[1] if len(parts) == 3 else None
        name = skill_dir.name
        if name in manifest["exclude_skills"]:
            actions.append({"action": "exclude", "name": name, "reason": "manifest exclude_skills"})
            continue
        target_cat = _target_category(manifest, source_cat, subcat, name)
        target_name = _skill_name(skill_dir, manifest)
        target = ROOT / "knowledge" / "skills" / target_cat / target_name
        actions.append({
            "action": "import-skill",
            "source": skill_dir,
            "target": target,
            "name": target_name,
            "renamed": target_name != name,
        })
    return actions


def plan_superpowers(manifest: dict) -> list[dict]:
    """Plan the import of the Superpowers workflow collection, namespaced."""
    source_root = _source_dir(manifest, "superpowers")
    base = source_root / "skills"
    actions: list[dict] = []
    if not base.is_dir():
        return actions
    for skill_dir in sorted(p.parent for p in base.rglob("SKILL.md")):
        if skill_dir.name in ("using-superpowers", "writing-skills"):
            # using-superpowers is replaced by using-coacus; keep writing-skills
            if skill_dir.name == "using-superpowers":
                actions.append({"action": "exclude", "name": skill_dir.name, "reason": "replaced by using-coacus"})
                continue
        target_name = f"superpowers-{skill_dir.name}"
        target = ROOT / manifest["superpowers"]["target_dir"] / target_name
        actions.append({
            "action": "import-workflow",
            "source": skill_dir,
            "target": target,
            "name": target_name,
        })
    return actions


def plan_agents(manifest: dict) -> list[dict]:
    """Plan agent imports, applying the manifest's merge and exclusion rules."""
    source_root = _source_dir(manifest, "skills")
    base = source_root / "agents"
    actions: list[dict] = []
    if not base.is_dir():
        return actions
    # merged target name -> list of source agent dirs (canonical first)
    merges: dict[str, list[str]] = {
        target: sources for target, sources in manifest["agent_merges"].items()
    }
    by_name = {p.parent.name: p.parent for p in base.rglob("AGENT.md")}
    for target_name, source_names in merges.items():
        present = [by_name[n] for n in source_names if n in by_name]
        if len(present) < 2:
            continue  # fewer than two real sources: no merge needed
        category = present[0].parent.name
        actions.append({
            "action": "import-agent",
            "source": present[0],
            "merge_sources": present[1:],
            "target": ROOT / "knowledge" / "agents" / category / target_name,
            "name": target_name,
        })
    consumed = {n for names in merges.values() for n in names}
    excluded_agents = set(manifest.get("exclude_agents", []))
    for name, agent_dir in sorted(by_name.items()):
        if name in consumed:
            continue
        if name in excluded_agents:
            actions.append({"action": "exclude", "name": name, "reason": "manifest exclude_agents"})
            continue
        category = agent_dir.parent.name
        actions.append({
            "action": "import-agent",
            "source": agent_dir,
            "target": ROOT / "knowledge" / "agents" / category / name,
            "name": name,
        })
    return actions


_LINK = re.compile(r"\]\(([^)\s]+)(#[^)]*)?\)")
_SKILL_PATH = re.compile(r"((?:\.\./)+)skills/([^)]+?)/SKILL\.md")


def _source_ref(rest: str, manifest: dict) -> tuple[str, str]:
    """(new_root_relative_skill_dir, new_name) for a source path fragment."""
    parts = rest.split("/")
    source_cat = parts[0]
    subcat = parts[1] if len(parts) == 3 else None
    original = parts[-1]
    new_name = manifest["name_dir_fixes"].get(original, original)
    target_cat = _target_category(manifest, source_cat, subcat, original)
    return f"knowledge/skills/{target_cat}/{new_name}", new_name


def _remap_skill_path(match: re.Match, manifest: dict) -> str:
    """Rewrite an old ../skills/<cat>/<sub>/<name>/SKILL.md to the new taxonomy.

    The agent-source contract resolves `skills:` paths relative to the
    REPOSITORY ROOT, so the remapped path is root-relative.
    """
    ref, _ = _source_ref(match.group(2), manifest)
    return f"{ref}/SKILL.md"


def _skill_index(root: Path) -> dict[str, str]:
    """Map skill name -> repo-relative skill directory (current tree)."""
    index: dict[str, str] = {}
    base = root / "knowledge" / "skills"
    if base.is_dir():
        for skill_md in base.rglob("SKILL.md"):
            index[skill_md.parent.name] = skill_md.parent.relative_to(root).as_posix()
    return index


def _resolve_skill_name(name: str, index: dict[str, str]) -> str | None:
    """Resolve a link target to a current skill dir, tolerating renamed skills.

    Import-time renames (e.g. `moodle` -> `program-moodle`) leave old links
    behind; try the exact name, then the `program-`/`superpowers-` variants.
    """
    for candidate in (name, f"program-{name}", f"superpowers-{name}"):
        if candidate in index:
            return index[candidate]
    return None


def _prune_orphan_outputs(root: Path) -> None:
    """Remove per-agent discovery entries whose source no longer exists.

    A merge replaces an agent; the old `.agents/entries/<name>.json` and any
    `dist/` are stale. Regeneration does not delete orphans, so the import
    prunes them before `generate`.
    """
    entries_dir = root / ".agents" / "entries"
    if entries_dir.is_dir():
        for manifest in entries_dir.glob("*.json"):
            try:
                entry = json.loads(manifest.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError):
                continue
            source = root / str(entry.get("source", ""))
            if not source.is_file():
                manifest.unlink()
    agents_dir = root / "knowledge" / "agents"
    if agents_dir.is_dir():
        for dist in agents_dir.glob("*/*/dist"):
            if not (dist.parent / "agent.source.md").is_file():
                shutil.rmtree(dist)


def _fix_misc_links(root: Path) -> None:
    """Post-import cleanups: AGENTS.md depth, dead using-superpowers links, and
    machine-specific paths leaked from the author's conversion workspace."""
    agent_pat = re.compile(r"\]\(((?:\.\./)+)AGENTS\.md\)")
    dead_super = re.compile(
        r"\[[^\]]*\]\(\.\./using-superpowers/references/[^)]*\)"
    )
    machine = re.compile(r"`?/tmp/opencode/[^`\s)]*`?")
    docs = list((root / "knowledge" / "skills").rglob("*.md"))
    docs += list((root / "knowledge" / "agents").rglob("*.md"))
    docs += list((root / "methodology" / "workflows").rglob("*.md"))
    for path in docs:
        text = path.read_text(encoding="utf-8")
        rel_dir = path.parent

        def repl_agents(match: re.Match) -> str:
            rel = os.path.relpath(root / "AGENTS.md", rel_dir)
            return f"]({rel})"

        new_text = agent_pat.sub(repl_agents, text)
        new_text = dead_super.sub("the per-harness tool mappings under references/", new_text)
        new_text = machine.sub("a local conversion workspace", new_text)
        if new_text != text:
            path.write_text(new_text, encoding="utf-8")


def _fix_skill_links(root: Path) -> None:
    """Rewrite cross-skill links in imported files to the new taxonomy.

    Any markdown link whose target ends in ``/SKILL.md`` is re-pointed to that
    skill's current location, relative to the linking file. Workflow-to-workflow
    links (siblings under ``methodology/workflows``) are resolved against the
    namespaced directories too.
    """
    index = _skill_index(root)
    index.update(_workflow_index(root))
    # Agent sources resolve skill paths RELATIVE TO THE REPO ROOT (agent
    # contract); `_convert_agent` already produced those. Only skill and
    # workflow bodies use file-relative links, so skip knowledge/agents here.
    files = list((root / "knowledge" / "skills").rglob("*.md"))
    files += list((root / "methodology" / "workflows").rglob("*.md"))
    for path in files:
        text = path.read_text(encoding="utf-8")
        rel_dir = path.parent.relative_to(root)

        def repl(match: re.Match) -> str:
            target, anchor = match.group(1), match.group(2) or ""
            if not target.endswith("/SKILL.md"):
                return match.group(0)
            target_name = target[: -len("/SKILL.md")].split("/")[-1]
            resolved = _resolve_skill_name(target_name, index)
            if not resolved:
                return match.group(0)
            rel = os.path.relpath(root / resolved / "SKILL.md", root / rel_dir)
            return f"]({rel}{anchor})"

        new_text = _LINK.sub(repl, text)
        # Sibling links to a namespaced workflow's non-SKILL file.
        for old, new in _workflow_renames(root).items():
            new_text = re.sub(
                rf"\]\(\.\./{re.escape(old)}/", f"](../{new}/", new_text
            )
        if new_text != text:
            path.write_text(new_text, encoding="utf-8")


def _workflow_index(root: Path) -> dict[str, str]:
    index: dict[str, str] = {}
    base = root / "methodology" / "workflows"
    if base.is_dir():
        for skill_md in base.rglob("SKILL.md"):
            index[skill_md.parent.name] = skill_md.parent.relative_to(root).as_posix()
    return index


def _workflow_renames(root: Path) -> dict[str, str]:
    """old workflow dir name -> namespaced name (for sibling links)."""
    renames: dict[str, str] = {}
    base = root / "methodology" / "workflows"
    if base.is_dir():
        for path in base.iterdir():
            if path.is_dir() and path.name.startswith("superpowers-"):
                renames[path.name[len("superpowers-"):]] = path.name
    return renames


def _superpowers_commit(root: Path) -> str:
    """The recorded upstream commit for the Superpowers import, for attribution."""
    for entry in provenance.load(root).get("entries", []):
        if isinstance(entry, dict) and entry.get("source_repo") == "superpowers":
            return str(entry.get("source_commit", "unknown"))
    return "unknown"


def _workflow_files(root: Path) -> list[Path]:
    """Every text file under the imported Superpowers workflow directories.

    Includes the extensionless helper scripts (`task-start`, `review-package`, …)
    alongside the Markdown, shell and JS/TS assets.
    """
    base = root / "methodology" / "workflows"
    if not base.is_dir():
        return []
    return sorted(
        p
        for p in base.glob("superpowers-*/**/*")
        if p.is_file() and (p.suffix in _TEXT_SUFFIXES or p.suffix == "")
    )


def _attribution_footer(commit: str) -> str:
    """The visible attribution + conventions pointer stamped into each SKILL.md."""
    return (
        "<!--\n"
        "Coacus adaptation of a Superpowers workflow (MIT).\n"
        f"Upstream: https://github.com/obra/superpowers @ {commit}\n"
        "Process artifacts are written under docs/temp/.\n"
        "Conventions: ../using-coacus/references/coacus-process-conventions.md\n"
        "-->"
    )


def _adapt_workflow_text(text: str) -> str:
    """Rewrite upstream namespace refs, output paths and dangling references.

    Pure text in, pure text out: the flat installed names replace the upstream
    colon namespace, plan/spec output moves under `docs/temp/`, sibling workflow
    paths are prefixed, and references to skills that do not exist in this
    corpus are repaired.
    """
    text = _USING_SUPERPOWERS.sub("../using-coacus/references/", text)
    text = _BARE_SIBLING.sub(r"../superpowers-\1", text)
    text = _COLON_NAMESPACE.sub("superpowers-", text)
    text = _UPSTREAM_OUTPUT.sub("docs/temp", text)
    text = text.replace(
        "elements-of-style:writing-clearly-and-concisely", "linguistic-en-us"
    )
    text = _FRONTEND_PROHIBITION.sub("never an implementation skill", text)
    text = _DUPLICATED_PHRASE.sub(r"\1", text)
    text = text.replace(
        "skills/brainstorming/visual-companion.md", "visual-companion.md"
    )
    return text


def _attach_attribution(text: str, footer: str) -> str:
    """Replace an existing attribution footer, or insert it after the frontmatter.

    Replacing rather than skipping keeps the footer honest when a re-import
    records a new upstream commit.
    """
    if _FOOTER_BLOCK.search(text):
        result = _FOOTER_BLOCK.sub(footer + "\n", text, count=1)
    else:
        lines = text.split("\n")
        insert_at = 0
        if lines and lines[0].strip() == "---":
            for index in range(1, len(lines)):
                if lines[index].strip() == "---":
                    insert_at = index + 1
                    break
        head = "\n".join(lines[:insert_at]).rstrip("\n")
        tail = "\n".join(lines[insert_at:]).lstrip("\n")
        prefix = f"{head}\n\n" if head else ""
        result = f"{prefix}{footer}\n\n{tail}"
    return result if result.endswith("\n") else result + "\n"


def _normalize_workflow_files(root: Path, commit: str | None = None) -> list[str]:
    """Adapt the imported Superpowers workflow files to Coacus conventions.

    Idempotent text pass over `methodology/workflows/superpowers-*` (Markdown,
    shell and JS/TS assets): it rewrites the upstream ``superpowers:`` colon
    namespace to the flat installed names, redirects plan/spec output to
    ``docs/temp/``, resolves bare sibling workflow paths, repairs dangling
    external references, and stamps a visible attribution footer on each
    ``SKILL.md``. ``commit`` overrides the upstream SHA used in the footer (the
    ``apply`` path passes the freshly imported one). Returns the
    repository-relative paths it changed (empty when the corpus is adapted).
    """
    footer = _attribution_footer(commit or _superpowers_commit(root))
    changed: list[str] = []
    for path in _workflow_files(root):
        text = path.read_text(encoding="utf-8")
        adapted = _adapt_workflow_text(text)
        if path.name == "SKILL.md":
            adapted = _attach_attribution(adapted, footer)
        if adapted != text:
            path.write_text(adapted, encoding="utf-8")
            changed.append(path.relative_to(root).as_posix())
    return changed


def _tag_adapted(root: Path, lock: dict, changed: list[str]) -> int:
    """Tag and re-hash the lock entries for the adapted targets.

    Lock-wide, not run-scoped: a target that was adapted in an earlier run still
    gets its tag and hash corrected. Returns the number of entries modified.
    """
    by_target = {
        entry.get("target_path"): entry
        for entry in lock.get("entries", [])
        if isinstance(entry, dict)
    }
    modified = 0
    for rel in changed:
        entry = by_target.get(rel)
        if entry is None:
            continue
        transform = entry.setdefault("transform", [])
        if ADAPTED_TAG not in transform:
            transform.append(ADAPTED_TAG)
            modified += 1
        digest = _sha256(root / rel)
        if entry.get("target_sha256") != digest:
            entry["target_sha256"] = digest
            modified += 1
    return modified


def _run_normalize() -> int:
    """Adapt the existing corpus in place and record it in `sources.lock.json`.

    Needs no source checkout: it is the surface for applying the adaptation to a
    corpus that was imported earlier. Idempotent — a second run changes nothing.
    """
    changed = _normalize_workflow_files(ROOT)
    lock = provenance.load(ROOT)
    modified = _tag_adapted(ROOT, lock, changed)
    if changed or modified:
        provenance.write(ROOT, lock)
    print(json.dumps({"normalized": len(changed), "files": changed}, indent=2))
    return 0


def _wrap_description(text: str, width: int = 70) -> list[str]:
    """Wrap a description on word boundaries (never mid-word)."""
    import textwrap

    if not text:
        return [""]
    return textwrap.wrap(text, width=width, break_long_words=False) or [""]


def _git_dirty(repo: Path) -> bool:
    try:
        out = subprocess.run(
            ["git", "-C", str(repo), "status", "--porcelain"],
            capture_output=True, text=True, check=False,
        )
        return bool(out.stdout.strip())
    except OSError:
        return False


def _source_commit(repo: Path) -> str:
    commit = _git_commit(repo)
    return f"{commit}+dirty" if _git_dirty(repo) else commit


def _looks_english(text: str) -> bool:
    """Heuristic: English prose has few of the PT-BR markers the validator uses."""
    from engine.validators.skills import PT_MARKERS

    return not any(marker in text for marker in PT_MARKERS)


def _import_transform(target: Path, extra: list[str]) -> list[str]:
    """`pending-translation` only when the imported file is actually non-English."""
    text = target.read_text(encoding="utf-8", errors="replace")
    base = ["imported"]
    if not _looks_english(text):
        base.append("pending-translation")
    return base + extra


def _convert_agent(
    source_md: Path, target_dir: Path, manifest: dict, merge_sources: list[Path] | None = None
) -> None:
    """Turn an imported AGENT.md into the canonical agent.source.md.

    Skill paths are remapped from the source taxonomy to the Coacus taxonomy
    (frontmatter ``skills:`` and inline markdown links alike). When
    ``merge_sources`` is given, the extra agents' charters are appended and
    their skills unioned, so a declared merge never drops content.
    """
    raw = source_md.read_text(encoding="utf-8")
    doc = parse(raw)
    meta = doc.meta
    name = target_dir.name
    category = target_dir.parent.name
    description = str(meta.get("description", "")).strip()
    skills_raw = meta.get("skills", [])
    skills = [str(s) for s in skills_raw] if isinstance(skills_raw, list) else []
    body_parts = [doc.body.strip()]
    titles = [doc_title(doc)]

    for extra in merge_sources or []:
        extra_md = extra / "AGENT.md" if extra.is_dir() else extra
        extra_doc = parse(extra_md.read_text(encoding="utf-8"))
        extra_skills = extra_doc.meta.get("skills", [])
        if isinstance(extra_skills, list):
            skills += [str(s) for s in extra_skills]
        titles.append(doc_title(extra_doc))
        body_parts.append(extra_doc.body.strip())

    remap = lambda s: _SKILL_PATH.sub(lambda m: _remap_skill_path(m, manifest), s)
    skills = sorted({remap(s) for s in skills})
    body = "\n\n---\n\n".join(remap(part) for part in body_parts)
    # Drop the leading H1 (the generated AGENT.md supplies the title).
    body_lines = body.splitlines()
    if body_lines and body_lines[0].startswith("# "):
        body = "\n".join(body_lines[1:]).strip()

    target_dir.mkdir(parents=True, exist_ok=True)
    lines = ["---", f"name: {name}", f"category: {category}", "description: >-"]
    for chunk in _wrap_description(description):
        lines.append(f"  {chunk}")
    lines.append("skills:")
    for skill in skills:
        lines.append(f"  - {skill}")
    lines.append("---")
    lines.append("")
    lines.append(body)
    lines.append("")
    (target_dir / "agent.source.md").write_text("\n".join(lines), encoding="utf-8")


def doc_title(doc) -> str:
    """Return the first ``# `` heading of a parsed document, or an empty string."""
    for line in doc.body.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return ""


def _namespace_workflow_name(target: Path) -> None:
    """After namespacing a workflow dir, sync the frontmatter ``name`` field."""
    from engine.frontmatter import parse as _parse

    skill_md = target / "SKILL.md"
    text = skill_md.read_text(encoding="utf-8")
    doc = _parse(text)
    old_name = str(doc.meta.get("name", ""))
    if old_name == target.name:
        return
    # Rewrite just the name line inside the frontmatter.
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(f"name: {old_name}"):
            lines[index] = f"name: {target.name}"
            break
    skill_md.write_text("\n".join(lines) + "\n", encoding="utf-8")


def apply_actions(manifest: dict, actions: list[dict]) -> list[dict]:
    """Execute the planned actions and return the recorded provenance entries."""
    entries: list[dict] = []
    run_id = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    skills_commit = _source_commit(_source_dir(manifest, "skills"))
    super_commit = _source_commit(_source_dir(manifest, "superpowers"))
    for action in actions:
        if action["action"] in ("exclude", "merge-into"):
            continue
        source: Path = action["source"]
        target: Path = action["target"]
        source_repo = "superpowers" if action["action"] == "import-workflow" else "skills"
        commit = super_commit if source_repo == "superpowers" else skills_commit
        if action["action"] == "import-agent":
            if target.exists():
                shutil.rmtree(target)
            _convert_agent(
                source / "AGENT.md", target, manifest, action.get("merge_sources")
            )
            target_file = target / "agent.source.md"
            transform = _import_transform(target_file, ["converted:agent.source.md"])
            if action.get("merge_sources"):
                transform.append(
                    "merged:" + ",".join(p.name for p in action["merge_sources"])
                )
            entries.append({
                "source_repo": source_repo,
                "source_commit": commit,
                "source_path": (source / "AGENT.md").relative_to(_source_dir(manifest, source_repo)).as_posix(),
                "source_sha256": _sha256(source / "AGENT.md"),
                "target_path": target_file.relative_to(ROOT).as_posix(),
                "target_sha256": _sha256(target_file),
                "origin_license": _origin_license(manifest, source_repo),
                "transform": transform,
                "aliases": [p.name for p in action.get("merge_sources", [])],
                "import_run_id": run_id,
                "imported_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            })
            continue
        # skills / workflows: copy the whole tree
        if target.exists():
            shutil.rmtree(target)
        shutil.copytree(source, target)
        if action["action"] == "import-workflow":
            _namespace_workflow_name(target)
        for file in _iter_skill_files(target):
            source_file = source / file.relative_to(target)
            transform = _import_transform(file, [])
            if action.get("renamed"):
                transform.append("renamed:dir")
            entries.append({
                "source_repo": source_repo,
                "source_commit": commit,
                "source_path": source_file.relative_to(_source_dir(manifest, source_repo)).as_posix(),
                "source_sha256": _sha256(source_file),
                "target_path": file.relative_to(ROOT).as_posix(),
                "target_sha256": _sha256(file),
                "origin_license": _origin_license(manifest, source_repo),
                "transform": transform,
                "import_run_id": run_id,
                "imported_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            })
    return entries


def _relabel_licenses(lock: dict, manifest: dict) -> int:
    """Stamp the declared license onto every entry of a known source repo.

    ``origin_license`` is written at import time, so entries imported before a
    license was declared still read ``see source repo``. Re-importing content to
    fix a label would pull unrelated upstream changes; this rewrites the label in
    place and leaves provenance hashes untouched. Returns the number relabeled.
    """
    licenses = manifest.get("licenses", {})
    relabeled = 0
    for entry in lock.get("entries", []):
        declared = licenses.get(entry.get("source_repo"))
        if declared and entry.get("origin_license") != declared:
            entry["origin_license"] = declared
            relabeled += 1
    return relabeled


def main(argv: list[str] | None = None) -> int:
    """Parse arguments and run the ``plan``, ``apply`` or ``normalize`` action."""
    parser = argparse.ArgumentParser(prog="coacus-import", description=__doc__)
    parser.add_argument("action", choices=["plan", "apply", "normalize"])
    parser.add_argument("--source", choices=["skills", "superpowers", "agents"], default=None)
    args = parser.parse_args(argv)

    if args.action == "normalize":
        if args.source not in (None, "superpowers"):
            parser.error("normalize applies only to the superpowers workflows")
        return _run_normalize()

    manifest = _load_manifest()
    actions: list[dict] = []
    if args.source in (None, "skills", "agents"):
        actions += plan_skills(manifest)
        actions += plan_agents(manifest)
    if args.source in (None, "superpowers"):
        actions += plan_superpowers(manifest)

    # Enforce the source-repo exclusion gate on the ACTUAL action sources (not
    # the top-level source_repos key), so an excluded repo can never be read.
    excluded = [str(Path(p)) for p in manifest.get("exclude_import_from", [])]
    for action in actions:
        source = action.get("source")
        if not source:
            continue
        source_str = str(Path(source))
        if any(source_str.startswith(excluded_root) for excluded_root in excluded):
            raise SystemExit(f"refusing to import from excluded repo: {source_str}")


    if args.action == "plan":
        counts: dict[str, int] = {}
        for action in actions:
            counts[action["action"]] = counts.get(action["action"], 0) + 1
        print(json.dumps({
            "counts": counts,
            "excluded": [a["name"] for a in actions if a["action"] == "exclude"],
            "merged": [a["name"] for a in actions if a["action"] == "merge-into"],
            "renamed": [a["name"] for a in actions if a.get("renamed")],
            "sample": [str(a.get("target", a["name"])) for a in actions[:8]],
        }, indent=2))
        return 0

    entries = apply_actions(manifest, actions)
    _prune_orphan_outputs(ROOT)
    _fix_skill_links(ROOT)
    _fix_misc_links(ROOT)
    lock = provenance.load(ROOT)
    # Replace entries for this run's targets (idempotent re-import).
    targets = {e["target_path"] for e in entries}
    lock["entries"] = [e for e in lock.get("entries", []) if e["target_path"] not in targets]
    lock["entries"].extend(entries)
    lock["entries"].sort(key=lambda e: e["target_path"])
    # Adapt the imported workflows to Coacus conventions. The pass walks the
    # whole superpowers corpus, so tagging is lock-wide and the footer carries
    # this run's upstream commit.
    if args.source in (None, "superpowers"):
        commit = _source_commit(_source_dir(manifest, "superpowers"))
        _tag_adapted(ROOT, lock, _normalize_workflow_files(ROOT, commit=commit))
    relabeled = _relabel_licenses(lock, manifest)
    provenance.write(ROOT, lock)
    print(json.dumps({
        "imported_files": len(entries),
        "lock_entries": len(lock["entries"]),
        "relabeled_licenses": relabeled,
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
