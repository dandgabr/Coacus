---
name: eu-digital-resilience-regulation
description: Acts as a DORA (EU Digital Operational Resilience Act, Regulation 2022/2554) compliance specialist covering the five pillars of ICT risk management, incident reporting, digital operational resilience testing including TLPT, ICT third-party risk with the Register of Information and CTPP oversight.
metadata:
  type: defensive
  phase: report
---

# DORA - EU Digital Operational Resilience Act

This skill guides the AI to implement and audit compliance with **DORA (Regulation (EU) 2022/2554)**, which applies to financial entities and their critical ICT third-party providers. DORA has applied since 17 January 2025.

---

## 🏛️ 1. The Five Pillars

1. **ICT Risk Management**: a documented, board-owned framework integrated into the entity's risk management, with identification, protection, detection, response and recovery.
2. **ICT-Related Incident Reporting**: a management process with classification criteria, initial notification, intermediate report and final report within fixed timelines.
3. **Digital Operational Resilience Testing**: a risk-based testing program including vulnerability assessments, scenario-based tests, and for significant entities **TLPT (Threat-Led Penetration Testing)** aligned with TIBER-EU.
4. **ICT Third-Party Risk Management**: due diligence, contractual requirements, a **Register of Information** on all ICT contracts, and oversight of Critical ICT Third-Party Providers (CTPPs) designated by the ESAs.
5. **Information Sharing**: voluntary sharing of cyber threat intelligence within trusted communities.

---

## 📋 2. Key Artifacts

- **Register of Information**: the structured inventory of every ICT third-party arrangement; a supervisory focal point.
- **Incident classification and reporting templates**: consistent with the ESAs' technical standards.
- **Resilience testing plan and TLPT scope**: documented, with findings tracked to closure.
- **Exit strategies** for critical providers to avoid lock-in.

---

## 🤝 3. Interaction with Other Regimes

- DORA is **lex specialis** for financial entities and displaces NIS2 in the areas it covers.
- DORA's third-party requirements overlap with general supply-chain security and cloud assurance; map them together rather than duplicating programs.

---

## 🔗 4. Integration with Other Skills

- For the EU cyber-regulation landscape, see the [nis2-cra-compliance](../nis2-cra-compliance/SKILL.md) skill.
- For third-party assurance, see the [third-party-risk-management](../third-party-risk-management/SKILL.md) skill.
- For ICT third-party cloud assurance, see the [csa-cloud-security](../../iam/csa-cloud-security/SKILL.md) skill.
- For incident handling, see the [secops-incident-responder](../../operations/secops-incident-responder/SKILL.md) skill.
