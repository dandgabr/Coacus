"""Validate canonical skill sources (D2/ADR-0003, corpus import contract).

Errors:
- frontmatter parses and ``name`` is kebab-case, equal to the directory name
- ``description`` present
- globally unique slug (flat namespace — harnesses load skills by name)
- SKILL.md lives at ``<category>[/<subcategory>]/<skill>/SKILL.md`` (no nesting)
- local markdown links resolve relative to the skill directory

Warnings (non-blocking):
- non-English markers in frontmatter/body (ADR-0001; becomes error post-import)
- oversized description (corpus guidance: keep frontmatter lean)
"""

from __future__ import annotations

import re
from pathlib import Path

from engine.frontmatter import FrontmatterError, parse

KEBAB = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+?)(?:\s+\"[^\"]*\")?\)")
SKIP_LINK_PREFIXES = ("http://", "https://", "mailto:", "tel:", "#")
DESCRIPTION_WARN_LEN = 1024
PT_MARKERS = ("ção", "ções", "ã", "õ", "Atua como", "Especialista em")


def discover_skills(root: Path) -> list[Path]:
    """All ``SKILL.md`` under ``knowledge/skills`` (any depth, for guard)."""
    skills_dir = root / "knowledge" / "skills"
    if not skills_dir.is_dir():
        return []
    return sorted(skills_dir.rglob("SKILL.md"))


def validate(root: Path) -> list[str]:
    """Return a list of error strings; empty list means valid."""
    errors: list[str] = []
    skills_dir = root / "knowledge" / "skills"
    discovered = discover_skills(root)
    skill_dirs = {source.parent for source in discovered}
    seen: set[str] = set()

    for source in discovered:
        rel = source.relative_to(root).as_posix()
        parts = source.relative_to(skills_dir).parts
        if len(parts) < 3:
            errors.append(
                f"{rel}: SKILL.md must live at <category>[/<subcategory>]/<skill>/"
            )
            continue
        ancestor = source.parent.parent
        nested = False
        while ancestor != skills_dir.parent and ancestor != skills_dir:
            if ancestor in skill_dirs:
                errors.append(f"{rel}: nested SKILL.md beneath {ancestor.name!r} (not allowed)")
                nested = True
                break
            ancestor = ancestor.parent
        if nested:
            continue
        try:
            doc = parse(source.read_text(encoding="utf-8"))
        except FrontmatterError as exc:
            errors.append(f"{rel}: {exc}")
            continue

        name = str(doc.meta.get("name", ""))
        if not KEBAB.match(name):
            errors.append(f"{rel}: 'name' must be kebab-case, got {name!r}")
        if source.parent.name != name:
            errors.append(
                f"{rel}: directory name {source.parent.name!r} != name {name!r}"
            )
        if name in seen:
            errors.append(f"{rel}: duplicate skill name {name!r} (flat namespace)")
        seen.add(name)
        if not str(doc.meta.get("description", "")).strip():
            errors.append(f"{rel}: 'description' is required")

        for link in LINK.findall(doc.body):
            if link.startswith(SKIP_LINK_PREFIXES):
                continue
            target = (source.parent / link.split("#", 1)[0]).resolve()
            if link.split("#", 1)[0] and not target.exists():
                errors.append(f"{rel}: broken local link: {link}")
    return errors


def warnings(root: Path) -> list[str]:
    """Non-blocking findings (language, description size)."""
    notes: list[str] = []
    for source in discover_skills(root):
        rel = source.relative_to(root).as_posix()
        try:
            doc = parse(source.read_text(encoding="utf-8"))
        except FrontmatterError:
            continue
        description = str(doc.meta.get("description", "")).strip()
        if len(description) > DESCRIPTION_WARN_LEN:
            notes.append(f"{rel}: description is {len(description)} chars (> {DESCRIPTION_WARN_LEN})")
        sample = f"{description} {doc.body}"
        if any(marker in sample for marker in PT_MARKERS):
            notes.append(f"{rel}: non-English markers detected (ADR-0001; translate at import)")
    return notes
