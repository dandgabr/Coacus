"""Prose-count reconciliation (D5 — counts are measured, never copied).

Prose drifts. The documentation states counts — skills, agents, workflows, MCPs,
catalog entries, provenance entries — that the generator and the lock file already
know, and hand-copied numbers fall behind the disk. This validator reconciles
every declared number (a) in the README corpus table and (b) anywhere in the
LIVING documentation, so a stale count is a build error rather than a silent lie.

Measured sources: the generated ``catalog/catalog.json`` counts, the on-disk
``methodology/workflows`` tree, and the entry count of ``sources.lock.json``.

Historical records are exempt by design: ``CHANGELOG.md`` and ``docs/migration.md``
describe past states, and ``docs/roadmap.md`` marks a past state with an "as of
F<n>" era, so a paragraph that is explicitly historical is not reconciled.

Counts have no generator (the test suite), so they are never stated as a fixed
number in the docs; the docs give the command to measure them instead.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

README = "README.md"
CATALOG = "catalog/catalog.json"
LOCK = "sources.lock.json"

# Markdown table row: | Skills | 273 | ...
ROW = re.compile(r"^\|\s*(Skills|Agents|Workflows|MCPs|Catalog|Provenance)\s*\|\s*(\d+)")

# (b) Prose scan over living docs. Longest, most specific tokens come first so
# that "288 skill entries" is not partially matched as "288 skill".
COUNT_TOKEN = re.compile(
    r"\b(\d+)\s+"
    r"(catalog skill entries?|skill entries?|repo skills?|knowledge skills?|"
    r"process workflows?|provenance entries?|agents?|MCPs?|workflows?|skills?)\b"
)
TOKEN_KEY = {
    "catalog skill entries": "catalog",
    "catalog skill entry": "catalog",
    "skill entries": "catalog",
    "skill entry": "catalog",
    "repo skills": "catalog",
    "repo skill": "catalog",
    "knowledge skills": "knowledge",
    "knowledge skill": "knowledge",
    "skills": "knowledge",
    "skill": "knowledge",
    "process workflows": "workflows",
    "process workflow": "workflows",
    "workflows": "workflows",
    "workflow": "workflows",
    "agents": "agents",
    "agent": "agents",
    "MCPs": "mcps",
    "MCP": "mcps",
    "provenance entries": "provenance",
    "provenance entry": "provenance",
}

# Living docs are reconciled. Records of past states are not.
LIVING_FILES = (
    "README.md",
    "CONTRIBUTING.md",
    "evals/README.md",
    "docs/architecture.md",
    "docs/usage.md",
    "docs/install.md",
    "docs/extending.md",
    "docs/roadmap.md",
)
LIVING_DIRS = ("docs/standards",)

# A paragraph naming a past state explicitly is history, not a current claim.
HISTORICAL = re.compile(
    r"(as of F\d|delivered \(as of|F\d+ corpus|reconciled with the shipped|"
    r"\b199 \+ 15\b|\b214 catalog\b|\b208 catalog\b)",
    re.IGNORECASE,
)


def _load(path: Path) -> dict:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return data if isinstance(data, dict) else {}


def _measured(root: Path) -> dict[str, int]:
    catalog = _load(root / CATALOG).get("counts", {})
    workflows = len(list((root / "methodology" / "workflows").rglob("SKILL.md")))
    knowledge_skills = max(int(catalog.get("skills", 0)) - workflows, 0)
    lock = _load(root / LOCK)
    return {
        "Skills": knowledge_skills,
        "Agents": int(catalog.get("agents", 0)),
        "Workflows": workflows,
        "MCPs": int(catalog.get("mcps", 0)),
        "Catalog": int(catalog.get("skills", 0)),
        "Provenance": len(lock.get("entries", [])),
    }


def _key_for_token(token: str) -> str | None:
    return TOKEN_KEY.get(token)


def _living_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for rel in LIVING_FILES:
        path = root / rel
        if path.is_file():
            files.append(path)
    for rel in LIVING_DIRS:
        directory = root / rel
        if directory.is_dir():
            files.extend(sorted(directory.glob("*.md")))
    return files


def _table_errors(root: Path, measured: dict[str, int]) -> list[str]:
    readme = root / README
    if not readme.is_file():
        return []
    errors: list[str] = []
    seen: set[str] = set()
    for line in readme.read_text(encoding="utf-8").splitlines():
        match = ROW.match(line)
        if not match:
            continue
        label, declared = match.group(1), int(match.group(2))
        if label in seen or label not in measured:
            continue
        seen.add(label)
        expected = measured[label]
        if declared != expected:
            errors.append(
                f"{README}: corpus table '{label}' says {declared}, disk says "
                f"{expected} (D5 — counts are measured, never copied)"
            )
    return errors


def _prose_errors(root: Path, measured: dict[str, int]) -> list[str]:
    errors: list[str] = []
    for path in _living_files(root):
        rel = path.relative_to(root).as_posix()
        paragraphs = re.split(r"\n\s*\n", path.read_text(encoding="utf-8"))
        for paragraph in paragraphs:
            if HISTORICAL.search(paragraph):
                continue
            for match in COUNT_TOKEN.finditer(paragraph):
                key = _key_for_token(match.group(2).lower())
                label = {
                    "knowledge": "Skills",
                    "workflows": "Workflows",
                    "catalog": "Catalog",
                    "agents": "Agents",
                    "mcps": "MCPs",
                    "provenance": "Provenance",
                }.get(key or "")
                if label is None:
                    continue
                declared = int(match.group(1))
                expected = measured[label]
                if declared != expected:
                    errors.append(
                        f"{rel}: '{match.group(0)}' says {declared}, disk says "
                        f"{expected} (D5 — counts are measured, never copied)"
                    )
    return errors


def validate(root: Path) -> list[str]:
    """Return prose-count mismatches (empty = docs agree with disk)."""
    measured = _measured(root)
    return _table_errors(root, measured) + _prose_errors(root, measured)
