---
name: using-coacus
description: >-
  Establishes how to work inside a Coacus repository: consult the skill
  catalog before acting, scan the index once per session, and follow the
  artifact lifecycle. Use when starting any conversation or task in a Coacus
  workspace.
---

# Using Coacus

<!-- SUBAGENT-STOP -->
If you were dispatched as a subagent to execute a specific task, skip this
skill unless that task explicitly asks you to plan, review, or coordinate.
<!-- /SUBAGENT-STOP -->

## The rule

Before you respond to any request — including asking a clarifying question —
check whether a relevant skill exists and follow it. Skills carry the project's
proven judgment; skipping them means improvising what already has an answer.

## Priority order

1. Process skills first (planning, debugging, review), then domain skills.
2. When two skills touch the same work, the more specific one wins.
3. User instructions outrank every skill; repository rules (`AGENTS.md`,
   `docs/adr/`) outrank individual skills.

## Red flags — you are about to rationalize skipping a skill

| Thought | Reality |
|---|---|
| "This is just a small change." | Small changes are where unchecked assumptions ship. |
| "I already know how to do this." | Knowledge is not the same as this repository's conventions. |
| "Let me look at the code first." | Reading code before loading the skill is how scope drifts. |
| "I'll check the skill after this edit." | The skill exists to shape the edit, not to audit it. |
| "There is probably no skill for this." | Check the index; that is exactly what it is for. |

## Session discipline — single scan

Read `catalog/INDEX.md` and `AGENTS.md` once at the start of the session. Do
not re-scan directories per turn; rely on the index and the session's memory.
If the index looks stale, regenerate it once, then continue.

## Artifact lifecycle

Every canonical artifact has one source. Work moves through:

`create (from templates/authoring)` → `validate` → `register (generate)` →
`discover (single scan)` → `activate (session start)`.

Never edit generated output (`catalog/`, `.agents/`, any `dist/`) by hand —
change the source and regenerate.

## Coordination

Cap concurrent work at the repository's governor limit and hand off between
agents with compact TOON payloads. Never spawn ungoverned parallel work.

## Harness adaptation

This skill names actions, not platform tools. The concrete substitution for
your harness is provided by the bootstrap's tool mapping at session start.
If a mapping is missing, prefer the repository's documented fallback wording
over inventing a capability.
