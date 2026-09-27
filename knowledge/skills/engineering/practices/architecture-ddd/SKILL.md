---
name: "architecture-ddd"
description: "Provides expert patterns for software architecture and Domain-Driven Design based on Domain-Driven Design Distilled (Vernon), Domain Storytelling, Balancing Coupling in Software Design (Khononov), Head First Software Architecture, and Effective Software Architecture (Goldman). Covers bounded contexts, ubiquitous language, context mapping, aggregates and domain events, event storming and domain storytelling, coupling strength/distance/volatility, architectural characteristics and styles, and Architecture Decision Records."
---

# AI Skill: Software Architecture and Domain-Driven Design

This skill guides the AI to design systems around the domain model, draw explicit boundaries, and treat every architectural choice as a documented trade-off. It builds on *Domain-Driven Design Distilled* (Vernon), *Domain Storytelling* (Hofer & Schwentner), *Balancing Coupling in Software Design* (Khononov), *Head First Software Architecture* (Gandhi, Richards & Ford), and *Effective Software Architecture* (Goldman).

---

## 🧭 When to Activate

- Boundary, decomposition or context-mapping decisions (monolith vs microservices).
- Designing entities, value objects, aggregates and domain events.
- Running event storming or domain-storytelling workshops to find subdomains.
- Evaluating coupling and modularity of an existing design.
- Recording and reasoning about architectural decisions.

---

## 🧱 Domain-Driven Design

**Strategic design** = Bounded Contexts, Ubiquitous Language, Subdomains, Context Mapping. **Tactical design** = Aggregates, Entities, Value Objects, Domain Events, Event Sourcing.

- **Ubiquitous Language:** one team-owned language whose written form is the code. Language boundaries are **Bounded Contexts**: one team, one repository, one schema per context. "Policy" in Underwriting, Inspections and Claims is three distinct models — name each simply within its context. Unbounded models become a **Big Ball of Mud**.
- **Subdomains:** **Core** (differentiator, best resources), **Supporting** (custom, not differentiating), **Generic** (buy/off-the-shelf). Aim for 1:1 Bounded Context ↔ Subdomain; if two models must share a context, segregate in separate **Modules**.
- **Context Mapping:** Partnership, Shared Kernel, Customer-Supplier, Conformist, **Anticorruption Layer** (preferred for downstream), Open Host Service, Published Language, Separate Ways. Avoid Big Ball of Mud.
- **Aggregate rules of thumb:** (R1) protect invariants inside the boundary; (R2) design **small** aggregates; (R3) reference other aggregates **by identity only** (`ProductId`); (R4) update other aggregates via **eventual consistency** (publish an event, a separate transaction updates the other aggregate). Avoid the **Anemic Domain Model** — business logic belongs in the model, not in application services.
- **Domain Events & Event Sourcing:** an aggregate changes state and publishes its event in the **same transaction** (aggregate row + event-store row). A command can be rejected; an event is history and cannot. Event Sourcing persists the event stream, reconstitutes by re-applying, and (with **snapshots**) gives high throughput; it obliges **CQRS**. Consumers must handle causality (sequence/causal id).
- **Architecture inside a context:** Ports and Adapters — input adapters → application services (use cases, transactions) → domain model (technology-free) → output adapters. Microservices ≈ Bounded Contexts.

**Event Storming** (Brandolini): sticky-note, event-centric, domain experts + developers in one room; orange events, commands, actors, policies, hotspots; timeboxed, cheap to refine.

**Domain Storytelling** (Hofer & Schwentner): a pictographic language — Actor, Work Object, Activity (verb), Sequence Number, Annotation, Group. Sentence grammar is subject–predicate–object. Give every sentence its own work object; avoid loopbacks and request/response patterns. Scope along *Granularity* (coarse/medium/fine), *Point in Time* (As-Is/To-Be) and *Domain Purity* (pure business / digitalized). Journey: explore (coarse, as-is) → drill into subdomains (fine, as-is) → introduce software (fine, to-be). Derive subdomain boundaries "from an actor's perspective," then Bounded Contexts and team boundaries; extract user stories and a story map.

