# ADR-0008: TOON Protocol for Agent Handoffs

* Status: accepted (2026-09-18, F0 gate)
* Deciders: repository owner
* Decision ID: D7

## Context

Agent-to-agent handoffs must be token-compact and machine-parseable.

## Decision

Option A: TOON payloads for all agent handoffs:

```text
@FROM: <emitter>
@TO: <receiver-or-orchestrator>
@STATUS: <OK | CONFLICT | BLOCKED | NEED_INFO>
@CTX: <concise-context-id>
@FILES: <path:lines>;...   (relative paths only)
@SUMMARY: <ultra-compact summary>
@ACTION_NEEDED: <objective next step>
```

JSON is reserved for machine contracts (APIs, manifests). A payload validator
(`engine/validators`) enforces required fields.

## Consequences

Free-text handoffs are non-compliant; conflict mediation flows through the
orchestrator with TOON evidence in `@FILES`. The TOON payload validator is
implemented with the governor (F4).

## Evidence

`skills/AGENTS.md:100-114`.
