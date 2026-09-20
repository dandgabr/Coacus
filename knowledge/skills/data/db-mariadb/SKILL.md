---
name: "db-mariadb"
description: "Provides administration and engineering patterns for MariaDB based on the official documentation (mariadb.com/docs). Covers storage engines (InnoDB, Aria, ColumnStore, MyRocks), InnoDB Buffer Pool tuning, Galera Cluster, MariaDB MaxScale, Mariabackup, and EXPLAIN FORMAT=JSON optimization."
---

# AI Skill: MariaDB Engineering and Administration (db-mariadb)

This skill guides the artificial intelligence to act as a specialist in the **MariaDB** database, rigorously grounded in the official documentation of the MariaDB Corporation and MariaDB Foundation ([mariadb.com/docs](https://mariadb.com/docs)). It covers pluggable storage engines, the Galera Cluster architecture, InnoDB optimization, physical backups, and high availability with MaxScale.

---

## 🧭 Pluggable Storage Engines

Unlike other relational DBMSs, MariaDB lets you choose a specific storage engine per table:

- **InnoDB**: The default OLTP transactional engine with ACID support, foreign keys, and row-level locking.
- **Aria**: The default non-transactional engine optimized to replace MyISAM and to process temporary tables on disk.
- **ColumnStore**: A column-oriented storage engine designed for large-scale analytical processing (OLAP) and Big Data.
- **MyRocks**: An engine based on RocksDB with an LSM-Tree (*Log-Structured Merge-tree*) structure optimized for high write rates and maximum data compression.
- **Spider**: A transparent sharding engine that connects multiple remote MariaDB instances.

---

## 🛠️ Performance Tuning and Sizing (`my.cnf`)

### 1. Memory and Buffer Pool (InnoDB)
```ini
[mysqld]
# Alocar de 50% a 70% da RAM em servidores dedicados a banco OLTP
innodb_buffer_pool_size = 16G
innodb_buffer_pool_instances = 16
innodb_log_file_size = 2G
innodb_flush_log_at_trx_commit = 1
innodb_file_per_table = 1

# Gerenciamento de conexões e threads
max_connections = 500
thread_handling = pool-of-threads
thread_pool_size = 16
```

### 2. Query and Execution Plan Analysis
Use `EXPLAIN FORMAT=JSON` to inspect the relative cost of sub-operations and optimizer statistics:

```sql
EXPLAIN FORMAT=JSON
SELECT c.name, COUNT(o.id) as total_orders
FROM customers c
LEFT JOIN orders o ON c.id = o.customer_id
WHERE c.status = 'ACTIVE'
GROUP BY c.id;
```

---

## ⚙️ High Availability and Replication

### 1. Galera Cluster (Synchronous Multi-Master)
- Certification-based synchronous replication for active nodes.
- Guarantees zero data loss (*RPO = 0*) and instant failover.
```ini
[mysqld]
# Configuração básica de nó Galera
wsrep_on = ON
wsrep_provider = /usr/lib/galera/libgalera_smm.so
wsrep_cluster_name = "production_galera_cluster"
wsrep_cluster_address = "gcomm://10.0.0.1,10.0.0.2,10.0.0.3"
wsrep_sst_method = mariabackup
```

### 2. MariaDB MaxScale
- An intelligent layer-7 proxy for MariaDB.
- Offers automatic read/write splitting, masking of sensitive data, and protection against denial-of-service (DoS) attacks and SQL Injection.

### 3. Online Physical Backups with Mariabackup
- A native open-source tool for non-blocking physical copies of InnoDB and Aria tables:
```bash
# Executando backup físico completo sem bloquear gravações
mariabackup --backup --target-dir=/var/backups/mariadb/full --user=backup_user --password=secret

# Preparando o backup para restauração (consistência de logs)
mariabackup --prepare --target-dir=/var/backups/mariadb/full
```

---

## 🔒 Hardening and Security Compliance (OWASP ASVS & CIS MariaDB Benchmark)

- **Encryption at Rest and in Transit**:
  - Enable native InnoDB table encryption (`innodb_encrypt_tables = ON`, `innodb_encrypt_log = ON`).
  - Force TLS 1.3 connections (`ssl = ON`, `require_secure_transport = ON`).
- **Secure Authentication and Access Control**:
  - Remove anonymous users and test databases (`mariadb-secure-installation`).
  - Use the `ed25519` or `caching_sha2_password` authentication plugin for all user accounts.
- **Auditing (`server_audit`)**: Enable the `server_audit` plugin to audit connections, DDL statements, and access to sensitive data.

---

## 🔗 Integration with Other Skills

- To integrate MariaDB into backend development ecosystems, see [backend-developer](../../roles/backend-developer/SKILL.md).
- For general administration guidelines for relational and NoSQL databases, see [dba-database-administrator](../../roles/dba-database-administrator/SKILL.md).
- For validating database security controls (V8/V14), see [appsec-owasp-asvs](../../security/appsec/appsec-owasp-asvs/SKILL.md), [cis-controls](../../security/grc/cis-controls/SKILL.md), and [security-privacy](../../security/grc/security-privacy/SKILL.md).
