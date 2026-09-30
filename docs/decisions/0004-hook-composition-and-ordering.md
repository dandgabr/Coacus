# ADR 0004: Hook composition and ordering

* **Status**: accepted
* **Date**: 2026-09-30
* **Tags**: guardrails, installer

## Context

Coacus installs alongside user hooks. Under Claude semantics every matching hook
runs and a deny from any wins; under a first-match-wins evaluator a user `allow`
at position 0 silently defeats a Coacus `deny`. The installer appended Coacus
entries last, which is safe for composable harnesses and dangerous otherwise.

## Decision

- Guardrail decisions compose monotonically: `deny > ask > allow`. Adding a hook
  can only make the outcome stricter.
- `harness.json.lifecycle` declares `composition`
  (`composable | first-match-wins | last-match-wins`) and `ordering`.
- Where composition is not `composable`, the installer places Coacus at the
  winning position or REFUSES a `deny`.
- Ownership is per ENTRY ID, never a repository path, so a re-install of one
  subsystem cannot delete the other's entry and `--uninstall` removes all Coacus
  ids.

## Consequences

- `--verify` proves position, not merely presence, where the harness allows.
- Cursor project-vs-user precedence must be probed before a user-scope `deny`.

## Alternatives considered

1. **Append always**: safe for Claude, silently defeated on first-match-wins —
   rejected.
2. **Path-based ownership**: breaks across clones and cannot represent two
   Coacus hook entries — rejected.
