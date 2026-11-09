"""Tri-state, fail-closed completion ledger (evidence standard).

A ledger records one status per claim and derives one overall status. The rule is
fail-closed: ``fail``, ``unknown``, ``unsupported``, ``truncated`` and ``skipped``
NEVER aggregate to ``pass``. A ``pass`` claim must cite at least one piece of
evidence — a missing id injects an ``unknown``, it does not round up.
"""

from __future__ import annotations

import hashlib
import json

STATUSES = ("pass", "fail", "unsupported", "truncated", "unknown", "skipped")
NON_PASS = ("fail", "unsupported", "truncated", "unknown", "skipped")


def _digest(records: list[dict]) -> str:
    canonical = json.dumps(records, sort_keys=True, separators=(",", ":"))
    return "ecl_" + hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def build(records: list[dict]) -> dict:
    """Build a ledger from claim records; derive the overall status fail-closed."""
    counts = {status: 0 for status in STATUSES}
    normalized: list[dict] = []
    for record in records:
        status = str(record.get("status", "unknown"))
        if status not in counts:
            status = "unknown"
        counts[status] += 1
        normalized.append(
            {
                "claim_id": record.get("claim_id"),
                "status": status,
                "evidence_ids": list(record.get("evidence_ids", [])),
            }
        )

    if counts["fail"]:
        overall = "fail"
    elif any(counts[s] for s in NON_PASS if s != "fail"):
        overall = "unknown"
    else:
        overall = "pass"

    total = len(normalized)
    return {
        "ledger_id": _digest(normalized),
        "overall": overall,
        "summary": {
            "total": total,
            **counts,
            "complete": overall == "pass" and total > 0,
        },
        "records": normalized,
    }


def validate(ledger: dict) -> list[str]:
    """Return ledger errors; empty means well-formed and self-consistent."""
    errors: list[str] = []
    records = ledger.get("records", [])
    if not isinstance(records, list):
        return ["ledger: 'records' must be a list"]
    for index, record in enumerate(records):
        where = f"ledger.records[{index}]"
        status = record.get("status")
        if status not in STATUSES:
            errors.append(f"{where}: unknown status {status!r}")
        if status == "pass" and not record.get("evidence_ids"):
            errors.append(f"{where}: a 'pass' claim must cite at least one evidence id")
    summary = ledger.get("summary", {})
    if summary.get("total") != len(records):
        errors.append("ledger.summary.total does not match the record count")
    if ledger.get("ledger_id") != _digest(records):
        errors.append("ledger.ledger_id does not match its records (tampered or stale)")
    derived = build(records)
    if ledger.get("overall") not in (None, derived["overall"]):
        errors.append(
            f"ledger.overall {ledger.get('overall')!r} is not fail-closed "
            f"(expected {derived['overall']!r})"
        )
    return errors
