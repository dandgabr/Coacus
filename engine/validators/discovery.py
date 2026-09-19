"""Validate generated discovery manifests (``.agents/*.json``, ADR-0006).

The manifests are generated, so the validator recomputes the source
fingerprint rather than trusting the stored value: a tampered or stale entry
must fail here even before the drift check runs.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

REQUIRED_KEYS = ("name", "description", "category", "source", "dist", "fingerprint")


def validate(root: Path) -> list[str]:
    """Return a list of error strings; empty list means valid."""
    errors: list[str] = []
    manifest_dir = root / ".agents"
    if not manifest_dir.is_dir():
        return errors

    for manifest in sorted(manifest_dir.glob("*.json")):
        rel = manifest.relative_to(root).as_posix()
        try:
            entry = json.loads(manifest.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError) as exc:
            errors.append(f"{rel}: unreadable manifest ({exc})")
            continue
        if not isinstance(entry, dict):
            errors.append(f"{rel}: manifest must be a JSON object")
            continue
        for key in REQUIRED_KEYS:
            if key not in entry:
                errors.append(f"{rel}: missing key {key!r}")
        name = str(entry.get("name", ""))
        if manifest.stem != name:
            errors.append(f"{rel}: file stem {manifest.stem!r} != name {name!r}")
        source = root / str(entry.get("source", ""))
        if not source.is_file():
            errors.append(f"{rel}: source does not exist: {entry.get('source')!r}")
            continue
        fingerprint = hashlib.sha256(source.read_bytes()).hexdigest()[:16]
        if entry.get("fingerprint") != fingerprint:
            errors.append(f"{rel}: fingerprint mismatch (stale discovery entry)")
        dist = root / str(entry.get("dist", ""))
        if not dist.is_dir():
            errors.append(f"{rel}: dist directory does not exist: {entry.get('dist')!r}")
    return errors
