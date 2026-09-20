---
name: nis2-cra-compliance
description: Acts as a NIS2 and EU Cyber Resilience Act compliance specialist covering essential and important entities, Article 21 risk-management measures, the 24h/72h/1-month incident reporting clocks, management accountability, and the CRA product security lifecycle with its 2026 reporting obligations.
metadata:
  type: defensive
  phase: report
---

# NIS2 and the Cyber Resilience Act

This skill guides the AI to implement the two broad EU instruments that sit alongside DORA: **NIS2** for entities and their incident obligations, and the **CRA** for products placed on the EU market.

---

## 🇪🇺 1. NIS2 (Directive (EU) 2022/2555)

- Applies to **essential** and **important** entities across 18 critical sectors; sizes and sector determine the category.
- **Article 21** requires risk-management measures: risk analysis, incident handling, business continuity and backup, supply-chain security, secure development and vulnerability disclosure, cryptography, access control and MFA.
- **Incident reporting**: an early warning within **24 hours**, an incident notification within **72 hours**, and a final report within **one month**.
- **Management accountability**: the governing body approves and can be held liable for non-compliance.
- Where DORA applies (financial entities), DORA prevails for the covered areas.

---

## 🛡️ 2. Cyber Resilience Act (Regulation (EU) 2024/2847)

- Applies to products with digital elements placed on the EU market; obligations scale with importance/criticality.
- Requirements span the whole lifecycle: secure by default, vulnerability handling, security updates, an SBOM, and coordinated vulnerability disclosure.
- **Timeline**: in force since December 2024; **reporting of actively exploited vulnerabilities from 11 September 2026**; main obligations from 11 December 2027.
- Manufacturers must notify actively exploited vulnerabilities and severe incidents to ENISA via the single reporting platform.
- Conformity assessment (and, for important/critical products, a notified body) leads to CE marking.

---

## 📋 3. Practical Program

1. Determine entity classification (NIS2) and product classification (CRA).
2. Map current controls to Article 21 and to the CRA essential requirements.
3. Stand up the incident-reporting workflow with the statutory clocks.
4. Build the SBOM and vulnerability-handling process for CRA products.
5. Assign management accountability and evidence.

---

## 🔗 4. Integration with Other Skills

- For the financial-sector counterpart, see the [eu-digital-resilience-regulation](../eu-digital-resilience-regulation/SKILL.md) skill.
- For product security lifecycle, see the [secure-sdlc-ssdf](../../appsec/secure-sdlc-ssdf/SKILL.md) skill.
- For SBOM, see the [program-sbom-tooling](../../tooling/program-sbom-tooling/SKILL.md) skill.
- For incident response, see the [secops-incident-responder](../../operations/secops-incident-responder/SKILL.md) skill.
