"""Validate canonical agent sources (frontmatter contract, D1/agent-manifests).

Checks: required keys, kebab-case name matching the directory, category
matching the parent directory, existing skill paths, unique slugs, a non-empty
instruction body and the D1 rule that `model` is omitted at source (harnesses
resolve the actual model; the generated `agent.yaml` uses `model: inherit`).
"""

from __future__ import annotations

import re
from pathlib import Path

from engine.frontmatter import FrontmatterError, parse
from engine.generators.agent_manifests import SOURCE_NAME as AGENT_SOURCE_NAME
from engine.generators.agent_manifests import discover_sources

KEBAB = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


def validate(root: Path) -> list[str]:
    """Return a list of error strings; empty list means valid."""
    errors: list[str] = []
    seen: set[str] = set()

    # A misplaced agent source (not at exactly knowledge/agents/<cat>/<name>/)
    # would be missed by the generator and its manifest would never render, yet
    # completeness would still count it as imported. Flag it explicitly.
    agents_dir = root / "knowledge" / "agents"
    discovered = {p.resolve() for p in discover_sources(root)}
    if agents_dir.is_dir():
        for found in agents_dir.rglob(AGENT_SOURCE_NAME):
            if found.resolve() not in discovered:
                errors.append(
                    f"{found.relative_to(root).as_posix()}: agent source must be at "
                    "knowledge/agents/<category>/<name>/agent.source.md"
                )

    for source in discover_sources(root):
        rel = source.relative_to(root).as_posix()
        try:
            doc = parse(source.read_text(encoding="utf-8"))
        except FrontmatterError as exc:
            errors.append(f"{rel}: {exc}")
            continue
        meta = doc.meta
        name = str(meta.get("name", ""))
        category = str(meta.get("category", ""))

        if not KEBAB.match(name):
            errors.append(f"{rel}: 'name' must be kebab-case, got {name!r}")
        if source.parent.name != name:
            errors.append(
                f"{rel}: directory name {source.parent.name!r} != name {name!r}"
            )
        if name in seen:
            errors.append(f"{rel}: duplicate agent name {name!r}")
        seen.add(name)

        expected_category = source.parent.parent.name
        if category != expected_category:
            errors.append(
                f"{rel}: 'category' {category!r} != directory category {expected_category!r}"
            )
        if not str(meta.get("description", "")).strip():
            errors.append(f"{rel}: 'description' is required")
        if "model" in meta:
            errors.append(
                f"{rel}: 'model' must be omitted at source (D1); harnesses resolve "
                "it and the generated agent.yaml uses 'model: inherit'"
            )
        if not doc.body.strip():
            errors.append(f"{rel}: instruction body is empty")
        raw_skills = meta.get("skills", [])
        if not isinstance(raw_skills, list):
            errors.append(f"{rel}: 'skills' must be a block list")
            raw_skills = []
        for skill in raw_skills:
            if not (root / str(skill)).is_file():
                errors.append(f"{rel}: skill path does not exist: {skill}")
    return errors
