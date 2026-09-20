# Changelog

All notable changes to Coacus are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/); entries are grouped by
development phase (F0–F8) because the repository has not yet cut version tags.
The repository adheres to [Semantic Versioning](https://semver.org/) once it does.

## [Unreleased] — F8 (completeness) and docs refresh

### Added

- Partial installs in `scripts/coacus_install.py`: `--only <categories>` (matched
  against any path segment under a skill root) and `--skills <globs>`, plus
  `--list` to print the available categories and names. Selection is recorded in
  the `coacus-install.json` manifest, so `--uninstall` stays exact. Useful when a
  harness caps the session-start skills budget (e.g. Codex shortening
  descriptions on a full-corpus install).
- `THIRD-PARTY-NOTICES.md` reproducing the MIT license of the Superpowers
  workflow collection by Jesse Vincent, and pointing at the GPL-3.0 license of
  the imported skills corpus. The installer writes it to each harness skills root.
- `scripts/coacus_import.py` resolves `origin_license` from a `licenses` map in
  the import manifest (`GPL-3.0` for `skills`, `MIT` for `superpowers`) and
  `apply` relabels existing entries in place without re-importing content.
- `engine/validators/completeness.py` and `python3 scripts/coacus.py
  completeness`: reconciles the import manifest against the source repositories,
  the target tree, the committed catalog, provenance (no orphan targets), agent
  skill references and the ADR set (ADR-0001…ADR-0017); recognises renames and
  merges. Wired into CI.
- `engine/generators/docstrings.py`: generates `docs/reference/python-api.md`
  from source docstrings, drift-checked like any generated artifact.
- Per-harness installation tutorial (`docs/install.md`) with an evidence class
  per vendor claim, plus a rewritten top-level `README.md`.

### Changed

- `templates/import/import-manifest.json` now resolves source repositories from
  a portable `{workspace}` token (`COACUS_WORKSPACE` override) instead of
  machine absolute paths.
- `engine/validators/hygiene.py` also scans `templates/**/*.json|yaml|yml`,
  closing the D12 blind spot for data files.
- `harnesses/cursor/harness.json` corrected to the documented Cursor hook path
  (`.cursor/hooks.json`, snake_case `additional_context`).
- Documentation count references reconciled (181 tests, six CLIs).

## [F7] — 2026-09-20 — consolidation

### Added

- Final documentation set under `docs/`: `README.md`, `architecture.md`,
  `usage.md`, `extending.md`, `migration.md`, `roadmap.md`.
- `CONTRIBUTING.md` and `CHANGELOG.md`.
- ADR-0017: corpus import with a data-driven manifest and a reorganized
  ten-category taxonomy.

### Changed

- Top-level `README.md` reconciled with the shipped F6 corpus (199 skills, 58
  agents, 15 workflows, 214 catalog entries).

## [F6] — 2026-09-20 — corpus import

### Added

- `scripts/coacus_import.py` and `templates/import/import-manifest.json`: the
  data-driven corpus importer.
- `sources.lock.json`: provenance for 1163 imported files (ADR-0015).
- Ten-category skill taxonomy under `knowledge/skills/`: `data`, `domains`,
  `engineering`, `frameworks`, `infrastructure`, `languages`, `mapping`,
  `platforms`, `roles`, `security`.
- 199 skills, 58 agents, 15 workflows (14 `superpowers-*` plus `using-coacus`)
  and the `context7` MCP.
- `engine/validators/completeness.py`: read-only reconciliation of source repos,
  lock file and catalog (F8 groundwork).
- `verticals/architecture_si/` with the unified ingest and analyze pipelines.

### Changed

- Superpowers workflows namespaced `superpowers-*` under `methodology/workflows/`.
- `containers` → `program-containers`, `github-actions` → `program-github-actions`,
  `markmap` → `program-markmap`, `moodle` → `program-moodle`.
- Agent merges applied: `explore` + `code-researcher` → `code-explorer`.
- `using-superpowers` replaced by the native `using-coacus` entry workflow.

### Fixed

- Hardened imported code against CodeQL/Bandit findings.
- Replaced the HTML conversion fallback with the stdlib `HTMLParser`.

## [F5] — 2026-09-19 — behavior evals

### Added

- `evals/` with four seeded scenarios: `bootstrap-activation`,
  `skill-first-discipline`, `artifact-lifecycle`, `governance-cap-and-toon`.
- `scripts/coacus_eval.py` with the static scenario gate and the opt-in live
  runner (`--judge-cmd`, `--judge-agent`).
- `engine/validators/evals.py`: deterministic scenario validation, part of
  `coacus.py validate`.
- Scheduled/manual static eval workflow `.github/workflows/evals.yml`.

## [F4] — 2026-09-19 — execution governance

### Added

- `engine/governor/ledger.py` and `scripts/coacus_governor.py`: disk-ledger
  concurrency governor with a default cap of 5, rate-limit parking and a lease
  TTL (ADR-0007).
- `engine/toon.py` and `coacus.py toon <file>`: TOON handoff payload validator
  (ADR-0008).
- Generated discovery manifests `.agents/{skills,mcps,agents}.json` and
  `.agents/entries/<name>.json` (ADR-0006).
- OpenCode governor gate plugin rendering.

## [F3] — 2026-09-19 — MCP and SessionStart bootstrap

### Added

- MCP single-source generation: `MCP.md` → `dist/mcp.json` +
  `dist/mcp_config.json` (ADR-0005, amended to Option B).
- Canonical bootstrap body `methodology/bootstrap/session-start.canonical.md`
  and per-harness rendering for shapes A/B/C (ADR-0016).
- `scripts/coacus_install.py` for per-harness installation with dry-run,
  uninstall and config-dir override.

### Changed

- ADR-0005 amended from a hand-authored triple to one source plus generation.

## [F2] — 2026-09-19 — quality gates

### Added

- Tolerant frontmatter parser covering the reference corpus (folded/literal
  scalars, block and inline lists, nested maps).
- `.github/workflows/ci.yml`: `validate` → `check` → tests, never `generate`.
- `secrets` CI job: pinned, checksum-verified gitleaks in directory mode.
- Two-layer testing strategy recorded in ADR-0011.

### Changed

- CI gating wired but never auto-commits generated output.

### Fixed

- Closed P2 findings from the F1 audits.

## [F1] — 2026-09-19 — foundation

### Added

- `engine/frontmatter.py`, the generators (`agent_manifests`, `bootstrap`,
  `catalog`, `discovery`, `mcp_configs`) and the validators (`agents`, `skills`,
  `mcps`, `hygiene`, `discovery`).
- `scripts/coacus.py`: `generate`, `check`, `validate`.
- Deterministic `tests/` suite (stdlib `unittest`, zero dependencies).
- Agent manifest generation from one source (ADR-0002).
- Catalog generated from disk (ADR-0004).

## [F0] — 2026-09-18 — framework charter

### Added

- Repository skeleton and the decision backlog D1–D12 ratified as ADR-0002…
  ADR-0013.
- ADR-0001 language policy (English).
- ADR-0014 committed generated artifacts and ADR-0015 provenance manifest
  placement.
- The core principle: disk is the truth; generation is the contract.
