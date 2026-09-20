"""Generate the routing index from the canonical agents plus the curated lexicon.

Writes ``.agents/routing.json``: for every agent, its canonical facts (name,
category, description, skills) merged with the curated bilingual trigger terms
from ``knowledge/routing/lexicon.json``. The router (``engine/router.py``) reads
this single file, so selection never re-scans directories per turn (discovery,
single-scan).

Deterministic and timestamp-free, like every other generated artifact
(generated-artifacts): ``check`` verifies idempotency.
"""

from __future__ import annotations

import json
from pathlib import Path

from engine.frontmatter import parse
from engine.generators.agent_manifests import discover_sources as discover_agent_sources

ROUTING_PATH = ".agents/routing.json"
LEXICON_PATH = "knowledge/routing/lexicon.json"


def _load_lexicon(root: Path) -> dict[str, list[str]]:
    path = root / LEXICON_PATH
    if not path.is_file():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    agents = data.get("agents", {}) if isinstance(data, dict) else {}
    return agents if isinstance(agents, dict) else {}


def build(root: Path) -> dict:
    """Build the routing index: one entry per agent, sorted by name."""
    lexicon = _load_lexicon(root)
    entries: list[dict] = []
    for source in discover_agent_sources(root):
        doc = parse(source.read_text(encoding="utf-8"))
        name = str(doc.meta.get("name", "")).strip()
        skills = [
            str(s) for s in doc.meta.get("skills", []) if isinstance(doc.meta.get("skills"), list)
        ]
        triggers = [str(t).strip().lower() for t in lexicon.get(name, []) if str(t).strip()]
        entries.append(
            {
                "name": name,
                "category": str(doc.meta.get("category", "")).strip(),
                "description": str(doc.meta.get("description", "")).strip(),
                "skills": skills,
                "triggers": sorted(set(triggers)),
            }
        )
    entries.sort(key=lambda item: item["name"])
    return {"schema": 1, "entries": entries}


def _expected(root: Path) -> dict[str, str]:
    return {
        ROUTING_PATH: json.dumps(build(root), indent=2) + "\n",
    }


def write_all(root: Path) -> list[str]:
    """Materialize ``.agents/routing.json``; return the written path."""
    written: list[str] = []
    for rel, content in _expected(root).items():
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        written.append(rel)
    return written


def check(root: Path) -> list[str]:
    """Drift check for the routing index (generated-artifacts)."""
    drift: list[str] = []
    for rel, content in _expected(root).items():
        path = root / rel
        if not path.is_file():
            drift.append(f"{rel}: missing (run generate)")
        elif path.read_text(encoding="utf-8") != content:
            drift.append(f"{rel}: out of date (run generate)")
    return drift
