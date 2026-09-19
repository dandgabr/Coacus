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
> GENERATED and verified by a drift check (`scripts/coacus.py check`); CI wiring
> lands in F2. Drift is a build error, not silent debt.

## Layout

```text
Coacus/
├── knowledge/          # WHAT to know: skills/, agents/, mcps/, rules/
├── methodology/        # HOW to work: workflows/ + bootstrap (SessionStart)
├── verticals/          # domain applications (architecture-si: ingest→markdown→analyze)
├── harnesses/          # thin per-harness adapters (harness.json + bootstrap render, F3)
├── templates/          # single source of templates (authoring + domains)
├── engine/             # closed core: generators, validators, dispatcher, governor
├── scripts/            # thin CLI (coacus.py)
├── catalog/            # GENERATED catalog (disk is the truth)
├── .agents/            # GENERATED discovery manifests (single-scan per session)
├── tests/              # deterministic infra tests (blocking CI)
├── evals/              # LLM behavior evals with judge (separate pipeline)
└── docs/adr/           # architecture decision records (MADR, English)
```

## Quickstart

```bash
python3 scripts/coacus.py generate   # regenerate per-agent dist/, .agents/, catalog/
python3 scripts/coacus.py check      # CI drift check (fails on un-regenerated diff)
python3 scripts/coacus.py validate   # schema + hygiene validators
python3 -m unittest discover -s tests  # deterministic test suite
```

## Canonical artifacts

| Artifact | Single source | Generated representations |
|---|---|---|
| Skill | `knowledge/skills/**/SKILL.md` | catalog entry |
| Agent | `knowledge/agents/**/agent.source.md` | `dist/AGENT.md`, `agent.yaml`, `agent.json`, `plugin.json`, `.agents/<name>.json` |
| MCP | triple: `MCP.md` + `mcp.json` + `mcp_config.json` (hand-authored, F3) | per-harness config (Option B, later) |
| Harness adapter | `harnesses/<h>/harness.json` (F3) | bootstrap render (F3) |

Phase tags mark representations produced in later phases; F1 generates the
catalog, agent manifests and discovery entries.

## Hard conventions

- No plaintext secrets — `{env:VAR}` only (D12); no absolute paths.
- Skills prescribe **actions, never harness tools** (D2).
- kebab-case names; `description` in 3rd person, trigger-oriented.
- `model` omitted in canonical sources; resolved per harness (D1).
- All repository content in English (ADR-0001); PT-BR imports are translated.

## Status

Phase **F1 — Foundation** in progress. Decision backlog D1–D12 fully ratified
(see `docs/adr/`); migration of the three source repositories starts at F6.
