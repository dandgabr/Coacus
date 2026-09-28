---
name: application-architect
description: >-
  Acts as the Application Architect owning the application portfolio: its map
  and lifecycle (invest, maintain, retire), application standards, reference
  architectures and integration coherence, and the build-versus-buy and SaaS
  fit decisions. Use when rationalizing an application portfolio, defining
  application standards, guiding modernization, or assessing build-versus-buy.
tags:
  - architecture
  - application-architecture
---

# Skill: Application Architect

The Application Architect owns the **application domain** of the enterprise
architecture (TOGAF ADM Phase C, Application Architecture): the portfolio of
applications, their structure, standards and lifecycle — distinct from the
infrastructure beneath them and from the structure of one software system.

---

## 1. When This Skill Applies

- Owning the application portfolio map and lifecycle (invest, maintain, retire).
- Defining application standards, patterns and reference architectures.
- Guiding application modernization and rationalization.
- Ensuring application-to-application integration coherence.
- Assessing build-versus-buy and SaaS fit.
- Aligning applications with business capabilities.

Does NOT apply to: the internal structure of one system (use
[software-architect](../../../roles/software-architect/SKILL.md)), or the
integration style between systems (use
[integration-architect](../integration-architect/SKILL.md)).

---

## 2. Portfolio Thinking

- **Map**: every application, its capabilities served, its criticality and its
  technical health.
- **Lifecycle**: time-based invest/maintain/retire decisions tied to business
  value and risk.
- **Rationalization**: eliminate overlap and duplication before adding systems.
- **Build vs. buy vs. SaaS**: decide by fit, differentiation and total cost of
  ownership, not by preference.

---

## 3. Method (TOGAF ADM Phase C, Application Architecture)

1. **Baseline** the application portfolio and its interfaces.
2. **Target** the portfolio aligned to the business capabilities and the
   enterprise target state.
3. **Gap analysis** with a rationalization and modernization plan.
4. **Govern** application standards and reusable reference architectures.
5. **Feed** the portfolio decisions to the enterprise architect for the
   investment plan.

---

## 4. Orchestration and Handoffs

| Concern | Owning skill |
|---|---|
| Enterprise frame and portfolio investment | [enterprise-architect](../../enterprise/enterprise-architect/SKILL.md) |
| Internal structure of one system | [software-architect](../../../roles/software-architect/SKILL.md) |
| Cross-system integration and messaging | [integration-architect](../integration-architect/SKILL.md) |
| API standards and lifecycle | [api-architect](../api-architect/SKILL.md) |
| Data model of the portfolio | [data-architect](../data-architect/SKILL.md) |
| Domain boundaries and bounded contexts | [architecture-ddd](../../../engineering/practices/architecture-ddd/SKILL.md) |
| Enterprise application patterns | [dp-* patterns](../../../engineering/patterns/dp-structural-patterns/SKILL.md) |

---

## 5. Reference Frameworks

- **TOGAF** — ADM Phase C, Application Architecture.
- **ArchiMate** — Application layer (application component, interface, service).
- **C4 model** — for describing a solution's containers and components.
- **Enterprise application patterns** — the classic application-pattern
  catalogue (resolve the edition; see `version-freshness`).

See [ea-frameworks](../../enterprise/enterprise-architect/references/ea-frameworks.md).

---

## 6. Common Mistakes

| Mistake | Correction |
|---|---|
| Adding an application before rationalizing | Rationalize overlap first |
| Treating the portfolio as an inventory only | It carries lifecycle and value decisions |
| Choosing build/buy by preference | Decide by fit, differentiation and TCO |
| Confusing application with solution | A solution may span several applications |
| No interface governance | Interfaces are governed by the integration architect |
