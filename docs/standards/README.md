# Coacus standards

Normative standards for the framework. A standard states a rule and names the
validator that enforces it. The rule is what governs the repository.

| Standard | What it governs |
|---|---|
| [`principles.md`](principles.md) | The core principle and the four project principles every other standard inherits. |
| [`english-only.md`](english-only.md) | Repo-wide English-only content, and the translation of imported non-English material. |
| [`skill-authoring.md`](skill-authoring.md) | `SKILL.md` structure, placement, agnostic bodies and per-harness adapters. |
| [`agent-manifests.md`](agent-manifests.md) | The single `agent.source.md` source and its generated representations. |
| [`generated-artifacts.md`](generated-artifacts.md) | Catalog-from-disk, committed generated output and the drift check. |
| [`mcp-definition.md`](mcp-definition.md) | The single MCP source and its generated harness configs. |
| [`discovery.md`](discovery.md) | Generated `.agents/` manifests and the single-scan-per-session rule. |
| [`orchestration-governance.md`](orchestration-governance.md) | The concurrency governor, the cap, rate-limit handling and orchestrator duties. |
| [`toon-protocol.md`](toon-protocol.md) | The TOON handoff payload fields, status enum and secret/path rules. |
| [`session-start-bootstrap.md`](session-start-bootstrap.md) | SessionStart injection and the one-body bootstrap render contract. |
| [`single-source.md`](single-source.md) | One home per script and template; no unverified copies. |
| [`testing.md`](testing.md) | The deterministic test gate and the two-tier behavior evals. |
| [`knowledge-ingestion.md`](knowledge-ingestion.md) | The open-closed ingestion dispatcher and format handlers. |
| [`secrets-portability.md`](secrets-portability.md) | `{env:VAR}` secrets and the ban on machine-specific absolute paths. |
| [`provenance.md`](provenance.md) | The `sources.lock.json` schema, dedup key and drift key. |
| [`corpus-and-taxonomy.md`](corpus-and-taxonomy.md) | The data-driven import manifest, the ten-category taxonomy and the dedup gate. |

The documentation index is [`../README.md`](../README.md). Repository-wide rules
for agents live in [`../../AGENTS.md`](../../AGENTS.md); the contribution contract
lives in [`../../CONTRIBUTING.md`](../../CONTRIBUTING.md).

## How a standard is enforced

Every standard ends with an `Enforcement` section naming the validator or CI job
that checks it. The local equivalent of the full gate:

```bash
python3 scripts/coacus.py validate
python3 scripts/coacus.py check
python3 scripts/coacus.py completeness
python3 -m unittest discover -s tests
```

`.github/workflows/ci.yml` runs exactly these four steps and never `generate`.
