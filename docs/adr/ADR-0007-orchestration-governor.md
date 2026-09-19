# ADR-0007: Orchestration Governor With Disk Ledger

* Status: accepted (2026-09-18, F0 gate)
* Deciders: repository owner
* Decision ID: D6

## Context

Multi-agent runs need bounded concurrency, 429 rate-limit handling, and a ban
on ungoverned subagent spawning.

## Decision

Option A: a disk ledger with `flock` (`engine/governor/`), configurable
concurrency cap (default 5, orchestrator included), 429 marking a slot PAUSED
with exponential backoff retry (2s→60s), and per-harness adapters
(governor CLI, harness hook, plugin gate). The cap test and health check land
with the governor in F4.

## Consequences

Governance is executable and testable (F4), not prose. No external broker
dependency until multi-host operation is actually required.

## Evidence

`skills/scripts/orchestrator-{governor,hook,gate}*`;
`skills/harness/orchestrator/README.md:7-41`.
