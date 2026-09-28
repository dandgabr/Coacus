---
name: isc2-cissp-csslp-standards
description: Acts as a Specialist in Information Security Governance and Secure Software Lifecycle based on the (ISC)² CISSP and CSSLP Common Bodies of Knowledge (CBK) (Mano Paul). Covers the 8 CISSP domains (Risk Management, Asset Security, Security Engineering, Communication/Network, IAM, Assessment/Testing, Operations, Software Development Security) and the 8 CSSLP phases.
---

# Security Governance and Secure SDLC Standards (ISC2 CISSP & CSSLP)

This skill establishes the standards and guidelines for strategic information security governance, regulatory compliance, and secure software engineering according to the Common Bodies of Knowledge (**CBK**) of the **CISSP** and **CSSLP** certifications from (ISC)².

---

## 🏛️ 1. The 8 Domains of the CISSP CBK

1. **Security and Risk Management**: Compliance, corporate governance, risk assessment (ALE, SLE, ARO), business continuity (BCP/DRP), and professional ethics.
2. **Asset Security**: Classification of information and assets, retention, ownership, and privacy controls.
3. **Security Architecture and Engineering**: Security models (Bell-LaPadula, Biba, Clark-Wilson), cryptography, vulnerability assessment, and physical security.
4. **Communication and Network Security**: Secure network architecture, protected transport protocols (TLS/IPsec), segmentation, and wireless security.
5. **Identity and Access Management (IAM)**: Identification, authentication, authorization (RBAC/ABAC), identity federation, and MFA.
6. **Security Assessment and Testing**: Control auditing, penetration testing, vulnerability reporting, and compliance reviews.
7. **Security Operations**: Forensic investigations, incident response, continuous monitoring (SIEM/SOAR), patching, and disaster recovery.
8. **Software Development Security**: Security in the SDLC, secure code controls, software maturity (SAMM/BSIMM), and supply chain protection.

---

## 🔒 2. The 8 Domains of the CSSLP (Certified Secure Software Lifecycle Professional)

```
┌─────────────────────────────────────────────────────────────┐
│ 1. Secure Software Concepts (CIA Triad, AAA, Defesa em      │
│    Profundidade, Menor Privilégio, Fail-Safe Defaults)      │
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│ 2. Secure Software Requirements (Requisitos de Segurança,   │
│    Modelagem de Ameaças, Conformidade Regulatória)          │
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│ 3. Secure Software Architecture and Design (Padrões de      │
│    Design Seguro, Redução de Superfície de Ataque)          │
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│ 4. Secure Software Implementation (Codificação Segura,      │
│    Tratamento Defensivo de Erros, Sanitização de Inputs)    │
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│ 5. Secure Software Testing (SAST, DAST, SCA, Fuzzing)       │
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│ 6. Secure Lifecycle Management (Gestão de Patches, Decom.)  │
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│ 7. Software Deployment, Operations & Maintenance            │
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│ 8. Secure Software Supply Chain (SBOM, Proveniência SLSA)   │
└─────────────────────────────────────────────────────────────┘
```

---

## 🧮 Crypto and Password Mechanisms (Spraul)

Mechanism-level grounding for the domain concepts above:

- **Cipher primitives:** transposition (reorder) and substitution (replace), parameterized by a key; attacker toolbox — brute force, guessed known plaintexts (cribs), frequency analysis on key reuse; key expansion derives a long round-key schedule from a short memorable key.
- **AES anatomy:** 128-bit keys expand into round keys; plaintext splits into byte grids processed by rounds of byte transposition, S-box substitution and key-dependent mixing; block chaining with a random starting value makes identical plaintext blocks produce different ciphertext, defeating frequency analysis; diffusion and avalanche properties make every ciphertext byte depend on all plaintext bytes. Known weaknesses concentrate in implementations (timing attacks), not the algorithm.
- **Password storage arms race:** store hashes, not plaintexts → dictionary attacks → precomputed tables → hash chains → salts and key-stretching defeat precomputation; rate-limit online guessing. Good hashes are deterministic, well distributed, one-way and avalanche-like; signatures authenticate by encrypting a hash.
- **Public-key bootstrap:** symmetric crypto cannot start a conversation between strangers; RSA-style public-key methods derive a public encryption exponent and a private decryption exponent from a composite modulus whose factorization the attacker lacks.
- **TLS-style handshake mechanics:** negotiate ciphers, verify a certificate chain against trusted roots, exchange a secret encrypted under the server's public key, derive session keys (encryption key, chaining value, integrity key) from the secret plus both parties' randoms — the secret never crosses the wire; hash-then-encrypt (keyed hashing) defeats man-in-the-middle tampering.
