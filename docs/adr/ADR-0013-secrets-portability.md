# ADR-0013: Secrets and Portability Guardrails

* Status: accepted (2026-09-18, F0 gate)
* Deciders: repository owner
* Decision ID: D12

## Context

Transversal rule of the three sources: no plaintext secrets, no absolute
paths. Already violated once (`agente-arquitetura-si/templates/README.md:11`
contained an absolute path from another machine). Convention alone does not
enforce it.

## Decision

Option A+C: canonical sources reference secrets only as `{env:VAR}` /
`${VAR}` (resolved at activation time, never stored); a validator
(`engine/validators/hygiene.py`) rejects absolute paths (`/home/`, `/Users/`,
`/root/`, `~`, `C:\` or `C:/`) and secret-shaped literals; a secrets scanner
joins the CI pipeline in F2.

## Consequences

Portability is machine-independent by construction; violations fail the build
before merge.

## Evidence

`skills/AGENTS.md:120-122`; `skills/MCPS.md:55-56`;
`skills/scripts/validate_harness.py:4-9`; map finding A2.
