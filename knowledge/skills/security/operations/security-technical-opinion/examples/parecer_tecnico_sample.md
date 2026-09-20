# Information Security Technical Opinion: Integration of the Medical Reports Portal and Partners

**Opinion Number:** SEC-ARQ-2026-0042  
**Issue Date:** 24/08/2026  
**Responsible Engineer:** Security Architect Agent  
**Verdict:** `APROVADO COM CONDIÇÕES`

---

## 1. Executive Summary
The initiative consists of an integration between the Medical Reports Portal and a third-party Diagnostic AI provider via a REST API. The solution was evaluated against the corporate risk matrix and the OWASP ASVS v5.0.0 standards. One P0 risk was identified (a Go-Live blocker) along with two P1 risks, conditioned on the execution of Wave 1 for release to production.

---

## 2. Security Gating and Go-Live Blockers (Wave 1 – 7-day SLA)

| ID | Classification | Risk Description | Mandatory Pre-Go-Live Action | Status |
| :--- | :--- | :--- | :--- | :--- |
| **BLK-01** | 🔴 **P0 (Critical)** | API token transmitted in a URL query parameter in the webhooks | Move the token to the `Authorization: Bearer <token>` header and enforce mandatory TLS 1.3 | Pending |

---

## 3. Three-Wave Remediation Roadmap

### 🌊 Wave 1: Pre-Go-Live (Within 7 days)
- [ ] Fix the token being sent in the HTTP header (BLK-01).
- [ ] Formal signature of the DPA / LGPD addendum by the partner.

### 🌊 Wave 2: Priority Post-Go-Live (Within 30 days)
- [ ] Implementation of mutual mTLS between the API Gateway and the AI partner.
- [ ] Forwarding of authentication logs to the corporate SIEM.

### 🌊 Wave 3: Resilience and Governance (30 to 180 days)
- [ ] Automated semi-annual rotation of API keys via Vault.
- [ ] Focused black-box pentest on the webhook endpoint.
