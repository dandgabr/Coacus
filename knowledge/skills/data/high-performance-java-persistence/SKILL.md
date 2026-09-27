---
name: "high-performance-java-persistence"
description: "Provides expert patterns for high-performance JDBC and JPA/Hibernate persistence based on High-Performance Java Persistence (Vlad Mihalcea). Covers JDBC batching and statement caching, connection pooling and result-set fetching, transactions and isolation levels, JPA entity state transitions and identifier generation strategies, the flush/ActionQueue and dirty checking, fetch strategies and the N+1 problem, DTO projection, second-level and query caching with concurrency strategies, and optimistic vs pessimistic locking."
---

# AI Skill: High-Performance Java Persistence

This skill guides the AI to make database access fast and correct: batch writes, avoid N+1, choose fetch and lock strategies deliberately, and measure before tuning. It builds on *High-Performance Java Persistence* (Vlad Mihalcea).

Resolve current Hibernate/JPA and JDBC driver versions from their publishers before pinning them.

---

## 🧭 When to Activate

- Diagnosing slow persistence (N+1, missing indexes, chatty round-trips).
- Choosing identifier generation, fetch types, or cache strategies.
- Tuning transactions and isolation levels.
- Designing for high write throughput or high read scalability.
- Interpreting Hibernate SQL logs and statement counts.

---

## 🔌 JDBC Fundamentals

- Think in **response time vs throughput**; size pools and capacity with queuing theory. Monitor concurrent connection requests, max pool size, acquisition time and lease time; prefer `DataSource` (pooled) over `DriverManager`.
- **Batch updates:** use `PreparedStatement` batching with a modest batch size; prefer **sequences** for retrieving auto-generated keys; `hibernate.order_inserts`/`order_updates`.
- **Statement caching** has a lifecycle (parser → optimizer → executor) with server-side and client-side variants.
- **ResultSet fetching:** set **fetch size** (default 10; cap around 100), avoid `maxRows` misuse, and select fewer columns ("less is more").
- **Scaling:** master-slave replication, multi-master, sharding; route read-only transactions to replicas.

---

## 🔐 Transactions and Concurrency Control

- **ACID**; two concurrency models — **2PL** (blocking) and **MVCC** (snapshot).
- Know the phenomena: dirty write/read, non-repeatable read, phantom read, read skew, **write skew**, lost update — and the isolation levels that permit them (Read Uncommitted → Serializable).
- **Distributed transactions / 2PC** are costly; prefer single-resource transactions or sagas. Use **application-level** transactions with explicit **pessimistic vs optimistic** locking.

---

## 🗃️ JPA / Hibernate

- **Identifier generation:** `IDENTITY` prevents JDBC batching — prefer **`SEQUENCE`** with a pooled optimizer (`pooled`/`pooled-lo`, `SequenceStyleGenerator`, `TableGenerator`).
- **Entity relationships:** `@ManyToOne`, bidirectional/unidirectional `@OneToMany`, `@ElementCollection`, `@OneToOne`, `@ManyToMany`, `@JoinColumn`; inheritance (single table, join, table-per-class, mapped superclass).
- **Flushing:** flush modes and the **ActionQueue** order; **dirty checking** uses a default snapshot costing proportional to the persistence-context size (bytecode enhancement is more efficient); batch inserts/updates/deletes.
- **Fetching:** prefer **DTO projection** (+ native queries); `FetchType.LAZY` by default, `EAGER` deliberately. The **N+1 query problem** is the dominant trap — catch it with `SQLStatementCountValidator` in tests. Avoid `LazyInitializationException`, the **Open-Session-in-View** anti-pattern, and the temporary-session lazy-loading anti-pattern. Beware associations with pagination and duplicate entity references; tune the **query plan cache** (default 2048).
- **Caching:** synchronization strategies — **cache-aside**, **read-through**, **write-invalidate**, **write-through**, **write-behind**. The **second-level cache** has entity/collection/query entries and concurrency strategies **READ_ONLY** (immutable), **NONSTRICT_READ_WRITE** (rare changes, stale window), **READ_WRITE** (soft locking), **TRANSACTIONAL** (XA, no stale reads).
- **Concurrency control:** implicit optimistic locking via `@Version`; versionless (`OptimisticLockType.ALL`/`DIRTY`); explicit `PESSIMISTIC_READ`/`PESSIMISTIC_WRITE` with lock scope and timeout; `OPTIMISTIC`/`OPTIMISTIC_FORCE_INCREMENT`.

---

## ⚠️ Pitfalls

- `IDENTITY` identifiers silently disabling batching.
- N+1 from lazy associations iterated in a loop.
- Eager fetching everywhere (cartesian products, memory blowups).
- Open-Session-in-View masking fetch problems and holding connections.
- Treating 2PL and MVCC the same; ignoring write skew.
- Caching mutable data with the wrong concurrency strategy.

---

## 🔗 Integration with Other Skills

- For the database engine and query tuning, see [db-postgresql](../db-postgresql/SKILL.md) and [dba-database-administrator](../../roles/dba-database-administrator/SKILL.md).
- For the Java language and concurrency, see [lang-java](../../languages/lang-java/SKILL.md) and [framework-spring-boot](../../frameworks/framework-spring-boot/SKILL.md).
- For persistence-layer clean architecture, see [clean-architecture](../../engineering/practices/clean-architecture/SKILL.md).
