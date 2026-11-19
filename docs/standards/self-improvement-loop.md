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
- Verification is a ladder: rung 0 structural (the repository's own gates), rung 0a protected surfaces,
  rung 0b freshness (a version pin needs an anchor), rung 1 coverage, rung 2
  retrieval, rung 3 ablation (advisory), rung 4 human. The loop's own critique is
  never the acceptance criterion.
- Proposals are appended to a runtime ledger (`docs/temp/`, gitignored) and the
  latest run is staged separately. Statements and source paths are withheld;
  routing metadata may still reveal information. Each run has a random identifier
  and each proposal lists 1-based positions among accepted JSON objects, excluding
  malformed lines and non-objects. A private association under the gitignored
  `.ai-memory/improve-sources/` stores the captured source snapshot and exact
  proposal references by run ID. On POSIX, directories must be owner-only and
  association files are created owner-only. Publishing fails closed if private
  storage is unavailable. Snapshots contain sensitive observations and consume
  storage proportional to the source; retain and delete them through an authorized
  process. On Windows no snapshot is written. Before running, the operator supplies
  a privately retained 32-byte hexadecimal key through the environment variable
  `COACUS_IMPROVE_RECOVERY_KEY`. The key is never returned or published. The keyed
  verifier authenticates the complete proposal and exact source. Keep the key and
  original source; losing either makes recovery impossible.
- On POSIX, call `engine.improve.loop.recover(root, proposal)` with the complete
  unmodified proposal in a trusted private environment. It rejects altered fields,
  missing or insecure associations, and review-only references for new snapshots.
  Legacy associations without a `proposals` field accept a matching review alone;
  they cannot authenticate the other proposal fields and must not be treated as
  fully authenticated. Original source changes do not affect the snapshot. An owner
  able to rewrite the private association can tamper with its contents. For a
  Windows proposal, use `recover(root, proposal, original_path, recovery_key)`;
  altered originals and proposals are rejected. Uncertain publication returns
  complete proposals in `reconciliation`. Never log the key or recovered sensitive
  observations. Do not promote unverifiable proposals.
- **Warning: older runtime ledger and staging records may contain raw sensitive
  statements or claim hashes, and old references may be ambiguous.** This change
  does not remove, redact, migrate, or secure existing records. Treat them as
  sensitive and handle retention or removal through an authorized process.
  The durable audit trail is committed separately and is NOT generated.

### Conditions for any self-editing loop (advisory)

These conditions are advisory: no validator enforces them today. A loop that edits
its own rules, skills or policies should meet all of them before a change is adopted:

- Rungs 0, 0b, 1 and 2 of the verification ladder are green.
- A human approves the change by pull request. The agent or model that proposed it is
  never the approver and never the judge.
- Each adoption can be undone in one step.
- The loop never edits its protected surfaces: `docs/standards/self-improvement-loop.md`,
  `docs/standards/evidence.md`, `docs/standards/untrusted-content.md`,
  `docs/standards/lifecycle-guardrails.md`, `engine/improve/`, `engine/guardrail/`,
  `engine/verify/`, `scripts/coacus_eval.py`, `evals/scenarios/`,
  `harnesses/*/bootstrap/guardrail-hooks.json` and `AGENTS.md`. The list is
  `engine/improve/protected.py`; a test keeps this sentence equal to it.

Rung 0a of the ladder enforces part of this: a candidate whose statement names a
protected surface, or that routes to a catalog target on one, is rejected before it is
staged ([ADR 0017](../decisions/0017-protected-surfaces-rung.md)). It is a text match on
a proposal, not a check of any file, so the human approval above stays the real gate. A
digest manifest and a safety text emitted from the engine are not built. Adapted from patterns recorded in ADR 0009 (revision
`6337341602be6aa5860b1e83138f03bdd0b78f71`, reviewed 2026-11-17; see
[`THIRD-PARTY-NOTICES.md`](../../THIRD-PARTY-NOTICES.md)).

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
