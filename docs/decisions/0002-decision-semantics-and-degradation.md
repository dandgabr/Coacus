# ADR 0002: Decision semantics and per-harness degradation

* **Status**: accepted
* **Date**: 2026-09-30
* **Tags**: guardrails, semantics

## Context

The canonical decision set must map onto harnesses with different vocabularies.
Cursor has allow/deny but no `ask`; Codex and Command Code expose deny-only;
Antigravity cannot bind `session.start`; OpenCode has no exit code (blocking is a
`throw`) and no `session.end`. A single harness-level "can_block" boolean cannot
express per-event capability.

## Decision

- Canonical decisions: `allow | deny | ask`. `ask` is valid only where the
  harness exposes a human channel (`can_ask`), and degrades per the policy's
  `on_ask_unavailable`.
- `ask` is forbidden in headless runs (`live_cli`) and inside subagent scope.
- A `deny` on an event with no native home degrades to `advisory`, never to a
  silent `allow`.
- Failure is split: `on_decision_failure` (the evaluator ran but could not
  decide) defaults to `deny`; `on_mechanism_failure` (the process failed)
  defaults to `allow` plus an advisory, so a broken hook cannot deny every call.
- Capabilities are per `(harness, event)` in `harness.json.lifecycle`.

## Consequences

- The capability matrix is generated with an evidence class per cell; a bare
  boolean is forbidden.
- The installer REFUSES a `deny` on a non-`can_block` event unless
  `--allow-advisory` records the downgrade.

## Alternatives considered

1. **Global fail-closed**: a crashed hook would deny every tool call — an
   availability incident, rejected.
2. **Global ask→allow**: a hole in headless CI — rejected.
