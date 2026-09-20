---
name: "db-sqlite"
description: "Provides engineering and optimization patterns for SQLite based on the official documentation (sqlite.org/docs.html). Covers serverless architecture, WAL mode (Write-Ahead Logging), performance pragmas, covering and partial indexes, FTS5, JSON1, and the WITHOUT ROWID extension."
---

# AI Skill: SQLite Engineering and Optimization (db-sqlite)

This skill guides the artificial intelligence to act as a specialist in the **SQLite** database, rigorously grounded in the official documentation ([sqlite.org/docs.html](https://sqlite.org/docs.html)). It covers software engineering patterns for embedded databases, high-concurrency tuning via WAL mode, performance pragmas, partial indexes, and `WITHOUT ROWID` tables.

---

## 🧭 Embedded Architecture and WAL Mode (Write-Ahead Logging)

Unlike client-server databases, SQLite operates as a database engine embedded in the application's own process.

### 1. Recommended Concurrency Configuration and PRAGMAs
By default, SQLite operates in Rollback Journal mode (which blocks reads during writes). To enable reads concurrent with writes, you must turn on **WAL** mode:

```sql
-- Ativar modo Write-Ahead Logging (persistido no arquivo da base)
PRAGMA journal_mode = WAL;

-- Sincronização segura para WAL (desempenho 10x superior sem perda de consistência)
PRAGMA synchronous = NORMAL;

-- Manter tabela temporária em memória RAM
PRAGMA temp_store = MEMORY;

-- Aumentar tamanho do cache de memória (ex: 64MB = 16000 páginas de 4KB)
PRAGMA cache_size = -64000;

-- Definir tempo limite de espera para evitar SQLITE_BUSY em escritas concorrentes
PRAGMA busy_timeout = 5000;

-- Habilitar verificação de chaves estrangeiras
PRAGMA foreign_keys = ON;
```

---

## 🛠️ Indexing Strategies and High-Performance Modeling

### 1. `WITHOUT ROWID` Tables
- For associative (N:M) tables or tables with a composite natural primary key, whether alphanumeric or not (e.g. UUID/TEXT), use the `WITHOUT ROWID` clause to save storage space and eliminate a double B-Tree lookup:
```sql
CREATE TABLE user_roles (
    user_id TEXT NOT NULL,
    role_id TEXT NOT NULL,
    assigned_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now')),
    PRIMARY KEY (user_id, role_id)
) WITHOUT ROWID;
```

### 2. Partial Indexes and Expression Indexes
- **Partial Index**: Index only the relevant rows of the table:
```sql
CREATE INDEX idx_active_subscriptions 
ON subscriptions (user_id) 
WHERE status = 'ACTIVE';
```
- **Expression Index**: Index the result of deterministic functions or data extracted from JSON:
```sql
CREATE INDEX idx_user_email_domain 
ON users (substr(email, instr(email, '@') + 1));
```

---

## 🔍 Full-Text Search (FTS5) and JSON Handling

### 1. Native JSON Support
SQLite has native JSON support (the JSON1 extension is enabled by default):
```sql
CREATE TABLE user_settings (
    user_id INTEGER PRIMARY KEY,
    data TEXT CHECK (json_valid(data))
);

-- Extraindo valores formatados
SELECT json_extract(data, '$.theme') AS theme FROM user_settings;
```

### 2. Full-Text Search (FTS5)
```sql
CREATE VIRTUAL TABLE documents_fts USING fts5(
    title,
    body,
    tokenize = 'porter ascii'
);

-- Consulta por frase ou prefixo com ordenação por relevância (bm25)
SELECT title, bm25(documents_fts) AS rank 
FROM documents_fts 
WHERE documents_fts MATCH 'sqlite AND performance*' 
ORDER BY rank;
```

---

## ⚙️ Application and Deployment Guidelines

1. **Handling the `SQLITE_BUSY` error**: Make sure your application's SQLite driver implements `busy_timeout` or handles the exception with retries and exponential backoff.
2. **Non-Blocking Online Backups**: Use SQLite's native backup API (`sqlite3_backup_init` or the `.backup` CLI command) instead of copying the `.db` file directly while the application is running.

---

## 🔒 Hardening and Encryption in Embedded Databases (OWASP MASVS & ASVS)

- **Encryption at Rest**: On mobile or desktop operating systems, adopt **SEE (SQLite Encryption Extension)** or **SQLCipher** (AES-256) to protect `.db` files against physical exfiltration or reverse engineering.
- **OS Permission Protection**: Restrict the database file's permissions (`chmod 600`) to exclusive access by the process that owns the application.
- **SQL Injection Mitigation**: Always use bound parameters (*prepared statements*) instead of string concatenation in `sqlite3_exec`.

---

## 🔗 Integration with Other Skills

- To integrate SQLite into desktop, mobile, or embedded applications in Python/C/Rust, see [lang-python](../../languages/lang-python/SKILL.md), [lang-c](../../languages/lang-c/SKILL.md), and [lang-rust](../../languages/lang-rust/SKILL.md).
- For general administration guidelines for relational databases, see [dba-database-administrator](../../roles/dba-database-administrator/SKILL.md).
- For security requirements in mobile and embedded storage, see [appsec-owasp-masvs](../../security/appsec/appsec-owasp-masvs/SKILL.md) and [appsec-owasp-asvs](../../security/appsec/appsec-owasp-asvs/SKILL.md).
