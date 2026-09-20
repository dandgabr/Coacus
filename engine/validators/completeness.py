"""Completeness verification (F8): nothing from the sources was left behind.

A read-only audit that answers "did the import miss anything?" by reconciling:

- the import manifest's declared expectations against the source repositories
  (when they are available locally), and
- the imported corpus against `sources.lock.json` and the generated catalog.

It is dependency-free and degrades gracefully: on a machine without the source
repos it still verifies the target side (lock + catalog + references).
"""

from __future__ import annotations

import json
from pathlib import Path

from engine.generators.catalog import build as build_catalog

MANIFEST = "templates/import/import-manifest.json"
LOCK = "sources.lock.json"


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _source_skills(repo: Path) -> dict[str, Path]:
    base = repo / "skills"
    if not base.is_dir():
        return {}
    return {p.parent.name: p.parent for p in base.rglob("SKILL.md")}


def _source_agents(repo: Path) -> dict[str, Path]:
    base = repo / "agents"
    if not base.is_dir():
        return {}
    return {p.parent.name: p.parent for p in base.rglob("AGENT.md")}


def _imported_skill_names(root: Path) -> set[str]:
    return {p.parent.name for p in (root / "knowledge" / "skills").rglob("SKILL.md")}


def _imported_workflow_names(root: Path) -> set[str]:
    return {p.parent.name for p in (root / "methodology" / "workflows").rglob("SKILL.md")}


def _imported_agent_names(root: Path) -> set[str]:
    return {p.parent.name for p in (root / "knowledge" / "agents").rglob("agent.source.md")}


def validate(root: Path) -> list[str]:
    """Return a list of completeness gaps (empty = nothing left behind)."""
    gaps: list[str] = []
    manifest_path = root / MANIFEST
    if not manifest_path.is_file():
        return [f"{MANIFEST}: missing"]
    manifest = _load(manifest_path)

    # --- target side (always checked) ---------------------------------------
    imported_skills = _imported_skill_names(root)
    imported_workflows = _imported_workflow_names(root)
    imported_agents = _imported_agent_names(root)
    if not imported_skills:
        gaps.append("no skills imported under knowledge/skills")
    if not imported_agents:
        gaps.append("no agents imported under knowledge/agents")

    lock_path = root / LOCK
    if lock_path.is_file():
        lock = _load(lock_path)
        for entry in lock.get("entries", []):
            target = root / entry.get("target_path", "")
            if not target.is_file():
                gaps.append(f"lock target missing on disk: {entry.get('target_path')}")
        lock_targets = {e.get("target_path") for e in lock.get("entries", [])}
    else:
        lock_targets = set()
        gaps.append(f"{LOCK}: missing")

    # --- catalog on disk vs live disk --------------------------------------
    catalog_file = root / "catalog" / "catalog.json"
    live = build_catalog(root)
    if catalog_file.is_file():
        committed = _load(catalog_file)
        if committed.get("counts") != live["counts"]:
            gaps.append(
                f"catalog/catalog.json counts {committed.get('counts')} != disk {live['counts']}"
            )
    else:
        gaps.append("catalog/catalog.json: missing")

    # --- orphan targets (a target with no provenance entry) ----------------
    provenance_targets = {
        str(e.get("target_path")) for e in (_load(lock_path).get("entries", []) if lock_path.is_file() else [])
    }
    for source in (root / "knowledge" / "skills").rglob("SKILL.md"):
        rel = source.relative_to(root).as_posix()
        if rel not in provenance_targets:
            gaps.append(f"orphan skill with no provenance: {rel}")

    # --- agent skill references (parsed from frontmatter) ------------------
    from engine.frontmatter import FrontmatterError, parse as parse_frontmatter

    for source in (root / "knowledge" / "agents").rglob("agent.source.md"):
        try:
            doc = parse_frontmatter(source.read_text(encoding="utf-8"))
        except FrontmatterError as exc:
            gaps.append(f"{source.relative_to(root).as_posix()}: frontmatter error ({exc})")
            continue
        for skill in doc.meta.get("skills", []):
            skill = str(skill)
            if skill and not (root / skill).is_file():
                gaps.append(
                    f"{source.relative_to(root).as_posix()}: broken skill ref {skill}"
                )

    # --- source side (only when the repos are present) ----------------------
    source_repos = manifest.get("source_repos", {})
    excluded_skills = set(manifest.get("exclude_skills", []))
    merged_sources = {
        name
        for names in manifest.get("agent_merges", {}).values()
        for name in names  # every listed source is folded into the merge target
    }
    merge_targets = set(manifest.get("agent_merges", {}).keys())
    blocked = set(manifest.get("exclude_import_from", []))

    skills_repo = source_repos.get("skills")
    renamed = manifest.get("name_dir_fixes", {})
    if skills_repo and Path(skills_repo).is_dir() and not any(
        str(Path(skills_repo)) == b for b in blocked
    ):
        repo = Path(skills_repo)
        for name in _source_skills(repo):
            if name in excluded_skills:
                continue
            expected = renamed.get(name, name)
            if expected not in imported_skills:
                gaps.append(f"source skill not imported: {name} (expected as {expected})")
        for name in _source_agents(repo):
            if name in merged_sources:
                continue  # merged into a target agent
            if name not in imported_agents:
                gaps.append(f"source agent not imported: {name}")
        for target in merge_targets:
            if target not in imported_agents:
                gaps.append(f"merge target agent missing: {target}")

    super_repo = source_repos.get("superpowers")
    if super_repo and Path(super_repo).is_dir():
        repo = Path(super_repo)
        for name, path in _source_skills(repo).items():
            if name in ("using-superpowers",):  # replaced by using-coacus
                continue
            if f"superpowers-{name}" not in imported_workflows and name not in imported_workflows:
                gaps.append(f"source workflow not imported: {name}")
        if "using-coacus" not in imported_workflows:
            gaps.append("entry workflow using-coacus is missing")

    # --- ADRs D1–D12 + the import/taxonomy ADR present ---------------------
    adr_dir = root / "docs" / "adr"
    present = {p.name.split("-")[1] for p in adr_dir.glob("ADR-*.md")}
    for number in [f"{n:04d}" for n in range(1, 18)]:  # ADR-0001..ADR-0017
        if number not in present:
            gaps.append(f"missing ADR: ADR-{number}")

    return gaps
