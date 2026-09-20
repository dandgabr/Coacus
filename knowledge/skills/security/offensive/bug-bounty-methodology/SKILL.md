---
name: bug-bounty-methodology
description: Acts as a Specialist in Bug Bounty and Large-Scale Vulnerability Hunting methodologies based on Bug Bounty Bootcamp (Vickie Li). Covers active/passive subdomain reconnaissance, hidden asset discovery, distributed port scanning, parameter fuzzing automation, logic flaw exploitation, and structuring professional impact reports (PoC, CVSS v3.1/v4.0, remediation).
---

# Bug Bounty Methodologies and Standards

This skill establishes the formal procedures for automated reconnaissance, attack surface mapping, high-impact vulnerability identification, and responsible report submission in **Bug Bounty** programs (HackerOne, Bugcrowd, Intigriti), based on the book **Bug Bounty Bootcamp** by Vickie Li.

---

## 🎯 1. Bug Bounty Methodological Flow

```
┌─────────────────────────────────────────────────────────────┐
│ 1. Reconhecimento Amplo (Subdomínios, ASN, WHOIS, CIDR)     │
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│ 2. Probing e Descoberta de Serviços (HTTP/S, Portas, Tecn.) │
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│ 3. Mapeamento de Conteúdo e Endpoints (JS Mining, Wayback)  │
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│ 4. Testes de Vulnerabilidades Lógicas e de Negócio          │
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│ 5. Elaboração de Relatório de Alto Impacto (Triagem & PoC)  │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔍 2. Advanced Reconnaissance and Surface Discovery

### A. Subdomain Enumeration (Horizontal & Vertical)

- **Passive**: Certificate Transparency (crt.sh), VirusTotal, Shodan, Censys, AlienVault OTX, SecurityTrails.
- **Active / Brute-force**: Contextualized wordlists with fast resolvers and Wildcard DNS verification.
- **Permutations**: Resolution of common variations (`api-`, `dev-`, `staging-`, `-internal`).

### B. JavaScript Mining and Endpoint Extraction

- Download and static analysis of all JS bundles in the application.
- Regex to extract undocumented routes, exposed API keys, staging secrets, and microservice endpoints.

---

## 💥 3. Critical High-Reward Vulnerabilities

| Vulnerability | Main Vector | Testing Approach |
| :--- | :--- | :--- |
| **IDOR / BOLA** | `/api/v1/documents/{docId}` | Creation of two user accounts (A and B). Swapping tokens/IDs to verify whether user B reads/changes A's resources. |
| **Race Conditions** | Coupons, redemptions, transfers | Simultaneous firing of parallel HTTP requests using HTTP/2 Single-Packet Attack to induce race conditions before the database lock. |
| **SSRF (Server-Side Request Forgery)** | Webhooks, image/PDF import | Injection of loopback URLs (`127.0.0.1`, `169.254.169.254` for AWS/GCP/Azure cloud metadata) or controlled servers (Collaborator/Interactsh). |
| **Business Logic Bypass** | Checkout, multi-step flows | Skipping steps in the payment flow, manipulating price parameters in requests, changing permission fields in `PATCH`. |
| **Subdomain Takeover** | CNAMEs pointing to deactivated services | Verification of DNS records pointing to unregistered S3 buckets, GitHub Pages, Heroku, or Azure App Services. |

---

## 📝 4. Professional Vulnerability Report Standard (HackerOne / Bugcrowd)

To maximize the triage score and avoid severity disputes:

1. **Descriptive Title**: `[Vulnerability] in [Component/Endpoint] allows [Business Impact]`  
   *(E.g., "IDOR in /api/v1/invoices allows any authenticated user to download invoices from other companies")*
2. **Severity & CVSS Vector**: Transparent calculation based on CVSS v3.1 / v4.0.
3. **Impact Summary**: Explanation in executive terms of the financial, reputational, or regulatory risk (LGPD/GDPR).
4. **Step-by-Step Reproduction (PoC)**:
   - Complete HTTP requests (cURL or raw HTTP).
   - Data from two distinct test accounts.
5. **Proof of Concept (Evidence)**: Screenshots, logs, or screen recording with restricted impact (without massively exploiting other users).
6. **Remediation Recommendation**: Suggested code or configuration to fix the root cause.

## 🔢 Version Sources

Moving release pins in this skill were resolved 2026-09-20:

- **CVSS v3.1** (verified) — first.org/cvss
- **CVSS v4.0** (verified) — first.org/cvss
