---
name: cloud-security-posture-cnapp
description: Acts as a Cloud Security Posture specialist covering CNAPP decomposition (CSPM, CWPP, KSPM, CIEM, DSPM), attack-path analysis, secure score, multi-cloud onboarding, misconfiguration remediation and continuous posture management.
metadata:
  type: defensive
  phase: recon
---

# Cloud Security Posture and CNAPP

This skill guides the AI to operate a Cloud-Native Application Protection Platform capability: continuous posture assessment across build, deploy and runtime.

---

## 🧭 1. CNAPP Decomposition

```
CNAPP = CSPM (posture/misconfiguration)
      + CWPP (workload protection/runtime)
      + KSPM (Kubernetes security posture)
      + CIEM (cloud entitlement management)
      + DSPM (data security posture)
      + IaC/CI-CD scanning
      + attack-path analysis
```

Name the capability, not the marketing label: the value is in the coverage, not the acronym.

---

## 🔍 2. Posture Management Workflow

1. **Onboard** every account, subscription and project; a cloud account outside the tool is invisible risk.
2. **Benchmark** against CIS Benchmarks and provider security baselines.
3. **Detect** misconfigurations: public storage, overly permissive roles, disabled logging, unencrypted data, exposed management ports.
4. **Rank by attack path**, not by raw severity: a medium finding on a path to sensitive data outranks a high finding that reaches nothing.
5. **Remediate** with infrastructure-as-code changes, not console clicks, so the fix persists.
6. **Prevent recurrence** with policy-as-code at deploy time.

---

## 🚨 3. High-Signal Findings

- Public object storage with sensitive data.
- Workloads with instance-metadata access and excessive IAM permissions (SSRF-to-credential path).
- Disabled audit logging in an account.
- Unencrypted databases or disks with regulated data.
- Management interfaces exposed to the internet.
- Long-lived access keys and unused admin roles.

---

## 🛡️ 4. Runtime (CWPP) and Data (DSPM)

- **CWPP**: detect anomalous process, file and network behavior in workloads; container and serverless runtime protections.
- **DSPM**: discover where sensitive data lives and whether it is reachable; feed the [data-classification-dspm](../../data/data-classification-dspm/SKILL.md) skill.

---

## 🔗 5. Integration with Other Skills

- For entitlement analysis, see the [ciem-cloud-entitlements](../../iam/ciem-cloud-entitlements/SKILL.md) skill.
- For cloud attack paths, see the [pentest-cloud-aws-azure-gcp](../../offensive/pentest-cloud-aws-azure-gcp/SKILL.md) skill.
- For infrastructure-as-code gating, see the [iac-security-scanning](../iac-security-scanning/SKILL.md) skill.
- For detection and response, see the [cloud-detection-response](../cloud-detection-response/SKILL.md) skill.
