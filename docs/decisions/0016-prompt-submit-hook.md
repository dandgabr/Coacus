# ADR 0016: Prompt-submit hook on Claude Code

* **Status**: accepted
* **Date**: 2026-11-18
* **Tags**: guardrails, events, prompt.submit, claude-code

## Context

ADR 0012 deferred rendering a hook for any event except `tool.pre`, because each
harness needs a verified payload shape, a native hook name in the capability data, and
a rule that no process starts for nothing. `prompt.submit` is the one gate event whose
meaning is clear: block the prompt, or let it through. Claude Code documents it
(https://code.claude.com/docs/en/hooks, resolved 2026-11-18): the stdin JSON carries
the text in `prompt`, `{"decision": "block", "reason": "..."}` stops the prompt and
shows the reason to the user, and the event takes no matcher. `turn.stop` and
`tool.post` stay deferred: a stop block means "keep going", and an observe event cannot
deny, so neither is a rule a policy can express with today's verbs.

## Decision

- A new verb, `prompt`, whose resource is a pattern over the text of the submitted
  prompt, compared case-insensitively (a prompt is prose). It is meaningful only on
  `prompt.submit`; a policy with another verb bound to that event, or a `prompt` policy
  bound to `tool.pre`, never fires, because the guard decides one event at a time
  (ADR 0012).
- The capability data names the native hook: `native` (and `payload`) on the event
  entry in `harnesses/<harness>/harness.json`. Only `claude-code` `prompt.submit` has it
  today. A harness without it gets no hook and answers "no opinion".
- The hook is rendered by the installer, not by `generate`, and only while an enabled
  policy (repository, user directory or generated this run) binds the event. The
  installer adds the entry to the guard fragment with the `tool.pre` command and the
  event swapped. When no policy binds it the entry is added empty, so a re-install
  removes a hook an earlier run left, and the merge no longer leaves an empty event
  array in a user's settings.
- A block answers `{"decision": "block", "reason": <policy message>}`; a policy with no
  message gets a generic reason. A prompt is never asked about: no channel reaches a
  person from this hook, so an `ask` degrades to its `on_ask_unavailable` (deny blocks,
  allow lets the prompt through), as on every harness that cannot ask.
- The size cap of the evaluator holds: a prompt over 100,000 characters matches every
  `prompt` rule and is blocked by a deny rule, as an oversize value is for every verb.

## Consequences

- Nothing changes for an installed policy: they were all `tool.pre`, no shipped policy
  binds `prompt.submit`, and the generated `guardrail-hooks.json` files are unchanged.
- A prompt rule is only as good as its pattern. It reads the text the user typed after
  the harness expanded nothing: attachments, pasted files read later by a tool and text
  the model produces are not prompts. It is a tripwire for pasting a secret, not DLP.
- A deny policy bound to `prompt.submit` on a harness with no native hook still installs
  and is inert there, as ADR 0012 accepted; the installer does not refuse it.
- Another harness needs its own verified payload and a `native` name; Codex documents a
  similar event but it was not run live, so it stays out.
- `turn.stop` (a block keeps the agent going) and `tool.post` (observe only) need verbs
  and semantics and are still deferred, with the rest of ADR 0012's list.

## Alternatives considered

- Render the hook always: one process per prompt for nothing, rejected.
- Render it in `generate`: shipped policies are all disabled, so it would never render,
  and enabling a user policy would then need a regeneration, rejected.
- Treat a prompt as a `read` or `exec` resource: mixes prose with paths and commands and
  the case rule, rejected.
