---
name: framework-quarkus-jnosql
description: "Provides Cloud-Native development patterns with Quarkus, GraalVM Native Image, and polyglot NoSQL persistence using Eclipse JNoSQL, Jakarta NoSQL, and Jakarta Data."
---

# Quarkus & Eclipse JNoSQL Cloud-Native Engineering

This skill establishes advanced Cloud-Native development standards in Java using the **Quarkus** and **Eclipse JNoSQL** (Jakarta NoSQL / Jakarta Data) ecosystem.

---

## 🧭 1. Quarkus Fundamentals and Philosophy
- **Supersonic Subatomic Java**: Instant startup and an ultra-low memory footprint through Ahead-of-Time (AOT) compilation with GraalVM Native Image.
- **Build-Time Metaprogramming**: Dependency injection via ArC (static CDI resolved at compile time) and elimination of dynamic reflection.
- **Unified Reactive and Imperative Architecture**: Transparent support for blocking calls managed by Virtual Threads or reactive code with Mutiny.

---

## 🗄️ 2. Polyglot Persistence with Eclipse JNoSQL and Jakarta Data
- **Supported Models**:
  - *Document*: MongoDB, Couchbase.
  - *Key-Value*: Redis, DynamoDB.
  - *Columnar*: Apache Cassandra, ScyllaDB.
  - *Graph*: Neo4j.
- **Jakarta Data Repository Pattern**:
  - Declarative interface extending typed repositories:
    ```java
    @Repository
    public interface CustomerRepository extends CrudRepository<Customer, String> {
        List<Customer> findByCity(String city);
    }
    ```
- **Entity Mapping**: `@Entity`, `@Id`, and `@Column` annotations that are independent of the underlying database, guaranteeing portability across NoSQL providers.

---

## 🚀 3. Best Practices for GraalVM Native Image
- Avoid dynamic classes, CGLIB proxies, and undeclared reflection.
- Register DTOs and JSON serialization entities with `@RegisterForReflection`.
- Keep Quarkus Dev Mode (`quarkus dev`) active for instant hot reload during the development cycle.
