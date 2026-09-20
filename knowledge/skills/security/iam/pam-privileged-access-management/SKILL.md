---
name: pam-privileged-access-management
description: Acts as a Privileged Access Management specialist covering credential vaulting, session recording and brokering, just-in-time and zero-standing-privilege access, break-glass procedures, cloud PAM and secrets rotation.
metadata:
  type: defensive
  phase: actions
---

# Privileged Access Management (PAM)

This skill guides the AI to design and operate **Privileged Access Management**. PAM governs the accounts that can change the system - root, domain admin, cloud administrator and service accounts - which are the highest-value targets in any environment.

---

## 🧭 1. Core Capabilities

1. **Credential vaulting**: store privileged credentials in a hardened vault, never in code, tickets or shared documents.
2. **Session brokering and recording**: users connect through the PAM proxy rather than directly to the target; record keystrokes, commands and screen for audit.
3. **Just-in-Time (JIT) access**: grant privilege for a bounded window on request and approval, then revoke automatically.
4. **Zero Standing Privilege (ZSP)**: no account holds standing administrative rights; privilege is always elevated on demand.
5. **Credential rotation**: rotate machine and service credentials automatically after each use or on a schedule.

---

## 🏗️ 2. Architecture

```
Requester --> Approval (policy/owner) --> Vault issues ephemeral credential
        --> Session proxy (recorded, command-filtered) --> Target system
        --> Automatic revocation + audit log to SIEM
```

- **Break-glass**: a sealed, monitored emergency path for when the normal flow is unavailable; its use triggers an alert and a mandatory review.
- **Command filtering**: block destructive commands on production (for example, recursive delete) while still allowing legitimate administration.
- **Cloud PAM**: broker cloud role assumption (AWS STS, Azure PIM, GCP IAM) rather than distributing long-lived access keys.

---

## 🛡️ 3. Operating Rules

1. Enumerate and classify every privileged identity, including non-human/service accounts.
2. Require phishing-resistant MFA on every privileged elevation.
3. Separate the vault administrator role from the vault user role; no one should be able to both approve and silently use privilege.
4. Review privileged group membership on a fixed cadence and remove stale entries.
5. Feed PAM session logs into the SIEM and alert on anomalous privileged behavior.

---

## 🔗 4. Integration with Other Skills

- For the identity and access layer, see the [iam-access-management](../iam-access-management/SKILL.md) skill.
- For secret lifecycle mechanics, see the [secrets-management-vault](../secrets-management-vault/SKILL.md) skill.
- For detection of stolen or abused credentials, see the [itdr-identity-threat-detection](../../operations/itdr-identity-threat-detection/SKILL.md) skill.
