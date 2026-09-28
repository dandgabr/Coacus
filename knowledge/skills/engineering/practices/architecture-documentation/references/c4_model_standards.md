# C4 Model Standards for Documentation

Definitions of the C4 Model's four levels of abstraction and how to express them in Mermaid.

## Level 1: System Context Diagram

```mermaid
C4Context
    title Context Diagram - SI Report Platform
    Person(user, "Physician / Specialist", "System user for exam validation")
    System(core_si, "SI Central System", "Management, validation, and delivery of reports")
    System_Ext(lis, "Laboratory LIS", "Source system for raw exams")
    System_Ext(iam, "Identity Provider", "SSO / OAuth2 service")

    Rel(user, core_si, "Accesses the portal and signs reports", "HTTPS")
    Rel(core_si, iam, "Authenticates the user and validates scope", "OIDC")
    Rel(lis, core_si, "Sends completed exam events", "Kafka / HL7 FHIR")
```

## Level 2: Container Diagram

```mermaid
C4Container
    title Container Diagram - SI Report Platform
    Person(user, "Physician", "System user")

    Container_Boundary(c1, "SI Central Platform") {
        Container(web_app, "SPA Frontend", "React / TypeScript", "User visual interface")
        Container(api_gw, "API Gateway", "Envoy", "Routing, TLS, and Rate Limiting")
        Container(report_svc, "Report Service", "Python / FastAPI", "Report business rules")
        ContainerDb(report_db, "Report Database", "PostgreSQL", "Encrypted transactional storage")
        ContainerQueue(event_bus, "Event Bus", "Apache Kafka", "Asynchronous messaging queue")
    }

    Rel(user, web_app, "Uses the interface", "HTTPS")
    Rel(web_app, api_gw, "API calls", "JSON/HTTPS")
    Rel(api_gw, report_svc, "Routes requests", "gRPC")
    Rel(report_svc, report_db, "Reads and writes reports", "SQL/TCP")
    Rel(report_svc, event_bus, "Publishes events", "Kafka")
```
