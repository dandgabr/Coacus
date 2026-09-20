---
name: macos-endpoint-security
description: Acts as a macOS Endpoint Security specialist covering Secure Enclave, FileVault and Data Protection classes, SIP and the Signed System Volume, Gatekeeper and notarization, TCC, the Endpoint Security framework and MDM profiles.
metadata:
  type: defensive
  phase: actions
---

# macOS Endpoint Security

This skill guides the AI to secure macOS endpoints using the platform's own layered model.

---

## 🍏 1. Platform Protections

| Control | Purpose |
| :--- | :--- |
| **Secure Enclave** | Hardware key storage and attestation |
| **FileVault + Data Protection classes** | Full-disk and per-file encryption keyed to the user's state |
| **SIP (System Integrity Protection)** | Prevents modification of protected system paths |
| **Signed System Volume** | Cryptographically seals the OS volume |
| **Gatekeeper + notarization** | Blocks unsigned/known-malicious apps |
| **TCC** | Per-app privacy permissions (camera, microphone, disk, screen) |
| **Managed Device Attestation** | Proves device identity and integrity to the MDM |

---

## 🔭 2. Telemetry

- The **Endpoint Security** framework is the only supported kernel-adjacent telemetry path; it emits auth and notify events for process execution, mounts, signals, TCC changes and XPC connections.
- Enroll through **MDM** (for example, Intune or Jamf) to enforce configuration, FileVault, firewall, and to apply a bootstrap token so security agents receive full disk access.

---

## 🛡️ 3. Hardening Rules

1. Enforce FileVault and escrow recovery keys.
2. Enable the application firewall and stealth mode; consider a host-based firewall for egress control.
3. Restrict TCC grants; review which apps hold screen-recording and accessibility rights.
4. Block execution of unsigned or unnotarized binaries.
5. Keep macOS updated; security responses (rapid security responses) should be allowed to install automatically.
6. Harden the MDM enrollment: an unenrolled Mac is an unmanaged Mac.

---

## 🔗 4. Integration with Other Skills

- For baselines, see the [os-hardening-baselines](../os-hardening-baselines/SKILL.md) skill.
- For mobile/device management, see the [mobile-enterprise-mdm](../../operations/mobile-enterprise-mdm/SKILL.md) skill.
- For macOS malware analysis, see the [malware-analysis-multios](../../appsec/malware-analysis-multios/SKILL.md) skill.
- For endpoint detection, see the [endpoint-detection-engineering](../../operations/endpoint-detection-engineering/SKILL.md) skill.
