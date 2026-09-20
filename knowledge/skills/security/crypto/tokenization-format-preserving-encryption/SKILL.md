---
name: tokenization-format-preserving-encryption
description: Acts as a Data Protection specialist covering tokenization (vault and vaultless), EMV payment tokens, format-preserving encryption (FF1/FF3-1 per SP 800-38G), masking and pseudonymization, and how each technique affects PCI DSS scope and privacy obligations.
metadata:
  type: defensive
  phase: weaponize
---

# Tokenization and Format-Preserving Encryption

This skill guides the AI to protect sensitive fields (card numbers, national IDs, account numbers) while keeping the systems that consume them working.

---

## 🎭 1. Technique Selection

| Technique | Reversible | Personal data? | Best for |
| :--- | :--- | :--- | :--- |
| **Vault tokenization** | Yes, via lookup | Yes | Removing card data from scope; the vault holds the mapping |
| **Vaultless tokenization** | Yes, via FPE | Yes | Scale without a lookup store |
| **Format-Preserving Encryption** | Yes, with key | Yes | Legacy fields that must retain the original alphabet and length |
| **Masking** | No | Yes if source remains | Display, logs, exports |
| **Pseudonymization** | Yes, with separate key | Yes | Analytics with re-identification under control |
| **Anonymization** | No, reasonably | No | Publication and long-term retention |

---

## 🔢 2. Format-Preserving Encryption (SP 800-38G)

- **FF1** and **FF3-1** encrypt a string of digits or characters into the same format, so no database schema or downstream parser changes.
- **FF3-1** fixed an FF3 weakness by reducing the tweak size; use FF3-1, never the original FF3.
- FPE preserves format, not confidentiality beyond the key: key management is still required and the token remains personal data for privacy purposes.

---

## 💳 3. Payment Tokenization and PCI Scope

- **Network tokens (EMV)**: replace the PAN with a token that only the payment network and issuer can detokenize; the merchant never holds the PAN.
- **PCI Token Service Provider (TSP)** and **point-to-point encryption (P2PE)** move sensitive data out of the merchant environment and reduce CDE scope.
- Tokenization reduces scope, but the token vault itself is in scope and must be protected accordingly.

---

## 🛡️ 4. Operating Rules

1. Never build your own cryptographic tokenization from a hash - a hash is not a token and is reversible by brute force for low-entropy inputs.
2. Separate the tokenization key from the application; compromise of the app must not expose the mapping.
3. Audit every detokenization event; treat it like privileged access.
4. Prefer removing the sensitive data from the system over protecting it in place, where the business allows.

---

## 🔗 5. Integration with Other Skills

- For key custody, see the [crypto-kms-hsm-key-management](../crypto-kms-hsm-key-management/SKILL.md) skill.
- For privacy classification and legal bases, see the [security-privacy](../../grc/security-privacy/SKILL.md) skill.
- For payment system scope, see the [pci-dss-compliance](../../grc/pci-dss-compliance/SKILL.md) skill.
- For data discovery before tokenization, see the [data-classification-dspm](../../data/data-classification-dspm/SKILL.md) skill.
