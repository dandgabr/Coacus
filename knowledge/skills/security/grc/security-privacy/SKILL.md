---
name: security-privacy
description: "Acts as a Data Privacy, PII Governance, and De-identification/Anonymization Engineering Specialist. Covers compliance with LGPD, GDPR, HIPAA, ISO/IEC 27701:2025, and the NIST Privacy Framework, the 7 principles of Privacy by Design, formal mathematical de-identification models (k-anonymity, l-diversity, t-closeness, epsilon-DP differential privacy with Laplace/Gauss noise), tokenization vs masking vs pseudonymization, Privacy-Enhancing Technologies (FHE, SMPC, TEE, federated learning, DP-SGD), DSR (Data Subject Request) automation, cross-border transfers, breach notification, and anonymization pipelines with Microsoft Presidio and Faker."
metadata:
  type: defensive
  phase: report
  tools: [privacy-checklists, microsoft-presidio, arx-data-anonymizer, open-differential-privacy]
  mitre: [T1068, T1005]
---

# Data Privacy and Anonymization Engineering Specialist

This skill guides the AI to act as a **Senior Specialist in Data Privacy, Privacy by Design, and Statistical De-identification Pipelines**, ensuring rigorous compliance with **LGPD**, **GDPR**, **HIPAA**, **ISO/IEC 27701:2025**, and the **NIST Privacy Framework**.

---

## 🧭 1. Regulatory Frameworks and Design Principles

