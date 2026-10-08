---
name: implement-spec
description: Use when implementing a whole specification or ticket set, working the ready frontier with parallel implementer subagents on one integration branch.
---

# Implement spec

Implement a specification end to end on one integration branch. The tickets are
not a list of steps — they are a **task graph**, so there is always a **frontier**
of tickets ready to be grabbed.

## Roles

- **Exploration subagent.** Before implementation, explore the codebase and save
  notes outside the repository so implementer subagents focus on implementation
  rather than discovery.
- **Implementer subagents.** Each runs in its own worktree on its own branch, based
  on the integration branch (reset onto it if not), builds with
  [superpowers-test-driven-development](../superpowers-test-driven-development/SKILL.md),
  and merges the integration tip into its own branch before reporting done, so its
  merge is a fast-forward.
- **Merger subagents.** Land finished work on the integration branch.
- **Final review.** Run [two-axis-code-review](../two-axis-code-review/SKILL.md)
  on the integration branch, then fix all issues in a single implementer subagent.

## Communication

Keep it sparse. Communicate through **context pointers**, not duplicated content:
point at the spec, the ticket and the exploration notes rather than restating them.

## Goal and cleanup

The goal is the **integration branch**, not a pull request; a draft pull request
opens only after the first merge. Completing a merge may change the frontier — that
is the scheduler, and it is what kicks off more implementers. Clean up every
worktree at the end.