---

## ⚖️ Balancing Coupling (Khononov)

`MAINTENANCE EFFORT = STRENGTH × DISTANCE × VOLATILITY` — any zero dimension neutralizes the pain.

- **Integration strength** (shared knowledge): Intrusive > Functional > Model > **Contract** (weakest, interface only).
- **Distance** = cost of changing one component in response to another (encapsulation, lifecycle, socio-technical separation, runtime coupling).
- **Volatility** = rate of change (solution + problem changes); infer from domain analysis and source-control history; watch **asymmetric volatility**.
- **Connascence** (static: Name, Type, Meaning, Algorithm, Position; dynamic: Execution, Timing, Value, Identity) — convert stronger to weaker (position → name). Structured-design module coupling worst→best: Content, Common, External, Control, Stamp, Data.
- Good shapes: low-strength + high-distance + high-volatility (loose); high-strength + low-distance + high-volatility (contained); high-strength + high-distance + low-volatility (legacy integration). Bad: high×high×high (global complexity) and low-strength/low-distance/high-volatility (local complexity).

---

## 🏛️ Architectural Characteristics and Styles (Head First)

Four dimensions: architectural **characteristics**, **decisions**, **logical components**, **styles**.

- **Characteristics** are the "-ilities" (quality attributes) — nondomain design considerations that shape structure. Limit their number and prioritize them contextually (map them to components). Sources: problem domain, environmental awareness, holistic domain knowledge.
- **Two laws:** (1) *everything in software architecture is a trade-off* (no best practices); (2) **why is more important than how**.
- **ADRs** capture decisions: Title, Status, Context, Decision, Consequences, Governance, Notes. The ADR log is the story of the architecture.
- **Logical components:** identify real components, avoid the **entity trap** (vague "Manager" components); analyze roles, responsibilities, cohesion and coupling (afferent/efferent; Law of Demeter).
- **Style grid** — Partitioning (Technical vs Domain) × Deployment (Monolith vs Distributed): **Layered** (technical monolith; kryptonite = scalability), **Modular Monolith** (domain monolith), **Microkernel** (core + plugins via a plugin registry), **Event-Driven** (broker vs mediator topology), **Microservices** (granularity, orchestration vs choreography, distributed DB, saga). Know each style's superpowers and kryptonite.

**Effective Software Architecture (Goldman):** architecture is a discipline of **constraint + accelerator**, not a priesthood. Dependability is an implementation attribute the architecture *enables*; capture Architecturally Significant Requirements. **Technical debt is not investment debt** — it is under-investment with ongoing cost. Practice: document the system, work toward a vision, write change proposals, maintain a backlog, consider alternatives, decide *not* to do things. Decision heuristics: Will more info help? Cost of not doing it? Cost of getting it wrong? Is it my decision? Can I document it?

---

## ⚠️ Pitfalls

- Merging genuinely different meanings into one context; unbounded models.
- Premature/wrong abstractions before change forces them.
- Anemic domain models and business logic leaking into services.
- Defaulting to layered monolith or microservices without evaluating characteristics and scaling.
- Recording *what* was decided but not *why*.

---

## 🔗 Integration with Other Skills

- For tactical design patterns and refactoring to abstractions, see [empirical-software-design](../empirical-software-design/SKILL.md) and the [dp-* pattern skills](../../patterns/dp-behavioral-patterns/SKILL.md).
- For hexagonal/ports-and-adapters implementation, see [clean-architecture](../clean-architecture/SKILL.md).
- For documenting architecture with C4, see [c4-model-architecture](../c4-model-architecture/SKILL.md) and [architecture-documentation](../architecture-documentation/SKILL.md).
- For distributed/event-driven styles, see [distributed-systems](../distributed-systems/SKILL.md) and [realtime-streaming-event-driven](../../../data/realtime-streaming-event-driven/SKILL.md).
