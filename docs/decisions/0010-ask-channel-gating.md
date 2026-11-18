# ADR 0010: Ask channel gating

* **Status**: accepted
* **Date**: 2026-11-17
* **Tags**: guardrails, ask, headless, degradation

## Context

ADR 0002 makes `ask` valid only where a harness exposes a human channel (`can_ask`),
forbids it in headless runs and inside subagent scope, and says it degrades by the
policy's `on_ask_unavailable`. The runtime guard did not implement the capability
check: it turned every `ask` into the policy fallback on every harness, so a policy
could never prompt a person even where the harness supports it.

A hook payload carries no signal that identifies a headless or subagent run, so the
guard cannot tell whether a person is present. Rendering `ask` by default would
reopen the headless hole that ADR 0002 rejected, and it would change what an
existing enabled `ask` policy does, which ADR 0006 says must never happen without an
opt-in.

## Decision

- The guard renders a native `ask` only when all of these hold: the operator set
  `COACUS_GUARD_ASK=1`, neither `COACUS_GUARD_NO_ASK` nor `CI` is set to a truthy
  value (anything except empty, `0`, `false`, `no` or `off`; other CI markers such
  as `GITHUB_ACTIONS` are not checked), the event is `tool.pre`, the harness name is
  a plain lowercase word, and `harnesses/<harness>/harness.json` declares both
  `can_ask` and `can_block` as exactly `true` for the event.
- In every other case, and on any error while reading capability data, `ask`
  degrades to the policy's `on_ask_unavailable`. An absent or invalid value there
  fails closed to `deny`. The degraded `deny` is enforced through the deny render the guard
  has for each harness, including OpenCode (see Consequences).
- The default is unchanged from before: nothing asks. Opting in is an operator
  decision for interactive use.

## Consequences

- No relaxation happens without an opt-in, and no shipped enabled policy uses `ask`.
  One tightening needs no opt-in: an invalid `on_ask_unavailable` used to be rendered
  as `ask` and now denies.
- With the opt-in set, policies on claude-code and antigravity can prompt a
  person, which is a relaxation compared with degrading to deny. The operator owns
  that choice, and the off switches always win.
- Known gaps, tracked separately: the installer does not refuse an `ask` policy on
  a harness that cannot ask. Two `ask` policies that match the same action no longer
  depend on file order: the strictest `on_ask_unavailable` wins (`deny` beats `allow`,
  and a missing or invalid value counts as `deny`). On OpenCode the guard now renders
  a `deny`, so a policy blocks a tool call there.
- Cursor was checked against its hooks documentation on 2026-11-18: the `preToolUse`
  output says `"ask"` is accepted by the schema but not enforced today, so its
  `can_ask` cell is `false` and an `ask` there degrades like on any other harness
  without a channel.

## Alternatives considered

1. **Render `ask` whenever the harness can ask**: simple, but it reopens the headless
   hole of ADR 0002 and changes enabled policies silently — rejected.
2. **Detect headless or subagent runs from the payload**: no repository evidence that
   any harness sends such a field — rejected until evidence exists.
3. **An installer flag baked into the hook command**: a cleaner signal for
   interactive installs, but it needs generator and installer changes — deferred.
