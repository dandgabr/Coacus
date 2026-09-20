---
name: cloud-secrets-management
description: Acts as a Cloud Secrets Management specialist covering provider secret stores (AWS Secrets Manager, Azure Key Vault, GCP Secret Manager, OCI Vault), External Secrets Operator, dynamic database credentials, automatic rotation and the elimination of static keys from workloads.
metadata:
  type: defensive
  phase: actions
---

# Cloud Secrets Management

This skill guides the AI to manage secrets natively in the cloud and to replace static cloud credentials with federated, short-lived ones.

---

## 🗄️ 1. Provider Secret Stores

| Provider | Service | Notes |
| :--- | :--- | :--- |
| AWS | Secrets Manager / SSM Parameter Store | Native rotation for RDS; encryption with KMS |
| Azure | Key Vault | HSM-backed option; managed identities for access |
| GCP | Secret Manager | IAM-scoped; regional replicas |
| OCI | Vault | Software and HSM-backed keys |

Access to the store must itself be authorized by workload identity, not by a secret.

---

## 🔄 2. Rotation and Dynamic Credentials

- Rotate automatically on a schedule and on suspicion; a rotation that has never been rehearsed will fail in an incident.
- Prefer **dynamic credentials**: a secrets engine that issues a database credential per consumer with a short TTL, so there is no long-lived secret to steal.
- For databases, rotate the credential and update the consumer atomically, with overlap to avoid downtime.

---

## ☸️ 3. Kubernetes Patterns

- **External Secrets Operator** syncs a cloud secret into a Kubernetes Secret, keeping a single source of truth.
- Prefer **CSI secret stores** or **workload identity** so the secret is never persisted in etcd.
- Enable encryption at rest for etcd and restrict who can read Secrets.

---

## 🛡️ 4. Rules

1. No secret in an environment file, image layer, pipeline log or repository.
2. Every secret has an owner, a rotation policy and an expiry.
3. Scanning for committed secrets is a build gate, and any hit triggers rotation, not just deletion from history.
4. Prefer eliminating the secret (federation) over protecting it.

---

## 🔗 5. Integration with Other Skills

- For the general secrets lifecycle, see the [secrets-management-vault](../../iam/secrets-management-vault/SKILL.md) skill.
- For cloud identity federation, see the [cloud-workload-identity-federation](../cloud-workload-identity-federation/SKILL.md) skill.
- For key hierarchy and KMS, see the [crypto-kms-hsm-key-management](../../crypto/crypto-kms-hsm-key-management/SKILL.md) skill.
