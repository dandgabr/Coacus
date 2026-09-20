---
name: security-architecture-patterns
description: Acts as a Security Architecture specialist defining reusable reference patterns, trust-boundary engineering, defense-in-depth layering, segmentation patterns, security design review and architecture risk assessment across on-prem and multi-cloud estates.
metadata:
  type: defensive
  phase: recon
---

# Security Architecture Patterns and Design Review

This skill guides the AI to design and review security architecture at the pattern level - the layer between strategic frameworks (SABSA, TOGAF) and code-level standards (ASVS). It supplies reusable patterns and a repeatable design-review method.

---

## 🧱 1. Foundational Design Principles

The Saltzer and Schroeder canon remains the baseline: least privilege, fail-safe defaults, complete mediation, open design, separation of privilege, least common mechanism, psychological acceptability and economy of mechanism. Treat them as the checklist behind any architecture review.

---

## 🔷 2. Reusable Security Patterns

| Pattern | Problem | Structure |
| :--- | :--- | :--- |
| **Trust boundary** | Unknown where trust changes | Explicitly enumerate every place data crosses a trust level and mediate it |
| **Defense in depth** | Single control failure is fatal | Independent, overlapping controls per layer (network, host, app, data) |
| **Policy Decision/Enforcement separation** | Scattered authorization logic | Central decision point with distributed enforcement points (NIST SP 800-207) |
| **Identity-aware proxy** | Direct exposure of services | Broker all access through an authenticating reverse proxy |
| **Gateway offloading** | Repeated security logic per service | Centralize TLS, auth, rate limiting and logging at the gateway |
| **Bulkhead / cell** | Blast radius of a compromise | Partition the estate into isolated cells with independent credentials |
| **Sidecar / service mesh** | Inconsistent service-to-service security | Inject mTLS and policy at the sidecar, not in each service |
| **Secrets broker** | Long-lived static credentials | Issue short-lived, dynamically scoped credentials on demand |
| **Immutable infrastructure** | Configuration drift and patching debt | Replace rather than mutate; rebuild from a known-good image |

---

## ☁️ 3. Reference-Architecture Alignment

- **AWS Well-Architected Security Pillar**: identity and access management, detection, infrastructure protection, data protection, incident response.
- **Azure Well-Architected + Cloud Adoption Framework Secure**: security readiness, confidentiality, integrity, availability, sustainment.
- **Google Cloud security pillar and Enterprise Foundations (BeyondProd)**: security by design, zero trust, shift-left, preemptive defense.
- Map the chosen reference architecture to the enterprise risk model; a reference architecture is an input, not a decision.

---

## 🔍 4. Security Design Review Method

1. **Scope**: what is being built, what is out of scope, and who owns the risk.
2. **Data-flow and trust-boundary diagram**: identify every crossing and every actor.
3. **Threat model**: apply STRIDE/PASTA and map to ATT&CK/D3FEND (see the [threat-modeler](../../operations/threat-modeler/SKILL.md) skill).
4. **Control selection**: for each threat, choose a preventive, detective and recovery control.
5. **Residual risk**: state what remains after controls and who accepts it.
6. **Verification plan**: define how each control will be tested.
7. **Formal verification where warranted**: for policy-heavy systems, model-check the access policy (for example, with TLA+ or UPPAAL-style tools) to prove properties such as "no path reaches the data without approval".

---

## 🔗 5. Integration with Other Skills

- For the strategic SABSA/TOGAF view, see the [security-architect-sabsa](../../operations/security-architect-sabsa/SKILL.md) skill.
- For secure-by-design outcomes, see the [secure-by-design](../../operations/secure-by-design/SKILL.md) skill.
- For C4 and documentation conventions, see the [architecture-documentation](../../../engineering/practices/architecture-documentation/SKILL.md) skill.
- For quantitative risk in the review, see the [quantitative-risk-fair](../../grc/quantitative-risk-fair/SKILL.md) skill.
