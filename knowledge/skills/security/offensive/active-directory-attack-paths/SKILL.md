---
name: active-directory-attack-paths
description: Acts as an Active Directory attack-path specialist covering Kerberoasting, AS-REP roasting, DCSync, delegation abuse, ADCS misconfiguration (ESC1-ESC8), ACL-based escalation and lateral movement, mapped to MITRE ATT&CK and mitigations.
metadata:
  type: offensive
  phase: exploitation
---

# Active Directory Attack Paths

This skill guides the AI to analyze and remediate the attack paths that let an initial foothold become domain dominance.

---

## 🎯 1. Credential-Based Escalation

- **Kerberoasting**: request service tickets for accounts with SPNs and crack them offline. Mitigation: strong service-account passwords, managed service accounts, AES-only encryption.
- **AS-REP roasting**: request an AS-REP for accounts without Kerberos pre-authentication, then crack. Mitigation: require pre-authentication.
- **Password spraying**: a few guesses across many accounts to avoid lockout. Mitigation: lockout policy plus monitoring for distributed failures.

---

## 🔗 2. Delegation Abuse

- **Unconstrained delegation**: a host can impersonate any user who authenticates to it; protect privileged accounts from authenticating to such hosts.
- **Constrained and resource-based constrained delegation**: abuses the ability to impersonate users to specific services; monitor changes to delegation attributes.

---

## 🎫 3. Certificate Services (ADCS)

- Misconfigured templates allow a low-privileged user to request a certificate that authenticates as a privileged account (the ESC1-ESC8 family).
- Audit template permissions, enrollment rights and the CA's web interfaces; restrict who can enroll and which templates are published.

---

## 🧭 4. ACL and Graph Abuse

- **DCSync**: an account with replication rights can pull password hashes from the domain controller; restrict `DS-Replication-Get-Changes` rights.
- **ACL-based escalation**: write permissions on objects (for example, `GenericAll` on a user or group) enable takeover; enumerate effective rights.
- Build and review the **attack graph** (paths from owned principals to Tier-0 assets) and cut the shortest paths first.

---

## 🛡️ 5. Mitigation Priorities

1. Tier the admin model: Tier 0 assets must never be administered from lower tiers.
2. Remove standing privilege; use just-in-time elevation (see the PAM skill).
3. Harden the domain controller: restrict replication, protect the krbtgt account, deploy Credential Guard/LSA protection.
4. Monitor for the signals: unusual service-ticket requests, DCSync, delegation changes, ADCS enrollment anomalies.
5. Rotate krbtgt twice after any suspected domain compromise.

---

## 🔗 6. Integration with Other Skills

- For privileged access, see the [pam-privileged-access-management](../../iam/pam-privileged-access-management/SKILL.md) skill.
- For Windows internals, see the [windows-internals-security](../../platform/windows-internals-security/SKILL.md) skill.
- For detection, see the [detection-engineering](../../operations/detection-engineering/SKILL.md) skill.
- For identity threat detection, see the [itdr-identity-threat-detection](../../operations/itdr-identity-threat-detection/SKILL.md) skill.
