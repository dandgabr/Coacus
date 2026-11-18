"""Consolidate raw observations into TYPED candidates (F10 step 2).

Compression, not accumulation: a raw transcript is input, never output. Each
candidate is one of:

- ``gotcha``    — an error or difficulty (negative knowledge);
- ``procedure`` — a confirmed successful approach;
- ``fact``      — a durable fact not derivable from the code;
- ``skill-gap`` — a request no skill or agent matched, declared by an observation
  with ``kind: "route-miss"`` (never inferred from text).

Candidates are typed deterministically from observation signals; no LLM is
required for v1. Each candidate carries its evidence units (channel, session,
claim hash) so the taint and independence rules can be enforced downstream.
"""

from __future__ import annotations

import hashlib
import unicodedata

from engine.improve import taint

ERROR_MARKERS = ("error", "failed", "failure", "exception", "traceback", "denied")
SUCCESS_MARKERS = ("passed", "succeeded", "fixed", "resolved", "worked")


# A skill gap is declared by a structured field set by the producer, never inferred
# from words in free text, which anyone can write. The statement is short and clean:
# it is withheld from the proposal anyway, and only its hash and counts are kept.
SKILL_GAP_KIND = "route-miss"
MAX_GAP_CLAIM = 200


def _claim(observation: dict) -> str:
    return str(observation.get("text") or observation.get("summary") or "").strip()


def _clean(text: str) -> str:
    """Drop control and format characters (invisible, bidi, tag) and cap the length."""
    kept = "".join(ch for ch in text if unicodedata.category(ch)[0] != "C" or ch in " \t")
    return kept.strip()[:MAX_GAP_CLAIM]


def _hash(text: str) -> str:
    return hashlib.sha256(text.strip().lower().encode("utf-8")).hexdigest()[:16]


def _type_of(observation: dict) -> str:
    if observation.get("kind") == SKILL_GAP_KIND:
        return "skill-gap"
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
    for index, obs in enumerate(observations, 1):
        claim = _claim(obs)
        if not claim:
            continue
        kind = _type_of(obs)
        if kind == "skill-gap":
            claim = _clean(claim)
            if not claim:
                continue
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
                "observation_index": index,
            }
        )
    candidates = list(grouped.values())
    candidates.sort(key=lambda c: (c["type"], c["claim_hash"]))
    for candidate in candidates:
        candidate["support"] = taint.independence(candidate)
        candidate["trusted"] = taint.has_trusted_evidence(candidate)
    return candidates
