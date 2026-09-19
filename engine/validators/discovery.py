"""Validate generated discovery manifests (ADR-0006).

Two kinds live under ``.agents/``:

- per-agent entries ``entries/<name>.json``: ``{name, description, category,
  source, dist, fingerprint}`` — the fingerprint is RECOMPUTED from the source
  bytes, so a tampered or stale entry fails even before the drift check. The
  ``entries/`` subdirectory keeps agent names from colliding with the
  consolidated stems.
- consolidated by-kind indexes ``skills.json`` / ``mcps.json`` / ``agents.json``:
  ``{entries: [{path}]}`` — the coarse single-scan surface.
"""

from __future__ import annotations

import hashlib
import json
import re
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
    source_rel = str(entry.get("source", ""))
    if _unsafe_path(source_rel):
        errors.append(f"{rel}: 'source' must be a relative in-repo path: {source_rel!r}")
        return
    source = root / source_rel
    if not source.is_file():
        errors.append(f"{rel}: source does not exist: {source_rel!r}")
        return
    fingerprint = hashlib.sha256(source.read_bytes()).hexdigest()[:16]
    if entry.get("fingerprint") != fingerprint:
        errors.append(f"{rel}: fingerprint mismatch (stale discovery entry)")
    dist_rel = str(entry.get("dist", ""))
    if _unsafe_path(dist_rel):
        errors.append(f"{rel}: 'dist' must be a relative in-repo path: {dist_rel!r}")
        return
    dist = root / dist_rel
    if not dist.is_dir():
        errors.append(f"{rel}: dist directory does not exist: {dist_rel!r}")


def _unsafe_path(value: str) -> bool:
    """Absolute, empty, or upward-escaping paths are unsafe to join onto root."""
    if not value:
        return True
    if value.startswith(("/", "~")) or re.match(r"^[A-Za-z]:[/\\]", value):
        return True
    return ".." in Path(value).parts


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
    agents_dir = root / ".agents"
    if not agents_dir.is_dir():
        return errors

    # Consolidated by-kind indexes live directly under .agents/.
    for name in CONSOLIDATED:
        manifest = agents_dir / f"{name}.json"
        if manifest.is_file():
            _validate_consolidated(manifest, manifest.relative_to(root).as_posix(), errors)

    # Per-agent manifests live under .agents/entries/ (no stem collision).
    entries_dir = agents_dir / "entries"
    if entries_dir.is_dir():
        for manifest in sorted(entries_dir.glob("*.json")):
            _validate_per_agent(
                root, manifest, manifest.relative_to(root).as_posix(), errors
            )
    return errors
