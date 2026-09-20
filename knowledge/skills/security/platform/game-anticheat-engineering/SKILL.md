---
name: game-anticheat-engineering
description: Acts as an Anti-Cheat Engineering specialist covering server-side detection, client-side anti-tamper, kernel-driver anti-cheat, hardware-assisted TEE/protected VMs, telemetry and ML-based detection, ban policy, HWID/reputation and the privacy and legal debate around ring-0 anti-cheat.
metadata:
  type: defensive
  phase: actions
---

# Game Anti-Cheat Engineering

This skill guides the AI to design and operate anti-cheat as a discipline, distinct from the engine-hardening view in the game engine security skill.

---

## 🧭 1. Defense Taxonomy

1. **Server-side detection**: non-intrusive and configuration-independent, but limited by the data the server sees; false positives on skilled players are the main risk.
2. **Client-side anti-tamper**: obfuscation, integrity checks, pack encryption; raise the cost but are bypassable.
3. **Kernel-driver anti-cheat**: high visibility and detection, but carry privacy, stability and rootkit-like-behavior concerns.
4. **Hardware-assisted (TEE/protected VM)**: strong isolation, higher performance cost; a promising privacy-friendly direction.
5. **Emerging**: consensus/voting schemes and proactive adversarial-texture defenses against visual aimbots.

---

## 📊 2. Detection

- **Telemetry and behavioral**: aim trajectories, reaction time, movement entropy, utility usage, view-angle statistics.
- **ML models**: transformer and LSTM detectors on server-side features; explainability matters for bans.
- **False-positive rate is the product metric**: in competitive play, a detector with lower accuracy but a far lower false-positive rate is often preferable.
- **Human-in-the-loop**: review and player reports before permanent sanctions.

---

## 🧾 3. Policy and Enforcement

- Define a **ban policy**: what constitutes a violation, the evidence standard, the sanction ladder, and the appeal path.
- **HWID and reputation systems**: persistent identity across accounts, with the legal and support implications of false positives.
- **Transparency**: publish detection philosophy and enforcement statistics; secrecy alone does not deter.

---

## ⚖️ 4. Privacy and Legal Posture

- Kernel-mode anti-cheat faces legal and ethical scrutiny; two of four studied kernel anti-cheats exhibited rootkit-like behavior.
- Privacy-first architectures (protected VMs, consensus schemes) are viable alternatives that avoid unverifiable ring-0 code.
- Document data collection, retention and user consent; gaming platforms are increasingly regulated.

---

## 🔗 5. Integration with Other Skills

- For engine-level protections, see the [game-engine-security](../game-engine-security/SKILL.md) skill.
- For the primary systemic defense, see the [game-network-authority-security](../game-network-authority-security/SKILL.md) skill.
- For the economic layer, see the [game-economy-fraud-security](../game-economy-fraud-security/SKILL.md) skill.
- For the detection lifecycle, see the [detection-engineering](../../operations/detection-engineering/SKILL.md) skill.
