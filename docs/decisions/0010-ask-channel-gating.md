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
- OpenCode can ask only through the V2 permission `evaluate` hook, so its capability
  cell carries `ask_channel: evaluate`. *(It first needed a second opt-in,
  `COACUS_GUARD_ASK_EXPERIMENTAL=1`, because the path was checked against the documentation
  only. The live check below removed it; the variable is now ignored.)* The guard takes a `--channel` argument
  (`default`, `before`, `evaluate`): on a harness with an `ask_channel` it asks only
  on `evaluate`, defers on `before` (the plugin passes it when the hook is
  registered) and degrades on `default`, so a V1 install never turns an `ask` into
  an allow. The hook may only tighten an effect (deny over ask over allow). Only read and write asks are deferred to the hook,
  because the hook sees a path in a shape the guard cannot know; a command or a
  subagent ask degrades to its fallback, and so does a read or write ask that does
  not hold for every plausible shape of the path (raw, absolute, relative to the
  working directory and its nearest ancestors, and the last component), so a policy
  anchored on one shape such as `sub/*` is not deferred. The path was then run live
  (see the check below).
- Residual risks of the OpenCode path, not removed by that single run: the
  `evaluate` hook may not fire for a tool call (the deferred ask is then an allow), it
  may receive an action name the guard does not map or an empty `resources`, the guard
  may time out inside the hook (the effect is left as it came), and a permission mode
  that approves prompts by itself would turn the ask into an allow. A V1 install, or a
  failed registration, degrades the ask to its fallback instead.
- Live check, OpenCode 2.3.0 on 2026-11-18 (see ADR 0014): with a policy asking on a
  read, the `evaluate` hook fired for the read, received the action `read` with the
  path in `resources`, and the harness enforced the `ask` that the plugin wrote over
  an `allow`. Run in the terminal UI, the harness showed its permission prompt:
  "Allow once" ran the read and "Reject" stopped it. With `--auto` the harness
  approved the same `ask` without a prompt and the read ran, so an `ask` is not a
  barrier in that mode; only a `deny` is. The `shell` and `edit` actions arrived
  under those names. Minimum supported version: OpenCode 2.3.0, the one tested. Earlier
  versions are not supported. The second opt-in was removed after this
  check: `COACUS_GUARD_ASK=1` is enough on OpenCode, and the `--auto` limit above is the
  documented cost, since the hook payload carries no signal for that mode.
- Risks that apply to every harness and are not removed by this record: a guard is a
  hook the agent's own session may be able to edit or disable (the harness settings,
  the plugin, the guard script and the user policy directory are ordinary files);
  tools the guard cannot classify (a tool no table knows; MCP tools have the `mcp` verb since
  ADR 0014) have no verb and so no policy;
  a permission mode that approves prompts by itself can turn a rendered `ask` into an
  allow; and the guard fails open on a crash or timeout, now with a one-line advisory
  on stderr that some harnesses show and some discard. With the opt-in set an `ask` can
  also be raised inside a subagent, which ADR 0002 forbids, because the hook payload
  does not say so. Shipping an enabled deny on the policy and hook paths would break
  the inert default of ADR 0006, so it stays an operator choice.
- The default is unchanged from before: nothing asks. Opting in is an operator
  decision for interactive use.

## Consequences

- No relaxation happens without an opt-in, and no shipped enabled policy uses `ask`.
  One tightening needs no opt-in: an invalid `on_ask_unavailable` used to be rendered
  as `ask` and now denies.
- With the opt-in set, policies on claude-code and antigravity can prompt a
  person, which is a relaxation compared with degrading to deny. The operator owns
  that choice, and the off switches always win.
- The installer warns, on stderr, about every enabled `ask` policy that will degrade
  (the harness cannot ask, or `COACUS_GUARD_ASK=1` is not set), flags a fallback of
  `allow` as failing open, and on a terminal asks whether to continue before it
  writes anything. `--yes` skips the question and a non-interactive run only warns.
  It never refuses, because the degradation is already safe. Two `ask` policies that match the same action no longer
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
