---
name: retro
description: Use after a work session to suggest improvements to the agent's environment — navigation, checks, standards, tooling — most severe first.
---

# Retro

Review the session and propose improvements to the environment the agent worked
in, most severe first.

## Mechanical versus judgement

Classify every finding:

- A **mechanical** violation — a rule a machine could check — earns a
  **deterministic check**: a validator, a lint rule, a test. Full stop. Do not
  write prose for it; prose is for the judgement calls.
- A **judgement** call — a trade-off without a single right answer — earns a
  standards note, not a check.

## A repository with no guardrail is itself a finding

If a class of mistake recurred and nothing prevents it, the missing guardrail is
the top finding. Convert the mechanical violations into checks in the same change
when they are small enough.

## What to survey

- **Navigation** — was the right file, index or map easy to find?
- **Checks** — which mistakes were caught late, and which by a machine at all?
- **Standards** — where did two choices conflict with no written rule?
- **Tooling** — which repeated action should be a single command?

## Output

Rank the findings by severity, and for each say whether it earns a check or a
standards note and what the concrete change is.
