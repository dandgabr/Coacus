"""Validate that every canonical agent has one exclusive specialty (agent-roles).

An agent is one role on one domain. Three machine-checkable consequences:

- the body carries a ``## Responsibility boundaries`` section, so a reader and a
  router can tell what the agent does not own;
- every owner named in backticks in that section is an agent that exists, so a
  retired or renamed agent cannot linger as an owner;
- no agent's skills are (almost) wholly contained in another agent's skills,
  which is how two roles that should be one (or one a subset of the other)
  show up in the data. Baseline practice skills that nearly every agent loads
  do not count towards the overlap.
"""

from __future__ import annotations

import itertools
import re
from pathlib import Path

from engine.frontmatter import FrontmatterError, parse
from engine.generators.agent_manifests import discover_sources

BOUNDARIES_HEADING = re.compile(r"^##\s+(?:\S+\s+)?Responsibility boundaries\s*$", re.M)
NEXT_SECTION = re.compile(r"^(?:## |---\s*$)", re.M)
BACKTICKED = re.compile(r"`([a-z0-9]+(?:-[a-z0-9]+)*)`")

# Practice skills loaded by nearly every agent; sharing them says nothing about role overlap.
BASELINE_SKILLS = frozenset(
    {"version-freshness", "clean-code-reusability", "security-privacy"}
)
MIN_SKILLS_FOR_OVERLAP = 5
MAX_CONTAINMENT = 0.9


def _section(body: str) -> str | None:
    match = BOUNDARIES_HEADING.search(body)
    if match is None:
        return None
    rest = body[match.end():]
    following = NEXT_SECTION.search(rest)
    return rest[: following.start()] if following else rest


def _owners(section: str) -> list[str]:
    """Backticked agent names in the last cell of each table row."""
    owners: list[str] = []
    for line in section.splitlines():
        if not line.lstrip().startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) >= 2:
            owners.extend(BACKTICKED.findall(cells[-1]))
    return owners


def _skill_name(path: str) -> str:
    return path.rstrip("/").split("/")[-2] if path.endswith("SKILL.md") else path


def validate(root: Path) -> list[str]:
    """Return a list of error strings; empty list means valid."""
    errors: list[str] = []
    names: set[str] = set()
    parsed: list[tuple[str, str, str, set[str]]] = []

    for source in discover_sources(root):
        rel = source.relative_to(root).as_posix()
        try:
            doc = parse(source.read_text(encoding="utf-8"))
        except FrontmatterError:
            continue  # the agent validator reports the frontmatter problem
        name = str(doc.meta.get("name", ""))
        names.add(name)
        skills = {
            _skill_name(str(s))
            for s in doc.meta.get("skills", []) or []
            if isinstance(s, str)
        } - BASELINE_SKILLS
        parsed.append((name, rel, doc.body, skills))

    for name, rel, body, _ in parsed:
        section = _section(body)
        if section is None:
            errors.append(
                f"{rel}: missing a '## Responsibility boundaries' section naming what "
                "the agent does not own and who does (agent-roles)"
            )
            continue
        for owner in _owners(section):
            if owner not in names:
                errors.append(
                    f"{rel}: responsibility boundaries name '{owner}', "
                    "which is not an existing agent (agent-roles)"
                )

    for (a, rel_a, _, skills_a), (b, rel_b, _, skills_b) in itertools.combinations(
        sorted(parsed), 2
    ):
        smaller = min(len(skills_a), len(skills_b))
        if smaller < MIN_SKILLS_FOR_OVERLAP:
            continue
        shared = len(skills_a & skills_b)
        if shared / smaller >= MAX_CONTAINMENT:
            errors.append(
                f"{rel_a}: skills of '{a}' and '{b}' overlap {shared}/{smaller} "
                f"(>= {MAX_CONTAINMENT:.0%} of the smaller set); merge the roles or give "
                f"each exclusive skills (agent-roles, also {rel_b})"
            )
    return errors
