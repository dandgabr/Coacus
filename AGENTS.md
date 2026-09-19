# AGENTS.md — Coacus Canonical Routing

Routing rules for any AI agent operating in this repository, in any harness.

## Mental map (scan once per session — single-scan, D5)

- `README.md` — what Coacus is; quickstart.
- `docs/adr/` — ratified architecture decisions (D1–D12 + policies). Read before changing structure.
- `docs/install.md` — how to install the rendered artifacts into each harness.
- `evals/README.md` — behavior evals (static gate + opt-in live runner).
- `catalog/catalog.json` — GENERATED machine index of all assets. Do not hand-edit.
- `catalog/INDEX.md` — GENERATED human index. Do not hand-edit.
- `sources.lock.json` — provenance manifest for imported artifacts (ADR-0015).
- `.agents/*.json` + `.agents/entries/*.json` — GENERATED discovery manifests. Do not hand-edit.

**Single-scan rule:** read the generated indexes once at session start. Never
re-scan directories per turn (D5). If indexes look stale, run
`python3 scripts/coacus.py generate` once and re-read.

## Artifact lifecycle

`create (from templates/authoring)` → `validate` → `register (generate)` →
`discover (single-scan)` → `activate (SessionStart bootstrap, 1 format per harness, F3)`.

## Conventions

1. **One source per artifact.** Skills: `SKILL.md`. Agents: `agent.source.md`.
   MCPs: the triple (`MCP.md` + configs). Everything under `dist/`, `.agents/`,
   `catalog/` is generated.
2. **Agnostic content (D2).** Canonical bodies name ACTIONS, never harness tools.
   Per-harness mappings live in `references/<harness>-tools.md` (F3).
3. **No secrets, no absolute paths (D12).** Secrets as `{env:VAR}` only.
4. **English only (ADR-0001).** kebab-case; descriptions in 3rd person with triggers.
5. **`model` omitted in canonical sources (D1).** Generated `agent.yaml` uses
   `model: inherit`; harnesses resolve the actual model.
6. **Multi-agent governance (D6/D7).** Cap concurrent subagents (governor);
   handoffs use TOON payloads; never spawn ungoverned subagents.

Enforcement status: items 1–3 are machine-checked (agents, skills, MCP, hygiene
and discovery validators, run by `generate` pre-flight and `validate`). Item 4 is
warned (non-English markers) until import translation completes at F6. Item 5's
generated output is asserted; canonical omission of `model` is not yet
validated. Item 6 is enforced at RUNTIME (the concurrency governor + the TOON
validator), not by a repository validator.

## Extending the framework (OCP)

Add data, not core code: a new skill/agent/MCP/harness/template/rule is a new
file following the corresponding template in `templates/authoring/`, then
`generate` + `validate`. The `engine/` core only changes when a new CONCEPT
arrives (new representation target, new validation class, new bootstrap shape).

## Memory

Project memory namespace: `Coacus/coacus` (see `.ai-memory.toml`). Decision
audit trail lives in `decisions/` of the memory namespace and `docs/adr/` here.
