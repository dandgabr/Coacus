"""Generate the repository catalog from disk (D3: disk is the truth).

Writes ``catalog/catalog.json`` (machine index) and ``catalog/INDEX.md``
(human index) — purely content-derived, no timestamps, so ``check`` can
verify idempotency and CI can fail on drift (ADR-0014).
"""

from __future__ import annotations

import json
from pathlib import Path

from engine.frontmatter import parse
from engine.generators.agent_manifests import discover_sources

CATALOG_PATH = "catalog/catalog.json"
INDEX_PATH = "catalog/INDEX.md"


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
    agents.sort(key=lambda item: item["name"])

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


def _index_markdown(data: dict) -> str:
    counts = data["counts"]
    lines = [
        "# Coacus Catalog Index",
        "",
        "> GENERATED from disk by `scripts/coacus.py generate` — do not edit.",
        "",
        f"**Totals:** {counts['skills']} skill(s) · {counts['agents']} agent(s) · "
        f"{counts['mcps']} MCP(s)",
        "",
        "## Agents",
        "",
    ]
    if data["agents"]:
        lines += ["| Agent | Category | Source |", "|---|---|---|"]
        lines += [
            f"| {a['name']} | {a['category']} | [{a['source']}](../{a['source']}) |"
            for a in data["agents"]
        ]
    else:
        lines.append("_None yet._")

    lines += ["", "## Skills", ""]
    if data["skills"]:
        lines += ["| Skill | Path |", "|---|---|"]
        lines += [
            f"| {s['name']} | [{s['path']}](../{s['path']}) |"
            for s in data["skills"]
        ]
    else:
        lines.append("_None yet._")

    lines += ["", "## MCPs", ""]
    if data["mcps"]:
        lines += ["| MCP | Path |", "|---|---|"]
        lines += [
            f"| {m['name']} | [{m['path']}](../{m['path']}) |" for m in data["mcps"]
        ]
    else:
        lines.append("_None yet._")

    return "\n".join(lines) + "\n"


def write(root: Path) -> list[Path]:
    """Materialize the catalog and its human index. Returns written paths."""
    data = build(root)
    out_dir = root / "catalog"
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "catalog.json").write_text(
        json.dumps(data, indent=2) + "\n", encoding="utf-8"
    )
    (out_dir / "INDEX.md").write_text(_index_markdown(data), encoding="utf-8")
    return [out_dir / "catalog.json", out_dir / "INDEX.md"]


def _expected(root: Path) -> dict[str, str]:
    data = build(root)
    return {
        CATALOG_PATH: json.dumps(data, indent=2) + "\n",
        INDEX_PATH: _index_markdown(data),
    }


def check(root: Path) -> list[str]:
    """Drift check for the catalog and its index (ADR-0014)."""
    drift: list[str] = []
    for rel, content in _expected(root).items():
        target = root / rel
        if not target.is_file():
            drift.append(f"{rel}: missing (run generate)")
        elif target.read_text(encoding="utf-8") != content:
            drift.append(f"{rel}: out of date (run generate)")
    return drift
