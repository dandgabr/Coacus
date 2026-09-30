"""Taint labeling for captured observations (F10 security).

Every observation is UNTRUSTED historical data. Its SOURCE CLASS decides whether
it may become a rule or a procedure:

- ``human-user-turn`` and ``repo-file`` are trusted channels;
- ``tool-result``, ``external-content`` and ``model-assistant`` are tainted.

A candidate of type ``rule`` or ``procedure`` MUST have at least one trusted-channel
unit; otherwise it may only be staged as a ``note``. This is the code enforcement
of the untrusted-content boundary (OWASP LLM01/LLM04).
"""

from __future__ import annotations

TRUSTED_CHANNELS = {"human-user-turn", "repo-file"}
TAINTED_CHANNELS = {"tool-result", "external-content", "model-assistant"}


def classify(observation: dict) -> str:
    """Return the source channel of an observation (defaults to tainted)."""
    channel = str(observation.get("channel", "")).strip()
    if channel in TRUSTED_CHANNELS or channel in TAINTED_CHANNELS:
        return channel
    # Unknown provenance is treated as external content: tainted.
    return "external-content"


def is_trusted(observation: dict) -> bool:
    """True when the observation came from a trusted channel."""
    return classify(observation) in TRUSTED_CHANNELS


def has_trusted_evidence(candidate: dict) -> bool:
    """True when at least one evidence unit is from a trusted channel."""
    return any(
        str(u.get("channel", "")) in TRUSTED_CHANNELS
        for u in candidate.get("evidence", [])
    )


def independence(candidate: dict) -> int:
    """Count independent evidence units: distinct channel+session+claim hash.

    Counting alone is gameable (two paraphrases of one injected sentence); this
    counts distinct (channel, session, normalized claim) triples.
    """
    seen: set[tuple[str, str, str]] = set()
    for unit in candidate.get("evidence", []):
        seen.add(
            (
                str(unit.get("channel", "")),
                str(unit.get("session_id", "")),
                str(unit.get("claim_hash", "")),
            )
        )
    return len(seen)
