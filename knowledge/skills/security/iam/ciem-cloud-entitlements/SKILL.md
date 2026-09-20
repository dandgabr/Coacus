---
name: ciem-cloud-entitlements
description: Acts as a Cloud Infrastructure Entitlement Management specialist covering effective-permission and identity-rightsizing analysis, unused-entitlement remediation, cross-account trust analysis and least-privilege enforcement across AWS, Azure, GCP and OCI.
metadata:
  type: defensive
  phase: actions
---

# Cloud Infrastructure Entitlement Management (CIEM)

This skill guides the AI to measure what a cloud identity can *actually* do - the effective permission - and to right-size it toward least privilege.

---

## 🧭 1. Why Effective Permission Differs From Policy

A single identity's access is the union of: attached policies, role assumptions, resource policies, permission boundaries, service-control policies, group memberships and inherited folder/management-group permissions. Reading one policy is not enough; the effective permission is the whole graph.

---

## 🔍 2. CIEM Workflow

1. **Discover** every human and non-human identity across accounts, subscriptions, projects and tenancies.
2. **Compute effective permissions** by resolving the full inheritance and trust graph.
3. **Observe usage** from audit and activity logs to distinguish used from unused entitlements.
4. **Right-size**: remove unused permissions, replace wildcards with explicit actions, and scope resources by tag or path.
5. **Enforce guardrails**: permission boundaries, SCPs and organization policies to prevent re-growth.
6. **Monitor continuously**: entitlement drift is constant; a one-time review decays.

---

## 🚨 3. High-Risk Patterns

- Wildcard actions or resources on a role bound to a workload.
- Cross-account role trust with no external ID or overly broad subject.
- Managed identities with subscription-level contributor rights.
- Unused admin roles retained after a project ends.
- Service accounts with key-based authentication and no rotation.

---

## 🔗 4. Integration with Other Skills

- For cloud IAM specifics, see the provider skills [iam-access-aws](../../iam/iam-access-aws/SKILL.md), [iam-access-azure](../../iam/iam-access-azure/SKILL.md), [iam-access-gcp](../../iam/iam-access-gcp/SKILL.md) and [iam-access-oci](../../iam/iam-access-oci/SKILL.md).
- For posture management that consumes CIEM findings, see the [cloud-security-posture-cnapp](../../cloud/cloud-security-posture-cnapp/SKILL.md) skill.
- For governance signals, see the [identity-governance-iga](../identity-governance-iga/SKILL.md) skill.
