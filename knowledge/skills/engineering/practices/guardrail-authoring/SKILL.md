---
name: guardrail-authoring
description: Use when adding a guardrail policy or an advisory content rule, to keep the rule precise, tested, and fail-open.
---

# Guardrail authoring

A guardrail is authored once and rendered natively (PAER). Keep it precise,
tested and fail-open. See the `lifecycle-guardrails` standard for the model.

## Rules are data

- A **policy** constrains an ACTION (`verb` + `resource`); the event only binds
  *when* it runs. Author it under the lifecycle policies directory, disabled by
  default: installing the framework never changes a session without an opt-in.
- An **advisory content rule** is `field x operator x pattern`, all conditions
  AND-combined. Author it in the security-pattern catalogue; a match produces an
  advisory, never a deny.

## Precision

- Give a rule at least one condition. A rule with no condition can never match.
- Test the pattern before shipping: run it against a known-good and a known-bad
  sample, and read the match count.
- Avoid over-broad patterns — `log` matches login, dialog and catalog. Anchor the
  pattern and use word boundaries.
- Prefer an unquoted pattern: quoting changes backslash handling.
- Attach the **mitigation** to the message, not just the alert. A warning with no
  fix trains the reader to ignore it.

## Failure

- Fail-open at the rule layer: no match is allow, and a non-compiling pattern does
  not match (and is a lint error).
- Separate the failure domains: a decision failure versus a mechanism failure. A
  broken hook must not deny every call.

## Ladder and hygiene

- **Ladder.** Layer defenses: a deterministic pattern, then a single-turn review,
  then a cross-file review. Each layer is independently switchable, and a deferred
  review may run in the background and wake the agent with its findings rather
  than blocking the turn.
- **Frozen ids.** Rule ids are frozen and append-only: add a new id, never
  renumber. An id that disappears is a build error, not a silent shift.
- **Inline suppression.** Provide a convention for recording a reviewed, safe
  case inline (for example a `safe because` comment) so a false positive can be
  silenced without disabling the whole layer.
- **Prompt budget.** When layered rule files concatenate under a size cap,
  document the truncation order: drop the tail first, so user-wide rules survive
  and the most local are lost.
