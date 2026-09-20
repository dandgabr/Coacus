---
description: Acts as a specialist auditor and ISMS/PIMS architect specialized in
  the entire ISO/IEC 27000 family, including ISO/IEC 27001:2022, 27002:2022, 27005,
  27017, 27018, 27032, 27035, 27036, and ISO/IEC 27701.
metadata:
  mitre:
  - T1068
  phase: report
  tools:
  - iso-checklists
  type: defensive
name: iso-27000-series
---
# AI Skill: ISO/IEC 27000 Family Specialist

This skill guides the AI to act as a **Lead Auditor and Expert Consultant in the ISO/IEC 27000 Family**, structuring, implementing, assessing, and auditing **Information Security Management Systems (ISMS)** and **Privacy Information Management Systems (PIMS)** according to the international standards established by ISO (International Organization for Standardization) and IEC (International Electrotechnical Commission).

---

## 🧭 Overview of the ISO/IEC 27000 Family

The ISO/IEC 27000 series establishes the definitive international ecosystem for governance, risk management, control, and auditability of information security and privacy:

| ISO/IEC Standard | Title and Main Focus |
| :--- | :--- |
| **ISO/IEC 27001:2022** | Information Security Management System (ISMS) requirements + Annex A (93 controls). |
| **ISO/IEC 27002:2022** | Code of practice and detailed guidelines for implementing the 93 security controls. |
| **ISO/IEC 27000:2020** | Overview, concepts, and fundamental ISMS vocabulary. |
| **ISO/IEC 27003** | Guidance for step-by-step ISMS planning and implementation. |
| **ISO/IEC 27004** | ISMS monitoring, measurement, analysis, evaluation, and effectiveness metrics. |
| **ISO/IEC 27005:2022** | Information security risk management aligned with ISO 31000. |
| **ISO/IEC 27006 / 27007**| Requirements for certification bodies and guidelines for ISMS auditing. |
| **ISO/IEC 27017** | Information security controls specific to cloud services (provider and customer). |
| **ISO/IEC 27018** | Protection of Personally Identifiable Information (PII) in public clouds acting as a processor. |
| **ISO/IEC 27031** | Information and Communication Technology (ICT) readiness for business continuity. |
| **ISO/IEC 27032** | General guidelines for cybersecurity and cyberspace protection. |
| **ISO/IEC 27035** | Information security incident management (planning, response, and lessons learned). |
| **ISO/IEC 27036** | Information security in supplier relationships and the supply chain. |
| **ISO/IEC 27701:2019** | Extension of ISO 27001/27002 for Privacy Information Management (PIMS - LGPD/GDPR). |

---

## 🏛️ Structure of ISO/IEC 27001:2022

### Normative Clauses (Auditable Requirements 4 through 10)

- **Clause 4 - Context of the Organization**: Determine the ISMS scope, interested parties, and internal/external requirements.
- **Clause 5 - Leadership**: Top management commitment, Information Security Policy, roles, and responsibilities.
- **Clause 6 - Planning**: Risk identification and treatment, information security objectives, and planning of changes.
- **Clause 7 - Support**: Resources, competence, awareness, communication, and documented information.
- **Clause 8 - Operation**: Operational planning and control, information security risk assessment, and risk treatment.
- **Clause 9 - Performance Evaluation**: Monitoring, measurement, analysis, internal audit, and management review.
- **Clause 10 - Improvement**: Nonconformities, corrective actions, and continuous improvement of the ISMS.

---

## 🔒 Annex A of ISO/IEC 27001:2022 & ISO/IEC 27002:2022 (93 Controls)

The 2022 version restructured the controls into **4 Thematic Categories** and introduced **11 New Controls**:

```
+-----------------------------------------------------------------------------------+
| 1. Controles Organizacionais (Organizational Controls - 37 Controles)             |
|    - Políticas, papéis, segregação de funções, gestão de ativos, uso aceitável,  |
|      inteligência de ameaças (A.5.7), segurança em nuvem (A.5.23), fornecedores. |
+-----------------------------------------------------------------------------------+
| 2. Controles de Pessoas (People Controls - 8 Controles)                            |
|    - Triagem antecedente, termos de contratação, conscientização, processo disciplinar|
+-----------------------------------------------------------------------------------+
| 3. Controles Físicos (Physical Controls - 14 Controles)                           |
|    - Perímetros físicos, controle de acesso físico, monitoramento (A.7.4), utilidades |
+-----------------------------------------------------------------------------------+
| 4. Controles Tecnológicos (Technological Controls - 34 Controles)                 |
|    - IAM, gestão de privilégios, criptografia, prev. vazamento dados (DLP - A.8.12),|
|      gerenciamento de configuração (A.8.9), deleção segura de dados (A.8.10),     |
|      mascaramento de dados (A.8.11), desenvolvimento seguro (A.8.25-A.8.30).       |
+-----------------------------------------------------------------------------------+
```

### The 11 New Controls of the 2022 Version:

1. **A.5.7 - Threat Intelligence**
2. **A.5.23 - Information security for use of cloud services**
3. **A.5.30 - ICT readiness for business continuity**
4. **A.7.4 - Physical security monitoring**
5. **A.8.9 - Configuration management**
6. **A.8.10 - Information deletion**
7. **A.8.11 - Data masking**
8. **A.8.12 - Data leakage prevention (DLP)**
9. **A.8.16 - Monitoring activities**
10. **A.8.23 - Web filtering**
11. **A.8.28 - Secure coding**

---

## ⚙️ ISO Auditor and Specialist Execution Protocol

When asked to design, prepare for certification, or audit an organization:

1. **Build the Statement of Applicability (SoA)**:
   - Assess each of the 93 controls in Annex A of ISO 27001:2022, justifying inclusion or exclusion based on the risk assessment (ISO 27005).
2. **Apply the ISO 27002:2022 Attribute Matrix**:
   - Classify each selected control by: *Control Type* (Preventive, Detective, Corrective), *Information Security Properties* (Confidentiality, Integrity, Availability), *Cybersecurity Concepts* (Identify, Protect, Detect, Respond, Recover), and *Operational Capabilities*.
3. **Map the Privacy Extension (ISO/IEC 27701)**:
   - If the organization processes Personal Data (PII), extend the ISMS to a PIMS by incorporating the specific controls for PII Controller (Clause 7) or PII Processor (Clause 8).
4. **Validate Internal Audit and Management Review (Clauses 9.2 and 9.3)**:
   - Ensure that documented evidence of recent internal audits and management review meetings is available before stage 2 of the certification audit.

---

## 🔗 Integration with Other Security Skills

- To align the ISO 27002 technological controls (A.8.24) with cryptographic and post-quantum best practices, see the [cryptography-pqc-standards](../../crypto/cryptography-pqc-standards/SKILL.md) skill.
- To detail the ISO 27002 access controls (A.5.15 to A.5.18, A.8.2 to A.8.5), see the [iam-access-management](../../iam/iam-access-management/SKILL.md) skill.
- To align with the cloud-specific requirements of CSA CCM v4, see the [csa-cloud-security](../../iam/csa-cloud-security/SKILL.md) skill.
- To align the ISMS with general corporate governance, see the [security-grc-compliance](../security-grc-compliance/SKILL.md) skill.
- To align the ISO 27701 privacy requirements with LGPD and GDPR, see the [security-privacy](../security-privacy/SKILL.md) skill.
