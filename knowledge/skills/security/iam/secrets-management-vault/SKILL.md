---
name: secrets-management-vault
description: Acts as a Secrets Management specialist covering secrets engines, dynamic credentials, secret-zero bootstrapping, rotation, KMS/HSM integration, and the elimination of static credentials from code, configuration and pipelines.
metadata:
  type: defensive
  phase: actions
---

# Secrets Management and Vaulting

This skill guides the AI to remove static secrets from applications and pipelines and replace them with a managed, auditable secrets lifecycle.

---

## 🧭 1. Secret Types and Stores

| Secret | Recommended store |
| :--- | :--- |
| Human credentials | Identity provider with phishing-resistant MFA |
| Application secrets | Central secrets manager with dynamic issuance |
| Cloud credentials | Cloud KMS/secret manager plus workload identity federation |
| Encryption keys | KMS/HSM; never export root keys |
| CI/CD credentials | OIDC federation to short-lived tokens |

---

## ⚙️ 2. Lifecycle

1. **Generate**: cryptographically strong, unique per environment and per consumer.
2. **Distribute**: over an authenticated channel at runtime; never bake into an image or repository.
3. **Use**: least privilege and short TTL; prefer **dynamic credentials** issued per request over long-lived ones.
4. **Rotate**: automatic rotation with overlap to avoid outages; rotation is a routine event, not an incident.
5. **Revoke**: immediate revocation on suspicion; verify revocation actually propagates to every cache.
6. **Audit**: log every read and every policy change.

---

## 🔐 3. Secret-Zero and Bootstrapping

The hardest problem is the first credential. Solutions: cloud workload identity (IID/IRSA/WIF), platform attestation, or a trusted orchestrator that injects the bootstrap secret into the workload at start. Never solve secret-zero with a hardcoded key.

---

## 🛡️ 4. Anti-Patterns to Eliminate

- Secrets in environment files committed to version control, or in container image layers.
- Shared secrets across environments or teams.
- Secrets in logs, error messages or analytics.
- Long-lived cloud access keys on developer machines or CI runners.
- Secret scanning treated as advisory rather than a build gate.

---

## 🔗 5. Integration with Other Skills

- For the privileged-account layer, see the [pam-privileged-access-management](../pam-privileged-access-management/SKILL.md) skill.
- For cryptographic key hierarchy, see the [crypto-kms-hsm-key-management](../../crypto/crypto-kms-hsm-key-management/SKILL.md) skill.
- For cloud-specific secret stores, see the [cloud-secrets-management](../../cloud/cloud-secrets-management/SKILL.md) skill.
