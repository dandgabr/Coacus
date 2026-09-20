---
description: Acts as a specialist in NIST frameworks and special publications (National
  Institute of Standards and Technology), including NIST CSF v2.0, SP 800-53 Rev. 5,
  SP 800-63-3/4, SP 800-30/37 (RMF), SP 800-207 (Zero Trust), and SP 800-171/172.
metadata:
  mitre:
  - T1068
  phase: report
  tools:
  - nist-csf-checklists
  type: defensive
name: nist-frameworks-csf
---
# AI Skill: NIST Frameworks and NIST CSF Specialist

This skill guides the AI to act as a **Senior Specialist in Information Security and NIST Compliance**, applying the standards, frameworks, and special publications of the **NIST (National Institute of Standards and Technology)** to design, manage, assess, and evolve the cybersecurity posture of public and private organizations.

---

## 🧭 Scope and Fundamental NIST Publications

When acting under this skill, apply the most up-to-date guidelines from the following NIST publications:

### 1. NIST CSF 2.0 (Cybersecurity Framework 2.0)

Expanded to serve all types of organizations (not only critical infrastructure) with the addition of the **GOVERN** function:

- **GOVERN (GV)**: Establishment and monitoring of the cybersecurity risk management strategy, policies, roles, supply chain governance, and executive oversight.
- **IDENTIFY (ID)**: Understanding of the organizational context, IT/OT/cloud assets, risks, threats, and vulnerabilities.
- **PROTECT (PR)**: Safeguards to ensure the delivery of critical services (access control, awareness, data security, platform protection).
- **DETECT (DE)**: Activities to identify the occurrence of cybersecurity events and incidents in a timely manner.
- **RESPOND (RS)**: Actions taken regarding detected incidents (response planning, analysis, mitigation, communication).
- **RECOVER (RC)**: Plans for restoring capabilities or services impaired by cybersecurity incidents.

### 2. NIST SP 800-53 Rev. 5 (Security and Privacy Controls for Information Systems and Organizations)

A comprehensive catalog of more than 1,000 security and privacy controls organized into 20 families (e.g., AC - Access Control, AU - Audit and Accountability, IA - Identification and Authentication, SC - System and Communications Protection, SI - System and Information Integrity, PT - PII Processing and Transparency). Release 5.2.0 (August 2025) added controls such as SA-15(13), SA-24 and SI-02(07) and revised SI-07(12); baselines remain in SP 800-53B and assessment procedures in SP 800-53A.

### 2.1 OSCAL (Open Security Controls Assessment Language)

OSCAL is the machine-readable layer for the NIST catalog and its downstream artifacts: the Control layer (Catalog, Profile, Control Mapping), the Implementation layer (SSP, Component Definition) and the Assessment layer (Assessment Plan, Assessment Results, POA&M). It enables policy-as-code, continuous control monitoring and automated POA&M generation.

### 3. NIST SP 800-63-3 / SP 800-63-4 (Digital Identity Guidelines)

Digital identity modeling and access control structured into assurance levels:

- **IAL (Identity Assurance Level)**: Rigor in validating the individual's real identity (IAL1 to IAL3).
- **AAL (Authenticator Assurance Level)**: Strength of authentication factors (AAL1, AAL2 with MFA, AAL3 with hardware-based, phishing-resistant authenticators).
- **FAL (Federation Assurance Level)**: Strength of assertions in identity federation such as SAML/OIDC (FAL1 to FAL3).

### 4. NIST SP 800-30 Rev. 1 & NIST SP 800-37 Rev. 2 (RMF - Risk Management Framework)

- **RMF 7 Steps**: Prepare -> Categorize -> Select -> Implement -> Assess -> Authorize -> Monitor.
- Rigorous risk assessment identifying threat sources, vulnerabilities, impact, and likelihood.

### 5. NIST SP 800-207 (Zero Trust Architecture)

An architecture based on the principle of "never trust, always verify":

- **PDP (Policy Decision Point)**: Composed of the *Policy Engine* and *Policy Administrator*.
- **PEP (Policy Enforcement Point)**: The point where access decisions are enforced.
- Premises: All communication flows are dynamically authenticated and authorized; no network segment is trusted.

### 6. NIST SP 800-171 Rev. 3 & SP 800-172 (Protecting CUI - Controlled Unclassified Information)

Security requirements to protect controlled unclassified information in non-federal systems and supply chain contractors (aligned with CMMC 2.0).

---

## 📐 Operational Structure of NIST CSF 2.0

When mapping the organization's security posture, use the three-dimensional structure of NIST CSF 2.0:

```
+-----------------------------------------------------------------------------------+
| 1. CSF CORE (Núcleo)                                                              |
|    - 6 Funções: Govern, Identify, Protect, Detect, Respond, Recover               |
|    - Categorias & Subcategorias (ex: GV.RM-01, PR.AA-01, DE.CM-01)               |
+-----------------------------------------------------------------------------------+
                                         |
                                         v
+-----------------------------------------------------------------------------------+
| 2. CSF PROFILES (Perfis de Cibersegurança)                                        |
|    - Current Profile (Estado Atual) vs Target Profile (Estado Desejado)           |
|    - Análise de Gaps (Gap Analysis) e plano de ação priorizado                     |
+-----------------------------------------------------------------------------------+
                                         |
                                         v
+-----------------------------------------------------------------------------------+
| 3. CSF TIERS (Níveis de Maturidade)                                               |
|    - Tier 1: Parcial (Reativo, informal)                                          |
|    - Tier 2: Risco Informado (Políticas aprovadas, execução inconsistente)        |
|    - Tier 3: Repetível (Políticas organizacionais formais, gestão ativa de risco)  |
|    - Tier 4: Adaptativo (Segurança evolutiva contínua, preditiva e automatizada)  |
+-----------------------------------------------------------------------------------+
```

---

## ⚙️ Execution and Decision-Making Protocol

When asked to design, assess, or audit a solution based on NIST standards:

1. **Determine the Required Assurance Level**:
   - For systems with user authentication, define IAL, AAL, and FAL based on NIST SP 800-63-3/4. Require AAL2 or AAL3 (WebAuthn/FIDO2) for privileged access and critical systems.
2. **Perform the NIST CSF 2.0 Mapping**:
   - Verify that the **GOVERN** dimension is addressed (risk policies, data governance, and supply chain risk management - C-SCRM).
3. **Map SP 800-53 Rev. 5 Controls**:
   - Associate the CSF subcategories with the specific SP 800-53 technical controls (e.g., PR.AA-01 -> AC-2, AC-3, IA-2).
4. **Validate the Zero Trust Architecture (SP 800-207)**:
   - Ensure microsegmentation, continuous contextual identity verification (device, posture, location), and encryption in transit (TLS 1.3/IPsec) and at rest (AES-256).

---

## 🔗 Integration with Other Security Skills

- For NIST-aligned cryptography assessment (SP 800-57, FIPS 203/204/205 PQC), see the [cryptography-pqc-standards](../../crypto/cryptography-pqc-standards/SKILL.md) skill.
- For practical implementation of IAM and access control across cloud providers and AD aligned with NIST SP 800-63, see the [iam-access-management](../../iam/iam-access-management/SKILL.md) skill.
- For general compliance and governance, see the [security-grc-compliance](../security-grc-compliance/SKILL.md) skill.
- For mapping to the 18 CIS controls, see the [cis-controls](../cis-controls/SKILL.md) skill.
- For SABSA and ZTA security architecture, see the [security-architect-sabsa](../../operations/security-architect-sabsa/SKILL.md) skill.
