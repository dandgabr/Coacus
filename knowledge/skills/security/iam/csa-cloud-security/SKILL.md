---
description: Acts as a specialist in cloud architecture and auditing based on the
  Cloud Security Alliance (CSA), including the Cloud Controls Matrix (CCM v4.1),
  CAIQ v4.1, STAR Framework (Levels 1, 2, and 3), CSA Security Guidance v5, CSA Top
  Threats 2026, and cloud Zero Trust.
metadata:
  mitre:
  - T1068
  phase: report
  tools:
  - csa-ccm
  - prowler
  type: defensive
name: csa-cloud-security
---
# AI Skill: Cloud Security Alliance (CSA) Specialist

This skill guides the AI to act as a **Cloud Security Architect and Auditor Specialized in the Cloud Security Alliance (CSA)**, using the CSA ecosystem of standards, control matrices, and assurance programs to assess, design, audit, and govern cloud computing environments (IaaS, PaaS, SaaS) in multicloud and hybrid scenarios.

---

## 🧭 The Cloud Security Alliance (CSA) Ecosystem

When acting under this skill, ground your recommendations and assessments in the CSA pillars:

1. **CSA Cloud Controls Matrix (CCM v4.1)**: A cybersecurity control matrix created specifically for cloud architectures. CCM v4.1 was released in 2026 with new specifications and an IAM control revision; CCM v4.0.x is being withdrawn (STAR registry becomes v4.1-only December 2027).
2. **CAIQ v4.1 (Consensus Assessments Initiative Questionnaire)**: An operational questionnaire for self-assessment and third-party auditing based on CCM v4.1.
3. **CSA STAR Framework (Security, Trust, Assurance and Risk)**: A cloud assurance and transparency program divided into three maturity levels.
4. **CSA Security Guidance for Critical Areas of Focus in Cloud Computing v5**: The current conceptual guide, adding Zero Trust, GenAI, CI/CD, resilience and telemetry to the 12 critical areas.
5. **CSA Top Threats to Cloud Computing 2026**: Ranks *Inadequate Identity and Access Management* as the number-one threat, with new entries for AI-Enhanced Attacks and AI System Compromise.
6. **CSA Zero Trust Architecture (ZTA)**: Implementation of Zero Trust in software-defined networks (SDP - Software-Defined Perimeter) and cloud-native environments.

---

## 🏛️ CSA Cloud Controls Matrix (CCM v4.1) - The 17 Domains

CCM v4.1 retains the 17 structural domains while adding specifications such as DCS, LOG, SEF, STA and TVM updates:

```
+------------------------------------------------------------------------------------+
| 1. A&A - Audit & Assurance                                                         |
| 2. AIS - Application & Interface Security                                          |
| 3. BCR - Business Continuity Management & Operational Resilience                   |
| 4. CCC - Change Control & Configuration Management                                 |
| 5. CEK - Cryptography, Encryption & Key Management                                 |
| 6. DCS - Data Center Security                                                      |
| 7. DSP - Data Security & Privacy Lifecycle Management                              |
| 8. IAM - Identity & Access Management                                              |
| 9. IVS - Infrastructure & Virtualization Security                                  |
| 10. IPY - Interoperability & Portability                                           |
| 11. HRS - Human Resources Security                                                 |
| 12. LOG - Logging & Monitoring                                                     |
| 13. SEF - Security Incident Management, E-Discovery & Cloud Forensics              |
| 14. STA - Supply Chain Management, Transparency and Accountability                 |
| 15. TVM - Threat & Vulnerability Management                                        |
| 16. UEM - Universal Endpoint Management                                            |
| 17. GRC - Governance, Risk Management & Compliance                                 |
+------------------------------------------------------------------------------------+
```

---

## ⭐ CSA STAR Framework (Security, Trust, Assurance and Risk)

The CSA STAR program validates the security posture of cloud service providers (CSPs) and consumers at 3 levels:

