---
name: os-hardening-baselines
description: Acts as an OS Hardening specialist covering CIS Benchmarks and DISA STIG baselines for Windows, Linux and macOS, patch management per NIST SP 800-40r4 and CISA KEV, host firewall, disk encryption (BitLocker/LUKS/FileVault), secure boot, TPM and firmware resilience per NIST SP 800-193.
metadata:
  type: defensive
  phase: actions
---

# OS Hardening Baselines

This skill guides the AI to configure and maintain operating systems against recognized baselines, and to keep them patched.

---

## 📋 1. Baseline Selection

- **CIS Benchmarks**: platform-specific and widely adopted; use Level 1 for general servers, Level 2 where risk justifies the operational cost.
- **DISA STIGs**: more prescriptive, common in defense.
- **Vendor security baselines**: useful starting point but not a substitute for a benchmark.
- Adopt one authoritative baseline per platform, then apply documented exceptions with owners.

---

## 🔒 2. Core Hardening Domains

| Domain | Controls |
| :--- | :--- |
| **Boot integrity** | UEFI secure boot, TPM 2.0, measured boot, firmware resiliency (NIST SP 800-193: protect/detect/recover) |
| **Disk encryption** | BitLocker (TPM + PIN for high security), LUKS2, FileVault; escrow recovery keys |
| **Access** | Least-privilege accounts, no shared admin, disable unused accounts, MFA for interactive admin |
| **Network** | Host firewall default-deny, disable unused services and ports, restrict listening interfaces |
| **Auditing** | Enable and centralize logs; protect log integrity |
| **Updates** | Automated patching with a defined SLA; reboot enforcement |

---

## ⏱️ 3. Patch Management (NIST SP 800-40r4)

1. **Identify** assets and their software inventory.
2. **Prioritize** by risk: CISA KEV membership and EPSS, not CVSS alone.
3. **Acquire** updates from trusted sources and verify signatures.
4. **Install** on a defined cadence with emergency handling for critical items.
5. **Verify** the patch actually applied; failed patches are a silent vulnerability.

Firmware and hypervisor updates are in scope, not just the OS packages.

---

## 🔁 4. Continuous Compliance

- Scan against the baseline regularly and treat drift as a defect.
- Automate configuration with the same tooling that scans it, so detection and remediation share a definition.
- Re-baseline when the platform changes; a stale baseline gives false assurance.

---

## 🔗 5. Integration with Other Skills

- For application control, see the [endpoint-application-control](../endpoint-application-control/SKILL.md) skill.
- For Linux kernel protections, see the [linux-kernel-systemd-internals](../../../infrastructure/linux-kernel-systemd-internals/SKILL.md) skill.
- For the EDR layer, see the [edr-evasion-endpoint-security](../edr-evasion-endpoint-security/SKILL.md) skill.
- For macOS specifics, see the [macos-endpoint-security](../macos-endpoint-security/SKILL.md) skill.
