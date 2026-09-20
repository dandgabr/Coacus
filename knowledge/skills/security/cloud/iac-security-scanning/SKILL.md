---
name: iac-security-scanning
description: Acts as an Infrastructure-as-Code Security specialist covering policy-as-code scanning of Terraform, CloudFormation, ARM/Bicep, Kubernetes manifests and Dockerfiles, drift detection, and CI gating with Checkov/KICS/tfsec-style tooling.
metadata:
  type: defensive
  phase: recon
---

# Infrastructure-as-Code Security Scanning

This skill guides the AI to catch insecure infrastructure before it is deployed, at the point where a fix is a code change rather than an incident.

---

## 🧭 1. What to Scan

- **Terraform** and OpenTofu plans and modules.
- **CloudFormation**, **ARM/Bicep** templates.
- **Kubernetes** manifests, Helm charts and Kustomize overlays.
- **Dockerfiles** and container build definitions.
- **Serverless** definitions (IAM roles, event sources, environment configuration).

---

## 🛠️ 2. Scanning Model

1. **Static policy checks** against a benchmark or custom policy (CIS, provider baselines, organizational rules).
2. **Graph-based checks** for issues that span resources (a public bucket plus a policy that allows read).
3. **Plan-time checks** against the rendered plan so dynamic values are evaluated.
4. **Drift detection** to find resources changed outside the pipeline.

---

## 🚦 3. CI Gating

- Fail the pipeline on new critical/high findings; allow an explicit, time-bounded exception with a justification.
- Scan on pull request (diff-only) and on merge (full).
- Suppress with policy, never with an inline "ignore" that outlives its reason.
- Treat the scanner as a floor, not a ceiling: it cannot see intent.

---

## 🔗 4. Integration with Other Skills

- For cloud posture management, see the [cloud-security-posture-cnapp](../cloud-security-posture-cnapp/SKILL.md) skill.
- For Kubernetes hardening, see the [kubernetes-security-posture](../../operations/kubernetes-security-posture/SKILL.md) skill.
- For pipeline security, see the [devsecops-engineer](../../operations/devsecops-engineer/SKILL.md) skill.
- For supply-chain integrity of the pipeline itself, see the [software-supply-chain-security](../../appsec/software-supply-chain-security/SKILL.md) skill.
