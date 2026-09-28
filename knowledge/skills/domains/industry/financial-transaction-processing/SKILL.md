---
name: "financial-transaction-processing"
description: "Acts as a specialist in financial transaction processing and payment systems in Brazil (Pix, SPI, DICT, SPB, Boleto, CIP/Núclea) and abroad (ISO 20022, SWIFT, FedNow, SEPA, Acquiring, Gateways, Anti-Fraud, Reconciliation, and Idempotency)."
---

# AI Skill: Financial Transaction Processing Specialist

This skill guides the artificial intelligence to act as a **Payments and Financial Systems Engineering Specialist**, providing messaging architectures, banking settlement protocols in Brazil and abroad, acquiring engines, fraud prevention, reconciliation, and transactional resilience assurance.

---

## 🇧🇷 1. Payment Arrangements and Financial Systems in Brazil (BCB / SPB)

### 1. Pix System & SPI (Instant Payment System)
- **Components of the Pix Arrangement**:
  - **SPI (Instant Payment System)**: Centralized infrastructure maintained by the Central Bank of Brazil (BCB) for real-time gross settlement (*RTGS - Real-Time Gross Settlement*) of Pix transfers between direct participants.
  - **DICT (Directory of Transactional Account Identifiers)**: Centralized BCB database that maps Pix Keys (CPF/CNPJ, Email, Phone, Random Key/EVP) to customers' transactional accounts (ISPB, Branch, Account).
- **Communication and Security Protocol**:
  - Communication via XML messages digitally signed with hardware security certificates (**ICP-Brasil / RSADSSA-PSS**).
  - Use of QR Code payloads in the **EMVCo** standard (Static and Dynamic with JWS / payload signature support).
- **Refund and Protection Mechanisms**:
  - **Pix Dev (Refund)**: Transaction triggered by the receiving user to reverse amounts.
  - **MED (Special Refund Mechanism)**: Operational procedure standardized by the BCB for freezing and refunding amounts in cases of founded suspicion of fraud or operational failure at the receiver's PSP.

### 2. SPB (Brazilian Payment System) & Registrars
- **STR (Reserve Transfer System)**: Real-time settlement system maintained by the BCB for interbank operations and TEDs (Available Electronic Transfer).
- **Bank Boleto & CIP (Núclea)**:
  - Mandatory registration of Boletos in the CIP/Núclea or C3 database.
  - Real-time validation of the barcode / digitable line with retrieval of payer data and settlement discount.

---

## 🌍 2. Global Financial Transaction Systems (Cross-Border & Instant)

### 1. ISO 20022 Messaging Standard
An international XML/JSON standard that replaces legacy text formats and standardizes the exchange of financial information between financial institutions worldwide:

- **Fundamental Messages (`pacs`, `camt`, `pain`)**:
  - `pacs.008` (Financial Customer Credit Transfer): Credit transfer instruction between customers.
  - `pacs.002` (Payment Status Report): Report confirming, rejecting, or pending a transaction.
  - `camt.053` (Bank to Customer Statement): Bank statement for a current account for reconciliation.
  - `pain.001` (Customer Credit Transfer Initiation): Transfer request initiated by the customer.

### 2. SWIFT & International Transfers (Cross-Border)
- **SWIFT Network (Society for Worldwide Interbank Financial Telecommunication)**:
  - Migration of legacy MT messages (MT103, MT202) to the **ISO 20022 MX** standard.
  - **SWIFT gpi (Global Payments Innovation)**: Real-time tracking with fee transparency and immediate end-to-end credit confirmation via the *Unique End-to-End Transaction Reference (UETR)*.

### 3. International Instant Payment Networks
- **FedNow (Federal Reserve System - USA)**: 24/7/365 instant payment infrastructure in the United States based on ISO 20022.
- **SEPA Instant Credit Transfer (SCT Inst - European Union)**: Instant euro transfers between accounts in the SEPA area in under 10 seconds.

---

## 💳 3. Acquiring, Gateways, and Card Processing

### 1. The Card Transaction Flow (4-Party Cycle)

```text
  Cardholder  --->  Merchant (POS / E-commerce)
                          |
                          v
                   Gateway / Sub-acquirer
                          |
                          v
                      Acquirer (Cielo, Rede, Stone, etc.)
                          |
                          v
                     Card Network (Visa, Mastercard, Elo)
                          |
                          v
                     Issuing Bank
```

### 2. ISO 8583 Protocol (Card Financial Messaging)
- **MTI (Message Type Identifier)**:
  - `0100`: Authorization Request.
  - `0110`: Authorization Response.
  - `0200`: Financial Transaction Request (capture).
  - `0400`: Reversal Request.
- **Main Fields (Data Elements / Bitmaps)**:
  - DE-3 (Processing Code), DE-4 (Amount), DE-11 (SYSTEM Trace Audit Number - STAN), DE-39 (Response Code - e.g., `00` Approved, `51` Insufficient Funds, `05` Do Not Honor), DE-55 (EMV / Chip ICC Data).

