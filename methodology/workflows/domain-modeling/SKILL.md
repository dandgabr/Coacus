---
name: domain-modeling
description: Use when a project's running language is fuzzy or drifting, to build and sharpen GLOSSARY.md and record durable decisions as ADRs while working.
---

# Domain modeling

Actively build and sharpen the project's domain language as you work, so names
in the code, the docs and the conversation agree.

## Moves

- **Challenge a term against the glossary.** "The glossary defines cancellation
  as X, but you seem to mean Y. Which is it?"
- **Sharpen fuzzy language.** "When you say account, do you mean the Customer or
  the User?"
- **Stress-test with a concrete scenario** to find where two meanings collide.
- **Cross-check the code.** "The code cancels whole Orders, but you said partial
  cancellation is possible. Which is right?"
- **Update the glossary inline**, as terms resolve — never batch the updates.

## The glossary

Follow [glossary-format.md](references/glossary-format.md). A glossary entry
defines *what a term is*, never what it does, and only project-specific concepts
belong. Keep a "Flagged ambiguities" section for resolved collisions.

## Decisions

Record an architecture decision record only when **all three** hold: the decision
is hard to reverse, it is surprising without context, and it is the result of a
real trade-off. If any is missing, skip it. Format:
[adr-format.md](references/adr-format.md).

## Boundaries

- Merely reading the glossary for vocabulary is a one-line pointer, not this
  skill. This skill is the active sharpen-and-record discipline.
- `grill-with-docs` is the user-invoked companion that applies this skill during
  an interview.
