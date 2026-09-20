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
   - **Level 4 — Code**: Class or sequence diagrams for critical flows.

2. **ADR Management (Architectural Decision Records — MADR 3.0)**:
   - Record every relevant structural decision with Context, Considered Options, Decision, and Consequences (Pros/Cons).
   - Standard naming: `0001-nome-da-decisao.md`.

3. **Traceability Matrices**:
   - Mapping between non-functional requirements (NFRs), decisions, and components.

---

## 🔗 Integration with Other Skills

- [c4-model-architecture](../c4-model-architecture/SKILL.md): the canonical C4 Model skill (abstraction, PlantUML, Structurizr, Mermaid) — use it as the in-depth visualization reference; this skill focuses on **documentation governance** (ADRs, traceability, and view structuring).
- [documentation-designer](../documentation-designer/SKILL.md): supplies the Mermaid syntax rules and the human technical prose (Anti-AI) for generated documents.
- [software-architect](../../../roles/software-architect/SKILL.md): consumes ADRs and C4 views as the record of design decisions.
- [security-architect-sabsa](../../../security/operations/security-architect-sabsa/SKILL.md): contributes trust zones and security requirements that belong in architectural views.

> For reference standards, see [`references/c4_model_standards.md`](./references/c4_model_standards.md) and [`references/madr_adr_standards.md`](./references/madr_adr_standards.md). For a filled-in example, see [`examples/c4_container_adr_sample.md`](./examples/c4_container_adr_sample.md).
