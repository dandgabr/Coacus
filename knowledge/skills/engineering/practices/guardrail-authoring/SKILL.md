---
name: guardrail-authoring
description: Use when adding a guardrail policy or an advisory content rule, to keep the rule precise, tested, and fail-open.
---

# Guardrail authoring

A guardrail is authored once and rendered natively (PAER). Keep it precise,
tested and fail-open. See the `lifecycle-guardrails` standard for the model.

## Rules are data

- A **policy** constrains an ACTION (`verb` + `resource`); the event only binds
  *when* it runs. Author it under the lifecycle policies directory, disabled by
  default: installing the framework never changes a session without an opt-in.
- An **advisory content rule** is `field x operator x pattern`, all conditions
  AND-combined. Author it in the security-pattern catalogue; a match produces an
  advisory, never a deny.

## Precision

- Give a rule at least one condition. A rule with no condition can never match.
- Test the pattern before shipping: run it against a known-good and a known-bad
  sample, and read the match count.
- Avoid over-broad patterns — `log` matches login, dialog and catalog. Anchor the
  pattern and use word boundaries.
- Prefer an unquoted pattern: quoting changes backslash handling.
- Attach the **mitigation** to the message, not just the alert. A warning with no
  fix trains the reader to ignore it.

## Failure

- Fail-open at the rule layer: no match is allow, and a non-compiling pattern does
  not match (and is a lint error).
- Separate the failure domains: a decision failure versus a mechanism failure. A
  broken hook must not deny every call.

## Ladder and hygiene

- **Ladder.** Layer defenses: a deterministic pattern, then a single-turn review,
  then a cross-file review. Each layer is independently switchable, and a deferred
  review may run in the background and wake the agent with its findings rather
  than blocking the turn.
- **Frozen ids.** Rule ids are frozen and append-only: add a new id, never
  renumber. An id that disappears is a build error, not a silent shift.
- **Inline suppression.** Provide a convention for recording a reviewed, safe
  case inline (for example a `safe because` comment) so a false positive can be
  silenced without disabling the whole layer.
- **Prompt budget.** When layered rule files concatenate under a size cap,
  document the truncation order: drop the tail first, so user-wide rules survive
  and the most local are lost.

## Conservative Tool & Missing-CLI Fallback Policy

When an autonomous agent encounters a missing CLI binary or tool failure:

- **Policy Modes (`disabled | observe | enforce`)**: Default to `observe` during development and `enforce` in production.
- **Strict Disallow Rules**: Prohibit blind auto-installation of missing tools. Specifically ban:
  - `curl_pipe_shell` (`curl ... | sh` / `bash`)
  - `wget_pipe_shell` (`wget -O- ... | sh`)
  - `untrusted_repository` (adding random third-party PPAs or unverified git URLs)
  - `model_generated_unverified_command` (executing hallucinated multi-line install scripts without user gating).
- **Fallback Result Transparency**: When a fallback mechanism or alternative tool is used, the report must preserve the primary tool's failure log alongside the fallback outcome, preventing silent degradation.

## Agent Workspace Permission Surface & Supply-Chain Auditing

Autonomous AI developer environments define their execution authority through workspace configuration, frontmatter tool grants, hooks, and ignore files. Author guardrails to enforce strict mechanical boundaries across this surface:

### 1. 3-Tier Permission Surface Model (`allow` / `ask` / `deny`)

1. **`ask` on the permission surface itself:** Any operation targeting files or actions that define the agent's own authorization boundary must require human gating (`ask`). An agent must never be permitted to unilaterally widen its own permissions. This includes:
   - Agent harness settings (`.claude/settings.json`, `.gemini/settings.json`, `.cursor/rules`, etc.).
   - Skill manifests (`SKILL.md`) carrying `allowed-tools` declarations.
   - CI/CD workflow configurations (`.github/workflows/**`, Azure pipeline definitions).
   - Security guard scripts and linter configurations.
   - Remote write actions (`git push`).
2. **`deny` tripwires for exfiltration and credential theft:** Enforce non-bypassable `deny` rules on patterns commonly used to siphon data or steal secrets:
   - Outbound HTTP data transmission flags: `curl -d`, `curl -F`, `curl -T`, `curl --data*`, `curl --upload-file`, `curl -X POST`, `wget --post*`, `scp`, `ssh`, `nc`.
   - Private key and sensitive credential paths: `.env`, `.env.*` (excluding `.env.example`), `~/.ssh/**`, `~/.aws/**`, `~/.gnupg/**`, `id_rsa`, `*.pem`, `*.key`.

### 2. Hook Allowlisting & Automated Execution Defense

Repository lifecycle hooks (`SessionStart`, `PreToolUse`, `PostToolUse`) execute automatically upon opening or interacting with a workspace without requiring a user prompt.
- Enforce an explicit, audited allowlist (`ALLOWED_HOOKS`) of verified hook scripts.
- Disallow unvetted hooks or dynamically generated hook definitions that could execute arbitrary commands upon repository cloning or branch checkout.

### 3. Skill Frontmatter and Subagent Tool-Grant Hygiene

- **Disallow wildcard globs in tool grants:** Reject frontmatter granting command patterns containing unanchored wildcards (e.g. `Bash(*)` or `Bash(curl *)`). Commands must use explicit subcommands and pinned arguments.
- **Explicit `tools:` list on untrusted-content subagents:** Subagents handling external untrusted data (scrapers, evaluators, parsers) must explicitly list allowed tools. Never leave `tools:` empty or omitted if the harness defaults to granting all parent tools (`Edit`, `Write`, `Bash`, `Agent`).
- **Granularity resolution traps:** Beware of harnessing engines where subagent `tools:` accepts tool names but ignores argument constraints (e.g. interpreting `Bash(ls *)` as full unconstrained `Bash`). Flag and prevent such misconfigurations.

### 4. Order-Sensitive `.gitignore` Negation & Package Lifecycle Script Bans

- **Negation allowlist in `.gitignore`:** In ignore configurations that exclude PII or credential folders, audit all `!<pattern>` unignore directives against an approved list (`ALLOWED_IGNORE_NEGATIONS`). A late negation in an ignore file can silently un-ignore and expose previously protected files.
- **Lifecycle script ban in development toolchains:** For supplementary tools or workspace scripts defining a `package.json`, explicitly disallow execution of arbitrary install hooks: `preinstall`, `install`, `postinstall`, `prepare`, `prepack`, and runtime `trustedDependencies`. Package installations in agent workspaces must be pure dependency unpacks without arbitrary shell execution.
