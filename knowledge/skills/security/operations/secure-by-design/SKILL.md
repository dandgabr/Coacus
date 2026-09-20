---
name: secure-by-design
description: Acts as a Secure-by-Design specialist applying CISA Secure by Design outcomes and NIST SP 800-160 systems security engineering. Covers executive ownership, secure defaults, memory-safe roadmaps, elimination of vulnerability classes, and design gates that make the safe path the default.
metadata:
  type: defensive
  phase: recon
---

# Secure by Design

This skill guides the AI to shift security from after-the-fact remediation to design-time engineering, following **CISA Secure by Design** and **NIST SP 800-160 (Engineering Trustworthy Secure Systems)**.

---

## 🧭 1. CISA Secure by Design Outcomes

1. **Take ownership of customer security outcomes**: the manufacturer, not the customer, is accountable for the security posture of the product.
2. **Embrace radical transparency and accountability**: publish vulnerability handling, advisories and provenance.
3. **Build organizational structure and leadership to achieve these goals**: a named executive owner with authority and budget.

Practices that follow: ship **secure defaults** (MFA, SSO and logging on by default, at no extra cost), eliminate whole vulnerability classes rather than individual bugs, and publish secure-by-design roadmaps.

---

## 🛠️ 2. Eliminate Vulnerability Classes

Rather than fix instances, remove the class:

| Class | Structural fix |
| :--- | :--- |
| SQL injection | Parameterized queries as the only query API |
| XSS | Auto-escaping templates plus a strict CSP, with no unsafe HTML sink |
| OS command injection | No shell API in the product surface |
| Memory-safety bugs | Migrate to a memory-safe language where feasible; a published roadmap otherwise |
| Path traversal | Canonicalize and confine every file access to a root |

---

## 🏗️ 3. Design Gates

- **Threat-model before implementation**; no design is approved without a data-flow diagram and abuse cases.
- **Security requirements are testable**: each has an acceptance criterion.
- **Default-deny at every boundary**: the failure mode of a missing rule is "deny".
- **Least privilege by construction**: components get the minimum identity and permissions they need to function.

---

## 📚 4. Systems Security Engineering (NIST SP 800-160)

SP 800-160 Vol. 1 frames security as a lifecycle engineering discipline (requirements, architecture, design, verification and validation, assurance). Vol. 2 adds **cyber resiliency**: anticipate, withstand, recover and adapt. Apply both so a compromise degrades gracefully rather than failing catastrophically.

---

## 🔗 5. Integration with Other Skills

- For the architecture patterns that implement these outcomes, see the [security-architecture-patterns](../security-architecture-patterns/SKILL.md) skill.
- For the lifecycle gates, see the [secure-sdlc-ssdf](../../appsec/secure-sdlc-ssdf/SKILL.md) skill.
- For threat modeling methods, see the [threat-modeler](../threat-modeler/SKILL.md) skill.
