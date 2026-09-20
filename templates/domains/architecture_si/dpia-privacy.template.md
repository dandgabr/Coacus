# Data Protection Impact Assessment Report Template (DPIA)

**Initiative:** `[Project / Module Name]`  
**Date:** `[MM/DD/YYYY]`  
**Data Controller:** `[Legal Entity Name]`  
**Processor / Vendor:** `[Partner Name]`  
**DPO / Data Protection Officer:** `[DPO Name]`  

---

## 1. Description of Personal Data Processing

* **Processing Purpose**: `[Why the data is being collected and processed]`
* **Legal Basis (LGPD Art. 7 or Art. 11)**: `[Consent / Contract Performance / Health Protection / Legal Compliance]`
* **Data Lifecycle**:
  * *Collection*: `[Form, API, medical device, mobile app]`
  * *Storage*: `[Database, retention for X years]`
  * *Sharing*: `[Third-party partners, cloud vendors]`
  * *Deletion / Disposal*: `[Automated expiration and secure purge procedure]`

---

## 2. Categories of Data Subjects and Processed Data

| Data Category | Type (Common / Sensitive) | Specific Attributes | Specific Purpose | Retention Period |
| :--- | :--- | :--- | :--- | :--- |
| **Civil Identification** | Common (Art. 5, I) | Full name, CPF, RG, Email | Authentication and registration | 5 years after termination |
| **Health Data / PHI**| Sensitive (Art. 11) | Test history, diagnoses, medical reports | Medical diagnosis issuance | 20 years (CFM regulation) |
| **Telemetry / Access** | Common | IP, User-Agent, Timestamp | Auditing and security | 6 months (Brazilian Internet Bill of Rights) |

---

## 3. Necessity and Proportionality Assessment (Privacy by Design)

- [ ] **Minimization**: Are only the data strictly necessary for the operation collected? `[Yes / No]`
- [ ] **Privacy by Default**: Do the default settings prioritize privacy and require active consent (*opt-in*)? `[Yes / No]`
- [ ] **Pseudonymization**: Are direct identifiers isolated from diagnostic data in analytics? `[Yes / No]`
- [ ] **Log Masking**: Is there an assurance that no personal data is recorded in application logs? `[Yes / No]`

---

## 4. Privacy Risk and Safeguards Matrix

| ID | Privacy Threat (LINDDUN) | Risk to the Data Subject | Technical and Administrative Safeguards | Residual Risk |
| :--- | :--- | :--- | :--- | :---: |
| **PR-01** | `Disclosure of Information` | Leakage of sensitive medical records | AES-256 column encryption in the database + Tenant Segregation | LOW |
| **PR-02** | `Linkability` | Correlation of logs with patient identity | CPF masking in SIEM logs + Deterministic hashing | LOW |
| **PR-03** | `Unawareness` | Data subject not informed about sharing | Privacy Policy update + Consent Form | LOW |

---

## 5. Concluding Opinion of the DPO / Privacy Specialist

**Conclusion:** `[The data processing was deemed adequate and proportional, provided the listed technical safeguards are implemented.]`
