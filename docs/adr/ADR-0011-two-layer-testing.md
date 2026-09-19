# ADR-0011: Two-Layer Testing Strategy

* Status: accepted (2026-09-18, F0 gate)
* Deciders: repository owner
* Decision ID: D10

## Context

Testing deterministic infrastructure and LLM behavior are different problems;
mixing them produces flaky CI or untested behavior.

## Decision

Option A: two layers. `tests/` — deterministic infrastructure tests (stdlib
`unittest`, zero dependencies) run on every commit as a blocking gate.
`evals/` — behavior evaluation in two tiers:

- **static** — the scenario-schema validator (`engine/validators/evals.py`),
  deterministic and blocking (it is part of `validate`);
- **live** — real agent sessions driven by `scripts/coacus_eval.py`, with a
  fixed rubric and a pluggable or agent judge; **advisory**, local/manual
  (never blocks CI), because it needs an installed harness CLI and credentials.

## Consequences

Structural regressions (schemas, generators, idempotency, dedup) are caught
deterministically; behavioral quality is tracked without destabilizing CI.

## Evidence

`superpowers/docs/testing.md`; `superpowers/tests/` (17 entries, 16 test dirs);
external `superpowers-evals` drill.
