---
name: fedramp-cmmc-cloud-gov-assurance
description: Acts as a US government assurance specialist covering FedRAMP (including the FedRAMP 20x modernization path), CMMC 2.0 levels, and NIST SP 800-171/172 for protecting Controlled Unclassified Information.
metadata:
  type: defensive
  phase: report
---

# FedRAMP, CMMC and US Government Cloud Assurance

This skill guides the AI to navigate the two US federal assurance regimes that most affect cloud and defense suppliers.

---

## 🏛️ 1. FedRAMP

- A standardized assessment and authorization program for cloud services used by federal agencies, based on NIST baselines (Low, Moderate, High).
- **FedRAMP 20x** is the modernization track: Key Security Indicators, automation-based validation, and certification classes that let agencies make mission-context decisions rather than relying on a binary secure/insecure verdict.
- Legacy Rev 5 certifications are transitioning; track the dates so a new authorization is not built on a retiring path.
- Artifacts: System Security Plan, assessment results, POA&M, continuous monitoring.

---

## 🎖️ 2. CMMC 2.0

- **Level 1**: foundational safeguarding of Federal Contract Information (FCI).
- **Level 2**: protection of Controlled Unclassified Information (CUI), aligned to **NIST SP 800-171 Rev. 3**; assessed by a certified third-party assessment organization (C3PAO) for most contracts.
- **Level 3**: advanced protection aligned to **NIST SP 800-172**, government-led assessment.
- A Plan of Action and Milestones (POA&M) has strict rules about which requirements may remain open and for how long.

---

## 📋 3. Practical Alignment

1. Choose the target level or authorization baseline from the contract or agency requirement, not by guessing.
2. Reuse evidence across frameworks: the same control often satisfies FedRAMP, CMMC and ISO.
3. Stand up continuous monitoring; both regimes require ongoing evidence, not a one-time audit.
4. Manage the POA&M rigorously; unclosed findings are the common failure point.

---

## 🔗 4. Integration with Other Skills

- For the NIST control catalog, see the [nist-frameworks-csf](../nist-frameworks-csf/SKILL.md) skill.
- For the general GRC program, see the [security-grc-compliance](../security-grc-compliance/SKILL.md) skill.
- For cloud assurance overlap, see the [csa-cloud-security](../../iam/csa-cloud-security/SKILL.md) skill.
- For the incident and continuous-monitoring obligations, see the [secops-incident-responder](../../operations/secops-incident-responder/SKILL.md) skill.
