---
name: soc2-trust-services
description: Acts as a SOC 2 specialist covering the AICPA Trust Services Criteria (Security, Availability, Processing Integrity, Confidentiality, Privacy), Type I vs Type II engagements, evidence and control design, and the common pitfalls of a rushed SOC 2 program.
metadata:
  type: defensive
  phase: report
---

# SOC 2 Trust Services Criteria

This skill guides the AI to prepare for and operate a **SOC 2** report, the customer-facing assurance vehicle for service organizations.

---

## 🧭 1. The Trust Services Criteria

| Criterion | Focus |
| :--- | :--- |
| **Security (Common Criteria)** | Protection against unauthorized access; required in every SOC 2 |
| **Availability** | The system is available for operation and use as committed |
| **Processing Integrity** | Processing is complete, valid, accurate, timely and authorized |
| **Confidentiality** | Information designated confidential is protected |
| **Privacy** | Personal information is collected, used, retained and disclosed per commitments |

Security is mandatory; the other four are in scope only when relevant to the service.

---

## 📅 2. Type I vs Type II

- **Type I**: design of controls at a point in time (does the control exist?).
- **Type II**: operating effectiveness over a period (did the control work throughout?).
- Customers increasingly require Type II; the observation period drives the workload.

---

## 🛠️ 3. Preparing

1. Define the system boundary and the services in scope.
2. Map controls to the criteria, including the **complementary user entity controls** you rely on the customer to perform.
3. Select an auditor early; a late start compresses the observation window.
4. Produce evidence continuously, not in a scramble: access reviews, change tickets, incident records, monitoring dashboards.
5. Fix gaps before the auditor finds them.

---

## ⚠️ 4. Common Pitfalls

- Treating SOC 2 as a checkbox: a report full of exceptions is worse than no report.
- Ignoring the observation period evidence discipline.
- Assuming a "fast and easy" engagement is credible; the AICPA has publicly warned against unlicensed or rushed engagements.
- Confusing SOC 2 with SOC 1 (financial controls), SOC for Cybersecurity or SOC for Supply Chain, which are distinct reports.

---

## 🔗 5. Integration with Other Skills

- For the general GRC program, see the [security-grc-compliance](../security-grc-compliance/SKILL.md) skill.
- For cloud assurance overlap, see the [csa-cloud-security](../../iam/csa-cloud-security/SKILL.md) skill.
- For audit evidence discipline, see the [iso-27000-series](../iso-27000-series/SKILL.md) skill.
- For third-party assurance of subservice providers, see the [third-party-risk-management](../third-party-risk-management/SKILL.md) skill.
