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

## 🧪 4b. Attack and Defense Taxonomy in Practice (Kumar et al.)

**Threat-model axes.** White-box (full knowledge), **gray-box** (partial/query access), **black-box** (no knowledge — the strongest real-world hazard). Attacks classify by stage: **training-time** vs **testing/inference-time** vs **deployment-time**. They threaten **integrity, availability and confidentiality**; adversarial examples are reliability attacks — the model is unmodified but the prediction is wrong.

### Attack families
- **Evasion / decision-time** — perturb the input to flip the prediction (an optimization: find the smallest `σ` maximizing loss). Gradient-based (**FGSM** via `∇ₓ` of the cost, **PGD**, **C&W**, L-BFGS) vs gradient-free/black-box. Two-step crafting: estimate direction sensitivity, then select the perturbation.
- **Poisoning / causal (training-time)** — corrupt the training distribution via **data injection** (adversarial samples preserving labels), **data manipulation** (features/images/labels), or **logic corruption**. Label flipping degrades classifiers (e.g. flipping 40% of SVM labels). **Backdoor/Trojan** triggers grant attacker control.
- **Model inversion** — reconstruct training subjects from confidence scores (MI-Face).
- **Attribute inference** — white- and black-box.
- **Model extraction/stealing** — query a black-box CNN with unlabeled data to build a functionally-equivalent substitute (Knockoff Nets, FEE).
- **Parameter/code modification** — tamper with training libraries or target hardware (fault attacks).

### Domain-specific attacks
- **Malware detection:** IagoDroid (mislabel families), **Stingray** (targeted poisoning), **ATMPA** (adversarial texture; high success and transferability against visualization-based detectors), **AdvAttack** (modify API calls to look benign), **MalGAN** (GAN-generated adversarial samples), SLEIPNIR, byte-sequence injection. Evaluate transferability, spatial invariance, payload size, entropy and functionality retention.
- **Spam/fraud:** denial-of-service on Naive Bayes spam filters (word attacks), crowdturfing-detection evasion/poisoning, keystroke-dynamics spoofing, credit-card-fraud evasion.
- **Intrusion detection:** signature vs anomaly detection, and poisoning/evasion of ML-based IDS.

### Defenses (three families)
1. **Data modification:** **adversarial training** (inject adversarial samples with correct labels — the canonical example cut MNIST misclassification from 89.4% to 17.9%), **gradient masking** (e.g. JPEG compression; too much hurts clean accuracy), data randomization/expansion, denoising autoencoders.
2. **Model modification:** regularization, **defensive distillation** (smoother output surface, lower transferability), **feature squeezing** (reduce color depth / smooth), deep contractive networks, **Parseval networks** (Lipschitz-constant regularization).
3. **Auxiliary tools:** adversarial-input detection, and attribution/explainability (layer-wise relevance propagation) for accountability. For privacy, note that anonymization is insufficient — model outputs and test results can leak.

### Offensive AI and GenAI abuse
**AI-enabled phishing** (language imitation from social media), **AI malware/ransomware**, **deepfakes** (voice/video forgery and identity bypass — e.g. the €220k UK voice-fraud case), poisoning-as-a-service, and GAN-based content generation. Offensive capability areas: prediction, generation, analysis (asset mining), retrieval, and decision-making (swarm botnets, heuristic attack graphs). Keep the distinction between *attacks using AI* and *attacks against AI* (adversarial ML).

The full taxonomy is reported as presented in *Attacks on Artificial Intelligence* (2026); pin any external standard before citing it as current.

---

## 🔗 5. Integration with Other Skills

- For the vision-specific attack surface, see the [ai-computer-vision-security](../ai-computer-vision-security/SKILL.md) skill.
- For the practical XAI tooling used in defenses and audits, see the [explainable-ai](../../../domains/industry/explainable-ai/SKILL.md) skill.
- For the LLM-specific attacks, see the [ai-llm-slm-security](../ai-llm-slm-security/SKILL.md) skill.
- For training privacy, see the [privacy-enhancing-technologies](../../data/privacy-enhancing-technologies/SKILL.md) skill.
- For evaluation tooling in the OWASP AI Exchange, see the [ai-governance-assurance](../ai-governance-assurance/SKILL.md) skill.
