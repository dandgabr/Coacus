# Lifecycle Guardrails

**Status:** normative
**Scope:** the portable lifecycle-hook and guardrail layer rendered per harness.

## Rule

A guardrail is authored once and rendered natively per harness. The model is
**PAER** — Policy over Action, Event binding, Rendering effect:

- **Action** — the portable subject: `verb` (`exec`, `read`, `write`, `network`,
  `spawn`, `mcp`, `delegate`) plus a normalized `resource`. Defined in
  `methodology/lifecycle/actions.schema.json`.
  An `mcp` resource is the tool name as the harness sends it, so the pattern is per
  harness: `mcp__server__tool` on Claude Code and Codex, `server_tool` on OpenCode and
  `MCP:tool` on Cursor (no server name). Write `*server*` to span them. A tool the guard
  cannot classify has no verb, so no rule sees it: remove it from the harness configuration.
  On OpenCode the code tool `execute` is an `exec` action with no command and also an
  `mcp` action named `execute`; code run through it can reach the network without a hook
  seeing it, so deny `execute` itself when that matters.
- **Policy** — authored once in `methodology/lifecycle/policies/*.policy.json`.
- **Event** — when the policy is consulted; the canonical taxonomy lives in
  `methodology/lifecycle/events.json`. An event has a `class`:
  `gate` (may `allow`/`deny`/`ask`), `observe` (advisory only, never denies), or
  `lifecycle` (injection or loop trigger).
- **Rendering effect** — the harness-native encoding, emitted by the guardrail
  generator.

### Capability data

`harnesses/<h>/harness.json` carries a `lifecycle` block with per-event
capabilities (`support`, `can_block`, `can_ask`, `effect`, `evidence`, `resolved`,
`source`) and declared `gaps`. A harness without a `lifecycle` block is a
**closed** capability: nothing renders and nothing installs. The capability
matrix (`docs/reference/lifecycle-matrix.md`) is GENERATED from this data and
carries each cell's evidence class; a bare boolean is forbidden.

### Decisions and failure

- The canonical decision set is `allow | deny | ask`. `ask` is valid only where
  the harness exposes a human channel (`can_ask`); elsewhere it degrades by the
  policy's `on_ask_unavailable`. Headless and subagent runs MUST
  degrade, and the hook payload carries no signal that identifies them, so the
  runtime renders `ask` only on an explicit opt-in (`COACUS_GUARD_ASK=1`) and only
  when `harness.json` declares `can_ask` and `can_block` for the event.
  `COACUS_GUARD_NO_ASK` and a `CI` variable set to a truthy value (anything but
  empty, `0`, `false`, `no` or `off`) always force the degradation, only `tool.pre`
  can ask, any doubt counts as no channel, and a missing or invalid `on_ask_unavailable` fails
  closed to `deny`. OpenCode asks only through the V2 permission `evaluate` hook
  (its cell has `ask_channel: evaluate`), only with the extra opt-in
  `COACUS_GUARD_ASK_EXPERIMENTAL=1`, and that hook can only tighten an effect.
  An `ask` is not a barrier when the person runs OpenCode with `--auto`: the harness
  then approves it without a prompt, and the person who chose that mode accepts it.
  Only a `deny` holds there, so a rule that must always hold is written as `deny`.
  When several `ask` policies match one action, the strictest
  `on_ask_unavailable` among them is used, whatever the file order. Rendering `ask` where it was previously degraded relaxes the
  outcome, which is why it needs the opt-in
  ([ADR 0010](../decisions/0010-ask-channel-gating.md)).
- Decisions compose monotonically: `deny > ask > allow`. Adding a hook can only
  make the outcome stricter.
- Failure domains are split: `on_decision_failure` (the evaluator ran but could
  not decide) defaults to `deny`; `on_mechanism_failure` (the guardrail process
  itself failed) defaults to `allow` plus an advisory. A broken hook MUST NOT
  deny every call.
- Where a harness requires an explicit decision in order to permit (Antigravity
  reads a decision-less `PreToolUse` result as a deny), the `allow` render is the
  harness-native permit and the fail-open path emits it too — `{}` is only a
  no-opinion permit on harnesses whose contract does not make `decision`
  mandatory.

### Installation

- Ownership is per entry id, never a repository path. `--uninstall` removes every
  Coacus id; `--verify` proves presence and, where possible, position.
- The installer REFUSES to install a `deny` policy whose bound event is not
  `can_block` on that harness; `--allow-advisory` records the downgrade.
- A `deny` whose event has no native home is refused, not silently dropped.

### Advisory content rules

