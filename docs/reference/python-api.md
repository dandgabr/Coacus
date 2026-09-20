# Python API Reference

> GENERATED from source docstrings by `scripts/coacus.py generate` — do not edit.
> Source of truth: the docstrings themselves.

### `engine/frontmatter.py`

Frontmatter parser for Coacus canonical sources.

Tolerant subset of YAML, sufficient for the reference corpus (testing:
stdlib only):

- single-line scalars, with indented continuation lines (multi-line plain)
- folded/literal block scalars: ``>-`` / ``>`` / ``|`` / ``|-``
- block lists (``- item``) and inline lists (``[a, b]`` / ``[]``)
- nested indented maps to any depth (e.g. the ``metadata:`` blocks found in
  49 of the 200 reference skills)

Unknown/extra keys are preserved as-is; the validators decide the canonical
contract. The closing ``---`` must sit at column 0.

#### `class FrontmatterError`

Raised when frontmatter cannot be parsed.


#### `class Document`

Parsed canonical source: metadata plus markdown body.

- `def title(self) -> str` — First ``# H1`` of the body, or an empty string.

#### `def parse(text: str) -> Document`

Parse ``---``-delimited frontmatter plus a markdown body.

### `engine/generators/agent_manifests.py`

Generate multi-harness agent representations from canonical sources (D1).

One canonical ``agent.source.md`` per agent yields, under a ``dist/`` folder:

- ``AGENT.md``     markdown profile (harness system-prompt consumers)
- ``agent.yaml``   ADK/Antigravity profile (``model: inherit``)
- ``agent.json``   neutral manifest for frameworks and APIs
- ``plugin.json``  plugin shim

plus a ``.agents/entries/<name>.json`` discovery entry (D5).

Generated files contain no timestamps so regeneration is byte-idempotent
(generated-artifacts). ``model`` is never emitted for AGENT.md/agent.json; the yaml
profile uses ``model: inherit``.

#### `def discover_sources(root: Path) -> list[Path]`

All canonical agent sources: knowledge/agents/<category>/<name>/.

#### `def generate(source_path: Path, root: Path) -> dict[str, str]`

Compute generated files for one source.

Returns a mapping of repo-relative path to file content. Nothing is
written here; ``write_all`` materializes the outputs.

#### `def expected_outputs(root: Path) -> dict[str, str]`

Union of generated content for every canonical source.

#### `def write_all(root: Path) -> list[str]`

Materialize all generated files. Returns repo-relative paths written.

#### `def check(root: Path) -> list[str]`

Drift check (generated-artifacts): disk vs a fresh regeneration, plus orphans.

### `engine/generators/bootstrap.py`

Render the SessionStart bootstrap per harness from a single canonical body (D8).

One canonical wrapper (`methodology/bootstrap/session-start.canonical.md`) plus
the entry skill body are rendered into the native artifact(s) each harness
expects, driven by data in `harnesses/<h>/harness.json` (OCP: a new harness is a
new data file; a new shape is an engine change).

Shapes:
- A (hook): a POSIX shell script that emits ONE native JSON field, plus the
  harness hook config. Claude Code and Codex read
  ``hookSpecificOutput.additionalContext``; Cursor reads the top-level
  ``additional_context``. The native key and the hook config come from
  ``harness.json``; the forbidden alias is never emitted (session-start-bootstrap).
- B (in-process): a JS module that injects the bootstrap into the first user
  message, with an anti-reinjection guard.
- C (instructions-file / rule): a markdown context file plus the plugin manifest
  that declares it. Antigravity rules are capped at 12,000 characters.
- native-discovery: nothing rendered (the harness surfaces skills natively).

Rendered artifacts are committed and drift-checked (generated-artifacts); no timestamps.

#### `def discover_harnesses(root: Path) -> list[Path]`

All harness manifests except the authoring template.

#### `def load_harness(path: Path, root: Path) -> dict`

Parse a ``harness.json``; a malformed file raises a readable ValueError.

#### `def render(harness: dict, root: Path) -> dict[str, str]`

Compute rendered files for one harness (repo-relative path -> content).

#### `def expected_outputs(root: Path) -> dict[str, str]`

Union of rendered content for every harness.

#### `def write_all(root: Path) -> list[str]`

Materialize all rendered bootstrap files. Returns repo-relative paths.

#### `def check(root: Path) -> list[str]`

Drift check: expected vs disk, plus orphan detection (generated-artifacts).

### `engine/generators/catalog.py`

Generate the repository catalog from disk (D3: disk is the truth).

Writes ``catalog/catalog.json`` (machine index) and ``catalog/INDEX.md``
(human index) — purely content-derived, no timestamps, so ``check`` can
verify idempotency and CI can fail on drift (generated-artifacts).

