---
name: third-party-risk-management
description: Acts as a Third-Party Risk Management specialist covering vendor due diligence, SIG and CAIQ questionnaires, CSA STAR, ISO/IEC 27036, contractual security requirements, the DORA Register of Information, continuous monitoring and fourth-party (subprocessor) risk.
metadata:
  type: defensive
  phase: report
---

# Third-Party Risk Management (TPRM)

This skill guides the AI to manage the risk introduced by suppliers, which is where many breaches actually begin.

---

## 🧭 1. Lifecycle

1. **Intake and classification**: what data and access will the vendor have? Classify by criticality.
2. **Due diligence**: questionnaires, certifications, independent reports, references.
3. **Contracting**: security, privacy, breach notification, audit rights, data return and deletion.
4. **Onboarding**: least-privilege access, integration review, monitoring.
5. **Continuous monitoring**: security posture changes, breaches, financial and ownership changes.
6. **Offboarding**: revoke access, retrieve or destroy data, verify.

---

## 📋 2. Assessment Instruments

- **CAIQ** (based on CSA CCM) for cloud providers; **CSA STAR** registry for published results.
- **SIG** questionnaires for a broader vendor base.
- **ISO/IEC 27036** for supplier-relationship security guidance.
- **SOC 2** reports for service organizations; read the exceptions, not just the opinion.
- **DORA Register of Information** for financial entities' ICT contracts.

---

## 🔍 3. Fourth-Party Risk

A vendor's subcontractors inherit your data. Ask for the vendor's own TPRM process and the list of material subprocessors; unmanaged fourth parties are an unmonitored breach path.

---

## ⚠️ 4. Common Failures

- Collecting questionnaires once and never monitoring changes.
- Accepting a certificate as proof without checking its scope and validity.
- Granting broad integration access beyond the vendor's need.
- No contractual breach-notification timeline, so you learn of a breach from the news.

---

## 🔗 5. Integration with Other Skills

- For cloud assurance, see the [csa-cloud-security](../../iam/csa-cloud-security/SKILL.md) skill.
- For DORA obligations, see the [eu-digital-resilience-regulation](../eu-digital-resilience-regulation/SKILL.md) skill.
- For supply-chain software risk, see the [supply-chain-threat-modeling](../../operations/supply-chain-threat-modeling/SKILL.md) skill.
- For the risk scoring methodology, see the [quantitative-risk-fair](../quantitative-risk-fair/SKILL.md) skill.
