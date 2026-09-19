# Coacus

A unified, multi-harness **agentic framework** covering development, information
security, and infrastructure. Coacus fuses three complementary sources into one
portable asset library — skills, agents, MCPs, methodology and governance — that
runs identically across AI coding harnesses (OpenCode, Claude Code, Antigravity,
Codex, Cursor, and frameworks like LangChain/AutoGen/CrewAI).

**Repository language: English** (see [ADR-0001](docs/adr/ADR-0001-language-policy.md)).

## Core principle

> **Disk is the truth; generation is the contract.**
> Every canonical artifact has ONE source. All per-harness representations are
> GENERATED and verified by a drift check (`scripts/coacus.py check`); the CI
> workflow executing it is authored in F2 and becomes active once pushed.
> Drift is a build error, not silent debt.

## Layout

```text
Coacus/
├── knowledge/          # WHAT to know: skills/, agents/, mcps/, rules/
├── methodology/        # HOW to work: workflows/ + bootstrap (SessionStart)
├── verticals/          # domain applications (architecture-si: ingest→markdown→analyze)
├── harnesses/          # thin per-harness adapters (harness.json + bootstrap render, F3)
├── templates/          # single source of templates (authoring + domains)
├── engine/             # closed core: generators, validators (dispatcher/governor: later phases)
├── scripts/            # thin CLI (coacus.py)
├── catalog/            # GENERATED catalog (disk is the truth)
├── .agents/            # GENERATED discovery manifests (single-scan per session)
├── tests/              # deterministic infra tests (CI gate; F2)
├── evals/              # LLM behavior evals with judge (separate pipeline)
└── docs/adr/           # architecture decision records (MADR, English)
```

## Quickstart

```bash
python3 scripts/coacus.py generate   # regenerate per-agent dist/, .agents/, catalog/
python3 scripts/coacus.py check      # fail if generated artifacts are stale
python3 scripts/coacus.py validate   # schema + hygiene validators
python3 -m unittest discover -s tests  # deterministic test suite

python3 scripts/coacus_install.py opencode   # install rendered artifacts into a harness
```

CI (`.github/workflows/ci.yml`) runs `validate` → `check` → `tests` plus a
pinned gitleaks secrets scan — it never runs `generate` (that would mask drift).
It runs on push/PR; a `main` ruleset makes `ci` + `secrets` required checks.

See [`docs/install.md`](docs/install.md) for per-harness installation.

## Canonical artifacts

| Artifact | Single source | Generated representations |
|---|---|---|
| Skill | `knowledge/skills/**/SKILL.md` + `methodology/workflows/**/SKILL.md` | catalog entry |
| Agent | `knowledge/agents/**/agent.source.md` | `dist/AGENT.md`, `agent.yaml`, `agent.json`, `plugin.json`, `.agents/<name>.json` |
| MCP | `knowledge/mcps/<mcp>/MCP.md` (frontmatter) | `dist/mcp.json`, `dist/mcp_config.json` |
| Harness adapter | `harnesses/<h>/harness.json` | rendered bootstrap (`harnesses/<h>/bootstrap/`, shapes A/B/C) |

Phase tags mark representations produced in later phases.

## Hard conventions

- No plaintext secrets — `{env:VAR}` only (D12); no absolute paths.
- Skills prescribe **actions, never harness tools** (D2); tool mappings live in `references/`.
- kebab-case names; `description` in 3rd person, trigger-oriented.
- `model` omitted in canonical sources; resolved per harness (D1).
- All repository content in English (ADR-0001); PT-BR imports are translated.

## Status

Phase **F3 — MCP + SessionStart Bootstrap**: implementation complete (uncommitted
at the time of writing) — MCP single-source generation + validator; canonical
bootstrap wrapper rendered from the entry skill (`using-coacus`); `harness.json`
adapters for opencode (B), claude-code (A), antigravity (C), codex
(native-discovery) and cursor (stub); `scripts/coacus_install.py` for per-harness
installation. OpenCode live acceptance passed; claude-code is structure-verified
only (binary not installed) — see `docs/install.md`. Decision backlog D1–D12
ratified plus ADR-0015/0016; migration of the three source repositories starts at F6.
