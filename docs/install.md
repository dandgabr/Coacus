# Installing Coacus into a harness

This tutorial takes you from a fresh checkout to a harness that loads Coacus and
injects its bootstrap at session start. Work through the harness that matches your
editor; each section is self-contained.

The repository **generates** the per-harness artifacts and commits them
([ADR-0016](adr/ADR-0016-bootstrap-render-contract.md)). Making a harness load
them is a separate, explicit step: each harness discovers plugins and skills from
its own locations, and Coacus never rewrites a harness config file wholesale.

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

## Step 1 — render the artifacts

Do this once, before any install. The installer copies rendered files; it does
not generate them.

```bash
python3 scripts/coacus.py generate
```

You now have `harnesses/<h>/bootstrap/`, the agent `dist/` trees, `.agents/`,
`catalog/` and `docs/reference/python-api.md`. The installer never touches the
harness's own config except where a vendor mechanism explicitly requires a
registry entry (Antigravity only).

## Step 2 — install

Two routes exist:

- **Script** — `python3 scripts/coacus_install.py <harness|all>`. Idempotent;
  `--dry-run` previews targets, `--uninstall` removes exactly what was installed,
  `--config-dir` installs into a non-default location for testing.
- **Manual** — perform the same file copies by hand, using the per-harness
  sections below and the tables in [Reference](#reference).

The script writes a `coacus-install.json` manifest beside each target so re-runs
and uninstalls are exact. It also backs up an Antigravity `plugins.json` before
editing it.

```bash
python3 scripts/coacus_install.py opencode      # one harness
python3 scripts/coacus_install.py all           # opencode, claude-code, antigravity, codex
python3 scripts/coacus_install.py opencode --dry-run
python3 scripts/coacus_install.py opencode --uninstall
```

Skill sources installed everywhere are `methodology/workflows/**` and
`knowledge/skills/**`, flattened into one namespace. Each skill installs as
`<skill>/SKILL.md` plus its companions (`references/`, `examples/`, `scripts/`).

## opencode

**Goal:** the OpenCode session starts with the Coacus entry skill already loaded.

**How it works.** Coacus ships an OpenCode **plugin** — an in-process module the
harness loads. The plugin does two jobs: it registers the two skill roots, and it
injects the bootstrap into the first user message. The bootstrap carries an
anti-reinjection guard so a compact or replay does not duplicate it
([ADR-0009](adr/ADR-0009-session-start-bootstrap.md)).

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
both injects the body twice ([ADR-0009](adr/ADR-0009-session-start-bootstrap.md)).

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

**Goal:** Antigravity loads Coacus as a plugin and injects an instructions file
at session start.

**How it works.** Antigravity uses an **instructions-file** bootstrap: instead of
a shell hook or an in-process module, the adapter renders `ANTIGRAVITY.md`, and
the harness injects that file's content through its plugin context mechanism.

**Vendor facts**

- `agy plugin install <dir>` installs a plugin; `list`, `enable`, `disable` and
  `uninstall` manage it. **[documented]**
- The manifest is `plugin.json` with only `name` and `description`. **[documented]**
- Plugin activation is by directory: `.agents/plugins/` in a workspace,
  `~/.gemini/config/plugins/` globally. The CLI stages plugins at
  `~/.gemini/antigravity-cli/plugins/<name>/`. **[documented]**
- `agy plugin validate` returned `[ok]` on the staged Coacus plugin.
  **[verified locally]**
- `contextFileName` in `plugin.json` and the `~/.gemini/config/plugins.json`
  `entries[].path` registry are **not** in the official documentation. Coacus
  uses both empirically because they activate the context file in the local
  installation. **[unverified]**

**Install**

```bash
python3 scripts/coacus_install.py antigravity
```

The script stages the plugin at `<config>/config/plugins/coacus/` with
`plugin.json`, `ANTIGRAVITY.md` and the skills, then registers the plugin path in
`<config>/config/plugins.json` under `entries[].path`, backing up the file first.
It does not invoke `agy plugin install` itself; that command expects a plugin or
marketplace target and is left to the operator.

**Verify**

```bash
agy plugin validate ~/.gemini/config/plugins/coacus   # expect: [ok]
```

If `agy plugin install` is your preferred route, point it at the staged
directory. The registry edit is the fallback the adapter performs.

## codex

**Goal:** Codex discovers the Coacus skills natively.

**Current state.** Coacus's Codex adapter is **native-discovery**: it mirrors the
skill trees and renders no bootstrap. `harnesses/codex/harness.json` reports
`bootstrap.supported: false` with the reason "Codex surfaces skills natively and
runs no session-start hook; nothing is rendered."

**Vendor facts**

- Codex loads skills from `$CWD/.agents/skills`, `$REPO_ROOT/.agents/skills` and
  `$HOME/.agents/skills` — **not** `~/.codex/skills/`. **[documented]**
- Codex **does** have a `SessionStart` hook framework, configured through
  `~/.codex/hooks.json`, `config.toml`, or `<repo>/.codex/hooks.json`, emitting
  `additionalContext`. **[documented]**
- `[[skills.config]]` enables skills explicitly. **[documented]**

> **Known gap.** The Coacus Codex adapter predates Codex's SessionStart support.
> It still installs skills to `~/.codex/skills/` and renders no bootstrap, so a
> Codex session never receives the entry skill through a hook. This is a candidate
> for a future phase: a shape-A render for Codex plus an install target under
> `.agents/skills` and a `SessionStart` hook manifest. The adapter file is not
> changed here; the gap is recorded so the next phase can close it.

**Install** (skills only):

```bash
python3 scripts/coacus_install.py codex
```

Because Codex's documented skill search does not include `~/.codex/skills/`, a
manual install should target a directory Codex actually scans — for example
`~/.agents/skills/` for a user-wide install, or `<repo>/.agents/skills/` for a
single project:

```bash
python3 scripts/coacus_install.py codex --config-dir ~            # -> ~/.codex/... (current default)
python3 scripts/coacus_install.py codex --config-dir ~/.agents    # -> ~/.agents/skills/<skill>/
```

Confirm which root your Codex version scans before relying on the default.

## cursor

**Goal:** none yet — the render is deferred.

**Current state.** Coacus's Cursor adapter is a **stub**. `harness.json` reports
`bootstrap.supported: false` because Cursor's `sessionStart` hook cannot be
verified live here; the render is deferred until a live acceptance test is
possible. `coacus_install.py cursor` prints guidance and exits 0.

**Vendor facts** (recorded for when the render is built)

- Plugins use `.cursor-plugin/plugin.json`. **[documented]**
- Hooks live in `.cursor/hooks.json` (project) or `~/.cursor/hooks.json` (user) —
  **not** `hooks-cursor.json`. **[documented]**
- `sessionStart` is fire-and-forget and outputs the snake_case key
  `additional_context`. **[documented]**
- Skills load from `.cursor/skills/`, `~/.cursor/skills/`, `.agents/skills/` and
  `~/.agents/skills/`, plus the Claude and Codex compatibility locations.
  **[documented]**

The legacy `hooks-cursor.json` filename is gone from the adapter; a future
render must use `.cursor/hooks.json` and emit `additional_context`, then pass a
live acceptance test before it is promoted out of stub status.

## Reference

### Install targets

| Harness | Shape | Bootstrap mechanism | Install target | Evidence |
|---|---|---|---|---|
| **opencode** | B (in-process) | `config` + `experimental.chat.messages.transform` hooks | `~/.config/opencode/plugins/{coacus.js,coacus-governor.js}` + skills at `~/.config/opencode/skills/` | plugin load **[verified locally]**; mirror path **[unverified]** |
| **claude-code** | A (shell hook) | `SessionStart` → `hookSpecificOutput.additionalContext` | skills at `~/.claude/skills/<skill>/`; helper plugin at `~/.claude/plugins/coacus/` | vendor plugin route **[documented]**; staging path **[unverified]** |
| **antigravity** | C (instructions file) | context file (`ANTIGRAVITY.md`) via `plugin.json` | `<config>/config/plugins/coacus/` registered in `<config>/config/plugins.json` | registry + `contextFileName` **[unverified]**; `agy plugin validate` **[verified locally]** |
| **codex** | native-discovery | none rendered | skills (see the Known gap; Codex scans `.agents/skills`) | skill roots + hook framework **[documented]** |
| **cursor** | stub | deferred | not installed | vendor hook facts **[documented]**; render deferred |

### Verifying

| Check | Command |
|---|---|
| Structure and drift | `python3 scripts/coacus.py check` |
| Source and artifact contracts | `python3 scripts/coacus.py validate` |
| Antigravity plugin | `agy plugin validate <staged-dir>` |
| Claude Code hook parses | `python3 -c "import json; json.load(open('harnesses/claude-code/bootstrap/hooks.json'))"` |
| Claude Code script syntax | `bash -n harnesses/claude-code/bootstrap/session-start.sh` |

The live test for any harness is behavioral: a fresh session with the bootstrap
must produce a string that exists only in `using-coacus` — the red-flag thought
`"This is just a small change."` A session without the bootstrap must not produce
it. Live acceptance has been run on OpenCode; Claude Code is structure-verified
only, because the binary was not available locally.
