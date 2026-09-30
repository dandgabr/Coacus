# ADR 0005: Self-improvement boundary and one-way interface

* **Status**: accepted
* **Date**: 2026-09-30
* **Tags**: self-improvement, security, boundary

## Context

The end-of-session loop can read untrusted session content and propose edits to
files that become the model's system prompt. If it could apply its own output,
a poisoned observation would reach every future session. The interface from the
loop to enforcement must therefore be one-way.

## Decision

- v1 ships the loop as a PROPOSER only: it stages proposals; promotion is a human
  pull request. No apply tool exists.
- The interface from the loop to the guardrail/policy layer is HUMAN REVIEW,
  never a file write. No import path connects the proposal writer to the policy
  loader.
- Logic lives in `engine/improve/`; `scripts/coacus_improve.py` is a thin CLI.
- The loop is opt-in and fail-open; the durable audit trail is committed in the
  repository, split from the gitignored runtime ledger.

## Consequences

- A security test asserts no import path links the proposal writer to the policy
  loader.
- A future apply is a separate, hash-pinned identity, PR-only.

## Alternatives considered

1. **Apply in v1**: exposes write capability before the pipeline is proven —
   rejected.
2. **Shadow only**: cannot deliver the requested improvement cycle — rejected.
