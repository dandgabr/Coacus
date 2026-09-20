---
name: ai-governance-assurance
description: Acts as an AI Assurance specialist binding MITRE ATLAS, the NIST AI RMF and Generative AI Profile, ISO/IEC 42001/42005/23894/27090 and the EU AI Act risk tiers into an auditable program with model cards, AI BOM, impact assessments and AI incident response.
metadata:
  type: defensive
  phase: report
---

# AI Governance and Assurance (Security)

This skill guides the AI to produce auditable assurance for AI systems, complementing the management-system view in the AI governance skill with the security and adversarial evidence.

---

## 🗺️ 1. Binding the Frameworks

- **MITRE ATLAS**: the adversary TTP knowledge base for AI; map threats and mitigations to it.
- **NIST AI RMF**: Govern, Map, Measure, Manage; the Generative AI Profile adds GenAI risks.
- **ISO/IEC 42001** (AIMS), **42005** (impact assessment), **23894** (AI risk), **27090** (AI security threats).
- **EU AI Act**: risk tiers determine the depth of assessment and documentation.

Use one program, multiple mappings; do not run a separate program per framework.

---

## 📋 2. Assurance Artifacts

- **Model card**: intended use, limitations, evaluation results, known risks.
- **AI BOM**: training data provenance, model lineage, dependencies and their security status.
- **Impact and risk assessment**: per system, with owners and mitigations.
- **Red-team report**: attacks attempted, success rates and residual risk.
- **AI incident response plan**: how an AI failure or misuse is detected, contained and disclosed.

---

## 🔍 3. Evaluation

- Use standardized benchmarks and harm taxonomies for safety and bias.
- Include adversarial and indirect-injection testing, not just benign evaluation.
- Measure over-refusal as well as under-refusal.
- Re-evaluate after every model, prompt or tool change; assurance decays.

---

## 🔗 4. Integration with Other Skills

- For the management-system view, see the [ai-governance-iso-42001](../../grc/ai-governance-iso-42001/SKILL.md) skill.
- For the technical LLM attacks, see the [ai-llm-slm-security](../ai-llm-slm-security/SKILL.md) skill.
- For adversarial ML, see the [ai-adversarial-ml-security](../ai-adversarial-ml-security/SKILL.md) skill.
- For agentic risk, see the [ai-agentic-security](../ai-agentic-security/SKILL.md) skill.
