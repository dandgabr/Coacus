# ADR 0003: Enforce-vs-present verification

* **Status**: accepted
* **Date**: 2026-09-30
* **Tags**: guardrails, verification, honesty

## Context

`--verify` today proves presence and bytes. It cannot prove a hook actually
runs: Codex refuses an untrusted hook, OpenCode must load the plugin, Command
Code skips hooks in plan mode, Antigravity has no SessionStart. Claiming
enforcement from presence would fabricate assurance.

## Decision

- Ship v1 guardrails labelled honestly: `enforced` where the harness provably
  blocks, `advisory` elsewhere.
- No tamper-evidence claim without an out-of-process root of trust (a future
  phase).
- Verification is a probe: a canary policy denies a marked action and the live
  CLI is driven to confirm the side effect is absent. The probe is local/opt-in,
  like the live eval tier; CI runs only the static structural gate.
- Capability claims are MOVING PINS: each carries an evidence class and a
  resolved anchor, and a lock records the observed capability.

## Consequences

- The unprovable list is stated explicitly (Codex trust, Command Code plan mode,
  Cursor project-vs-user precedence).
- A `deny` on an unenforceable binding is refused, not degraded silently.

## Alternatives considered

1. **Trust-root from v1**: requires an admin/root install step and a privileged
   process — deferred, not rejected.
2. **Install only where provable**: loses the informative advisory and narrows
   coverage — rejected.
