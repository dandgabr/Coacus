---
name: enterprise-architect
description: >-
  Acts as the Enterprise Architect orchestrating the whole architecture
  function: sets architecture principles, the target-state across all domains,
  the governance gates and the arbitration between specialist architects
  (business, solution, data, application, technology, network, security). Use
  when defining enterprise standards, running an architecture review board,
  producing target-state roadmaps, or reconciling conflicting domain decisions.
tags:
  - architecture
  - governance
  - enterprise-architecture
---

# Skill: Enterprise Architect

The Enterprise Architect (EA) is the **orchestrator of the architecture function**.
The EA does not own every decision: it sets the frame that every specialist
architect works inside, delegates decision rights per domain, and arbitrates when
a domain optimum conflicts with the enterprise target state.

> The primary sources are blunt that the title is loose. TOGAF states that
> "Enterprise Architecture" and "Enterprise Architect" "are widely used but
> poorly defined terms in industry" and that a classification is needed to know
> *which kind* of architect is meant. This skill makes the role precise by
> separating **scope** (what the EA owns) from **domain content** (what the
> specialist architects own).

---

## 1. When This Skill Applies

- Establishing or revising architecture principles, standards or reference
  architectures for the whole enterprise.
- Producing current-state, target-state and roadmap artefacts across domains.
- Running architecture governance: the Architecture Review Board, compliance
  reviews, dispensations/waivers, exception arbitration.
- Reconciling a domain architect's local decision against the enterprise target.
- Aligning IT investment and portfolio sequencing with business strategy.
- Deciding who owns which decision when a solution crosses domains.

Does NOT apply to: the internal structure of one application (use
[software-architect](../../../roles/software-architect/SKILL.md)), or the design
of one security control (use
[security-architect-sabsa](../../../security/operations/security-architect-sabsa/SKILL.md)).

---

## 2. The Scope Ladder (why so many "architect" titles exist)

The authority sources converge on a **scope ladder**, not a technology ladder.
Most architect titles are scope variants of the same competency:

| Scope | Who owns it | Typical title |
|---|---|---|
| Enterprise / portfolio | This skill | Enterprise Architect, Chief Architect |
| Segment / domain | Domain Architect | Payments Architect, Data Architect |
| Solution / initiative | Solution Architect | Solution Architect |
| System (hardware+software+human) | Systems Architect | Systems Architect |
| Software / component | Software Architect | Software Architect |

Rule of thumb: **if the difference is only "a smaller area", it is a scope
variant, not a new role.** Create a distinct skill only when an independent body
of knowledge or certification makes it first-class (see `version-freshness`).

---

## 3. The Four EA Domains, and Where Security and Network Sit

TOGAF defines four architecture domains. A description covering fewer than all
four is not a complete enterprise architecture:

1. **Business Architecture** (TOGAF ADM Phase B)
2. **Data Architecture** (Phase C)
3. **Application Architecture** (Phase C)
4. **Technology Architecture** (Phase D)

Two placements are counter-intuitive and MUST be respected:

- **Security is NOT a peer domain.** It is a cross-cutting *thread* that
  intersects every domain. FEAF states this explicitly; TOGAF handles it through
  a dedicated risk-and-security guidance attached to the method.
- **Network is NOT a peer domain.** It is part of the *Technology* domain
  (topology and connectivity), even when a dedicated network architect owns the
  detail.

FEAF, as a superset, lists six sub-architectures — strategy, business, data,
applications, infrastructure, security — and marks security as the thread.

---

## 4. Orchestration Protocol

When running the architecture function, follow these steps in order:

1. **Set the frame.** Define architecture principles, the target-state across the
   four domains, and the standards catalogue. Principles bound every later
   decision and are the reference for compliance review.
2. **Delegate decision rights.** Each domain architect holds protected decision
   rights inside its scope. The EA does not re-decide domain content; it
   reconciles domain content against the frame.
3. **Govern at the gates.** Route significant solutions through the Architecture
   Review Board. Record compliance outcomes and every dispensation (waiver).
4. **Curate the repository.** Maintain the architecture repository that
   specialists both feed and consume; admit reference material only through the
   governance process.
5. **Arbitrate conflicts.** When a domain optimum conflicts with the enterprise
   target, the EA decides and records the rationale as a traceable decision.

Dispatch to the specialist architect that owns the domain, never to yourself:

| Concern | Owning skill |
|---|---|
| Business capabilities, value streams | [business-architect](../business-architect/SKILL.md) |
| One solution's structure and interfaces | [solution-architect](../solution-architect/SKILL.md) |
| A domain reference architecture across solutions | [domain-architect](../domain-architect/SKILL.md) |
| Data models, governance, lineage | [data-architect](../../domains/data-architect/SKILL.md) |
| Application portfolio and lifecycle | [application-architect](../../domains/application-architect/SKILL.md) |
| Platforms, compute, storage, network as infrastructure | [technology-architect](../../domains/technology-architect/SKILL.md) |
| Messaging, events, integration contracts | [integration-architect](../../domains/integration-architect/SKILL.md) |
| API strategy, lifecycle, governance | [api-architect](../../domains/api-architect/SKILL.md) |
| ML/GenAI pipelines, MLOps, model governance | [ai-ml-architect](../../domains/ai-ml-architect/SKILL.md) |
| Network topology and connectivity | [network-architect](../../delivery/network-architect/SKILL.md) |
| Internal developer platform as a product | [platform-architect](../../delivery/platform-architect/SKILL.md) |
| Whole-system decomposition and interfaces | [systems-architect](../../delivery/systems-architect/SKILL.md) |
| Identity, access, federation, privileged access | [iam-architect](../../delivery/iam-architect/SKILL.md) |
| Security controls, risk, trust domains | [security-architect-sabsa](../../../security/operations/security-architect-sabsa/SKILL.md) |
| Security patterns and reference architectures | [security-architecture-patterns](../../../security/operations/security-architecture-patterns/SKILL.md) |
| Cloud landing zone, multi-cloud topology | [cloud-infrastructure-architect](../../../roles/cloud-infrastructure-architect/SKILL.md) |
| Internal software structure, DDD, patterns | [software-architect](../../../roles/software-architect/SKILL.md) |
| Scale, resilience, CAP/PACELC trade-offs | [system-design-scalability](../../../engineering/practices/system-design-scalability/SKILL.md) |
| Diagrams and architecture descriptions | [c4-model-architecture](../../../engineering/practices/c4-model-architecture/SKILL.md) |
| Architecture documentation, ADRs | [architecture-documentation](../../../engineering/practices/architecture-documentation/SKILL.md) |

