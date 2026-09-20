---
name: owasp-top-10-2025
description: Acts as an Application Security specialist applying the OWASP Top 10 2025 edition (8th release). Covers the two new categories (A03 Software Supply Chain Failures and A10 Mishandling of Exceptional Conditions), the re-ranked categories, SSRF merged into A01, and the CWE-to-category mapping used to plan preventive and detective controls.
metadata:
  type: defensive
  phase: recon
---

# OWASP Top 10 2025 (Application Security Risk Ranking)

This skill guides the AI to act as an **Application Security Specialist** using the **OWASP Top 10 2025** as the awareness and prioritization baseline for web application risk. The 2025 edition is the 8th release; it ranks categories by observed incident data and root causes rather than by CVSS score alone, and caps each category at a defined CWE set.

---

## 🧭 1. The 2025 Categories

| ID | Category | Note vs 2021 |
| :--- | :--- | :--- |
| **A01** | Broken Access Control | Remains #1; **SSRF is now folded into A01** |
| **A02** | Security Misconfiguration | Re-ranked up (was #5) |
| **A03** | Software Supply Chain Failures | **New**; expands the former "Vulnerable and Outdated Components" to the whole build and distribution chain |
| **A04** | Cryptographic Failures | Was #2 |
| **A05** | Injection | Was #3 |
| **A06** | Insecure Design | Was #4 |
| **A07** | Authentication Failures | Renamed from Identification and Authentication Failures |
| **A08** | Software and Data Integrity Failures | Unchanged focus |
| **A09** | Security Logging and Alerting Failures | Renamed to emphasize **alerting**, not only logging |
| **A10** | Mishandling of Exceptional Conditions | **New**; fail-open paths, unchecked returns, resource leaks |

---

## ⚙️ 2. How to Apply the Ranking

1. **Map findings to categories and CWEs**, not to vague labels. Each category carries a bounded CWE list; a finding that does not map is either a gap in the taxonomy or a lower-tier issue.
2. **Prioritize by root cause**, not by symptom. A single root cause (for example, absent server-side authorization) can surface as several categories.
3. **Treat A03 and A10 as first-class, not footnotes.** Supply-chain failures now cover the build pipeline, the registry and the distribution channel; exceptional-condition handling covers fail-open logic, partial failures and unbounded resource consumption.
4. **Pair with ASVS for verification depth.** The Top 10 is awareness; the OWASP ASVS is the verifiable control set. See the [appsec-owasp-asvs](../appsec-owasp-asvs/SKILL.md) skill.
5. **Feed the ranking into the secure SDLC** so each category has an owner, a control and a test. See the [secure-sdlc-ssdf](../secure-sdlc-ssdf/SKILL.md) skill.

---

## 🧪 3. Representative CWEs per Category

- **A01**: CWE-22 path traversal, CWE-284 improper access control, CWE-639 authorization bypass via user-controlled key, CWE-918 SSRF.
- **A03**: dependency confusion, typosquatting, compromised build tools, unsigned artifacts.
- **A05**: CWE-89 SQL injection, CWE-79 XSS, CWE-78 OS command injection, CWE-94 code injection.
- **A08**: unsigned updates, insecure deserialization, CI/CD integrity gaps.
- **A10**: unchecked return values, fail-open authorization, unhandled exceptions that leak state.
- **CWE Top 25 2025** leaders include CWE-79 XSS, CWE-89 SQLi, CWE-352 CSRF, CWE-862 Missing Authorization, CWE-787 Out-of-bounds Write and CWE-78 OS Command Injection.

---

## 🔗 4. Integration with Other Skills

- For the detailed injection classes and prototype pollution, see the [web-injection-classes](../web-injection-classes/SKILL.md) skill.
- For API-specific risks, see the [api-protocol-security](../api-protocol-security/SKILL.md) skill and the existing [pentester-owasp-api-security-2023](../pentester-owasp-api-security-2023/SKILL.md) skill.
- For the dependency and build-chain specifics of A03, see the [software-supply-chain-security](../software-supply-chain-security/SKILL.md) skill.
- For logic-driven abuse that is not a memory-safety bug, see the [business-logic-flaws](../business-logic-flaws/SKILL.md) skill.
