---
name: security-technical-opinion
description: >-
  Provides a guide and procedure for autonomously drafting Information Security Technical Opinions,
  architecture risk assessments, integrations, and third parties (TPRM). Supports dynamic
  selection of Threat Modeling methodologies (STRIDE, PASTA, LINDDUN, VAST, DREAD),
  control auditing based on OWASP ASVS (V1 to V17), normative severity classification
  P0 to P3 (SLAs of 7d, 30d, and 30-180d), and structuring the action plan into 3 time waves.
---

# Skill: Information Security Technical Opinion and Architecture Risk Assessment

This skill instructs the autonomous agent to execute rigorous, standardized technical assessments of information security, software architecture, integrations, and vendor/third-party risks (TPRM), producing formal technical opinions.

---

## 🎯 Skill Objectives

1. **Dynamic Threat Modeling:** Select and apply the Threat Modeling methodology best suited to the solution context (**STRIDE, PASTA, LINDDUN, VAST, or DREAD**).
2. **Structured Auditing via OWASP ASVS:** Classify and audit critical points and requirements across the **OWASP ASVS** chapters and rigor levels (**L1, L2, L3**), according to the detailed controls of the [appsec-owasp-asvs](../../appsec/appsec-owasp-asvs/SKILL.md) skill.
3. **Normative Classification and SLAs (P0 to P3):** Map risks to the corporate standard:
   - **🔴 P0 (Critical):** Mandatory SLA of **up to 7 days** (*Go-Live Blocker*).
   - **🟠 P1 (High):** Mandatory SLA of **up to 30 days** (*Priority Action*).
   - **🟡 P2 (Medium) / 🟢 P3 (Low):** Handled through **Formal Risk Acceptance** and a roadmap of **30 to 180 days**.
4. **Remediation Roadmap in 3 Time Waves:**
   - **Wave 1 (Up to 7 days / Pre-Go-Live):** Mitigation of 100% of P0 blockers.
   - **Wave 2 (Up to 30 days / Priority Post-Go-Live):** Mitigation of P1 items and operational controls.
   - **Wave 3 (30 to 180 days / Risk Acceptances and Resilience):** Handling of P2 and P3 items, automation, and continuous improvement.
5. **Non-Negotiable Security Gating:** Establish objective criteria for releasing traffic to production.

---

## 🧭 Step-by-Step Execution Workflow

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        FLUXO DE EXECUÇÃO DO PARECER TÉCNICO                            │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ 1. INGESTÃO & EVIDÊNCIAS ──► Validação de topologias, APIs, DPA, TPRM e Pentests       │
│                                                                                        │
│ 2. SELEÇÃO METODOLÓGICA ──► Escolha justificada: STRIDE / PASTA / LINDDUN / VAST / ... │
│                                                                                        │
│ 3. MAPA ASVS & DFD      ──► Mapeamento de Zonas (Trust Boundaries) e Capítulos V1-V17  │
│                                                                                        │
│ 4. MODELAGEM & MATRIZ   ──► Cálculo de Severidade (5x5) e Enquadramento P0 a P3        │
│                                                                                        │
│ 5. GATING & 3 ONDAS     ──► Definição de Bloqueadores (7d) e Roadmap (7d / 30d / 180d) │
│                                                                                        │
│ 6. VEREDITO & EMISSÃO   ──► Geração do parecer em conformidade com o template padrão   │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

### **Step 1: Evidence Collection and Validation**

- **Architecture and Flow Diagrams:** Validate the presence of ports, protocols, and network boundaries.
- **Pentest Reports:** Check whether they were issued in the last 12 months and whether vulnerabilities were addressed.
- **Certifications:** Validate independent reports (ISO 27001, SOC 2 Type II, PCI-DSS).
- **Contracts and DPA:** Check for the formal existence of a data protection addendum (LGPD) with audit and incident notification clauses.
- *Golden Rule:* The absence of documentary evidence of a critical control must be recorded as a **Formal Risk**.

### **Step 2: 5x5 Risk Matrix and Normative Classification (P0 to P3)**

$$\text{Severidade} = \text{Probabilidade (1 a 5)} \times \text{Impacto (1 a 5)}$$

| Matrix Score | Normative Level | Severity | Mandatory SLA | Handling and Governance |
| :---: | :---: | :---: | :---: | :--- |
| **20 to 25** | 🔴 **P0** | **Critical** | **Up to 7 days** | **Go-Live Blocker (*Hard Blocker*).** Production entry prohibited without prior fix. |
| **12 to 19** | 🟠 **P1** | **High** | **Up to 30 days** | **Priority Action.** Mitigation plan approved and executed in Wave 2. |
| **6 to 11** | 🟡 **P2** | **Medium** | **Risk Acceptance (30-180d)** | Tolerable risk in the short term; mitigation in Wave 3 or formal acceptance. |
| **1 to 5** | 🟢 **P3** | **Low** | **Risk Acceptance (30-180d)** | Acceptable residual risk; handled through continuous monitoring. |

### **Step 3: Security Gating and Structuring the 3 Waves**

1. **Go-Live Blockers (Wave 1 - Up to 7 days / Pre-Go-Live):**
   - Identified P0 flaws.
   - Critical violations mandated by ASVS L1/L2 without a compensating control.
   - Cleartext traffic containing credentials or sensitive personal data.
   - Cleartext credentials with administrative privileges.
   - Absence of a contractual data protection instrument (DPA/LGPD).

2. **Wave 2 (Up to 30 days / Priority Post-Go-Live):**
   - Mitigation of P1 items, SIEM/SOC integration, port hardening, and focused pentest.

3. **Wave 3 (30 to 180 days / Risk Acceptances and Resilience):**
   - Mitigation of P2 and P3, automation, redundancy (HA), mTLS, and periodic auditing.

### **Step 4: Final Verdict**

- **`APPROVED WITHOUT RESERVATIONS`:** Only if all risks are P3 and all applicable ASVS requirements are met.
- **`APPROVED WITH CONDITIONS`:** When P0 or P1 risks exist that are formally converted into Go-Live Blockers (Wave 1 - up to 7 days).
- **`REJECTED / BLOCKED`:** Structural P0 risks with no viable control within 7 days, or refusal to meet security requirements.

---

## 🔗 Integration with Other Skills

- [security-architect-sabsa](../security-architect-sabsa/SKILL.md): provides the business drivers, the Business Attribute Profile (BAP), and the trust zones that underpin the opinion.
- [threat-modeler](../threat-modeler/SKILL.md): produces the threats and DFDs that feed the detailed risk analysis.
- [appsec-owasp-asvs](../../appsec/appsec-owasp-asvs/SKILL.md): provides the verifiable technical controls of each ASVS domain.
- [security-privacy](../../grc/security-privacy/SKILL.md): validates LGPD/GDPR compliance, DPIA/RIPD, and DPA clauses.
- [security-grc-compliance](../../grc/security-grc-compliance/SKILL.md): defines policies, risk appetite, and organizational SLAs.

> For the formal, mandatory structure of the sections, see [`references/parecer_tecnico_guidelines.md`](./references/parecer_tecnico_guidelines.md). For a completed example, see [`examples/parecer_tecnico_sample.md`](./examples/parecer_tecnico_sample.md).
