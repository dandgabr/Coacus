# ADR 0015: Guard self-protection

* **Status**: accepted
* **Date**: 2026-11-18
* **Tags**: guardrails, tamper, installer

## Context

The guard runs inside the agent's session and the agent has write tools, so a session
(or text injected into it) can switch the guard off by editing a file rather than by
dodging a rule: the user policy files, the installed guard script and evaluator, and each
harness's hook configuration. Measured before this record: no shipped policy protected
any of those paths.

## Decision

- Coacus ships `methodology/lifecycle/policies/self-protection.policy.json`: `deny` rules
  on the `write` verb for the policy directories, `scripts/coacus_guard.py`,
  `engine/guardrail/`, and the hook files of Claude Code, Codex, OpenCode, Cursor and
  Antigravity. It is disabled, like every shipped policy (ADR 0006).
- The installer takes `--self-protection on|off|prompt`. The default is `prompt` on an
  interactive terminal, where the default answer is No, and `off` otherwise. So installing
  never turns it on silently. When chosen, the installer writes an enabled, machine-local
  copy into the user policy directory, adds a rule for the policy directory actually in use
  (a custom `COACUS_POLICY_DIR` or `--browser-policy-dir`), and checks it renders on every
  target harness like any generated policy. A full `uninstall all` removes the copy it
  wrote and never a hand-written file of the same name; `--verify` reports its status.
- Every denial message tells the person how to release a legitimate edit: make it in their
  own terminal (the guard governs the agent's tools, not the person's shell), or set
  `"enabled": false` in the installed policy, edit, and turn it back on. The agent cannot
  do this itself, because the policy file is one of the protected paths.

## Consequences

- This is a speed bump and a tripwire, not a sandbox. A write through the shell (`sed -i`,
  a redirection, `tee`) is an `exec` action, not a `write`, and is not covered; command
  rules over editing programs are easy to evade (ADR 0011). On a harness that approves
  automatically the `deny` still holds, because the rule is a `deny`.
- It blocks legitimate edits of those paths made by the agent, including edits to Coacus
  itself in a session working on this repository. That is why it is opt-in.
- The only real fix is isolation outside the session: a sandbox, read-only files, or the
  harness's managed settings. The standard says so next to the rule.

## Alternatives considered

- Documentation only: leaves the easy mistake unmarked.
- A manifest of hashes checked at `--verify`: detects an edit after the fact, but needs a
  new manifest in the installer. Deferred.
- Blocking editing commands in the shell: the item 1 problem again, with false positives.
