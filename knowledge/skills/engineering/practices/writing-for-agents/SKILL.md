---
name: writing-for-agents
description: Use when writing or editing a skill, an AGENTS.md line, or any document an agent reaches by a pointer, to keep it followable and free of drift.
---

# Writing for agents

The discipline behind a document that an agent will actually follow. Apply it to a
skill body, an `AGENTS.md` line, or any material an agent reaches by a pointer.

Adapted for Coacus from the `writing-for-agents` practice in the `mattpocock/skills`
collection (MIT). The wording is Coacus's own.

## Context pointers

A **context pointer** is a reference held in the agent's context that names
out-of-context material and encodes the condition for reaching it. A skill's
`description` is one; an `AGENTS.md` line naming a document is the same object.

The pointer's **wording**, not its target, decides when the agent reaches the
material and how reliably. A must-have target behind a weakly worded pointer is a
variance bug: sharpen the wording first; inline the material only if sharpening
fails.

- **Front-load the leading word** — the agent scans the first token.
- **One trigger per branch** — two synonyms that rename one branch are one branch
  written twice; collapse them.
- **Cut identity the body already carries** — a pointer that restates the target
  wastes the trigger slot.

## The information hierarchy

Rank material by immediacy: (1) in-file step, (2) in-file reference consulted on
demand, (3) disclosed reference reached through a pointer.

**Progressive disclosure is the move down this ladder.** It is not primarily a
token optimisation: it is how the hierarchy is protected. The disclosure test is
branching — inline what every branch needs; disclose what only some branches reach.

## Co-location, duplication, scattering

- **Co-location** — a concept's definition, rules and caveats under one heading.
- **Duplication** — one meaning repeated in two places; it costs maintenance and
  inflates the meaning's prominence past its real rank.
- **Scattering** — one meaning fragmented across many places; it hides the whole.

## Completion criteria

Every step ends on a checkable done-condition, set by two levers:

- **Clarity** — can the agent tell done from not-done? A vague bound invites
  premature completion. Sharpen the bound first; only if it is irreducibly fuzzy,
  hide later steps behind a real context boundary.
- **Demand** — "every modified model accounted for" forces thorough work where
  "produce a change list" does not. Demand can bind a body of flat reference too.

## Leading words

A **leading word** is a compact concept already in the model's prior knowledge that
the agent thinks with while running the document (*tight loop*, *red*, *tracer
bullet*). Repeat it as a **token, never as a sentence**. Prefer an existing word: a
made-up word pays in definition tokens what a pretrained word gives free. A word
too weak to beat the default is a no-op; reach for a stronger word.

## The negation anti-pattern

Steering by prohibition drags the forbidden behaviour into context and makes it
more available, not less. Prompt the **positive** target; a prohibition earns its
place only as a hard guardrail, paired with the positive.

## Pruning

- **No-op** — an instruction the model already obeys by default. The test is
  model-relative. When a sentence fails, delete the whole sentence, not the words.
- **Cache** — a restatement of a source of truth that already exists. The
  environment is a source of truth too; cache only the unwritten convention, the
  reason behind a choice, the gotcha no config confesses.
- **Sediment** — stale layers that settle because adding feels safe and removing
  feels risky.

## When to split

- **By sequence** — split where post-completion steps tempt rushing.
- **By invocation** — split off a model-invoked skill when it has a distinct
  leading word, or when another skill must reach it.
- **Orphan case** — shared reference two user-invoked skills both need can live in
  neither; push it to a plain file outside the skill system.
