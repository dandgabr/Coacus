# Extending the framework

Coacus is open for extension, closed for modification
([skill-authoring](standards/skill-authoring.md),
[knowledge-ingestion](standards/knowledge-ingestion.md)). Extend it by adding **data**:
a new skill, agent, MCP, harness, workflow, template or ingestion handler is a
new file. The `engine/` core changes only when a new *concept* arrives — a new
representation target, a new validation class, a new bootstrap shape.

After every addition, run the full gate:

```bash
python3 scripts/coacus.py generate
python3 scripts/coacus.py validate
python3 scripts/coacus.py check
python3 -m unittest discover -s tests
```

`generate` refuses to write artifacts while source validation fails, so fix
`[error]` lines before regenerating. `check` must report no drift; CI fails if it
does not.

## Add a skill

1. Copy `templates/authoring/skill.template.md` to
   `knowledge/skills/<category>[/<subcategory>]/<name>/SKILL.md`. Use one of the
   ten categories: `data`, `domains`, `engineering`, `frameworks`,
   `infrastructure`, `languages`, `mapping`, `platforms`, `roles`, `security`.
2. Set `name` to the kebab-case directory name and write a third-person,
   trigger-oriented `description`.
3. Prescribe actions only — no harness tool names. Put tool mappings in
   `references/<harness>-tools.md` beside the skill. Put examples in
   `examples/`, runnable helpers in `scripts/`.
4. Keep paths relative and secrets as `{env:VAR}` ([secrets-portability](standards/secrets-portability.md)).

Validator contract (`engine/validators/skills.py`): frontmatter parses; `name`
is kebab-case and equals the directory; `description` present; the slug is
globally unique across both skill roots (one flat namespace); placement depth is
`knowledge/skills/<category>` or `knowledge/skills/<category>/<subcategory>`;
no nested `SKILL.md`; every local Markdown link resolves. Oversized
descriptions and non-English markers are warnings, not errors.

## Add a workflow (process skill)

Same contract as a skill, but the path is
`methodology/workflows/<name>/SKILL.md` (depth 1). Imported Superpowers
workflows are namespaced `superpowers-<name>`. The native entry workflow
`using-coacus` is the single source of the bootstrap body; if you change how
sessions start, edit that skill, not the bootstrap.

## Add an agent

1. Copy `templates/authoring/agent.source.template.md` to
   `knowledge/agents/<category>/<name>/agent.source.md`. Existing categories:
   `academic-sciences`, `core-orchestration`, `cybersecurity`,
   `data-cloud-devops`, `research-discovery`, `software-engineering`,
   `specialized-domains`.
2. Set `name` to the directory name, `category` to the parent directory name,
   and list every skill in `skills:` as a **repository-root-relative** path
   (`knowledge/skills/.../SKILL.md`).
3. Omit `model`. The generated `agent.yaml` uses `model: inherit`; harnesses
   resolve the real model ([agent-manifests](standards/agent-manifests.md)).

Validator contract (`engine/validators/agents.py`): `name` kebab-case and equal
to the directory; `category` equal to the parent directory; `description`
required; instruction body non-empty; every `skills:` path exists; names unique.

Then add bilingual routing triggers for the new agent to
`knowledge/routing/lexicon.json` ([routing](standards/routing.md)). The routing
validator fails until every agent has a trigger list, so a new agent without one
does not pass `validate`.

`generate` produces `dist/AGENT.md`, `dist/agent.yaml`, `dist/agent.json`,
`dist/plugin.json` and `.agents/entries/<name>.json` from the single source. Do
not hand-edit any of them.

## Add an MCP

1. Copy `templates/authoring/mcp.template.md` to
   `knowledge/mcps/<name>/MCP.md` (flat namespace, globally unique name).
2. Declare the server in frontmatter: `transport`, `command`/`args` or
   `remote_url`, `env_vars` as **names only**, `capabilities`, `requires`,
   `docs`, `author`, `license`, `version`.
3. Reference secrets only as `{env:VAR}`; values never enter the repository.

Validator contract (`engine/validators/mcps.py`): `name` kebab-case and equal to
the directory; `description` required; `transport` is one of `stdio`, `http`,
`streamable-http`, `sse`; `stdio` requires `command`; the HTTP transports
require `remote_url`; `capabilities` is a mapping if present; `env_vars` is a
list of upper-case names.

`generate` writes `dist/mcp.json` and `dist/mcp_config.json`
([mcp-definition](standards/mcp-definition.md)).

## Add a harness

Copy `harnesses/_template/harness.json` to `harnesses/<name>/harness.json` and
fill in the data. A harness manifest declares:

- `bootstrap.supported` and `bootstrap.shape` — `A` (shell hook), `B`
  (in-process), `C` (instructions file) or `native-discovery` (nothing rendered).
- `bootstrap.outputs` — the paths the generator writes and their formats.
- `bootstrap.native_key` / `bootstrap.forbidden_keys` — for shape A, the one
  native JSON key emitted and the aliases never emitted (anti-double-injection).
- `detection` — environment variables the adapter checks.
- `tool_mapping` — action → native tool, injected into the bootstrap.
- `tool_denylist` — tool names banned from canonical skill bodies; the hygiene
  validator unions every harness's denylist.
- `install.method` / `install.target`.

A new harness that uses an existing shape needs **no engine change**: run
`generate`, then `python3 scripts/coacus_install.py <name>` (add a `_plan_<name>`
only if its install mechanism is new). A new *shape* is an engine change in
`engine/generators/bootstrap.py`; see [session-start-bootstrap](standards/session-start-bootstrap.md).

## Add a template

Templates follow [single-source](standards/single-source.md): one
copy, consumed by path. Authoring templates live in `templates/authoring/`.
Domain templates live under `templates/domains/<vertical>/` and already cover
ADRs (`adr.template.md`), C4 models, threat models, DPIAs and security technical
opinions for the `architecture_si` vertical. Add `<name>.template.md` there; no
generator or validator change is needed.

## Add an ingestion format

The dispatcher is open-closed: a new format is a new handler file, and
`engine/dispatcher/__init__.py` never changes
([knowledge-ingestion](standards/knowledge-ingestion.md)).

1. Create `verticals/architecture_si/pipelines/ingest/handlers/<format>.py`.
2. Register the extensions with the decorator and import shared helpers:

```python
from engine.dispatcher import register_converter
from verticals.architecture_si.pipelines.ingest.handlers import _common as common


@register_converter(".myext")
def handle_myext(input_path: str, output_path: str | None = None) -> str:
    # ... produce Markdown ...
    return common.write_markdown(markdown_text, output_path, input_path)
```

3. Accept `input_path, output_path` and ignore unknown keyword options —
   `dispatcher.convert` forwards extras (`toc_only`, `split_chapters`) but falls
   back to the two-argument call when a handler does not accept them.
4. Import no sibling handler. Shared logic goes in `_common.py`.

`dispatcher.load_handlers()` imports every non-underscore module in the handlers
directory, so the new extension appears in
`python3 scripts/coacus_vertical.py formats` immediately. Add a test under
`tests/test_vertical.py` following the existing pattern.

## Adding a new concept

Only these changes belong in `engine/`: a new representation target for an
existing artifact, a new validation class, a new bootstrap shape, or a new
runtime gate. Treat each as a deliberate core change, add tests under `tests/`,
and record the decision as a new standard in `docs/standards/` before merging.
