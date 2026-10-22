# Orchestration Governance

**Status:** normative
**Scope:** every multi-agent run launched from or inside this repository.

## Rule

Parallel work is governed, executable and testable. No agent may spawn a subagent
without acquiring a slot from the shared ledger, and ungoverned parallel spawning
is prohibited.

### The governor

The concurrency governor is a disk ledger guarded by `flock`
(`engine/governor/ledger.py`). It MUST be consulted before dispatching a subagent.

- Concurrency is managed per harness/provider scope (`ledger-{scope}`) without a
  shared global bottleneck. An exhausted local model (e.g. Ollama cap = 2) does not
  starve cloud harnesses (Antigravity cap = 6, Claude Code cap = 8, Codex cap = 10).
- For unlisted or custom harnesses/providers, the default fallback cap is 6.
- The cap is dynamically configurable via environment variables (`COACUS_MAX_<SCOPE>`,
  `COACUS_MAX_<MODEL>`, `CLAUDE_CODE_MAX_TOOL_USE_CONCURRENCY`, `OLLAMA_NUM_PARALLEL`,
  `ORCH_MAX_CONCURRENT`) or authoritatively updated via `coacus_governor.py set-max <n> [--scope <scope>]`.
- A caller parks as PAUSED on a 429 rate-limit and reports the backoff hint the
  orchestrator uses to retry (2s → 60s).
- Because the acquiring CLI process is short-lived, slots are released by the
  harness adapter after the task, and on the next turn as a safety net. A crashed
  holder is reclaimed by a lease TTL (`GOVERNOR_LEASE_SECONDS`).

The command surface is `scripts/coacus_governor.py`:
`acquire`, `release`, `fail`, `paused`, `status`, `health`, `reset`, `set-max`.

### The orchestrator

A task that invokes two or more agents MUST route through the
`multi-agent-orchestrator` as supervisor. The orchestrator:

1. Anchors the initial goal and acceptance criteria against scope drift.
2. Supervises each subagent's progress using quantitative tool caps and mentor checks.
3. Mediates conflicts through TOON evidence in `@FILES` (see
   [`toon-protocol.md`](toon-protocol.md)).
4. Intervenes or terminates a subagent that loops, drifts or acts out of scope.

Handoffs between agents MUST be TOON payloads. Free-text handoffs are
non-compliant.

### Quantitative supervision and mentor loop

The supervisor MUST enforce quantitative execution bounds:

- **Differentiated tool-call budgets**: general/deep execution agents operate under
  `MAX_GENERAL_AGENT_TOOL_CALLS = 100`, while limited/refinement/search agents operate
  under `MAX_LIMITED_AGENT_TOOL_CALLS = 20`.
- **Sliding-window loop detection**: `same_tool_limit` triggers after 3–5 identical
  consecutive calls with unchanged inputs or repetitive errors. Exceeding `total_tool_limit`
  forces an immediate pause and supervisor evaluation.
- **`<mentor_analysis>` progress checkpoint**: before redelegating or accepting completion,
  the supervisor answers a 6-question progress check:
  1. Did the subagent produce concrete artifacts or verifiable evidence?
  2. Are tools being called in a repetitive or unproductive loop?
  3. Is the subagent performing unrequested work or touching out-of-scope files?
  4. Can the question be answered directly from the existing context without further calls?
  5. Has the tool-call budget reached 80% without measurable progress?
  6. Is the next step clearly grounded in the user's initial objective?

### Language policy: English-first and dual-channel

To maintain semantic precision in cross-model reasoning and retrieval:

- **Technical wire and memory channel (100% `en`)**: all TOON handoff payloads, tool arguments,
  vector queries, graph triples, and long-term memory entries MUST be strictly in English (`en`).
- **Human communication and reporting channel (`en` default; `en | pt-BR | es` supported)**:
  when interacting with human operators or rendering final deliverables, the supervisor supports
  the three official languages: `en` (canonical default), `pt-BR`, and `es`.

### Cryptographic evidence receipt chain

For high-assurance and security audits, multi-agent workflows MAY emit an Ed25519-signed,
hash-linked DAG of execution receipts:

```text
flow_start -> task_created -> subtask_started -> toolcall_finished -> artifact_recorded -> report_created
```

Each receipt records `receipt_id`, `parent_receipt_ids`, `event_type`, `input_hash`,
`output_hash`, and `artifact_hashes` (SHA-256). Any receipt validation failure halts downstream
processing fail-closed.

### Health

`coacus_governor.py health` verifies the ledger is readable and consistent. A
cross-process cap test ships with the governor; the rendered gate
`harnesses/opencode/bootstrap/governor-gate.js` enforces the same ledger from the
OpenCode adapter.

## Rationale

Multi-agent runs need bounded concurrency, deterministic rate-limit handling and a
hard ban on ungoverned spawning. A disk ledger with `flock` makes governance
executable and testable rather than prose, and adds no external broker dependency
before multi-host operation is actually required.

## Enforcement

- `scripts/coacus_governor.py` exposes the runtime command surface
  (`acquire/release/fail/paused/status/health/reset`) over
  `engine/governor/ledger.py`.
- `harnesses/opencode/bootstrap/governor-gate.js` is the rendered OpenCode gate;
  `harnesses/*/harness.json` declares plugin wiring.
- `tests/test_governor.py` exercises the cross-process cap and lease behavior.
- The TOON half is enforced by `engine/toon.py` via
  `python3 scripts/coacus.py toon <file>`.
