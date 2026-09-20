# Complete Mermaid.js Syntax Guide for Architecture and Documentation

Detailed syntax for every diagram type used in software and security documentation.

## 1. Flowchart with Trust Boundaries

```mermaid
flowchart LR
    subgraph Internet ["Zona Externa (Não Confiável)"]
        User["Cliente Web / Mobile"]
    end

    subgraph DMZ ["Borda de Segurança (DMZ)"]
        WAF["WAF Cloudflare"]
        Proxy["Reverse Proxy NGINX"]
    end

    subgraph VPC ["Rede Privada (VPC Interna)"]
        API["API Gateway (OAuth2/JWT)"]
        ServiceA["Service de Cadastro"]
        ServiceB["Service de Cobrança"]
    end

    subgraph SecureDB ["Zona de Armazenamento Seguro"]
        DB[(PostgreSQL Cifrado)]
    end

    User -->|HTTPS TLS 1.3| WAF --> Proxy
    Proxy -->|mTLS| API
    API --> ServiceA & ServiceB
    ServiceA --> DB
```

## 2. Secure Authentication Sequence Diagram

```mermaid
sequenceDiagram
    autonumber
    actor User as Usuário
    participant App as Frontend SPA
    participant IdP as Provedor IAM (OIDC)
    participant API as Backend API

    User->>+App: Clica em Login
    App->>+IdP: Redireciona com PKCE + State
    IdP-->>-User: Exibe tela de MFA
    User->>+IdP: Fornece credencial + TOTP
    IdP-->>-App: Retorna Código de Autorização
    App->>+IdP: Troca Código + Code Verifier por Tokens
    IdP-->>-App: Retorna Access Token (JWT) e ID Token
    App->>+API: GET /api/v1/profile (Bearer JWT)
    API-->>-App: 200 OK (Dados do perfil)
```
