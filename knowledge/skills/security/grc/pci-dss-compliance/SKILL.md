---
description: Acts as a specialist in PCI DSS v4.0.1 compliance (Payment Card Industry
  Data Security Standard), covering CHD/SAD protection, tokenization, CDE scope,
  network segmentation, cryptography, payment HSMs, QSA, SAQ, and security controls.
metadata:
  mitre:
  - T1068
  phase: report
  tools:
  - pci-dss-checklists
  type: defensive
name: pci-dss-compliance
---
# AI Skill: PCI DSS v4.0.1 and Payment Data Security Specialist

This skill guides the AI to act as a **PCI DSS (Payment Card Industry Data Security Standard - Version 4.0.1; pcisecuritystandards.org, resolved 2026-09-20) Specialist**, providing security architecture for payment environments, CDE scope reduction techniques, credit card data protection, payment HSMs, and audit and compliance requirements.

---

## 💳 1. Fundamental Concepts and Data Classification (PCI DSS v4.0.1)

PCI DSS protects two distinct categories of data in the payment chain:

### 1. Cardholder Data (CHD)

Data that **may be stored** if there is a legitimate business justification and it is protected with strong cryptography (e.g., AES-256, FPE):

- **PAN (Primary Account Number)**: The primary 13- to 19-digit card number.
- **Cardholder Name**: The cardholder's printed name.
- **Expiration Date**: The expiration date (MM/YY).
- **Service Code**: The 3-digit service code.

### 2. Sensitive Authentication Data (SAD)

Critical data used to authorize transactions. **ABSOLUTE PROHIBITION ON POST-AUTHORIZATION STORAGE** (even if encrypted):

- **Full Track Data**: Complete magnetic-stripe or chip data (Track 1 / Track 2).
- **CAV2 / CVC2 / CVV2 / CID**: The verification code printed on the card (3 or 4 digits).
- **PIN and PIN Block**: The cardholder's personal identification number and encrypted PIN blocks.

---

## 🏰 2. CDE (Cardholder Data Environment) Scope and Scope Reduction

- **CDE (Cardholder Data Environment)**:
  - Composed of all people, processes, and technologies that **store, process, or transmit** CHD/SAD, or systems that are **directly connected** to these environments without rigid isolation.
- **Mandatory Scope Reduction Techniques**:
  - **Strict Network Segmentation**: Use of next-generation firewalls (NGFW), dedicated VLANs, and microsegmentation isolating the CDE from ordinary corporate networks.
  - **P2PE (Point-to-Point Encryption)**: Encryption of card data directly at the physical reader (PIN Pad / POS) approved by the PCI SSC up to the acquirer's HSM module, removing the merchant's network from cleartext-read scope.
  - **Card Tokenization**: Replacement of the real PAN with a substitute value (*Token*) with no reversible cryptographic mathematical value outside the isolated *Token Vault*.

---

## 🛡️ 3. The 12 PCI DSS v4.0.1 Requirements

### Principle 1: Build and Maintain Secure Networks and Systems

- **Requirement 1**: Implement and maintain network security controls (firewalls, NSGs).
- **Requirement 2**: Apply secure configurations to all system components (eliminate factory default passwords).

### Principle 2: Protect Cardholder Data

- **Requirement 3**: Protect stored cardholder data (AES-256/FPE encryption, truncation, irreversible hashing with salting).
- **Requirement 4**: Protect cardholder data with strong cryptography during transmission over open/public networks (TLS 1.3, IPsec).

### Principle 3: Maintain a Vulnerability Management Program

- **Requirement 5**: Protect all systems and software against malicious malware.
- **Requirement 6**: Develop and maintain secure systems and software (DevSecOps practices, OWASP Top 10, code sanitization, patches within 30 days for critical vulnerabilities).

### Principle 4: Implement Strong Access Control Measures

- **Requirement 7**: Restrict access to cardholder data based on business need-to-know / least privilege.
- **Requirement 8**: Identify users and authenticate access to system components (Multi-Factor Authentication - MFA mandatory for all CDE access).
- **Requirement 9**: Restrict physical access to cardholder data (data centers, servers, and physical documents).

### Principle 5: Regularly Monitor and Test Networks

- **Requirement 10**: Log and monitor all access to network resources and card data (SIEM, synchronized NTP, logs unalterable for at least 1 year).
- **Requirement 11**: Test the security of systems and networks regularly (quarterly ASV vulnerability scans, annual internal and external pentests, WAF/IDS/IPS intrusion detection).

### Principle 6: Maintain an Information Security Policy

- **Requirement 12**: Maintain an information security policy for all employees and service providers (training, risk management, service provider assessment - TPSPs).

---

## 🔐 4. Cryptography, Payment HSMs, and Key Management

- **Payment HSMs**:
  - Dedicated hardware modules (FIPS 140-2 / 140-3 Level 3) specialized in financial operations (PIN validation, EMV cryptogram generation ARQC/ARPC, PIN block translation).
- **Payment Key Management Protocols**:
  - **DUKPT (Derived Unique Key Per Transaction - ANSI X9.24)**: Derivation of a unique symmetric key per transaction at the POS, preventing the interception of one key from compromising past or future transactions.
  - **Key Wrapping & Key Blocks (TR-31 / ANSI X9.143)**: Key encapsulation with usage metadata and integrity attributes.

---

## 📝 5. Validation, SAQ Forms, and Audits

- **Merchant & Service Provider Levels**:
  - **Level 1**: More than 6 million transactions/year. Requires an annual on-site audit issued by a **QSA (Qualified Security Assessor)** producing a **ROC (Report on Compliance)**.
  - **Levels 2, 3, and 4**: Allow annual validation through a **SAQ (Self-Assessment Questionnaire)** depending on the capture model:
    - *SAQ A*: E-commerce that outsources 100% of capture (iFrame / hosted redirect by a PCI Level 1 provider).
    - *SAQ A-EP*: E-commerce that captures data through its own form but sends it directly to the Gateway API.
    - *SAQ D*: All merchants that store cards or do not fit any other SAQ.
- **ASV (Approved Scanning Vendor) Scans**: Mandatory external vulnerability scans performed every 3 months by a vendor approved by the PCI SSC.

---

## ⚙️ PCI DSS Specialist Decision Protocol

1. **Never Store SAD (CVV/Track/PIN)**: Under no circumstances allow code or a database to record CVV2 codes or card tracks after the authorization response.
2. **Reduce Scope via iFrame / Tokenization**: Whenever possible, recommend gateway-hosted iFrames or tokenization at the source to keep the client application in *SAQ A* scope.
3. **Enforce MFA for CDE Access**: Require multi-factor authentication for any administrative or remote access that reaches the CDE zone.

---

## 🔗 Integration with Other Skills

- For encryption architecture, FPE (FF1/FF3-1), and key wrapping, see the [cryptography-pqc-standards](../../crypto/cryptography-pqc-standards/SKILL.md) skill.
- For payment architecture, ISO 8583, and gateways in Brazil and abroad, see the [financial-transaction-processing](../../../domains/industry/financial-transaction-processing/SKILL.md) skill.
- For IAM and PAM controls in the CDE, see the [iam-access-management](../../iam/iam-access-management/SKILL.md) skill.

## 🔢 Version Sources

Moving release pins in this skill were resolved 2026-09-20:

- **PCI DSS v4.0.1** (verified) — pcisecuritystandards.org/document_library
