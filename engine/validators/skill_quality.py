"""Skill-quality lint beyond the structural contract (skill-authoring).

The structural validator (:mod:`engine.validators.skills`) checks placement,
naming and link resolution. This module checks the authoring-quality contract
that has signal on this corpus:

- ERRORS (safe on the current corpus, catch a regression):
  - ``name`` longer than the Agent Skills limit (64 chars);
  - an unbalanced code fence (a ``` block that is never closed).
- WARNINGS (non-blocking):
  - a body over the word budget — depth belongs in ``references/``;
  - a ``description`` that opens with an instruction-to-reader instead of a
    third-person trigger description.

The resource-pointer and duplication disciplines are GUIDANCE in
``docs/standards/skill-authoring.md``, not checks: the corpus links reference
directories by name rather than every file, so a per-file pointer check would
fire on hundreds of valid skills and carry no signal.
"""

from __future__ import annotations

import re
from pathlib import Path

from engine.frontmatter import FrontmatterError, parse
from engine.validators.skills import discover_skills

NAME_MAX = 64
BODY_WORD_WARN = 3500
BAD_DESCRIPTION_OPENER = re.compile(r"(?i)^\s*(use this skill|load when)\b")


def _fence_lines(body: str) -> int:
    """Number of lines that open or close a fenced code block."""
    return sum(1 for line in body.splitlines() if line.lstrip().startswith("```"))


def validate(root: Path) -> list[str]:
    """Return blocking quality errors; empty means clean."""
    errors: list[str] = []
    for source in discover_skills(root):
        rel = source.relative_to(root).as_posix()
        try:
            doc = parse(source.read_text(encoding="utf-8"))
        except FrontmatterError:
            continue
        name = str(doc.meta.get("name", ""))
        if len(name) > NAME_MAX:
            errors.append(
                f"{rel}: 'name' is {len(name)} chars (max {NAME_MAX}, Agent Skills spec)"
            )
        if _fence_lines(doc.body) % 2:
            errors.append(
                f"{rel}: unbalanced code fence — a ``` block is never closed "
                "(content after it is swallowed)"
            )
    return errors


def warnings(root: Path) -> list[str]:
    """Return non-blocking quality findings; empty means clean."""
    notes: list[str] = []
    for source in discover_skills(root):
        rel = source.relative_to(root).as_posix()
        try:
            doc = parse(source.read_text(encoding="utf-8"))
        except FrontmatterError:
            continue
        words = len(doc.body.split())
        if words > BODY_WORD_WARN:
            notes.append(
                f"{rel}: body is {words} words (> {BODY_WORD_WARN}); move depth into "
                "references/ (skill-authoring)"
            )
        description = str(doc.meta.get("description", "")).strip()
        if BAD_DESCRIPTION_OPENER.match(description):
            notes.append(
                f"{rel}: description opens with an instruction-to-reader; write a "
                "third-person, trigger-oriented description (skill-authoring)"
            )
    return notes
