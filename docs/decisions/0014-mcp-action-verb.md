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
  guard classifies a call as `mcp` when the name starts with `mcp__` (Claude Code) or
  `mcp:` (Cursor). Arguments are not inspected: they have no shared shape.
- A policy on `mcp` names the tool it constrains, for example `mcp__playwright__*`.
  Matching is case-insensitive on both sides, because a tool name is an identifier and
  a harness may send it in either case. An operator writes the rule; Coacus ships none,
  so the default stays inert (ADR 0006).
- `ask` on an `mcp` action follows ADR 0010 like any non-file verb: OpenCode cannot
  defer it, so the policy's `on_ask_unavailable` applies.

## Consequences

- Claude Code documents `mcp__<server>__<tool>` for its PreToolUse hook, and Cursor
  documents `MCP:<tool>` for HTTP MCP servers. Codex, OpenCode and Antigravity are
  recorded as `unverified` gaps in their `harness.json`: the pages read do not say
  whether the hook fires for MCP tools, so a rule may never run there.
- An MCP tool with no `mcp` rule is still unconstrained, and a tool whose name the
  guard does not recognise (a harness that prefixes it differently) is too. A rule on
  what an MCP tool does inside (a URL or a path in its arguments) is not possible here.
- For a hard block of a browser or other MCP server, remove it from the harness
  configuration; the policy is a second layer.

## Alternatives considered

- Map known MCP tools to the existing verbs: rejected, the table would need constant
  upkeep and a wrong entry reads as coverage.
- Deny every unclassified tool: rejected, it breaks all MCP use.