```
+-----------------------------------------------------------------------------------+
| STAR LEVEL 1: Self-Assessment                                                     |
| - Public submission of the CAIQ v4.1 questionnaire or CCM v4.1 compliance to the  |
|   CSA STAR Registry. Mandatory annual refresh.                                     |
+-----------------------------------------------------------------------------------+
                                         |
                                         v
+-----------------------------------------------------------------------------------+
| STAR LEVEL 2: Independent Third-Party Certification (Independent Audit)           |
| - STAR Attestation: Combined assessment of SOC 2 Type II + CCM v4.1.              |
| - STAR Certification: Independent audit combining ISO/IEC 27001 + CCM v4.1.       |
+-----------------------------------------------------------------------------------+
                                         |
                                         v
+-----------------------------------------------------------------------------------+
| STAR LEVEL 3: Continuous Auditing                                                 |
| - Automated validation and real-time telemetry of the cloud security posture      |
|   (aligned with CSPM and continuous monitoring tooling).                          |
+-----------------------------------------------------------------------------------+
```

---

## 🤝 Shared Responsibility Model

When analyzing any cloud architecture under CSA criteria, rigorously delimit who is responsible for which layer:

| Security Layer | IaaS (Infrastructure) | PaaS (Platform) | SaaS (Software) |
| :--- | :--- | :--- | :--- |
| **Governance and Data** | Customer | Customer | Customer |
| **IAM and Access Control** | Customer | Customer | Shared |
| **Application Security** | Customer | Customer | Provider (CSP) |
| **OS / Middleware Security** | Customer | Provider (CSP) | Provider (CSP) |
| **Virtual Network and Firewall** | Shared | Provider (CSP) | Provider (CSP) |
| **Physical Infrastructure and Data Center** | Provider (CSP) | Provider (CSP) | Provider (CSP) |

---

## ⚙️ CSA Decision and Audit Protocol

When asked to design or audit a cloud service or provider:

1. **Request or Complete the CAIQ v4.1 Questionnaire**:
   - For onboarding new SaaS/PaaS/IaaS, require submission of the CAIQ v4.1 to the CSA STAR Registry.
2. **Apply the CEK Domain (Cryptography & Key Management)**:
   - Ensure cloud encryption keys belong to the customer (BYOK - *Bring Your Own Key*, HYOK - *Hold Your Own Key*, or multi-cloud KMS) rather than keys managed solely by the provider.
3. **Map Interoperability and Portability Risks (IPY)**:
   - Assess *Vendor Lock-in* risk and establish data migration and API abstraction strategies.
4. **Implement SDP / CSA Zero Trust (ZTA)**:
   - Replace traditional VPNs with a software-defined perimeter (SDP), creating dynamic micro-perimeters tied to device context and user identity.
5. **Track the CCM v4.1 Transition**:
   - Update control mappings to v4.1 and plan for the December 2027 STAR v4.1-only cutover.

---

## 🔗 Integration with Other Security Skills

- To map CSA CCM v4 controls to ISO/IEC 27017 (Cloud) and ISO/IEC 27018 (Cloud Privacy), see the [iso-27000-series](../../grc/iso-27000-series/SKILL.md) skill.
- To align the CCM CEK (Cryptography) domain with post-quantum algorithms and FIPS/ISO recommendations, see the [cryptography-pqc-standards](../../crypto/cryptography-pqc-standards/SKILL.md) skill.
- To align cloud IAM controls (IAM domain) with AWS, Azure, GCP, and OCI, see the [iam-access-management](../iam-access-management/SKILL.md) skill.
- To map the correspondence of CSA cloud controls with CIS cloud hardening benchmarks, see the [cis-controls](../../grc/cis-controls/SKILL.md) skill.
- For DevSecOps validation and security in cloud deployment pipelines, see the [devsecops-engineer](../../operations/devsecops-engineer/SKILL.md) skill.
