---
name: c4-model-architecture
description: Acts as a specialist in modeling and documenting software architecture with the C4 Model (Context, Containers, Components, Code) created by Simon Brown, integrated with PlantUML, Structurizr DSL, and Mermaid.js.
---

# C4 Model for Software Architecture Visualization

This skill establishes the formal standards for modeling, hierarchical abstraction, and visual representation of software architectures based on Simon Brown's **C4 Model** (*The C4 model for visualising software architecture*).

---

## 📌 The 4 Abstraction Levels of the C4 Model

The C4 Model organizes software-system visualization into four hierarchical levels of progressive zoom:

```
┌─────────────────────────────────────────────────────────────┐
│  Level 1: System Context Diagram                            │
│  (People and Software Systems around the ecosystem)         │
└──────────────────────────────┬──────────────────────────────┘
                               │ Zoom In
┌──────────────────────────────▼──────────────────────────────┐
│  Level 2: Container Diagram (Containers)                    │
│  (Applications, Databases, Microservices, Gateways)         │
└──────────────────────────────┬──────────────────────────────┘
                               │ Zoom In
┌──────────────────────────────▼──────────────────────────────┐
│  Level 3: Component Diagram (Components)                    │
│  (Controllers, Services, Repositories, Internal Modules)    │
└──────────────────────────────┬──────────────────────────────┘
                               │ Zoom In (Optional)
┌──────────────────────────────▼──────────────────────────────┐
│  Level 4: Code Diagram (Code / Classes)                     │
│  (UML Class Diagrams, AST, GoF Design Patterns)             │
└─────────────────────────────────────────────────────────────┘
```

---

## 📐 Detailed Guidelines per Level

### 1. Level 1: System Context
- **Goal**: Provide a 30,000-foot view of the software system's scope.
- **Audience**: Business stakeholders, product managers, new developers, and the architecture team.
- **Represented Elements**:
  - **People (Users/Personas)**: Human actors who interact directly with the system.
  - **Software System (Focus)**: The system being designed or documented.
  - **External Software Systems**: Payment providers, corporate authentication (SSO), SaaS services, government APIs.
  - **Relationships**: Directional, with a clear description of purpose and high-level protocol (for example, `Sends payment requests via HTTPS/JSON`).

### 2. Level 2: Containers (Runtime Containers)
- **Container Definition**: Any separately executable or deployable unit that stores data or runs code (for example, a React SPA, a Spring/Node backend API, a Go worker, a PostgreSQL database, a RabbitMQ/Kafka queue, or an S3 bucket).
- **Goal**: Show the high-level shape of the software architecture and how responsibilities are distributed.
  - Frontend applications (web, mobile).
  - API gateways and reverse proxies.
  - Microservices and modular monoliths.
  - Databases (SQL, NoSQL, in-memory cache).
  - Explicit technologies and protocols (for example, `Go, REST/gRPC`, `PostgreSQL 16, TCP 5432`).

### 3. Level 3: Components (Internal Components)
- **Component Definition**: A grouping of related code encapsulated behind a clean interface (for example, Controller, Service Layer, Repository, Event Producer).
- **Goal**: Decompose a single container to detail how its internal components collaborate.
- **Guideline**: Draw component diagrams only for critical or complex containers that justify the detail.

### 4. Level 4: Code (Code / Classes)
- **Goal**: Show implementation detail at the code level (UML class diagrams, interfaces, inheritance).
- **Guideline**: In most projects, this level is generated dynamically by reverse-engineering and AST tooling via [`skills/mapping/code-architecture-mapping/SKILL.md`](../../../mapping/code-architecture-mapping/SKILL.md) or [`skills/mapping/uml-diagram-generation/SKILL.md`](../../../mapping/uml-diagram-generation/SKILL.md).

---

## 🛠️ Syntax Patterns: Mermaid.js & C4-PlantUML

