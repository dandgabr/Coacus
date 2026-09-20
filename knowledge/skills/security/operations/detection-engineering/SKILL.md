---
name: detection-engineering
description: Acts as a Detection Engineering specialist covering detection-as-code, Sigma authoring and conversion, log-source mapping, false-positive tuning, alert triage, ATT&CK coverage measurement and detection validation with Atomic Red Team and MITRE CAR.
metadata:
  type: defensive
  phase: actions
---

# Detection Engineering

This skill guides the AI to build, test and maintain detections as an engineering product, not as a pile of ad-hoc alerts.

---

## 🧭 1. Detection Lifecycle

1. **Identify** the behavior to detect (from threat intel, ATT&CK, an incident, or a hypothesis).
2. **Map** it to a technique and to the log source that can see it.
3. **Author** the rule in a portable format (Sigma) and convert to the target SIEM.
4. **Test** against known-good and known-bad data.
5. **Deploy** with a defined severity and response.
6. **Tune** based on false-positive and false-negative feedback.
7. **Retire** detections that no longer earn their alert volume.

---

## 📝 2. Detection-as-Code

- Keep rules in version control with review, tests and CI conversion.
- Use the `logsource` contract (category/product/service) to declare telemetry dependency.
- Include metadata: ATT&CK mapping, author, date, `falsepositives`, `level`.
- Treat a rule change like a code change: peer review and a regression test.

---

## 🎯 3. Coverage and Validation

- Measure coverage against ATT&CK techniques relevant to the environment, not against the full matrix.
- Validate with **Atomic Red Team** (reproducible technique tests) and **MITRE CAR** analytics.
- Track detection gaps in a register with an owner.
- Purple-team after every major change to confirm the detection still fires.

---

## ⚙️ 4. Operating Metrics

- Alerts per rule, false-positive rate, mean time to triage.
- **Alert-to-incident ratio**: if almost every alert is noise, the program is failing even if coverage looks good.
- Detection latency: how long after the event does the alert appear.

---

## 🔗 5. Integration with Other Skills

- For YARA/Sigma depth, see the [detection-engineering-yara-sigma](../detection-engineering-yara-sigma/SKILL.md) skill.
- For endpoint telemetry, see the [endpoint-detection-engineering](../endpoint-detection-engineering/SKILL.md) skill.
- For SOC operations and triage, see the [soc-operations-maturity](../soc-operations-maturity/SKILL.md) skill.
- For threat-informed priorities, see the [cti-mitre-attack](../../cti/cti-mitre-attack/SKILL.md) skill.
