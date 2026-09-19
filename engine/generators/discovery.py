"""Generate consolidated discovery manifests from disk (D5/ADR-0006).

Writes `.agents/{skills,mcps,agents}.json` — each a list of `entries[].path`
(a directory or source file), derived purely from disk so discovery is
deterministic and drift-checked (ADR-0014). Single-scan rule: agents read these
indexes once per session (AGENTS.md).

The per-agent `.agents/entries/<name>.json` files are still produced by
`agent_manifests` (fine-grained fingerprints); these consolidated manifests are
the coarse by-kind index.
"""

from __future__ import annotations

import json
from pathlib import Path

from engine.generators.mcp_configs import discover_sources as discover_mcp_sources
from engine.generators.agent_manifests import discover_sources as discover_agent_sources

SKILL_ROOTS = ("knowledge/skills", "methodology/workflows")
MANIFESTS = ("skills", "mcps", "agents")


def _entries(root: Path, paths: list[Path]) -> dict:
    return {"entries": [{"path": p.relative_to(root).as_posix()} for p in paths]}


def build(root: Path) -> dict[str, dict]:
    skills: list[Path] = []
    for top in SKILL_ROOTS:
        base = root / top
        if base.is_dir():
            skills.extend(sorted(p.parent for p in base.rglob("SKILL.md")))
    mcps = [source.parent for source in discover_mcp_sources(root)]
    agents = [source.parent for source in discover_agent_sources(root)]
    return {
        "skills": _entries(root, skills),
        "mcps": _entries(root, sorted(mcps)),
        "agents": _entries(root, sorted(agents)),
    }


def _expected(root: Path) -> dict[str, str]:
    data = build(root)
    return {
        f".agents/{name}.json": json.dumps(data[name], indent=2) + "\n"
        for name in MANIFESTS
    }


def write_all(root: Path) -> list[str]:
    written: list[str] = []
    for rel, content in _expected(root).items():
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        written.append(rel)
    return sorted(written)


def check(root: Path) -> list[str]:
    """Drift check for the consolidated discovery manifests (ADR-0014)."""
    drift: list[str] = []
    for rel, content in _expected(root).items():
        path = root / rel
        if not path.is_file():
            drift.append(f"{rel}: missing (run generate)")
        elif path.read_text(encoding="utf-8") != content:
            drift.append(f"{rel}: out of date (run generate)")
    return drift
