# Roadmap

Coacus was built in phases. Each phase has a single-line scope and a status.
Status values: **done** (merged), **active** (in progress), **planned**.

| Phase | Scope | Status |
|---|---|---|
| **F0** | Framework charter: settle the architecture standards and lay the repository skeleton. | done |
| **F1** | Foundation: engine core — frontmatter parser, generators, validators, thin CLI, first tests. | done (commit `e98dc1a`) |
| **F2** | Quality gates: tolerant parser, hardened CI (`ci` + `secrets`), drift check, two-layer testing. | done (commit `a8ae7ed`) |
| **F3** | MCP single-source generation and per-harness SessionStart bootstrap render ([session-start-bootstrap](standards/session-start-bootstrap.md)). | done (commit `cb50394`) |
| **F4** | Execution governance: concurrency/rate-limit governor, TOON validator, discovery manifests. | done (commit `e6e0057`) |
| **F5** | Behavior evals: static scenario gate plus opt-in live runner with a pluggable judge. | done (commit `cfc195e`) |
| **F6** | Corpus import: import, translate and organize the full corpus into the 10-category taxonomy. | done (commit `65b9fbc`) |
| **F7** | Final consolidation: documentation set, corpus-and-taxonomy, changelog, contribution contract; reconcile the README with the shipped corpus. | done |
| **F8** | Completeness verification: reconcile source repos, `sources.lock.json` and the catalog to prove nothing was left behind. | done |

## Phase detail

### F0 — Framework charter

Established the architecture standards agent-manifests…secrets-portability, plus the language
policy english-only, committed-generated-artifacts generated-artifacts and the provenance
placement provenance. Defined the core principle: disk is the truth; generation is
the contract.

### F1 — Foundation

Built the engine: `frontmatter.py`, the generators (five at the time), the source validators,
the thin `coacus.py` CLI, and the first deterministic tests. Established that
the engine is closed for modification and operates on data registries.

### F2 — Quality gates

Made the tolerant frontmatter parser pass the reference corpus, wired
`.github/workflows/ci.yml` (validate → check → tests, never `generate`), and
added the pinned gitleaks `secrets` job scanning the checked-out state. Split
testing into deterministic `tests/` and behavior `evals/`
([testing](standards/testing.md)). A `main` ruleset makes `ci` and
`secrets` required checks.

### F3 — MCP and SessionStart bootstrap

Amended mcp-definition to MCP single-source generation: `MCP.md` frontmatter renders
`dist/mcp.json` and `dist/mcp_config.json`. Fixed the bootstrap render contract
in session-start-bootstrap: one canonical wrapper plus the `using-coacus` entry body renders to
exactly one native artifact per harness, driven by `harness.json` data.

### F4 — Execution governance

Implemented the disk-ledger governor with the default cap of 5 (orchestrator
included), rate-limit parking and a lease TTL, exposed as
`scripts/coacus_governor.py`. Added the TOON payload validator and the generated
discovery manifests.

### F5 — Behavior evals

Added `evals/` with four seeded scenarios, the static scenario validator that
runs in CI, and the opt-in live runner (`--judge-cmd`, `--judge-agent`). Live
evaluation never blocks CI.

### F6 — Corpus import

Imported and translated the corpus using `templates/import/import-manifest.json`
and `scripts/coacus_import.py`, recorded provenance in `sources.lock.json`, and
reorganized the material into the ten-category taxonomy. Delivered (as of F6)
199 knowledge skills, 58 agents, 15 process workflows and one MCP (214 catalog
skill entries: 199 + 15). See [`migration.md`](migration.md) and
[corpus-and-taxonomy](standards/corpus-and-taxonomy.md).

> Post-F7 the corpus was pruned of components coupled to a specific MCP server
> (the `ai-memory` skills + `ai-memory-specialist`, and `autodoc-code-explorer`,
> which drives the AutoDoc MCP). They are deliberately excluded in the import
> manifest (`exclude_skills` / `exclude_agents`); the current corpus is **277
> knowledge skills plus 15 process workflows (292 catalog skill entries, the
> number the installer and `--verify` report)**, 73 agents and one MCP.

### F7 — Final consolidation (done)

Produced the final documentation set (`docs/`), the contribution contract
(`CONTRIBUTING.md`), the changelog, and corpus-and-taxonomy for the import decision.
Added the generated Python API reference (`docs/reference/python-api.md`),
rendered from module/function docstrings by `engine/generators/docstrings.py`
during `generate`, and reconciled the top-level README with the shipped corpus.

### F8 — Completeness verification (done)

Standing verification that nothing from the sources was left behind:
`engine/validators/completeness.py` reconciles the import manifest against the
source repositories (when present locally), the target tree, `sources.lock.json`,
the generated catalog and the agent skill references — recognising intentional
renames (`name_dir_fixes`) and merges (`agent_merges`). Run it with
`python3 scripts/coacus.py completeness` (also run in CI). Current result:
`completeness OK: nothing left behind`.
