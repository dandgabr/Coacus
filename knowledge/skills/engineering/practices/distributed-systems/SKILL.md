---
name: "distributed-systems"
description: "Provides expert patterns for distributed systems based on Distributed Systems (van Steen & Tanenbaum) and Distributed systems: principles and paradigms, covering architecture styles, processes and virtualisation, communication (RPC, messaging, streams, multicast), naming (DNS, DHT, LDAP), coordination (physical/logical clocks, mutual exclusion, election, gossip), consistency and replication (sequential/causal/eventual, client-centric models, primary-based and replicated-write protocols, quorum), fault tolerance (failure models, Paxos/Raft, PBFT, 2PC/3PC, checkpointing) and the eight fallacies."
---

# AI Skill: Distributed Systems Engineering

This skill guides the AI to reason about partial failure, ordering and consistency explicitly, and to choose coordination mechanisms whose cost matches the requirement. It builds on *Distributed Systems* (van Steen & Tanenbaum).

---

## 🧭 When to Activate

- Designing or debugging anything spanning processes, nodes or regions.
- Choosing consistency/replication protocols for a data store.
- Reasoning about clocks, ordering, and causal delivery.
- Selecting a coordination primitive (mutex, election, consensus, distributed commit).
- Auditing assumptions that make distributed code fail in production.

---

## 🎯 Design Goals and Fallacies

Goals: resource sharing, **distribution transparency**, openness (interoperability/composability/extensibility via a complete, neutral **IDL**), dependability, security, scalability. Scalability techniques: hide latency, distribute (partition), replicate + cache (caching is a special case of replication; both create consistency problems).

**Deutsch's eight fallacies** — treat every one as false: the network is reliable, is secure, is homogeneous, has a stable topology, has zero latency, has infinite bandwidth, has zero transport cost, and has one administrator. **Full failure transparency is provably impossible** — partial failure is intrinsic. **Copy-before-use (Wams):** access data only after transferring it locally, and never modify in place.

---

## 🏗️ Architecture, Processes, Communication

- **Styles:** layered; service-oriented (SOA); publish-subscribe; symmetric P2P (structured — Chord/consistent hashing, unstructured — gossip) and hybrid (cloud, edge-cloud, blockchain).
- **Processes:** threads vs processes; multithreaded servers; **virtualisation** — VMs virtualise hardware, containers virtualise the OS; server clusters; code migration (weak vs strong mobility).
- **Communication:** RPC (client/server stubs, marshalling; synchronous vs **asynchronous** RPC) realises *access transparency*; message-oriented transient (sockets) vs **persistent** (queues, AMQP); stream-oriented with **QoS**; multicast (application-level **tree-based**, **flooding**, **gossip/anti-entropy**).

---

## 🏷️ Naming

Flat naming (broadcast, **DHT** consistent hashing), structured naming (name spaces, recursive vs iterative resolution — **DNS**, **NFS**), attribute-based naming (**LDAP**), and named-data networking. Names vs identifiers vs addresses are distinct.

---

## ⏱️ Coordination

- **Physical clocks:** UTC/TAI, clock skew; synchronization algorithms (Cristian's, NTP, **RBS**). Physical synchronization is bounded, never exact.
- **Logical clocks:** **Lamport** scalar clocks (happens-before); **vector clocks** — `ts(a) < ts(b)` iff all components ≤ and at least one `<`; used for causal delivery and conflict detection.
- **Mutual exclusion:** centralized; distributed (**Ricart–Agrawala**); **token-ring**; decentralized.
- **Election:** **bully**, ring; **Raft leader election** (follower/candidate/leader, terms, heartbeats, randomized timeouts to avoid split votes).
- **Gossip-based coordination:** aggregation, peer-sampling, overlay construction.

---

## 🔁 Consistency, Replication, Fault Tolerance

- **Data-centric models:** **sequential consistency** (a sequential order preserving program order; time plays no role), causal, FIFO, **eventual**, continuous (bounded staleness/numerical/ordering deviation).
- **Client-centric models:** **monotonic reads**, **monotonic writes**, **read your writes**, **writes follow reads**.
- **Consistency protocols:** **primary-based** (remote-write, local-write), **replicated-write** (active/passive, **quorum**), cache coherence.
- **Failure models:** crash, omission, timing, response; refinements **fail-stop**, **fail-noisy**, **fail-safe**, **fail-arbitrary**; masking by redundancy (information, time, physical).
- **Consensus:** crash-fault consensus (majority), **Paxos**, **Raft**; **Byzantine agreement** needs **> 3k+1** nodes for k faulty; **PBFT**; blockchain consensus.
- **Reliable RPC semantics under failure:** at-most-once, at-least-once, exactly-once (retransmission + duplicate detection, idempotent servers).
- **Atomic multicast** (virtually synchronous, totally ordered); **distributed commit**: **two-phase commit (2PC)** blocks on coordinator crash — 3PC improves liveness.
- **Recovery:** **checkpointing** (coordinated/independent), **message logging**, recovery-oriented computing.

---

## ⚠️ Pitfalls

- Assuming reliable, ordered delivery without sequence numbers or acknowledgements.
- Using wall-clock timestamps for ordering across nodes.
- Reaching for strong consistency (a round-trip) when eventual consistency suffices — and vice versa.
- Forgetting that 2PC blocks and consensus needs a majority (and Byzantine agreement > 3k+1).
- Treating a cache as a source of truth without an invalidation strategy.

---

## 🔗 Integration with Other Skills

- For distributed SQL/NoSQL, replication and sharding, see [data-intensive-systems](../../../data/data-intensive-systems/SKILL.md) and [system-design-scalability](../system-design-scalability/SKILL.md).
- For event-driven/streaming integration, see [realtime-streaming-event-driven](../../../data/realtime-streaming-event-driven/SKILL.md).
- For functional concurrency primitives (actors, futures), see [functional-concurrent-programming](../functional-concurrent-programming/SKILL.md).
- For API contracts across services, see [api-design](../api-design/SKILL.md).