Beyond action policies, the guardrail layer evaluates ADVISORY CONTENT RULES:
`field x operator x pattern`, all conditions AND-combined, authored under
`methodology/lifecycle/patterns/*.json`. A match produces an advisory, never a
deny — an observe binding can only surface. Rule ids are FROZEN and append-only:
`engine/guardrail/rules.py` records the required ids and
`engine/validators/guardrails.py` fails the build when one disappears. A rule with
no condition can never match; a non-compiling pattern does not match and is a lint
error. Every rule carries its mitigation, not just the alert.

### Defense ladder and suppression

Layer defenses: a deterministic pattern, then a single-turn review, then a
cross-file review; each layer is independently switchable. A deferred review may
run in the background and wake the agent with findings rather than block the turn.
Provide an inline-suppression convention (a reviewed / safe-because comment) so a
false positive is silenced without disabling the layer. When layered rule files
concatenate under a size cap, drop the tail first so user-wide rules survive.

### Machine-local policies and command matching

Some policies depend on the machine, not on the project. They are GENERATED at
install time into the user policy directory (`engine/guardrail/evaluate.py:
user_policy_dir`) and loaded by the runtime guard next to the repository policies;
the repository never carries them (no machine-specific paths, D2 opt-in). The
browser policy is the reference case: the installer detects the browsers present
(`methodology/lifecycle/browsers.json`), the user selects a primary and an
optional fallback, and `engine/guardrail/browsers.py` renders a `deny` policy for
every other known browser (launch, and read/write of its profile).

An `exec` policy may declare `"match": "command"` and a list of `resource`
patterns. The patterns are compared with the executable names the command would
run (`engine/guardrail/evaluate.py:command_candidates`: wrappers, `sh -c`,
`$(...)`, symlinks resolved), never with arguments, so a mention of a name inside
`grep`, `git commit -m` or a path does not fire. Matching is best-effort (shell is
Turing complete); it narrows accidents, it is not a sandbox.

## Protecting the guard from the session

The guard runs in the session it governs, so an agent can switch it off by editing a
file instead of dodging a rule. `methodology/lifecycle/policies/self-protection.policy.json`
denies the write tools on the guard script, the evaluator, the policy directories and each
harness's hook files. It is disabled by default (ADR 0006); the installer offers it with
`--self-protection on|off|prompt` (an interactive install asks, and No is the default), see
[ADR 0015](../decisions/0015-guard-self-protection.md). It does not cover a write made
through the shell, so it is a tripwire, not a sandbox: for a real barrier use isolation
outside the session (a sandbox, read-only files, the harness's managed settings).

**To release a legitimate edit**, the person (never the agent) either makes the edit in their
own terminal, or sets `"enabled": false` in the installed `self-protection.policy.json`,
edits, and sets it back to `true`. Every denial message says this.

## Prompts

A `prompt` rule bound to `prompt.submit` blocks a user prompt whose text matches its
pattern (case-insensitive). Today only Claude Code has the hook, installed while an
enabled policy binds the event, and a block shows its reason to the user. A prompt is never
asked about, and a prompt over 100,000 characters matches every prompt rule. Enabling or
disabling a prompt policy takes effect at the next install. See ADR 0016.

## Which tools a rule can see

The guard classifies a call by the tool's name and reads its arguments from the
harness's documented payload (Antigravity nests them under `toolCall`). A tool with
no verb, such as a todo list, is never offered to a policy. A search tool that scans a
directory (`Grep`, `Glob`, `grep_search`, `find_by_name`) is checked against the
directory and, best effort, against each glob it was given joined under that directory,
never against the files it finds. A rule that names one file by a pattern such as
`*/.env` can still miss a search that reads it, for example through a bracket or brace
glob, so a file-level read rule is not a barrier against search tools. A test reads
each harness's `tool_mapping` and `tool_denylist` and fails when a documented tool has
no verb and is not on its short list of exemptions.

## Rationale

Event names are the least portable axis; the policy is the most portable. Inverting
the conventional event-centric model puts the authored judgment in the shared
layer and leaves only the binding per harness. The capability data keeps the
framework honest: what a harness cannot enforce is declared, generated into the
matrix with its evidence class, and refused at install rather than degraded in
silence.

## Enforcement

- `engine/validators/harnesses.py` validates every `lifecycle` block against the
  canonical taxonomy and the registered plugin kinds.
- `engine/generators/guardrails.py` renders the native artifacts;
  `engine/generators/lifecycle.py` renders the matrix; `scripts/coacus.py check`
  fails on drift.
- `scripts/coacus_guard.py` evaluates policies at runtime; the generated hooks
  call it and never re-implement a decision.
- `engine/guardrail/rules.py` evaluates the advisory content catalogue;
  `engine/validators/guardrails.py` (via `validate`) checks it is well-formed and
  append-only.
- `tests/test_lifecycle.py` covers the render contract, the matrix and the
  validator; `tests/test_guardrail_scripts.py` executes the rendered hook.
