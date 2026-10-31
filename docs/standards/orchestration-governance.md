# Orchestration Governance

**Status:** normative
**Scope:** every multi-agent run launched from or inside this repository.

## Rule

Parallel work is governed, executable and testable. No agent may spawn a subagent
without a slot acquired from the shared ledger, and ungoverned parallel spawning
is prohibited. Use exactly one acquisition per dispatch: when an adapter manages
acquisition, let it acquire and release the slot; otherwise the caller must use
the governor lifecycle. Never acquire manually in addition to the adapter.

### The governor

The concurrency governor is a disk ledger with platform-specific locking
(`engine/governor/ledger.py`). It MUST be consulted before dispatching a subagent.
Adapter wiring and live enforcement must be verified for the actual host; the
existence of a hook or ledger alone does not establish enforcement.

- Concurrency is managed per harness/provider scope (`ledger-{scope}`) without a
  shared global bottleneck. An exhausted local model (e.g. Ollama cap = 2) does not
  starve cloud harnesses (Antigravity cap = 6, Claude Code cap = 8, Codex cap = 10).
- For unlisted or custom harnesses/providers, the default fallback cap is 6.
- The cap is dynamically configurable via environment variables (`COACUS_MAX_<SCOPE>`,
  `COACUS_MAX_<MODEL>`, `CLAUDE_CODE_MAX_TOOL_USE_CONCURRENCY`, `OLLAMA_NUM_PARALLEL`,
  `ORCH_MAX_CONCURRENT`) or authoritatively updated via `coacus_governor.py set-max <n> [--scope <scope>]`.
- An existing scope ledger persists its effective cap. A higher requested cap may
  raise it, but lowering configuration alone does not reduce a persisted cap;
  lower the relevant caller configuration as well as using `set-max` for a durable
  decrease. A subsequent caller with a higher resolved cap can raise it again.
  Verify the effective result with `status`.
- A caller parks as PAUSED on a 429 rate-limit and reports the backoff hint the
  orchestrator uses to retry (2s → 60s).
- The adapter releases a slot after the task when its lifecycle is supported.
  RUNNING slots are not reaped by age: a crash can leave a stale slot. Recover
  a stale slot only after independently verifying that its worker has stopped;
  otherwise retain it and report the blocker. Never reset the ledger or increase
  its cap merely to clear congestion; either action can permit over-cap work.

The OpenCode gate can release a slot when a background spawn returns rather than
when its worker finishes. Until a runtime fix is verified, governed background
dispatch on that adapter is prohibited: report this limitation and use a
supported foreground dispatch if permitted. Do not claim the gate bounds the
lifetime of background workers.

The Antigravity hook denies recognized subagent spawn on all platforms until host
call identity and worker lifetime are verified; recognized list and kill operations
remain allowed. Live host behavior is unverified. Do not claim runtime enforcement;
report a blocker rather than dispatching without established governance.

The command surface is `scripts/coacus_governor.py`:
`acquire`, `release`, `fail`, `paused`, `status`, `health`, `reset`, `set-max`.

### The orchestrator

The main chat acts as orchestrator for delegated work; it need not spawn a
separate `multi-agent-orchestrator`. Delegate substantive specialist work to
routed specialists when delegation is available and permitted. A dispatched
subagent executes its bounded assignment and does not recursively orchestrate
unless explicitly tasked to coordinate.

Decompose work into dependency-aware, non-overlapping tasks. Dispatch independent
ready tasks concurrently up to the actual free governor capacity and any lower
applicable limit; queue the remainder. A proposal or status check does not reserve
a slot: each dispatch still requires acquisition. If delegation is unavailable,
prohibited, or cannot be governed, report the explicit blocker; do not silently
substitute ungoverned delegation. Follow the user's instructions on whether to
proceed inline. Delegation never grants approval for destructive, privileged,
external, or otherwise approval-gated actions; obtain required human approval.

The orchestrator:

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

### State-through-tools context hygiene and CLI portability

To preserve LLM context windows and prevent token saturation during long-running or multi-agent sessions:

1. **State moves through tools, never context:**
   - Append-only or cumulative state files (e.g. `seen_jobs.json`, processed message IDs, triage queues, audit event streams) MUST NOT be ingested in their entirety into conversational context.
   - Agents interact with state strictly through deterministic helper CLI tools that expose filtered candidate queries, dry-run sweeps, and atomic update flags (`apply --results <temp.json>`).
2. **Cross-platform CLI I/O and process hygiene:**
   - Helper scripts written in Python MUST defensively reconfigure `sys.stdout` and `sys.stderr` to UTF-8 on Windows (`reconfigure(encoding="utf-8")`) without closing underlying binary streams.
   - Scripts that discover Python interpreters on Windows MUST detect and skip Microsoft Store `WindowsApps` 0-byte redirection stubs, resolving only fully qualified Python executables.

### Health

`coacus_governor.py health` verifies the ledger is readable and consistent. A
cross-process cap test ships with the governor; the rendered gate
`harnesses/opencode/bootstrap/governor-gate.js` enforces the same ledger from the
OpenCode adapter.

## Rationale

Multi-agent runs need bounded concurrency, deterministic rate-limit handling and a
hard ban on ungoverned spawning. A disk ledger makes governance
executable and testable rather than prose, subject to host and adapter limitations,
and adds no external broker dependency
before multi-host operation is actually required.

## Enforcement

- `scripts/coacus_governor.py` exposes the runtime command surface
  (`acquire/release/fail/paused/status/health/reset`) over
  `engine/governor/ledger.py`.
- `harnesses/opencode/bootstrap/governor-gate.js` is the OpenCode gate; its
  background slot-lifetime limitation above remains a dispatch blocker.
  `harnesses/*/harness.json` declares plugin wiring.
- `tests/test_governor.py` exercises governor behavior, including cross-process capacity.
- The TOON half is enforced by `engine/toon.py` via
  `python3 scripts/coacus.py toon <file>`.
