---
name: mobile-enterprise-mdm
description: Acts as an Enterprise Mobility specialist covering MDM/UEM (Intune, Jamf, Android Enterprise, Apple ADE/DEP/VPP), BYOD vs COPE vs dedicated devices, work profiles, Managed Device Attestation, mobile threat defense and the NIST SP 800-124r2 device lifecycle.
metadata:
  type: defensive
  phase: actions
---

# Mobile Enterprise Management (MDM/UEM)

This skill guides the AI to manage and secure corporate mobile devices and the access they carry.

---

## 🧭 1. Deployment Models

| Model | Ownership | Notes |
| :--- | :--- | :--- |
| **BYOD** | Employee | Work profile/container isolates corporate data |
| **COPE** (corporate-owned, personally enabled) | Employer | Stronger control, personal use permitted |
| **COBO** (corporate-owned, business only) | Employer | Maximum control, no personal use |
| **Dedicated** | Employer | Kiosk or task-specific device |

Choose the model from the data sensitivity and the user population, not from convenience.

---

## 🛠️ 2. Platform Management

- **Android Enterprise**: work profile, fully managed, and dedicated device modes; managed Google Play.
- **Apple**: Automated Device Enrollment (formerly DEP), Volume Purchase Program, Managed Device Attestation.
- Enforce: encryption, screen lock, OS version floor, jailbreak/root detection, and per-app VPN or tunnel.
- Keep an accurate inventory; an unenrolled device with corporate access is the core risk.

---

## 🧱 3. The NIST SP 800-124r2 Lifecycle

1. **Selection and configuration**: choose the platform and baseline it.
2. **Deployment**: enroll, attest and provision only the needed apps and data.
3. **Use**: monitor compliance, patch the OS, manage the app catalogue.
4. **Disposal**: wipe corporately owned devices; remove corporate data from BYOD at offboarding.

---

## 🛡️ 4. Mobile Threat Defense (MTD)

- Deploy MTD for phishing protection, malicious-app detection, network threat detection and device compromise signals.
- Feed MTD signals into conditional access so a compromised device loses access.
- Treat MDM compliance as an access condition, not just an inventory tag.

---

## 🔗 5. Integration with Other Skills

- For mobile app security, see the [appsec-owasp-masvs](../../appsec/appsec-owasp-masvs/SKILL.md) skill.
- For identity and conditional access, see the [iam-access-management](../../iam/iam-access-management/SKILL.md) skill.
- For macOS endpoints, see the [macos-endpoint-security](../../platform/macos-endpoint-security/SKILL.md) skill.
- For mobile malware and forensics, see the [mobile-malware-forensics](../../appsec/mobile-malware-forensics/SKILL.md) skill.
