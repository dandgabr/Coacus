"""Generate the repository catalog from disk (D3: disk is the truth).

Writes ``catalog/catalog.json`` — purely content-derived, no timestamps — so
``check`` can verify idempotency and CI can fail on drift (ADR-0014).
"""

from __future__ import annotations

import json
from pathlib import Path

from engine.frontmatter import parse
from engine.generators.agent_manifests import discover_sources

CATALOG_PATH = "catalog/catalog.json"


def build(root: Path) -> dict:
    """Build the catalog structure from canonical sources on disk."""
    agents = []
    for source in discover_sources(root):
        doc = parse(source.read_text(encoding="utf-8"))
        agents.append(
            {
                "name": str(doc.meta.get("name", "")),
                "category": str(doc.meta.get("category", "")),
                "description": str(doc.meta.get("description", "")),
                "source": source.relative_to(root).as_posix(),
            }
        )
    agents.sort(key=lambda a: a["name"])

    skills_dir = root / "knowledge" / "skills"
    skills = [
        {"name": path.parent.name, "path": path.relative_to(root).as_posix()}
        for path in sorted(skills_dir.rglob("SKILL.md"))
    ] if skills_dir.is_dir() else []

    mcps_dir = root / "knowledge" / "mcps"
    mcps = [
        {"name": path.parent.name, "path": path.relative_to(root).as_posix()}
        for path in sorted(mcps_dir.rglob("MCP.md"))
    ] if mcps_dir.is_dir() else []

    return {
        "schema": 1,
        "counts": {"agents": len(agents), "skills": len(skills), "mcps": len(mcps)},
        "agents": agents,
        "skills": skills,
        "mcps": mcps,
    }


def write(root: Path) -> Path:
    """Materialize the catalog. Returns the written path."""
    out = root / CATALOG_PATH
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(build(root), indent=2) + "\n", encoding="utf-8")
    return out


def check(root: Path) -> list[str]:
    """Drift check for the catalog (ADR-0014)."""
    target = root / CATALOG_PATH
    if not target.is_file():
        return [f"{CATALOG_PATH}: missing (run generate)"]
    expected = json.dumps(build(root), indent=2) + "\n"
    if target.read_text(encoding="utf-8") != expected:
        return [f"{CATALOG_PATH}: out of date (run generate)"]
    return []
