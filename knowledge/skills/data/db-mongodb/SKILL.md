---
name: "db-mongodb"
description: "Provides administration and engineering patterns for MongoDB based on the official documentation in Portuguese (mongodb.com/pt-br/docs). Covers document modeling (Embedding vs Referencing), the WiredTiger engine, Read/Write Concern, indexes (Compound, Multikey, Text, TTL, 2dsphere), the Aggregation Framework, and Sharded Clusters."
---

# AI Skill: MongoDB Engineering and Administration (db-mongodb)

This skill guides the artificial intelligence to act as a specialist in the document-oriented **MongoDB** database, grounded in the official documentation ([mongodb.com/pt-br/docs](https://www.mongodb.com/pt-br/docs/)). It covers advanced schema-modeling strategies, the WiredTiger storage engine, consistency guarantees (Write/Read Concern), index optimization, the Aggregation Framework, Replica Sets, and Sharded Clusters.

---

## 🧭 Document-Oriented Data Modeling

In MongoDB, modeling is driven by the application's access patterns (read and write queries together), rather than by strict normalization:

### 1. Embedding vs. Referencing
- **Embed (Denormalization - Preferred)**:
  - Use when there are 1:1 or 1:N relationships (where N is bounded and small, e.g. a customer's addresses).
  - Guarantees write atomicity and high-performance reads in a single I/O operation.
- **Reference (Normalization)**:
  - Use when there are 1:N relationships (where N is unbounded or very large, e.g. audit logs) or N:M relationships.
  - Avoids the maximum BSON document size limit (16 MB).

### 2. Schema Design Patterns
- **Subset Pattern**: Keeps only the N most recent or most accessed data in the main document and the rest in a separate collection.
- **Bucket Pattern**: Groups time-series data or IoT metrics into time windows (e.g. 1 hour) to reduce the number of documents and optimize indexes.
- **Outlier Pattern**: Handles exceptionally large documents separately without penalizing the majority of standard documents.

---

## 🛠️ Advanced Indexing and Query Optimization

### 1. Index Types in MongoDB
- **Compound Index**: Follow the ESR rule (**Equality, Sort, Range**):
  - 1st: Exact-equality fields (`$eq`).
  - 2nd: Fields used for sorting (`sort()`).
  - 3rd: Range fields (`$gte`, `$lte`, `$in`).
- **Multikey Index**: Created automatically when indexing fields that contain arrays.
- **TTL Index**: Automatically deletes documents after a specified time:
  ```javascript
  db.sessions.createIndex({ "createdAt": 1 }, { expireAfterSeconds: 3600 });
  ```
- **Geospatial (`2dsphere`)**: For proximity queries (`$near`, `$geoWithin`).

### 2. Analysis with `explain()`
Always run the explanation in `executionStats` mode to diagnose collection scans (*COLLSCAN*):
```javascript
db.orders.explain("executionStats").find({
  status: "COMPLETED",
  createdAt: { $gte: ISODate("2026-01-01") }
});
```

---

## 🔍 Native Aggregation Framework

Use aggregation pipelines for complex data transformations natively and in parallel:

```javascript
db.orders.aggregate([
  // 1. Filtragem inicial usando índice
  { $match: { status: "COMPLETED", orderDate: { $gte: ISODate("2026-01-01") } } },
  
  // 2. Junção com a coleção de clientes
  {
    $lookup: {
      from: "customers",
      localField: "customerId",
      foreignField: "_id",
      as: "customer_details"
    }
  },
  
  // 3. Desfazer o array gerado pelo lookup
  { $unwind: "$customer_details" },
  
  // 4. Agrupamento e cálculo de métricas
  {
    $group: {
      _id: "$customer_details.segment",
      totalRevenue: { $sum: "$totalAmount" },
      averageOrderValue: { $avg: "$totalAmount" },
      totalOrders: { $count: {} }
    }
  },
  
  // 5. Ordenação do resultado
  { $sort: { totalRevenue: -1 } }
]);
```

---

## ⚙️ Concurrency, Consistency, and High Availability

### 1. Consistency and Durability Guarantees
- **Write Concern**: Controls write acknowledgment by the cluster:
  - `w: "majority"`: Guarantees the write was persisted to the journal of the majority of Replica Set nodes (prevents *rollback* on failover).
- **Read Concern**:
  - `rc: "majority"`: Returns only data confirmed by the majority of nodes.
  - `rc: "linearizable"`: Guarantees strictly real-time reads (avoids stale reads).

### 2. Production Architecture
- **Replica Sets**: A minimum of 3 voting nodes (1 Primary and 2 Secondary) to automate election and failover without downtime.
- **Sharded Cluster**: For horizontal scalability across multiple terabytes of data. Choose the **Shard Key** carefully to avoid *jumbo chunks* or write hotspots.

---

## 🔒 Hardening and Security Compliance (OWASP ASVS & CIS MongoDB Benchmark)

- **Mandatory Authentication and TLS**:
  - Enable access-control authentication (`security.authorization: enabled`).
  - Require encrypted TLS 1.3/1.2 connections (`net.tls.mode: requireTLS`).
- **Internal Cluster Authentication**: Use X.509 certificates or a keyfile for communication between Replica Set or Shard nodes.
- **Client-Side Field Level Encryption (CSFLE)**: Encrypt sensitive data (PII, card numbers) on the client side using KMS keys before transmission to the database.
- **Schema Validation (`$jsonSchema`)**: Apply Schema Validation on the collection to prevent NoSQL operator injection (`$where`, `$gt: ""`).

---

## 🔗 Integration with Other Skills

- To integrate MongoDB into Node.js/TypeScript or Python APIs, see [backend-developer](../../roles/backend-developer/SKILL.md), [lang-typescript](../../languages/lang-typescript/SKILL.md), and [lang-python](../../languages/lang-python/SKILL.md).
- For general administration guidelines for NoSQL and SQL databases, see [dba-database-administrator](../../roles/dba-database-administrator/SKILL.md).
- For data security and compliance validation (V8/V14), see [appsec-owasp-asvs](../../security/appsec/appsec-owasp-asvs/SKILL.md), [cis-controls](../../security/grc/cis-controls/SKILL.md), and [security-privacy](../../security/grc/security-privacy/SKILL.md).
