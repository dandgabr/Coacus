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
├── verticals/          # domain applications: architecture_si (ingest→analyze)
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
python3 scripts/coacus_eval.py validate      # static behavior-eval scenario gate
python3 scripts/coacus_vertical.py formats   # architecture_si document ingestion/analysis
```

CI (`.github/workflows/ci.yml`) runs `validate` → `check` → `tests` plus a
pinned gitleaks secrets scan — it never runs `generate` (that would mask drift).
It runs on push/PR; a `main` ruleset makes `ci` + `secrets` required checks.

See [`docs/install.md`](docs/install.md) for per-harness installation.

## Canonical artifacts

| Artifact | Single source | Generated representations |
|---|---|---|
| Skill | `knowledge/skills/**/SKILL.md` + `methodology/workflows/**/SKILL.md` | catalog entry |
| Agent | `knowledge/agents/**/agent.source.md` | `dist/AGENT.md`, `agent.yaml`, `agent.json`, `plugin.json`, `.agents/entries/<name>.json` |
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

Phases **F0–F6** (F1 foundation · F2 quality gates · F3 MCP + SessionStart
bootstrap · F4 execution governance · F5 behavior evals · F6 corpus import).
The framework now carries the imported corpus — **199 skills, 58 agents and 15
workflows (14 imported + the native `using-coacus`); 214 catalog entries** —
fully translated to English, with generated catalog + discovery,
multi-harness agent manifests, MCP single-source generation, per-harness
SessionStart bootstrap, a concurrency/rate-limit governor, the TOON handoff
validator, a per-harness installer and behavior-eval scenarios. OpenCode live
acceptance passed; claude-code is structure-verified (binary not installed) —
see `docs/install.md` and `evals/README.md`. Decision backlog D1–D12 ratified
plus ADR-0015/0016/0017. Documentation index: [`docs/README.md`](docs/README.md).
Phases F0–F8 complete (F7 consolidation + F8 completeness verification).
