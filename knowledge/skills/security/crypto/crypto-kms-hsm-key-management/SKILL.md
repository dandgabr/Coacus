---
name: crypto-kms-hsm-key-management
description: Acts as a Key Management specialist covering key hierarchy (DEK/KEK), envelope encryption, KMS/HSM architecture, FIPS 140-3 and CMVP, key ceremonies, key wrapping, KDFs and DRBGs, and BYOK/HYOK across cloud providers.
metadata:
  type: defensive
  phase: weaponize
---

# Key Management (KMS, HSM and Envelope Encryption)

This skill guides the AI to protect the keys that protect the data. Cryptography fails in practice at key management far more often than at the algorithm.

---

## 🗝️ 1. Key Hierarchy

```
Root / Master Key (HSM, non-exportable)
        |  wraps
Key Encryption Key (KEK) - per tenant or per service
        |  wraps
Data Encryption Key (DEK) - per object or per field, short-lived
        |  encrypts
Data at rest
```

Never encrypt bulk data directly with a long-lived master key. Envelope encryption keeps key rotation cheap: rotate the KEK and re-wrap the DEKs without touching the data.

---

## 🏭 2. HSM and FIPS 140-3

- **FIPS 140-3** defines four security levels; the **CMVP validated-module list** is the compliance evidence, not a vendor claim.
- Use HSMs for root keys, CA signing, and any key with legal or regulatory weight.
- Key ceremonies (generation, backup, restore, destruction) are witnessed, scripted and logged.
- Interfaces: PKCS#11 and KMIP for portability; cloud KMS APIs for managed keys.

---

## 🔁 3. Key Lifecycle

1. **Generate** inside the boundary; never import a root key if it can be generated in place.
2. **Distribute** wrapped, never in clear.
3. **Use** with the narrowest possible scope; one key per purpose.
4. **Rotate** on a schedule and on suspicion; rotation must be routine and rehearsed.
5. **Backup and recover** with split knowledge and dual control (M-of-N).
6. **Destroy** verifiably at end of life.

---

## 🧮 4. KDFs and Randomness

- **SP 800-108** for key derivation (counter, feedback, double-pipeline modes) and **SP 800-56C** HKDF for extraction/expansion.
- **SP 800-90A** DRBGs (Hash, HMAC, CTR) with entropy from **SP 800-90B** sources and constructions per **SP 800-90C**.
- A weak or duplicated RNG undermines every downstream control; treat entropy as a first-class asset.

---

## ☁️ 5. Cloud Key Management

- **BYOK/HYOK**: keep key material under customer control; for HYOK the key never leaves the customer boundary.
- Understand the provider's key hierarchy and what "customer-managed key" actually means for key custody.
- Prefer multi-region/multi-cloud key strategies where resilience requires it, and document the trust boundary of each.

---

## 🔗 6. Integration with Other Skills

- For algorithms and PQC, see the [cryptography-pqc-standards](../cryptography-pqc-standards/SKILL.md) skill.
- For storage encryption specifics, see the [tokenization-format-preserving-encryption](../tokenization-format-preserving-encryption/SKILL.md) skill.
- For cloud secret stores, see the [cloud-secrets-management](../../cloud/cloud-secrets-management/SKILL.md) skill.
- For PKI key custody, see the [crypto-pki-certificate-lifecycle](../crypto-pki-certificate-lifecycle/SKILL.md) skill.
