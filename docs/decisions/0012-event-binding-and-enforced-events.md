# ADR 0012: Event binding and enforced events

* **Status**: accepted
* **Date**: 2026-11-18
* **Tags**: guardrails, events, prompt.submit, turn.stop, tool.post

## Context

ADR 0001 makes a guardrail a policy over an action; the event only says when it is
consulted. In code the evaluator ignored the event: a policy written for a tool call
would also fire if the guard were ever bound to a prompt, a tool result or a stop.
Only `tool.pre` has a rendered hook, but the capability matrix lists more events,
and three of its cells disagreed with the vendor documentation.

`prompt.submit` and `turn.stop` are not actions on a resource, and a `block` on a
stop means "keep going", not "deny". They need their own semantics before any hook
is rendered for them.

## Decision

*Amended by ADR 0016 (`prompt.submit` is rendered on Claude Code) and ADR 0018 (`tool.post`
is rendered for a note, and an `output` rule with no event defaults to `tool.post`). The
bullets below describe the first decision.*

- A policy binds one event through its `event` field; a missing field means
  `tool.pre`. The evaluator skips a policy whose event is not the one being decided,
  so adding a new rendered event can never change what an existing policy does.
- A missing event means `tool.pre`. An event value that is not one of the canonical
  ids (a typo, another harness's name, a list, a number) is not skipped: the policy
  applies on every event, so a mistake can never switch a rule off.
- The guard decides, blocks and asks only on `tool.pre`. Any other event gets "no
  opinion" (`{}`, or an explicit allow where the harness requires one). Observe
  events can never deny (`events.json`), and no other gate event is rendered yet.
- Rendering hooks for `tool.post`, `prompt.submit` and `turn.stop` is deferred (ADR 0016
  renders `prompt.submit` on Claude Code only). It
  needs, per harness, a verified payload shape and a native hook name field in the
  capability data, and it should render only when an enabled policy binds the event,
  so that no process starts for nothing. `prompt.submit` and `turn.stop` also need
  verbs and a meaning for a stop block, which amends ADR 0001 and is a later record.
- Three capability cells were corrected against the vendor documentation of
  2026-11-18: claude-code `prompt.submit` cannot ask (it can only block), codex
  `prompt.submit` can block, and cursor `turn.stop` cannot block (it only adds a
  follow-up message). A test requires that no event other than `tool.pre` may ask.

## Consequences

- Nothing changes for installed policies: they were all `tool.pre`.
- Writing a policy for another event is now accepted and inert until a hook is
  rendered for it, which is the safe default.
- The remaining work is one branch per harness with its verified payload shape.

## Alternatives considered

- Render every event now: the payload shapes are not verified for every harness and
  every rendered hook costs a process per event, so rejected.
- Leave the evaluator event-blind: a future binding would silently widen every rule,
  so rejected.
