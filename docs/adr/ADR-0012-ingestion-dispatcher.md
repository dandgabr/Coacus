# ADR-0012: Ingestion Pipeline Reused With an OCP Dispatcher

* Status: accepted (2026-09-18, F0 gate)
* Deciders: repository owner
* Decision ID: D11

## Context

`agente-arquitetura-si` ships a working docs→markdown→analysis pipeline
(`pdf2md`, `doc2md`, `doc-analyze`) with dual human/JSON output and dependency
fallback, but couples `document_converter.py:217` to `pdf_to_markdown`.

## Decision

Option A: reuse the pipeline inside `verticals/architecture-si/pipelines/`,
removing the cross-script coupling. The dispatcher protocol lives in
`engine/dispatcher/`; format handlers register via `@register_converter`
(open-closed: new formats are new handler files, the dispatcher never changes).

## Consequences

Every ingestion script has an entrypoint, dependency fallback and stable JSON
output; no cross-imports between handlers.

## Evidence

`agente-arquitetura-si/scripts/*.py`;
`skills/skills/engineering-practices/clean-code-reusability/examples/reusability_patterns.md:13-18`.
