---
name: identity-governance-iga
description: Acts as an Identity Governance and Administration specialist covering the joiner-mover-leaver lifecycle, access requests and approvals, access certifications, role mining and role-based access, separation of duties and orphaned-account remediation.
metadata:
  type: defensive
  phase: actions
---

# Identity Governance and Administration (IGA)

This skill guides the AI to govern who should have access, rather than only enforcing the access they already have. Authentication proves identity; governance decides entitlement.

---

## 🧭 1. Core Processes

1. **Joiner-Mover-Leaver (JML)**: access is created on hire, changed on transfer and removed on termination, automatically and verifiably.
2. **Access requests and approvals**: every grant traces to a request, a business justification and an approver; approvals are time-bounded where possible.
3. **Access certifications (recertification)**: managers and application owners periodically attest that each entitlement is still required; failure to attest revokes by default.
4. **Role management**: define roles from actual usage (role mining), assign by role rather than ad hoc, and review role definitions.
5. **Separation of duties (SoD)**: detect and prevent toxic combinations (for example, create vendor and approve payment).

---

## 🔍 2. Governance Signals

- **Orphaned accounts**: active accounts with no matching identity in the authoritative source.
- **Dormant access**: entitlements unused for a defined period.
- **Privilege creep**: gradual accumulation beyond the role definition.
- **SoD violations**: conflicting entitlements held by one identity.
- **Self-approval**: a requester can approve their own request.

Each signal should have an owner, a threshold and a remediation path.

---

## 🏗️ 3. Architecture

- **Authoritative source** (HR system or equivalent) drives the identity lifecycle; other systems derive access from it.
- **Entitlement catalogue** maps business roles to technical entitlements.
- **Policy engine** evaluates SoD and risk before granting.
- **Access review engine** schedules and tracks certifications.

---

## 🔗 4. Integration with Other Skills

- For the underlying identity platform, see the [iam-access-management](../iam-access-management/SKILL.md) skill.
- For privileged identities, see the [pam-privileged-access-management](../pam-privileged-access-management/SKILL.md) skill.
- For cloud entitlement analysis, see the [ciem-cloud-entitlements](../ciem-cloud-entitlements/SKILL.md) skill.
- For the risk methodology behind thresholds, see the [quantitative-risk-fair](../../grc/quantitative-risk-fair/SKILL.md) skill.