### Example: Context Diagram (Level 1) in Mermaid.js C4
```mermaid
C4Context
    title Context Diagram - Digital Payments Platform

    Person(customer, "End Customer", "User who makes purchases and payments via the app.")
    Person(admin, "Financial Operator", "Internal reconciliation and compliance analyst.")

    System(payment_sys, "Payment Gateway System", "Processes financial transactions, Pix, cards and bank reconciliation.")

    System_Ext(bank_core, "Banco Central / SPI", "BACEN's Instant Payment System.")
    System_Ext(anti_fraud, "Anti-Fraud Service", "Real-time behavioral risk analysis engine.")
    System_Ext(notify_service, "Push / SMS Provider", "External notification delivery service.")

    Rel(customer, payment_sys, "Initiates transactions and queries balances", "HTTPS / JSON API")
    Rel(admin, payment_sys, "Audits reconciliation and authorizes refunds", "HTTPS / Web GUI")
    Rel(payment_sys, anti_fraud, "Queries transaction risk score", "gRPC / mTLS")
    Rel(payment_sys, bank_core, "Settles Pix transactions via DICT/SPI", "ISO 20022 / mTLS")
    Rel(payment_sys, notify_service, "Triggers confirmation alerts", "REST / HTTPS")
```

### Example: Container Diagram (Level 2) in Mermaid.js C4
```mermaid
C4Container
    title Container Diagram - Payment Gateway System

    Person(customer, "End Customer", "Mobile app user.")

    Container_Boundary(c1, "Payment Gateway System") {
        Container(mobile_app, "Mobile App", "Flutter / iOS & Android", "Interface for payments and transfers.")
        Container(api_gw, "API Gateway & WAF", "Kong Gateway / Envoy", "Routing, rate limiting and TLS termination.")
        Container(auth_svc, "Auth Service", "Go / JWT & OAuth 2.0", "Authentication and MFA token validation.")
        Container(trans_svc, "Transaction Engine", "Java Spring Boot / Kotlin", "Idempotent transaction processing.")
        Container(ledger_db, "Ledger Database", "PostgreSQL 16", "Immutable storage of accounting entries.")
        Container(msg_broker, "Event Bus", "Apache Kafka", "Streaming of transaction events for reconciliation.")
        Container(cache_store, "Idempotency Cache", "Redis Cluster", "Duplicate control and rate limits.")
    }

    System_Ext(bank_core, "Banco Central / SPI", "National Financial System Network.")

    Rel(customer, mobile_app, "Uses")
    Rel(mobile_app, api_gw, "Payment requests", "JSON / HTTPS")
    Rel(api_gw, auth_svc, "Validates credentials", "gRPC")
    Rel(api_gw, trans_svc, "Forwards authorized operations", "gRPC")
    Rel(trans_svc, cache_store, "Checks idempotency key", "Redis Protocol / RESP")
    Rel(trans_svc, ledger_db, "Writes ACID accounting records", "SQL / TCP")
    Rel(trans_svc, msg_broker, "Publishes event 'TransactionCreated'", "Kafka Protocol")
    Rel(trans_svc, bank_core, "Instant settlement", "ISO 20022 / mTLS")
```

---

## 📋 Quality Checklist for C4 Diagrams

1. **Clearly Identified Elements**:
   - Every element has a `Name`, `Type/Role`, `Primary Technology` (for Levels 2 and 3), and a `Clear Statement of Purpose`.
2. **Explicit Relationships**:
   - Every connection line must carry a present-tense verb (for example, `Queries`, `Writes`, `Publishes event`) and the transport protocol (`HTTPS`, `gRPC`, `AMQP`, `SQL/TCP`).
3. **System Focus and Boundaries**:
   - Use boundary delimiters (`System_Boundary`, `Container_Boundary`) to separate clearly what belongs to the system scope from what is external.
4. **Alignment with Documentation**:
   - Integrate C4 diagrams into Software Architecture Documents (SADs) and Architectural Decision Records (ADRs).
