"""Validate canonical skill sources (D2/ADR-0003, corpus import contract).

Skills live under two roots sharing one flat name namespace:

- ``knowledge/skills/<category>[/<subcategory>]/<skill>/SKILL.md``
- ``methodology/workflows/<skill>/SKILL.md`` (process skills)

Errors: frontmatter parses; ``name`` is kebab-case and equals the directory;
``description`` present; globally unique slug; correct placement; no nested
SKILL.md; local markdown links resolve.

Warnings (non-blocking): non-English markers and oversized descriptions.
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

# root -> allowed depth (number of parts from the root to the skill dir)
SKILL_ROOTS: dict[str, tuple[int, ...]] = {
    "knowledge/skills": (2, 3),  # <category>[/<subcategory>]/<skill>
    "methodology/workflows": (1,),  # <skill>
}


def _root_for(source: Path, root: Path) -> tuple[str, Path] | None:
    for top in SKILL_ROOTS:
        base = root / top
        try:
            source.relative_to(base)
        except ValueError:
            continue
        return top, base
    return None


def discover_skills(root: Path) -> list[Path]:
    """All ``SKILL.md`` under every skill root."""
    found: list[Path] = []
    for top in SKILL_ROOTS:
        base = root / top
        if base.is_dir():
            found.extend(sorted(base.rglob("SKILL.md")))
    return found


def validate(root: Path) -> list[str]:
    """Return a list of error strings; empty list means valid."""
    errors: list[str] = []
    discovered = discover_skills(root)
    skill_dirs = {source.parent for source in discovered}
    seen: set[str] = set()

    for source in discovered:
        rel = source.relative_to(root).as_posix()
        located = _root_for(source, root)
        if located is None:
            errors.append(f"{rel}: SKILL.md is outside a known skill root")
            continue
        _, base = located
        parts = source.relative_to(base).parts
        allowed = SKILL_ROOTS[located[0]]

        ancestor = source.parent.parent
        nested = False
        while ancestor != base.parent and ancestor != base:
            if ancestor in skill_dirs:
                errors.append(
                    f"{rel}: nested SKILL.md beneath {ancestor.name!r} (not allowed)"
                )
                nested = True
                break
            ancestor = ancestor.parent
        if nested:
            continue

        if len(parts) - 1 not in allowed:  # minus the SKILL.md filename
            errors.append(
                f"{rel}: SKILL.md must live at the right depth for "
                f"'{located[0]}' (expected {allowed})"
            )
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
            notes.append(
                f"{rel}: description is {len(description)} chars (> {DESCRIPTION_WARN_LEN})"
            )
        sample = f"{description} {doc.body}"
        if any(marker in sample for marker in PT_MARKERS):
            notes.append(
                f"{rel}: non-English markers detected (ADR-0001; translate at import)"
            )
    return notes
