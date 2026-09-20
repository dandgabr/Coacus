---
name: itdr-identity-threat-detection
description: Acts as an Identity Threat Detection and Response specialist covering token theft, adversary-in-the-middle phishing, credential stuffing, session hijacking, impossible travel, MFA fatigue and the detection of abnormal identity behavior across identity providers and clouds.
metadata:
  type: defensive
  phase: actions
---

# Identity Threat Detection and Response (ITDR)

This skill guides the AI to detect and respond to attacks that target identity itself, since the modern intrusion usually begins with a credential rather than a vulnerability.

---

## 🎯 1. Attack Classes to Detect

| Attack | Signal |
| :--- | :--- |
| **Credential stuffing** | Many failed logins across many accounts from distributed sources |
| **Password spraying** | Few attempts per account across many accounts |
| **AiTM phishing** | Successful login followed by a new session token from a different device or ASN |
| **Token theft and replay** | A valid token used from two geographies or device fingerprints |
| **Session hijacking** | Cookie reused after logout or with a changed user agent |
| **Impossible travel** | Consecutive logins from physically impossible locations |
| **MFA fatigue** | Repeated push prompts followed by an approval |
| **Consent phishing** | A new OAuth application granted broad scopes |

---

## 🛡️ 2. Detection Signals to Instrument

- Successful authentication metadata: device, ASN, client, conditional-access outcome.
- Token issuance, refresh and revocation events.
- OAuth application consent and scope grants.
- Privileged role activation and directory changes.
- Password and MFA reset events.

Correlate identity events with endpoint and network telemetry; a login is only suspicious in context.

---

## 🚑 3. Response Actions

1. Revoke sessions and refresh tokens for the affected identity.
2. Force credential and MFA re-registration.
3. Invalidate OAuth consents granted during the incident window.
4. Hunt for persistence (new MFA methods, mail rules, app passwords, service principals).
5. Eradicate and then review the conditional-access policy that allowed it.

---

## 🔗 4. Integration with Other Skills

- For the identity platform and federation, see the [iam-access-management](../../iam/iam-access-management/SKILL.md) skill.
- For the authentication protocols, see the [auth-protocols-mfa](../../operations/auth-protocols-mfa/SKILL.md) skill.
- For the broader incident process, see the [secops-incident-responder](../../operations/secops-incident-responder/SKILL.md) skill.
- For detection authoring, see the [detection-engineering](../../operations/detection-engineering/SKILL.md) skill.
