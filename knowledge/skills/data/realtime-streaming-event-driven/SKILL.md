---
name: realtime-streaming-event-driven
description: Specializes in Real-Time Streaming Architectures, Batch-Stream Unification, and Streaming Databases based on Streaming Databases (Hubert Dulay) and Building Real-Time Analytics Systems (Mark Needham). Covers Apache Kafka, Apache Pinot, Apache Flink, ClickHouse, Change Data Capture (CDC via Debezium), and real-time OLAP queries with sub-second latency.
---

# Real-Time Streaming Architectures and Streaming Databases

This skill establishes patterns for designing and operating systems oriented toward continuous event streams, unified batch-stream processing, and real-time OLAP analytics with millisecond-scale latencies.

---

## ⚡ 1. Lambda vs Kappa vs Unification in a Streaming DB

```
┌─────────────────────────────────────────────────────────────┐
│ Fontes Operacionais (OLTP: Postgres, MySQL, APIs, IoT)     │
└──────────────────────────────┬──────────────────────────────┘
                               │ CDC (Debezium) / Event Producer
┌──────────────────────────────▼──────────────────────────────┐
│ Log de Eventos Distribuído (Apache Kafka / Apache Pulsar)   │
└──────────────────────────────┬──────────────────────────────┘
                               │
            ┌──────────────────┴──────────────────┐
            │                                     │
┌───────────▼───────────┐             ┌───────────▼───────────┐
│ Processador Stateful  │             │ Streaming OLAP DB     │
│ (Apache Flink)        │             │ (Apache Pinot /       │
│ (Janelas, Agregações) │             │  ClickHouse)          │
└───────────────────────┘             └───────────┬───────────┘
                                                  │
                                      ┌───────────▼───────────┐
                                      │ Dashboards & APIs     │
                                      │ (< 50ms Query Latency)│
                                      └───────────────────────┘
```

---

## 📊 2. Change Data Capture (CDC) Patterns with Debezium

- **Log-Based CDC**: Directly reads the database's transaction logs (WAL in PostgreSQL, Binlog in MySQL) without the overhead of polling `SELECT` queries.
- **Outbox Pattern**: Atomic write to the `outbox` table within the same relational database transaction to guarantee that domain events are never lost during network failures.
