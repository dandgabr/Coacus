---
name: superpowers-verification-before-completion
description: Use when about to claim work is complete, fixed, or passing, before committing or creating PRs - requires running verification commands and confirming output before making any success claims; evidence before assertions always
---

<!--
Coacus adaptation of a Superpowers workflow (MIT).
Upstream: https://github.com/obra/superpowers @ 5bf4e78011075bcfc0dc295f0724994cd123ee71
Process artifacts are written under docs/temp/.
Conventions: ../using-coacus/references/coacus-process-conventions.md
-->

# Verification Before Completion

## Overview

**Core principle:** Evidence before claims, always.

**Violating the letter of this rule is violating the spirit of this rule.**

## The Iron Law

```
NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE
```

If you haven't run the verification command in this message, you cannot claim it passes.

## The Gate Function

```
BEFORE claiming any status or expressing satisfaction:

1. IDENTIFY: What command proves this claim?
2. RUN: Execute the FULL command (fresh, complete)
3. READ: Full output, check exit code, count failures
4. VERIFY: Does output confirm the claim?
   - If NO: State actual status with evidence
   - If YES: State claim WITH evidence
5. ONLY THEN: Make the claim

Skip any step = lying, not verifying
```

## Common Failures

| Claim | Requires | Not Sufficient |
|-------|----------|----------------|
| Tests pass | Test command output: 0 failures | Previous run, "should pass" |
| Linter clean | Linter output: 0 errors | Partial check, extrapolation |
| Build succeeds | Build command: exit 0 | Linter passing, logs look good |
| Bug fixed | Test original symptom: passes | Code changed, assumed fixed |
| Regression test works | Red-green cycle verified | Test passes once |
| Agent completed | VCS diff shows changes | Agent reports "success" |
| Requirements met | Line-by-line checklist | Tests passing |
| A version, path or tool is X | Its manifest/registry entry in the resolved tree, **named** | Recalling it; a wildcard glob that matched a sibling; a lock you assumed |
| A feature or entry is absent | The exact **error or `Result`**, printed | A count or summary line — several different causes produce the same one |
| The artifact says Y | The artifact **at the path in force** | Another checkout, a generated mirror, a cached rendering |

## Red Flags - STOP

- Using "should", "probably", "seems to"
- Expressing satisfaction before verification ("Great!", "Perfect!", "Done!", etc.)
- About to commit/push/PR without verification
- Trusting agent success reports
- Relying on partial verification
- Thinking "just this once"
- Tired and wanting work over
- **ANY wording implying success without having run verification**

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "Should work now" | RUN the verification |
| "I'm confident" | Confidence ≠ evidence |
| "Just this once" | No exceptions |
| "Linter passed" | Linter ≠ compiler |
| "Agent said success" | Verify independently |
| "I'm tired" | Exhaustion ≠ excuse |
| "Partial check is enough" | Partial proves nothing |
| "Different words so rule doesn't apply" | Spirit over letter |
| "It returned 0, so it isn't there" | Absent, unreachable, out of scope and locked all return 0. Print the **`Result`** and read it. |
| "I read the manifest" | *Which* manifest? `ls …/foo-*` also matches `foo-bar`. Name the file every number came from. |
| "The spec says so" | Which **copy** — the one in force, a stale checkout, or a generated mirror? |
| "The output shows no such field" | You read a rendering. Ask for the field by name before concluding it is missing. |

## Key Patterns

**Tests:**
```
✅ [Run test command] [See: 34/34 pass] "All tests pass"
❌ "Should pass now" / "Looks correct"
```

**Regression tests (TDD Red-Green):**
```
✅ Write → Run (pass) → Revert fix → Run (MUST FAIL) → Restore → Run (pass)
❌ "I've written a regression test" (without red-green verification)
```

**Build:**
```
✅ [Run build] [See: exit 0] "Build passes"
❌ "Linter passed" (linter doesn't check compilation)
```

**Requirements:**
```
✅ Re-read plan → Create checklist → Verify each → Report gaps or completion
❌ "Tests pass, phase complete"
```

**Agent delegation:**
```
✅ Agent reports success → Check VCS diff → Verify changes → Report actual state
❌ Trust agent report
```

## A published number is a claim until code reproduces it

Before declaring the work done, recompute the numbers the artifact publishes — a
document, a README, a spec — and compare at the document's own precision.

- **A tolerance wider than the document's rounding is not a check.** Comparing at two
  decimals with `< 0.02` is 50–200× the smallest real edit: a colour drifting by one
  channel step went unnoticed because the tolerance, not the implementation, was
  doing the work. Use the document's precision (±0.005 at two decimals); when it
  cannot be beaten because the document itself is rounded, say so.
- **A test's name is not its assertion.** A test named
  `contrast_is_computed_so_a_copied_dark_block_fails` did not test that: a light
  palette is legible, so the copied block passed every contrast assertion, and only
  the `assert_ne!` beside it noticed. Read the assertions, not the titles.
- **A value brought from memory is not a measurement — including the environment.**
  Probe it; see "Measure the environment before a command" in the process
  conventions.

Anchor at least one assertion outside the artifact's own snapshot. Forty-eight
published ratios reproduced to ±0.005 prove the code agrees with the document, and
not that either is right; `contrast("#000000", "#ffffff") == 21` anchors the formula.

## When To Apply

**ALWAYS before:**
- ANY variation of success/completion claims
- ANY expression of satisfaction
- ANY positive statement about work state
- Committing, PR creation, task completion
- Moving to next task
- Delegating to agents

**Rule applies to:**
- Exact phrases
- Paraphrases and synonyms
- Implications of success
- ANY communication suggesting completion/correctness
