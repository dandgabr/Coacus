---
name: privacy-enhancing-technologies
description: Acts as a Privacy-Enhancing Technologies specialist covering homomorphic encryption, secure multi-party computation, trusted execution environments and confidential computing, federated learning, differential privacy (DP-SGD) and synthetic data, with the trade-offs that determine when each is appropriate.
metadata:
  type: defensive
  phase: weaponize
---

# Privacy-Enhancing Technologies (PETs)

This skill guides the AI to compute over sensitive data without exposing it, selecting the right PET for the threat and the cost budget.

---

## 🧭 1. PET Selection Matrix (a data-sharing discipline, not only cryptography)

| PET | Protects against | Cost | Fit |
| :--- | :--- | :--- | :--- |
| **Differential Privacy (DP-SGD)** | Inference from model outputs/statistics | Small accuracy loss, privacy budget management | Publishing statistics, training models on personal data |
| **Federated Learning** | Centralizing raw data | Communication and orchestration | Training across siloed data |
| **Secure Multi-Party Computation (SMPC)** | Any party seeing others' inputs | High communication | Cross-organization analytics, joint computation |
| **Homomorphic Encryption (FHE)** | The compute host seeing data | Very high | Narrow, high-value encrypted computation |
| **Trusted Execution Environment (TEE)** | The host OS/operator | Hardware trust dependency | Confidential computing in an untrusted cloud |
| **Synthetic Data** | Direct exposure of records | Validation effort | Testing and sharing, with disclosure-risk checks |

---

## 🧮 2. Differential Privacy Essentials

- **(epsilon, delta)-DP** bounds how much a single record can change the output distribution.
- **Laplace mechanism** adds noise calibrated to sensitivity/epsilon; **Gaussian** is common for approximate DP.
- **Composition**: the privacy budget depletes with each query or training step; account for it.
- **DP-SGD**: per-example gradient clipping plus noise for training; combine with federated learning for stronger protection.
- Never claim "anonymous" from de-identified data without validating disclosure risk.

---

## 🛡️ 3. TEE and Confidential Computing

- The computation runs in an attested enclave; the operator cannot read the data.
- Depends on a hardware root of trust; verify **remote attestation** and understand the threat model (side channels, firmware).
- Good for "trusted-but-curious" cloud operators, not for a fully compromised host.

---

## ⚠️ 4. Discipline

- Match the PET to the actual threat; a TEE does not help against a malicious data subject, and DP does not help against a compromised host.
- Measure the utility loss and the performance cost before committing.
- Document the privacy claim precisely; "differentially private" and "encrypted" are different guarantees.

---

## 🔗 5. Integration with Other Skills

- For the privacy governance context, see the [security-privacy](../../grc/security-privacy/SKILL.md) skill.
- For the cryptographic primitives, see the [cryptography-pqc-standards](../../crypto/cryptography-pqc-standards/SKILL.md) skill.
- For AI training privacy, see the [ai-llm-slm-security](../../ai/ai-llm-slm-security/SKILL.md) skill.
- For discovery before applying a PET, see the [data-classification-dspm](../data-classification-dspm/SKILL.md) skill.
