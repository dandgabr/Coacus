"""Generate catalog/groups.json — a grouping manifest by top-level category.

Skills share one flat name namespace but live under a category directory.
This manifest groups them for directory-style browsing without changing the flat
catalog. It is derived from disk, byte-idempotent and drift-checked.
"""

from __future__ import annotations

import json
from pathlib import Path

from engine.frontmatter import FrontmatterError, parse
from engine.generators.discovery_index import is_internal

GROUPS_PATH = "catalog/groups.json"


def _category(root: Path, source: Path) -> str:
    rel = source.relative_to(root).as_posix()
    if rel.startswith("methodology/workflows/"):
        return "workflows"
    parts = rel.split("/")
    # knowledge/skills/<category>/...
    return parts[2] if len(parts) > 3 else "uncategorized"


def build(root: Path) -> dict:
    """Build the grouping manifest from disk."""
    groups: dict[str, list[str]] = {}
    for top in ("knowledge/skills", "methodology/workflows"):
        base = root / top
        if not base.is_dir():
            continue
        for source in sorted(base.rglob("SKILL.md")):
            try:
                doc = parse(source.read_text(encoding="utf-8"))
            except FrontmatterError:
                continue
            if is_internal(doc.meta):
                continue
            groups.setdefault(_category(root, source), []).append(source.parent.name)
    return {
        "schema": 1,
        "groups": [
            {"title": title, "skills": sorted(names)}
            for title, names in sorted(groups.items())
        ],
    }


def _content(root: Path) -> str:
    return json.dumps(build(root), indent=2) + "\n"


def write(root: Path) -> list[Path]:
    """Write the grouping manifest; return the written path."""
    target = root / GROUPS_PATH
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(_content(root), encoding="utf-8")
    return [target]


def check(root: Path) -> list[str]:
    """Drift check for the grouping manifest (generated-artifacts)."""
    target = root / GROUPS_PATH
    if not target.is_file():
        return [f"{GROUPS_PATH}: missing (run generate)"]
    if target.read_text(encoding="utf-8") != _content(root):
        return [f"{GROUPS_PATH}: out of date (run generate)"]
    return []
