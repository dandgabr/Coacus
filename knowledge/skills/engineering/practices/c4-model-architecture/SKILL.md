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
│  Nível 1: Diagrama de Contexto de Sistema (System Context)  │
│  (Pessoas e Sistemas de Software ao redor do ecossistema)   │
└──────────────────────────────┬──────────────────────────────┘
                               │ Zoom In
┌──────────────────────────────▼──────────────────────────────┐
│  Nível 2: Diagrama de Contêineres (Containers)              │
│  (Aplicações, Bancos de Dados, Microserviços, Gateways)     │
└──────────────────────────────┬──────────────────────────────┘
                               │ Zoom In
┌──────────────────────────────▼──────────────────────────────┐
│  Nível 3: Diagrama de Componentes (Components)              │
│  (Controladores, Serviços, Repositórios, Módulos internos)  │
└──────────────────────────────┬──────────────────────────────┘
                               │ Zoom In (Opcional)
┌──────────────────────────────▼──────────────────────────────┐
│  Nível 4: Diagrama de Código (Code / Classes)               │
│  (Diagramas de Classes UML, AST, Padrões de Projeto GoF)    │
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
  - **Relationships**: Directional, with a clear description of purpose and high-level protocol (for example, `Envia requisições de pagamento via HTTPS/JSON`).

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
    title Diagrama de Contexto - Plataforma de Pagamentos Digitais

    Person(customer, "Cliente Final", "Usuário que realiza compras e pagamentos via aplicativo.")
    Person(admin, "Operador Financeiro", "Analista interno de conciliação e compliance.")

    System(payment_sys, "Payment Gateway System", "Processa transações financeiras, Pix, cartões e conciliação bancária.")

    System_Ext(bank_core, "Banco Central / SPI", "Sistema de Pagamentos Instantâneos do BACEN.")
    System_Ext(anti_fraud, "Serviço Antifraude", "Motor de análise comportamental de risco em tempo real.")
    System_Ext(notify_service, "Push / SMS Provider", "Serviço externo de entrega de notificações.")

    Rel(customer, payment_sys, "Inicia transações e consulta saldos", "HTTPS / JSON API")
    Rel(admin, payment_sys, "Audita conciliação e autoriza estornos", "HTTPS / Web GUI")
    Rel(payment_sys, anti_fraud, "Consulta score de risco de transação", "gRPC / mTLS")
    Rel(payment_sys, bank_core, "Liquida transações Pix via DICT/SPI", "ISO 20022 / mTLS")
    Rel(payment_sys, notify_service, "Dispara alertas de confirmação", "REST / HTTPS")
```

### Example: Container Diagram (Level 2) in Mermaid.js C4
```mermaid
C4Container
    title Diagrama de Contêineres - Payment Gateway System

    Person(customer, "Cliente Final", "Usuário do aplicativo móvel.")

    Container_Boundary(c1, "Payment Gateway System") {
        Container(mobile_app, "Mobile App", "Flutter / iOS & Android", "Interface para pagamentos e transferências.")
        Container(api_gw, "API Gateway & WAF", "Kong Gateway / Envoy", "Roteamento, rate limiting e terminação TLS.")
        Container(auth_svc, "Auth Service", "Go / JWT & OAuth 2.0", "Autenticação e validação de tokens MFA.")
        Container(trans_svc, "Transaction Engine", "Java Spring Boot / Kotlin", "Processamento idempotente de transações.")
        Container(ledger_db, "Ledger Database", "PostgreSQL 16", "Armazenamento imutável de lançamentos contábeis.")
        Container(msg_broker, "Event Bus", "Apache Kafka", "Streaming de eventos de transação para conciliação.")
        Container(cache_store, "Idempotency Cache", "Redis Cluster", "Controle de duplicação e rate limits.")
    }

    System_Ext(bank_core, "Banco Central / SPI", "Rede do Sistema Financeiro Nacional.")

    Rel(customer, mobile_app, "Utiliza")
    Rel(mobile_app, api_gw, "Requisições de pagamento", "JSON / HTTPS")
    Rel(api_gw, auth_svc, "Valida credenciais", "gRPC")
    Rel(api_gw, trans_svc, "Encaminha operações autorizadas", "gRPC")
    Rel(trans_svc, cache_store, "Verifica chave de idempotência", "Redis Protocol / RESP")
    Rel(trans_svc, ledger_db, "Grava registros contábeis ACID", "SQL / TCP")
    Rel(trans_svc, msg_broker, "Publica evento 'TransactionCreated'", "Kafka Protocol")
    Rel(trans_svc, bank_core, "Liquidação instantânea", "ISO 20022 / mTLS")
```

---

## 📋 Quality Checklist for C4 Diagrams

1. **Clearly Identified Elements**:
   - Every element has a `Name`, `Type/Role`, `Primary Technology` (for Levels 2 and 3), and a `Clear Statement of Purpose`.
2. **Explicit Relationships**:
   - Every connection line must carry a present-tense verb (for example, `Consulta`, `Grava`, `Publica evento`) and the transport protocol (`HTTPS`, `gRPC`, `AMQP`, `SQL/TCP`).
3. **System Focus and Boundaries**:
   - Use boundary delimiters (`System_Boundary`, `Container_Boundary`) to separate clearly what belongs to the system scope from what is external.
4. **Alignment with Documentation**:
   - Integrate C4 diagrams into Software Architecture Documents (SADs) and Architectural Decision Records (ADRs).
