---
name: integration-architect
description: >-
  Acts as the Integration Architect owning how systems talk: messaging, APIs,
  events, ETL and streaming, canonical data models and interface contracts, plus
  integration governance and versioning. Use when defining integration patterns
  and standards, designing an event backbone, governing interface contracts, or
  ensuring reliable, idempotent and observable integrations.
tags:
  - architecture
  - integration-architecture
---

# Skill: Integration Architect

The Integration Architect owns the **horizontal specialty of how systems
communicate**: messaging, events, APIs, batch and streaming, canonical models
and interface governance. It is a domain that cuts across every solution.

---

## 1. When This Skill Applies

- Defining integration patterns and standards (sync/async, messaging, events).
- Owning the canonical data model and interface contracts.
- Governing integration platforms (message broker, event bus, API gateway).
- Ensuring reliable, idempotent and observable integrations.
- Managing interface versioning and compatibility.

Does NOT apply to: API product strategy and lifecycle (use
[api-architect](../api-architect/SKILL.md)), or the internal structure of one
service (use [software-architect](../../../roles/software-architect/SKILL.md)).

---

## 2. Style Selection

| Style | When it fits | Watch out for |
|---|---|---|
| Request/response (REST, gRPC) | Synchronous, query-like interactions | Coupling, cascading failure |
| Messaging / queues | Work distribution, decoupling | Ordering, idempotency |
| Event streaming | High-volume, replay, analytics | Schema evolution, ordering |
| Batch / ETL | Large periodic movements | Latency, windowing |
| File / SFTP | Legacy and partner exchange | Reliability, security |

Choose the style from the interaction semantics, not from fashion. Every
integration must define idempotency, delivery guarantee and observability.

---

## 3. Method

1. **Map** the systems and the information that must move between them.
2. **Define** the integration patterns and the canonical model.
3. **Govern** interface contracts, versioning and compatibility rules.
4. **Ensure** reliability semantics (at-least-once vs. exactly-once),
   idempotency and dead-letter handling.
5. **Observe**: correlation identifiers, tracing and integration metrics.

---

## 4. Orchestration and Handoffs

| Concern | Owning skill |
|---|---|
| Enterprise frame and standards | [enterprise-architect](../../enterprise/enterprise-architect/SKILL.md) |
| API strategy, gateway, lifecycle | [api-architect](../api-architect/SKILL.md) |
| REST contract design | [framework-rest-api](../../../frameworks/framework-rest-api/SKILL.md) |
| gRPC contracts | [framework-grpc](../../../frameworks/framework-grpc/SKILL.md) |
| GraphQL schemas | [framework-graphql](../../../frameworks/framework-graphql/SKILL.md) |
| Streaming and event-driven architecture | [realtime-streaming-event-driven](../../../data/realtime-streaming-event-driven/SKILL.md) |
| Microservices patterns | [distributed-systems](../../../engineering/practices/distributed-systems/SKILL.md) |
| Data flows and lineage | [data-architect](../data-architect/SKILL.md) |

---

## 5. Reference Frameworks

- **Enterprise integration patterns** — the classic messaging/patterns
  catalogue (resolve the edition; see `version-freshness`).
- **Microservices patterns** — distributed system patterns.
- **OpenAPI, gRPC/protobuf, AsyncAPI** — the contract notations; resolve the
  version before citing.
- **TOGAF / ArchiMate** — for placement in the enterprise description.

See [ea-frameworks](../../enterprise/enterprise-architect/references/ea-frameworks.md).

---

## 6. Common Mistakes

| Mistake | Correction |
|---|---|
| Picking a style by fashion | Choose from interaction semantics |
| No idempotency on retries | Define idempotency and delivery guarantees |
| Breaking interface changes silently | Govern versioning and compatibility |
| No correlation/tracing | Integration must be observable |
| Scattering point-to-point links | Prefer governed, reusable interfaces |
