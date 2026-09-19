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
`evals/` — LLM behavior evaluation with a fixed rubric and a judge model, run
in a separate scheduled pipeline, advisory (never blocking).

## Consequences

Structural regressions (schemas, generators, idempotency, dedup) are caught
deterministically; behavioral quality is tracked without destabilizing CI.

## Evidence

`superpowers/docs/testing.md`; `superpowers/tests/` (17 entries, 16 test dirs);
external `superpowers-evals` drill.
