# Complete Guide to the SABSA 6x6 Matrix and the Business Attribute Profile (BAP)

This guide serves as the technical reference document for the rigorous application of the **SABSA (Sherwood Applied Business Security Architecture)** framework in the repository.

---

## 📐 SABSA 6x6 Matrix (Full View)

The SABSA matrix crosses the 6 layers of architectural abstraction with the 6 fundamental aspects of any information system:

| Layer \ Question | **Assets (What)** | **Motivation (Why)** | **Process (How)** | **People (Who)** | **Location (Where)** | **Time (When)** |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **1. Contextual** *(Business)* | Business Objectives & Value | Business Drivers & Risks | Core Business Processes | Business Actors & Organization | Business Geography & Markets | Business Calendar & Windows of Opportunity |
| **2. Conceptual** *(Architect)* | Business Attribute Profile (BAP) | Business Security Objectives | Security Engineering Concept | Trust and Access Concept | Boundary and Domain Concept | Time Opportunity & Durability Concept |
| **3. Logical** *(Designer)* | Information & Data Models | Logical Security Policies | Security Services & Logical Flows | Logical Entities and Actors | Logical Trust Zones & Networks | Logical Schedule & Sequencing |
| **4. Physical** *(Builder)* | Servers, Databases & Hardware | Physical Security Mechanisms | Applications, Middleware & Protocols | Physical Users & IDs in IdPs | Network Nodes, Cloud & Physical IPs | Real-Time Scalability & Performance |
| **5. Component** *(Tradesman)* | Data Structures, Files & Keys | Security Configuration Rules | Code Functions, APIs & Scripts | Certificates, Keys & Credentials | Memory Addresses & URIs | Timers, Timeouts & Latencies |
| **6. Operational** *(Service Mgr)* | Operational Assets & SIEM Logs | Risk Metrics (KRI/KPI) | SOPs, Playbooks & Runbooks | Operators, DevOps & SOC | Production Environments & Disaster Recovery | Schedules, Maintenance Windows & SLAs |

---

## 📊 Business Attribute Taxonomy (BAP)

The **Business Attribute Profile (BAP)** is the heart of SABSA. It translates subjective business expectations into quantifiable security requirements.

### Main Attribute Categories:

1. **Financial Attributes**:
   - *Transactional Auditability*: End-to-end traceability with no balance deviation.
   - *Cost-Effectiveness*: Positive return on security investment (ROSI).

2. **Operational Attributes**:
   - *Uninterrupted Availability*: Fault tolerance and high resilience (for example, 99.99% SLAs).
   - *Secure Scalability*: Support for traffic spikes without degrading the security profile.

3. **Protection and Privacy Attributes**:
   - *Strict Confidentiality*: Protection against unauthorized access to personal data/PHI.
   - *Inviolable Integrity*: Assurance that no unauthorized modification has occurred.

4. **Regulatory and Compliance Attributes**:
   - *Legal Compliance*: Full adherence to LGPD, GDPR, PCI DSS, and BCB/BACEN regulations.
   - *Non-Repudiation*: Legally valid digital signatures.

---

## 🔁 The SABSA Lifecycle

1. **Strategy & Planning**:
   - Mapping of business objectives and system boundaries.
   - Initial construction of the Contextual layer.
2. **Design**:
   - Definition of the Conceptual, Logical, Physical, and Component Matrices.
   - Creation of Security Domains and the Attribute Profile (BAP).
3. **Implement**:
   - Provisioning of secure infrastructure (IaC), defensive code, and AppSec/Pentesting tests.
4. **Manage & Measure**:
   - Continuous security operations (SecOps), log monitoring, incident response, and measurement of KPIs/KRIs.
