"""Validate the routing index and its curated lexicon (routing).

``.agents/routing.json`` is generated; this validator checks:

- every canonical agent has exactly one entry and vice versa;
- each entry carries the required keys with the right types;
- the curated lexicon (``knowledge/routing/lexicon.json``) covers every agent
  and names none that does not exist, so a rename cannot silently drop a
  vocabulary;
- trigger terms are lowercase and non-empty.

The drift check (``python3 scripts/coacus.py check``) proves the committed index
matches a fresh regeneration; this validator proves the data is coherent.
"""

from __future__ import annotations

import json
from pathlib import Path

from engine.generators.agent_manifests import discover_sources as discover_agent_sources
from engine.generators.routing import LEXICON_PATH, ROUTING_PATH

ENTRY_KEYS = ("name", "category", "description", "skills", "triggers")


def _load(path: Path) -> dict | None:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    return data if isinstance(data, dict) else None


def _agent_names(root: Path) -> set[str]:
    names: set[str] = set()
    for source in discover_agent_sources(root):
        from engine.frontmatter import parse

        names.add(str(parse(source.read_text(encoding="utf-8")).meta.get("name", "")))
    return names


def validate_sources(root: Path) -> list[str]:
    """Source contract: the curated lexicon is present and coherent.

    Runs in ``source_errors`` (before ``generate``); it never reads the generated
    index, so a missing/regenerating ``.agents/routing.json`` cannot deadlock
    generation.
    """
    errors: list[str] = []

    lexicon_path = root / LEXICON_PATH
    if not lexicon_path.is_file():
        errors.append(f"{LEXICON_PATH}: missing (the router needs its trigger lexicon)")
        return errors
    lexicon = _load(lexicon_path)
    if lexicon is None or not isinstance(lexicon.get("agents"), dict):
        errors.append(f"{LEXICON_PATH}: needs an 'agents' object")
        return errors
    lexicon_agents: dict = lexicon["agents"]
    for name, terms in lexicon_agents.items():
        if not isinstance(terms, list):
            errors.append(f"{LEXICON_PATH}: '{name}' triggers must be a list")
            continue
        for term in terms:
            if not isinstance(term, str) or not term.strip():
                errors.append(f"{LEXICON_PATH}: '{name}' has an empty trigger")
            elif term != term.lower():
                errors.append(f"{LEXICON_PATH}: '{name}' trigger {term!r} must be lowercase")

    agents = _agent_names(root)
    for name in sorted(agents - set(lexicon_agents)):
        errors.append(f"{LEXICON_PATH}: no triggers for agent {name!r}")
    for name in sorted(set(lexicon_agents) - agents):
        errors.append(f"{LEXICON_PATH}: triggers for unknown agent {name!r}")
    return errors


def validate_index(root: Path) -> list[str]:
    """Artifact contract: the generated routing index matches the agents.

    Runs in ``artifact_errors`` (after generation / on ``validate``).
    """
    errors: list[str] = []
    agents = _agent_names(root)
    routing_path = root / ROUTING_PATH
    if not routing_path.is_file():
        errors.append(f"{ROUTING_PATH}: missing (run generate)")
        return errors
    routing = _load(routing_path)
    if routing is None or not isinstance(routing.get("entries"), list):
        errors.append(f"{ROUTING_PATH}: needs an 'entries' list")
        return errors

    seen: set[str] = set()
    for index, entry in enumerate(routing["entries"]):
        if not isinstance(entry, dict):
            errors.append(f"{ROUTING_PATH}: entry {index} must be an object")
            continue
        for key in ENTRY_KEYS:
            if key not in entry:
                errors.append(f"{ROUTING_PATH}: entry {index} missing {key!r}")
        name = str(entry.get("name", ""))
        if name in seen:
            errors.append(f"{ROUTING_PATH}: duplicate agent {name!r}")
        seen.add(name)
        if not isinstance(entry.get("skills"), list):
            errors.append(f"{ROUTING_PATH}: {name!r} skills must be a list")
        if not isinstance(entry.get("triggers"), list):
            errors.append(f"{ROUTING_PATH}: {name!r} triggers must be a list")

    for name in sorted(agents - seen):
        errors.append(f"{ROUTING_PATH}: no entry for agent {name!r}")
    for name in sorted(seen - agents):
        errors.append(f"{ROUTING_PATH}: entry for unknown agent {name!r}")
    return errors


def validate(root: Path) -> list[str]:
    """Full contract: curated lexicon (source) plus the generated index (artifact)."""
    return validate_sources(root) + validate_index(root)
