"""Revisioned residual-unknown registry (evidence standard).

An unknown is not a TODO: it is a record of what is not yet known, which evidence
supports and contradicts it, what class of evidence would settle it, and how many
probes are recommended. Every update is a new revision, and a resolved-verified
unknown must cite evidence — absence is never a pass.
"""

from __future__ import annotations

import hashlib
import json

STATUSES = ("open", "investigating", "blocked", "contradicted", "resolved")
SEVERITIES = ("low", "medium", "high", "critical")
DISPOSITIONS = ("verified", "withdrawn", "out-of-scope")


def _revision_digest(entry: dict) -> str:
    body = {k: v for k, v in entry.items() if k not in ("revision_digest", "previous_revision_digest")}
    canonical = json.dumps(body, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def build(question: str, severity: str = "medium", required_authority: str = "") -> dict:
    """Create a new, open unknown at revision 1."""
    entry = {
        "question": question,
        "status": "open",
        "severity": severity,
        "required_authority": required_authority,
        "supporting_evidence_ids": [],
        "contradicting_evidence_ids": [],
        "recommended_probes": [],
        "resolution": None,
        "revision": 1,
    }
    entry["revision_digest"] = _revision_digest(entry)
    return entry


def update(entry: dict, expected_revision: int) -> dict:
    """Return a new revision, or raise when ``expected_revision`` is stale."""
    if entry.get("revision") != expected_revision:
        raise ValueError(
            f"stale revision: expected {expected_revision}, entry is {entry.get('revision')}"
        )
    revised = dict(entry)
    revised["revision"] = int(expected_revision) + 1
    revised["previous_revision_digest"] = entry.get("revision_digest")
    revised["revision_digest"] = _revision_digest(revised)
    return revised


def validate(entry: dict) -> list[str]:
    """Return registry-entry errors; empty means well-formed."""
    errors: list[str] = []
    if entry.get("status") not in STATUSES:
        errors.append(f"unknown: bad status {entry.get('status')!r}")
    if entry.get("severity") not in SEVERITIES:
        errors.append(f"unknown: bad severity {entry.get('severity')!r}")
    supporting = set(entry.get("supporting_evidence_ids", []))
    contradicting = set(entry.get("contradicting_evidence_ids", []))
    overlap = supporting & contradicting
    if overlap:
        errors.append(f"unknown: evidence id in both sides: {sorted(overlap)}")
    if entry.get("status") == "contradicted" and not contradicting:
        errors.append("unknown: status 'contradicted' requires contradicting evidence")
    if entry.get("status") == "resolved":
        resolution = entry.get("resolution") or {}
        disposition = resolution.get("disposition")
        if disposition not in DISPOSITIONS:
            errors.append(f"unknown: bad resolution disposition {disposition!r}")
        if disposition == "verified" and not resolution.get("evidence_ids"):
            errors.append("unknown: a verified resolution requires at least one evidence id")
    if not isinstance(entry.get("revision"), int) or entry.get("revision", 0) < 1:
        errors.append("unknown: 'revision' must be a positive integer")
    if entry.get("revision_digest") != _revision_digest(entry):
        errors.append("unknown: revision_digest does not match the entry (tampered or stale)")
    return errors
