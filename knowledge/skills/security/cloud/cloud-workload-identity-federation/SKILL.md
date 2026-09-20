---
name: cloud-workload-identity-federation
description: Acts as a Cloud Workload Identity specialist covering IAM Roles for Service Accounts, Azure Workload Identity, GCP Workload Identity Federation, CI/CD OIDC federation, and the replacement of static cloud access keys with short-lived federated credentials.
metadata:
  type: defensive
  phase: actions
---

# Cloud Workload Identity Federation

This skill guides the AI to eliminate static cloud credentials by giving each workload a federated, short-lived identity.

---

## 🌐 1. Federation Patterns

- **Kubernetes to AWS**: IAM Roles for Service Accounts (IRSA) or EKS Pod Identity.
- **Kubernetes to Azure**: Microsoft Entra Workload Identity.
- **Kubernetes to GCP**: Workload Identity Federation for GKE.
- **CI/CD to any cloud**: OIDC federation where the pipeline presents a signed token and the cloud trusts it for a short window.
- **Cross-cloud**: trust a workload identity from one provider in another via OIDC, without importing keys.

---

## 🔒 2. Trust Policy Narrowing

The trust policy is the security boundary. Pin it tightly:

- Restrict the subject to the exact repository, branch and environment (not `repo:org/*`).
- Restrict the audience to the intended service.
- Restrict the conditions (environment, workflow) rather than allowing any workflow in the organization.
- Note that providers increasingly use immutable subject claims; verify your trust conditions against the current claim format.

A wildcard subject is equivalent to publishing the credentials.

---

## 🛡️ 3. Operating Rules

1. No long-lived cloud access keys on workloads, developer machines or CI runners.
2. Workload identity is scoped per service, not shared across the namespace.
3. Monitor token issuance for anomalies (new subject, unusual audience).
4. Rotate root/break-glass credentials on a schedule and keep them sealed.

---

## 🔗 4. Integration with Other Skills

- For machine identity concepts, see the [machine-identity-spiffe-workload](../../iam/machine-identity-spiffe-workload/SKILL.md) skill.
- For cloud secret stores, see the [cloud-secrets-management](../cloud-secrets-management/SKILL.md) skill.
- For entitlements, see the [ciem-cloud-entitlements](../../iam/ciem-cloud-entitlements/SKILL.md) skill.
- For pipeline hardening, see the [devsecops-engineer](../../operations/devsecops-engineer/SKILL.md) skill.
