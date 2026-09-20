---
name: crypto-pki-certificate-lifecycle
description: Acts as a PKI specialist covering certificate authority hierarchy design, X.509v3 certificate lifecycle, ACME/CMP/EST automation, Certificate Transparency, revocation at scale, long-term validation and post-quantum X.509 migration per RFC 9881.
metadata:
  type: defensive
  phase: weaponize
---

# PKI and Certificate Lifecycle

This skill guides the AI to design and operate a public key infrastructure end to end, from root CA ceremony to automated renewal and revocation.

---

## 🏛️ 1. CA Hierarchy

```
Offline Root CA (air-gapped HSM)
        |  signs only subordinate CAs
Intermediate / Issuing CA (online, HSM-backed)
        |  issues end-entity certificates
End-Entity (TLS server, mTLS client, code signing)
```

Keep the root offline; its only job is to sign intermediates. Use separate issuing CAs per use case (TLS, client, code signing) so a compromise is contained.

---

## 🔄 2. Automated Lifecycle

- **ACME (RFC 8555)**: the default for TLS certificate automation; validates domain control and issues short-lived certificates with nonce-based replay protection.
- **CMP** and **EST**: enterprise enrollment protocols for device and service certificates.
- **Certificate Transparency (RFC 6962)**: public logs let anyone detect mis-issuance; monitor the logs for your domains.
- Renew well before expiry and monitor expiry centrally; an expired certificate is an outage.

---

## 🚫 3. Revocation at Scale

- **OCSP** for real-time status and **CRLs** as the fallback; both scale poorly at internet size.
- **Short-lived certificates** reduce the reliance on revocation: if a certificate lives for hours, revocation matters less.
- **OCSP stapling** moves the status check to the server.
- Plan for **long-term validation (LTV)** when signatures must remain verifiable for years: timestamp authority (RFC 3161) plus embedded revocation data (PAdES-LTV / CAdES-A).

---

## ⚛️ 4. Post-Quantum X.509 (RFC 9881)

- ML-DSA OIDs and key encodings are standardized; **HashML-DSA is disallowed in PKIX**.
- Prefer the **seed-only private key** representation for portability.
- Signature sizes grow substantially; test protocol and storage limits before rollout.
- Plan hybrid certificate chains during migration so legacy verifiers continue to work.

---

## 🔗 5. Integration with Other Skills

- For the cryptographic algorithms and PQC migration, see the [cryptography-pqc-standards](../cryptography-pqc-standards/SKILL.md) and [crypto-agility-pqc-migration](../crypto-agility-pqc-migration/SKILL.md) skills.
- For key storage in HSM/KMS, see the [crypto-kms-hsm-key-management](../crypto-kms-hsm-key-management/SKILL.md) skill.
- For machine identity certificates, see the [machine-identity-spiffe-workload](../../iam/machine-identity-spiffe-workload/SKILL.md) skill.