#### `def build(root: Path) -> dict`

Build the catalog structure from canonical sources on disk.

#### `def write(root: Path) -> list[Path]`

Materialize the catalog and its human index. Returns written paths.

#### `def check(root: Path) -> list[str]`

Drift check for the catalog and its index (generated-artifacts).

### `engine/generators/discovery.py`

Generate consolidated discovery manifests from disk (discovery).

Writes `.agents/{skills,mcps,agents}.json` — each a list of `entries[].path`
(a directory or source file), derived purely from disk so discovery is
deterministic and drift-checked (generated-artifacts). Single-scan rule: agents read these
indexes once per session (AGENTS.md).

The per-agent `.agents/entries/<name>.json` files are still produced by
`agent_manifests` (fine-grained fingerprints); these consolidated manifests are
the coarse by-kind index.

#### `def build(root: Path) -> dict[str, dict]`

Build the three discovery manifests (skills, mcps, agents) from disk.

#### `def write_all(root: Path) -> list[str]`

Materialize ``.agents/{skills,mcps,agents}.json``; return written paths.

#### `def check(root: Path) -> list[str]`

Drift check for the consolidated discovery manifests (generated-artifacts).

### `engine/generators/docstrings.py`

Generate a Python API reference from module/function/class docstrings (F7).

Docstrings are the single source of truth (the "disk is the truth" principle):
this generator walks the framework's Python modules, extracts signatures and
docstrings via the stdlib ``ast`` parser, and writes a Markdown reference. The
output is committed and drift-checked (generated-artifacts) like any other generated
artifact, so documentation cannot fall out of sync with the code.

#### `def build(root: Path) -> str`

Render the Markdown API reference from the sources' docstrings.

#### `def write(root: Path) -> Path`

Write the generated API reference to disk and return its path.

#### `def check(root: Path) -> list[str]`

Drift check for the generated API reference (generated-artifacts).

### `engine/generators/mcp_configs.py`

Generate per-MCP harness declarations from a single canonical source (D4).

Supersedes the hand-authored MCP triple of mcp-definition: `knowledge/mcps/<mcp>/MCP.md`
is the single source; the generator derives:

- `dist/mcp.json`         server declaration (name, transport, command/url,
                          args, ``{env:VAR}`` placeholders, capabilities)
- `dist/mcp_config.json`  setup metadata (description, requires, env VAR names,
                          docs, author, license, version)

Generated files are committed and drift-checked (generated-artifacts), contain no
timestamps, and never carry secret values.

#### `def discover_sources(root: Path) -> list[Path]`

Canonical MCP sources: ``knowledge/mcps/<mcp>/MCP.md`` (flat).

#### `def generate(source_path: Path, root: Path) -> dict[str, str]`

Compute ``dist/mcp.json`` and ``dist/mcp_config.json`` for one MCP.

#### `def expected_outputs(root: Path) -> dict[str, str]`

Union of generated content for every canonical MCP source.

#### `def write_all(root: Path) -> list[str]`

Materialize all generated MCP files. Returns repo-relative paths.

#### `def check(root: Path) -> list[str]`

Drift check: expected vs disk, plus orphan detection (generated-artifacts).

### `engine/governor/ledger.py`

On-disk concurrency governor with an flock-guarded slot ledger (orchestration-governance).

Bounds how many agents may run at once (default 5, orchestrator included),
handles rate-limit (429) by parking a caller as PAUSED for retry, and is the
executable counterpart of the AGENTS.md governance rule. Zero dependencies.

Ledger format (text, one record per line):
    MAX <n>                                  # authoritative cap (first line)
    RUNNING <caller> <yes|no> <token> <pid> <started-unix-ts>
    PAUSED  <caller> <unix-ts> <attempts>

Callers are validated tokens (``[A-Za-z0-9._:-]+``); matching is EXACT, never
prefix-based. The cap is persisted so no caller can raise it. Stale RUNNING
rows (dead PID or older than the lease) are reaped before capacity is judged,
so a crashed holder cannot leak a slot forever.

#### `def state_dir() -> Path`

The governor's state directory (``GOVERNOR_STATE_DIR`` or a runtime default).

#### `class Ledger`

A file-backed slot ledger guarded by ``fcntl.flock``.

