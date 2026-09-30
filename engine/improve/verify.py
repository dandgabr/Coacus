"""The verification ladder (F10 step 4).

A candidate is verified before staging, cheapest rung first:

- rung 0  structural: the proposal must not violate the repository's own gates;
- rung 0b freshness: a version-like pin must carry a resolved anchor or be marked
  unverified (version-freshness);
- rung 1  coverage: an ``already covered`` candidate is not staged as new;
- rung 2  retrieval: the origin terms must reach the target under the router;
- rung 3  ablation: advisory only (the evaluator is the verifier, not the loop);
- rung 4  human: the promotion gate.

This module implements rungs 0b–2 deterministically; rung 0 is the repo's own
``validate``/``check`` run by the CLI; rungs 3–4 are out of band.
"""

from __future__ import annotations

import re
from pathlib import Path

from engine.improve import route as router

VERSION_PIN = re.compile(r"\bv?\d+\.\d+(?:\.\d+)?\b")
RESOLVED_ANCHOR = re.compile(r"(resolved\s+\d{4}-\d{2}-\d{2}|unverified)", re.IGNORECASE)


def freshness_ok(candidate: dict) -> tuple[bool, str]:
    """Rung 0b: a version pin needs a resolution anchor."""
    text = candidate.get("statement", "")
    if VERSION_PIN.search(text) and not RESOLVED_ANCHOR.search(text):
        return False, "version pin without a resolved anchor (version-freshness)"
    return True, ""


def coverage_ok(routing: dict) -> tuple[bool, str]:
    """Rung 1: an already-covered candidate is skipped, not staged as new."""
    if routing.get("decision") == "skip" and routing.get("reason", "").startswith("already covered"):
        return False, "candidate is already covered"
    return True, ""


def retrieval_ok(root: Path, candidate: dict) -> tuple[bool, str]:
    """Rung 2: the candidate terms must reach a target under the router."""
    routing = router.route(root, candidate)
    if routing.get("target") is None and routing.get("decision") == "create":
        # A genuine gap has no target by definition; that is acceptable.
        return True, ""
    if routing.get("features", {}).get("lex", 0.0) <= 0.0:
        return False, "candidate does not reach any catalog target (retrieval test)"
    return True, ""


def verify(root: Path, candidate: dict, routing: dict) -> dict:
    """Run the deterministic rungs; return a per-rung result."""
    results: dict[str, dict] = {}
    for name, (ok, reason) in (
        ("freshness", freshness_ok(candidate)),
        ("coverage", coverage_ok(routing)),
        ("retrieval", retrieval_ok(root, candidate)),
    ):
        results[name] = {"ok": ok, "reason": reason}
    results["passed"] = all(r["ok"] for r in results.values())
    return results
