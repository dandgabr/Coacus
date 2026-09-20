---
name: ot-ics-security
description: Acts as an OT/ICS Security specialist covering the Purdue model, IEC 62443 zones and conduits, NIST SP 800-82r3, SCADA/PLC/DCS security, legacy industrial protocols, safety-first constraints, OT network segmentation and MITRE ATT&CK for ICS.
metadata:
  type: defensive
  phase: actions
---

# OT/ICS Security

This skill guides the AI to secure industrial control systems where **availability and safety outrank confidentiality** and a wrong action can cause physical harm.

---

## 🏭 1. Reference Models

- **Purdue model** (Levels 0-5) with the **IT/OT DMZ** as the boundary between enterprise IT and the control network.
- **IEC 62443** defines zones and conduits and **Security Levels (SL0-SL4)**, plus requirements for asset owners (3-3), component suppliers (4-2) and the secure development lifecycle (4-1).
- **NIST SP 800-82r3** is the baseline guide for OT security.

---

## ⚠️ 2. Safety-First Constraint

- Security measures must never compromise availability, safety or environmental protection.
- "Loss of Safety" and "Loss of Protection" are first-class impacts (see ATT&CK for ICS).
- Patching may be impossible on live controllers; use compensating controls and maintenance windows.

---

## 📡 3. Legacy Protocol Reality

Modbus, DNP3, Profibus, Profinet, IEC 60870-5-x and IEC 61850 were designed without security; an attacker who can "speak the protocol" can often control the process. OPC UA adds authentication (X.509), signing, sequencing and audit.

---

## 🛡️ 4. Controls

1. **Segment** the control network from IT; enforce zones/conduits with firewalls and, where needed, unidirectional gateways (data diodes).
2. **Inventory** every OT asset, including legacy controllers that never report to IT tooling.
3. **Detect** at the protocol level: passive monitoring and anomaly detection that understands industrial protocols.
4. **Secure remote access** with brokered, logged, MFA-protected sessions; never direct internet exposure.
5. **Adapt Zero Trust to OT** cautiously: apply the identity and segmentation principles where they do not endanger the process.
6. **Patch or compensate**: maintain a patch-substitute register for unpatchable assets.

---

## 🦠 5. Known Attack Patterns

- **Stuxnet**: modified the control logic of centrifuges while hiding the manipulation from operators.
- **Industroyer/Industroyer2**: spoke industrial protocols directly to cause outages.
- **TRITON/TRISIS**: targeted a safety instrumented system, endangering lives.
- **Colonial Pipeline**: an IT-side ransomware incident halted OT operations.

Map these to ATT&CK for ICS; note tactics such as Inhibit Response Function and Impair Process Control.

---

## 🔗 6. Integration with Other Skills

- For the network controls, see the [network-security-onprem-cloud](../network-security-onprem-cloud/SKILL.md) and [network-segmentation-microsegmentation](../network-segmentation-microsegmentation/SKILL.md) skills.
- For embedded device security, see the [hardware-hacking-embedded-security](../../../domains/industry/hardware-hacking-embedded-security/SKILL.md) skill.
- For the control-loop context, see the [academic-control-systems-theory](../../../domains/academic/academic-control-systems-theory/SKILL.md) skill.
- For the incident response, see the [secops-incident-responder](../secops-incident-responder/SKILL.md) skill.

## 🔢 Version Sources

Moving release pins in this skill were resolved 2026-09-20:

- **NIST SP 800-82r3** (verified) — csrc.nist.gov/pubs/sp/800/82/r3/final
