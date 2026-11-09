---
name: architecture-documentation
description: >-
  Guides the technical documentation of software systems and architectures with the C4 Model,
  Mermaid-structured diagrams, Architectural Decision Record management (ADRs in MADR 3.0 format),
  and traceability matrices that link requirements, decisions, and components.
---

# Skill: Software Architecture Documentation and ADRs

This skill establishes the standards and methodologies for documenting information systems, architectural decisions, and structural views clearly, traceably, and with rich visual support.

---

## 🎯 Pillars of Architecture Documentation

1. **C4 Model (Context, Container, Component, Code)**:
   - **Level 1 — System Context**: Macro view showing the system under analysis, its users, and the external ecosystem.
   - **Level 2 — Containers**: Applications, microservices, APIs, databases, and queues.
   - **Level 3 — Components**: Internal modules, controllers, and adapters inside a container.
   - **Level 4 — Code**: Optional implementation detail within a component, such as classes or entities. Dynamic interaction views describe flows separately.

2. **ADR Management (Architectural Decision Records — MADR 3.0)**:
   - Record every relevant structural decision with Context, Considered Options, Decision, and Consequences (Pros/Cons).
   - Standard naming: `0001-decision-name.md`.

3. **Traceability Matrices**:
   - Mapping between non-functional requirements (NFRs), decisions, and components.

---

## 🔗 Integration with Other Skills

- [c4-model-architecture](../c4-model-architecture/SKILL.md): the canonical C4 Model skill (abstraction, PlantUML, Structurizr, Mermaid) — use it as the in-depth visualization reference; this skill focuses on **documentation governance** (ADRs, traceability, and view structuring).
- [documentation-designer](../documentation-designer/SKILL.md): supplies the Mermaid syntax rules and the human technical prose (Anti-AI) for generated documents.
- [software-architect](../../../roles/software-architect/SKILL.md): consumes ADRs and C4 views as the record of design decisions.
- [security-architect-sabsa](../../../security/operations/security-architect-sabsa/SKILL.md): contributes trust zones and security requirements that belong in architectural views.

> For reference standards, see [`references/c4_model_standards.md`](./references/c4_model_standards.md) and [`references/madr_adr_standards.md`](./references/madr_adr_standards.md). For a filled-in example, see [`examples/c4_container_adr_sample.md`](./examples/c4_container_adr_sample.md).

## Model Authority and View Freshness

Identify the authoritative model or source already established by the task and
record its revision, extraction scope and relationship to each published view.
A filtered view is a projection, not an independent copy of architectural truth.
Keep declared configuration, observed snapshots, inferred dependencies and
proposed design distinct. Record unsupported or missing facts rather than
inventing security metadata to complete a view.

For persistent editable artifacts, use [editable diagram engineering](../../../mapping/editable-diagram-engineering/SKILL.md)
for identity, human-preserving reconciliation, conversion loss and readback.
This skill retains ADR, traceability and view-governance responsibility; it does
not introduce a mandatory intermediate representation or synchronized sidecar.
Review semantic changes separately from geometry and presentation changes.

Sources reviewed 2026-10-27: [C4 code diagrams](https://c4model.com/diagrams/code)
and [dynamic diagrams](https://c4model.com/diagrams/dynamic). These distinguish
implementation detail from an ordered interaction view.
