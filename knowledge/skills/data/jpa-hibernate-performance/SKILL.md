---
name: jpa-hibernate-performance
description: Specializes in Java Persistence performance (JPA/Hibernate) based on High-Performance Java Persistence (Vlad Mihalcea). Covers JDBC batching, the N+1 query problem and fetch strategies (JOIN FETCH, EntityGraph), FlushOperationQueue and ActionQueue, dirty checking, first- and second-level caching (read-through/nonstrict-read-write), optimistic and pessimistic locking, efficient pagination (keyset vs OFFSET), transactions and isolation, and per-database SQL tuning (EXPLAIN, execution plans).
---

# AI Skill: High Performance in Java Persistence (JPA/Hibernate)

This skill guides the artificial intelligence to design the Java/JPA persistence layer with a focus on performance, based on *High-Performance Java Persistence* (Vlad Mihalcea), covering raw JDBC, JPA, and Hibernate.

---

## 🧱 1. Persistence Layer Architecture

- **Deliberate choice of tool**: raw JDBC batching for ETL/bulk; JPA+Hibernate for domain OLTP; native SQL/projections for analytical queries — **do not force an ORM on everything**.
- **Access stereotypes**: domain entities (aggregates with short transactions), DTO projections (read queries), value types (immutable embeddables).
- **Short transactions**: the transaction scope equals the smallest atomic unit; never run UI or remote calls inside an open transaction.

---

## 🔥 2. The N+1 Problem and Fetch Strategies

### Diagnosis
- **N+1**: one query for the root entity plus N lazy queries while navigating associations; detect it with `hibernate.generate_statistics=true`, `nullSafeGet`/SQL log, and hydration tests.

### Mitigations (in order of preference)
1. **JOIN FETCH** in JPQL: `SELECT a FROM Author a JOIN FETCH a.books WHERE a.id = :id` — a single round-trip fetch.
2. **@EntityGraph**: declarative definition of the fetch plan per use case (without polluting queries).
3. **`@_BATCH(size)` / `hibernate.default_batch_fetch_size`**: turn N queries into N/size `IN (...)` queries — the best balance for arbitrary associations.
4. **`@Fetch(FetchMode.SUBSELECT)`**: for collections accessed in bulk within the same transaction.
5. **`@BatchSize`** on lazy collections; `@LazyCollection(LazyCollectionOption.EXTRA)` for count-only.

### Rules
- `FetchType.LAZY` on **every** association (the safe default); a UNI-side `@ManyToOne(optional=false)` may be EAGER with justification.
- Never use "open session in view" in production — the classic villain of N+1 and long transactions.
- For large many-to-many, prefer **two unilateral bidirectional** associations with an extra `@LazyCollection(ExtraLazyType)`. Access them through a DTO when the write model does not need the collection.

---

## 📦 3. Write-Behind, Flush, and Batching

### ActionQueue and Flush Order
- Hibernate orders operations in the `ActionQueue` (inserts → updates → collection removes → deletions), already designed for FK/UNIQUE; understand the order in multi-entity transactions.
- `FlushModeType.AUTO` flushes on queries "[flush before a query that may touch pending data]"; use `COMMIT` for read-only hot paths and control the flush manually (`em.flush()`).

### JDBC Batching
- Enable: `hibernate.jdbc.batch_size` (30–50 typical), `order_inserts=true`, `order_updates=true`, `batch_versioned_data=true`.
- **Driver requirement**: `rewriteBatchedStatements` (MySQL), `reWriteBatchedInserts` (PostgreSQL) for a real batch on the wire.
- **IDENTITY disables insert batching** (Hibernate needs the generated id); prefer `SEQUENCE` (with `allocationSize` 50+) or `TABLE` with a pooler (pooled-lo).
- Bulk: `JPQL/HQL bulk update+delete` (they bypass the persistence context), `StatelessSession`, or `Session.doWork` with direct JDBC for large volumes.

### Dirty Checking and State
- Default dirty checking scans the context's entities; for large or read-only entities use `@Immutable` or `Session.refresh`.
- `@DynamicUpdate` generates an UPDATE only for the changed columns (less traffic, avoids overwriting) — beware of less cacheable query plans.
- Limit the **size of the Session/Persistence Context**: `clear()`/`detach()` in long loops; measure with `em.getEntityManagerFactory().getPersistenceUnitUtil()` and statistics.