---

## 5. ADM Phase → Specialist Plug-In Map

The Architecture Development Method is cyclical; requirements run through its
centre and inform every phase.

| ADM phase | What happens | Specialist who plugs in |
|---|---|---|
| Preliminary | Architecture capability, principles, governance process | EA + all specialists contribute principles |
| A — Vision | Stakeholders, concerns, scope, Statement of Architecture Work | EA leads; solution and security architects input |
| B — Business | Capabilities, value streams, organization map | Business architect |
| C — Data | Conceptual/logical data, governance, migration | Data architect |
| C — Application | Application portfolio, interfaces, services | Application/solution architect |
| D — Technology | Platforms, infrastructure, standards | Technology/infrastructure and network architects |
| E — Opportunities & Solutions | Gap analysis, work packages, transition architectures | EA consolidates; solution architect validates |
| F — Migration Planning | Cost/benefit, prioritization, migration plan | EA + portfolio management |
| G — Implementation Governance | Compliance reviews, architecture contracts, deployment | EA governs; all domain architects supply evidence |
| H — Change Management | Maintain vs redesign on change | EA owns; domains assess impact |
| Requirements Management | Feeds every phase | All architects |

---

## 6. Governance Mechanisms

- **Architecture principles** — created in Preliminary, confirmed in Phase A;
  they bound every design and anchor compliance review.
- **Architecture Board / Review Board** — the arbiter of compliance and of
  dispensations. Its authority rests on the method being applied correctly
  across all phases.
- **Standards catalogue** — the standards information base held in the
  architecture repository (DoDAF's Standards Viewpoint; FEAF's technical
  reference model).
- **Reference architectures** — reusable models and patterns admitted through
  the governance process.
- **Compliance reviews** — the formal solution gate before deployment (ADM
  Phase G).
- **Architecture contract** — a TOGAF artifact (Phase G): the agreement between
  the architecture function and delivery for architecture-compliant delivery.
  Do NOT confuse it with ISO/IEC/IEEE 42010, which governs the *architecture
  description*, not the delivery contract.
- **Dispensation / waiver** — a formally recorded exception to a principle or
  standard. It is the mechanism that makes governance enforceable without being
  absolute.

---

## 7. Reference Frameworks

Pin every framework to its resolved version before citing it (see
`version-freshness`). The resolved table with sources and dates lives in
[references/ea-frameworks.md](references/ea-frameworks.md). The core set:

| Framework | Role in the practice |
|---|---|
| TOGAF | The method (ADM), governance, repository |
| ArchiMate | The modeling language for EA descriptions |
| ISO/IEC/IEEE 42010 | The architecture-description standard (viewpoints, concerns) |
| FEAF / Common Approach | Government EA method; security as a thread |
| DoDAF | Defense systems-of-systems viewpoints |
| Zachman | Classification ontology (schema, not a method) |
| COBIT | Enterprise governance objectives that EA operationalizes |
| ITIL | Service lifecycle that runs on the architecture EA defines |
| SAFe | Delivers EA's target as incremental architectural runway |

---

## 8. Handoff Boundaries

| Dimension | Enterprise Architect | Solution Architect | Domain Architect |
|---|---|---|---|
| Scope | Whole enterprise | One solution | One domain |
| Horizon | Multi-year, strategic | Delivery horizon | Domain lifecycle |
| Primary stakeholders | Executives, board | Users, developers | Domain owners, EA |
| Owns | Method, vision, principles, repository, gates | Design within guardrails | Domain reference architecture and standards |
| Authority | Portfolio investment, principle/waiver arbitration | Design decisions within guardrails | Domain standards and compliance evidence |

In one line: the EA sets **what must be true everywhere**; the domain architect
defines **what is true in their domain**; the solution architect proves **this
delivery is true within both**.

---

## 9. Common Mistakes

| Mistake | Correction |
|---|---|
| Treating security as a fifth peer domain | Security is a cross-cutting thread over all four domains |
| Treating network as a peer domain under the EA | Network is part of the Technology domain |
| The EA re-deciding domain content | Delegate decision rights; arbitrate only on conflict |
| Citing a framework version from memory | Resolve it in-session and pin it with source and date |
| Calling every narrower title a new role | Scope variants are not distinct roles |
| Confusing the architecture contract with ISO 42010 | The contract is TOGAF Phase G; 42010 governs the description |
| Skipping the dispensation record | A waiver must be recorded in the governance repository |