- `def acquire(self, caller: str, orchestrator: bool=False, timeout: float=30.0) -> str | None` — Reserve a slot. Returns the token, or None if the cap stayed full.
- `def release(self, caller: str) -> None` — Release the slot held by ``caller`` (a no-op if it holds none).
- `def fail(self, caller: str, attempts: int=1) -> None` — Park a caller as PAUSED after a rate-limit (429) for retry.
- `def paused(self) -> list[dict]` — Callers parked for retry, with a backoff hint (2s -> 60s).
- `def clear_paused(self, caller: str | None=None) -> None` — Drop PAUSED rows for ``caller``, or for every caller when ``None``.
- `def status(self) -> dict` — Reap stale leases and return the current running/paused/slots snapshot.
- `def reset(self) -> None` — Clear every record, returning the ledger to an idle state.

### `engine/provenance.py`

Provenance manifest for imported artifacts (P4 / provenance).

Lives at the repository root as ``sources.lock.json`` — deliberately OUTSIDE
the generated ``catalog/`` surface so that the per-import ``imported_at``
timestamp cannot break the generated-artifacts drift check (the catalog generator must
stay timestamp-free and idempotent).

This module owns the schema and the (empty) seed. The F6 import pipeline
populates entries; nothing here writes timestamps at generation time.

#### `def empty() -> dict`

Seed structure, deterministic (no timestamp).

#### `def load(root: Path) -> dict`

Read the manifest, or return the empty seed if absent.

#### `def validate(root: Path) -> list[str]`

Check the manifest shape; entries may be empty pre-import.

#### `def write(root: Path, data: dict | None=None) -> Path`

Write the manifest (seed by default). Import pipeline supplies entries.

#### `def sync_authoring(root: Path, imported_at: str) -> list[str]`

Ensure every authored source has an ``authoring`` provenance entry.

The import pipeline records imported files; a file authored directly in this
repository (a new skill, workflow or agent) has no importer to record it, so
F8 completeness reported it as an orphan. This adds a missing entry and, when
an authored entry already exists, refreshes its hashes. It never touches an
imported entry and never removes one. Returns the target paths it added.

Idempotent: a second call with the same tree adds nothing, and an unchanged
authored entry keeps its original ``imported_at`` (only a content change
rewrites the hash).

### `engine/toon.py`

TOON (Token-Oriented Object Notation) payload parsing and validation (toon-protocol).

TOON is the compact handoff format between agents:

    @FROM: <emitter>
    @TO: <receiver-or-orchestrator>
    @STATUS: <OK | CONFLICT | BLOCKED | NEED_INFO>
    @CTX: <context id>
    @FILES: <path:lines>;<path:lines>       (optional, relative paths only)
    @SUMMARY: <compact summary>
    @ACTION_NEEDED: <objective next step>    (optional)

JSON is reserved for machine contracts; TOON is for prose handoffs.

#### `def parse(text: str) -> dict[str, str]`

Parse a TOON payload into a field->value mapping (duplicates: last wins).

#### `def validate(text: str) -> list[str]`

Return a list of error strings; empty list means a valid payload.

#### `def is_valid(text: str) -> bool`

Return ``True`` when ``text`` is a valid TOON payload (no errors).

### `engine/validators/agents.py`

Validate canonical agent sources (frontmatter contract, D1/agent-manifests).

Checks: required keys, kebab-case name matching the directory, category
matching the parent directory, existing skill paths, unique slugs, a non-empty
instruction body and the D1 rule that `model` is omitted at source (harnesses
resolve the actual model; the generated `agent.yaml` uses `model: inherit`).

#### `def validate(root: Path) -> list[str]`

Return a list of error strings; empty list means valid.

### `engine/validators/completeness.py`

Completeness verification (F8): nothing from the sources was left behind.

A read-only audit that answers "did the import miss anything?" by reconciling:

- the import manifest's declared expectations against the source repositories
  (when they are available locally), and
- the imported corpus against `sources.lock.json` and the generated catalog.

It is dependency-free and degrades gracefully: on a machine without the source
repos it still verifies the target side (lock + catalog + references).

#### `def validate(root: Path) -> list[str]`

Return a list of completeness gaps (empty = nothing left behind).

### `engine/validators/discovery.py`

Validate generated discovery manifests (discovery).

Two kinds live under ``.agents/``:

- per-agent entries ``entries/<name>.json``: ``{name, description, category,
  source, dist, fingerprint}`` — the fingerprint is RECOMPUTED from the source
  bytes, so a tampered or stale entry fails even before the drift check. The
  ``entries/`` subdirectory keeps agent names from colliding with the
  consolidated stems.
- consolidated by-kind indexes ``skills.json`` / ``mcps.json`` / ``agents.json``:
  ``{entries: [{path}]}`` — the coarse single-scan surface.

#### `def validate(root: Path) -> list[str]`

Return a list of error strings; empty list means valid.

### `engine/validators/docs.py`

