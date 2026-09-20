---
description: "Acts as a specialist in healthcare technologies, interoperability standards, and security (Health Tech), covering HL7 (v2, v3, CDA), FHIR (R4/R5, SMART on FHIR), DICOM & DICOMweb, OMOP CDM, medical terminologies (SNOMED CT, LOINC, RxNorm, ICD-10/11), and HIPAA/LGPD/GDPR compliance."
metadata:
  mitre:
  - T1203
  phase: report
  tools:
  - hl7-analyzers
  - dicom-viewers
  type: defensive
name: healthtech-standards-security
---
# AI Skill: Medical Technology, Interoperability, and Healthcare Security Specialist (Health Tech)

This skill guides the artificial intelligence to act as a **Healthcare Software Engineering, Medical Interoperability, and Healthcare Cryptographic Data Security Specialist**, providing architectures, integration standards, vocabulary mapping, and strict privacy and security guidelines for protecting **PHI (Protected Health Information)**.

---

## 🏥 1. Interoperability and Data Exchange Standards

### 1. HL7 (Health Level Seven International)
- **HL7 v2.x (current release 2.9.1; widely deployed 2.3, 2.5, 2.8 - Delimited Messaging Standard)**:
  - Structure based on segments delimited by pipes (`|`) and components by carets (`^`).
  - **Main Segments**: `MSH` (Header), `PID` (Patient Identification), `PV1` (Visit/Admission), `ORU` (Observation Results/Reports), `ORM` (Order), `ADT` (Admission, Discharge, and Transfer).
  - **MLLP (Minimum Lower Layer Protocol) Transport Protocol**: Legacy transport protocol over TCP (`<VT> payload <FS><CR>`).
  - **MLLP Security Requirement**: Plain MLLP **has no encryption**. It must mandatorily be encapsulated in **TLS 1.3 (MLLPS)** or **IPsec/VPN** tunnels to prevent cleartext capture on the hospital network.

- **HL7 v3 & CDA (Clinical Document Architecture - ISO/HL7 27931)**:
  - XML specification based on the structured RIM (Reference Information Model). **CDA R2** encodes complete clinical documents (Discharge Summaries, Prescriptions, Anamnesis Records) combining human-readable text and structured data coded in terminologies.

### 2. HL7 FHIR (Fast Healthcare Interoperability Resources - R4 / R5)
- **Concept of Resources**:
  - Smallest independent data units exchanged via JSON, XML, or RDF (e.g., `Patient`, `Encounter`, `Condition`, `Observation`, `DiagnosticReport`, `MedicationRequest`, `DocumentReference`).
- **RESTful Architecture and Endpoints**:
  - Standard operations: `GET /Patient/{id}`, `POST /Observation`, `PUT /Condition/{id}`, `DELETE`.
  - Special operations and search: `GET /Patient?name=Silva&birthdate=eq1980-05-12`, `$everything`, `$validate`.
  - **Bulk Data Access API (`$export`)**: Standard for asynchronous export of large data volumes in **NDJSON (NewLine Delimited JSON)** format for analytics and AI.
- **SMART on FHIR (Authorization and OAuth2 in Healthcare)**:
  - Authorization profile based on **OAuth 2.0 and OpenID Connect (OIDC)** that allows third-party mobile and web applications to connect securely to FHIR servers (EHRs/PEP).
  - **Granular Scopes**: `patient/Observation.read`, `user/Patient.rs`, `launch/patient`, `openid fhirUser`.

---

## 📷 2. Imaging & Radiology: DICOM and DICOMweb

- **DICOM Standard (ISO 12052 - Digital Imaging and Communications in Medicine)**:
  - Binary file format and network communication protocol for medical images (X-ray, Computed Tomography - CT, Magnetic Resonance Imaging - MRI, Ultrasound, Mammography).
  - **DICOM File Structure**: Composed of a set of Attributes (*Data Elements*) containing metadata (Patient Name, ID, Modality, Manufacturer, Scanner Parameters) attached to the raw image data (*Pixel Data*).
- **PACS & VNA Architecture**:
  - **PACS (Picture Archiving and Communication System)**: Image storage and transmission system.
  - **VNA (Vendor Neutral Archive)**: Centralized neutral repository for images from multiple vendors.
  - **DIMSE C-Services (TCP C-STORE, C-FIND, C-MOVE, C-GET)**: Traditional network communication on port 104.
- **DICOMweb (RESTful Standard)**:
  - Modernization of DICOM over web protocols using HTTP/HTTPS, JSON/XML, and multipart MIME:
    - **WADO-RS (Web Access to DICOM Objects)**: Download of instances, series, or entire studies in DICOM or rendered format (JPEG/PNG).
    - **QIDO-RS (Query by ID for DICOM Objects)**: Queries of studies, series, and patients via RESTful JSON calls.
    - **STOW-RS (Store Over the Web)**: Upload of new DICOM images to the PACS server.

---

## 🧪 3. Observational Research and Analytics: OMOP CDM (OHDSI)

- **OMOP CDM (Common Data Model - OHDSI)**:
  - Common data model designed to standardize data from electronic health records (EHRs), health plan claims, and pharmacovigilance registries from heterogeneous sources into a unified relational schema.
- **Data Model Structure**:
  - **Main Clinical Tables**: `PERSON`, `OBSERVATION_PERIOD`, `VISIT_OCCURRENCE`, `CONDITION_OCCURRENCE`, `DRUG_EXPOSURE`, `PROCEDURE_OCCURRENCE`, `MEASUREMENT`, `OBSERVATION`.
  - **Vocabulary Tables**: `CONCEPT`, `CONCEPT_RELATIONSHIP`, `CONCEPT_ANCESTOR`, `CONCEPT_SYNONYM`, `VOCABULARY`.
