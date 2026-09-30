# Harness Lifecycle Capability Matrix

> GENERATED from `harnesses/*/harness.json` and `methodology/lifecycle/events.json` by `scripts/coacus.py generate` — do not edit.

Each cell is `support / can_block / effect / evidence`. A harness without
a `lifecycle` block is a closed capability (no events, nothing installable).

| Event | Class | antigravity | claude-code | codex | command-code | cursor | opencode |
|---|---|---|---|---|---|---|---|
| `tool.pre` | gate | gate / B / decision / documented | gate / B / permissionDecision / documented | gate / B / permissionDecision / documented | gate / B / permissionDecision / documented | gate / B / permission / documented | gate / B / throw / documented |
| `prompt.submit` | gate | unsupported | gate / B / additionalContext / documented | gate / - / additionalContext / documented | unsupported | gate / B / continue / documented | unsupported |
| `turn.stop` | gate | gate / B / decision / documented | gate / B / decision / documented | gate / B / decision / documented | gate / B / decision / documented | gate / B / followup_message / documented | none / - / - / documented |
| `tool.post` | observe | observe / - / none / documented | observe / - / additionalContext / documented | observe / - / additionalContext / documented | observe / - / decision / documented | observe / - / additional_context / documented | observe / - / metadata / documented |
| `tool.failure` | observe | unsupported | observe / - / additionalContext / documented | observe / - / additionalContext / documented | observe / - / decision / documented | observe / - / additional_context / documented | unsupported |
| `session.start` | lifecycle | none / - / - / documented | lifecycle / - / additionalContext / documented | lifecycle / - / additionalContext / documented | lifecycle / - / additionalContext / documented | lifecycle / - / additional_context / documented | lifecycle / - / transform / documented |
| `session.end` | lifecycle | unsupported | lifecycle / - / advisory / documented | lifecycle / - / advisory / documented | unsupported | lifecycle / - / advisory / documented | none / - / - / documented |
| `context.precompact` | lifecycle | unsupported | lifecycle / B / decision / documented | lifecycle / - / observe / documented | unsupported | lifecycle / - / observe / documented | lifecycle / - / context / documented |
| `subagent.start` | lifecycle | unsupported | lifecycle / - / additionalContext / documented | lifecycle / - / additionalContext / documented | unsupported | lifecycle / B / permission / documented | gate / B / throw / documented |
| `subagent.stop` | lifecycle | unsupported | lifecycle / B / decision / documented | lifecycle / B / decision / documented | unsupported | lifecycle / - / advisory / documented | unsupported |

## Declared gaps

- **antigravity** `session.start` — unsupported: Antigravity has no SessionStart event; only an always_on rule
- **antigravity** `session.end` — unsupported: no session-end event
- **antigravity** `subagent.start` — emulate: only via PreToolUse on the spawn tool
- **codex** `session.end` — advisory: SessionEnd is advisory on Codex; it cannot block
- **codex** `tool.pre` — trust-gate: Codex refuses to run an untrusted hook until the operator approves it
- **command-code** `session.start` — never-blocks: SessionStart is non-blocking by design on Command Code
- **command-code** `session.end` — unsupported: no SessionEnd hook
- **command-code** `subagent.start` — unsupported: the agent tool cannot be intercepted by a hook
- **command-code** `tool.pre` — plan-mode-skip: hooks are skipped entirely in plan mode
- **cursor** `tool.pre` — unverified: project vs user hooks.json precedence is unverified; a user-scope deny must be probed before trust
