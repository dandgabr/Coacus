---
description: Acts as a specialist in cloud architecture and auditing based on the
  Cloud Security Alliance (CSA), including the Cloud Controls Matrix (CCM v4), CAIQ
  v4, STAR Framework (Levels 1, 2, and 3), CSA Security Guidance v4, and cloud Zero Trust.
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

1. **CSA Cloud Controls Matrix (CCM v4 / v4.0.10)**: A cybersecurity control matrix created specifically for cloud architectures.
2. **CAIQ v4 (Consensus Assessments Initiative Questionnaire)**: An operational questionnaire for self-assessment and third-party auditing based on CCM v4.
3. **CSA STAR Framework (Security, Trust, Assurance and Risk)**: A cloud assurance and transparency program divided into three maturity levels.
4. **CSA Security Guidance for Critical Areas of Focus in Cloud Computing v4**: A conceptual guide covering the 14 critical areas of cloud computing.
5. **CSA Zero Trust Architecture (ZTA)**: Implementation of Zero Trust in software-defined networks (SDP - Software-Defined Perimeter) and cloud-native environments.

---

## 🏛️ CSA Cloud Controls Matrix (CCM v4) - The 17 Domains

CCM v4 is composed of **197 control objectives** distributed across **17 structural domains**:

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
| STAR LEVEL 1: Autoavaliação (Self-Assessment)                                     |
| - Envio público do questionário CAIQ v4 ou submissão de conformidade CCM v4 ao    |
|   STAR Registry da CSA. Atualização anual obrigatória.                             |
+-----------------------------------------------------------------------------------+
                                         |
                                         v
+-----------------------------------------------------------------------------------+
| STAR LEVEL 2: Certificação por Terceiros Independentes (Independent Audit)        |
| - STAR Attestation: Avaliação combinada SOC 2 Type II + CCM v4.                   |
| - STAR Certification: Auditoria independente combinando ISO/IEC 27001 + CCM v4.   |
+-----------------------------------------------------------------------------------+
                                         |
                                         v
+-----------------------------------------------------------------------------------+
| STAR LEVEL 3: Auditoria Contínua (Continuous Auditing)                            |
| - Validação e telemetria automatizada em tempo real da postura de segurança dos   |
|   controles da nuvem (alinhado a ferramentas CSPM e CMM - Continuous Monitoring). |
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

1. **Request or Complete the CAIQ v4 Questionnaire**:
   - For onboarding new SaaS/PaaS/IaaS, require submission of the CAIQ v4 to the CSA STAR Registry for validation of the 197 controls.
2. **Apply the CEK Domain (Cryptography & Key Management)**:
   - Ensure cloud encryption keys belong to the customer (BYOK - *Bring Your Own Key* or HYOK - *Hold Your Own Key*) rather than keys managed solely by the provider.
3. **Map Interoperability and Portability Risks (IPY)**:
   - Assess *Vendor Lock-in* risk and establish data migration and API abstraction strategies.
4. **Implement SDP / CSA Zero Trust (ZTA)**:
   - Replace traditional VPNs with a software-defined perimeter (SDP), creating dynamic micro-perimeters tied to device context and user identity.

---

## 🔗 Integration with Other Security Skills

- To map CSA CCM v4 controls to ISO/IEC 27017 (Cloud) and ISO/IEC 27018 (Cloud Privacy), see the [iso-27000-series](../../grc/iso-27000-series/SKILL.md) skill.
- To align the CCM CEK (Cryptography) domain with post-quantum algorithms and FIPS/ISO recommendations, see the [cryptography-pqc-standards](../../crypto/cryptography-pqc-standards/SKILL.md) skill.
- To align cloud IAM controls (IAM domain) with AWS, Azure, GCP, and OCI, see the [iam-access-management](../iam-access-management/SKILL.md) skill.
- To map the correspondence of CSA cloud controls with CIS cloud hardening benchmarks, see the [cis-controls](../../grc/cis-controls/SKILL.md) skill.
- For DevSecOps validation and security in cloud deployment pipelines, see the [devsecops-engineer](../../operations/devsecops-engineer/SKILL.md) skill.
