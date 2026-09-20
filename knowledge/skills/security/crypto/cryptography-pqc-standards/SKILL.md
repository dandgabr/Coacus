---
name: cryptography-pqc-standards
description: "Acts as a senior specialist in Cryptographic Engineering, Post-Quantum Cryptography (PQC FIPS 203/204/205), Public Key Infrastructure (PKI X.509v3), Key Management (DEK/KEK, Envelope Encryption, KMS/HSM), Digital Signatures (CAdES, XAdES, PAdES, JAdES, eIDAS, ICP-Brasil), Encryption at Rest (FDE, XTS-AES, TDE), Advanced Cryptography (Homomorphic FHE, FPE, ZKP, MPC/Threshold FROST), and Secure Transport Protocols (TLS 1.3, ECH, mTLS, QUIC, WireGuard, IPsec)."
metadata:
  type: defensive
  phase: weaponize
  tools: [openssl, step-cli, vault, cert-manager, cosign, botan, libsodium]
  mitre: [T1203, T1573, T1140]
---

# Cryptographic Engineering, PKI, Digital Signatures, and PQC Standards

This skill guides the AI to act as a **Senior Specialist in Cryptographic Engineering, PKI, and Communications Security**, covering data at rest, in transit, and in use, aligning with the **NIST**, **ISO/IEC**, **IETF RFCs**, **ETSI**, and **ICP-Brasil/eIDAS** standards.

---

## 🧭 1. Reference Standards and Specifications

- **Post-Quantum Cryptography (PQC)**: NIST FIPS 203 (ML-KEM / Kyber), FIPS 204 (ML-DSA / Dilithium), FIPS 205 (SLH-DSA / SPHINCS+), SP 800-208 (LMS / XMSS).
- **Symmetric Cryptography and Modes of Operation**: NIST SP 800-38A/D/E/F/G (GCM, XTS-AES, Key Wrap KW/KWP, Format-Preserving FF1/FF3-1).
- **Key Management and Lifecycle**: NIST SP 800-57 Part 1 Rev. 5, SP 800-131A, RFC 3394/5649.
- **Secure Transport Protocols**: RFC 8446 (TLS 1.3), RFC 9458 (Encrypted Client Hello - ECH), RFC 9000/9114 (QUIC/HTTP-3), RFC 8804 (WireGuard), RFC 7296 (IPsec IKEv2), SPIFFE/SPIRE (mTLS for workloads).
- **PKI and Digital Signatures**: RFC 5280 (X.509v3 PKI), ETSI EN 319 122 (CAdES), ETSI EN 319 132 (XAdES), ETSI EN 319 142 (PAdES), ETSI TS 119 182 (JAdES), RFC 3161 (TSA - Time Stamping Authority), ICP-Brasil (DOC-ICP-01/05), eIDAS (EU Regulation 910/2014).

---

## 💾 2. Data-at-Rest Encryption Matrix

| Layer | Algorithm / Mechanism | Application and Protection Mechanisms |
| :--- | :--- | :--- |
| **Full Disk Encryption (FDE)** | **XTS-AES-256** (IEEE 1619 / SP 800-38E) | Sector/block on NVMe/SSD through dm-crypt/LUKS2, BitLocker, and FileVault. Prevents block-level tampering. |
| **Database TDE** | **AES-256-GCM / CBC** | Transparent encryption in PostgreSQL, MariaDB, MySQL InnoDB, and Oracle tablespaces. |
| **Field-Level / App Encryption** | **AES-256-GCM** / **ChaCha20-Poly1305** | Encryption at the application layer before sending to the database, protecting against leakage from a compromised DBA. |
| **Envelope Encryption** | **DEK + KEK** (KMS / HSM) | Data encrypted locally with a Data Encryption Key (DEK); the DEK encrypted with a Key Encryption Key (KEK) in the KMS/HSM (AWS KMS, Azure Key Vault, HashiCorp Vault). |

---

## 🏛️ 3. Public Key Infrastructure (PKI) and X.509v3 Lifecycle

```
┌─────────────────────────────────────────────────────────────┐
│ 1. Offline Root CA (Air-gapped HSM, 4096-bit RSA / P-384)   │
└──────────────────────────────┬──────────────────────────────┘
                               │ Assina exclusivamente CAs subordinadas
┌──────────────────────────────▼──────────────────────────────┐
│ 2. Intermediate / Issuing CA (Vault PKI / Step-CA / EJBCA)  │
└──────────────────────────────┬──────────────────────────────┘
                               │ Emissão automatizada (ACME / SCEP / EST)
┌──────────────────────────────▼──────────────────────────────┐
│ 3. End-Entity Certs (TLS Server, mTLS Client, Code Signing)  │
└─────────────────────────────────────────────────────────────┘
```

### 3.1 Essential Commands with `step-cli` and `openssl`

```bash
# Gerar CA Raiz e Intermediária efêmera com step-cli
step certificate create "Root CA Corporativa" root-ca.crt root-ca.key --profile root-ca
step certificate create "Intermediate CA" intermediate-ca.crt intermediate-ca.key \
    --profile intermediate-ca --ca root-ca.crt --ca-key root-ca.key

# Inspecionar CSR e certificado X.509
openssl req -in server.csr -noout -text
openssl x509 -in server.crt -noout -text -certopt no_pubkey,no_sigdump
```

---

## ✍️ 4. Digital Signature Standards and Legal Assurance

| Standard | Target Format | Technical Structure | Typical Use Cases |
| :--- | :--- | :--- | :--- |
| **CAdES** | Binaries / arbitrary | CMS (*Cryptographic Message Syntax*) | Executables, medical images, immutable logs |
| **XAdES** | XML documents | Enveloped/enveloping XML-DSig | Electronic Invoice (NF-e, NFS-e), eSocial, SPED |
| **PAdES** | PDF documents | ISO 32000-1 signature dictionary | Contracts, legal reports, electronic medical records |
| **JAdES** | JSON / REST APIs | RFC 7515 (JWS) with ETSI attributes | Open Banking, Open Insurance, federated tokens |

- **ICP-Brasil**: Types **A1** (key in software/PKCS#12, 1 year), **A3** (key on USB token/smartcard PKCS#11, up to 5 years), **A4/Cloud** (cloud HSM with MFA).
- **Long-Term Validation (LTV)**: Incorporation of a Time Stamp (TSA RFC 3161) and CRL/OCSP responses in the signature envelope (PAdES-LTV / CAdES-A).

---

## ⚛️ 5. Post-Quantum Cryptography (PQC) and FIPS Algorithms

1. **ML-KEM (FIPS 203 - Kyber)**:
   - Key Encapsulation Mechanism based on algebraic lattices (*Module-LWE*).
   - Security levels: Kyber-512 (Level 1 ~ AES-128), Kyber-768 (Level 3 ~ AES-192), Kyber-1024 (Level 5 ~ AES-256).
2. **ML-DSA (FIPS 204 - Dilithium)**:
   - Digital Signature standard based on lattices (*Module-LWE/SIS*).
   - Replaces RSA and ECDSA in government PKI and PQC X.509 digital certificates.
3. **Hybrid Classical + PQC Schemes**:
   - Secure transition in TLS 1.3 combining `X25519 + Kyber768` (IETF draft) to guarantee confidentiality against *"Harvest Now, Decrypt Later"* attacks without breaking legacy compatibility.
