---
name: cti-mitre-attack
description: Acts as a CTI specialist for MITRE ATT&CK, covering the matrices, tactics, techniques and sub-techniques, groups, software and campaigns, ATT&CK Navigator layers, behavioral mapping methodology, ATT&CK to D3FEND defensive mapping, and the disciplined attribution of intrusion sets.
metadata:
  type: defensive
  phase: recon
---

# CTI and MITRE ATT&CK Mapping

This skill guides the AI to use **MITRE ATT&CK** as the common language between threat intelligence, detection and defense.

---

## 🧭 1. The ATT&CK Model

- **Matrices** per domain: Enterprise, Mobile, ICS.
- **Tactics** (the adversary's goal) contain **techniques** and **sub-techniques** (the how).
- **Groups**, **Software** and **Campaigns** map observed activity to techniques with public references.
- **ATT&CK as a defensive map**: the newer Detection Strategies, Analytics and Data Components layer makes coverage machine-readable.

Note the evolving tactic model: recent versions add **Stealth** and **Defense Impairment** alongside the legacy Defense Evasion concept, and techniques such as querying public AI services reflect the current threat landscape.

---

## 🗺️ 2. Mapping Methodology

1. Start from observed behavior (telemetry or reporting), not from a tool name.
2. Map to the most specific technique/sub-technique; record the evidence and the confidence.
3. Use Navigator layers to express coverage, gaps and a threat-actor profile.
4. Keep the mapping versioned; ATT&CK evolves and mappings age.
5. Cross-map to **D3FEND** to select defensive countermeasures for each technique.

---

## 🕵️ 3. Attribution Discipline

- Track intrusion sets, campaigns, malware families and infrastructure separately; aliases are not exact equivalence.
- Use victimology and infrastructure pivoting, and express likelihood with calibrated estimative language.
- Avoid naming an actor when the evidence supports only a capability; over-attribution misleads defense.

---

## 🔗 4. Integration with Other Skills

- For the intelligence lifecycle and sharing, see the [cti-threat-intel-lifecycle](../cti-threat-intel-lifecycle/SKILL.md) skill.
- For data exchange formats, see the [cti-platforms-stix-taxii-misp](../cti-platforms-stix-taxii-misp/SKILL.md) skill.
- For detection authoring, see the [detection-engineering](../../operations/detection-engineering/SKILL.md) skill.
- For design-time modeling, see the [threat-modeler](../../operations/threat-modeler/SKILL.md) skill.
