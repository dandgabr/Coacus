# C4 Model Standards for Documentation

Definitions of the C4 Model's four levels of abstraction and how to express them in Mermaid.

## Level 1: System Context Diagram

```mermaid
C4Context
    title Diagrama de Contexto - Plataforma de Laudos SI
    Person(user, "Médico / Especialista", "Usuário do sistema para validação de exames")
    System(core_si, "Sistema Central SI", "Gerenciamento, validação e entrega de laudos")
    System_Ext(lis, "LIS Laboratorial", "Sistema de origem dos exames brutos")
    System_Ext(iam, "Identity Provider", "Serviço SSO / OAuth2")

    Rel(user, core_si, "Acessa portal e assina laudos", "HTTPS")
    Rel(core_si, iam, "Autentica usuário e valida escopo", "OIDC")
    Rel(lis, core_si, "Envia eventos de exames concluídos", "Kafka / HL7 FHIR")
```

## Level 2: Container Diagram

```mermaid
C4Container
    title Diagrama de Contêineres - Plataforma de Laudos SI
    Person(user, "Médico", "Usuário do sistema")

    Container_Boundary(c1, "Plataforma Central SI") {
        Container(web_app, "Frontend SPA", "React / TypeScript", "Interface visual do usuário")
        Container(api_gw, "API Gateway", "Envoy", "Roteamento, TLS e Rate Limiting")
        Container(report_svc, "Report Service", "Python / FastAPI", "Regras de negócio de laudos")
        ContainerDb(report_db, "Report Database", "PostgreSQL", "Armazenamento transacional cifrado")
        ContainerQueue(event_bus, "Event Bus", "Apache Kafka", "Fila de mensageria assíncrona")
    }

    Rel(user, web_app, "Usa interface", "HTTPS")
    Rel(web_app, api_gw, "Chamadas de API", "JSON/HTTPS")
    Rel(api_gw, report_svc, "Roteia requisições", "gRPC")
    Rel(report_svc, report_db, "Lê e grava laudos", "SQL/TCP")
    Rel(report_svc, event_bus, "Publica eventos", "Kafka")
```
