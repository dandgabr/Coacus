---
name: "db-postgresql"
description: "Provides administration and engineering patterns for PostgreSQL based on the official documentation (postgresql.org/docs). Covers MVCC architecture, Autovacuum tuning, advanced types (JSONB, PostGIS), index strategy (B-Tree, GIN, GiST, BRIN), EXPLAIN ANALYZE BUFFERS analysis, replication, and PgBouncer."
---

# AI Skill: PostgreSQL Engineering and Administration (db-postgresql)

This skill guides the artificial intelligence to act as a specialist in the **PostgreSQL** database, rigorously grounded in the official documentation of the PostgreSQL Global Development Group ([postgresql.org/docs](https://www.postgresql.org/docs/)). It covers advanced modeling, MVCC concurrency control, memory and disk tuning, indexing strategies, and high availability.

---

## 🧭 Architecture and Concurrency Control (MVCC)

### 1. Multi-Version Concurrency Control (MVCC) and Autovacuum
- **Tuple Visibility**: PostgreSQL creates row versions (*tuples*) for non-blocking reads.
- **Autovacuum Tuning**:
  - Configure Autovacuum to prevent table bloat and transaction ID wraparound:
  ```ini
  # postgresql.conf
  autovacuum = on
  autovacuum_vacuum_scale_factor = 0.05
  autovacuum_analyze_scale_factor = 0.02
  autovacuum_max_workers = 4
  autovacuum_vacuum_cost_limit = 1000
  ```
  - On tables with a high volume of writes/updates, adjust parameters individually via `ALTER TABLE tbl SET (autovacuum_vacuum_scale_factor = 0.01);`.

### 2. Memory Sizing (`postgresql.conf`)
- `shared_buffers`: 25% to 40% of the system's total RAM dedicated to the page cache.
- `work_mem`: Memory allotted per sort or hash join operation per query node. Set it carefully to avoid excessive RAM consumption under concurrency.
- `maintenance_work_mem`: Memory allocated to `VACUUM`, `CREATE INDEX`, and `ALTER TABLE`.
- `effective_cache_size`: An estimate of the memory available for operating-system caching (helps the query planner decide between an index scan and a sequential scan).

---

## 🛠️ Indexing Strategies and Advanced Types

### 1. Index Types
- **B-Tree**: The default type. Use `INCLUDE` clauses for index-only scans.
- **GIN (Generalized Inverted Index)**: Essential for `JSONB` columns, full-text search, and `array` types.
- **GiST (Generalized Search Tree)**: Ideal for geographic data (PostGIS) and range types.
- **BRIN (Block Range Index)**: High performance and a minimal memory footprint for giant tables ordered by time (e.g. logs, telemetry).

### 2. JSONB and Semi-Structured Queries
- Prefer `JSONB` over `JSON` because of its pre-parsing and GIN index support:
```sql
CREATE TABLE app_events (
    id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    payload jsonb NOT NULL,
    created_at timestamptz DEFAULT clock_timestamp()
);

-- Criando índice GIN no campo JSONB
CREATE INDEX idx_events_payload_gin ON app_events USING gin (payload);

-- Consulta otimizada usando operador de contenção (@>)
SELECT * FROM app_events WHERE payload @> '{"event_type": "user_signup"}';
```

---

## 🔍 Query Optimization with EXPLAIN

To diagnose performance bottlenecks, always use the command with buffer-counter support:

```sql
EXPLAIN (ANALYZE, BUFFERS, VERBOSE)
SELECT u.id, u.email, o.total_amount
FROM users u
JOIN orders o ON u.id = o.user_id
WHERE u.created_at >= '2026-01-01' AND o.status = 'COMPLETED';
```
- **Warning Signs**:
  - `Sequential Scan` on tables with millions of rows (missing an appropriate index).
  - `Sort Method: external merge Disk` (indicates the need to increase `work_mem`).
  - High `Loops` in a `Nested Loop Join` (consider replacing it with a `Hash Join` or adding an index on the foreign key).

---

## ⚙️ High Availability and Connection Pooling

- **PgBouncer**: A high-performance proxy for connection pooling (`transaction` mode).
- **Replication**:
  - **Streaming Replication**: Block-level physical replication for a read standby and failover.
  - **Logical Replication**: Selective table/publication replication for microservice integration.
- **Failover Tools**: Patroni (with etcd/consul) for high availability with automatic leader-node failover.

---

## 🔒 Hardening and Security Compliance (OWASP ASVS & CIS PostgreSQL Benchmark)

- **Encryption in Transit**: Force encrypted TLS 1.3/1.2 connections (`ssl = on`, `ssl_min_protocol_version = 'TLSv1.2'`).
- **Strict Access Control (`pg_hba.conf`)**: Forbid `trust` or `md5` authentication; require `scram-sha-256` for all remote connections.
- **Least Privilege and Row Level Security (RLS)**:
  - Never run applications as the `postgres` superuser.
  - Enable RLS for multitenant data isolation (`ALTER TABLE tbl ENABLE ROW LEVEL SECURITY;`).
- **Auditing (`pgaudit`)**: Enable the `pgaudit` extension to record DDL operations and modifications to sensitive tables without overloading the system log.

---

## 🔗 Integration with Other Skills

- To integrate PostgreSQL into backend applications, see [backend-developer](../../roles/backend-developer/SKILL.md) and [lang-python](../../languages/lang-python/SKILL.md).
- For general database administration guidelines, see [dba-database-administrator](../../roles/dba-database-administrator/SKILL.md).
- For validating database security requirements (V8/V14), see [appsec-owasp-asvs](../../security/appsec/appsec-owasp-asvs/SKILL.md), [cis-controls](../../security/grc/cis-controls/SKILL.md), and [security-privacy](../../security/grc/security-privacy/SKILL.md).
