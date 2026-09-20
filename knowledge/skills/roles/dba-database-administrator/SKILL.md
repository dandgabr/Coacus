---
name: "dba-database-administrator"
description: "Provides software engineering and database administration (DBA) standards for SQL and NoSQL systems. Covers data modeling, indexing strategies, query optimization (EXPLAIN), concurrency control (ACID/BASE), replication, high availability, backups (PITR), TLS-secured connections by default, and security in PostgreSQL, MariaDB, SQLite, and MongoDB."
---

# AI Skill: Database Administrator (DBA Specialist)

This skill guides the artificial intelligence to act as a **Database Administrator (DBA)**, specialized in the planning, provisioning, optimization, security, and ongoing maintenance of **relational (SQL)** and **non-relational (NoSQL / Document-oriented)** databases. The skill adopts data engineering best practices, covering the complete information lifecycle in production environments.

---

## 🧭 Fundamental Principles and Data Architecture

### 1. Relational (SQL) vs. Non-Relational (NoSQL)
- **Relational Systems (RDBMS)**:
  - **ACID Guarantees**: Atomicity, Consistency, Isolation, and Durability.
  - **Normalized Modeling (3NF)** for OLTP (reducing redundancy and guaranteeing referential integrity) and **Dimensional Modeling (Star/Snowflake Schema)** for OLAP/Data Warehouse.
- **Non-Relational Systems (NoSQL)**:
  - **CAP Theorem & BASE Model**: *Basically Available, Soft-state, Eventual consistency*. A pragmatic choice between Consistency (CP) and Availability (AP) under network partition.
  - **Document-Oriented / Key-Value Modeling**: Conscious denormalization based on the application's read and write access patterns.

### 2. Global Indexing Strategies
- **B-Tree**: The default index for equality and range searches over sortable data.
- **Composite Indexes**: Strict column order based on selectivity (equality columns first, followed by range columns).
- **Special Indexes**: GIN/GiST for full-text search and semi-structured data (JSON/JSONB), TTL for automatic data expiration, and partial indexes to filter frequent subsets.

### 3. Query Analysis and Optimization (Performance Tuning)
- Inspection of execution plans (`EXPLAIN` / `EXPLAIN ANALYZE`).
- Elimination of full scans (*Full Table Scans* / *Collection Scans*) on large tables.
- Adequate memory sizing for read buffers, sorting, and page cache.

### 4. High Availability, Replication, and Backup
- **Replication**: Primary-Replica (synchronous/asynchronous) for read separation and failover.
- **Backup & Disaster Recovery**:
  - **Logical Backup**: Export as SQL/BSON scripts (e.g., `pg_dump`, `mariadb-dump`, `mongodump`).
  - **Physical Backup / PITR**: Capture of data files with continuous archiving of transaction logs (WAL/Binlog) for *Point-In-Time Recovery*.
- **Connection Pooling**: Mitigating the cost of creating connections using dedicated proxies (e.g., PgBouncer, MaxScale, Mongos).

---

## 🛠️ Database-Specific Sub-Skills

For in-depth technical implementation guidelines, syntax, and commands per DBMS, consult the dedicated sub-skills:

| Database | Type | Official Reference Documentation | Related Skill |
| :--- | :--- | :--- | :--- |
| **PostgreSQL** | Relational (SQL) | [postgresql.org/docs](https://www.postgresql.org/docs/) | [db-postgresql](../../data/db-postgresql/SKILL.md) |
| **MariaDB** | Relational (SQL) | [mariadb.com/docs](https://mariadb.com/docs) | [db-mariadb](../../data/db-mariadb/SKILL.md) |
| **SQLite** | Relational Embedded | [sqlite.org/docs.html](https://sqlite.org/docs.html) | [db-sqlite](../../data/db-sqlite/SKILL.md) |
| **MongoDB** | NoSQL (Documents) | [mongodb.com/pt-br/docs](https://www.mongodb.com/pt-br/docs/) | [db-mongodb](../../data/db-mongodb/SKILL.md) |

---

## 🧰 Security and Hardening Practices Checklist (DBA)

1. **Principle of Least Privilege (RBAC)**: Application accounts must hold only the minimum necessary privileges (`SELECT`, `INSERT`, `UPDATE`, `DELETE`), forbidding the use of superusers (`postgres`, `root`).
2. **Encryption in Transit (Secure Connections by Default)**:
   - **Default posture**: every remote connection MUST be encrypted via TLS/SSL, with server certificate verification. In production, refuse `disable`, `allow`, `prefer`, and bare `require` (without verifying the server).
   - **PostgreSQL (server)** — in `postgresql.conf`:
     - `ssl = on`
     - `ssl_min_protocol_version = 'TLSv1.2'` (minimum; for a strict policy use only `TLSv1.3` by pinning min+max = `'TLSv1.3'`)
     - `ssl_tls13_ciphers = 'TLS_AES_256_GCM_SHA384:TLS_AES_128_GCM_SHA256:TLS_CHACHA20_POLY1305_SHA256'` (AEAD-only on TLS 1.3)
     - `ssl_key_file` with `chmod 0600`; `ssl_cert_file`; `ssl_ca_file` for client-cert verification
   - **PostgreSQL (hba)** — in `pg_hba.conf`, force TLS and reject non-TLS:
     ```
     hostssl  all  all  0.0.0.0/0  scram-sha-256  clientcert=verify-ca
     hostnossl all  all  0.0.0.0/0  reject
     ```
   - **PostgreSQL (client / connection string)** — use **`sslmode=verify-full`** + `sslrootcert=<CA>` (verifies chain + hostname). `require` only encrypts but is vulnerable to MITM. In Node.js applications (pg/Drizzle) and PgBouncer, force `verify-full`.
   - **Verifying that the connection is encrypted (Postgres)**:
     ```sql
     SELECT ssl, version, cipher FROM pg_stat_ssl WHERE pid = pg_backend_pid();  -- ssl=t => encrypted
     ```
   - **MariaDB/MySQL**: `tls_version = TLSv1.2,TLSv1.3`, account with `REQUIRE SSL` via `GRANT ... REQUIRE SSL`, client with `--ssl-verify-server-cert` on.
   - **MongoDB**: server `--tlsMode requireSSL`; client `tls=true` + `tlsCAFile`; keep `tlsAllowInvalidCertificates=false` and `tlsAllowInvalidHostnames=false`.
   - **SQLite**: embedded, with no network listener and **no TLS of its own** — protect the file's transport (encrypted share) or use **SQLCipher** (AES-256) for encryption at rest.
   - **At Rest (*Encryption at Rest*)**: encrypted disks and volumes (AES-256) or native table/collection encryption; passwords/hashes always with strong algorithms (e.g., `scram-sha-256`).
3. **Auditing and Monitoring**:
   - Enabling slow query logs (*Slow Query Log*) and auditing administrative actions.
   - Active monitoring of IOPS, cache hit ratio, CPU usage, connection saturation, and replication lag.

---

## 🔗 Integration with Other Skills

- To integrate database access into resilient backend applications, consult [backend-developer](../backend-developer/SKILL.md) and [clean-code-reusability](../../engineering/practices/clean-code-reusability/SKILL.md).
- For provisioning database infrastructure via IaC, Docker, and Kubernetes, consult [devops-engineer](../devops-engineer/SKILL.md) and [cloud-aws](../../infrastructure/cloud-aws/SKILL.md).
- For data compliance, retention, and privacy requirements (LGPD/GDPR), consult [security-privacy](../../security/grc/security-privacy/SKILL.md) and [pci-dss-compliance](../../security/grc/pci-dss-compliance/SKILL.md).
