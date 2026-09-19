# Installing Coacus into a harness

The repository **generates** the per-harness artifacts (ADR-0016) and commits
them. Making a harness actually load them is a separate, explicit step: each
harness discovers plugins/skills from its own locations, and Coacus never edits
a harness config file wholesale.

Two ways to install:

- **Manual** — copy the rendered artifact to the path in the table below.
- **Script** — `python3 scripts/coacus_install.py <harness|all>` (idempotent;
  `--dry-run` to preview, `--uninstall` to remove a previous install,
  `--config-dir` to install into a non-default location for testing).

Run `python3 scripts/coacus.py generate` first so the rendered artifacts exist.

## What gets installed, by harness

| Harness | Shape | Bootstrap mechanism | Install target | How Coacus installs |
|---|---|---|---|---|
| **opencode** | B (in-process) | message transform + `config.skills.paths` | `~/.config/opencode/plugins/{coacus.js,coacus-governor.js}` + skills mirrored to `~/.config/opencode/skills/` | `coacus_install.py opencode` copies both plugins (substituting `__COACUS_ROOT__`) and mirrors the skill trees |

The opencode install includes the **governor gate** (`coacus-governor.js`): it
intercepts subagent spawns, enforces the concurrency cap, and parks a caller as
PAUSED on a rate-limit. Knobs: `ORCH_MAX_CONCURRENT` (default 5),
`GOVERNOR_STATE_DIR` (ledger location), `GOVERNOR_LEASE_SECONDS` (stale-slot
reclaim). Inspect the ledger with `python3 scripts/coacus_governor.py status`.
| **claude-code** | A (shell-hook) | `SessionStart` hook → `hookSpecificOutput.additionalContext` | skills: `~/.claude/skills/<skill>/`; plugin: `~/.claude/plugins/coacus/` with the script at `bootstrap/session-start.sh` | `coacus_install.py claude-code` (a published Claude Code plugin/marketplace is the long-term path) |
| **antigravity** | C (instructions-file) | extension context file (`contextFileName` → `ANTIGRAVITY.md`) | `<config>/config/plugins/coacus/` registered in `<config>/config/plugins.json` | `coacus_install.py antigravity` stages the plugin and registers its path (backs up `plugins.json`) |
| **codex** | native-discovery | none — Codex surfaces skills natively, no SessionStart hook | `~/.codex/skills/<skill>/` | `coacus_install.py codex` mirrors the skill trees |
| **cursor** | A (shell-hook) | `.cursor-plugin/` + `hooks-cursor.json` | plugin marketplace | not installed — render deferred until a live acceptance test is possible |

Skill sources installed everywhere are `methodology/workflows/**` and
`knowledge/skills/**` (one flat namespace; each `<skill>/SKILL.md`).

## Manual install (per harness)

### opencode

1. Generate: `python3 scripts/coacus.py generate`.
2. Copy `harnesses/opencode/bootstrap/coacus.js` to `~/.config/opencode/plugins/coacus.js`,
   replacing `__COACUS_ROOT__` with this repository's absolute path.
3. Alternatively, add the skill folders directly in `opencode.json`:
   ```jsonc
   { "skills": { "paths": ["<repo>/methodology/workflows", "<repo>/knowledge/skills"] } }
   ```
   The plugin already does this via the `config` hook, so step 3 is only needed
   if you prefer config over a plugin.

Verify (isolated, no global changes):
```bash
mkdir -p /tmp/oc/plugins
sed "s|__COACUS_ROOT__|$PWD|" harnesses/opencode/bootstrap/coacus.js > /tmp/oc/plugins/coacus.js
OPENCODE_CONFIG_DIR=/tmp/oc opencode run \
  "In one short sentence, name one 'red flag' thought from the guidance already in your context."
```

### claude-code

1. Skills: copy each `<skill>/SKILL.md` tree (with its `references/`) under
   `~/.claude/skills/<skill>/`.
2. Bootstrap hook: the plugin's `hooks.json` invokes
   `"${CLAUDE_PLUGIN_ROOT}/bootstrap/session-start.sh"`, so the script must be
   installed at `<plugin>/bootstrap/session-start.sh`. `coacus_install.py
   claude-code` stages exactly that at `~/.claude/plugins/coacus/`.
3. Long-term, publish the repository as a Claude Code plugin/marketplace; the
   hook emits exactly one native key (`hookSpecificOutput.additionalContext`).

### antigravity

1. Stage a plugin directory containing `plugin.json` (with `contextFileName:
   "ANTIGRAVITY.md"`) and `ANTIGRAVITY.md`.
2. Validate through the harness's own command (verified live):
   ```bash
   agy plugin validate <staged-dir>   # expect: [ok]
   ```
   `coacus_install.py antigravity` performs the staging and registers the path
   in `~/.gemini/config/plugins.json` (`entries[].path`) — it does not invoke
   `agy plugin install` itself; that command expects a plugin/marketplace
   target and is left to the operator.

### codex

Codex runs no SessionStart hook; it surfaces skills natively. Install only the
skills:
```bash
python3 scripts/coacus_install.py codex     # -> ~/.codex/skills/<skill>/SKILL.md
```

### cursor

Not installed yet: no local installation exists to run the acceptance test that
shape A requires. When a Cursor install is available, the render is a shell hook
plus `.cursor-plugin/plugin.json` pointing at `hooks-cursor.json`.

## Verifying

- **Structure**: `python3 scripts/coacus.py check` (rendered artifacts are
  committed and drift-checked) and `python3 scripts/coacus.py validate`.
- **Live (unique marker)**: after installing, a fresh session must repeat a
  string that exists only in `using-coacus` (e.g. ask the model to name a
  red-flag thought; the correct answer quotes `"This is just a small change."`).
  A session without the bootstrap must not produce it.
- **antigravity structure**: `agy plugin validate` on the staged plugin.
- **claude-code structure**: `hooks.json` parses; `session-start.sh` passes
  `bash -n` and emits a single `hookSpecificOutput` key.
