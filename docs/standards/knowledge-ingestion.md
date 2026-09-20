# Knowledge Ingestion

**Status:** normative
**Scope:** document ingestion — the `architecture_si` vertical, the dispatcher and
every format handler.

## Rule

Document ingestion is an OPEN-CLOSED pipeline. The dispatcher protocol lives in
`engine/dispatcher/`; format handlers register themselves with
`@register_converter` and declare the extensions they own.

- A new format is a NEW HANDLER FILE under
  `verticals/architecture_si/pipelines/ingest/handlers/`. The dispatcher never
  changes for a new format.
- Call sites NEVER import a specific converter. They call
  `engine.dispatcher.convert(...)`, which dispatches by file extension. Coupling a
  generic pipeline step to one concrete converter is forbidden.
- Every ingestion script MUST expose an entrypoint, a dependency fallback and a
  stable JSON output.
- There MUST be no cross-imports between handlers.

The pipeline is used as three stages: docs → markdown (`pdf2md`, `doc2md`) →
analysis (`doc-analyze`).

## Rationale

The source repository shipped a working pipeline but coupled one script directly
to a specific PDF converter. Removing that coupling and routing through a registry
means a new format is data, not a change to shared code, which is the open-closed
rule applied to ingestion.

## Enforcement

- `engine/dispatcher/__init__.py` implements `@register_converter`,
  `supported_extensions`, `converter_for` and `convert`; `load_handlers()`
  imports each handler so its decorator runs.
- `python3 scripts/coacus_vertical.py formats` lists the registered extensions;
  the vertical CLI is the executable surface.
- `python3 scripts/coacus_vertical.py` is covered by `tests/test_vertical.py`.
