# ADR-0010: Single Source for Scripts and Templates

* Status: accepted (2026-09-18, F0 gate)
* Deciders: repository owner
* Decision ID: D9

## Context

`document_converter.py` and `document_analyzer.py` were byte-identical copies
across `skills` and `agente-arquitetura-si`; `pdf_to_markdown.py` diverged;
5 of 6 templates were identical. Copies without canonicity rot.

## Decision

Option A: scripts and templates live in exactly ONE place in this monorepo
(`engine/` + `templates/`) and are consumed by path. While transient copies
exist (e.g., during migration), a CI hash guard fails on divergence. Option B
(published pip package) is deferred until external consumers exist.

## Consequences

No copy without a verified hash; divergent copies are migration debt tracked
to closure in F6.

## Evidence

Map findings R1–R3, A5; `agente-arquitetura-si/scripts/document_converter.py:217`.
