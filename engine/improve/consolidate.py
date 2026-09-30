"""Consolidate raw observations into TYPED candidates (F10 step 2).

Compression, not accumulation: a raw transcript is input, never output. Each
candidate is one of:

- ``gotcha``    — an error or difficulty (negative knowledge);
- ``procedure`` — a confirmed successful approach;
- ``fact``      — a durable fact not derivable from the code.

Candidates are typed deterministically from observation signals; no LLM is
required for v1. Each candidate carries its evidence units (channel, session,
claim hash) so the taint and independence rules can be enforced downstream.
"""

from __future__ import annotations

import hashlib

from engine.improve import taint

ERROR_MARKERS = ("error", "failed", "failure", "exception", "traceback", "denied")
SUCCESS_MARKERS = ("passed", "succeeded", "fixed", "resolved", "worked")


def _claim(observation: dict) -> str:
    return str(observation.get("text") or observation.get("summary") or "").strip()


def _hash(text: str) -> str:
    return hashlib.sha256(text.strip().lower().encode("utf-8")).hexdigest()[:16]


def _type_of(observation: dict) -> str:
    status = str(observation.get("status", "")).lower()
    text = _claim(observation).lower()
    if status in ("error", "failure") or any(m in text for m in ERROR_MARKERS):
        return "gotcha"
    if status in ("ok", "success") or any(m in text for m in SUCCESS_MARKERS):
        return "procedure"
    return "fact"


def consolidate(observations: list[dict]) -> list[dict]:
    """Group observations into typed candidates, deduped by normalized claim."""
    grouped: dict[tuple[str, str], dict] = {}
    for obs in observations:
        claim = _claim(obs)
        if not claim:
            continue
        kind = _type_of(obs)
        key = (kind, _hash(claim))
        session = str(obs.get("session_id", "session"))
        if key not in grouped:
            grouped[key] = {
                "type": kind,
                "statement": claim,
                "claim_hash": key[1],
                "evidence": [],
            }
        grouped[key]["evidence"].append(
            {
                "channel": taint.classify(obs),
                "session_id": session,
                "claim_hash": key[1],
                "observation_id": str(obs.get("id", "")),
            }
        )
    candidates = list(grouped.values())
    candidates.sort(key=lambda c: (c["type"], c["claim_hash"]))
    for candidate in candidates:
        candidate["support"] = taint.independence(candidate)
        candidate["trusted"] = taint.has_trusted_evidence(candidate)
    return candidates
