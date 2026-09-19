# ADR-0002: Agent Manifests Generated From a Single Canonical Source

* Status: accepted (2026-09-18, F0 gate)
* Deciders: repository owner
* Decision ID: D1

## Context

The three source repositories use incompatible agent packaging dialects
(`skills`: quadruple AGENT.md/agent.yaml/agent.json/plugin.json with known
drift — 3 missing plugin.json; `agente-arquitetura-si`: reduced pair;
`superpowers`: JS/TS plugin). One canonical standard with derived
representations is required.

## Decision

Option A: each agent has ONE canonical `agent.source.md`. A generator emits
`dist/AGENT.md` (markdown profile), `dist/agent.yaml` (ADK/Antigravity,
`model: inherit`), `dist/agent.json` (frameworks/APIs) and `dist/plugin.json`
(plugin shim). Only `name`, `description` and `skills` must stay in sync — and
they do so by construction. `model` is omitted in the canonical source and
resolved per harness; `inherit` is never copied into AGENT.md/agent.json.

## Consequences

Generator + golden tests are mandatory; the validator fails if representations
diverge from a regeneration. Adding a new representation target later is a
core change (legitimate OCP variation point).

## Evidence

`skills/AGENTS.md:47-67`; `skills/agents/README.md:31-37`;
`agente-arquitetura-si/agents/*/agent.yaml`; `superpowers/docs/porting-to-a-new-harness.md:24-56`.
