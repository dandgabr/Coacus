# Changelog

All notable changes to Coacus are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/); entries are grouped by
development phase (F0–F8) because the repository has not yet cut version tags.
The repository adheres to [Semantic Versioning](https://semver.org/) once it does.

## [Unreleased] — Verify reports a missing hook script

### Changed

- `coacus_install.py --verify` now reads the hook files an install wrote and lists, under `hook_scripts_missing`, any Coacus hook whose script is no longer on disk (a moved repository or a removed worktree). A non-empty list fails the verification. A plugin that embeds its path as source, such as the OpenCode one, is not covered.

## [Unreleased] — OpenCode ask without the experimental opt-in

### Changed

- An `ask` policy on an OpenCode read or write is now decided through the permission `evaluate` hook with `COACUS_GUARD_ASK=1` alone. `COACUS_GUARD_ASK_EXPERIMENTAL` is retired and ignored, and the installer no longer asks for it. Instead it warns, for each OpenCode ask that will be deferred, that `--auto` approves the ask without a prompt. The path was run live on OpenCode 2.3.0 (interactive "Allow once" and "Reject"). Under `--auto` the harness still approves an ask by itself, so only a `deny` is a barrier there; see ADR 0010.

## [Unreleased] — Isolated Python for every hook

### Changed

- Every installed hook that runs a Coacus script (the session-start bootstrap and the guard on all harnesses, and the OpenCode guard and governor plugins) now starts Python with `-I`, so a file named like a standard module in the working directory or the user site cannot be imported in its place. Entries from an earlier install are still recognised and replaced when the installer runs again. The scripts add the repository root themselves, so nothing else changes. See ADR 0019.

## [Unreleased] — Exclusive roles for three review agents

### Changed

- `security-specialist` now answers security questions and routes work to the agent that owns it. It no longer carries the code-review protocol or runs assessments.
- `security-architect` is the security architect of the project: threat models, trust zones, control baseline, Technical Opinions and Go-Live gates, with an explicit role boundary.
- `project-reviewer` is the general reviewer across every aspect. It received the security code-review protocol and its finding schema, and it can dispatch project-defined and catalog agents, read-only and under the governor.
- A security-only review has an owner: `project-reviewer` takes a review limited to one aspect. Dispatch rules no longer cite a `@CTX` chain, which the TOON protocol does not define; they say never to re-dispatch the agent that handed you the task, and that a delegate returns `NEED_INFO`.
- Routing terms: `revisao de seguranca` moved from `security-architect` to `project-reviewer`; `security question`, `security triage` and common vulnerability names route to `security-specialist`, and pull-request and threat-model phrases route to `project-reviewer` and `security-architect`.

## [Unreleased] — Skill-gap candidate type

### Added

- Snapshots are split on newlines only, so a record that carries U+2028 or U+0085 is no longer cut and dropped. A downgraded proposal records `downgraded` and `original_type`, and a gap claim is compared after NFKC folding, case folding and whitespace collapse.
- The improvement loop can propose a `skill-gap` when an observation carries the structured field `kind: "route-miss"`. On every routing branch it needs a trusted-channel unit from three distinct sessions; its claim is cleaned and hashed in full, its statement is capped, and the stored proposal never keeps the text. Types that need trust now come from one constant, `taint.TRUST_REQUIRED`. See ADR 0013.
- A `skill-gap` can only come from the new `route-miss` source, which `scripts/coacus_route.py` feeds when no agent matches and `COACUS_ROUTE_MISS_LOG=1` is set, in a private per-user state file outside any repository, with the UTC day as the session. The source sets the kind, channel and session in code, so a transcript or export record can no longer declare a gap, and a prompt typed without a terminal never counts as trusted evidence.

## [Unreleased] — Guard events, MCP verb and self-protection

### Added

- A `prompt` verb and a `prompt.submit` hook on Claude Code (`UserPromptSubmit`): a policy can block a prompt whose text matches a case-insensitive pattern, with the reason shown to the user and the original prompt not echoed. The hook exists only while an enabled policy binds the event; a prompt over 100,000 characters matches every prompt rule. See ADR 0016.
- An `output` verb and a `tool.post` hook on Claude Code (`PostToolUse`): a `note` policy attaches its message to the result of a tool that already ran. It never blocks; a `deny` on `tool.post` in a repository policy that names the event is refused at install, and at run time only a `note` renders. The output is read whole, in overlapping windows, after folding. See ADR 0018.
- An `mcp` verb, so a policy can constrain an MCP tool by the name the harness sends (`mcp__server__tool`, `server_tool`, `MCP:tool`), and OpenCode tools outside its native list are classified as `mcp`. See ADR 0014.
- An opt-in self-protection policy that denies the session's write tools on the guard, its policies and the harness hook files, with `coacus_install.py --self-protection on|off|prompt` (default `prompt` on a terminal, answer No). See ADR 0015 and `docs/install.md`.
- Antigravity payloads (`toolCall.name` and `toolCall.args`) are now read, and `grep_search`, `find_by_name`, `list_dir`, `multi_replace_file_content` and `search_web` are classified; a search tool also checks the glob it was given. The argument names other than `CommandLine` are unverified and marked so in `harness.json`.

### Changed

- The hook for `prompt.submit` and `tool.post` runs through a launcher that skips a missing guard script instead of letting Claude Code read the exit code 2 as a block, and runs with `python -I` so a file in the project's working directory cannot shadow a standard module. `tool.pre` keeps its plain command and still blocks when the guard is missing.
- `tool.post` and `prompt.submit` hooks are added to or removed from the user's hook file on every install according to whether an enabled policy binds the event, so enabling or disabling one takes effect at the next install.

### Known limits

- `turn.stop` is not rendered: a block there means "keep going" and needs a repetition limit.
- Codex documents the same events but ignores a new hook until it is trusted in `/hooks`; it was not run live for `prompt.submit` or `tool.post`, so it stays out.
- The Antigravity argument names, the `tool_response` shape of tools other than Bash, and the stderr visibility of a skipped hook are unverified.

## [Unreleased] — Final review findings

### Fixed

- The installer warning no longer crashes on a policy whose `action` is not an object or on a non-object policy document, and it warns when an OpenCode read or write `ask` is anchored on one path shape (for example `sub/*`), which the guard does not defer.
- A mechanism failure in the guard now writes a one-line advisory on stderr (without the payload) while still allowing the call, as ADR 0002 says. ADR 0010 now lists the risks that apply to every harness: a guard the session can edit, tools the guard cannot classify, permission modes that auto-approve, and asks inside a subagent.
- New tests guard fail-closed branches that mutation testing showed were unprotected: the value of `ask_channel`, the relative path forms, the step limit, the depth cap of the keyword loop, an internal error in the walk, and the two-terminal rule of the installer prompt.

## [Unreleased] — Event binding

### Fixed

- The evaluator now honours a policy's `event` (default `tool.pre`), so a rule written for a tool call never fires on another event. A policy whose `event` is not a canonical id applies everywhere instead of silently stopping. The guard decides, blocks and asks only on `tool.pre` and answers "no opinion" on any other event. At that point no hook was rendered for `tool.post`, `prompt.submit` or `turn.stop`; `prompt.submit` and `tool.post` have one now (see below) and `turn.stop` is still deferred. See ADR 0012.
- Three capability cells now match the vendor documentation (2026-11-18): claude-code `prompt.submit` cannot ask, codex `prompt.submit` can block, cursor `turn.stop` cannot block.

## [Unreleased] — Installer ask warning

### Added

- `coacus_install.py` warns on stderr about each enabled `ask` policy that will not prompt anyone (the harness cannot ask, or `COACUS_GUARD_ASK=1` is not set) and marks a fallback of `allow` as failing open. On a terminal it asks "Continue with the installation? [y/N]" before writing anything; any answer but yes, EOF or Ctrl-C cancels with exit code 2. `--yes` skips the question, a non-interactive run only warns, and `--dry-run` never asks. It also names the off switches (`CI`, `COACUS_GUARD_NO_ASK`) and, on OpenCode, any `ask` that is not a read or a write, which that harness cannot defer. The warnings are also in the JSON result and in `--verify`, and a malformed policy file no longer crashes either.

## [Unreleased] — OpenCode ask through the evaluate hook

### Added

- The OpenCode guardrail plugin registers the V2 permission `evaluate` hook when the API exists. With `COACUS_GUARD_ASK=1` and the explicit `COACUS_GUARD_ASK_EXPERIMENTAL=1` an `ask` policy on a read or write whose pattern holds for every plausible shape of the path (for example `*.env`) now prompts a person there; a command, a subagent request or a policy anchored on one path shape is not deferred and degrades to its fallback, because the hook sees a resource shape the guard cannot know; the hook can only tighten an effect (deny over ask over allow) and leaves it unchanged if the guard fails.
- `scripts/coacus_guard.py` takes `--channel default|before|evaluate`. A harness whose capability cell has `ask_channel` asks only on that channel, so a V1 install, or a failed hook registration, degrades an `ask` to its fallback instead of letting it through.

### Known gaps

- Checked against the OpenCode documentation of 2026-11-18 and a fake `ctx`, not a live V2 run. Whether OpenCode awaits the hook, how it orders `evaluate` against `tool.execute.before`, and the resource shape for each permission are not verified and are recorded as a gap in the harness data. If the guard cannot run when the hook fires, the effect is left as it came, so the prompt is lost (fail open by design).

## [Unreleased] — Command walk hardening

### Fixed

- A final adversarial pass, again checked against a real bash, found 18 more inputs; all are closed: a comment that hides a here-document marker, more than eight option words in front of a wrapped command, `trap`, `flock -c`, `su`/`script --command=`, `mapfile -C`, `alias`, `hash -p`, `BASH_ENV` and other startup variables, `bash -o posix` and `--rcfile`, a named `coproc`, a `case` pattern inside a substitution, a `$'EOF'` here-document tag, a quote inside a nested here-document, `at`, `batch` and `parallel`. Substitutions are now skipped as a unit, so a stray quote in a commit-message heredoc no longer causes a false deny, and an interpreter here-document (`python3 - <<EOF`) is read as data. Interpreters that run a program themselves (`python3 -c`, `perl -e`) are out of scope and now said so in ADR 0011.
- A second security review ran each input against a real bash and found 13 classes that a command deny rule let through. All are closed: an apostrophe or a `<<` inside a here-document or quotes, a here-document read by an absolute-path shell or by `source`, shells that read a script from a pipe, expansions and globs inside the command word, line continuations, `A+=1` and array assignment prefixes, the `function` keyword, nested parentheses in a substitution, and launchers such as `chroot`, `strace`, `watch 'cmd'` and `script -qc 'cmd'`. See ADR 0011.
- One malformed policy file or entry (`[]`, `"policies": null`, a string, bad UTF-8, a non-object `action`) used to make the guard allow everything. Each file and entry is now skipped alone, and a policy that raises while matching is skipped on its own.
- A very long chain (`env env env ...`, `find -exec ...`, thousands of unbalanced `$(`) took seconds to minutes and hundreds of megabytes; the walk is now memoized and capped and fails closed beyond the cap.
- Tool names are matched without regard to case; `Grep`, `Glob`, `MultiEdit`, `NotebookEdit`, `patch` and `WebSearch` are classified, and a patch that touches several files is checked for each file.

## [Unreleased] — Command deny bypasses

### Fixed

- Command deny rules now look through brace groups, `if`/`then`/`while` and `!`, process substitution, `eval`, here-strings to a shell, `find -exec` and `env -S`. Review then widened it: leading redirections and `--`, a shell behind a wrapper (`sudo sh -c`), `busybox`, `su -c`, `runuser` and `watch`, ANSI-C quoting, brace expansion, an expansion in command position and a pipe into a bare shell now fail closed. Three shapes stay open and are pinned in the corpus. See ADR 0011.
- An unbalanced quote now counts as unresolved and denies, instead of being guessed; a quoted argument that spans lines still parses, so a multi-line commit message is not denied. A value over 100,000 characters matches every pattern, and exactly one trailing newline is ignored (thousands of them no longer crash the matcher and turn a deny into an allow).

## [Unreleased] — Strictest ask fallback

### Fixed

- Two `ask` policies that match the same action used to take the `on_ask_unavailable` of the first file. The strictest value now wins (`deny` beats `allow`; a missing or invalid value counts as `deny`), so the result no longer depends on file order, and the reported policy is the one that holds the winning fallback.

## [Unreleased] — Evaluator fails closed

### Fixed

- A resource pattern with several `*` could take exponential time in the regex fallback (about 1.7 s for 50 characters, growing roughly five times per ten more), which made the guard time out and fail open. The fallback is now a bounded two-pointer matcher.
- A command nested deeper than the depth limit, longer than the size cap, or behind a long wrapper chain used to yield no executable names, so a command deny rule saw nothing to block. It now counts as unresolved and matches every `match: command` policy. The depth limit rose from 4 to 8 so ordinary wrapper chains stay resolved.
- A policy with an unknown or misspelled `decision` (for example `Deny`) used to rank below `allow` and let the call through. It now denies.

## [Unreleased] — Guard command corpus

### Added

- `tests/test_guardrail_command_corpus.py` locks how command deny rules read shell lines: wrappers, `sh -c`, command substitution, pipes, symlinks and mere mentions, plus two end-to-end checks of the JSON the guard prints.
- It also records seven shapes that bypass a command deny rule today (a brace group, process substitution, `eval`, a here-string, `find -exec`, `env -S` and variable indirection) and two false positives (`sudo grep NAME` and `xargs grep NAME`). They are pinned to today's answer, so the suite fails when one is fixed and says where to move it. Plain assertions are used instead of `expectedFailure`, which would also hide a crash.

## [Unreleased] — Guard deny for OpenCode

### Fixed

- The OpenCode `tool.pre` evidence now cites the current plugin documentation, `install.target` lists all three plugins, and `docs/install.md` describes the guardrail plugin.
- `scripts/coacus_guard.py` now renders a `deny` for OpenCode. Before this change it printed `{}` for that harness, so the generated plugin never saw a deny and no policy blocked a tool call there. An `ask` also renders as `deny`, because OpenCode has no way to ask. Tests prove the block end to end with the generated plugin under Node, through both the named export and the default export; they skip locally without Node and fail in CI.

## [Unreleased] — Guard `ask` capability gating

### Changed

- `scripts/coacus_guard.py` now renders a native `ask` only when the operator sets `COACUS_GUARD_ASK=1`, neither `COACUS_GUARD_NO_ASK` nor `CI` is set to a truthy value, and `harness.json` declares both `can_ask` and `can_block` for `tool.pre`. By default nothing asks, as before: every `ask` still degrades to the policy's `on_ask_unavailable`. See ADR 0010.
- A missing or invalid `on_ask_unavailable` now fails closed to `deny`. Before this change an unrecognised value was rendered as `ask`; this is a tightening that needs no opt-in.
- Any error while reading capability data degrades the decision instead of escaping, and harness names are limited to lowercase ASCII letters, digits and dashes that start with a letter or a digit.
- With the opt-in set, policies can now prompt a person on claude-code and antigravity instead of denying, which is a relaxation chosen by the operator.

### Known gaps

- On OpenCode the guard rendered no effect, so a `deny` did not block a tool call. Fixed in the "Guard deny for OpenCode" entry.

### Fixed

- The Cursor `tool.pre` cell now says `can_ask: false`. Its hooks documentation says `"ask"` is accepted by the schema but not enforced for `preToolUse`, so an opted-in `ask` would not have prompted anyone there.

## [Unreleased] — Tabler component integration and consumer verification

### Added

- Narrow `framework-tabler` skill with version-matched documentation lookup, client lifecycle guidance and conditional discovery from existing frontend and design QA agents.
- Consumer-contract procedures for unknown classes, stale exceptions and baseline-first compatibility checks; these are guidance, not new runtime validators.
- Standalone forced-colors and reduced-motion fixture exercises and focused behavior evaluation scenarios. Static schema checks, live evaluation and browser observations remain separate evidence layers.

## [Unreleased] — Zero external MCP dependencies and primary version resolution

### Removed

- Canonical `context7` MCP definition under `knowledge/mcps/context7/` (`MCP.md`, `dist/mcp.json`, `dist/mcp_config.json`).
- External MCP recommendation from `README.md` and `docs/install.md`.

### Changed

- `docs/standards/version-freshness.md` and skill `version-freshness`: migrated library and framework version resolution from Context7 to authoritative package registries (npm, PyPI, crates.io, Maven Central) and vendor release sources.
- Canonical agents (`web-researcher`, `scientific-researcher`, `web-search-specialist`) and entry workflow `using-coacus`: updated instructions to resolve versions via primary registries and publisher release notes.
- Synchronized generated discovery manifests (`.agents/mcps.json`), catalog indexes (`catalog/catalog.json`, `catalog/INDEX.md`), and python API reference (`docs/reference/python-api.md`).

## [Unreleased] — Session learnings: gate parity and baselines

### Added

- Process conventions: the local gate is what CI runs, linter included, with the
  declared development tools installed; removing a concept orphans parameters,
  branches, fixtures and saved identifiers, not only files.
- Test-driven development: tests pin the environment inputs they read, and a reader of
  stored data keeps legacy values readable, proven by a test with an old saved value.
- Verification before completion: measure the baseline on the base revision before
  attributing a failure, and rebuild generated inputs after switching revisions.
- `lang-bash`: process control by PID, never by a command-line match from a shell that
  contains the pattern.
- `ui-design-craftsmanship`: icon and asset set constraints live in a structural test.
- `ui-ux-principles`: a display preference must not change alerting or ranking.

## [Unreleased] — Antigravity hooks never deny by omission

### Fixed

- Antigravity: the `coacus-guard` and `coacus-governor` PreToolUse hooks returned
  an empty object (`{}`) to permit. Antigravity's contract makes `decision`
  required on that event and reads a decision-less result as a denial
  (`tool call denied by pre-tool hook:` with an empty reason), so an
  unopinionated hook blocked every tool call. Both now answer an explicit
  `{"decision": "allow"}`, including the guard's mechanism-failure path so the
  fail-open guarantee holds on the one harness where `{}` is a deny.
- Antigravity: the rendered `coacus-guard` hook now uses the documented
  `matcher`/`hooks` grouping for tool events instead of a flat handler.

## [Unreleased] — Browser selection policy

### Added

- Install-time browser policy: the installer detects installed browsers
  (`methodology/lifecycle/browsers.json`), lets the user choose a primary and an
  optional fallback, and generates a machine-local deny policy for every other
  known browser (launch and profile read/write). Opt-in (`--browser-policy
  auto|prompt|off`, `--browser-primary`, `--browser-fallback`,
  `--browser-policy-dir`); prompts on an interactive terminal, off otherwise.
- `exec` policies may use `"match": "command"` with a `resource` pattern list to
  match executable names instead of the whole command string.
- The runtime guard also loads machine-local policies from the user policy
  directory (`COACUS_POLICY_DIR`, `$XDG_CONFIG_HOME/coacus/policies`).

### Removed

- The imported `browser-harness` skill: Coacus does not ship or own that tool.

## [Unreleased] — Dynamic per-harness concurrency governor

### Changed

- Concurrency governor (`engine/governor/ledger.py` and `scripts/coacus_governor.py`):
  Eliminated single shared global cap bottleneck; partitioned disk ledgers into
  isolated scopes (`ledger-{scope}`). Default caps map to documented limits
  (Ollama = 2, Command Code = 4, Cursor = 5, OpenCode = 5, Antigravity = 6,
  Claude Code = 8, Codex = 10, and unlisted/others = 6).
- Added authoritative `set-max <n> [--scope <scope>]` command to allow dynamic
  elevation of persisted caps without destroying the ledger.
- Added hierarchical precedence resolution for model and harness environment
  variables (`COACUS_MAX_<MODEL>`, `COACUS_MAX_<SCOPE>`,
  `CLAUDE_CODE_MAX_TOOL_USE_CONCURRENCY`, `OLLAMA_NUM_PARALLEL`, and `ORCH_MAX_CONCURRENT`).

## [Unreleased] — Shared skills tree (single source of truth)

### Changed

- The installer places real skill files once in the shared `~/.agents/skills` tree
  and wires a harness that scans its **own** skill home (Claude Code's
  `~/.claude/skills`) with a symlink per skill, so a consumer that scans several
  homes at once (Orca's Skills page reads Claude, Codex, Agent Skills and OMP)
  shows each skill once instead of a duplicate. Adds `--skills-mode {link,copy}`
  (`link` is the default for `claude-code`; `copy` restores the previous
  per-harness copies). Uninstall removes only the link, never the shared target.
- At a harness's real install location the shared `~/.agents/skills` tree is left
  read-only after install (default; `--no-lock-skills` opts out), so a consumer's
  own delete/update of a Coacus skill fails instead of silently rewriting it. The
  next install restores write access before rewriting; `--config-dir` is never locked.

## [Unreleased] — Elfvision lifecycle and discovery lessons

### Changed

- GNOME extension references cover observable preferences actions, signal cleanup,
  session-turnover recovery, account-preserving updates, and native theme geometry.
- The skill's discovery description names stale controls, coordination failures
  and installed-versus-loaded mismatches.
- README and documentation indexes link the desktop-extension reference map;
  usage and contribution guidance describe skill discovery and reference updates.
- The durable [Elfvision learning report](docs/reports/2026-10-08-elfvision-learning-consolidation.md)
  moved from process scratch into the committed reports directory.

## [Unreleased] — GNOME connector, effects and delivery lessons

### Changed

- GNOME extension guidance routes account identity and deletion, monetary API
  reporting, native layout/materials and installed-runtime verification into
  evidence-linked references.
- Theme guidance distinguishes default backgrounds from supported overrides and
  native rendering from browser previews; release guidance rejects false or
  unfinished evaluation results and checks the installed archive and uploaded assets.
- Security-scanning guidance distinguishes successful analysis jobs from aggregate
  alert status and addresses incomplete URL assertions in tests.

### Added

- Read-only behavioral scenarios for native delivery evidence and connector/theme
  contracts, with semantic rubrics distinct from their lightweight output checks.
- A [consolidation and verification record](docs/reports/2026-10-08-gnome-quota-delivery-learnings.md).

## [Unreleased] — Codex installer migration fixes

### Fixed

- Reinstallation retires legacy Coacus shell hooks from earlier checkout paths
  while preserving unrelated user hooks.
- Codex interface tables inserted inside the managed skill-profile markers are
  preserved during reinstallation and uninstall, and no longer cause false
  profile drift reports.

## [Unreleased] — Process measurement and evidence lessons

### Changed

- `superpowers-verification-before-completion` requires claims to name the
  resolved manifest, exact error/result and artifact copy in force.
- `superpowers-systematic-debugging` distinguishes absence from unreachable,
  locked or out-of-scope results and requires the measured file to be identified.
- `superpowers-executing-plans` treats plan code as a snapshot of intent and
  returns interface corrections to later plan references.
- `superpowers-subagent-driven-development` requires the delegated artifact path
  and evidence that the worker actually read it.
- `using-coacus` carries these measurement rules and requires consent for
  credential metadata inspection, redaction before output and synthetic checks
  of redaction behavior.
- Generated harness bootstraps and the provenance lock carry the updated entry
  skill and workflow sources. These changes are proposed in
  [PR #62](https://github.com/dandgabr/Coacus/pull/62).

## [Unreleased] — Python tooling portability and Codex catalog

### Added

- Portable Python workflow helpers, a checksum-verified Python secret-scan
  runner, and Linux/macOS/Windows hook-contract CI at the supported Python floor.
- A compact Codex native skill profile and on-demand canonical skill search.
- A [dated implementation and verification record](docs/reports/2026-10-02-python-only-migration.md)
  covering PRs #60/#61, integration into `main`, local reinstallation and the
  authorized removal of historical shell files while preserving plugins.

### Changed

- Generated hook wrappers use JSON payloads and direct Python entrypoints.
  OpenCode's vendor plugin adapters invoke Python through native JavaScript.
- The installer pins its interpreter, handles host command quoting, retires
  manifest-owned legacy scripts and excludes Python bytecode caches.
- Workflow imports preserve reviewed Python conversions and upstream provenance;
  changed upstream helpers require review before reimport.

### Fixed

- Host bootstraps install before verification and propagate failures.
- Windows shell expansion, native child-output encoding and legacy manifest
  separators are covered by regression checks.
- SessionStart resolves the Codex skill-search repository path inside JSON.
- The Antigravity Python governor hook uses the supported ledger timeout option.
- Verification checks all expected Coacus hook entries; provenance refresh keeps
  the source identities of converted and adapted artifacts.

## [Unreleased] — F9/F10: lifecycle guardrails and self-improvement loop

### Added

- **F9 — Portable lifecycle guardrails (PAER).** One policy authored once,
  rendered natively per harness:
  - Canonical data: `methodology/lifecycle/{events.json,actions.schema.json,records.schema.json}`
    and `methodology/lifecycle/policies/` (empty and disabled by default).
  - `engine/generators/plugins.py` — a `kind`-keyed plugin registry extracted from
    `bootstrap.py` (a hooks-only harness is now representable).
  - `engine/generators/guardrails.py` + `engine/generators/lifecycle.py` (generated
    capability matrix) + `engine/generators/outputs.py` (cross-generator path
    uniqueness).
  - `engine/guardrail/` + `scripts/coacus_guard.py` — the runtime evaluator.
  - `engine/validators/harnesses.py` — the harness-manifest schema validator.
  - Installer: per-ENTRY-id hook ownership, container-aware merge, and
    refuse-to-install for a `deny` the harness cannot block (`--allow-advisory`
    records the downgrade).
  - Standards `lifecycle-guardrails` and `decision-records`; ADRs 0001–0004 and
    0006.
- **F10 — Self-improvement loop (proposer-only).** `engine/improve/` plus a thin
  `scripts/coacus_improve.py`: pluggable episodic sources (`transcript` default,
  `ai-memory` optional), typed consolidation, retrieval-first routing, a
  verification ladder, taint labeling, and a runtime ledger. It never applies.
  Standard `self-improvement-loop`; ADR 0005.
- New standards count is machine-reconciled (`engine/validators/docs.py`).

### Changed

- `engine/generators/bootstrap.py` is now a facade over `plugins.py`; guardrail
  artifacts are disjoint from the bootstrap `hooks.json` (one producer per path).
- `tests/test_idempotency.py` covers the bootstrap, discovery and routing
  generators, not just agent manifests and the catalog.

### Security

- Guardrails default to an empty, disabled policy set; the reference policy is
  disabled (ADR 0006).
- Failure is split: a decision failure denies, a mechanism failure allows with an
  advisory (ADR 0002).
- The improvement loop has no apply path and no import path to the policy loader
  (ADR 0005), asserted by test.

## [Unreleased] — Skill source is not an app write target

### Added

- `skill-authoring` standard: an "App-owned sources" section stating that a root
  under `knowledge/skills/` is the framework's SOURCE and must never be declared
  as an external application's WRITE target (a Maestri `skillBases` entry, an
  editor's skill directory, a sync destination). An app that installs its own
  bundled skills is integrated at the harness level instead.

### Fixed

- Diagnosed the source of flat `knowledge/skills/maestri*` directories appearing in
  the canonical tree: the Maestri canvas declares its `skillBases` as install
  destinations and rewrites its bundled skills into each enabled base on launch.
  One base pointed at this repository's `knowledge/skills/`. The app's own copies
  are not corpus; the corpus stays at 273 knowledge skills and the app keeps its
  skills at its own paths.

## [Unreleased] — Command Code harness

### Added

- `command-code` harness adapter (`harnesses/command-code/harness.json`, shape A)
  plus installer support in `scripts/coacus_install.py`. It mirrors skills to the
  shared `~/.agents/skills/` tree, writes agents to
  `~/.commandcode/agents/<name>.md` with `tools: "*"`, stages the bootstrap script
  as a Python hook (the original shell wrapper was retired by the migration
  above), **merges** the `SessionStart` entry
  into `~/.commandcode/settings.json` (Command Code keeps hooks there, not in a
  `hooks.json`), **merges** `context7` into `~/.commandcode/mcp.json`, and writes
  the Coacus user rules to `~/.commandcode/AGENTS.md` only when that file does not
  already exist. `--uninstall` strips only the merged hook and MCP entries (via
  new `_merge_mcp`/`_strip_mcp` helpers and a generalized merged-config path) and
  keeps the user's other keys.
- Command Code reserved agent names (`explore`, `plan`, `review`, `general`) are
  skipped by the agent renderer, since the harness ignores a custom file with one
  of those names.
- `harnesses/command-code/AGENTS.md`: the Coacus user rules for Command Code
  (inspection auto-approve, phase gating, skill-first + specialist delegation, and
  the advisory concurrency governor), installed to `~/.commandcode/AGENTS.md`.

### Changed

- The concurrency governor is **advisory** for `command-code`: Command Code hooks
  cover only `shell`/`read`/`write`/`edit`, so the `agent` tool cannot be
  intercepted and the cap is documented rather than enforced in-process. Command
  Code subagents cannot spawn subagents, so the main agent is the orchestrator and
  `multi-agent-orchestrator` installs as a coordinator persona.

## [Unreleased] — Agent routing

### Added

- `routing` standard plus the agent routing system: a generated index
  (`.agents/routing.json`) merging each agent's canonical facts with a curated
  bilingual (PT-BR + EN) trigger lexicon (`knowledge/routing/lexicon.json`), and a
  deterministic, offline scorer (`engine/router.py`). Two modes share one source:
  **Mode M** (manual — `--list`, `--agents`, with suggestions on an unknown name)
  and **Mode A** (automated curation — `--top`, `--max-slots`).
- `scripts/coacus_route.py`, the routing CLI. It only PROPOSES; `--max-slots` caps
  the proposal at the governor's free slots, and `--rerank "<command>"` plugs in an
  optional semantic reranker behind the same interface, failing open.
- The orchestrator now routes BEFORE delegating (mandatory step 0), and the
  multi-agent supervision skill carries the same rule. An OPT-IN OpenCode router
  hook (`router-hook.js`, installed with `COACUS_ROUTER_HOOK=1`) injects the
  candidates into the prompt automatically.
- Tests: `test_routing.py` (index/lexicon), `test_router.py` (scorer),
  `test_router_calibration.py` (quality against the real corpus).
- `docs/tutorials/`: three verified walkthroughs — choose agents manually
  (Mode M), choose agents automatically (Mode A, incl. `--rerank` and the opt-in
  hook), and tune the bilingual routing lexicon. Each command's expected output
  is shown, and the tuning example was exercised before writing.

### Changed

- Calibration fixes: diacritics are folded before router trigger matching;
  multi-word triggers match as phrases (``sistema digital`` no longer matches a
  bare ``sistema``); the curated lexicon was enriched for paraphrase
  (``revisar``/``relatório``/``ameaça``).

### Removed

- The opt-in OpenCode router hook (`router-hook.js`, installed with
  `COACUS_ROUTER_HOOK=1`). Routing is user-invoked only
  (`scripts/coacus_route.py`); candidates are never injected into the
  conversation automatically.

## [Unreleased] — Version freshness

### Added

- `version-freshness` normative standard (`docs/standards/version-freshness.md`)
  plus the operational skill (`knowledge/skills/engineering/practices/version-freshness/SKILL.md`):
  a version of a standard, framework, library or regulation is resolved in the
  current session before it is asserted — Context7 for libraries and frameworks,
  the publisher for standards — and pinned with its source and resolution date.
  An unresolved pin is marked `unverified`, never presented as current.
- `engine/validators/freshness.py` (with `tests/test_freshness.py`): flags a
  moving release pin in a canonical artifact with no nearby source anchor or
  resolution marker. It is a **hard gate** (`source_errors`), so the corpus
  cannot regress; fixed document identifiers (RFC/ISO/IEC base/FIPS numbers) are
  not release claims and are not flagged.
- `python3 scripts/coacus.py freshness [--references]`: a read-only, offline
  inventory of every moving pin with its `resolved`/`UNRESOLVED` status, so pin
  age can be audited without a network.
- `provenance.sync_authoring`, called by `generate`: every authored skill,
  workflow and agent gets an idempotent `authoring` provenance entry, closing the
  orphan gap F8 used to report when a file was authored without an importer.
- The standard records the precedence rule: Context7 is the first channel for
  libraries/frameworks but does not guarantee the newest release, so on a
  divergence the **most recent** definition wins, the publisher remains the
  authority for standards, and the divergence is recorded. Context7 stays
  recommended, never required.
- The MASVS reference was rewritten to the current **v2.1.0** (8 control groups,
  24 controls, real upstream control text) and renamed
  `OWASP_MASVS_v2.1_Detailed_Controls.md`; the obsolete v2.0.0 profiles and
  invented controls were removed.
- Freshness guidance in the research agents: a "Documentation Freshness (mandatory)"
  section and a version-provenance line in the response protocol for
  `web-researcher` and `scientific-researcher`; every agent that names a version
  now lists the `version-freshness` skill.
- A "Version Sources" section in the 35 skills that carried a moving release pin:
  each pinned release line is listed with `(verified)` or `(unverified)` and its
  publisher source, resolved 2026-09-20. Fixed document identifiers (RFC numbers,
  ISO/IEC base numbers, FIPS) are not release claims and are not listed. All 61
  entries are `verified`; HL7 v2.x was confirmed as the current 2.9.1 release.
- The Context7 MCP endpoint was exercised over its streamable-HTTP transport
  (`tools/list`, `resolve-library-id`, `query-docs`), confirming it as a working
  library/framework resolution channel; the standard keeps the publisher as the
  authority for standards, where Context7 can lag (its OpenAPI index stops at
  3.1.1 while the publisher publishes 3.2.1).

- `engine/validators/docs.py` (with `tests/test_docs_counts.py`): the README
  corpus table AND the living-documentation prose (`README.md`,
  `CONTRIBUTING.md`, `evals/README.md`, `docs/architecture.md`, `docs/usage.md`,
  `docs/install.md`, `docs/extending.md`, `docs/roadmap.md`,
  `docs/standards/*.md`) are reconciled against the catalog and the lock during
  `validate`, so a stale hand-copied count is a build error. Historical
  paragraphs (`CHANGELOG.md`, `docs/migration.md`, an "as of F6" era) are exempt.
  Volatile counts (the test suite) are no longer stated as fixed numbers — the
  docs give the command to measure them. Corrected the drifted provenance count
  (1233 → 1234).

### Changed

- Corrected version drift verified against publishers this session: PCI DSS
  `v4.0 → v4.0.1`; CycloneDX `1.7 → 1.7.2`; `MASVS v2.1.0`, `NIST SP 800-61r3`,
  `OWASP Kubernetes Top 10 2025` and `ISO/IEC 27701:2025` confirmed and now carry
  their source and resolution date in the agent bodies.
- `using-coacus`, `web-search-specialist` and `academic-scientific-research` now
  require version resolution before a version is stated. The `version-freshness`
  skill is on the agents that cite a version plus the artifact authors
  (`skill-creator`, `documenter`, `code-mapping-specialist`).

## [Unreleased] — Security corpus expansion (19 macro-areas)

### Added

- Security corpus expansion across 19 information-security macro-areas, based on
  parallel web and academic research (3 rounds each; findings recorded in the
  project's `ai-memory` namespace under `research/security-*`). Added **79 new
  skills** and **14 new agents**, and refreshed the `skills:` lists of
  `ai-security-specialist`, `malware-analyst`, `reverse-engineer-agent`,
  `hardware-security-specialist`, `embedded-systems-specialist`,
  `security-specialist`, `iam-specialist`, `pentester-agent` and
  `security-architect`.
- New security agents covering the remaining disciplines: `grc-security-specialist`,
  `cryptography-specialist`, `network-security-specialist`,
  `cloud-security-specialist`, `endpoint-security-specialist`,
  `soc-dfir-specialist`, `threat-intelligence-specialist`,
  `data-security-privacy-specialist`, `mobile-security-specialist`,
  `container-security-specialist`, `game-security-specialist`,
  `ot-security-specialist`, `automotive-security-specialist` and
  `medical-device-security-specialist` (cybersecurity category now covers 22
  disciplines).
- New categories under `knowledge/skills/security/`: `cloud`, `cti` and `data`
  (joining `ai`, `appsec`, `crypto`, `grc`, `iam`, `offensive`, `operations`,
  `platform`, `tooling`).
- `untrusted-content-security`: a prompt-injection trust boundary added to the
  `web-researcher` and `scientific-researcher` agents, which now treat all
  retrieved content as untrusted data.
- Authored (non-imported) artifacts are now recorded in `sources.lock.json` with
  `source_repo: authoring` and `transform: [authored]` so the F8 completeness gate
  can reconcile them, since `sources.lock.json` was previously populated only by
  the import pipeline.

### Changed

- Corrected factual drift in existing skills: TLS 1.3 `RFC 8446 → RFC 9846` and
  PQC hybrid `RFC 10024`; SLSA `v1.2` (L3 is isolated, not hermetic) plus
  CycloneDX `1.7`/ECMA-424 and SPDX `3.0.1`; MASVS `v2.1.0` (8 groups, MASWE);
  OWASP LLM Top 10 `2026` (LLM01–LLM10); CSA CCM `v4.1` and Security Guidance v5;
  SP 800-53 Rel 5.2.0 and OSCAL; OAuth `RFC 9700` and NIST SP 800-63-4;
  ISO/IEC 27701:2025; and translated the Portuguese code-block prose in
  `cryptography-pqc-standards`, `iso-27000-series` and `csa-cloud-security`
  (english-only).
- Expanded previously thin skills: `zero-trust-architecture-engineering` (NIST SP
  800-207/207A, CISA ZTMM, SPIFFE/WIMSE, policy-as-code), `secops-incident-responder`
  (SP 800-61r3, PICERL, evidence, metrics), `malware-analysis-multios` (PE internals,
  unpacking, C2 taxonomy), `hardware-hacking-embedded-security` (secure boot,
  TPM/HSM/TEE/PUF, firmware SBOM) and `security-privacy` (tokenization vs
  pseudonymization, PETs, consent, cross-border transfers, breach notification).

### Fixed

- Reconciled corpus counts in `README.md`, `docs/architecture.md`,
  `docs/roadmap.md` and `docs/install.md` with the measured values
  (272 knowledge skills, 71 agents, 287 catalog skill entries), per the
  "counts are measured, never copied" convention.
- Fixed broken relative links in the new industry, endpoint and identity skills.

## [Unreleased] — F8 (completeness) and docs refresh

### Added

- `coacus_install.py <harness> --verify`: a read-only check that re-derives the
  plan from the install manifest and reports canonical component counts
  (skills, agents, hooks), the install root and any missing/drifted file,
  exiting non-zero on mismatch. Lets an agent answer "is it installed and
  current?" with one command instead of counting directories, which is how a
  concurrent report ended up citing a wrong agent count and two nonexistent
  paths.
- Partial installs in `scripts/coacus_install.py`: `--only <categories>` (matched
  against any path segment under a skill root) and `--skills <globs>`, plus
  `--list` to print the available categories and names. Selection is recorded in
  the `coacus-install.json` manifest, so `--uninstall` stays exact. Useful when a
  harness caps the session-start skills budget (e.g. Codex shortening
  descriptions on a full-corpus install).
- Agent filtering in the installer: `--only` now filters **agents as well as
  skills** (agent categories under `knowledge/agents/`), and a new `--agents
  <globs>` narrows agents by name. `--skills` never narrows agents. The manifest
  records the agent filter, so `--uninstall` and `--verify` stay exact.
- Claude Code and Cursor now install agents. Claude Code writes
  `~/.claude/agents/<name>.md`; Cursor writes `~/.cursor/agents/<name>.md` (both
  with `name`+`description` frontmatter). All five harnesses install agents:
  OpenCode and Cursor flat `<config>/agent(s)/<name>.md`, Antigravity
  `<plugin>/agents/<name>/agent.md`, Codex `<config>/agents/<name>.toml`.
- `_component_counts` distinguishes flat agent files (`<name>.md`) from nested
  ones (`<name>/agent.md`), so `--verify` reports the true agent count for every
  harness instead of collapsing a flat directory to one.
- `engine/validators/agents.py` now enforces D1's canonical omission of `model`:
  a `model` key in an `agent.source.md` fails validation. Harnesses resolve the
  actual model, and the generated `agent.yaml` carries `model: inherit` (already
  asserted in `tests/test_generators.py`). This closes the last self-declared
  "not yet validated" gap in the `AGENTS.md` enforcement paragraph.
- The behavior-eval live runner (`scripts/coacus_eval.py`) now reads each
  harness's non-interactive invocation from `harnesses/<h>/harness.json`
  (`live_cli`) instead of a hardcoded `opencode`-only map, and gains
  `--harness <name>` to override a scenario's target. Live acceptance is now
  possible for OpenCode, Codex (`codex exec`) and Antigravity (`agy --print`) —
  previously only OpenCode. A harness without `live_cli` is reported as
  `NO_RUNNER`. The docstring's promised `--harness` flag, which the code never
  implemented, now exists.
- Two behavior-eval scenarios: `evidence-before-claims` (run the verification
  command before claiming done) and `brainstorm-before-build` (explore intent and
  design before implementation). Both are live-green on OpenCode; the seeded set
  is now six.

### Fixed

- The OpenCode plugin no longer registers the repository's skill roots via
  `config.skills.paths`. Doing so re-registered the whole corpus at runtime and
  bypassed partial installs: measured with `opencode debug skill`, an
  `--only languages` install (19 mirrored skills) still exposed all 208 repo
  skills. OpenCode discovers the mirrored `~/.config/opencode/skills/` tree
  natively, so the registration was both redundant and harmful. The plugin now
  only injects the bootstrap. **[verified locally]**
- Installer hardening (final security audit): path-traversal via an agent
  `name`, JSON corruption/injection when the checkout path has a quote, symlink
  exfiltration from a skill tree, uninstall orphaning files whose source was
  deleted, Codex/Cursor uninstall deleting the other's shared skills, binary
  companion crashes, and tracebacks on a malformed install manifest.
- `agents.validate` flags a misplaced `agent.source.md` (not at
  `knowledge/agents/<cat>/<name>/`), closing a generator/validator/completeness
  divergence; `completeness` reports a malformed lock/catalog instead of
  crashing; the eval runner uses stderr when stdout is empty.
- `--only <unknown>` is now a clear error instead of silently installing only
  the harness files; dead imports/locals removed across `engine/` and `scripts/`.
- Codex and Cursor installs **merge** into an existing `hooks.json` instead of
  overwriting it. The prior behaviour discarded the user's other keys and events,
  contradicting the installer's own "never rewrites a harness config file
  wholesale" contract; `--uninstall` now strips only the Coacus `SessionStart`
  entry and keeps the rest.
- A "Verification — measure, do not infer" section in the entry skill
  (`using-coacus`), propagated to every harness bootstrap: quote a command's
  output for any count, path or status; never extend a path from a sibling and
  never state an unmeasured number.
- `THIRD-PARTY-NOTICES.md` reproducing the MIT license of the Superpowers
  workflow collection by Jesse Vincent, and pointing at the GPL-3.0 license of
  the imported skills corpus. The installer writes it to each harness skills root.
- `scripts/coacus_import.py` resolves `origin_license` from a `licenses` map in
  the import manifest (`GPL-3.0` for `skills`, `MIT` for `superpowers`) and
  `apply` relabels existing entries in place without re-importing content.
- `engine/validators/completeness.py` and `python3 scripts/coacus.py
  completeness`: reconciles the import manifest against the source repositories,
  the target tree, the committed catalog, provenance (no orphan targets) and
  agent skill references; recognises renames and merges. Wired into CI.
- `engine/generators/docstrings.py`: generates `docs/reference/python-api.md`
  from source docstrings, drift-checked like any generated artifact.
- Per-harness installation tutorial (`docs/install.md`) with an evidence class
  per vendor claim, plus a rewritten top-level `README.md`.

### Changed

- Docstring convention applied across the codebase (PEP 257): every public
  module, function, class and public method under `engine/`, `scripts/` and
  `verticals/` now carries a docstring. The generated JavaScript plugins
  (`harnesses/opencode/bootstrap/{coacus.js,governor-gate.js}`) document their
  exported symbols with JSDoc (`@param`/`@returns`), emitted from the generator.
  `tests/test_docstrings.py` enforces the Python side; the three imported
  Superpowers JS/TS files are verbatim MIT copies and stay out of scope.
- `templates/import/import-manifest.json` now resolves source repositories from
  a portable `{workspace}` token (`COACUS_WORKSPACE` override) instead of
  machine absolute paths.
- `engine/validators/hygiene.py` also scans `templates/**/*.json|yaml|yml`,
  closing the D12 blind spot for data files.
- `harnesses/cursor/harness.json` corrected to the documented Cursor hook path
  (`.cursor/hooks.json`, snake_case `additional_context`).
- Documentation count references reconciled (181 tests, six CLIs).
- `docs/roadmap.md` count wording reconciled: it now labels the 193 knowledge
  skills, the 15 process workflows and the 208 catalog skill entries (193 + 15)
  separately, instead of using "skills" for two different totals.

## [F7] — 2026-09-20 — consolidation

### Added

- Final documentation set under `docs/`: `README.md`, `architecture.md`,
  `usage.md`, `extending.md`, `migration.md`, `roadmap.md`.
- `CONTRIBUTING.md` and `CHANGELOG.md`.
- ADR-0017: corpus import with a data-driven manifest and a reorganized
  ten-category taxonomy.

### Changed

- Top-level `README.md` reconciled with the shipped F6 corpus (199 skills, 58
  agents, 15 workflows, 214 catalog entries).

## [F6] — 2026-09-20 — corpus import

### Added

- `scripts/coacus_import.py` and `templates/import/import-manifest.json`: the
  data-driven corpus importer.
- `sources.lock.json`: provenance for 1163 imported files (ADR-0015).
- Ten-category skill taxonomy under `knowledge/skills/`: `data`, `domains`,
  `engineering`, `frameworks`, `infrastructure`, `languages`, `mapping`,
  `platforms`, `roles`, `security`.
- 199 skills, 58 agents, 15 workflows (14 `superpowers-*` plus `using-coacus`)
  and the `context7` MCP.
- `engine/validators/completeness.py`: read-only reconciliation of source repos,
  lock file and catalog (F8 groundwork).
- `verticals/architecture_si/` with the unified ingest and analyze pipelines.

### Changed

- Superpowers workflows namespaced `superpowers-*` under `methodology/workflows/`.
- `containers` → `program-containers`, `github-actions` → `program-github-actions`,
  `markmap` → `program-markmap`, `moodle` → `program-moodle`.
- Agent merges applied: `explore` + `code-researcher` → `code-explorer`.
- `using-superpowers` replaced by the native `using-coacus` entry workflow.

### Fixed

- Hardened imported code against CodeQL/Bandit findings.
- Replaced the HTML conversion fallback with the stdlib `HTMLParser`.

## [F5] — 2026-09-19 — behavior evals

### Added

- `evals/` with four seeded scenarios: `bootstrap-activation`,
  `skill-first-discipline`, `artifact-lifecycle`, `governance-cap-and-toon`.
- `scripts/coacus_eval.py` with the static scenario gate and the opt-in live
  runner (`--judge-cmd`, `--judge-agent`).
- `engine/validators/evals.py`: deterministic scenario validation, part of
  `coacus.py validate`.
- Scheduled/manual static eval workflow `.github/workflows/evals.yml`.

## [F4] — 2026-09-19 — execution governance

### Added

- `engine/governor/ledger.py` and `scripts/coacus_governor.py`: disk-ledger
  concurrency governor with a default cap of 5, rate-limit parking and a lease
  TTL (ADR-0007).
- `engine/toon.py` and `coacus.py toon <file>`: TOON handoff payload validator
  (ADR-0008).
- Generated discovery manifests `.agents/{skills,mcps,agents}.json` and
  `.agents/entries/<name>.json` (ADR-0006).
- OpenCode governor gate plugin rendering.

## [F3] — 2026-09-19 — MCP and SessionStart bootstrap

### Added

- MCP single-source generation: `MCP.md` → `dist/mcp.json` +
  `dist/mcp_config.json` (ADR-0005, amended to Option B).
- Canonical bootstrap body `methodology/bootstrap/session-start.canonical.md`
  and per-harness rendering for shapes A/B/C (ADR-0016).
- `scripts/coacus_install.py` for per-harness installation with dry-run,
  uninstall and config-dir override.

### Changed

- ADR-0005 amended from a hand-authored triple to one source plus generation.

## [F2] — 2026-09-19 — quality gates

### Added

- Tolerant frontmatter parser covering the reference corpus (folded/literal
  scalars, block and inline lists, nested maps).
- `.github/workflows/ci.yml`: `validate` → `check` → tests, never `generate`.
- `secrets` CI job: pinned, checksum-verified gitleaks in directory mode.
- Two-layer testing strategy recorded in ADR-0011.

### Changed

- CI gating wired but never auto-commits generated output.

### Fixed

- Closed P2 findings from the F1 audits.

## [F1] — 2026-09-19 — foundation

### Added

- `engine/frontmatter.py`, the generators (`agent_manifests`, `bootstrap`,
  `catalog`, `discovery`, `mcp_configs`) and the validators (`agents`, `skills`,
  `mcps`, `hygiene`, `discovery`).
- `scripts/coacus.py`: `generate`, `check`, `validate`.
- Deterministic `tests/` suite (stdlib `unittest`, zero dependencies).
- Agent manifest generation from one source (ADR-0002).
- Catalog generated from disk (ADR-0004).

## [F0] — 2026-09-18 — framework charter

### Added

- Repository skeleton and the decision backlog D1–D12 ratified as ADR-0002…
  ADR-0013.
- ADR-0001 language policy (English).
- ADR-0014 committed generated artifacts and ADR-0015 provenance manifest
  placement.
- The core principle: disk is the truth; generation is the contract.
