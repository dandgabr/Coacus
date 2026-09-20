# Orchestration Governance

**Status:** normative
**Scope:** every multi-agent run launched from or inside this repository.

## Rule

Parallel work is governed, executable and testable. No agent may spawn a subagent
without acquiring a slot from the shared ledger, and ungoverned parallel spawning
is prohibited.

### The governor

The concurrency governor is a disk ledger guarded by `flock`
(`engine/governor/ledger.py`). It MUST be consulted before dispatching a subagent.

- The concurrency cap defaults to 5, the orchestrator INCLUDED.
- The cap is persisted in the ledger. A later caller MAY only LOWER it, never
  raise it.
- A caller parks as PAUSED on a 429 rate-limit and reports the backoff hint the
  orchestrator uses to retry (2s → 60s).
- Because the acquiring CLI process is short-lived, slots are released by the
  harness adapter after the task, and on the next turn as a safety net. A crashed
  holder is reclaimed by a lease TTL (`GOVERNOR_LEASE_SECONDS`).
- The cap may be overridden by `ORCH_MAX_CONCURRENT`.

The command surface is `scripts/coacus_governor.py`:
`acquire`, `release`, `fail`, `paused`, `status`, `health`, `reset`.

### The orchestrator

A task that invokes two or more agents MUST route through the
`multi-agent-orchestrator` as supervisor. The orchestrator:

1. Anchors the initial goal and acceptance criteria against scope drift.
2. Supervises each subagent's progress.
3. Mediates conflicts through TOON evidence in `@FILES` (see
   [`toon-protocol.md`](toon-protocol.md)).
4. Intervenes or terminates a subagent that loops, drifts or acts out of scope.

Handoffs between agents MUST be TOON payloads. Free-text handoffs are
non-compliant.

### Health

`coacus_governor.py health` verifies the ledger is readable and consistent. A
cross-process cap test ships with the governor; the rendered gate
`harnesses/opencode/bootstrap/governor-gate.js` enforces the same ledger from the
OpenCode adapter.

## Rationale

Multi-agent runs need bounded concurrency, deterministic rate-limit handling and a
hard ban on ungoverned spawning. A disk ledger with `flock` makes governance
executable and testable rather than prose, and adds no external broker dependency
before multi-host operation is actually required.

## Enforcement

- `scripts/coacus_governor.py` exposes the runtime command surface
  (`acquire/release/fail/paused/status/health/reset`) over
  `engine/governor/ledger.py`.
- `harnesses/opencode/bootstrap/governor-gate.js` is the rendered OpenCode gate;
  `harnesses/*/harness.json` declares plugin wiring.
- `tests/test_governor.py` exercises the cross-process cap and lease behavior.
- The TOON half is enforced by `engine/toon.py` via
  `python3 scripts/coacus.py toon <file>`.
