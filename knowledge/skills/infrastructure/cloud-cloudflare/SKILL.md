---
name: "cloud-cloudflare"
description: "Acts as a specialist on the Cloudflare platform, covering the new unified cf CLI, Wrangler v3/v4, C3 (create-cloudflare), private tunnels with cloudflared, Edge Compute (Workers, Pages, Durable Objects, Workers AI), edge storage (D1, R2, KV, Vectorize, Hyperdrive, Queues), security (WAF Managed Rulesets, Turnstile, Rate Limiting, SSL/TLS), and Cloudflare Zero Trust architecture."
---

# ☁️ Skill: Cloudflare Platform, Edge Computing & the New `cf` CLI Specialist

This skill enables the artificial intelligence to act as a **Senior Cloudflare Engineer and Architect**. Its domain spans the entire Cloudflare global platform, from the development and orchestration of microservices and full-stack applications at the edge (*Edge Computing*) to the governance of Anycast networks, perimeter security (WAF, DDoS, Turnstile), low-latency distributed storage, and complete administration through the **new unified `cf` CLI**, **Wrangler**, **C3**, and **`cloudflared`**.

---

## ⚡ 1. Command-Line Tools (Cloudflare CLIs)

Cloudflare offers an integrated set of command-line tools for automation, local development, and global operations:

```text
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                          ECOSSISTEMA DE CLIS CLOUDFLARE                                │
├─────────────────────────┬─────────────────────────┬────────────────────────────────────┤
│ 🚀 CLI Unificada `cf`   │ 🛠️ Wrangler CLI (v3/v4) │ 🔒 cloudflared CLI                 │
├─────────────────────────┼─────────────────────────┼────────────────────────────────────┤
│ • npx cf                │ • npx wrangler dev      │ • cloudflared tunnel create        │
│ • Superfície unificada  │ • npx wrangler deploy   │ • Zero-port reverse proxy          │
│ • Design para Agentes/IA│ • npx wrangler types    │ • Ingress rules privadas           │
│ • Gerencia toda a conta │ • Local Miniflare/workerd│ • Integração Zero Trust Access    │
└─────────────────────────┴─────────────────────────┴────────────────────────────────────┘
```

### 1.1. The New Unified `cf` CLI (`npx cf`)
The `cf` CLI is Cloudflare's next-generation command-line interface, designed to consolidate all products and APIs of the platform under a predictable, consistent syntax, purpose-built to be consumed by both engineers and **autonomous AI agents**:

```bash
# Execução direta via npx ou instalação global
npx cf --help
npm install -g cf

# Autenticação e contexto de conta
cf login
cf whoami
cf accounts list

# Inspeção e gerenciamento de recursos globais
cf zones list
cf dns records list --zone <zone_id>
cf workers list
cf r2 buckets list
cf d1 databases list
```

### 1.2. Wrangler CLI (v3/v4): Developing and Deploying Workers & Pages
Wrangler is the heart of the development lifecycle for edge applications:

```bash
# Inicialização e desenvolvimento local (emulado com motor nativo workerd / Miniflare)
npx wrangler dev
npx wrangler dev --remote         # Executa contra recursos reais da Cloudflare

# Geração automática de contratos de tipagem TypeScript a partir do wrangler.jsonc/toml
npx wrangler types

# Deploy para produção ou ambientes específicos (staging/preview)
npx wrangler deploy
npx wrangler deploy --env staging

# Gerenciamento de segredos de ambiente criptografados
npx wrangler secret put API_SECRET_KEY
npx wrangler secret list
npx wrangler secret delete API_SECRET_KEY

# Streaming de telemetria e logs de execução em tempo real
npx wrangler tail
npx wrangler tail --format pretty --status error
```

### 1.3. C3 (`create-cloudflare`): Project Scaffolding
Standardized initialization of Workers and Pages applications with modern templates:
```bash
# Inicialização interativa de novos projetos com frameworks suportados
npm create cloudflare@latest meu-projeto-edge
# Suporta: Hono, Astro, Next.js (OpenNext), Remix, Nuxt, SvelteKit
```

### 1.4. `cloudflared` CLI: Private Tunnels and Zero Trust
Connects local servers, containers, and networks directly to Cloudflare's network without exposing any public inbound port to the internet:

```bash
# Autenticação do cloudflared com a conta Cloudflare
cloudflared tunnel login

# Criação de um túnel nomeado
cloudflared tunnel create producao-tunnel

# Roteamento de tráfego DNS para o túnel
cloudflared tunnel route dns producao-tunnel api.minhaempresa.com

# Execução do túnel baseado no arquivo de configuração
cloudflared tunnel run producao-tunnel
```

