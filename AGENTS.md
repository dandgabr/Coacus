# AGENTS.md — Coacus Canonical Routing

Routing rules for any AI agent operating in this repository, in any harness.

## Mental map (scan once per session — single-scan, D5)

- `README.md` — what Coacus is; quickstart.
- `docs/standards/` — the normative standards. Read the relevant one before changing that area.
- `docs/install.md` — how to install the rendered artifacts into each harness.
- `evals/README.md` — behavior evals (static gate + opt-in live runner).
- `catalog/catalog.json` — GENERATED machine index of all assets. Do not hand-edit.
- `catalog/INDEX.md` — GENERATED human index. Do not hand-edit.
- `sources.lock.json` — provenance manifest for imported artifacts (provenance).
- `.agents/*.json` + `.agents/entries/*.json` — GENERATED discovery manifests. Do not hand-edit.

**Single-scan rule:** read the generated indexes once at session start. Never
re-scan directories per turn (D5). If indexes look stale, run
`python3 scripts/coacus.py generate` once and re-read.

## Artifact lifecycle

`create (from templates/authoring)` → `validate` → `register (generate)` →
`discover (single-scan)` → `activate (SessionStart bootstrap, 1 format per harness)`.

## Conventions

1. **One source per artifact.** Skills: `SKILL.md`. Agents: `agent.source.md`.
   MCPs: the triple (`MCP.md` + configs). Everything under `dist/`, `.agents/`,
   `catalog/` is generated.
2. **Agnostic content (D2).** Canonical bodies name ACTIONS, never harness tools.
   Per-harness mappings live in `references/<harness>-tools.md`.
3. **No secrets, no absolute paths (D12).** Secrets as `{env:VAR}` only.
4. **English only (english-only).** kebab-case; descriptions in 3rd person with triggers.
5. **`model` omitted in canonical sources (D1).** Generated `agent.yaml` uses
   `model: inherit`; harnesses resolve the actual model.
6. **Multi-agent governance (D6/D7).** Cap concurrent subagents (governor);
   handoffs use TOON payloads; never spawn ungoverned subagents.
7. **Counts are measured, never copied (D5).** Never assert a corpus count
   (skills, agents, tests, provenance) from prose or memory. Read the generated
   `catalog/INDEX.md` (`**Totals:**`), run
   `python3 scripts/coacus_install.py <harness> --verify`, or measure directly.
   Prose drifts; the generator is the contract. The README corpus table is
   reconciled against the catalog and the lock by `engine/validators/docs.py`, so
   a stale count there is a build error; test counts are stated as a command to
   run, never as a fixed number.
8. **Versions are resolved, never recalled (version-freshness).** Before naming a
   version of a standard, framework or library, resolve it in the current session
   — Context7 for libraries/frameworks, the publisher for standards — and pin the
   resolved version with its source and date. An unresolved pin is marked
   `unverified`, never presented as current.

Enforcement status: skills, agents, MCP, hygiene, discovery and language
validators run in `generate` pre-flight and `validate`; `completeness` (F8)
reconciles the corpus against the sources; the eval scenario gate is static in
CI. Item 4 (English-only) is machine-checked corpus-wide since the F6
translation. Item 5 is checked: the agent validator rejects a `model` key in a
canonical source, and the generated `agent.yaml` is asserted to carry
`model: inherit`. Item 6 is enforced at RUNTIME (the concurrency
governor + the TOON validator). Item 7 is enforced by the generated catalog, the
installer's `--verify` and the README-count reconciliation in
`engine/validators/docs.py`. Item 8 is
advisory: the freshness validator warns on a version-like pin with no nearby
source anchor or resolution marker, and the `version-freshness` skill carries the
resolution workflow.

## Extending the framework (OCP)

Add data, not core code: a new skill/agent/MCP/harness/template/rule is a new
file following the corresponding template in `templates/authoring/`, then
`generate` + `validate`. The `engine/` core only changes when a new CONCEPT
arrives (new representation target, new validation class, new bootstrap shape).

## Memory

Project memory namespace: `Coacus/coacus` (see `.ai-memory.toml`). Decision
audit trail lives in `decisions/` of the memory namespace and `docs/standards/` here.
