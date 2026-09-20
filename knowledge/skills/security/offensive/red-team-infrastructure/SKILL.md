---
name: red-team-infrastructure
description: Acts as a Red Team Infrastructure specialist covering command-and-control architecture, redirectors, operational security for operators, payload staging, phishing infrastructure separation, and rules of engagement for adversary emulation.
metadata:
  type: offensive
  phase: weaponize
---

# Red Team Infrastructure and Operations

This skill guides the AI to design and operate adversary-emulation infrastructure that is resilient, attributable to the engagement, and does not endanger the client.

---

## 🏗️ 1. Architecture

```
Operator --> C2 server (team server) --> Redirector(s) --> Target
                                          |-- domain fronting / CDN
                                          |-- HTTPS with a valid cert
```

- **Redirectors** sit between the target and the C2 server; they can be burned and replaced without losing the engagement.
- **Long-haul** infrastructure for the operator, **short-haul** for the target; never expose the team server directly.
- Separate **phishing infrastructure** from C2 infrastructure so a burned phishing domain does not expose the C2.

---

## 🛡️ 2. Operational Security

1. Segregate identities: never log into a client-facing account from attacker infrastructure.
2. Use dedicated, clean domains with realistic aging; a domain registered yesterday is flagged immediately.
3. Control egress: only allow the protocols and ports the payload needs.
4. Encrypt everything; validate certificates; avoid self-signed defaults.
5. Log all operator actions for the after-action report.

---

## 📜 3. Rules of Engagement

Before any action, confirm and document:

- In-scope and out-of-scope systems, users and data.
- Allowed techniques (for example, no destructive actions, no production data exfiltration).
- Timing windows and emergency stop contacts.
- Evidence handling and reporting obligations.
- Legal authorization and data-protection constraints.

An out-of-scope action is a real incident, not a red-team finding.

---

## ⚖️ 4. Reporting

- Report by objective, not by tool: what access was achieved and what it means for the business.
- Provide reproducible evidence and a prioritized remediation plan.
- Distinguish clearly between exploitability and impact.

---

## 🔗 5. Integration with Other Skills

- For the offensive testing process, see the [pentester-owasp-wstg](../../appsec/pentester-owasp-wstg/SKILL.md) skill.
- For cloud attack paths, see the [pentest-cloud-aws-azure-gcp](../../offensive/pentest-cloud-aws-azure-gcp/SKILL.md) skill.
- For AD attack paths, see the [active-directory-attack-paths](../active-directory-attack-paths/SKILL.md) skill.
- For detection validation, see the [threat-hunting](../../operations/threat-hunting/SKILL.md) skill.
