---
name: data-intensive-systems
description: Specializes in Data-Intensive Systems (Reliability, Scalability, and Maintainability) based on Designing Data-Intensive Applications, 2nd Edition (Martin Kleppmann & Chris Riccomini). Covers data models and query languages, storage engines (LSM-Tree, B-Tree, column stores), encoding and schema evolution, replication, partitioning/sharding, ACID transactions and isolation (snapshot isolation, SSI serializability), consistency and consensus (Raft, linearizable consensus), batch and stream processing (log-structured, CDC, exactly-once), stream-system philosophy, and data ethics.
---

# AI Skill: Data-Intensive Systems (Data-Intensive Applications)

This skill guides the artificial intelligence to design, evaluate, and operate systems whose primary challenge is **data quantity, complexity, and velocity** (not CPU-intensive), based on *Designing Data-Intensive Applications, 2nd Edition* (Martin Kleppmann & Chris Riccomini, O'Reilly 2026).

---

## 🏛️ 1. Foundations: Reliability, Scalability, Maintainability

- **Trade-offs in data systems** (ch. 1): every choice — SQL vs NoSQL, consistency vs latency, batch vs stream — is a trade-off; the decision driver is the **non-functional requirements** (latency SLOs, throughput, availability).
- **Reliability**: tolerate hardware, software, and human failures with chaos testing, graceful degradation, and verified recovery.
- **Scalability**: describe load with parameters (RPS, hit ratio, cardinality) and assess how growing 10× affects each layer; performance via percentiles (p50/p99) and steady-state throughput.
- **Maintainability**: operate through simplicity (abstractions that hide accidental complexity), evolvability, and operational transparency.

---

## 🗃️ 2. Data Models, Storage, and Encoding

### Models and query languages
- **Relational vs Document vs Graph**: documents reflect local structures (one-to-many) with a flexible schema; relational normalizes and supports joins and a strong optimizer; graphs (Cypher/SPARQL) naturalize recursive navigation and many-to-many.
- Choose by the **domain's data shape and access pattern**, not by fashion.

### Storage engines
- **LSM-Tree (log-structured)**: fast sequential writes, high compression; pays with compactions, write amplification, and latency variance (compaction stalls).
- **B-Tree**: predictable reads, mature strong transactions; pays write amplification across random pages and the write-ahead log.
- **Secondary indexes, clustering, column-oriented**: column stores compress and crunch analytics (vectorized execution); row stores optimize OLTP per row.
- **Hash vs range partitions** on disk; bloom filters to avoid empty lookups in LSM.

### Encoding and schema evolution
- **Encoding schemes**: JSON/XML are readable but verbose; binary formats (Protocol Buffers, Avro, Thrift) are compact and typed.
- **Evolution (rolling upgrades)**: *backward* compatibility (new reader reads old data) and *forward* compatibility (old reader reads new data) — regulate with `optional` fields and numbered fields (Avro: writer/reader schema; schema registry).
- **Mature dataflows**: through the database (data outlives the code), REST/RPC (versioned contracts), event streaming (immutable events with a versioned schema).

---

## 🔁 3. Replication and Partitioning

### Replication
| Strategy | Description | Central trade-off |
| :--- | :--- | :--- |
| **Single-leader** | Writes go to the leader; replicas follow the log | Simple; lag and failover with possible loss |
| **Multi-leader** | Several leaders accept writes | Multi-DC writing; conflicts that need resolution (LWW/CRDT/hook) |
| **Leaderless (Dynamo-style)** | Client writes to a quorum | High availability; quorum `W+R>N`, read repair, anti-entropy |

- Guarantee semantics: read-your-writes, monotonic reads, consistent prefix reads — implementable via sticky sessions or version tokens.
- **Failure detection** (timeouts) and **failover consensus** (avoid split brain with epoch/fencing tokens).

### Partitioning (sharding)
- **By key (hash) vs by range**: hash distributes load evenly but kills range queries; range preserves queries but creates hotspots.
- **Skew and hotspots**: mitigate with salting, composite partitioning (e.g. (user_id, timestamp)), and dynamic-gravity shards.
- **Rebalancing**: a fixed hash-mod strategy ages badly; use consistent hashing or fixed partitions (more partitions than nodes) for cheap migration.
- **Cross-shard queries**: scatter/gather is costly; design schemas with "transactional locality" (data kept together in the aggregate's shard) and global secondary indexes (document-based vs term-based).
- **Rebalancing and consistency**: move data with a "dual-write + backfill + cutover" protocol, avoiding dirty reads during migration.

---

## 🛡️ 4. Transactions and Isolation

- **Isolation levels and anomalies**: dirty reads, lost updates, write skew, phantom reads — each level (READ COMMITTED, REPEATABLE READ, SERIALIZABLE) denies a set of anomalies.
- **Snapshot Isolation (MVCC)**: consistent snapshot reads without blocking writers; implementations: PostgreSQL, Oracle; enduring in distributed DBs (Spanner, FoundationDB).
- **Serializable Snapshot Isolation (SSI)**: rw/ww conflict detection plus rethrows — serializability with the performance of SI.
- **Distributed transactions**: blocking 2PC; semi-asynchronous alternatives: Percolator, Spanner (TrueTime + 2PC), Calvin (deterministic pre-ordering).
- **Practical guidance**: if the requirement does not demand multi-object atomicity at scale, consider a single-object transaction plus asynchronous logging; if it does, plan a fallback strategy (saga/compensation) for the limits of isolation.

---

## 🌐 5. Consistency and Consensus

- **Linearizability**: the maximum degree of consistency (the register behaves as a single node); it costs latency and availability under partition (CAP).
- **Causal order and happens-before**: causal consistency is cheaper than linearizable; causality sequencing (version vectors, Lamport clocks).
- **Consensus (Raft/Paxos/Zab)**: unanimity on a value with an elected leader and a replicated log; the basis of metadata stores (etcd/ZooKeeper) and locking/fencing.
- **Fencing tokens**: each lease/lock issues a monotonic token; storage services reject old tokens to kill zombie writes.
- **No consensus?** Use "just enough" for the case: read-your-writes within a session, a causal API, sticky sessions, or CRDTs for offline collaborative data.

---

## 🔬 6. Batch and Stream Processing

### Batch (ch. 11)
- **MapReduce / dataflow engine model (Spark, Flink batch, Beam)**: partition → map → shuffle → reduce; failures handled by task retry with deterministic output.
- **Joins**: reduce-side (large × large), map-side (broadcast), hash partition joins.
- **Materialized views / batch over datasets** (Dataflow + HDFS/S3) feeds ML output, indexes, and BI results with incremental reprocessing (checkpoints).

### Stream (ch. 12–13)
- **Log-structured message broker (Kafka/Amazon Kinesis)**: partitioned append-only log, safe replay, offsets instead of destructive acks.
- **Streaming languages**: event processing (Flink/Dthree) — windows (event-time vs processing-time), watermarks for lateness, exactly-once via checkpoints (Chandy-Lamport) and sink 2PC transactions.
- **CDC (Change Data Capture) and Database Internals**: the database as an event source — Debezium, log-based extraction without thrashing the database.
- **Deriving state from streams**: compacted topics (Kafka Streams, changelog topics), the "unbundled database" — a stream processor plus storage specialized per view.
- **Stream philosophy (ch. 13)**: unify batch and stream (Lambda vs Kappa), design the flow first, derive views; layers of exactly-once (idempotency plus transactions) and per-key ordering.

---

## ⚖️ 7. Ethics, Impact, and Design Philosophy (ch. 14)

- Privacy by design (minimized PII), consent monitoring, data derivatives (inference risks), algorithmic fairness, and deterministic authorization.
- Data systems are socio-technical products: document lineage and sources, promote transparency and the ability to correct (GDPR art. 16–17, LGPD arts. VIII/18).

---

## 🧭 8. Decision Protocol for Data Architecture

1. **List the non-functional requirements** (read/write SLO, volume and retention, availability SLA) before choosing the storage.
2. **Model the domain** (relational/document/graph) by the access pattern (OLTP vs analytics vs relationships).
3. **Define the consistency contract** per use case (linearizable vs causal vs eventual) and choose the replication architecture that supports it at the lowest cost.
4. **Size the partitioning** with headroom (shard key chosen for future throughput), avoiding known hotspots.
5. **Specify evolution** (schema compatibility, rolling-upgrade policy, schema registry).
6. **Choose integrated tooling**, not monocultures: an event log as the backbone, streams for incremental views, batch for reprocessing.
7. **Validate against failure modes**: timeouts, partition, replica lag, GC pause — test each one with chaos experiments and verify invariants (quorum, fencing, idempotency).

---

## 🔗 Integration with Other Skills

- [system-design-scalability](../../engineering/practices/system-design-scalability/SKILL.md): CAP/PACELC, sharding, and caching at large scale (systemic view).
- [latency-engineering](../../engineering/practices/latency-engineering/SKILL.md): the latency cost of consensus, replicas, and the consistency window.
- [dba-database-administrator](../../roles/dba-database-administrator/SKILL.md) and [db-postgresql](../db-postgresql/SKILL.md): real operation of storage engines and transactions.
- [realtime-streaming-event-driven](../realtime-streaming-event-driven/SKILL.md): Kafka, Flink, Pinot, and real-time OLAP.
- [data-mesh-governance](../data-mesh-governance/SKILL.md): federated governance and data products in the enterprise mesh.