### 3. Anti-Fraud and Risk Engines
- **3D Secure 2.0 (EMV 3DS)**: Silent customer authentication based on contextual data (Device, Geolocation, History) sent to the Issuer to avoid checkout friction.
- **Risk Score & Decision Rules**: Pre-authorization analysis via ML models (card velocity detection, bin attack, suspicious proxy/VPN, fingerprinting).

---

## 🔄 4. Cryptographic Resilience, Reconciliation, and Architecture

### 1. Strict Idempotency
Guarantee that duplicate requests sent due to network failure never result in double debits:

```json
// Mandatory request header in the Payment API
HTTP/1.1 POST /v1/payments
Idempotency-Key: ${IDEMPOTENCY_KEY}
```

- **Idempotency Engine**: Concurrent locking in Redis/Cache with payload hash verification and idempotency key. If the request has already been processed, the previous result is returned immediately without resending the transaction to the acquirer/bank.

### 2. Financial Reconciliation Engine
- **Triple Reconciliation**:
  1. *Sales Reconciliation*: Comparison between Application Orders vs Approved Transactions at the Gateway.
  2. *Receivables Reconciliation*: Comparison between Approved Sales at the Gateway vs Acquirers' EDI/MDR files (e.g., File 200/Sales, 202/Adjustments, 204/Payments).
  3. *Bank Reconciliation*: Comparison between Payments Promised by Acquirers vs the Actual Current Account Statement (camt.053 / OFX).

### 3. SAGA Pattern and Distributed Compensation
- Implementation of an orchestrated/choreographed SAGA architecture for multi-step financial flows (Reserve Balance -> Process Card -> Confirm Inventory -> Execute Debit).
- Execution of automatic compensating transactions (Cancellation/Reversal) in case of intermediate failures.

---

## ⚙️ Financial Transaction Engineer Decision Protocol

1. **Require Idempotency at the API Layer**: No payment or transfer route can be accepted without a valid idempotency key.
2. **Separate Authorization from Capture**: For e-commerce sales and services that depend on inventory validation, use prior Authorization and later Capture (*Two-Step Authorization*).
3. **Audit ISO 8583 / Pix Response Codes**: Map payment rejections uniformly, distinguishing human failures (insufficient funds), operational failures (timeout), and security blocks (fraud).

---

## 🏦 5. ACH Processing and Sanctions Screening (Kardell & Brouwer)

- **ACH domain model:** originator → originating depository financial institution → ACH operator (central bank or clearing house) → receiving depository financial institution; the Nacha specification owns the format; routing transit numbers identify banks and trace numbers (originator routing plus an ascending sequence) exist for reconciliation and regulatory traceability.
- **File structure is fixed-width and hierarchical:** 94-character records — file header, repeated batches of batch header, entry details, optional addenda records, batch control, and a file trailer; record order and control totals are part of validity.
- **Parser design decisions:** accumulate an error list instead of fail-fast (testability and batch visibility); decide validate-before-parse versus parse-then-validate explicitly; name functions honestly when a "parser" starts validating; handle addenda look-ahead within streaming constraints.
- **Rejection taxonomy:** file rejection (wrong record length), batch rejection (non-ascending trace numbers), entry rejection (addenda flag inconsistent with the following record); detect before posting wherever possible — posted transactions require reversals.
- **Exception model in operations terms:** error = processing cannot continue; exception = business condition blocking the file (format, invalid data, risk rules); warning = notify and continue (control-total mismatch). Every check needs documented recovery steps — undocumented checks get disabled during incidents. Corrections require an audit trail and originator notification.
- **Persistence principles:** enforce referential integrity with constraints (eliminates cleanup jobs and integrity crashes); store the file hash for identity; keep unparsed raw records beside parsed records for audit and reprocessing.
- **Sanctions screening:** scan entry names and counterparties against sanctions lists at onboarding and in periodic sweeps; upgrade exact and wildcard matching with phonetic and edit-distance functions so deliberately misspelled names still hit; weigh fuzzy-match recall against false-positive review cost and plan rescan scaling as lists grow.
- **Audit log as a control:** capture timestamp, user, request, URL, user agent and IP (CIDR-queryable type) through middleware; logs without a monitor and alert strategy are useless; baseline normal behavior so incident responders do not chase stale errors.
- **GenAI-assisted workflow posture:** generate → run tests → read the code → refine → commit only what passes; nondeterministic output is a draft to be validated by test suites that enumerate each record type, never an oracle; keep customer PII, credentials and proprietary logic out of prompts.

---

## 🔗 Integration with Other Skills

- For adapting the environment to credit card security standards and CDE scope, consult the [pci-dss-compliance](../../../security/grc/pci-dss-compliance/SKILL.md) skill.
- For RSADSSA-PSS digital signatures and Pix/SPB payload encryption, consult the [cryptography-pqc-standards](../../../security/crypto/cryptography-pqc-standards/SKILL.md) skill.
- For developing resilient REST APIs and payment microservices, consult the [backend-developer](../../../roles/backend-developer/SKILL.md) skill.