Prose-count reconciliation (D5 — counts are measured, never copied).

Prose drifts. The documentation states counts — skills, agents, workflows, MCPs,
catalog entries, provenance entries — that the generator and the lock file already
know, and hand-copied numbers fall behind the disk. This validator reconciles
every declared number (a) in the README corpus table and (b) anywhere in the
LIVING documentation, so a stale count is a build error rather than a silent lie.

Measured sources: the generated ``catalog/catalog.json`` counts, the on-disk
``methodology/workflows`` tree, and the entry count of ``sources.lock.json``.

Historical records are exempt by design: ``CHANGELOG.md`` and ``docs/migration.md``
describe past states, and ``docs/roadmap.md`` marks a past state with an "as of
F<n>" era, so a paragraph that is explicitly historical is not reconciled.

Counts have no generator (the test suite), so they are never stated as a fixed
number in the docs; the docs give the command to measure them instead.

#### `def validate(root: Path) -> list[str]`

Return prose-count mismatches (empty = docs agree with disk).

### `engine/validators/evals.py`

Validate behavior-eval scenarios (testing).

Scenarios live at ``evals/scenarios/<id>/scenario.json``. The static validator
is deterministic (no LLM) and safe for CI; it checks the schema, that the
target harness exists, that every check is well-formed, and that no scenario
string carries a secret or an absolute path (D12).

#### `def discover(root: Path) -> list[Path]`

Return every scenario file (``evals/scenarios/<id>/scenario.json``).

#### `def validate(root: Path) -> list[str]`

Return a list of error strings; empty list means valid.

### `engine/validators/freshness.py`

Version-freshness check (version-freshness).

Canonical artifacts pin versions of standards, frameworks, libraries and
regulations in their instruction bodies. A training-memory pin is a claim about
an unknown instant, so every such pin must sit near evidence that it was
resolved: a source anchor (a URL, an RFC identifier, a publisher or vendor name)
or an explicit resolution marker (``resolved YYYY-MM-DD``).

This validator reports WARNINGS, not errors. It keeps a machine surface on the
pin list so the corpus can be reconciled; the standard promotes it to a hard gate
once the list is clean.

Prose only. The scan excludes the YAML frontmatter, fenced code blocks and inline
code spans: those are samples and identifiers, not behavioural claims, and flagging
them buries the real pins.

Only MOVING targets are flagged: a release line that a publisher supersedes — a
``vX.Y[.Z]`` framework version, an ``OWASP ... YYYY`` release, a ``MASVS``/``CSF``/
``CIS Controls``/``SLSA``/``SBOM``/``PCI DSS`` release, or a ``NIST SP`` WITH a
revision suffix (``800-61r3``, ``Rev. 5``). A bare document identifier — ``RFC 9110``,
``ISO/IEC 9899``, ``FIPS 203``, ``NIST SP 800-53`` without a revision — names a
fixed document, not a current-version claim, and is not flagged.

#### `def discover_sources(root: Path) -> list[Path]`

Every canonical artifact subject to the freshness rule.

#### `def warnings(root: Path) -> list[str]`

Return a list of warning strings (empty = no unanchored pins).

#### `def validate(root: Path) -> list[str]`

Alias of :func:`warnings` for callers that expect ``validate``.

#### `def report(root: Path, include_references: bool=False) -> list[str]`

Read-only pin inventory (offline; no network).

