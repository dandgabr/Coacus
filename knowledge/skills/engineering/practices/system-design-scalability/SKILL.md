---
name: system-design-scalability
description: Acts as a specialist in System Design, large-scale systems engineering, and highly available distributed architectures. Covers sharding, partitioning, replication, eventual consistency (CAP/PACELC), distributed caching, load balancing, rate limiting, circuit breakers, and resilience.
---

# System Design and Large-Scale Systems Engineering

This skill supplies the principles, patterns, and heuristics for designing scalable, reliable, fault-tolerant, and high-performance distributed systems, drawing on industry reference works (*System Design* by Karan Pratap Singh and *Strategic Monoliths and Microservices* by Vaughn Vernon).

---

## 🏛️ 1. Fundamental Principles and Theorems

### CAP Theorem & PACELC Theorem
- **CAP**: In the event of a Network Partition (**P**), the system must choose between Consistency (**C**) and Availability (**A**).
  - **CP (Consistency + Partition Tolerance)**: Databases with strict locks and Paxos/Raft consensus (for example, Spanner, etcd, ZooKeeper).
  - **AP (Availability + Partition Tolerance)**: Highly available systems with eventual consistency (for example, Cassandra, DynamoDB).
- **PACELC**: If there is a Partition (**P**), choose between Availability (**A**) and Consistency (**C**); **E**lse, in normal operation, choose between Latency (**L**) and Consistency (**C**).

### Consistency Models
1. **Strong Consistency**: Every read returns the most recent write.
2. **Sequential / Linearizable Consistency**: A global order of operations is preserved.
3. **Eventual Consistency**: If no new update occurs, all replicas eventually converge.
4. **Read-Your-Writes / Monotonic Reads**: Essential guarantees for user experience on replicated nodes.

---

## 🧱 2. Data Scalability Patterns

### Sharding and Partitioning Strategies
- **Horizontal Sharding (Range-Based)**: Split by key ranges (for example, ID 1-1M on Shard A, 1M-2M on Shard B). Prone to *Hotspots*.
- **Hash-Based Sharding**: Distribution via `hash(chave) % num_shards`. Requires costly re-sharding when nodes are added.
- **Consistent Hashing**: A virtual ring with virtual nodes (V-Nodes). Minimizes key movement when servers are added or removed (used by DynamoDB, Cassandra, and CDNs).

### Replication Strategies
- **Single-Leader (Master-Slave)**: Writes go to the leader, reads are distributed across replicas. Risk of *replication lag*.
- **Multi-Leader**: Multiple active datacenters with asynchronous reconciliation (CRDTs or Last-Write-Wins).
- **Leaderless (Quorum Reads/Writes)**: Based on the Quorum formula: $W + R > N$ (where $N$ is the replication factor, $W$ nodes for writes and $R$ nodes for reads guarantee strong consistency).

---

## ⚡ 3. Distributed Caching Patterns

| Strategy | Operation Flow | Pros | Cons |
| :--- | :--- | :--- | :--- |
| **Cache-Aside (Lazy Loading)** | The application queries the cache; on a miss it reads from the DB and updates the cache. | Only queried data is cached; resilient to cache failures. | Latency penalty on a cache miss; risk of stale data. |
| **Read-Through** | The application queries the cache; the cache reads from the DB on a miss. | Clean, unified application code. | Requires dedicated plugins/handlers in the cache. |
| **Write-Through** | The application writes to the cache, and the cache updates the DB synchronously. | Cached data is always up to date and consistent. | Higher write latency (waits for confirmation from both). |
| **Write-Behind (Write-Back)** | The application writes to the cache; the cache writes to the DB asynchronously in batches. | Minimal write latency and absorption of I/O spikes. | Risk of data loss if the cache fails before flushing to the DB. |

### Eviction Policies
- **LRU (Least Recently Used)**: Discards the least recently accessed item (the Redis default).
- **LFU (Least Frequently Used)**: Discards the item with the lowest total access count.
- **TTL (Time to Live)**: Deterministic expiration to balance freshness and memory use.

---

## 🛡️ 4. Resilience and Concurrency Patterns

```
               ┌────────────────────────┐
               │    Cliente / Gateway   │
               └───────────┬────────────┘
                           │
                 [ Rate Limiting & WAF ]
                           │
              ┌────────────▼────────────┐
              │     Circuit Breaker     │
              │  (Closed / Open / Half) │
              └────────────┬────────────┘
                           │
              ┌────────────▼────────────┐
              │   Bulkhead & Isolation  │
              └────────────┬────────────┘
                           │
              ┌────────────▼────────────┐
              │    Serviço Dependente   │
              └─────────────────────────┘
```

1. **Circuit Breaker**:
   - **Closed**: Requests pass normally; it counts the error rate.
   - **Open**: Failures exceed the threshold; it rejects requests immediately (*fail-fast*) without burdening the backend.
   - **Half-Open**: Allows canary traffic to test whether the downstream service has recovered.
2. **Bulkhead**:
   - Isolates thread pools, connections, and memory between critical services so that a cascading failure cannot take down the whole system.
3. **Rate Limiting & Throttling**:
   - Algorithms: **Token Bucket**, **Leaky Bucket**, **Fixed Window**, **Sliding Window Log**.
4. **Idempotency Keys**:
   - Unique UUID keys in the `Idempotency-Key` header with temporary storage in Redis to prevent duplication on network retries.

---

## 📊 5. System Design Interview & Real Architecture Checklist

- [ ] **1. Requirements Clarification**: Functional scope, volume (DAU/MAU), read vs. write rate (RPS), average data size.
- [ ] **2. Capacity Estimation (Back-of-the-Envelope)**:
  - Write/read throughput (QPS).
  - Five-year storage (with a replication factor).
  - Network bandwidth (Ingress/Egress).
  - Cache RAM size (the 80/20 rule: 20% of keys generate 80% of traffic).
- [ ] **3. API Definition**: REST/gRPC contracts with data types, pagination, and RFC 7807 status codes.
- [ ] **4. Data Model**: Choice between Relational (ACID) and NoSQL (Document/Key-Value/Columnar/Graph).
- [ ] **5. High-Level Diagram**: Core components and the primary request flow.
- [ ] **6. Technical Deep Dives**: Bottleneck resolution, partitioning, replication, failover, and observability.