---

## 🗄️ 4. Cache (L1, L2, and Query Cache)

| Cache | Scope | Recommended use |
| :--- | :--- | :--- |
| **First-level (Session)** | Transaction/Session | Identity and object caching; always on |
| **Second-level (L2)** | SessionFactory (multi-session) | Read-mostly data, references; use TTL/versioning |
| **Query cache** | Query result | Only with few results and stable tables (invalidation is costly) |

- **Concurrency strategies** (from strictest to lightest): `READ_WRITE` → `NONSTRICT_READ_WRITE` → `READ_ONLY`.
  - `NONSTRICT_READ_WRITE`: a light asynchronous lock; fine for read-mostly; never under high concurrent write (it invalidates too much).
- **Providers**: JCache (Ehcache 3, Infinispan, Caffeine bridge); size L2 regions to the working set (do not "cache everything").
- **Read-through in the app**: an explicit Cache-Aside pattern ([system-design-scalability](../../engineering/practices/system-design-scalability/SKILL.md)) often beats L2 when the domain suits it.

---

## 🔒 5. Locking, Concurrency, and Transactions

- **Optimistic (version/numeric)**: handle `OptimisticLockException` with a retry (short transaction); ideal for medium to low contention. Increment the version manually in bulk actions.
- **Pessimistic**: `PESSIMISTIC_WRITE` (SELECT FOR UPDATE) for job queues, critical counters, bid/reserve stock; keep lock time minimal.
- **Lost update**: the biggest silent plague — a reader and a writer in separate transactions; mitigations: optimistic locking, `PESSIMISTIC_FORCE_INCREMENT`, or atomicity in SQL (`UPDATE ... SET x = x + 1`).
- **Isolation**: READ_COMMITTED plus versioning solves 90%; SERIALIZABLE only with good justification (cost in locks and anomalies even in Postgres SSI).

---

## 📑 6. Pagination and Queries

- **OFFSET degrades badly** (it scans and discards): for deep pagination use **keyset/seek** (`WHERE (a.id > :last) ORDER BY a.id LIMIT :n`) — constant cost.
- Modern standard SQL: `OFFSET ? ROWS FETCH FIRST ? ROWS ONLY` (SQL:2008); dialects vary — let Hibernate map it.
- **Projections**: `SELECT new com.x.Dto(...)` for reads (against the traffic of managed entities); `Tuple`/interface-based projections for flexibility.
- **Criteria API** for dynamic filters; beware of generating non-cacheable plans (use the query plan cache with constant parameters).
- Measurement per database: `EXPLAIN (ANALYZE, BUFFERS)` (Postgres), `set showplan` (SQL Server), autotrace (Oracle) — validate the plan before and after ([db-postgresql](../db-postgresql/SKILL.md)).

---

## 🧭 7. Persistence Optimization Protocol

1. **Measure first**: `hibernate.generate_statistics=true` in dev; APM in prod; identify N+1, repeated queries, long sessions.
2. **Fix the fetch** (JOIN FETCH/EntityGraph) before touching the cache.
3. **Enable batching** and verify the wire (driver logs) — a batch that never reaches the database is pure overhead.
4. **Cache with policy**: L2 for read-mostly with TTL/versions; query cache rarely.
5. **Locking per case**: optimistic by default; pessimistic only for micro-intervals.
6. **Keyset pagination**; OFFSET only for small initial pages.
7. **Load tests** with realistic data (cardinality and skew) and verification of plans after index changes or migration.
8. **Django-like providers**: keep the driver and dialect up to date (optimizations arrive with each Hibernate/JDBC driver version).

---

## 🔗 Integration with Other Skills

- [lang-java](../../languages/lang-java/SKILL.md): JPA fundamentals under concurrency and the JVM.
- [db-postgresql](../db-postgresql/SKILL.md), [db-mariadb](../db-mariadb/SKILL.md), [db-sqlite](../db-sqlite/SKILL.md): tuning the target database (EXPLAIN, indexes, buffer).
- [dba-database-administrator](../../roles/dba-database-administrator/SKILL.md): modeling, indexes, and reference queries.
- [backend-developer](../../roles/backend-developer/SKILL.md): integration into Java services/APIs with short transactions.
- [latency-engineering](../../engineering/practices/latency-engineering/SKILL.md): connection-pool round-trips and N+1 as p99 villains.
