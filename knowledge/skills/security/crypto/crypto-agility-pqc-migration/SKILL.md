---
name: crypto-agility-pqc-migration
description: Acts as a Cryptography Migration specialist covering cryptographic discovery and CBOM inventory, harvest-now-decrypt-later risk, CNSA 2.0 and ENISA/NCSC timelines, hybrid-to-pure PQC sequencing, deprecation gates and the engineering process for crypto agility.
metadata:
  type: defensive
  phase: recon
---

# Crypto Agility and PQC Migration

This skill guides the AI to plan and execute the migration from classical to post-quantum cryptography as a managed engineering process, not a one-off algorithm swap.

---

## 🗺️ 1. Cryptographic Discovery

- Build a **Cryptographic Bill of Materials (CBOM)** in CycloneDX format: every algorithm, key, certificate and protocol in the estate, with location and owner.
- Scan code, configuration, certificates, firmware and third-party dependencies.
- Rank by exposure: long-lived confidentiality requirements first (harvest-now-decrypt-later).

---

## ⏱️ 2. Timelines and Drivers

- **CNSA 2.0** (NSA, updated 2025) phases migration through 2035 for national-security systems.
- **ENISA** and national bodies (for example, UK NCSC) publish migration guidance and target dates.
- Regulatory pressure (CRA, sector rules) increasingly requires disclosure of cryptographic posture.

---

## 🔀 3. Migration Sequencing

1. **Hybrid first**: deploy hybrid key exchange (for example, X25519MLKEM768 in TLS 1.3 or PQC in IKEv2) so security is not reduced if either component fails.
2. **Signatures second**: migrate code signing, firmware signing and PKI to ML-DSA/SLH-DSA (or LMS/XMSS where hash-based signatures fit).
3. **Pure PQC last**: move to pure PQC only when the ecosystem fully supports it and legacy compatibility is no longer required.
4. **Crypto agility as a property**: abstract algorithm choice behind configuration so the next migration is a config change, not a rewrite.

---

## 🚧 4. Deprecation Gates

Define explicit gates for weak algorithms: SHA-1, 1024-bit RSA, CBC in new designs, TLS below 1.2, non-authenticated encryption. Each gate names the replacement, the owner and the deadline.

---

## 🔗 5. Integration with Other Skills

- For the standards and algorithm details, see the [cryptography-pqc-standards](../cryptography-pqc-standards/SKILL.md) skill.
- For key management during migration, see the [crypto-kms-hsm-key-management](../crypto-kms-hsm-key-management/SKILL.md) skill.
- For PKI migration, see the [crypto-pki-certificate-lifecycle](../crypto-pki-certificate-lifecycle/SKILL.md) skill.
- For network protocol migration, see the [network-security-onprem-cloud](../../operations/network-security-onprem-cloud/SKILL.md) skill.
