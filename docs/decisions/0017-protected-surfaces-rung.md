# ADR 0017: Reject proposals that touch the loop's protected surfaces

* **Status**: accepted
* **Date**: 2026-11-18
* **Tags**: self-improvement, verification, guardrails

## Context

`docs/standards/self-improvement-loop.md` lists surfaces the improvement loop must never
edit: the guardrail and verification engines, the loop itself, the evals and the
standards that govern untrusted content. Until now that was prose only, with the
enforcement left to a later decision (ADR 0009 recorded it as advisory).

The loop never applies a change, so the practical risk is a poisoned observation that
steers a proposal towards weakening one of these files and a reviewer who approves it
because it looks routine.

## Decision

- `engine/improve/protected.py` holds the list as one constant, with `is_protected(path)`
  and `mentions(text)`. The standard quotes the list and a test fails if the two differ.
- `engine/improve/verify.py` gains rung 0a. A candidate fails it when its statement names
  a protected surface or when the router's target is a catalog entry on one. A failed
  candidate is not staged.
- Matching folds the text first (NFKC, format characters removed, case-insensitive, one
  path separator) and resolves `..` in path-like tokens. A name must stand alone, so
  `engine/improved/` and `AGENTS.mdx` do not match.

## Consequences

- This is a text match on prose that an attacker may write. A spaced-out name, an
  encoding the fold does not undo or a paraphrase ("the guard evaluator") passes rung 0a.
  Human approval of every proposal stays the real gate; the rung only removes the
  obvious cases and records why.
- The router targets catalog skills and agents, so the routed-path check cannot fire
  today. It is kept for the day a catalog entry points at a protected file.
- Not built: a digest manifest of the protected files (it would fail on every legitimate
  edit and prove nothing about a proposal) and a safety text emitted from an engine
  constant. Neither blocks a candidate; add them when a reviewer tool needs them.
- Changing the list is a change to a protected surface and goes through review like one.

## Alternatives

- A check on the staged diff: there is no diff, the loop proposes statements.
- Leave it advisory: the cost of the rung is small and a test now ties the list to the
  standard.
