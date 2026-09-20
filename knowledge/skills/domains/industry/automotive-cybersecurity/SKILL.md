---
name: automotive-cybersecurity
description: Acts as an Automotive Cybersecurity specialist covering ISO/SAE 21434, UNECE WP.29 R155/R156, TARA (threat analysis and risk assessment), in-vehicle network security (CAN/LIN/FlexRay/Automotive Ethernet), ECU and OTA update security, and the vehicle security operations center.
metadata:
  type: defensive
  phase: report
---

# Automotive Cybersecurity

This skill guides the AI to secure vehicles and the systems that build and update them, where safety and regulation are inseparable from security.

---

## 📜 1. Standards and Regulation

- **ISO/SAE 21434:2021**: cybersecurity engineering across the vehicle lifecycle, from concept to decommissioning; it complements functional-safety **ISO 26262**.
- **UNECE WP.29 R155** (cybersecurity management system) and **R156** (software update management system): the regulatory type-approval obligations in many markets.
- **TARA** (Threat Analysis and Risk Assessment): identify assets, threats, attack paths and impact; assign risk and treatment, analogous to threat modeling with safety impact.

---

## 🚗 2. In-Vehicle Attack Surface

| Bus / Interface | Character |
| :--- | :--- |
| **CAN** | Broadcast, no authentication; the classic attack surface |
| **LIN** | Low-speed body control |
| **FlexRay** | Deterministic, time-triggered |
| **Automotive Ethernet** | High bandwidth; carries SOME/IP and IP stacks |
| **Wireless** | BLE, Wi-Fi, cellular, key fobs, TPMS, GPS |
| **Diagnostic** | OBD-II, UDS over CAN |

Attacks range from message injection and ECU reflashing to relay attacks on passive entry and telematics compromise.

---

## 🔄 3. Secure Update and Lifecycle

- **OTA (over-the-air) updates** must be signed, authenticated and anti-rollback; an update channel is a code-execution channel into a moving vehicle.
- Maintain a component inventory and SBOM per ECU.
- Plan end-of-support for ECUs and the vehicle's crypto-agility (for example, for post-quantum readiness).

---

## 📊 4. Vehicle SOC

- Collect and correlate vehicle telemetry, IDS alerts from in-vehicle monitors, and backend logs.
- Detect anomalies at fleet scale (unusual CAN patterns, unauthorized diagnostic sessions, update anomalies).
- Respond with containment strategies that respect safety (for example, limiting telematics rather than braking).

---

## 🔗 5. Integration with Other Skills

- For the embedded/firmware layer, see the [hardware-hacking-embedded-security](../../../domains/industry/hardware-hacking-embedded-security/SKILL.md) skill.
- For the supply chain of components, see the [software-supply-chain-security](../../../security/appsec/software-supply-chain-security/SKILL.md) skill.
- For cryptography and PQC, see the [cryptography-pqc-standards](../../../security/crypto/cryptography-pqc-standards/SKILL.md) skill.
- For the governance program, see the [iso-27000-series](../../../security/grc/iso-27000-series/SKILL.md) skill.
