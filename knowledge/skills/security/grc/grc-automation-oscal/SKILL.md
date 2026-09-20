---
name: grc-automation-oscal
description: Acts as a GRC Automation specialist covering NIST OSCAL models, policy-as-code, continuous control monitoring, machine-readable evidence and the automated generation of SSPs, assessment results and POA&Ms.
metadata:
  type: defensive
  phase: report
---

# GRC Automation and OSCAL

This skill guides the AI to turn compliance from a periodic document exercise into continuous, machine-readable control monitoring.

---

## 🧩 1. OSCAL (Open Security Controls Assessment Language)

OSCAL provides machine-readable models in three layers:

- **Control layer**: Catalog, Profile (a tailored baseline), Control Mapping (how controls relate across frameworks).
- **Implementation layer**: System Security Plan (SSP), Component Definition (reusable control implementations).
- **Assessment layer**: Assessment Plan, Assessment Results, POA&M.

Serializations include XML, JSON and YAML. The value is traceability: a POA&M entry links back to the control it violates, which links to the framework it came from.

---

## ⚙️ 2. Continuous Control Monitoring (CCM)

1. Express each control's assertion as an automated test where possible (configuration query, log check, API call).
2. Collect evidence on a schedule and store it with a timestamp and a hash.
3. Evaluate results and open findings automatically.
4. Route findings to owners with a due date.
5. Re-evaluate; a control that is not measured continuously drifts.

---

## 📜 3. Policy-as-Code

- Encode policy in a language a machine can evaluate (Rego, CEL or a provider policy engine).
- Version, review and test policy like code.
- Apply the same policy in the pipeline (prevention) and in monitoring (detection), so intent and evidence cannot diverge.

---

## ⚠️ 4. Limits

- Automation covers the measurable subset of controls; governance, culture and judgment remain human.
- A passing automated check is evidence of configuration, not proof of effectiveness; pair with periodic human validation.
- Beware false assurance from monitoring a proxy rather than the control itself.

---

## 🔗 5. Integration with Other Skills

- For the NIST catalog and CSF, see the [nist-frameworks-csf](../nist-frameworks-csf/SKILL.md) skill.
- For the general GRC program, see the [security-grc-compliance](../security-grc-compliance/SKILL.md) skill.
- For cloud posture evidence, see the [cloud-security-posture-cnapp](../../cloud/cloud-security-posture-cnapp/SKILL.md) skill.
- For IaC policy enforcement, see the [iac-security-scanning](../../cloud/iac-security-scanning/SKILL.md) skill.