Lists every moving release pin with its artifact and line and one of three
statuses: ``resolved`` (has a resolution declaration), ``unverified`` (the
standard's explicit "could not resolve" state, with a reason) or
``UNRESOLVED`` (a gate error). Never fails: it is the audit surface for "how
old is the corpus", not a gate.

### `engine/validators/hygiene.py`

Repository hygiene validators (D2 anti-tools, D12 paths/secrets).

Scans canonical source directories (never ``dist/`` derived content, never
``docs/`` evidence) for:

- absolute paths (``/home/``, ``/Users/``, ``/root/``, ``~``, ``C:\``/``C:/``)
- secret-shaped literals — use ``{env:VAR}``
- harness tool names inside canonical skill bodies (D2). ``references/``
  directories are exempt: they are the sanctioned home for tool mappings.

The tool-name denylist is the union of the built-in seed and every
``harnesses/*/harness.json`` ``tool_denylist`` (D2 derivation, F3).

#### `def validate(root: Path) -> list[str]`

Return a list of error strings; empty list means clean.

### `engine/validators/language.py`

Language policy check (english-only).

Validates that imported CONTENT is English across skills, workflows, agents and
their reference/example assets. Prose only: fenced code blocks, inline code and
markdown link targets are excluded, because samples, identifiers and anchor
slugs are not prose.

Returns WARNINGS (non-blocking during import) — it becomes a hard gate once the
corpus is translated.

#### `def validate(root: Path) -> list[str]`

Return a list of warning strings (empty = English-clean).

### `engine/validators/mcps.py`

Validate canonical MCP sources (D4/mcp-definition as amended at F3).

Source contract only; the generated dist/ coherence and orphan detection live
in ``engine.generators.mcp_configs.check`` (artifact layer), so an edited source
never deadlocks ``generate``.

#### `def validate(root: Path) -> list[str]`

Return a list of error strings; empty list means valid.

### `engine/validators/skills.py`

Validate canonical skill sources (D2/skill-authoring, corpus import contract).

Skills live under two roots sharing one flat name namespace:

- ``knowledge/skills/<category>[/<subcategory>]/<skill>/SKILL.md``
- ``methodology/workflows/<skill>/SKILL.md`` (process skills)

Errors: frontmatter parses; ``name`` is kebab-case and equals the directory;
``description`` present; globally unique slug; correct placement; no nested
SKILL.md; local markdown links resolve.

Warnings (non-blocking): non-English markers and oversized descriptions.

#### `def discover_skills(root: Path) -> list[Path]`

All ``SKILL.md`` under every skill root.

#### `def validate(root: Path) -> list[str]`

Return a list of error strings; empty list means valid.

#### `def warnings(root: Path) -> list[str]`

Non-blocking findings (language, description size).

The language check inspects PROSE only: fenced code blocks are skipped, so
illustrative samples that quote upstream docs (SQL comments, config values)
do not count as untranslated text. This mirrors the hygiene scan.

### `scripts/coacus.py`

Coacus thin CLI: generate | check | validate.

Deterministic build tooling for the framework (generated-artifacts, secrets-portability, generated-artifacts).

Validation is split in two layers:
- SOURCE errors (agents, skills, hygiene) gate ``generate`` — invalid canonical
  sources never produce committed artifacts.
- ARTIFACT errors (discovery manifests, provenance) validate the GENERATED
  outputs. They run AFTER writing in ``generate`` (a stale discovery
  fingerprint is exactly what regeneration fixes), and alongside sources in
  ``validate``.

#### `def source_errors(root: Path) -> list[str]`

Canonical-source contract violations (block generation).

#### `def artifact_errors(root: Path) -> list[str]`

Generated-artifact violations (checked after writing / on validate).

#### `def cmd_generate(_args: argparse.Namespace | None=None, root: Path | None=None) -> int`

Regenerate every derived artifact; return a non-zero exit on failure.

#### `def cmd_check(_args: argparse.Namespace | None=None, root: Path | None=None) -> int`

Fail if any generated artifact has drifted from its source.

#### `def cmd_toon(args: argparse.Namespace) -> int`

Validate a TOON handoff payload file; print errors and return the exit code.

#### `def cmd_completeness(_args: argparse.Namespace | None=None, root: Path | None=None) -> int`

Reconcile the corpus against its sources; fail if anything is unreconciled.

#### `def cmd_freshness(args: argparse.Namespace, root: Path | None=None) -> int`

Read-only, offline inventory of moving version pins (version-freshness).

#### `def cmd_validate(_args: argparse.Namespace | None=None, root: Path | None=None) -> int`

Run the schema and hygiene validators; fail on any error.

#### `def main(argv: list[str] | None=None) -> int`

Parse arguments and dispatch to the selected subcommand.

### `scripts/coacus_eval.py`

Behavior-eval runner for Coacus (testing).

Deterministic by default; live evaluation is opt-in.

    # static validation only (safe for CI, no LLM, no network)
    python3 scripts/coacus_eval.py validate

    # live run against a harness CLI installed locally
    python3 scripts/coacus_eval.py run [--scenario <id>] [--harness codex]
        [--judge-cmd "<command that reads the transcript on stdin>"]
        [--judge-agent]            # delegate judgment to a subagent via the harness

Live scenarios drive a real agent CLI, so they need the CLI + credentials and
run outside CI. Each harness declares its non-interactive invocation in
`harnesses/<h>/harness.json` (`live_cli`); a harness without one is reported as
`NO_RUNNER`. `--harness` overrides the scenario's target so one scenario can be
exercised against any locally installed live CLI. Deterministic checks
(`contains`/`not_contains`/`regex`) run on the captured transcript; the `rubric`
is passed to the judge.

The `--judge-cmd` receives JSON on stdin: {"scenario": {...}, "transcript": "..."}
and must print a verdict line (anything). `--judge-agent` runs the rubric through
the same harness as an orchestrated subagent (multi-agent-orchestrator pattern).

#### `def cmd_validate(root: Path) -> int`

Statically validate every eval scenario; return non-zero on any error.

#### `def cmd_run(root: Path, scenario_id: str | None, judge_cmd: str | None, judge_agent: bool, timeout: float, harness: str | None=None) -> int`

Run scenarios live and report check/judge results; fail if any did not pass.

#### `def main(argv: list[str] | None=None) -> int`

Parse arguments and dispatch to ``validate`` or ``run``.

### `scripts/coacus_governor.py`

Thin CLI over the concurrency governor (orchestration-governance).

Mirrors the reference command surface so harness adapters (the OpenCode gate
plugin) can call it directly:

    coacus_governor.py acquire <caller> [orchestrator-yes|no] [timeout-secs] [max-total]
    coacus_governor.py release <caller>
    coacus_governor.py fail    <caller>
    coacus_governor.py paused
    coacus_governor.py status  [max-total]
    coacus_governor.py reset

``acquire`` prints the token on success (exit 0) or nothing (exit 1) when the
cap stayed saturated past the timeout.

#### `def main(argv: list[str] | None=None) -> int`

Parse arguments and run the requested governor action.

### `scripts/coacus_import.py`

Coacus corpus importer (F6).

Imports the source corpora into the repository per `templates/import/import-manifest.json`,
recording provenance in `sources.lock.json` (provenance) and leaving content in
its original language with `transform: [..., "pending-translation"]` (english-only:
PT-BR imports are translated in tracked batches).

    python3 scripts/coacus_import.py plan   [--source skills|superpowers|agents]
    python3 scripts/coacus_import.py apply  [--source ...]

`plan` writes nothing and prints the actions; `apply` performs the copy and
updates `sources.lock.json`. The import is idempotent: re-running refreshes the
target and the provenance entry (dedup keyed on source repo/commit/path).

#### `def plan_skills(manifest: dict) -> list[dict]`

Plan the import (or exclusion) of every source skill into the taxonomy.

#### `def plan_superpowers(manifest: dict) -> list[dict]`

Plan the import of the Superpowers workflow collection, namespaced.

#### `def plan_agents(manifest: dict) -> list[dict]`

Plan agent imports, applying the manifest's merge and exclusion rules.

#### `def doc_title(doc) -> str`

Return the first ``# `` heading of a parsed document, or an empty string.

#### `def apply_actions(manifest: dict, actions: list[dict]) -> list[dict]`

Execute the planned actions and return the recorded provenance entries.

#### `def main(argv: list[str] | None=None) -> int`

Parse arguments and run the ``plan`` or ``apply`` import action.

### `scripts/coacus_install.py`

Coacus installer: activate rendered artifacts into a harness.

The repository GENERATES the per-harness artifacts (session-start-bootstrap); this script
INSTALLS them into a harness's own discovery locations. It is explicit and
idempotent — nothing runs at session start, and it never rewrites a harness
config file wholesale.

Mechanisms (verified against vendor docs, see docs/install.md):

- opencode    plugin -> <config_dir>/plugins/coacus.js  (`__COACUS_ROOT__`
              substituted) + governor gate, plus skill trees under
              <config_dir>/skills/ and agents under <config_dir>/agent/.
- claude-code skills   -> <config_dir>/skills/<skill>/  (documented personal path)
              agents   -> <config_dir>/agents/<name>.md
              hook     -> plugin staged at <config_dir>/plugins/coacus/ with the
              script at bootstrap/session-start.sh (matching hooks.json).
- antigravity plugin (manifest + rule + skills + agents) ->
              <config_dir>/config/plugins/coacus/; activation is by directory,
              so no registry edit is needed.
- codex       skills   -> ~/.agents/skills/<skill>/  (Codex scans .agents/skills,
              not ~/.codex/skills); agents -> <config_dir>/agents/<name>.toml;
              plus the SessionStart hook at <config_dir>/hooks.json.
- cursor      skills   -> ~/.agents/skills/<skill>/; agents ->
              <config_dir>/agents/<name>.md; plus the sessionStart hook at
              <config_dir>/hooks.json (snake_case `additional_context`).

Usage:
    python3 scripts/coacus_install.py <harness|all> [--dry-run] [--uninstall]
    python3 scripts/coacus_install.py opencode --config-dir /tmp/oc

A manifest (`coacus-install.json`) is written next to each target so re-runs
are idempotent and `--uninstall` removes exactly what was installed.

Partial installs keep the session-start skills budget small: a harness that
indexes every skill pays for every description. Filter with `--only` (top-level
category, applied to skills and agents), `--skills` (skill name glob) and/or
`--agents` (agent name glob); `--list` prints what is available.

    python3 scripts/coacus_install.py codex --only security,engineering
    python3 scripts/coacus_install.py codex --skills 'lang-python,framework-*'
    python3 scripts/coacus_install.py codex --agents 'qa-*,*-architect'
    python3 scripts/coacus_install.py codex --list

#### `def default_config_dir(harness: str, home: Path) -> Path`

Return the default config directory for ``harness`` under ``home``.

#### `def discover_skills(root: Path, only: list[str] | None=None, skills: list[str] | None=None) -> list[Path]`

All skill directories (the parent of a SKILL.md) in the repository.

``only`` keeps skills whose path under its root contains one of the given
category tokens (matched against every path segment, so both ``domains`` and
``academic`` select the academic skills). ``skills`` keeps skills whose
directory name matches one of the given fnmatch globs. Both filters are
OR-ed within their own list and AND-ed with each other; an empty filter is
no filter.

#### `def list_skills(root: Path) -> dict[str, object]`

Inventory for `--list`: categories and skill names, no harness needed.

#### `def discover_agents(root: Path, only: list[str] | None=None, agents: list[str] | None=None) -> list[Path]`

All canonical agent sources: knowledge/agents/<category>/<name>/.

``only`` keeps agents whose path under ``knowledge/agents`` contains one of
the given category tokens (matched against every path segment). ``agents``
keeps agents whose directory name matches one of the given fnmatch globs.
Both filters are OR-ed within their own list and AND-ed with each other; an
empty filter is no filter. ``--skills`` never narrows agents.

#### `def plan(harness: str, root: Path, config_dir: Path, only: list[str] | None=None, skills: list[str] | None=None, agents: list[str] | None=None) -> list[tuple[Path, FileContent]]`

Compute the files to install for ``harness`` under the given filters.

Returns ``(target, content)`` pairs; nothing is written. ``only`` selects by
category across skills and agents; ``skills``/``agents`` narrow each tree by
name glob. Shared by ``install``, ``verify`` and ``uninstall``.

#### `def install(harness: str, root: Path, config_dir: Path, dry_run: bool, only: list[str] | None=None, skills: list[str] | None=None, agents: list[str] | None=None) -> dict[str, object]`

Install a harness and write its manifest; report files written.

With ``dry_run``, returns the plan without touching disk. Every target is
containment-checked first, so an install never writes outside the allowed
roots (see ``_assert_contained``).

#### `def verify(harness: str, root: Path, config_dir: Path) -> dict[str, object]`

Compare an installed harness against the repository, read-only.

Reports canonical component counts, the install root, and any file that is
missing or has drifted from the repository. Exits non-zero (via the caller)
when the harness is not installed or drift is found. The counts come from
the plan the installer would write — never inferred — so a report can quote
this output verbatim.

#### `def uninstall(harness: str, root: Path, config_dir: Path, dry_run: bool=False) -> dict[str, object]`

Remove the recorded install, staying inside the allowed roots.

Deletion is gated on containment under ``config_dir`` or the shared
``<config_dir>/../.agents`` tree — not on membership in a freshly re-derived
plan, which would orphan a file whose repository source was deleted after
install. Files still claimed by another harness's manifest (the shared
``.agents/skills`` tree) are skipped, so uninstalling Codex does not break
Cursor. A path recorded by a doctored manifest but outside the allowed roots
is skipped, so the manifest cannot delete arbitrary files.

#### `def main(argv: list[str] | None=None, root: Path | None=None) -> int`

Parse arguments and run install, uninstall, verify or list.

### `scripts/coacus_vertical.py`

Architecture-SI vertical CLI: document ingestion and analysis (F6c).

Unifies the former `pdf2md` / `doc2md` / `doc-analyze` entrypoints over one
dispatcher (knowledge-ingestion):

    coacus_vertical.py ingest  <file|--dir DIR> [output] [--toc-only] [--split-chapters]
    coacus_vertical.py analyze <file|--dir DIR> [--json]
    coacus_vertical.py formats

#### `def main(argv: list[str] | None=None) -> int`

Parse arguments and dispatch to the ``ingest`` or ``analyze`` subcommand.

### `verticals/architecture_si/pipelines/analyze/analyzer.py`

Analyze Markdown documents: outline, metrics, diagrams, security keywords.

Ported from the `agente-arquitetura-si` analyzer (F6c), translated and placed
under the vertical pipeline. Dual output: human report or stable JSON, ready to
be exposed as an MCP tool.

#### `class Analysis`

Structured result of analysing one Markdown document.


#### `def analyze_markdown(file_path: str) -> Analysis`

Analyse a Markdown file and return its metrics, outline and detected terms.

#### `def human_report(analysis: Analysis) -> str`

Render an analysis as a human-readable text report.

#### `def analyze_dir(directory: str, as_json: bool) -> str`

Analyse every ``*.md`` file in ``directory``, as JSON or human reports.

### `verticals/architecture_si/pipelines/ingest/handlers/_common.py`

Shared formatting helpers for ingest handlers.

#### `def format_markdown_table(rows: List[List[str]]) -> str`

Format a 2D list of strings as a GitHub-flavored Markdown table.

#### `def write_markdown(content: str, output_path: str | None, source: str) -> str`

Write ``content`` to ``output_path``.

Default output keeps the original extension to avoid stem collisions in a
mixed directory (e.g. ``data.csv`` -> ``data.csv.md``), so ``a.txt`` and
``a.csv`` never overwrite each other.

### `verticals/architecture_si/pipelines/ingest/handlers/csv_table.py`

CSV / TSV to a Markdown table.

#### `def handle_csv(input_path: str, output_path: str | None=None) -> str`

Convert a CSV/TSV file to a Markdown table and return the written path.

### `verticals/architecture_si/pipelines/ingest/handlers/docx.py`

DOCX to Markdown (headings, paragraphs, lists, tables).

#### `def convert_docx_to_md(docx_path: str) -> str`

Convert a DOCX document's headings, paragraphs, lists and tables to Markdown.

Legacy ``.doc`` (OLE) raises ``RuntimeError`` (unsupported by python-docx).

#### `def handle_docx(input_path: str, output_path: str | None=None) -> str`

Convert a DOCX file to Markdown and return the written path.

### `verticals/architecture_si/pipelines/ingest/handlers/html.py`

HTML to Markdown, with a stdlib HTMLParser fallback when BeautifulSoup is absent.

#### `def convert_html_to_md(html_path: str) -> str`

Convert an HTML file to Markdown, preferring BeautifulSoup when present.

#### `def handle_html(input_path: str, output_path: str | None=None) -> str`

Convert an HTML file to Markdown and return the written path.

### `verticals/architecture_si/pipelines/ingest/handlers/pdf.py`

PDF to structured Markdown, with PyMuPDF → pypdf fallback (knowledge-ingestion).

Preserves the upstream behavior: TOC/bookmark map, per-page anchors, list and
code heuristics, and the ``--toc-only`` / ``--split-chapters`` options. The
dependency is auto-detected so the framework runs with either library.

#### `def clean_text(text: str) -> str`

Fix hyphenation across line breaks and normalize whitespace.

#### `def convert_pdf_with_fitz(pdf_path: str, output_path: Optional[str]=None, split_chapters: bool=False, toc_only: bool=False) -> str`

Convert a PDF to Markdown using PyMuPDF (per-page anchors, TOC map).

``toc_only`` emits just the outline; ``split_chapters`` is accepted for
interface parity with the upstream converter.

#### `def convert_pdf_with_pypdf(pdf_path: str, output_path: Optional[str]=None) -> str`

Convert a PDF to Markdown using pypdf (plain per-page text extraction).

#### `def convert_pdf_to_markdown(pdf_path: str, output_path: Optional[str]=None, **kwargs: Any) -> str`

Convert a PDF to Markdown, selecting PyMuPDF or pypdf by availability.

#### `def handle_pdf(input_path: str, output_path: str | None=None) -> str`

Convert a PDF to Markdown and return the written path.

### `verticals/architecture_si/pipelines/ingest/handlers/pptx.py`

PPTX to Markdown slides (text frames and tables).

#### `def convert_pptx_to_md(pptx_path: str) -> str`

Convert a PPTX presentation's slides to Markdown.

Legacy ``.ppt`` (OLE) raises ``RuntimeError`` (unsupported by python-pptx).

#### `def handle_pptx(input_path: str, output_path: str | None=None) -> str`

Convert a PPTX file to Markdown and return the written path.

### `verticals/architecture_si/pipelines/ingest/handlers/structured.py`

JSON / YAML to a fenced Markdown code block.

#### `def handle_structured(input_path: str, output_path: str | None=None) -> str`

Convert a JSON/YAML file to a fenced Markdown block; return the path.

### `verticals/architecture_si/pipelines/ingest/handlers/text.py`

Text-like formats: TXT, RTF, LOG, and the raw fallback.

#### `def convert_txt_to_md(txt_path: str) -> str`

Read a text-like file and return it as Markdown with an H1 title.

#### `def handle_text(input_path: str, output_path: str | None=None) -> str`

Convert a text-like file to Markdown and return the written path.
