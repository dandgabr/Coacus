# ADR 0014: MCP action verb

* **Status**: accepted
* **Date**: 2026-11-18
* **Tags**: guardrails, mcp, actions

## Context

The guard turns a tool call into a verb and a resource by tool name. Names it does not
know became the empty verb, which no policy matches, so a tool served by an MCP server
(`mcp__playwright__browser_navigate`, `mcp__rea__push_adb_file`) was never constrained:
a `network` rule did not see a navigation and a `write` rule did not see a pushed file.
The guard cannot know what an arbitrary MCP tool does, so mapping each one to `read`,
`write` or `network` would claim coverage it does not have.

## Decision

- ADR 0001's vocabulary gains the verb `mcp`. Its resource is the tool name, and the
  guard classifies a call as `mcp` when the name starts with `mcp_` (which covers Claude
  Code and Codex `mcp__` and Antigravity `mcp_`) or `mcp:` (Cursor), and, on OpenCode, when
  it is outside that harness's native tool list. Arguments are not inspected: they have no shared shape.
- A policy on `mcp` names the tool it constrains, for example `mcp__playwright__*`.
  Matching is case-insensitive on both sides, because a tool name is an identifier and
  a harness may send it in either case. An operator writes the rule; Coacus ships none,
  so the default stays inert (ADR 0006).
- `ask` on an `mcp` action follows ADR 0010 like any non-file verb: OpenCode cannot
  defer it, so the policy's `on_ask_unavailable` applies.

## Consequences

- Claude Code documents `mcp__<server>__<tool>` for its PreToolUse hook, and Cursor
  documents `MCP:<tool>` for HTTP MCP servers. Codex 0.169.0 was run live (2026-11-18,
  isolated `CODEX_HOME`): the hook fires for an MCP tool as `mcp__<server>__<tool>` and a
  deny from the guard blocked it. Antigravity is a `unverified` gap: a live
  run was not possible. Its documentation
  names MCP tools `mcp_<server>_<tool>`, which the `mcp_` prefix now classifies, but that
  is unproven.
- OpenCode was run live (2.3.0, 2026-11-18, isolated project, stub MCP server). An MCP
  tool reaches both hooks as `<server>_<tool>` (`probe_echo`), not `mcp__...`. The guard
  therefore decides native or MCP on OpenCode by an exact list of its own tool names
  (`OPENCODE_NATIVE` in `scripts/coacus_guard.py`), never by the shared tables: a server
  named `web` serving `fetch` arrives as `web_fetch`, which the shared tables would call a
  network tool and skip every `mcp` rule. Every name outside that list is an `mcp` action
  named by the raw tool name, except a few native tools with no verb (`todowrite`, `skill`,
  `question`, `lsp`, `batch`), which stay unclassified so a broad `mcp` rule does not
  block them; `lsp` and `skill` can read files and no `read` rule sees them. A rule such as
  `probe_*` denied the stub, including a call made from inside the `execute` code tool
  (the nested call is guarded on its own). The `execute` call itself carries code, not a
  command, so it is both an `exec` action with no command and an `mcp` action named
  `execute`, and a rule can deny it by that name. The installed tool description says
  that code can also call `fetch` directly, which no hook sees, so a `network` rule is
  not a barrier against code run through `execute`; deny `execute` when that matters.
  Native names there are `read`, `write` and `shell`, and `edit` as a permission name.
- A plugin whose `id` equals that of an already installed plugin is skipped without a
  message: a project copy of `coacus-guardrails` never loaded beside the global one
  until the `id` changed. Install one copy of the guard per harness.
- An MCP tool with no `mcp` rule is still unconstrained, and a tool whose name the
  guard does not recognise (a harness that prefixes it differently) is too. A rule on
  what an MCP tool does inside (a URL or a path in its arguments) is not possible here.
- For a hard block of a browser or other MCP server, remove it from the harness
  configuration; the policy is a second layer.

## Alternatives considered

- Map known MCP tools to the existing verbs: rejected, the table would need constant
  upkeep and a wrong entry reads as coverage.
- Deny every unclassified tool: rejected, it breaks all MCP use.
