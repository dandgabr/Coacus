# ADR-0001: Selection of a Relational Database for the Financial Module

- **Status**: Approved
- **Date**: 2026-08-06
- **Authors**: Software Architecture Team

---

##  Context and Problem

The system's financial module requires a strong ACID integrity guarantee, complex transactions, and support for high-performance relational queries to generate regulatory reports.

---

## 🎯 Options Considered

1. **PostgreSQL 15** (Relational)
2. **MongoDB 6.0** (Document)
3. **MySQL 8.0** (Relational)

---

## ⚡ Decision

We decided to adopt **PostgreSQL 15** as the primary database for the financial module.

### Rationale
- Robust native support for ACID transactions and transaction isolation.
- Excellent performance with complex queries and native support for the `JSONB` type when flexibility is needed.
- Mature backup, replication, and monitoring tools in the cloud ecosystem.

---

## 📊 Consequences

### Positive
- Guaranteed transactional consistency without the need for manual compensations in the application.
- Easy integration with modern ORMs (Prisma, TypeORM).

### Negative / Risks
- Requires fine-tuning of indexes for high-volume audit tables.
- Need to manage schema migrations in an automated way in the CI/CD pipeline.
