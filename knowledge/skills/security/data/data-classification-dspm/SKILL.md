---
name: data-classification-dspm
description: Acts as a Data Security Posture Management specialist covering data classification and taxonomy, PII/PHI discovery, data profiling and sensitivity scoring, shadow-data scanning, DSPM across clouds and databases, and the mapping of classification to control baselines.
metadata:
  type: defensive
  phase: recon
---

# Data Classification and DSPM

This skill guides the AI to know where sensitive data lives and how sensitive it is, which is the precondition for protecting it.

---

## 🏷️ 1. Classification Taxonomy

- **Direct identifiers**: name, national ID, email, account number.
- **Quasi-identifiers**: age, postal code, gender - alone insufficient, combinable to re-identify.
- **Sensitive categories**: health, biometric, financial, criminal, children's data - attracting stricter rules.
- **Levels**: public, internal, confidential, restricted.
- Map each level to a control baseline (encryption, access, retention, masking).

---

## 🔍 2. Discovery and Profiling

- **Discovery**: find where data resides across databases, object stores, SaaS, endpoints and backups.
- **Profiling**: measure the actual content - volume, type, sensitivity - rather than trusting metadata labels.
- **Shadow data**: copies outside governance (exports, caches, analytics replicas). Shadow data is where breaches often concentrate.
- Use a detection primitive of pattern plus context plus checksum to reduce false positives; classify by likelihood, then tune.

---

## ☁️ 3. DSPM Workflow

1. Enumerate data stores across cloud accounts and on-prem systems.
2. Classify content and assign sensitivity.
3. Map **reachability**: who and what can access the data, including indirect paths.
4. Rank by risk (sensitivity x exposure x controls).
5. Remediate: tighten access, encrypt, mask, or delete data that should not exist.
6. Monitor for new stores and classification drift.

---

## 🔗 4. Integration with Other Skills

- For DLP enforcement, see the [dlp-data-loss-prevention](../dlp-data-loss-prevention/SKILL.md) skill.
- For privacy governance and legal bases, see the [security-privacy](../../grc/security-privacy/SKILL.md) skill.
- For cloud reachability context, see the [cloud-security-posture-cnapp](../../cloud/cloud-security-posture-cnapp/SKILL.md) skill.
- For tokenization of discovered data, see the [tokenization-format-preserving-encryption](../../crypto/tokenization-format-preserving-encryption/SKILL.md) skill.
