# Routing

**Status:** normative
**Scope:** the agent routing index, the curated lexicon, the deterministic router
and the surfaces that use it (the orchestrator and the CLI).

## Rule

Agent selection is data-driven and offline. A caller picks agents by reading a
generated index, never by guessing a name or re-scanning the tree.

### Two modes, one source

- **Mode M — manual.** The user names the agents. `coacus_route.py --list` browses
  the index; `coacus_route.py --agents a,b` validates an explicit selection. An
  unknown name is an ERROR — with close suggestions when one exists — never a
  silent drop.
- **Mode A — automated curation.** `coacus_route.py "<prompt>"` ranks the agents
  for the prompt and prints the best candidates. The ranking is lexical and
  deterministic (``engine/router.py``): curated trigger terms weigh most, then the
  name, then the description and skill slugs. An optional
  `--rerank "<command>"` plugs in a semantic reranker (embeddings, a local model,
  an LLM) behind the same interface and **fails open** when it is absent.

### The index

`.agents/routing.json` is GENERATED from the canonical agents plus
`knowledge/routing/lexicon.json`, the curated bilingual (PT-BR + EN) trigger
vocabulary. One source per fact: the agent's name, category, description and
skills come from its `agent.source.md`; only the triggers are curated. The index
is drift-checked like every generated artifact, and the lexicon must cover every
agent with none extra (`engine/validators/routing.py`).

### Concurrency

Routing PROPOSES; it never spawns or reserves a slot. `--max-slots` caps a
proposal using the governor's reported free slots, a snapshot that can change.
The main chat routes before delegating specialist work and dispatches independent
ready tasks up to actual available capacity and any lower applicable limit. Each
dispatch requires one governor slot; use adapter-managed acquisition where present,
or manual acquisition otherwise, never both. Queue tasks when capacity is exhausted.
OpenCode background dispatch is prohibited until its slot-lifetime fix is verified;
report the limitation and use supported foreground dispatch if permitted.
If delegation is unavailable, prohibited or cannot be governed, report the blocker
rather than silently substituting ungoverned work. Routing does not authorize
approval-gated actions. See [orchestration governance](orchestration-governance.md).

### Language

Prompts are PT-BR and EN; canonical descriptions are English only
([english-only](english-only.md)). The curated lexicon bridges the two, so accent
and language do not block a lexical match. Paraphrase beyond the vocabulary is the
reranker's job, not the lexical scorer's.

### User-invoked only

Routing never observes ambient prompts or spends context on unsolicited
suggestions. Selection happens on an explicit call to
`scripts/coacus_route.py` — by the user, by the orchestrator before it
delegates, or by the planning workflow's roster step (below).

The roster step is the one caller that may route without a user naming an agent:
it routes the plan's OWN task text and MUST present the candidates for human
selection — it proposes, it never auto-selects. See
`../../methodology/workflows/using-coacus/references/coacus-process-conventions.md`
→ "Select agents for a task (roster)".

### Deterministic suggestions

The router's output is deterministic: prefix matching, de-duplicated, sorted
stably. Every suggestion is a STARTING POINT, never an authorization — selection
is not consent, and a routed name is validated (`--agents`) before it is relied
on.

## Rationale

The orchestrator was told to "delegate to appropriate specialized agents" with no
way to determine which — the choice was an unindexed guess and the user selected by
hand. A generated index plus a deterministic scorer makes selection reproducible,
testable and offline, while the curated bilingual lexicon keeps a PT-BR prompt
from matching nothing against English descriptions. The semantic upgrade stays
optional so the framework keeps running with the standard library alone.

## Enforcement

- `engine/generators/routing.py` writes `.agents/routing.json`;
  `python3 scripts/coacus.py check` fails on drift.
- `engine/validators/routing.py` (via `validate`) checks the lexicon covers every
  agent (source) and the index is coherent (artifact).
- `scripts/coacus_route.py` is the command surface (Mode M and Mode A).
- `tests/test_routing.py`, `tests/test_router.py` and
  `tests/test_router_calibration.py` cover the index, the scorer and the observed
  routing quality.
