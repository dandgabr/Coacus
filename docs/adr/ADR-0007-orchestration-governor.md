# ADR-0007: Orchestration Governor With Disk Ledger

* Status: accepted (2026-09-18, F0 gate)
* Deciders: repository owner
* Decision ID: D6

## Context

Multi-agent runs need bounded concurrency, 429 rate-limit handling, and a ban
on ungoverned subagent spawning.

## Decision

Option A: a disk ledger with `flock` (`engine/governor/ledger.py`), a
configurable concurrency cap (default 5, orchestrator included; the cap is
persisted in the ledger and a later caller may only lower it), and a 429 path
that parks a caller as PAUSED. Because the acquiring CLI process is
short-lived, slots are released by the harness adapter after the task (and on
the next turn as a safety net); a crashed holder is reclaimed by a lease TTL
(`GOVERNOR_LEASE_SECONDS`). `scripts/coacus_governor.py` exposes
`acquire/release/fail/paused/status/health/reset`; `paused` reports the backoff
hint (2s→60s) the orchestrator uses to retry. A health check
(`coacus_governor.py health`) and a cross-process cap test ship with it.

## Consequences

Governance is executable and testable (F4), not prose. No external broker
dependency until multi-host operation is actually required.

## Evidence

`~/Code/skills/scripts/orchestrator-{governor,hook,gate}*` and
`~/Code/skills/harness/orchestrator/README.md:7-41` (reference implementation in
the upstream `skills` repo); Coacus port: `engine/governor/ledger.py`,
`scripts/coacus_governor.py`, `harnesses/*/harness.json` (`plugins`), rendered
gate in `harnesses/opencode/bootstrap/governor-gate.js`.
