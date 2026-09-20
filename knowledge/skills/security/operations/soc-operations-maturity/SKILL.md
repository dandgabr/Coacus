---
name: soc-operations-maturity
description: Acts as a SOC Operations and Maturity specialist covering tiering models, SOC-CMM assessment, SIEM/SOAR operations, MSSP considerations, analyst workflows and the metrics that measure a security operations center.
metadata:
  type: defensive
  phase: actions
---

# SOC Operations and Maturity

This skill guides the AI to run and improve a Security Operations Center as a managed service with measurable outcomes.

---

## 🏢 1. Operating Model

- **Tier 1**: triage and known-incident handling; fast, repetitive, scripted.
- **Tier 2**: investigation and response for non-trivial incidents.
- **Tier 3**: hunting, detection engineering and tooling.
- **Fusion/IR**: incident command and coordination for major events.
- Keep escalation criteria explicit so Tier 1 does not sit on a serious incident.

---

## 📊 2. Metrics

- **MTTD** (mean time to detect), **MTTA** (acknowledge), **MTTR** (respond/resolve).
- **False-positive rate** and **alert-to-incident ratio**.
- Automation rate: the share of alerts closed without human touch.
- Coverage: ATT&CK techniques with a validated detection.
- Measure trends, not absolute numbers; a single month is noise.

---

## 🧰 3. Tooling

- **SIEM** for correlation and retention; normalization (for example, a common schema) is what makes correlation possible.
- **SOAR** for orchestration: enrich, contain, notify, and document automatically where the decision is deterministic.
- Case management for incidents, with a searchable history.
- Keep the tooling boundary honest: a SOAR playbook should contain, not adjudicate.

---

## 📈 4. Maturity (SOC-CMM)

Assess across business, people, process, technology and services dimensions; plan improvements against the weakest relevant dimension rather than the most visible tool. SOC-CMM is the de-facto assessment instrument.

---

## 🔗 5. Integration with Other Skills

- For the incident process, see the [secops-incident-responder](../secops-incident-responder/SKILL.md) skill.
- For detections, see the [detection-engineering](../detection-engineering/SKILL.md) skill.
- For proactive work, see the [threat-hunting](../threat-hunting/SKILL.md) skill.
- For intelligence inputs, see the [cti-threat-intel-lifecycle](../../cti/cti-threat-intel-lifecycle/SKILL.md) skill.
