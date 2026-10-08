---
name: review-findings-pipeline
description: Use when a review or audit produces many candidate findings, to filter false positives through adversarial validation and a confidence threshold before reporting.
---

# Review findings pipeline

Turn many candidate findings into a short, trustworthy list. Generate in
parallel, validate each finding adversarially, and report only what survives.

## Stages

1. **Generate — parallel and lens-diverse.** Compose reviewers by an opposed axis,
   not by topic: minimal change versus clean architecture versus pragmatic balance,
   or standards versus spec. Deliberately run two reviewers on the highest-stakes
   axis: an independent second opinion is a cheap recall win. Fail fast before
   fanning out — an empty diff or a bad fixed point fails here, not inside the
   reviewers.
2. **Validate each finding.** One validator per finding, given the diff (or spec)
   and the claim, tasked to confirm the issue is real with high confidence. Drop
   every finding the validator does not confirm.
3. **Score confidence 0–100 with anchored descriptors**, not vibes:
   - **0** — false positive, or pre-existing.
   - **25** — might be real; stylistic and not in a written rule.
   - **50** — real, but possibly a nitpick.
   - **75** — double-checked and verified; important, or in a written rule.
   - **100** — confirmed, and frequent in practice.
4. **Threshold.** Report only findings scored **80 or above**.

## Do NOT flag

- Pre-existing issues.
- Code that only looks like a bug but is correct.
- Pedantic nitpicks a senior engineer would not raise.
- Anything a linter would catch — do not run the linter to check.
- General quality concerns (missing tests, broad security worries) unless a written
  rule requires them.
- An issue a written rule names but the code explicitly silences.

## Positive signal

Flag when the code fails to compile or parse, will produce wrong results
regardless of input, or clearly violates a written rule you can quote exactly.

## Why

False positives erode trust and waste the reviewer's time. Post one comment per
unique issue, and never rerank findings across isolated reviewers — the separation
exists precisely to prevent a single ranked winner.
