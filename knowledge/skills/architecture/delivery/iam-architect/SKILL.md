---
name: iam-architect
description: >-
  Acts as the Identity and Access Architect owning identity lifecycle,
  authentication and authorization, federation, privileged access and identity
  governance across applications and clouds. Use when designing IAM/CIAM
  architecture, defining identity lifecycle and access governance, or
  standardizing identity across systems and clouds.
tags:
  - architecture
  - iam-architecture
  - security-architecture
---

# Skill: Identity and Access Architect

The Identity and Access Architect owns the **identity domain** as a security
specialization: how identities are created, authenticated, authorized, federated,
governed and revoked. Identity is the primary control plane of a zero-trust
posture, so this role coordinates tightly with the security architect.

---

## 1. When This Skill Applies

- Designing IAM/CIAM architecture (SSO, MFA, federation).
- Defining identity lifecycle and access-governance models.
- Owning privileged access and zero-standing-privilege design.
- Standardizing identity across applications and clouds.
- Designing workload and machine identity.

Does NOT apply to: the enterprise security frame and threat model (use
[security-architect-sabsa](../../../security/operations/security-architect-sabsa/SKILL.md)),
or identity operations and administration (use the IAM operations skills).

---

## 2. The Identity Control Plane

| Concern | Decision |
|---|---|
| Human identity | Lifecycle, authentication, MFA, federation |
| Customer identity | CIAM, consent, scale, privacy |
| Privileged access | Vaulting, JIT access, session control |
| Workload identity | Service identities, federation, short-lived credentials |
| Governance | Access certification, SoD, orphaned accounts |
| Protocol | OIDC, OAuth 2.x, SAML, SCIM, WebAuthn |

---

## 3. Method

1. **Baseline** the identity sources, protocols and access paths.
2. **Target** the identity architecture: authoritative sources, federation,
   privileged access and workload identity.
3. **Design** lifecycle and governance (joiner, mover, leaver; certification;
   separation of duties).
4. **Standardize** protocols and token handling across applications and clouds.
5. **Eliminate** standing credentials in favor of short-lived, federated ones.

---

## 4. Orchestration and Handoffs

| Concern | Owning skill |
|---|---|
| Enterprise security frame and threat model | [security-architect-sabsa](../../../security/operations/security-architect-sabsa/SKILL.md) |
| Enterprise frame | [enterprise-architect](../../enterprise/enterprise-architect/SKILL.md) |
| Zero-trust architecture | [zero-trust-architecture-engineering](../../../infrastructure/zero-trust-architecture-engineering/SKILL.md) |
| Authentication protocols and MFA | [auth-protocols-mfa](../../../security/operations/auth-protocols-mfa/SKILL.md) |
| Identity governance and administration | [identity-governance-iga](../../../security/iam/identity-governance-iga/SKILL.md) |
| Privileged access management | [pam-privileged-access-management](../../../security/iam/pam-privileged-access-management/SKILL.md) |
| Machine identity (SPIFFE/workload) | [machine-identity-spiffe-workload](../../../security/iam/machine-identity-spiffe-workload/SKILL.md) |
| Cloud workload identity federation | [cloud-workload-identity-federation](../../../security/cloud/cloud-workload-identity-federation/SKILL.md) |
| Cloud IAM specifics | [iam-access-aws](../../../security/iam/iam-access-aws/SKILL.md), [iam-access-azure](../../../security/iam/iam-access-azure/SKILL.md), [iam-access-gcp](../../../security/iam/iam-access-gcp/SKILL.md), [iam-access-oci](../../../security/iam/iam-access-oci/SKILL.md) |

---

## 5. Reference Frameworks

- **NIST Digital Identity Guidelines** — the identity assurance baseline
  (resolve the revision before citing).
- **OIDC / OAuth 2.x / SAML 2.0 / SCIM** — the protocol specifications.
- **WebAuthn / FIDO2** — phishing-resistant authentication.
- **Zero-trust architecture guidance** — for the control-plane placement.

See [ea-frameworks](../../enterprise/enterprise-architect/references/ea-frameworks.md).

---

## 6. Common Mistakes

| Mistake | Correction |
|---|---|
| Treating identity as an operational concern only | It is the zero-trust control plane |
| Standing privileged credentials | Prefer just-in-time, vaulted access |
| Long-lived static workload keys | Federate short-lived workload identity |
| No access certification | Governance requires periodic certification |
| Protocol sprawl | Standardize on a governed protocol set |
