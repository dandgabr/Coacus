---
name: superpowers-requesting-code-review
description: Use when completing tasks, implementing major features, or before merging to verify work meets requirements
---

<!--
Coacus adaptation of a Superpowers workflow (MIT).
Upstream: https://github.com/obra/superpowers @ 5bf4e78011075bcfc0dc295f0724994cd123ee71
Process artifacts are written under docs/temp/.
Conventions: ../using-coacus/references/coacus-process-conventions.md
-->

# Requesting Code Review

Dispatch a code reviewer subagent to catch issues before they cascade. The reviewer gets precisely crafted context for evaluation — never your session's history.

**Core principle:** Review early, review often.

## When to Request Review

**Mandatory:**
- After each task in subagent-driven development
- After completing major feature
- Before merge to main

**Optional but valuable:**
- When stuck (fresh perspective)
- Before refactoring (baseline check)
- After fixing complex bug

## How to Request

**1. Get git SHAs:**
```bash
BASE_SHA=$(git rev-parse HEAD~1)  # or: git merge-base origin/main HEAD
HEAD_SHA=$(git rev-parse HEAD)
```

**2. Dispatch code reviewer subagent:**

Dispatch a `general-purpose` subagent, filling the template at [code-reviewer.md](code-reviewer.md)

**Placeholders:**
- `{DESCRIPTION}` - Brief summary of what you built
- `{PLAN_OR_REQUIREMENTS}` - What it should do
- `{BASE_SHA}` - Starting commit
- `{HEAD_SHA}` - Ending commit

**3. Act on feedback:**
- Fix Critical issues immediately
- Fix Important issues before proceeding
- Note Minor issues for later
- Push back if reviewer is wrong (with reasoning)

## Example

```
[Just completed Task 2: Add verification function]

You: Let me request code review before proceeding.

BASE_SHA=$(git log --oneline | grep "Task 1" | head -1 | awk '{print $1}')
HEAD_SHA=$(git rev-parse HEAD)

[Dispatch code reviewer subagent]
  DESCRIPTION: Added verifyIndex() and repairIndex() with 4 issue types
  PLAN_OR_REQUIREMENTS: Task 2 from docs/temp/plans/deployment-plan.md
  BASE_SHA: a7981ec
  HEAD_SHA: 3df7661

[Subagent returns]:
  Strengths: Clean architecture, real tests
  Issues:
    Important: Missing progress indicators
    Minor: Magic number (100) for reporting interval
  Assessment: Ready to proceed

You: [Fix progress indicators]
[Continue to Task 3]
```

## Two lenses, and one of them mutates

Ask for review in **two independent lenses**, in parallel, with the same output
contract (`Strengths` / `Issues` by severity with the exact input that proves each /
`Recommendations` / a one-line verdict):

- a **domain** lens — security, UX, data — asking what the surface does to the person
  who meets it;
- a **QA** lens that replays single-edit mutants of the implementation against the
  assertions already written and reports which of them **fail to die**. The mutation
  score is the finding: "6 of 12 killed" names the six weak assertions, which is more
  actionable than "add more tests".

State the contract in the prompt — read-only, no subagents, findings ordered by
severity with the input that proves each — or the review returns adjectives. Where
both lenses report the same defect independently, that is the strongest signal
available; a defect only one lens reports is a judgment call.

## Consult before building, then review after

For a part that decides user experience, security or structure, hold a **design
consultation before any code**, and a review after each piece.

- Brief read-only consultants (interface, experience, frontend, security) in parallel
  with the same material: the decisions already taken, the constraints, and the
  questions you want answered. Ask for ranked decisions with a one-line rationale and
  the open questions for the owner.
- **Wait for every report before consolidating.** Reports that agree independently are
  the strongest signal; where they disagree, choose, and record the reason in the
  decision record. Decide the open questions yourself when an earlier decision already
  answers them; ask the owner only for what the record does not settle.
- **Read what each reviewer says it did not read.** A report that admits it skipped
  files is evidence about those files only; check the skipped ones, and verify its
  factual claims against the code before accepting them.
- Reviews found defects that no test would have: a setting that did nothing (the
  platform already decided it), a promise in a dialog that the code could not keep, an
  alert that could fire for a provider the user had removed, a combo row that undid a
  reset. Apply every finding that survives reproduction, and write down what was not
  applied and why.

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "I'll just review the diff myself instead of dispatching a reviewer" | You're the coordinator — reviewing the diff inline burns the context window you need to keep driving the work. Dispatch a reviewer subagent: the diff and the evaluation live in its context, and only the findings come back to you. |
| "The reviewer needs my whole session history to understand the change" | Hand it precisely crafted context, never your session's history. That keeps the reviewer on the work product, not your thought process. |

## Red Flags

**Never:**
- Skip review because "it's simple"
- Ignore Critical issues
- Proceed with unfixed Important issues
- Argue with valid technical feedback

**If reviewer wrong:**
- Push back with technical reasoning
- Show code/tests that prove it works
- Request clarification

See template at: [code-reviewer.md](code-reviewer.md)