#### `config.yml` Example for Private Ingress Rules:
```yaml
tunnel: <UUID_DO_TUNEL>
credentials-file: /etc/cloudflared/<UUID_DO_TUNEL>.json

ingress:
  # Roteamento para microsserviço interno seguro
  - hostname: api.minhaempresa.com
    service: http://localhost:8080
    originRequest:
      connectTimeout: 10s
      noTLSVerify: false
  # Fallback obrigatório: retorna 404 para qualquer outro tráfego
  - service: http_status:404
```

---

## ⚡ 2. Edge Compute & Runtime (Workers, Pages & Durable Objects)

### 2.1. V8 Isolates Architecture (`workerd`)
Unlike traditional containers and serverless functions (such as AWS Lambda) that depend on heavyweight virtual machines or Node.js processes with 200ms–2s cold starts, Cloudflare Workers run on the open-source **`workerd`** engine with **V8 Isolates**:
- **Zero Cold Start** (< 5 milliseconds).
- **Minimal Memory Consumption**: Hundreds of isolates share the same process with secure memory isolation at the V8 runtime level.
- **Web Standards Patterns**: Native support for `Fetch API`, `Streams`, `Web Crypto`, `TextEncoder/TextDecoder`, `URLPattern`.

### 2.2. Canonical TypeScript Worker Example (`wrangler.jsonc`)

#### `wrangler.jsonc` Configuration:
```jsonc
{
  "$schema": "node_modules/wrangler/config-schema.json",
  "name": "api-gateway-edge",
  "main": "src/index.ts",
  "compatibility_date": "2024-09-01",
  "compatibility_flags": ["nodejs_compat"],
  // Binds para Bancos e Armazenamento
  "d1_databases": [
    {
      "binding": "DB",
      "database_name": "app-production-db",
      "database_id": "xxxx-xxxx-xxxx"
    }
  ],
  "r2_buckets": [
    {
      "binding": "STORAGE",
      "bucket_name": "app-media-bucket"
    }
  ],
  "kv_namespaces": [
    {
      "binding": "CACHE_KV",
      "id": "yyyy-yyyy-yyyy"
    }
  ]
}
```

#### Worker TypeScript Code (`src/index.ts`):
```typescript
export interface Env {
  DB: D1Database;
  STORAGE: R2Bucket;
  CACHE_KV: KVNamespace;
  API_SECRET_KEY: string;
}

export default {
  async fetch(request: Request, env: Env, ctx: ExecutionContext): Promise<Response> {
    const url = new URL(request.url);

    // Rota de Health Check
    if (url.pathname === "/health") {
      return new Response(JSON.stringify({ status: "healthy", region: request.cf?.colo }), {
        headers: { "Content-Type": "application/json" }
      });
    }

    // Consulta otimizada com D1 (SQLite distribuído)
    if (url.pathname === "/users" && request.method === "GET") {
      // Checa cache na borda via KV
      const cached = await env.CACHE_KV.get("active_users", "json");
      if (cached) {
        return Response.json(cached, { headers: { "X-Cache": "HIT" } });
      }

      const { results } = await env.DB.prepare(
        "SELECT id, name, email, created_at FROM users WHERE active = 1 LIMIT 50"
      ).all();

      // Salva no KV em background sem bloquear a resposta ao usuário
      ctx.waitUntil(env.CACHE_KV.put("active_users", JSON.stringify(results), { expirationTtl: 300 }));

      return Response.json(results, { headers: { "X-Cache": "MISS" } });
    }

    return new Response("Not Found", { status: 404 });
  }
};
```

---

## 💾 3. Edge Storage and Databases

Cloudflare offers a complete suite of serverless persistence at the edge:

| Service | Data Model | Primary Use Case | Technical Differentiator |
| :--- | :--- | :--- | :--- |
| **D1** | Relational SQL (SQLite) | Profiles, authentication, catalogs, transactions | Global read replicas, ACID, no provisioning. |
| **R2** | Object Storage (S3 API) | Media, uploads, backups, ML datasets | **Zero Egress Fees** (no data-egress charge). |
| **Workers KV** | Global Key-Value | Configuration, tokens, session cache | Distributed ultra-fast reads (sub-millisecond). |
| **Vectorize** | Vector Embedding Database | Semantic search, RAG, AI classification | Native integration with Workers AI and embedding models. |
| **Hyperdrive** | SQL Connection Accelerator | External PostgreSQL and MySQL | Connection pooling and query caching at the global edge. |
| **Queues** | Asynchronous Messaging Queues | Batch processing, data pipelines | Guaranteed *at-least-once* delivery, no queue servers. |

