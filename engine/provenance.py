"""Provenance manifest for imported artifacts (P4 / provenance).

Lives at the repository root as ``sources.lock.json`` — deliberately OUTSIDE
the generated ``catalog/`` surface so that the per-import ``imported_at``
timestamp cannot break the generated-artifacts drift check (the catalog generator must
stay timestamp-free and idempotent).

This module owns the schema and the (empty) seed. The F6 import pipeline
populates entries; nothing here writes timestamps at generation time.
"""

from __future__ import annotations

import json
from pathlib import Path

LOCK_PATH = "sources.lock.json"
SCHEMA = 1

REQUIRED_ENTRY_KEYS = (
    "source_repo",
    "source_commit",
    "source_path",
    "source_sha256",
    "target_path",
    "target_sha256",
    "origin_license",
    "transform",
    "import_run_id",
    "imported_at",
)

# Optional per-entry key: searchable aliases created by import-time renames.
OPTIONAL_ENTRY_KEYS = ("aliases",)


def empty() -> dict:
    """Seed structure, deterministic (no timestamp)."""
    return {"schema": SCHEMA, "entries": []}


def load(root: Path) -> dict:
    """Read the manifest, or return the empty seed if absent."""
    path = root / LOCK_PATH
    if not path.is_file():
        return empty()
    return json.loads(path.read_text(encoding="utf-8"))


def validate(root: Path) -> list[str]:
    """Check the manifest shape; entries may be empty pre-import."""
    errors: list[str] = []
    path = root / LOCK_PATH
    if not path.is_file():
        return errors
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        return [f"{LOCK_PATH}: unreadable manifest ({exc})"]
    if not isinstance(data, dict):
        return [f"{LOCK_PATH}: manifest root must be a JSON object"]
    if data.get("schema") != SCHEMA:
        errors.append(f"{LOCK_PATH}: unsupported schema {data.get('schema')!r}")
    entries = data.get("entries", [])
    if not isinstance(entries, list):
        errors.append(f"{LOCK_PATH}: 'entries' must be a list")
        return errors
    for index, entry in enumerate(entries):
        if not isinstance(entry, dict):
            errors.append(f"{LOCK_PATH}: entry {index} must be a JSON object")
            continue
        for key in REQUIRED_ENTRY_KEYS:
            if key not in entry:
                errors.append(f"{LOCK_PATH}: entry {index} missing {key!r}")
        if "aliases" in entry and not isinstance(entry["aliases"], list):
            errors.append(f"{LOCK_PATH}: entry {index} 'aliases' must be a list")
        target = root / str(entry.get("target_path", ""))
        if entry.get("target_path") and not target.is_file():
            errors.append(
                f"{LOCK_PATH}: entry {index} target does not exist: {entry['target_path']!r}"
            )
            continue
        # Drift key: the recorded content hash of the target must match disk
        # (provenance.md, "Drift key"). A hand-edited imported file that never
        # re-ran the import leaves the lock lying about the corpus.
        recorded = entry.get("target_sha256")
        if entry.get("target_path") and recorded and recorded != _sha256(target):
            errors.append(
                f"{LOCK_PATH}: entry {index} target_sha256 mismatch for "
                f"{entry['target_path']!r} (run: python3 scripts/coacus.py refresh)"
            )
    return errors


def write(root: Path, data: dict | None = None) -> Path:
    """Write the manifest (seed by default). Import pipeline supplies entries."""
    path = root / LOCK_PATH
    path.write_text(
        json.dumps(data or empty(), indent=2) + "\n", encoding="utf-8"
    )
    return path


def _sha256(path: Path) -> str:
    import hashlib

    return hashlib.sha256(path.read_bytes()).hexdigest()


def sync_authoring(root: Path, imported_at: str) -> list[str]:
    """Ensure every authored source has an ``authoring`` provenance entry.

    The import pipeline records imported files; a file authored directly in this
    repository (a new skill, workflow or agent) has no importer to record it, so
    F8 completeness reported it as an orphan. This adds a missing entry and, when
    an authored entry already exists, refreshes its hashes. It never touches an
    imported entry and never removes one. Returns the target paths it added.

    Idempotent: a second call with the same tree adds nothing, and an unchanged
    authored entry keeps its original ``imported_at`` (only a content change
    rewrites the hash).
    """
    data = load(root)
    entries = data.setdefault("entries", [])
    by_target = {str(e.get("target_path")): e for e in entries if isinstance(e, dict)}

    candidates: list[Path] = []
    for pattern in (
        "knowledge/skills/**/SKILL.md",
        "methodology/workflows/**/SKILL.md",
        "knowledge/agents/**/agent.source.md",
    ):
        candidates.extend(root.glob(pattern))

    added: list[str] = []
    changed = False
    for path in sorted(set(candidates)):
        rel = path.relative_to(root).as_posix()
        digest = _sha256(path)
        entry = by_target.get(rel)
        if entry is None:
            entry = {
                "source_repo": "authoring",
                "source_commit": "native",
                "source_path": rel,
                "source_sha256": digest,
                "target_path": rel,
                "target_sha256": digest,
                "origin_license": "AGPL-3.0",
                "transform": ["authored"],
                "aliases": [],
                "import_run_id": "authored-sync",
                "imported_at": imported_at,
            }
            entries.append(entry)
            by_target[rel] = entry
            added.append(rel)
            changed = True
        elif entry.get("source_repo") == "authoring" and entry.get("target_sha256") != digest:
            entry["source_sha256"] = digest
            entry["target_sha256"] = digest
            changed = True
    if changed:
        write(root, data)
    return added


def refresh_targets(root: Path) -> list[str]:
    """Re-hash every drifted target in the manifest; return the paths refreshed.

    The lock's drift key is ``target_sha256`` (provenance.md). When a canonical
    source is edited outside the importer — a direct hand-edit of an imported
    file — the hash goes stale and ``validate`` now fails. This recomputes
    ``target_sha256`` from disk for each entry whose recorded hash no longer
    matches.

    For an in-place entry (``source_sha256 == target_sha256``, the imported or
    authored convention where the target IS the content) the source hash is
    advanced alongside it, preserving the equality. For a transformed entry
    (``source_sha256 != target_sha256``) only the target hash moves: the source
    hash describes the upstream file, which is not verifiable from here and must
    not be fabricated.

    Idempotent: a clean manifest is left byte-identical and nothing is written.
    """
    data = load(root)
    entries = data.get("entries", [])
    refreshed: list[str] = []
    changed = False
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        target_path = entry.get("target_path")
        if not target_path:
            continue
        target = root / str(target_path)
        if not target.is_file():
            continue
        recorded = entry.get("target_sha256")
        digest = _sha256(target)
        if not recorded or recorded == digest:
            continue
        if entry.get("source_sha256") == recorded:
            entry["source_sha256"] = digest
        entry["target_sha256"] = digest
        refreshed.append(str(target_path))
        changed = True
    if changed:
        write(root, data)
    return refreshed
