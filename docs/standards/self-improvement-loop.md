# Self-Improvement Loop

**Status:** normative
**Scope:** the optional, asynchronous end-of-session improvement subsystem.

## Rule

The framework ships an OPT-IN, FAIL-OPEN loop that reads a finished session,
compresses it into typed candidates, routes each candidate, verifies it, and
stages a PROPOSAL. It NEVER applies a change: promotion is a human pull request.

### Opt-in and portability

- The loop is inert unless invoked by `scripts/coacus_improve.py`; it is never
  called from `generate`, `check`, `validate` or CI (P2).
- Episodic sources are pluggable (`engine/improve/sources/`). `transcript` is the
  portable default; `ai-memory` is an OPTIONAL enricher. Absence of every external
  source degrades to a no-op, never to a build failure.
- Three source states are distinguished: `present`, `absent_by_config` (safe
  skip, proven by configuration) and `absent_unexpectedly` (an alarm, because an
  attacker must not be able to make auditing vanish silently).

### Capture and typing

- A raw transcript is INPUT, never output: the loop persists typed candidates,
  not transcripts.
- Every observation carries a SOURCE CHANNEL. `human-user-turn` and `repo-file`
  are trusted; `tool-result`, `external-content` and `model-assistant` are
  tainted. A `gotcha` or `procedure` requires at least one trusted unit;
  otherwise it is downgraded to a `note`.
- Evidence independence is computed (distinct channel + session + claim hash),
  not counted.

### Routing, verification, staging

- Improve-vs-create is a deterministic, auditable procedure (retrieval-first,
  default IMPROVE) in `engine/improve/route.py`.
- Verification is a ladder: rung 0 structural (the repository's own gates),
  rung 0b freshness (a version pin needs an anchor), rung 1 coverage, rung 2
  retrieval, rung 3 ablation (advisory), rung 4 human. The loop's own critique is
  never the acceptance criterion.
- Proposals are written to a runtime ledger (`docs/temp/`, gitignored) and a
  reviewable staging bundle. The durable audit trail is committed separately and
  is NOT part of the generated surface.

## Rationale

The self-critique literature is unambiguous: without an external verifier,
self-correction degrades (Huang et al., ICLR 2024); verification is not easier
than generation (Stechly et al., 2024). A learned artifact that reaches the
bootstrap is injected into every future session, so the blast radius of a bad
promotion is the whole installed fleet. The loop therefore proposes, the repo's
deterministic gates and a human dispose.

## Enforcement

- `tests/test_improve.py` covers the source registry, taint, consolidation,
  routing, the ladder, the ledger placement and a poisoned candidate.
- A test asserts `engine.improve` is not imported by `generate`/`check`.
- `docs/standards/lifecycle-guardrails.md` governs the enforcement layer the loop
  is forbidden to weaken.
