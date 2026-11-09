---
name: two-axis-code-review
description: Use when reviewing a diff, running a Standards review and a Spec review as isolated parallel subagents so neither pollutes the other.
---

# Two-axis code review

For review timing, scope and dispatch context, see [requesting code review](../requesting-code-review/SKILL.md). For handling returned findings, see [review reception](../receiving-code-review/SKILL.md).

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

## Axis Criteria

### 1. Standards Axis (Code Health & Quality)
- **Silent failure hunting:** Flag swallowed exceptions, empty error catch blocks, unlogged rejection handlers, and silent fallbacks that hide corrupt state.
- **Type invariants & illegal states:** Enforce that domain invariants are guaranteed by construction (making invalid states unrepresentable via discriminated unions or value objects).
- **Comment rot & noise:** Flag comments that merely restate the code, comments that contradict the implementation, or stale docstrings left behind after refactoring.
- **Complexity concentration:** Flag shallow abstraction wrappers that add indirection without eliminating complexity.

### 2. Spec Axis (Requirements & Correctness)
- **Self-containment check:** Verify whether the diff can be reviewed and understood on its own merits without unreferenced external context.
- **Contract & edge fulfillment:** Verify every acceptance criterion, boundary condition, and error branch specified in the originating requirement.
- **Scope creep:** Flag unrequested architectural changes or speculative code that does not serve the originating ticket.

## Output

Report each axis separately, each finding with its location and the standard or
spec line it violates.
