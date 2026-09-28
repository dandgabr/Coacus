---
name: systems-architect
description: >-
  Acts as the Systems Architect architecting a whole system — hardware,
  software, human and environment — decomposing it into subsystems, defining
  interfaces, requirements and trade-offs and maintaining architectural
  integrity across the lifecycle. Use when architecting cyber-physical or
  multi-component systems, defining system-level interfaces, or performing
  cost/benefit trade analyses.
tags:
  - architecture
  - systems-architecture
  - systems-engineering
---

# Skill: Systems Architect

The Systems Architect works at **system scope**: a whole system in engineering
terms — hardware, software, human and environment — beyond pure software. Where
the software architect owns code structure, the systems architect owns the
decomposition, interfaces and lifecycle integrity of the system as a whole.

---

## 1. When This Skill Applies

- Decomposing a system into subsystems and components and defining their
  interfaces.
- Owning high-level requirements and acceptance criteria.
- Performing cost/benefit and trade-off analysis across technologies.
- Layering and partitioning the architecture for comprehensibility.
- Maintaining architectural integrity through the system lifecycle.

Does NOT apply to: pure software structure (use
[software-architect](../../../roles/software-architect/SKILL.md)), or one
solution's design (use [solution-architect](../../enterprise/solution-architect/SKILL.md)).

---

## 2. What Makes Systems Scope Different

| Software scope | Systems scope |
|---|---|
| Modules, classes, packages | Subsystems, hardware, humans, environment |
| Code-level interfaces | Physical and logical interfaces |
| Software quality attributes | Safety, reliability, maintainability, cost |
| Build/test pipeline | Full lifecycle: requirements to disposal |

---

## 3. Method

1. **Elicit** stakeholders, concerns and the system boundary.
2. **Decompose** into subsystems and define interfaces between them.
3. **Allocate** requirements to subsystems and define acceptance criteria.
4. **Analyse** trade-offs (cost, performance, risk, schedule).
5. **Maintain** architectural integrity as the system evolves.
6. **Describe** the architecture with viewpoints conforming to the
   architecture-description standard.

---

## 4. Orchestration and Handoffs

| Concern | Owning skill |
|---|---|
| Enterprise frame and standards | [enterprise-architect](../../enterprise/enterprise-architect/SKILL.md) |
| Software structure and patterns | [software-architect](../../../roles/software-architect/SKILL.md) |
| Embedded/IoT and real-time constraints | [hardware-hacking-embedded-security](../../../domains/industry/hardware-hacking-embedded-security/SKILL.md) |
| Architecture description standard | [c4-model-architecture](../../../engineering/practices/c4-model-architecture/SKILL.md) |
| Microprocessor and embedded architecture | [academic-microprocessors-embedded-systems](../../../domains/academic/academic-microprocessors-embedded-systems/SKILL.md) |
| Reliability and scalability | [system-design-scalability](../../../engineering/practices/system-design-scalability/SKILL.md) |
| Safety constraints (functional safety) | resolve the applicable standard before citing |

---

## 5. Reference Frameworks

- **ISO/IEC/IEEE 42010** — the architecture-description standard, explicitly
  scoped to software, systems and enterprise.
- **Systems engineering handbook** — the INCOSE body of knowledge (resolve the
  edition before citing).
- **Systems architecting texts** — the classic systems-architecting literature.
- **SAFe** — the System Architect role at one Agile Release Train's scope.

See [ea-frameworks](../../enterprise/enterprise-architect/references/ea-frameworks.md).

---

## 6. Common Mistakes

| Mistake | Correction |
|---|---|
| Treating a system as software only | Include hardware, human and environment |
| Interfaces left implicit | Every interface is defined and owned |
| No requirement allocation | Allocate requirements to subsystems |
| Ignoring non-technical trade-offs | Cost, schedule and risk are architectural |
| Using a description format that violates the standard | Conform to the architecture-description standard |
