"""The end-of-session improvement loop (F10).

Runs the pipeline once per invocation: capture → consolidate → route → verify →
stage. It is opt-in, fail-open, and NEVER applies a change (D7): the output is a
runtime proposal ledger entry plus a reviewable staging bundle.

The loop is intentionally not imported by ``generate``/``check``: a test asserts
``engine.improve`` is absent from ``sys.modules`` after those commands, so the
non-deterministic subsystem cannot leak into the deterministic build contract.
"""

from __future__ import annotations

import json
from pathlib import Path

from engine.improve import consolidate, ledger, route as router, sources, verify

STAGING = "docs/temp/improvement"


def _alarm_for(statuses: dict[str, str]) -> list[str]:
    """Absent-by-config is a safe skip; absent-unexpectedly is an alarm."""
    return [
        f"source {name!r} is configured but unreachable — improvement auditing is degraded"
        for name, status in statuses.items()
        if status == "absent_unexpectedly"
    ]


def run(root: Path, options: dict) -> dict:
    """Execute the pipeline; return a summary (never raises on absence)."""
    registry = sources.SourceRegistry()
    sources.register_builtin(registry)
    requested = options.get("source") or "transcript"
    source = registry.get(requested)
    if source is None:
        return {"ok": False, "reason": f"unknown source {requested!r}", "proposals": []}

    statuses = {name: registry.get(name).status(root) for name in registry.names()}  # type: ignore[union-attr]
    alarms = _alarm_for(statuses)

    observations = source.read(root, options)
    if not observations:
        return {
            "ok": True,
            "status": source.status(root),
            "alarms": alarms,
            "proposals": [],
            "note": "no observations available — fail-open no-op",
        }

    candidates = consolidate.consolidate(observations)
    proposals: list[dict] = []
    for candidate in candidates:
        # Taint rule: a rule/procedure needs trusted evidence; else it is a note.
        if candidate["type"] in ("gotcha", "procedure") and not candidate["trusted"]:
            candidate["type"] = "note"
            candidate["downgraded"] = "externally-tainted evidence"

        routing = router.route(root, candidate)
        if routing["decision"] == "skip":
            continue
        result = verify.verify(root, candidate, routing)
        if not result["passed"]:
            continue
        record = {
            "type": candidate["type"],
            "statement": candidate["statement"],
            "claim_hash": candidate["claim_hash"],
            "support": candidate.get("support", 0),
            "trusted": candidate.get("trusted", False),
            "routing": routing,
            "verification": result,
            "status": "proposed",
        }
        ledger.append_runtime(root, record)
        proposals.append(record)

    staging = root / STAGING
    staging.mkdir(parents=True, exist_ok=True)
    (staging / "last-run.json").write_text(
        json.dumps({"proposals": proposals, "alarms": alarms}, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return {
        "ok": True,
        "status": source.status(root),
        "alarms": alarms,
        "proposals": proposals,
    }
