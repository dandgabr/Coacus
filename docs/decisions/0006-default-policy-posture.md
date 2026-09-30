# ADR 0006: Default guardrail policy posture

* **Status**: accepted
* **Date**: 2026-09-30
* **Tags**: guardrails, defaults, blast-radius

## Context

A guardrail that denies runs on every tool call of every session of every user of
every harness. Shipping enforcement on by default is a categorically larger blast
radius than the bootstrap, which is inject-only.

## Decision

- v1 ships the guardrail CAPABILITY with an EMPTY, DISABLED default policy set.
- Policies are opt-in per install. "Fail-closed" applies to evaluating the
  policies that exist, not to inventing policies.
- A policy file is active only when it declares `"enabled": true`.

## Consequences

- Installing Coacus never changes a session's behaviour without an explicit
  opt-in.
- The reference policy is disabled; it demonstrates shape only.

## Alternatives considered

1. **Enforcement on by default**: unacceptable blast radius — rejected.
2. **Secrets-only default**: a reasonable middle path, but still an unrequested
   behaviour change — rejected for v1; operators may enable it.
