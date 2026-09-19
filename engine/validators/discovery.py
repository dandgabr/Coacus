"""Validate generated discovery manifests (ADR-0006).

Two kinds live under ``.agents/``:

- per-agent entries ``<name>.json``: ``{name, description, category, source,
  dist, fingerprint}`` — the fingerprint is RECOMPUTED from the source bytes,
  so a tampered or stale entry fails even before the drift check.
- consolidated by-kind indexes ``skills.json`` / ``mcps.json`` / ``agents.json``:
  ``{entries: [{path}]}`` — the coarse single-scan surface.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

PER_AGENT_KEYS = ("name", "description", "category", "source", "dist", "fingerprint")
CONSOLIDATED = ("skills", "mcps", "agents")


def _validate_per_agent(root: Path, manifest: Path, rel: str, errors: list[str]) -> None:
    try:
        entry = json.loads(manifest.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        errors.append(f"{rel}: unreadable manifest ({exc})")
        return
    if not isinstance(entry, dict):
        errors.append(f"{rel}: manifest must be a JSON object")
        return
    for key in PER_AGENT_KEYS:
        if key not in entry:
            errors.append(f"{rel}: missing key {key!r}")
    name = str(entry.get("name", ""))
    if manifest.stem != name:
        errors.append(f"{rel}: file stem {manifest.stem!r} != name {name!r}")
    source = root / str(entry.get("source", ""))
    if not source.is_file():
        errors.append(f"{rel}: source does not exist: {entry.get('source')!r}")
        return
    fingerprint = hashlib.sha256(source.read_bytes()).hexdigest()[:16]
    if entry.get("fingerprint") != fingerprint:
        errors.append(f"{rel}: fingerprint mismatch (stale discovery entry)")
    dist = root / str(entry.get("dist", ""))
    if not dist.is_dir():
        errors.append(f"{rel}: dist directory does not exist: {entry.get('dist')!r}")


def _validate_consolidated(manifest: Path, rel: str, errors: list[str]) -> None:
    try:
        data = json.loads(manifest.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        errors.append(f"{rel}: unreadable manifest ({exc})")
        return
    if not isinstance(data, dict) or not isinstance(data.get("entries"), list):
        errors.append(f"{rel}: consolidated manifest needs an 'entries' list")
        return
    for index, entry in enumerate(data["entries"]):
        if not isinstance(entry, dict) or "path" not in entry:
            errors.append(f"{rel}: entry {index} needs a 'path'")
        elif not str(entry["path"]).strip():
            errors.append(f"{rel}: entry {index} has an empty 'path'")


def validate(root: Path) -> list[str]:
    """Return a list of error strings; empty list means valid."""
    errors: list[str] = []
    manifest_dir = root / ".agents"
    if not manifest_dir.is_dir():
        return errors

    for manifest in sorted(manifest_dir.glob("*.json")):
        rel = manifest.relative_to(root).as_posix()
        if manifest.stem in CONSOLIDATED:
            _validate_consolidated(manifest, rel, errors)
        else:
            _validate_per_agent(root, manifest, rel, errors)
    return errors
