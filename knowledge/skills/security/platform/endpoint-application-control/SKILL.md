---
name: endpoint-application-control
description: Acts as an Application Control specialist covering App Control for Business (formerly WDAC), AppLocker, Smart App Control, code-signing trust, Constrained Language Mode and attack-surface-reduction rules on Windows endpoints.
metadata:
  type: defensive
  phase: actions
---

# Endpoint Application Control

This skill guides the AI to allow only trusted code to execute on an endpoint - the single most effective control against unapproved binaries, including many ransomware and toolkits.

---

## 🧭 1. Mechanisms

- **App Control for Business** (formerly WDAC): signature, hash and reputation based; covers executables, DLLs, MSI and scripts, and can force PowerShell into Constrained Language Mode. The recommended modern mechanism.
- **AppLocker**: the legacy sibling; still useful where WDAC is unavailable.
- **Smart App Control**: consumer-oriented, cloud-reputation based; starts in evaluation and disables itself on managed devices. Not an enterprise control.
- Application control **complements** antivirus and EDR; it does not replace them.

---

## 🏗️ 2. Deployment Approach

1. **Inventory** the applications and publishers genuinely required.
2. **Audit mode first**: measure what would be blocked before enforcing.
3. **Build a base policy** from trusted signers plus a managed installer, then add explicit path rules only where unavoidable.
4. **Enforce**, and monitor blocked events.
5. **Manage change**: an application-control policy that is not maintained becomes either useless (too permissive) or an outage (too strict).

---

## ⚠️ 3. Common Pitfalls

- Over-reliance on path rules (easily bypassed by writing to the allowed path).
- Forgetting script hosts (PowerShell, WSH, mshta) and signed script policies.
- Ignoring vulnerable-driver blocklists, which application control alone does not cover.
- Deploying enforcement without an audit period, causing mass breakage.

---

## 🔗 4. Integration with Other Skills

- For the EDR and evasion context, see the [edr-evasion-endpoint-security](../edr-evasion-endpoint-security/SKILL.md) skill.
- For OS baselines, see the [os-hardening-baselines](../os-hardening-baselines/SKILL.md) skill.
- For Windows internals and code integrity, see the [windows-internals-security](../windows-internals-security/SKILL.md) skill.
