# Normative Standards

This directory contains the normative standards of the Coacus framework. Every standard defines strict, machine-enforceable contracts, rules, rationales, and validation surfaces governing the generation, authoring, and lifecycle of skills, agents, workflows, and harness configurations.

All standards are written in English (see [`english-only.md`](english-only.md)) and enforced during pre-flight generation (`python3 scripts/coacus.py generate`) and validation (`python3 scripts/coacus.py validate`).

---

## Index of Standards

### 1. Architecture & Core Principles

| Standard | Scope & Mission |
| :--- | :--- |
| [`principles.md`](principles.md) | The fundamental architectural axioms of Coacus (D1 through D12): single source of truth, disk as truth, measured counts, and portability across AI harnesses. |
| [`single-source.md`](single-source.md) | Single-source authoring rules. Canonical sources live in `knowledge/`, `methodology/`, or `harnesses/`; all derived formats in `dist/`, `.agents/`, and `catalog/` are generated. |
| [`generated-artifacts.md`](generated-artifacts.md) | Contracts for machine-generated code and manifests. Generated files are committed, deterministically reproducible, and guarded against manual editing. |
| [`session-start-bootstrap.md`](session-start-bootstrap.md) | Specification of the per-harness bootstrap wrapper mechanism (Hook, Plugin, or Instruction Rule) executed at session start. |
| [`discovery.md`](discovery.md) | Single-scan discovery protocol via `.agents/{skills,agents,mcps}.json` and fast index loading without recursive filesystem scans. |
| [`routing.md`](routing.md) | Agent and skill routing engine (`scripts/coacus_route.py`), intent matching, and semantic index resolution. |

### 2. Authoring, Corpus & Taxonomy

| Standard | Scope & Mission |
| :--- | :--- |
| [`corpus-and-taxonomy.md`](corpus-and-taxonomy.md) | Normalization of the 11 top-level categories under `knowledge/skills/`, dedup gates, flat namespaces, and provenance tracking. |
| [`skill-authoring.md`](skill-authoring.md) | Canonical contract for `SKILL.md` authoring: frontmatter schema, action-oriented bodies without hardcoded tool names, 3rd-person triggers, and word-count boundaries (<3500 words). |
| [`agent-manifests.md`](agent-manifests.md) | Canonical agent definition in `agent.source.md`, prohibition of hardcoded models (enforcing `model: inherit`), and generation of `agent.yaml`, `agent.json`, and `plugin.json`. |
| [`mcp-definition.md`](mcp-definition.md) | Canonical declaration of Model Context Protocol (MCP) servers via the triple: `MCP.md`, `mcp.json`, and `mcp_config.json`. |
| [`english-only.md`](english-only.md) | Strict English-only mandate across all canonical bodies, code identifiers, frontmatter, and machine manifests. |
| [`version-freshness.md`](version-freshness.md) | Dynamic resolution and provenance pinning of external libraries, standards, and framework versions via primary package registries and publisher sources. |

### 3. Product, Design & Plan Artifacts

| Standard | Scope & Mission |
| :--- | :--- |
| [`product-and-design-truth.md`](product-and-design-truth.md) | Separation of durable business context (`PRODUCT.md`) from visual systems (`DESIGN.md`), 4 surface modes (`Persuade`, `Operate`, `Read`, `Experience`), and Anti-AI Slop Mandate. |
| [`ui-style-architecture.md`](ui-style-architecture.md) | The 14-part content architecture for canonical UI styles, style-purity boundaries, accessibility and consumer-integration limits. |
| [`plan-artifacts.md`](plan-artifacts.md) | Structure, lifecycle, and strict isolation of implementation plans and interactive artifacts under the brain directory (`RequestFeedback: true`). |
| [`decision-records.md`](decision-records.md) | Architecture Decision Records (ADRs) authored under `docs/decisions/` using the MADR 3.0 format. |

### 4. Governance, Runtime & Lifecycle Guardrails

| Standard | Scope & Mission |
| :--- | :--- |
| [`orchestration-governance.md`](orchestration-governance.md) | Multi-agent concurrency limits (Governor ledger, max 5 subagents + orchestrator), rate-limit backoff, and topology isolation. |
| [`toon-protocol.md`](toon-protocol.md) | Task-Oriented Object Notation (TOON) payload schema for structured, loss-free handoffs between autonomous agents. |
| [`lifecycle-guardrails.md`](lifecycle-guardrails.md) | PAER policy runtime (`engine/guardrail/`), fail-open posture, event interception, and native hook rendering per harness. |
| [`self-improvement-loop.md`](self-improvement-loop.md) | Opt-in, deterministic proposal pipeline (`scripts/coacus_improve.py`) with dry-run ledger audit and fail-open execution. |
| [`untrusted-content.md`](untrusted-content.md) | Defense-in-depth isolation against prompt injection, indirect context pollution, and unvalidated third-party inputs. |
| [`secrets-portability.md`](secrets-portability.md) | Portability of environment variables and access keys using `{env:VAR}` syntax, strictly forbidding hardcoded secrets. |

### 5. Provenance, Ingestion & Quality Assurance

| Standard | Scope & Mission |
| :--- | :--- |
| [`provenance.md`](provenance.md) | SHA-256 integrity hashing and source commit tracking recorded in `sources.lock.json` for every ingested and native asset. |
| [`knowledge-ingestion.md`](knowledge-ingestion.md) | Document conversion pipelines, PDF/Markdown normalization, and metadata tagging under `engine/dispatcher/`. |
| [`testing.md`](testing.md) | Deterministic testing standards using Python standard library `unittest`, the pinned language-detector test dependency and behavioral evals. |
| [`evidence.md`](evidence.md) | Concrete artifact and telemetry verification requirement: every architectural assertion must be supported by reproducible evidence. |

---

## Machine Enforcement

Standards are not advisory guidelines — they are compiled and validated by Python modules in `engine/validators/`:

```bash
# 1. Regenerate all derived artifacts from canonical sources
python3 scripts/coacus.py generate

# 2. Run the complete validator suite against the standards
python3 scripts/coacus.py validate
```
