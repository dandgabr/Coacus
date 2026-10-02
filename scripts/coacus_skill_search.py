#!/usr/bin/env python3
"""Find a canonical Coacus skill without loading every skill into model context."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from engine.frontmatter import parse  # noqa: E402


@dataclass(frozen=True)
class Skill:
    """One validated skill entry from the canonical catalog."""

    name: str
    path: Path
    description: str


def load_skills(root: Path) -> list[Skill]:
    """Read and validate the generated index and its canonical skill paths."""
    root = root.resolve()
    try:
        data = json.loads((root / "catalog/catalog.json").read_text(encoding="utf-8"))
        entries = data["skills"]
        if not isinstance(entries, list):
            raise TypeError("skills must be an array")
    except (OSError, ValueError, KeyError, TypeError) as exc:
        raise ValueError(f"invalid skill catalog: {exc}") from exc

    skills: list[Skill] = []
    for entry in entries:
        try:
            name = entry["name"]
            raw_path = Path(entry["path"])
            if not isinstance(name, str) or raw_path.is_absolute():
                raise ValueError("invalid skill name or path")
            path = (root / raw_path).resolve()
            if not path.is_relative_to(root):
                raise ValueError(f"skill path outside repository: {raw_path}")
            if path.name != "SKILL.md" or not path.is_file():
                raise ValueError(f"missing SKILL.md: {raw_path}")
            doc = parse(path.read_text(encoding="utf-8"))
            if doc.meta.get("name") != name:
                raise ValueError(f"skill name differs from catalog: {raw_path}")
            description = " ".join(str(doc.meta.get("description", "")).split())
            skills.append(Skill(name, path, description))
        except (KeyError, TypeError, OSError) as exc:
            raise ValueError(f"invalid skill catalog entry: {entry!r}: {exc}") from exc
    return skills


def search(root: Path, query: str, top: int = 10) -> list[Skill]:
    """Rank matching skills; prefer full-query and name matches."""
    terms = re.findall(r"[\w]+", query.casefold())
    if not terms or top < 1:
        raise ValueError("search needs words and a positive --top")
    scored: list[tuple[int, Skill]] = []
    for skill in load_skills(root):
        name = skill.name.casefold()
        description = skill.description.casefold()
        hits = [term for term in terms if term in name or term in description]
        if hits:
            score = (100 if len(hits) == len(terms) else 0) + sum(
                3 if term in name else 1 for term in hits
            )
            scored.append((score, skill))
    scored.sort(key=lambda item: (-item[0], item[1].name))
    return [skill for _, skill in scored[:top]]


def show(root: Path, name: str) -> Skill:
    """Resolve an exact canonical skill name, rejecting ambiguity."""
    matches = [skill for skill in load_skills(root) if skill.name == name]
    if not matches:
        raise ValueError(f"unknown skill: {name}")
    if len(matches) != 1:
        raise ValueError(f"ambiguous skill: {name}")
    return matches[0]


def main(argv: list[str] | None = None) -> int:
    """Run the search or exact-name command and return a CLI status code."""

    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="action", required=True)
    search_parser = sub.add_parser("search", help="search names and descriptions")
    search_parser.add_argument("query", nargs="+", help="words to search")
    search_parser.add_argument("--top", type=int, default=10)
    show_parser = sub.add_parser("show", help="resolve one exact name")
    show_parser.add_argument("name")
    args = parser.parse_args(argv)
    try:
        if args.action == "show":
            print(show(ROOT, args.name).path)
        else:
            for skill in search(ROOT, " ".join(args.query), args.top):
                summary = (
                    skill.description[:197] + "..."
                    if len(skill.description) > 200
                    else skill.description
                )
                print(f"{skill.name}\t{skill.path}\t{summary}")
    except ValueError as exc:
        print(f"coacus-skill-search: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
