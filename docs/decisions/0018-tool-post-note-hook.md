# ADR 0018: Note policies on tool output (`tool.post`)

* **Status**: accepted
* **Date**: 2026-11-18
* **Tags**: guardrails, hooks, claude-code

## Context

Only `tool.pre` and `prompt.submit` had a rendered hook. `tool.post` was documented in the
capability matrix but nothing read it. A tool result is also where injected instructions
arrive (a web page, a file, an MCP reply), so a way to flag a result has a use. Claude Code
documents `PostToolUse` with `tool_name`, `tool_input` and `tool_response` on stdin, and
`hookSpecificOutput.additionalContext` to put text next to the result (cut to a file preview
above 10,000 characters). Its `decision: "block"` only adds the reason after a tool that
has already run.

## Decision

- A new verb `output`, bound to `tool.post`, matched case-insensitively with the same fold
  as `prompt`.
- Only the decision `note` is rendered, as `additionalContext`. `note` ranks below `allow`
  in `evaluate`, so `engine.guardrail.evaluate.notes` reads the matching notes directly and
  `evaluate` is unchanged. A `deny` or `ask` on `tool.post` is refused at install by the
  existing `can_block` check, and a runtime guard that meets one still only adds the note.
- The installer adds the `PostToolUse` hook only while an enabled policy binds the event,
  like `UserPromptSubmit`, through the same launcher that skips a missing guard script.
- `turn.stop` stays deferred: a block there means "keep going" and needs a loop limit.

## Consequences

- The note is advice to the model that read the output; a model that was already steered
  by that output may ignore it. It is a tripwire, not a control.
- The shape of `tool_response` is documented only for Bash. Other tools are scanned as JSON
  text, so a pattern can match a key name, and a long response keeps only its head and tail.
- Hook output is the policy author's text. Matching text from the tool is never copied into
  the note.
- Not run live: the payload and the answer come from the vendor documentation, as for
  ADR 0016. Codex documents `PostToolUse` too but needs hook trust through `/hooks`, so it
  stays out until it can be tested.

## Alternatives

- Let `note` surface through `evaluate`: it would change the composition law that every
  caller relies on.
- Render `decision: "block"` for `deny`: the tool already ran, so it would look like
  enforcement and enforce nothing.
