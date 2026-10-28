---
name: editable-diagram-engineering
description: >-
  Provides persistent editable technical diagram authoring, incremental updates
  and conversion guidance when creating or maintaining editable diagram files
  or editor documents, preserving human edits, or assessing roundtrip fidelity.
tags:
  - editable-diagrams
  - diagram-synchronization
  - diagram-interoperability
  - diagram-adapters
---

# Editable Diagram Engineering

Maintain an editable artifact that answers a reader's question while preserving
its declared meaning and human work. Use this skill for persistent diagram
creation, import, reconciliation or conversion. Keep ordinary inline Mermaid
snippets and general architecture decisions with their existing owners.

## Establish the representation contract

Identify audience, question, notation, the authority established by the task,
source revision, editable deliverable, preview and known limitations. Distinguish
extracted facts, inferences, proposals and unknowns. Do not introduce a universal
intermediate format or an always-synchronized sidecar merely to follow this skill.

Choose the tool by required capabilities, not a preferred vendor. Establish what
it can read, edit, preserve and verify before selecting an operation. Product
references below are optional case studies, not required tools.

Choose only the reference needed:

- For stable identity, source evidence, manual changes and reconciliation, use
  [model and synchronization](references/model-and-sync.md).
- When using draw.io, for XML pages, compression, editable exports and notation conversion, use
  [draw.io guidance](references/drawio.md).
- When using DrawCMS, for saved documents, live editor commands, undo, local/cloud boundaries and
  narrative motion, use [DrawCMS guidance](references/drawcms.md).
- For structural, rendered, reopening and conversion evidence, use
  [verification](references/verification.md).

Read the actual state, make the smallest justified change and inspect the result.
Keep a recoverable original when an operation can discard information. Report
conflicts or unsupported capabilities rather than promising safe synchronization.

## Preserve existing owners

Use [architecture documentation](../../engineering/practices/architecture-documentation/SKILL.md)
for authority, traceability and view governance, [UML generation](../uml-diagram-generation/SKILL.md)
and [C4 modeling](../../engineering/practices/c4-model-architecture/SKILL.md) for
notation and abstraction, and [code mapping](../code-architecture-mapping/SKILL.md)
for extraction. Keep graph analysis with [relationship mapping](../graph-relationship-mapping/SKILL.md).
The documenter coordinates communication and format selection.

Use [deterministic motion rendering](../../domains/design/deterministic-motion-rendering/SKILL.md)
for exported animation timing and media evidence. An authored animated path is
an explanation, not an observed execution trace. Apply the existing
[accessibility guidance](../../engineering/practices/web-accessibility-wcag/SKILL.md)
to the presentation and provide a textual or static equivalent.

## State what was verified

Separate parsing, model consistency, rendered legibility, editable reopening and
runtime observations. Deliver the editable artifact and a concise change/loss
record with observed results, checks not run and remaining unknowns. A screenshot
or successful command alone does not establish editability or semantic fidelity.
