# ADR 0001: Guardrails are policies over actions, not events

* **Status**: accepted
* **Date**: 2026-09-30
* **Tags**: architecture, guardrails, portability

## Context

The framework renders one canonical artifact into six harnesses. A guardrail
must be authored once and enforced everywhere it can be. The first design
canonicalized the lifecycle EVENT (`session.start`, `tool.pre`, ...) and left the
policy — what is actually permitted — to be re-authored inside each harness's
native hook. That puts the authored judgment in the least portable layer and
leaves the shared layer (the event name) carrying no semantics, so single-source
has nothing to verify.

## Decision

Adopt **PAER**: Policy over Action, Event binding, Rendering effect.

- The portable subject is an ACTION: `verb` (`exec`, `read`, `write`, `network`,
  `spawn`, `delegate`) plus a normalized `resource`.
- Policies are authored once under `methodology/lifecycle/policies/`.
- The EVENT is only a binding (`methodology/lifecycle/events.json`).
- The RENDER is the harness-native effect.

## Consequences

- One policy, six bindings — the shared layer is verifiable.
- `subagent.start`/`subagent.stop` are classifications derived from `tool.pre`/
  `tool.post`, not peer events.
- An observe-class event can annotate but never deny.

## Alternatives considered

1. **Event-centric** (original): simple to map, but the policy is duplicated per
   harness — rejected.
2. **Minimal hybrid**: canonical policies only for security verbs — rejected as a
   half-measure that still splits the model.
