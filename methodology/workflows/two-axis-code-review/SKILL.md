---
name: two-axis-code-review
description: Use when reviewing a diff, running a Standards review and a Spec review as isolated parallel subagents so neither pollutes the other.
---

# Two-axis code review

Review the diff since a fixed point on two axes, isolated from each other:

- **Standards** — does the change follow the repository's coding standards, plus a
  smell baseline?
- **Spec** — does the change faithfully implement the originating issue or spec?

Run the two axes as **parallel subagents** so neither pollutes the other's context.

## Rules

- **Fail fast before fanning out.** A bad fixed point or an empty diff must fail
  here, not inside two parallel subagents.
- **Compare against the merge base** (a three-dot diff), not the branch tip.
- **Inline what a subagent cannot fetch.** A subagent has no other access to the
  repository's own standing rules — paste the baseline it must judge against. A
  documented repository standard overrides the baseline, and every smell is
  reported as a judgement call, never a hard violation.
- **Never merge or rerank findings across the axes.** A single ranked winner is
  exactly what the separation exists to prevent.

## Output

Report each axis separately, each finding with its location and the standard or
spec line it violates.