### 3.1. D1: Migrations and Queries
```bash
# Criação do banco D1
npx wrangler d1 create app-production-db

# Criação de arquivo de migração
npx wrangler d1 migrations create app-production-db criar_tabela_usuarios

# Aplicação local das migrações
npx wrangler d1 migrations apply app-production-db --local

# Aplicação em produção na borda global
npx wrangler d1 migrations apply app-production-db --remote
```

### 3.2. R2: S3-Compatible Storage
```typescript
// Upload de arquivo para o R2 com metadados customizados
await env.STORAGE.put("uploads/relatorio.pdf", request.body, {
  httpMetadata: { contentType: "application/pdf" },
  customMetadata: { autor: "sistema", data: new Date().toISOString() }
});

// Download com streaming direto
const object = await env.STORAGE.get("uploads/relatorio.pdf");
if (!object) return new Response("Objeto não encontrado", { status: 404 });

const headers = new Headers();
object.writeHttpMetadata(headers);
headers.set("etag", object.httpEtag);
return new Response(object.body, { headers });
```

---

## 🛡️ 4. Edge Security, WAF, DNS & Zero Trust

### 4.1. Web Application Firewall (WAF) & Managed Rulesets
- **Cloudflare Managed Ruleset**: Rules maintained and dynamically updated by Cloudflare's threat-intelligence team against zero-day vulnerabilities (e.g., Log4j, Spring4Shell).
- **OWASP Core Ruleset**: Rigorous protection against the OWASP Top 10 (SQLi, XSS, RFI/LFI) with a configurable anomaly score (*Paranoia Level* 1 to 4).
- **Custom Rules**: Boolean expressions for blocking and challenging:
  ```text
  (http.request.uri.path contains "/admin" and not ip.src in {203.0.113.0/24}) -> Action: Block
  (cf.threat_score gt 40 and not cf.client.bot) -> Action: Managed Challenge
  ```
- **Rate Limiting Rules**: Protection against brute force and resource exhaustion by limiting, for example, 5 requests per minute to the `/api/login` endpoint per IP address.

### 4.2. Cloudflare Turnstile: Frictionless Anti-Bot Protection
A smart, privacy-preserving replacement for intrusive CAPTCHAs:
- Invisible validation of browser telemetry with no irritating visual challenges.
- Server-side verification through a simple HTTP call:
```typescript
const formData = await request.formData();
const token = formData.get("cf-turnstile-response");
const ip = request.headers.get("CF-Connecting-IP");

const verifyRes = await fetch("https://challenges.cloudflare.com/turnstile/v0/siteverify", {
  method: "POST",
  headers: { "Content-Type": "application/x-www-form-urlencoded" },
  body: new URLSearchParams({
    secret: env.TURNSTILE_SECRET_KEY,
    response: token as string,
    remoteip: ip || ""
  })
});

const outcome = await verifyRes.json<{ success: boolean }>();
if (!outcome.success) {
  return new Response("Falha na validação anti-bot", { status: 403 });
}
```

### 4.3. Anycast DNS, Caching & SSL/TLS
- **Anycast DNS**: Resolution with an average global latency under 15ms, automatic DNSSEC support, and CNAME flattening at the root (`@`).
- **Cache Rules**: Granular TTL control at the edge, ignoring or honoring `Cache-Control` headers per URI or extension.
- **SSL/TLS Mode**:
  - *Full (Strict)*: Requires a valid TLS certificate issued by a trusted authority on the origin server.
  - *mTLS (Mutual TLS)*: Mutual authentication with client certificates for APIs and microservice-to-microservice communication.

### 4.4. Cloudflare Zero Trust Architecture (Cloudflare One)
- **Cloudflare Access**: Protection of internal applications without a VPN through an authenticated reverse proxy with corporate identity providers (Google Workspace, Okta, Microsoft Entra ID).
- **Cloudflare Gateway**: Deep inspection of outbound DNS, HTTP/HTTPS, and network traffic with malware filtering and DLP (Data Loss Prevention) policies.
- **Device Posture**: Access granting conditioned on the health of the user's machine (presence of antivirus, encrypted disk, and OS version).
