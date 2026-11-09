---
name: to-spec
description: Use when the current conversation should be turned into a written specification — synthesize what was discussed, confirm the test seams, and publish it.
---

# To spec

Turn the current conversation into a specification. No interview: synthesize what
has already been discussed.

## Confirm the seams first

Before writing anything, sketch the **seams** at which the feature will be tested.
Prefer an existing seam over a new one, the highest seam possible, and the fewest
seams — the ideal number is one. Check the seams with the user before continuing.

## Template

- **Problem statement** — the problem, in the user's terms.
- **Solution** — the approach, at the level the seams imply.
- **User stories** — a long, numbered list.
- **Implementation decisions.**
- **Testing decisions** — the confirmed seams and what is asserted at each.
- **Out of scope.**
- **Further notes.**

## Rules

- Do **not** include specific file paths or code snippets — they go stale quickly.
  The one exception is a prototype snippet that encodes a decision more precisely
  than prose can (a state machine, a reducer, a schema, a type shape).
- One meaning, one place.
- Publish the spec where the project keeps its specifications.
