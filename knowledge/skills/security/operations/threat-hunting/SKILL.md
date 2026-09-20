---
name: threat-hunting
description: Acts as a Threat Hunting specialist applying hypothesis-driven hunts, the PEAK and TaHiTI methodologies, ATT&CK-based hunting, structured analytic techniques, and the feedback loop that turns hunts into detections.
metadata:
  type: defensive
  phase: actions
---

# Threat Hunting

This skill guides the AI to proactively find adversaries that automated detection has missed, using hypotheses rather than alerts.

---

## 🧭 1. Hunt Methodologies

- **PEAK** (Prepare, Execute, Act with Knowledge): frame the hunt around a hypothesis and measurable data.
- **TaHiTI**: a structured, iterative hunt process with clear scoping and documentation.
- **ATT&CK-driven hunting**: pick techniques relevant to your threat model and environment, then look for their evidence in telemetry.
- **Intelligence-driven hunting**: start from a reported campaign and hunt its TTPs in your estate.

Both PEAK and TaHiTI are named methodologies; treat their detailed steps as guidance rather than a rigid standard.

---

## 🎯 2. The Hunt Loop

1. **Hypothesis**: "If an adversary did X here, we would see Y in data source Z."
2. **Data**: confirm the telemetry exists and is reliable before hunting.
3. **Query and analyze**: search, pivot, and correlate across sources.
4. **Findings**: classify as detection gap, control gap, or benign - and document each.
5. **Detect**: convert validated hunting queries into detections.
6. **Feed back**: update the threat model and the detection backlog.

---

## 🧰 3. Useful Data Sources

Endpoint process and memory telemetry, authentication and identity logs, network flows and DNS, cloud audit logs, email and web proxy logs, and SaaS audit trails.

---

## ⚠️ 4. Discipline

- A hunt without a hypothesis is a fishing expedition; state what would falsify it.
- Document negative results; "we looked and found nothing" is a finding.
- Use structured analytic techniques to avoid confirmation bias.
- Do not run hunts that could disrupt production without a plan.

---

## 🔗 5. Integration with Other Skills

- For detection authoring, see the [detection-engineering](../detection-engineering/SKILL.md) skill.
- For adversary behavior mapping, see the [cti-mitre-attack](../../cti/cti-mitre-attack/SKILL.md) skill.
- For SOC operations, see the [soc-operations-maturity](../soc-operations-maturity/SKILL.md) skill.
- For the adversary model, see the [threat-modeler](../threat-modeler/SKILL.md) skill.
