# ADR 0020: A stop rule for `turn.stop`, and the prompt hook on Codex

* **Status**: accepted
* **Date**: 2026-11-19
* **Tags**: guardrails, hooks, claude-code, codex

## Context

ADR 0016 and ADR 0018 left two things open: `turn.stop`, because a block there means "keep
going" and an unconditional rule could hold the agent forever, and Codex, which documents the
same events but was not run. Both vendors document the Stop hook the same way
(https://code.claude.com/docs/en/hooks and https://learn.chatgpt.com/docs/hooks, resolved
2026-11-19): the payload carries `stop_hook_active` and `last_assistant_message`, and
`{"decision": "block", "reason": "..."}` makes the agent continue with the reason as its
next instruction. Claude Code also ends the turn after eight consecutive stop-hook
continuations. Codex documents the prompt hook with the same answer, and skips a hook until
it is trusted (`/hooks`, or `--dangerously-bypass-hook-trust` for one run).

## Decision

- A new verb `stop`, bound to `turn.stop` (it defaults there), matched case-insensitively
  against the end of `last_assistant_message`. `deny` renders the block answer; `ask` has no
  human to reach and degrades to its fallback; `note` and `allow` render nothing.
- The guard allows whenever `stop_hook_active` is true, so a rule asks at most once per
  turn, whatever its pattern.
- Claude Code and Codex gain the `Stop` hook, and Codex gains `UserPromptSubmit`, both added
  at install time only while an enabled policy binds the event, through the isolated,
  missing-script-tolerant launcher. Codex gets the prompt answer without the Claude-only
  `suppressOriginalPrompt` field.
- Codex `tool.post` stays out: its documented example pairs `additionalContext` with a
  block that replaces the tool result, and a context-only answer is not documented.

## Consequences

- Run live on Codex 0.169.0 (2026-11-19, isolated `CODEX_HOME`, `--dangerously-bypass-hook-trust`,
  no login): an installed `UserPromptSubmit` hook received the prompt in `prompt` and its block
  answer stopped the prompt. The Stop hook needs a finished model turn and was not run
  live on either harness; it follows the documentation. The capability data says which.
- A hook the user has not trusted does nothing on Codex. The installer cannot trust it: the
  hash behind `trusted_hash` is not documented.
- A `stop` rule keeps a tired agent working once, which can spend tokens. The pattern is the
  only filter, so a catch-all `*` should carry a message that asks for something checkable.
- Enabling or disabling a policy takes effect at the next install.

## Alternatives considered

- Block as long as the pattern matches: the vendor cap would end the turn after eight
  rounds and the user would see a loop.
- Match the whole transcript: it is not in the payload, and reading the file is another
  surface to protect.
