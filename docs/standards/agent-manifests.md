# Agent Manifests

**Status:** normative
**Scope:** every agent under `knowledge/agents/<category>/<name>/` and its
generated representations.

## Rule

Each agent has exactly ONE canonical source: `agent.source.md`. The generator
emits every harness and framework representation from it. No representation is
hand-edited, and no representation is a second source of truth.

The generator emits, under a `dist/` folder beside the source:

| Artifact | Consumer |
|---|---|
| `AGENT.md` | Markdown/system-prompt consumers |
| `agent.yaml` | ADK / Antigravity profile |
| `agent.json` | Neutral manifest for frameworks and APIs (LangChain, AutoGen, CrewAI) |
| `plugin.json` | Plugin shim |

`name`, `description` and `skills` MUST stay in sync across representations — and
they do by construction, because they are derived from one header.

### The canonical source

`agent.source.md` carries YAML frontmatter with:

- `name` — kebab-case, MUST equal the enclosing directory name.
- `category` — MUST equal the parent directory name (the category).
- `description` — REQUIRED, English, third person, trigger-oriented.
- `skills` — a block list of REPOSITORY-RELATIVE paths (for example
  `knowledge/skills/...`). Every listed path MUST exist.

`model` MUST be omitted from the canonical source. A harness resolves the model
at runtime; the framework does not pin one.

### Generated `model`

`model: inherit` appears ONLY in the generated `agent.yaml`, where ADK/Antigravity
interprets it as "use the user's model". It MUST NOT be copied into `AGENT.md`,
`agent.json` or the canonical source. Omitting `model` in the generated Markdown
and JSON is the contract; a framework consumer resolves the real model from its
own configuration.

### Link rewriting

Canonical agent bodies link skills with root-relative paths. The generated
`dist/AGENT.md` sits four levels below the root, so the generator rewrites those
links against `dist/`; source links stay root-relative.

## Rationale

The source repositories shipped incompatible packaging dialects — a
four-file quadruple that drifted (three missing `plugin.json`), a reduced pair,
and a JS/TS plugin. Deriving all representations from one file makes the drift
class impossible rather than merely detectable, and adding a new representation
target later is a legitimate engine variation point.

## Enforcement

- `engine/validators/agents.py` (via `python3 scripts/coacus.py validate`) checks
  required keys, kebab-case name equal to the directory, category equal to the
  parent directory, unique slugs, existing skill paths and a non-empty body.
- `engine/generators/agent_manifests.py` owns `write_all` and `check`;
  `python3 scripts/coacus.py check` fails when a `dist/` tree diverges from a
  fresh regeneration.
- `tests/test_generators.py` and `tests/test_idempotency.py` assert the emitted
  shapes and byte-idempotent regeneration.