- **LGPD (Brazilian Law 13.709/2018, as amended)**: Legal bases (Art. 7 and Art. 11), data subject rights (Art. 18), data protection impact report (RIPD/DPIA), anonymization standard (Art. 12), and the ANPD as supervisory authority.
- **GDPR (EU Regulation 2016/679)**: Art. 25 (*Data protection by design and by default*), Art. 30 (ROPA), Art. 35 (DPIA), Art. 33 (breach notification within 72 hours), Chapter V transfers (adequacy decisions, SCCs, BCRs), and structural fines.
- **CCPA/CPRA**: Rights to know, delete, correct, opt out of sale/share (GPC), and limit the use of sensitive personal information.
- **HIPAA**: Privacy, Security and Breach Notification Rules; 60-day breach notification for covered entities.
- **ISO/IEC 27701:2025 (PIMS)**: Privacy management requirements for data controllers and data processors. The 2025 edition is an independent management-system standard, not merely an ISO 27001 extension.
- **NIST Privacy Framework 1.0**: Core (Identify-P, Govern-P, Control-P, Communicate-P, Protect-P) → Profiles → Implementation Tiers.
- **Privacy by Design (Ann Cavoukian's 7 Principles)**:
  1. *Proactive, not reactive; preventive, not remedial*
  2. *Privacy as the default setting (Privacy by Default)*
  3. *Privacy embedded into the design of the architecture*
  4. *Full functionality (positive sum, dual business and security gain)*
  5. *End-to-end security across the entire data lifecycle*
  6. *Visibility and transparency of processing*
  7. *Respect for privacy and user centricity*

---

## 🔐 2. Formal and Mathematical De-identification Models

### 2.1 $k$-Anonymity (Sweeney, 2002)

A dataset satisfies $k$-anonymity if every tuple of quasi-identifiers (QIDs, such as `Age`, `ZIP`, `Gender`) is indistinguishable from at least $k - 1$ other records in the same database.

- **Generalization**: Mapping specific values to ranges (e.g., age `27` $\rightarrow$ `[20-30]`, ZIP `01310-100` $\rightarrow$ `01310-***`).
- **Suppression**: Removal of outlier records that would prevent the group from reaching the threshold $k$.

### 2.2 $l$-Diversity (Machanavajjhala et al., 2006)

Prevents homogeneity attacks where all records in a $k$-anonymous group share the same sensitive value (e.g., everyone in the group has *Cancer*).

- Requires that each equivalence class contains at least $l$ "well-represented" values for each sensitive attribute.

### 2.3 $t$-Closeness (Li et al., 2007)

An equivalence class has $t$-closeness if the distance (measured by *Earth Mover's Distance*) between the probability distribution of a sensitive attribute within the group and its distribution in the global dataset is less than or equal to $t$.

### 2.4 $\epsilon$-Differential Privacy (Dwork, 2006)

A randomized algorithm $\mathcal{M}$ provides $\epsilon$-differential privacy if for all neighboring datasets $D_1, D_2$ differing by at most one individual and every set of outputs $S$:

$$\mathbb{P}[\mathcal{M}(D_1) \in S] \le e^\epsilon \cdot \mathbb{P}[\mathcal{M}(D_2) \in S]$$

- **Laplace Mechanism**: Adds noise calibrated by the global sensitivity $\Delta f$:
  $$Y = f(D) + \text{Laplace}\left(0, \frac{\Delta f}{\epsilon}\right)$$

---

## 🛠️ 3. Implementing Anonymization Pipelines (Microsoft Presidio)

```python
from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import OperatorConfig

# 1. Detecção de PII em texto livre
analyzer = AnalyzerEngine()
text = "O paciente João Silva, CPF 123.456.789-00, reside em São Paulo, email joao@email.com"
results = analyzer.analyze(text=text, language="pt", entities=["PERSON", "EMAIL_ADDRESS", "CPF"])

# 2. Desidentificação e Mascaramento
anonymizer = AnonymizerEngine()
operators = {
    "CPF": OperatorConfig("mask", {"type": "mask", "masking_char": "*", "chars_to_mask": 8, "from_end": True}),
    "EMAIL_ADDRESS": OperatorConfig("replace", {"new_value": "<EMAIL_ANONIMIZADO>"}),
    "PERSON": OperatorConfig("hash", {"hash_type": "sha256"})
}

anonymized_result = anonymizer.anonymize(text=text, analyzer_results=results, operators=operators)
print(anonymized_result.text)
```

---

## ⚖️ 4. Data Subject Rights (DSRs) Management and Retention

1. **Right of Access and Portability**: Structured APIs to issue JSON or an encrypted PDF containing all data linked to the data subject.
2. **Right to Erasure / Deletion**: Cascading purge of data across transactional databases, logs, and analytical replicas, persisting only immutable audit hashes.
3. **Record of Processing Activities (ROPA)**: Continuous mapping of purpose, data category, transfers, and legally justifiable retention periods.
4. **Consent Management**: Granular, revocable consent with proof of capture, honoring Global Privacy Control (GPC) signals and downstream propagation to processors.
5. **Retention and Disposal**: Defensible disposal schedules with proof of deletion, and legal hold exceptions.

---

## 🌍 5. Cross-Border Transfers and Breach Notification

- **Transfers**: map data flows, rely on an adequacy decision where one exists, otherwise execute SCCs or BCRs and perform a Transfer Impact Assessment (TIA); honor data-residency and sovereignty constraints.
- **Breach notification**: GDPR within **72 hours** to the supervisory authority, HIPAA within 60 days, LGPD to the ANPD and data subjects when there is relevant risk; maintain an incident log and a notification decision record.

---

## 🧪 6. Privacy-Enhancing Technologies (PETs)

| PET | When to use | Notes |
| :--- | :--- | :--- |
| **Differential Privacy (DP-SGD)** | Training or publishing statistics over personal data | Per-example gradient clipping and noise; compose privacy budget across steps. |
| **Federated Learning** | Training across data that must not be centralized | Combine with DP and secure aggregation; never assume the gradients are private without it. |
| **Secure Multi-Party Computation (SMPC)** | Joint computation without revealing inputs | Higher communication cost; good for cross-organization analytics. |
| **Homomorphic Encryption (FHE)** | Computation on encrypted data | Still expensive; use for narrow, high-value workloads. |
| **Trusted Execution Environments (TEE / Confidential Computing)** | Processing in an attested enclave | Depends on a hardware root of trust; verify remote attestation. |
| **Synthetic Data** | Sharing or testing without exposing real records | Validate disclosure risk; synthetic data is not automatically anonymous. |

---

## 🔀 7. Tokenization vs Masking vs Pseudonymization vs Anonymization

| Technique | Reversible? | Still personal data? | Typical use |
| :--- | :--- | :--- | :--- |
| **Tokenization** | Yes (via a vault or, vaultless, via FPE) | Yes | Payment card data (PCI DSS / EMV tokens), internal identifiers |
| **Format-Preserving Encryption (FPE FF1/FF3-1)** | Yes (with the key) | Yes | Legacy fields that require the original format (SP 800-38G) |
| **Masking** | No | Yes (if the underlying data remains) | Display and logs |
| **Pseudonymization** | Yes (with a separately held key) | Yes — Recital 26 / LGPD Art. 13 §4 | Analytics where linkage must remain possible under controls |
| **Anonymization** | No, under reasonable means | No — out of scope | Publication, long-term retention |

> For regulatory requirements on data classification and legal bases (LGPD/GDPR), see [`references/lgpd_gdpr_privacy_by_design.md`](./references/lgpd_gdpr_privacy_by_design.md). For a DPIA/RIPD assessment example, see [`examples/dpia_privacy_assessment.md`](./examples/dpia_privacy_assessment.md).
