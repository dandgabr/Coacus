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
- Matching folds the text first (NFKC and NFKD, format and combining characters removed,
  case-insensitive, look-alike slashes mapped, one path separator), reads it again after
  decoding HTML entities and percent escapes, strips code and bold markup and the spaces
  around a slash, and resolves `..`, `.` and `//` in path-like tokens. A directory matches
  with or without its closing slash and by its Python name (`engine.guardrail`); a name
  must stand alone, so `engine/improved/` and `AGENTS.mdx` do not match.
- A statement longer than 64,000 characters is refused unread.
- A rejected candidate adds a content-free alarm to the run (the protected pattern, never
  the statement), so a dropped proposal is visible.

## Consequences

- This is a text match on prose that an attacker may write. Letters from another script
  that look like Latin ones, a glob or brace form (`engine/guard*/`), a bare file name
  (`evaluate.py`), a name spread over spaced letters or lines, and a paraphrase ("the
  guard evaluator") pass rung 0a.
- `AGENTS.md` matches inside any path, so a proposal about another project's `AGENTS.md`
  is dropped too. That is the cost of not guessing where the repository root is; the alarm
  shows it happened.
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
