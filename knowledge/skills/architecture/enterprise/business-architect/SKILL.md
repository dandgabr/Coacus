---
name: business-architect
description: >-
  Acts as the Business Architect modeling business capabilities, value streams
  and business motivation, producing the business architecture (TOGAF ADM
  Phase B) that technology architecture must serve. Use when mapping business
  capabilities, defining value streams, aligning strategy to change, or tracing
  business objectives to IT investment.
tags:
  - architecture
  - business-architecture
  - togaf
---

# Skill: Business Architect

The Business Architect owns the **pre-technology view**: what the business does,
what it can do (capabilities), how it delivers value (value streams) and why it
changes (motivation). The technology layers exist to serve this view, not the
reverse.

---

## 1. When This Skill Applies

- Modeling business capabilities and value streams.
- Mapping business motivation (goals, drivers, assessments) to executable change.
- Producing a business architecture that feeds the enterprise target state.
- Ensuring traceability from business objectives to IT investment.
- Defining the organizational and process view that applications must support.

Does NOT apply to: the application portfolio (use
[application-architect](../../domains/application-architect/SKILL.md)), or the
enterprise-wide frame (use
[enterprise-architect](../enterprise-architect/SKILL.md)).

---

## 2. Core Models

- **Business capabilities** — what the business can do, expressed as a
  stable, technology-agnostic capability map. Capabilities change slowly;
  processes and systems change around them.
- **Value streams** — the end-to-end sequences that deliver value to a
  customer or stakeholder, and the capabilities each stage stages.
- **Business motivation** — goals, objectives, drivers and assessments, modeled
  separately from the solutions that realize them.
- **Business processes** — the executable flows, governed in coordination with
  process ownership and automation.

---

## 3. Method (TOGAF ADM Phase B)

1. **Baseline** the current business architecture: capabilities, value streams,
   organization map, business processes.
2. **Target** the business architecture for the strategic horizon.
3. **Gap analysis** between baseline and target.
4. **Feed the enterprise frame**: the business architecture is the primary input
   to the enterprise target state and the investment plan.
5. **Trace** every downstream application and technology decision back to a
   capability and a value stream.

---

## 4. Orchestration and Handoffs

| Concern | Owning skill |
|---|---|
| Enterprise frame, principles, target across domains | [enterprise-architect](../enterprise-architect/SKILL.md) |
| Application portfolio realizing the capabilities | [application-architect](../../domains/application-architect/SKILL.md) |
| Data assets behind the value streams | [data-architect](../../domains/data-architect/SKILL.md) |
| Business process automation, ERP/BPM | [academic-enterprise-information-systems](../../../domains/academic/academic-enterprise-information-systems/SKILL.md) |
| Requirements and backlog refinement | [product-owner](../../../roles/product-owner/SKILL.md) |

In one line: the Business Architect supplies the **why and what**; the
Enterprise Architect converts it into **how across the enterprise**.

---

## 5. Reference Frameworks

- **TOGAF** — ADM Phase B (Business Architecture), Business Architecture
  guidance; see [ea-frameworks](../enterprise-architect/references/ea-frameworks.md)
  for the resolved version.
- **ArchiMate** — the modeling language: Business layer (actor, role, business
  object, capability, value stream).
- **BPMN** — the notation for executable business processes.
- **Business architecture body of knowledge** — a recognized BoK for the
  discipline (pin the edition before citing; see `version-freshness`).

Resolve every version before citing it; mark an unresolved pin `unverified`.

---

## 6. Common Mistakes

| Mistake | Correction |
|---|---|
| Jumping to systems before modeling capabilities | Capabilities and value streams come first |
| Mixing motivation with solution | Goals and drivers are modeled separately from systems |
| Treating capabilities as processes | Capabilities are stable; processes change |
| Skipping traceability to IT investment | Every application must trace to a capability |
| Citing a BoK edition from memory | Resolve the edition in-session |
