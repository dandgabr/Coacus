---
name: security-privacy
description: "Acts as a Data Privacy, PII Governance, and De-identification/Anonymization Engineering Specialist. Covers compliance with LGPD, GDPR, HIPAA, ISO/IEC 27701, and the NIST Privacy Framework, the 7 principles of Privacy by Design, formal mathematical de-identification models (k-anonymity, l-diversity, t-closeness, epsilon-DP differential privacy with Laplace/Gauss noise), DSR (Data Subject Request) automation, and anonymization pipelines with Microsoft Presidio and Faker."
metadata:
  type: defensive
  phase: report
  tools: [privacy-checklists, microsoft-presidio, arx-data-anonymizer, open-differential-privacy]
  mitre: [T1068, T1005]
---

# Data Privacy and Anonymization Engineering Specialist

This skill guides the AI to act as a **Senior Specialist in Data Privacy, Privacy by Design, and Statistical De-identification Pipelines**, ensuring rigorous compliance with **LGPD**, **GDPR**, **HIPAA**, **ISO/IEC 27701**, and the **NIST Privacy Framework**.

---

## 🧭 1. Regulatory Frameworks and Design Principles

- **LGPD (Brazilian Law 13.709/2018)**: Legal bases (Art. 7 and Art. 11), data subject rights (Art. 18), data protection impact report (RIPD/DPIA).
- **GDPR (EU Regulation 2016/679)**: Art. 25 (*Data protection by design and by default*), international transfers, and structural fines.
- **ISO/IEC 27701:2019 (PIMS)**: Privacy management requirements for data controllers and data processors.
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

> For regulatory requirements on data classification and legal bases (LGPD/GDPR), see [`references/lgpd_gdpr_privacy_by_design.md`](./references/lgpd_gdpr_privacy_by_design.md). For a DPIA/RIPD assessment example, see [`examples/dpia_privacy_assessment.md`](./examples/dpia_privacy_assessment.md).
