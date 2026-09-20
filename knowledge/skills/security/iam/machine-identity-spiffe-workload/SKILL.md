---
name: machine-identity-spiffe-workload
description: Acts as a Machine Identity specialist covering SPIFFE/SPIRE workload identity, SVIDs, workload identity federation, the IETF WIMSE architecture, non-human identity lifecycle governance, and the replacement of static service credentials with short-lived attested identities.
metadata:
  type: defensive
  phase: actions
---

# Machine Identity and Workload Identity (SPIFFE/SPIRE, WIMSE)

This skill guides the AI to give every workload a verifiable identity and to retire static, long-lived service credentials.

---

## 🪪 1. SPIFFE/SPIRE Fundamentals

- **SPIFFE ID**: a URI identifying a workload, scoped to a trust domain.
- **SVID**: the short-lived credential that proves the identity - X.509, JWT, or WIT-SVID.
- **Trust domain and bundle**: the federation boundary and its set of trusted roots.
- **Workload API / Broker API**: how a workload obtains and rotates its SVID without a static secret.
- **Federation**: SPIFFE-to-SPIFFE and OIDC federation let trust domains interoperate without shared keys.

---

## 🌐 2. Workload Identity Federation in the Cloud

Replace cloud access keys with federated workload identity:

- **AWS**: IAM Roles for Service Accounts, EKS Pod Identity, Roles Anywhere.
- **Azure**: Workload Identity federation for managed identities.
- **GCP**: Workload Identity Federation.
- **CI/CD**: OIDC federation from the pipeline to the cloud, with the subject claim pinned to the repository and branch/environment.

Pin the trust policy narrowly: a wildcard subject allows any workflow in the organization to assume the role.

---

## 📐 3. IETF WIMSE

The **Workload Identity in Multi-System Environments** working group defines an architecture and a JOSE-based workload token for chained HTTP/REST calls, local token issuance and token exchange (RFC 8693). Use WIMSE concepts when a request crosses multiple trust boundaries and the original caller's identity must be preserved.

---

## 🔄 4. Non-Human Identity (NHI) Governance

1. Inventory every non-human identity: service accounts, API keys, bot tokens, certificates and workload identities.
2. Classify by blast radius and data access.
3. Enforce short lifetimes and automatic rotation.
4. Detect orphaned identities and remove them.
5. Monitor for anomaly (new source, unusual destination, sudden volume).

---

## 🔗 5. Integration with Other Skills

- For the broader IAM program, see the [iam-access-management](../iam-access-management/SKILL.md) skill.
- For the Zero Trust architecture that consumes these identities, see the [zero-trust-architecture-engineering](../../../infrastructure/zero-trust-architecture-engineering/SKILL.md) skill.
- For certificate lifecycle, see the [crypto-pki-certificate-lifecycle](../../crypto/crypto-pki-certificate-lifecycle/SKILL.md) skill.
- For cloud federation specifics, see the [cloud-workload-identity-federation](../../cloud/cloud-workload-identity-federation/SKILL.md) skill.
