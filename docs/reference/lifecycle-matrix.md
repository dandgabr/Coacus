# Harness Lifecycle Capability Matrix

> GENERATED from `harnesses/*/harness.json` and `methodology/lifecycle/events.json` by `scripts/coacus.py generate` — do not edit.

Each cell is `support / can_block / effect / evidence`. A harness without
a `lifecycle` block is a closed capability (no events, nothing installable).

| Event | Class | antigravity | claude-code | codex | command-code | cursor | opencode |
|---|---|---|---|---|---|---|---|
| `tool.pre` | gate | gate / B / decision / documented | gate / B / permissionDecision / documented | gate / B / permissionDecision / documented | gate / B / permissionDecision / documented | gate / B / permission / documented | gate / B / throw / documented |
| `prompt.submit` | gate | unsupported | gate / B / additionalContext / documented | gate / B / additionalContext / documented | unsupported | gate / B / continue / documented | unsupported |
| `turn.stop` | gate | gate / B / decision / documented | gate / B / decision / documented | gate / B / decision / documented | gate / B / decision / documented | gate / - / followup_message / documented | none / - / - / documented |
| `tool.post` | observe | observe / - / none / documented | observe / - / additionalContext / documented | observe / - / additionalContext / documented | observe / - / decision / documented | observe / - / additional_context / documented | observe / - / metadata / documented |
| `tool.failure` | observe | unsupported | observe / - / additionalContext / documented | observe / - / additionalContext / documented | observe / - / decision / documented | observe / - / additional_context / documented | unsupported |
| `session.start` | lifecycle | none / - / - / documented | lifecycle / - / additionalContext / documented | lifecycle / - / additionalContext / documented | lifecycle / - / additionalContext / documented | lifecycle / - / additional_context / documented | lifecycle / - / transform / documented |
| `session.end` | lifecycle | unsupported | lifecycle / - / advisory / documented | lifecycle / - / advisory / documented | unsupported | lifecycle / - / advisory / documented | none / - / - / documented |
| `context.precompact` | lifecycle | unsupported | lifecycle / B / decision / documented | lifecycle / - / observe / documented | unsupported | lifecycle / - / observe / documented | lifecycle / - / context / documented |
| `subagent.start` | lifecycle | unsupported | lifecycle / - / additionalContext / documented | lifecycle / - / additionalContext / documented | unsupported | lifecycle / B / permission / documented | gate / B / throw / documented |
| `subagent.stop` | lifecycle | unsupported | lifecycle / B / decision / documented | lifecycle / B / decision / documented | unsupported | lifecycle / - / advisory / documented | unsupported |

## Declared gaps

- **antigravity** `tool.pre` — unverified: the hooks page does not say whether PreToolUse receives MCP tools or under what name (the MCP page names them mcp_<server>_<tool>, which the guard does not match); an mcp rule may never run here
- **antigravity** `session.start` — unsupported: Antigravity has no SessionStart event; only an always_on rule
- **antigravity** `session.end` — unsupported: no session-end event
- **antigravity** `subagent.start` — emulate: only via PreToolUse on the spawn tool
- **codex** `tool.pre` — unverified: whether PreToolUse fires for MCP tools, and under what name, is not stated in the pages read; an mcp rule may never run here
- **codex** `session.end` — advisory: SessionEnd is advisory on Codex; it cannot block
- **codex** `tool.pre` — trust-gate: Codex refuses to run an untrusted hook until the operator approves it
- **command-code** `session.start` — never-blocks: SessionStart is non-blocking by design on Command Code
- **command-code** `session.end` — unsupported: no SessionEnd hook
- **command-code** `subagent.start` — unsupported: the agent tool cannot be intercepted by a hook
- **command-code** `tool.pre` — plan-mode-skip: hooks are skipped entirely in plan mode
- **cursor** `tool.pre` — unverified: preToolUse is documented to fire for HTTP MCP servers with the name MCP:<tool>; stdio MCP servers are not stated
- **cursor** `tool.pre` — unverified: project vs user hooks.json precedence is unverified; a user-scope deny must be probed before trust
- **opencode** `tool.pre` — unverified: whether tool.execute.before runs for MCP tools, and under what name, is not documented in the pages read; an mcp rule may never run here
- **opencode** `tool.pre` — unverified: ask works only through the V2 permission evaluate hook; its event shape, the permission names it receives and its order against tool.execute.before are documented but not verified by a live V2 run
