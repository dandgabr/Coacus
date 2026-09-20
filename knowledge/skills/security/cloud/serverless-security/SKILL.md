---
name: serverless-security
description: Acts as a Serverless Security specialist covering function-level IAM least privilege, event-source injection, dependency and layer risk, secret handling, cold-start and timeout abuse, and the runtime protections available for Lambda, Cloud Functions and Cloud Run.
metadata:
  type: defensive
  phase: actions
---

# Serverless Security

This skill guides the AI to secure function-as-a-service and container-serving platforms, where the unit of deployment is a function and the attack surface is the event, not a port.

---

## 🎯 1. Threat Model

| Threat | Vector | Control |
| :--- | :--- | :--- |
| Over-privileged function | Attached role grants broad access | Per-function least-privilege role |
| Event injection | Malicious payload in an event (S3, SQS, HTTP) | Validate and schema-check every event |
| Dependency risk | Vulnerable package in the bundle or layer | SCA plus SBOM per function |
| Secret exposure | Secrets in environment variables or code | Secret manager plus workload identity |
| Function URL exposure | Public endpoint bypassing the gateway | Authorize at the function or gateway |
| Cost/resource abuse | Infinite recursion or unbounded concurrency | Concurrency limits, reserved capacity, budgets |
| Dependency-layer drift | A shared layer is updated under consumers | Version and pin layers; rebuild consumers |

---

## 🛡️ 2. Rules

1. One function, one purpose, one minimal role. Do not share a "god" role across functions.
2. Validate input at the trust boundary; the event source is untrusted.
3. Keep functions short-lived and stateless; state belongs in managed services.
4. Turn on logging and tracing, and centralize it; ephemeral functions leave little else.
5. Set timeouts and concurrency limits deliberately to bound both denial-of-service and cost.
6. Scan the bundle, not just the repository: the deployed artifact includes transitive code.

---

## 🔗 3. Integration with Other Skills

- For cloud posture, see the [cloud-security-posture-cnapp](../cloud-security-posture-cnapp/SKILL.md) skill.
- For entitlement analysis, see the [ciem-cloud-entitlements](../../iam/ciem-cloud-entitlements/SKILL.md) skill.
- For runtime detection, see the [container-runtime-security](../../operations/container-runtime-security/SKILL.md) skill.
- For the supply chain of the bundle, see the [software-supply-chain-security](../../appsec/software-supply-chain-security/SKILL.md) skill.
