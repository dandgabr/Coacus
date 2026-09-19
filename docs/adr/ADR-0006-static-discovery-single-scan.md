# ADR-0006: Static Discovery Manifests With Single-Scan Per Session

* Status: accepted (2026-09-18, F0 gate)
* Deciders: repository owner
* Decision ID: D5

## Context

Discovery must be deterministic and cheap: agents must not re-scan directories
every turn.

## Decision

Option A: static discovery manifests under `.agents/{skills,mcps,agents}.json`
(consolidated) and `.agents/entries/<name>.json` (per-agent) (GENERATED, see
ADR-0014) plus a single-scan rule — read the indexes once at session start,
then rely on session cache. Migrate to a DB-backed index only if the inventory
grows past a few hundred assets or semantic search becomes a requirement.

## Consequences

Discovery manifests are generated and drift-checked (ADR-0014); a dedicated
manifest validator lands in F2. Per-turn re-scanning is prohibited by
`AGENTS.md`.

## Evidence

`skills/.agents/{skills,harness,mcps,plugins}.json`; `skills/AGENTS.md:73-86`.
