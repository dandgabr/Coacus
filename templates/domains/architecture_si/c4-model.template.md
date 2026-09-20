# C4 Model Visual Modeling Template with Mermaid.js

This template provides ready-made structures for the four C4 Model levels in Mermaid.js syntax.

---

## 1. Level 1: System Context Diagram (System Context)

```mermaid
C4Context
    title System Context Diagram - [System Name]

    Person(user_primary, "[Primary User]", "[Description of the user's role and goal]")
    Person(admin_user, "[Administrator / Operator]", "[Internal management user]")

    System(core_system, "[Assessed System]", "[Description of the assessed software's core function]")

    System_Ext(ext_auth, "[SSO / IAM Provider]", "[Federated authentication OAuth2 / OIDC]")
    System_Ext(ext_partner, "[Partner System / External API]", "[Data source or partner service]")
    System_Ext(ext_notification, "[Notification Service]", "[Email, SMS, or Push delivery]")

    Rel(user_primary, core_system, "Accesses features via Web/App", "HTTPS / TLS 1.3")
    Rel(admin_user, core_system, "Manages settings and auditing", "HTTPS / MFA")
    Rel(core_system, ext_auth, "Validates tokens and permissions", "OAuth2 / OIDC")
    Rel(core_system, ext_partner, "Consumes transactional data", "REST / mTLS")
    Rel(core_system, ext_notification, "Triggers alerts", "HTTPS / API Key")
```

---

## 2. Level 2: Container Diagram (Containers)

```mermaid
C4Container
    title Container Diagram - [System Name]

    Person(user, "[User]", "[End user]")

    Container_Boundary(c1, "[Application / System Boundary]") {
        Container(spa, "Single-Page Application", "React / TypeScript", "Browser-based user interface")
        Container(api_gw, "API Gateway / BFF", "Envoy / Kong", "Authentication, rate limiting, and TLS termination")
        Container(core_api, "Core Service", "Python / FastAPI", "Business rules and core processing")
        Container(worker, "Async Worker", "Python / Celery", "Asynchronous batch task processing")
        ContainerDb(db_main, "Primary Database", "PostgreSQL (AES-256)", "Relational storage of business data")
        ContainerQueue(queue_bus, "Message Broker", "Apache Kafka / RabbitMQ", "Asynchronous messaging queue")
    }

    Rel(user, spa, "Browses and interacts", "HTTPS")
    Rel(spa, api_gw, "API calls", "JSON / HTTPS")
    Rel(api_gw, core_api, "Routes authenticated calls", "gRPC / mTLS")
    Rel(core_api, db_main, "Reads and writes data", "TCP / SQL")
    Rel(core_api, queue_bus, "Publishes events", "Kafka Protocol")
    Rel(queue_bus, worker, "Consumes messages", "Kafka Protocol")
    Rel(worker, db_main, "Updates status", "TCP / SQL")
```

---

## 3. Level 3: Component Diagram (Components)

```mermaid
C4Component
    title Component Diagram - [Container / Microservice Name]

    Container_Boundary(api_service, "[Core Service]") {
        Component(controller, "REST Controller", "FastAPI Router", "Validates endpoints and input schemas")
        Component(auth_filter, "Auth Middleware", "JWT / Security Filter", "Validates JWT token signatures and claims")
        Component(domain_service, "Domain Service", "Business Logic", "Executes pure business rules")
        Component(repo_adapter, "Repository Adapter", "SQLAlchemy / DAO", "Abstracts database persistence")
        Component(event_publisher, "Event Publisher", "Kafka Client", "Publishes structured domain events")
    }

    Rel(controller, auth_filter, "Delegates security validation", "")
    Rel(controller, domain_service, "Invokes use case", "")
    Rel(domain_service, repo_adapter, "Persists entities", "")
    Rel(domain_service, event_publisher, "Emits business event", "")
```

---

## 4. Trust and Security Zone Diagram (Trust Boundaries)

```mermaid
flowchart LR
    subgraph ZonePublic ["Untrusted Zone (Internet)"]
        Client["Web / Mobile Client"]
    end

    subgraph ZoneDMZ ["Security Edge (DMZ)"]
        WAF["WAF / DDoS Protection"]
        LB["Load Balancer (TLS 1.3 Termination)"]
    end

    subgraph ZoneInternal ["Trusted Zone (Private VPC)"]
        GW["API Gateway (mTLS / OAuth2)"]
        Service["Business Microservice"]
    end

    subgraph ZoneSecure ["High-Security Restricted Zone"]
        DB[(Encrypted Database)]
        Vault["Secrets Vault (KMS/Vault)"]
    end

    Client -->|1. HTTPS| WAF --> LB
    LB -->|2. Secure Forwarding| GW
    GW -->|3. mTLS| Service
    Service -->|4. Authenticated Connection| DB
    Service -.->|5. JIT Secret Lookup| Vault
```
