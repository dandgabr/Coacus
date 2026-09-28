---
name: solution-architect
description: >-
  Acts as the Solution Architect designing one bounded solution within the
  enterprise guardrails: its structure, components, interfaces and quality
  attributes, selecting technologies and integration patterns and proving
  compliance at the architecture review gate. Use when architecting a specific
  initiative, choosing technologies for a delivery, producing solution options
  or validating a solution against enterprise standards.
tags:
  - architecture
  - solution-architecture
  - togaf
---

# Skill: Solution Architect

The Solution Architect bridges enterprise intent and engineering reality. It
owns **one bounded solution** — the architecture that satisfies a specific
business problem inside the principles and standards the enterprise architect
sets.

---

## 1. When This Skill Applies

- Defining a solution's structure, components, interfaces and quality
  attributes.
- Selecting technologies and integration patterns for a delivery.
- Producing solution options and build/migration roadmaps.
- Validating a solution against enterprise standards and escalating exceptions.
- Leading technical delivery across teams or suppliers.

Does NOT apply to: the enterprise frame (use
[enterprise-architect](../enterprise-architect/SKILL.md)), or the internal
structure of a single software system (use
[software-architect](../../../roles/software-architect/SKILL.md)).

---

## 2. The Solution Architect's Boundary

| Dimension | Owns | Does NOT own |
|---|---|---|
| Scope | One solution or initiative | The whole enterprise |
| Horizon | Delivery horizon | Multi-year strategy |
| Stakeholders | Users, developers, delivery teams | Executives, board |
| Decisions | Design within guardrails | Principles, standards, waivers |
| Output | Solution design + compliance evidence | Target-state roadmap |

The Solution Architect proves **this delivery is true within** the enterprise
frame and the domain standards. When the frame and the delivery conflict, it
escalates to the Architecture Review Board rather than silently deviating.

---

## 3. Method (TOGAF ADM Phases A–G, content)

1. **Scope** the solution against the business problem and the Statement of
   Architecture Work.
2. **Design** the solution across the relevant domains (application, data,
   technology), reusing reference architectures and patterns.
3. **Select** technologies and integration patterns; document the trade-offs.
4. **Validate** against enterprise standards; record the compliance evidence.
5. **Escalate** exceptions and required dispensations to the review board.
6. **Feed back** reusable patterns and debt signals to the enterprise
   repository.

---

## 4. Orchestration and Handoffs

| Concern | Owning skill |
|---|---|
| Enterprise principles, standards, target state | [enterprise-architect](../enterprise-architect/SKILL.md) |
| Internal system structure, DDD, patterns | [software-architect](../../../roles/software-architect/SKILL.md) |
| Integration style, messaging, APIs | [integration-architect](../../domains/integration-architect/SKILL.md) |
| Data model and governance for the solution | [data-architect](../../domains/data-architect/SKILL.md) |
| Cloud landing zone and infrastructure | [technology-architect](../../domains/technology-architect/SKILL.md) |
| Security controls for the solution | [security-architect-sabsa](../../../security/operations/security-architect-sabsa/SKILL.md) |
| Scale, resilience, CAP trade-offs | [system-design-scalability](../../../engineering/practices/system-design-scalability/SKILL.md) |
| Solution diagrams and descriptions | [c4-model-architecture](../../../engineering/practices/c4-model-architecture/SKILL.md) |

---

## 5. Reference Frameworks

- **TOGAF** — the method; the architecture of a solution.
- **SAFe** — the Solution Architect role at solution-train scope.
- **ISO/IEC/IEEE 42010** — the architecture-description standard.
- **C4 model** — the viewpoint notation for solution descriptions.
- **Design-pattern catalogues** — GoF patterns and enterprise integration
  patterns (see [dp-creational](../../../engineering/patterns/dp-creational-patterns/SKILL.md),
  [dp-structural](../../../engineering/patterns/dp-structural-patterns/SKILL.md),
  [dp-behavioral](../../../engineering/patterns/dp-behavioral-patterns/SKILL.md)).

See [ea-frameworks](../enterprise-architect/references/ea-frameworks.md) for the
resolved versions; resolve any new pin before citing it.

---

## 6. Common Mistakes

| Mistake | Correction |
|---|---|
| Designing the enterprise from one solution | Stay inside the frame; escalate conflicts |
| Ignoring the enterprise standards | Validate and record compliance evidence |
| No reusable pattern fed back | Feed patterns and debt signals to the repository |
| Optimizing locally against the target state | Reconcile with the enterprise architect |
| Treating a solution as a synonym for a system | A solution may span several systems |
