# Installing Coacus into a harness

This tutorial takes you from a fresh checkout to a harness that loads Coacus and
injects its bootstrap at session start. Work through the harness that matches your
editor; each section is self-contained.

The repository **generates** the per-harness artifacts and commits them
([session-start-bootstrap](standards/session-start-bootstrap.md)). Making a harness load
them is a separate, explicit step: each harness discovers plugins and skills from
its own locations, and Coacus never rewrites a harness config file wholesale. The
installer writes only the files a vendor mechanism actually reads — a plugin
directory, a hook manifest — and nothing else.

## Evidence classes

Harness behavior is a moving target, so every vendor claim below carries its
evidence class. Do not treat them as equally authoritative.

| Class | Meaning |
|---|---|
| **[documented]** | Stated in the vendor's own documentation, cited when it exists. |
| **[verified locally]** | Confirmed by running the command in this repository. |
| **[unverified]** | Observed empirically or inferred; not confirmed by vendor docs. Treat as likely to change. |

## Prerequisites

- Python 3.14 (the CI target). The core tooling uses the standard library only.
- The harness CLI you intend to install into, unless you only want a dry run.
- Run every command from the repository root.

### Recommended MCP dependency

The [`context7`](https://context7.com/) MCP server is the framework's recommended
external dependency. It is hosted, keyless and declared once under
[`knowledge/mcps/context7/`](../knowledge/mcps/context7/MCP.md); the generator
derives `dist/mcp.json` and `dist/mcp_config.json` from it. Registering it with a
harness is optional — the scripts, validators and generated artifacts all work
without it — but the corpus skills assume current library/framework docs when a
task needs them, which is what context7 provides.

## Step 1 — render the artifacts

Do this once, before any install. The installer copies rendered files; it does
not generate them.

```bash
python3 scripts/coacus.py generate
```

You now have `harnesses/<h>/bootstrap/`, the agent `dist/` trees, `.agents/`,
`catalog/` and `docs/reference/python-api.md`.

## Step 2 — install

Two routes exist:

- **Script** — `python3 scripts/coacus_install.py <harness|all>`. Idempotent;
  `--dry-run` previews targets, `--uninstall` removes exactly what was installed,
  `--config-dir` installs into a non-default location for testing.
- **Manual** — perform the same file copies by hand, using the per-harness
  sections below and the tables in [Reference](#reference).

The script writes a `coacus-install.json` manifest beside each target so re-runs
and uninstalls are exact.

```bash
python3 scripts/coacus_install.py opencode      # one harness
python3 scripts/coacus_install.py all           # opencode, claude-code, antigravity, codex, cursor
python3 scripts/coacus_install.py opencode --dry-run
python3 scripts/coacus_install.py opencode --uninstall
```

Skill sources installed everywhere are `methodology/workflows/**` and
`knowledge/skills/**`, flattened into one namespace. Each skill installs as
`<skill>/SKILL.md` plus its companions (`references/`, `examples/`, `scripts/`).

### Partial installs

A harness that indexes every skill pays, at session start, for every skill
description it must load — Codex, for example, shortens descriptions when the
corpus overflows its skills context budget. Install only what a session needs:

```bash
python3 scripts/coacus_install.py codex --only security,engineering
python3 scripts/coacus_install.py codex --skills 'lang-*,framework-*'
python3 scripts/coacus_install.py codex --only languages --skills 'lang-python,lang-rust'
python3 scripts/coacus_install.py --list     # categories and skill names, then exit
```

- `--only` matches the top-level category (`security`, `domains`, `languages`, …)
  or any nested segment (`academic`, `appsec`, `grc`, …); the workflows
  collection is selected with `workflows`.
- `--skills` matches skill directory names with fnmatch globs.
- Tokens are comma-separated; the two filters are AND-ed, and the selected files
  are recorded in the manifest, so `--uninstall` stays exact.

## opencode

**Goal:** the OpenCode session starts with the Coacus entry skill already loaded.

**How it works.** Coacus ships an OpenCode **plugin** — an in-process module the
harness loads. The plugin does two jobs: it registers the two skill roots, and it
injects the bootstrap into the first user message. The bootstrap carries an
anti-reinjection guard so a compact or replay does not duplicate it
([session-start-bootstrap](standards/session-start-bootstrap.md)).

**Vendor facts**

- The config key is `plugin`, singular — not `plugins`. **[documented]**
- Plugins load from `~/.config/opencode/plugins/` and `.opencode/plugins/`.
  **[documented]**
- Skill discovery includes `~/.config/opencode/skills/`, `.opencode/skills/`,
  `~/.claude/skills/` and `~/.agents/skills/`. **[documented]**
- `skills.paths` exists in the official config schema; the plugin sets it through
  the `config` hook. The `experimental.chat.messages.transform` hook is the
  injection point. Both hooks are documented. **[documented]**
- The Coacus plugin loads and injects the bootstrap. **[verified locally]**
- Whether OpenCode mirrors skills under an `OPENCODE_CONFIG_DIR` override is not
  stated in the docs; the installer relies on it for isolated testing.
  **[unverified]**

**Install**

```bash
python3 scripts/coacus_install.py opencode
```

The script copies both plugins into `~/.config/opencode/plugins/` with
`__COACUS_ROOT__` substituted for this repository's path, and mirrors the skills
under `~/.config/opencode/skills/`. The second plugin, `coacus-governor.js`, is
the governor gate: it intercepts subagent spawns, enforces the concurrency cap,
and parks a caller as PAUSED when it sees a rate limit. Knobs:
`ORCH_MAX_CONCURRENT` (default 5), `GOVERNOR_STATE_DIR`, `GOVERNOR_LEASE_SECONDS`.
Inspect the ledger with `python3 scripts/coacus_governor.py status`.

**Manual equivalent.** Copy `harnesses/opencode/bootstrap/coacus.js` and
`governor-gate.js` to `~/.config/opencode/plugins/`, replacing
`__COACUS_ROOT__` with this repository's absolute path. Alternatively, skip the
skill registration and add the folders to `opencode.json` yourself:

```jsonc
{ "skills": { "paths": ["<repo>/methodology/workflows", "<repo>/knowledge/skills"] } }
```

**Verify** (isolated, no global changes):

```bash
mkdir -p /tmp/oc/plugins
sed "s|__COACUS_ROOT__|$PWD|" harnesses/opencode/bootstrap/coacus.js > /tmp/oc/plugins/coacus.js
OPENCODE_CONFIG_DIR=/tmp/oc opencode run \
  "In one short sentence, name one 'red flag' thought from the guidance already in your context."
```

A session with the bootstrap answers with a string from the entry skill
(`"This is just a small change."`). A session without it does not.

## claude-code

**Goal:** a `SessionStart` hook injects the bootstrap through the one native key
Claude Code reads.

**How it works.** Claude Code has no in-process plugin API like OpenCode. Instead
the harness exposes a `SessionStart` hook that emits JSON. Coacus ships a shell
script that prints exactly one native field —
`hookSpecificOutput.additionalContext` — and never the forbidden alias
`additional_context`; Claude Code reads both without deduplication, so emitting
both injects the body twice ([session-start-bootstrap](standards/session-start-bootstrap.md)).

**Vendor facts**

- Personal skills live at `~/.claude/skills/<name>/SKILL.md`. **[documented]**
- The supported plugin route is a plugin directory with
  `.claude-plugin/plugin.json` plus a marketplace file
  `.claude-plugin/marketplace.json`, installed with `/plugin marketplace add`
  and `/plugin install`. The `CLAUDE_PLUGIN_ROOT` variable is available inside
  hook commands. **[documented]**
- The `SessionStart` hook and `hookSpecificOutput.additionalContext` are the
  documented injection mechanism. **[documented]**
- The installer's staging path `~/.claude/plugins/coacus/` is **not** an
  official plugin location. It is a manual helper: the script places the script
  and hook manifest where the hook's relative `bootstrap/session-start.sh` path
  resolves, so you can test the hook without publishing a marketplace.
  **[unverified]**

**Install**

```bash
python3 scripts/coacus_install.py claude-code
```

This mirrors the skills to `~/.claude/skills/<skill>/` and stages the hook plugin
at `~/.claude/plugins/coacus/` with `.claude-plugin/plugin.json`,
`hooks/hooks.json` and `bootstrap/session-start.sh`. Treat that staging as a
local helper. For a durable install across machines, publish the repository as a
Claude Code plugin and install it through the marketplace path, which is the
supported route. **[documented]**

**Verify** (structure only; no live Claude Code binary was available here):

```bash
python3 -c "import json; json.load(open('harnesses/claude-code/bootstrap/hooks.json'))"
bash -n harnesses/claude-code/bootstrap/session-start.sh
bash harnesses/claude-code/bootstrap/session-start.sh | python3 -c "import json,sys; d=json.load(sys.stdin); print(sorted(d['hookSpecificOutput']))"
```

The last command must print `['additionalContext', 'hookEventName']` — one
context key, not two.

## antigravity

**Goal:** Antigravity loads Coacus as a plugin and applies its rule at session
start.

**How it works.** Antigravity uses an **instructions-file** bootstrap: the adapter
renders a rule file, `coacus-rule.md`, with frontmatter `activation: always_on`,
plus the `plugin.json` manifest that packages it. The rule directory is the
activation unit; there is no shell hook and no in-process module.

**Vendor facts**

- `agy plugin install <dir>` installs a plugin; `list`, `enable`, `disable` and
  `uninstall` manage it. **[documented]**
- The `plugin.json` schema is strict: `additionalProperties: false`, so it
  carries only `name` and `description`. There is **no** `contextFileName`
  field. **[documented]**
- Plugin activation is by directory: `.agents/plugins/<name>/` in a workspace,
  `~/.gemini/config/plugins/<name>/` globally. The CLI also supports
  `agy plugin install /path/to/plugin`, which stages to
  `~/.gemini/antigravity-cli/plugins/<name>/`. **[documented]**
- Plugin components are `skills/`, `agents/`, `rules/`, `mcp_config.json` and
  `hooks.json`. Rules are capped at 12,000 characters. **[documented]**
- There is **no** `~/.gemini/config/plugins.json` registry. Earlier Coacus
  revisions claimed one; that claim was wrong and has been removed. Activation
  is by directory placement alone. **[documented]**
- `agy plugin validate` returned `[ok]` on the staged Coacus plugin.
  **[verified locally]**
- Hooks (`hooks.json`) support `PreToolUse`, `PostToolUse`, `PreInvocation`,
  `PostInvocation` and `Stop`. `PreInvocation` can return `injectSteps` with an
  `ephemeralMessage`, which is a candidate for bootstrap injection on a future
  revision; the current adapter does not use it. **[documented]**

**Install**

```bash
python3 scripts/coacus_install.py antigravity
```

The script stages the plugin at `~/.gemini/config/plugins/coacus/` with
`plugin.json`, `coacus-rule.md` and the skills. It does not edit any registry —
none exists — and it does not invoke `agy plugin install` itself; that command
expects a plugin or marketplace target and is left to the operator.

**Verify**

```bash
agy plugin validate ~/.gemini/config/plugins/coacus   # expect: [ok]
```

If `agy plugin install` is your preferred route, point it at the staged
directory.

## codex

**Goal:** a `SessionStart` hook injects the bootstrap, and Codex discovers the
Coacus skills natively.

**How it works.** Codex supports both halves of the adapter. It scans
`.agents/skills` for skills, and its hooks framework runs a `SessionStart` hook
that emits `hookSpecificOutput.additionalContext` — the same native key Claude
Code uses. The adapter renders `harnesses/codex/bootstrap/session-start.sh` and
the matching `hooks.json`.

**Vendor facts**

- Codex loads skills from `$CWD/.agents/skills`, `$REPO_ROOT/.agents/skills` and
  `$HOME/.agents/skills` — **not** `~/.codex/skills/`. **[documented]**
- Codex has a full hooks framework: a `SessionStart` hook emitting
  `hookSpecificOutput.additionalContext`, configured through
  `~/.codex/hooks.json`, `<repo>/.codex/hooks.json`, inline `[hooks]` in
  `config.toml`, or a plugin-bundled `hooks/hooks.json`. **[documented]**
- The Coacus skill install and hook install both complete against a temporary
  config directory. **[verified locally]**
- `[[skills.config]]` enables skills explicitly. **[documented]**

Codex is supported via its SessionStart hook. There is no known gap.

**Install**

```bash
python3 scripts/coacus_install.py codex
```

The script installs skills to `$HOME/.agents/skills/` — the root Codex actually
scans, beside `~/.codex/`, not inside it — and the hook to `~/.codex/hooks.json`
with `__COACUS_ROOT__` substituted for this repository's path. The bootstrap
script is staged at `~/.codex/coacus/session-start.sh`.

**Verify**

```bash
python3 -c "import json; json.load(open('harnesses/codex/bootstrap/hooks.json'))"
bash -n harnesses/codex/bootstrap/session-start.sh
bash harnesses/codex/bootstrap/session-start.sh | python3 -c "import json,sys; d=json.load(sys.stdin); print(sorted(d['hookSpecificOutput']))"
```

The last command must print `['additionalContext', 'hookEventName']`. No flat
`additional_context` key may appear.

## cursor

**Goal:** a `sessionStart` hook injects the bootstrap, and Cursor discovers the
Coacus skills from its scan roots.

**How it works.** Cursor's hook framework runs `sessionStart` at the top of a
session. The handler is fire-and-forget and prints the snake_case top-level key
`additional_context` — **not** `additionalContext`, and **not** a nested
`hookSpecificOutput`. The adapter renders
`harnesses/cursor/bootstrap/session-start.sh` and the matching `hooks.json`.

**Vendor facts**

- Hooks live at `<project>/.cursor/hooks.json` (project) or
  `~/.cursor/hooks.json` (user) — **not** `hooks-cursor.json`. **[documented]**
- The schema is version 1: top-level `version`, an event map, and each handler a
  `{ "command": ... }` object with no matcher. **[documented]**
- `sessionStart` is fire-and-forget and outputs the snake_case key
  `additional_context`. **[documented]**
- Plugins use `.cursor-plugin/plugin.json`, or a root `plugin.json` under the
  agent-plugins standard. **[documented]**
- Skills load from `.cursor/skills/`, `~/.cursor/skills/`, `.agents/skills/` and
  `~/.agents/skills/`, plus the Claude and Codex compatibility locations.
  **[documented]**
- The Coacus hook install completes and emits `additional_context` against a
  temporary config directory. **[verified locally]**

The legacy `hooks-cursor.json` filename is gone from the adapter. The render uses
`.cursor/hooks.json` and emits `additional_context`.

**Install**

```bash
python3 scripts/coacus_install.py cursor
```

The script installs skills to `$HOME/.agents/skills/` — a Cursor scan root — and
the hook to `~/.cursor/hooks.json` with `__COACUS_ROOT__` substituted. The
bootstrap script is staged at `~/.cursor/coacus/session-start.sh`. For a project
install, copy the same two artifacts into `<project>/.cursor/` by hand.

**Verify**

```bash
python3 -c "import json; json.load(open('harnesses/cursor/bootstrap/hooks.json'))"
bash -n harnesses/cursor/bootstrap/session-start.sh
bash harnesses/cursor/bootstrap/session-start.sh | python3 -c "import json,sys; d=json.load(sys.stdin); print('additional_context' in d)"
```

The last command must print `True`. The script must not emit
`additionalContext` or `hookSpecificOutput`.

## Reference

### Install targets

| Harness | Shape | Bootstrap mechanism | Install target | Evidence |
|---|---|---|---|---|
| **opencode** | B (in-process) | `config` + `experimental.chat.messages.transform` hooks | plugin at `~/.config/opencode/plugins/{coacus.js,coacus-governor.js}` + skills at `~/.config/opencode/skills/` | plugin load **[verified locally]**; mirror path **[unverified]** |
| **claude-code** | A (shell hook) | `SessionStart` → `hookSpecificOutput.additionalContext` | skills at `~/.claude/skills/<skill>/`; helper plugin at `~/.claude/plugins/coacus/` | vendor plugin route **[documented]**; staging path **[unverified]** |
| **antigravity** | C (rule file) | `coacus-rule.md` with `activation: always_on`, packaged by `plugin.json` | plugin staged at `~/.gemini/config/plugins/coacus/`; activation by directory | rule + strict schema **[documented]**; `agy plugin validate` **[verified locally]** |
| **codex** | A (shell hook) | `SessionStart` → `hookSpecificOutput.additionalContext` | skills at `~/.agents/skills/`; hook at `~/.codex/hooks.json` | skill roots + hook framework **[documented]**; install **[verified locally]** |
| **cursor** | A (shell hook) | `sessionStart` → top-level `additional_context` | skills at `~/.agents/skills/`; hook at `~/.cursor/hooks.json` | hook schema + key **[documented]**; install **[verified locally]** |

### Verifying

| Check | Command |
|---|---|
| Structure and drift | `python3 scripts/coacus.py check` |
| Source and artifact contracts | `python3 scripts/coacus.py validate` |
| Antigravity plugin | `agy plugin validate <staged-dir>` |
| Claude Code hook parses | `python3 -c "import json; json.load(open('harnesses/claude-code/bootstrap/hooks.json'))"` |
| Claude Code script syntax | `bash -n harnesses/claude-code/bootstrap/session-start.sh` |
| Codex hook parses | `python3 -c "import json; json.load(open('harnesses/codex/bootstrap/hooks.json'))"` |
| Codex script syntax | `bash -n harnesses/codex/bootstrap/session-start.sh` |
| Cursor hook parses | `python3 -c "import json; json.load(open('harnesses/cursor/bootstrap/hooks.json'))"` |
| Cursor emits `additional_context` | `bash harnesses/cursor/bootstrap/session-start.sh \| python3 -c "import json,sys; print('additional_context' in json.load(sys.stdin))"` |

The live test for any harness is behavioral: a fresh session with the bootstrap
must produce a string that exists only in `using-coacus` — the red-flag thought
`"This is just a small change."` A session without the bootstrap must not produce
it. Live acceptance has been run on OpenCode; Claude Code, Codex and Cursor are
structure-verified only, because their binaries were not available locally.
