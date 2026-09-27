---
name: "flow-architectures"
description: "Provides expert patterns for flow architectures and event-driven integration based on Flow Architectures (James Urquhart). Covers the definition of flow (standard interfaces, self-service streams, push delivery), the signal/event/event-stream primitives, the logical connection and discovery interfaces, Wardley mapping and promise theory, and the flow service taxonomy (Collector, Distributor, Signal, Facilitator) with edge-computing and retention concerns."
---

# AI Skill: Flow Architectures and Event-Driven Integration

This skill guides the AI to design integration that is loosely coupled and adaptable through event streams, and to distinguish *eventing* from *messaging*. It builds on *Flow Architectures: The Future of Streaming and Event-Driven Integration* (Urquhart).

---

## 🧭 When to Activate

- Designing integration between systems or organizations.
- Deciding between request/response APIs and event streams.
- Modeling an event-driven platform or a data-distribution topology.
- Reasoning about where processing should live (cloud vs edge).

---

## 🌊 What Flow Is

**Flow** is event-driven, loosely coupled, highly adaptable integration via **standard interfaces and protocols**. Consumers request streams through **self-service interfaces**; producers accept or reject; once connected, data is **pushed**; producers retain control over what, when, and to whom.

Primitives:
- **Signal** — an indication that state changed.
- **Event** — a signal plus context (timestamp, identity).
- **Event stream** — a series of events; a **raw data stream** vs an **event stream** differs by whether context is embedded or added by the consumer.

---

## 🔌 Interfaces and Protocols

Two required **interfaces**:
1. **Logical connection** — negotiate, establish, subscribe, close (contrast the *physical connection* handled by infrastructure).
2. **Discovery** — find streams and describe their properties (volume, schema, fees).

Two **protocol parts**: a **metadata format** and a **payload format**.

---

## 🗺️ Modeling Value and Trust

- **Wardley Mapping**: identify scope and user need, plot components by evolution from novel to commodity, and use it to reason about where a flow service sits.
- **Promise Theory** (Burgess): autonomous agents; a promisor makes a promise to a promisee; the promise **body** = quality + quantifier; reciprocal `+Body`/`−Body`; no promise can be imposed. This frames producer/consumer contracts in flow.

---

## 🏗️ Flow Service Taxonomy

- **Collector** — one consumer subscribes to topics from **many producers** (IoT, inventory, trading). Scaling concerns many inputs and who initiates.
- **Distributor** — one stream broadcast to **many consumers** (stock ticker, weather). Reverse scaling problem; latency/bandwidth push toward **edge computing**; regional partitioning; optional synchronize-then-publish.
- **Signal** — a traffic-cop processor routing events from producers to consumers; observability and complexity are the risks; tends to evolve from a centralized pane of glass toward composable, domain-managed platforms.
- **Facilitator** — a specialized Signal acting as a broker matching sellers with buyers (e.g. logistics); raises the double-sale/transaction-exclusivity question.

---

## 🧩 Design Concerns

- **Event-first use cases** differ by messaging vs eventing, discrete events vs event series, and single actions vs workflows.
- **Security, agility, timeliness, manageability**, memory (state rebuilt from the stream), and IP control.
- **Retention policy** on in-motion events.
- **Edge computing and flow are codependent** — localizing processing reduces the round-trip that flow would otherwise require.

---

## ⚠️ Pitfalls

- Confusing messaging (point-to-point commands) with eventing (published facts).
- Designing discovery last — without it, consumers cannot self-serve.
- Assuming one centralized event router scales indefinitely.
- Ignoring retention and replay policy, then being unable to rebuild state or audit.

---

## 🔗 Integration with Other Skills

- For streaming engines and CDC, see [realtime-streaming-event-driven](../../../data/realtime-streaming-event-driven/SKILL.md).
- For consistency and delivery guarantees, see [distributed-systems](../distributed-systems/SKILL.md).
- For event-based API style and governance, see [api-design](../api-design/SKILL.md).
- For event-sourced domain design, see [architecture-ddd](../architecture-ddd/SKILL.md).
