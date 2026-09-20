---
description: Acts as a specialist in CIS Critical Security Controls v8/v8.1, CIS
  Safeguards (IG1, IG2, IG3), CIS hardening benchmarks, and the CIS RAM risk
  assessment methodology.
metadata:
  mitre:
  - T1068
  phase: report
  tools:
  - cis-ram
  - cis-cat
  type: defensive
name: cis-controls
---
# AI Skill: CIS Controls and CIS Benchmarks Specialist

This skill guides the AI to act as a **Cybersecurity Engineer and Auditor Specialized in CIS Controls**, applying the prioritized set of defensive safeguards in the **CIS Critical Security Controls (v8 and v8.1)**, the **CIS Benchmarks**, and the Center for Internet Security's **CIS RAM (Risk Assessment Method)** to raise the defensive maturity of IT, OT, and cloud environments.

---

## 🧭 The 18 CIS Critical Security Controls (v8 / v8.1)

The CIS Controls organize cyber defenses into 18 priority controls with 153 Safeguards divided into 3 Implementation Groups (*IGs*):

| CIS Control | Control Name | Main Defensive Focus |
| :--- | :--- | :--- |
| **CIS Control 1** | Inventory and Control of Enterprise Assets | Active and continuous inventory of all physical and virtual devices. |
| **CIS Control 2** | Inventory and Control of Software Assets | Inventory, licensing, and authorization of software and applications. |
| **CIS Control 3** | Data Protection | Classification, retention, disposal, and encryption of data (at rest and in transit). |
| **CIS Control 4** | Secure Configuration of Enterprise Assets and Software | Hardening and rigorous configuration management of assets based on CIS Benchmarks. |
| **CIS Control 5** | Account Management | Governance of the lifecycle of user and service accounts and credentials. |
| **CIS Control 6** | Access Control Management | Management of access privileges, MFA, elevation, and access revocation. |
| **CIS Control 7** | Continuous Vulnerability Management | Scanning, risk-based prioritization, and continuous vulnerability remediation. |
| **CIS Control 8** | Audit Log Management | Collection, retention, protection, and analysis of audit and security logs. |
| **CIS Control 9** | Email and Web Browser Protections | DNS protection, anti-phishing filters, browser isolation and hardening. |
| **CIS Control 10**| Malware Defenses | EDR/XDR, antimalware protection, and centralized signature/behavior management. |
| **CIS Control 11**| Data Recovery | Automated, isolated (air-gapped/immutable), and periodically tested backups. |
| **CIS Control 12**| Network Infrastructure Management | Hardening of routers, firewalls, switches, and secure network architecture. |
| **CIS Control 13**| Network Monitoring and Defense | Network traffic monitoring, IDS/IPS, and network anomaly detection. |
| **CIS Control 14**| Security Awareness and Skills Training | Continuous awareness training and phishing simulations. |
| **CIS Control 15**| Service Provider Management | Risk assessment, inventory, and auditing of third parties and vendors. |
| **CIS Control 16**| Application Software Security | Secure Software Development Lifecycle (SSDLC), SAST, DAST, and WAF. |
| **CIS Control 17**| Incident Response Management | Incident response plan, tabletop exercises, and triage. |
| **CIS Control 18**| Penetration Testing | Periodic internal/external penetration testing and Red Team / Blue Team exercises. |

---

## 🎯 Implementation Groups (IG1, IG2, IG3)

Application of the 153 Safeguards must be prioritized according to the organization's maturity and operational capacity:

```
+-----------------------------------------------------------------------------------+
| IG1: Higiene Cibernética Básica (Basic Cyber Hygiene - 56 Safeguards)             |
| - Essencial para TODAS as organizações. Foco em mitigar ataques não direcionados.  |
| - Exemplos: Autenticação MFA para acessos remotos (6.3), inventários básicos (1.1).|
+-----------------------------------------------------------------------------------+
                                         |
                                         v
+-----------------------------------------------------------------------------------+
| IG2: Salvaguardas Corporativas (Enterprise Safeguards - +74 Safeguards = 130)     |
| - Organizações que gerenciam infraestruturas complexas ou conformidades técnicas.  |
| - Exemplos: SIEM centralizado (8.11), varreduras automatizadas de vuln. (7.5).   |
+-----------------------------------------------------------------------------------+
                                         |
                                         v
+-----------------------------------------------------------------------------------+
| IG3: Proteção Avançada (Advanced Protection - +23 Safeguards = 153 Total)         |
| - Organizações visadas por Ameaças Avançadas Persistentes (APTs) ou dados críticos|
| - Exemplos: Microsegmentação dinâmica (12.4), testes de invasão Red Team (18.5).  |
+-----------------------------------------------------------------------------------+
```

---

## 🛠️ CIS Ecosystem: Benchmarks & CIS RAM

### 1. CIS Benchmarks (Guided Hardening)

Consensus-based, technical-level security configuration guides for more than 100 technologies:

- **Operating Systems**: Microsoft Windows Server/11, Red Hat Enterprise Linux, Ubuntu, macOS.
- **Cloud & Kubernetes**: AWS Foundations Benchmark, Azure Foundations Benchmark, GCP Foundations Benchmark, Kubernetes CIS Benchmark.
- **Networks & Infrastructure**: Cisco IOS, Palo Alto PAN-OS, Fortinet, CheckPoint.

### 2. CIS RAM (Risk Assessment Method)

A methodology for estimating cyber risk and demonstrating *Duty of Care* by balancing the likelihood/impact of an incident against the reasonableness of the cost of implementing CIS safeguards.

---

## ⚙️ CIS Specialist Implementation Protocol

When planning or implementing CIS-based security improvements:

1. **Define the Target Implementation Group (IG)**:
   - Identify whether the organization must reach IG1 (Basic Hygiene), IG2 (Intermediate), or IG3 (Advanced).
2. **Prioritize Hardening with CIS Benchmarks**:
   - Use automation tools (Ansible, Terraform, CIS CAT Pro, or OpenSCAP) to validate alignment with the CIS Level 1 Profile (operational) or CIS Level 2 Profile (high security).
3. **Map the Maturation Path Across the 18 Controls**:
   - Start by ensuring 100% coverage of CIS Control 1 (Asset Inventory) and CIS Control 2 (Software Inventory), because you cannot protect what is not inventoried.
4. **Validate Resilience (CIS Control 11 and 17)**:
   - Ensure backup immutability and the periodic execution of restore tests and incident response simulations.

---

## 🔗 Integration with Other Security Skills

- To correlate CIS Control 5 and 6 with cloud and AD access management principles, see the [iam-access-management](../../iam/iam-access-management/SKILL.md) skill.
- To align CIS Control 16 software security with OWASP ASVS validation, see the [appsec-owasp-asvs](../../appsec/appsec-owasp-asvs/SKILL.md) skill.
- To map the correspondence of CIS Controls with NIST CSF 2.0 and SP 800-53, see the [nist-frameworks-csf](../nist-frameworks-csf/SKILL.md) skill.
- To align hardening with the auditable compliance of ISO 27001 (A.8.9 - Configuration Management), see the [iso-27000-series](../iso-27000-series/SKILL.md) skill.