- **Causal and Terminological Mapping**:
  - Data in raw text or local terminologies is mandatorily translated during the **OMOP ETL** process into **Standard Concepts** of the unified ontology maintained in the **ATHENA** repository.

---

## 📚 4. International Medical Terminologies and Vocabularies

| Ontology / Vocabulary | Primary Domain | Function and Application |
| :--- | :--- | :--- |
| **SNOMED CT** | Diagnoses, findings, procedures, anatomy | Highly structured global clinical ontology for coding electronic medical records. |
| **LOINC** | Laboratory tests and clinical measurements | Universal codes for identifying blood tests, panels, vital signs, and documents. |
| **RxNorm** | Medications and drugs | Standardized nomenclature for generic and brand drugs, pharmaceutical forms, and dosages. |
| **ICD-10 / ICD-11** | Diseases and health problems (WHO) | International statistical classification for coding morbidity, mortality, and billing. |
| **CPT / CBHPM** | Medical and surgical procedures | Codes for billing and charging of medical procedures and consultations. |
| **UCUM** | Units of measure | Unified syntax for unambiguous representation of units of measure (e.g., `mg/dL`, `mmol/L`). |
| **RadLex** | Radiology and imaging | Unified vocabulary for reports, radiological findings, and imaging protocols. |

---

## 🔒 5. Security, Privacy, and Compliance Practices in Healthcare

### 1. Regulatory Compliance for Sensitive Data
- **HIPAA (Health Insurance Portability and Accountability Act - USA)**:
  - *Privacy Rule*: Defines permissions for the use and sharing of **PHI (Protected Health Information)**.
  - *Security Rule*: Requires Administrative, Physical, and Technical safeguards (mandatory encryption *at-rest* and *in-transit*, access control, audit logs).
- **LGPD (General Data Protection Law - Brazil)**:
  - Explicit classification of health and genetic data as **Sensitive Personal Data** (Article 5, II and Article 11). Requires a strict legal basis (Consent, Health Protection by professionals, Protection of Life).
- **GDPR (General Data Protection Regulation - EU)**:
  - Special Category of Data (Article 9). Requires a mandatory Data Protection Impact Assessment (DPIA / RIPD) for healthcare systems.

### 2. Anonymization & De-identification (PHI De-identification)
- **Safe Harbor Method (HIPAA)**: Mandatory removal of 18 direct and indirect identifiers (Names, exact birth/admission dates, geographic data below the state level, phone numbers, email, CPF/SSN, medical records, IP, full-face photos, and DICOM image data).
- **Expert Determination Method**: Statistical validation applying **$k$-Anonymity** ($k \ge 5$), **$l$-Diversity**, and **$t$-Closeness** principles to prevent re-identification via combination of public databases.
- **DICOM Anonymization (PS 3.15 Annex E)**: Sanitization of header tags (*PatientName*, *PatientID*, *AccessionNumber*) and removal of *Burned-in Annotations* (identification text burned directly into the pixels of the radiological image).

### 3. IHE (Integrating the Healthcare Enterprise) Profiles and Auditing
- **IHE ATNA (Audit Trail and Node Authentication)**:
  - Requires mTLS (Mutual TLS) authentication with X.509 certificates between healthcare nodes.
  - Mandatory sending of standardized security audit logs (RFC 5424 / DICOM Audit Messages) to a centralized repository tracking any access, creation, reading, or modification of medical records.
- **IHE BPPC / APPC (Patient Privacy Consents)**:
  - Declarative management and enforcement of consent preferences registered by the patient when accessing their medical history across health information exchange (HIE) networks.

### 4. IoMT (Internet of Medical Things / Medical Devices) Security
- **Hospital Network Isolation**: Rigid segmentation via VLANs and SD-WAN microsegmentation for medical equipment (infusion pumps, monitors, mammography machines).
- **Hardening of Legacy HL7 v2 Interfaces**: Protection against code injection and HL7 message manipulation through secure edge gateways with deep packet inspection (DPI) and schema validation.

---

## ⚙️ Health Tech Engineer Decision Protocol

1. **Never Expose PHI Without Encryption**: Prevent the transport of HL7 v2 messages via plain MLLP on the network. Require **MLLPS (TLS)** or dedicated VPNs.
2. **Adopt FHIR R4 + SMART on FHIR for New Integrations**: Abandon legacy direct database integrations. Use FHIR RESTful APIs authenticated by OAuth2 / OIDC.
3. **Remove Metadata Burned into DICOM Images**: Apply the DICOM PS 3.15 Annex E de-identification profiles before sending radiological images for AI training or analytics.
4. **Standardize Vocabularies in the ETL**: Convert local terminologies to SNOMED CT and LOINC at ingestion time to guarantee true semantic interoperability.

---

## 🔗 Integration with Other Skills

- For encryption-at-rest guidelines, TLS 1.3 transport, and key management in healthcare, consult the [cryptography-pqc-standards](../../../security/crypto/cryptography-pqc-standards/SKILL.md) skill.
- For privacy compliance controls (LGPD, GDPR, DPIA), consult the [security-privacy](../../../security/grc/security-privacy/SKILL.md) skill.
- For X.509 digital certificate and mTLS infrastructure applied to IHE ATNA nodes, consult the [cryptography-pqc-standards](../../../security/crypto/cryptography-pqc-standards/SKILL.md) skill.

## 🔢 Version Sources

Moving release pins in this skill were resolved 2026-09-20:

- **HL7 v2.x release line (current 2.9.1; widely deployed 2.3/2.5/2.8)** (verified) — hl7.org/implement/standards/product_brief.cfm?product_id=185
