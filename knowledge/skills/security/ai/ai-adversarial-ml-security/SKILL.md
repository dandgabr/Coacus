---
name: ai-adversarial-ml-security
description: Acts as an Adversarial Machine Learning specialist covering evasion (FGSM, PGD, C&W, universal and patch attacks), poisoning and backdoors, model inversion and membership inference, model extraction, and defenses including adversarial training and certified robustness, aligned with the NIST AI 100-2 taxonomy.
metadata:
  type: defensive
  phase: weaponize
---

# Adversarial Machine Learning Security

This skill guides the AI to assess predictive and generative models against adversarial manipulation, beyond the vision-only scope of a single CV skill.

---

## 🧭 1. Attack Taxonomy (NIST AI 100-2)

| Stage | Attack | Goal |
| :--- | :--- | :--- |
| **Training** | Data poisoning, backdoor/trojan | Corrupt the learned behavior |
| **Inference** | Evasion (adversarial examples) | Cause a wrong prediction at test time |
| **Inference** | Model inversion, membership inference | Recover training data or learn if a record was used |
| **Deployment** | Model extraction/stealing | Replicate the model through queries |
| **Supply** | Compromised weights or dependencies | Insert malicious behavior |

---

## 🧪 2. Evasion Techniques

- **FGSM**: a single gradient step in the loss-increasing direction.
- **PGD**: iterative FGSM with projection; the standard strong attack.
- **C&W**: optimization that minimizes perturbation under an Lp norm.
- **Universal perturbations and GCG-style suffixes**: transferable triggers that work across inputs and often across models.
- **Adversarial patches**: physically realizable patterns that fool a camera-based system.

Measure robustness with a strong attack, not a weak one; a defense evaluated only against FGSM is not evaluated.

---

## 🛡️ 3. Defenses

- **Adversarial training** (min-max): train on adversarial examples; effective but costly and can reduce clean accuracy.
- **Certified robustness**: randomized smoothing provides a provable radius, at a cost.
- **Input sanitization and anomaly detection**: raise the cost but are not proofs.
- **Poisoning defenses**: data provenance, deduplication, outlier detection and influence analysis.
- **Privacy defenses**: DP-SGD for membership inference, output limiting for inversion and extraction.
- **Monitoring**: detect query patterns consistent with extraction.

---

## ⚠️ 4. Discipline

- Every defense has an adaptive adversary; re-evaluate after each change.
- Report the attack, the budget and the success rate together.
- A model with no adversarial testing has unknown robustness, not good robustness.

---

## 🔗 5. Integration with Other Skills

- For the vision-specific attack surface, see the [ai-computer-vision-security](../ai-computer-vision-security/SKILL.md) skill.
- For the LLM-specific attacks, see the [ai-llm-slm-security](../ai-llm-slm-security/SKILL.md) skill.
- For training privacy, see the [privacy-enhancing-technologies](../../data/privacy-enhancing-technologies/SKILL.md) skill.
- For evaluation tooling in the OWASP AI Exchange, see the [ai-governance-assurance](../ai-governance-assurance/SKILL.md) skill.
