# Practical Example: Business Attribute Profile (BAP) for a Critical Information System

Applied example of security requirements engineering for a healthcare and clinical-management API ecosystem.

## 1. Structured BAP Table

| SABSA Dimension | Attribute | Business Goal | Metric / SLA | Architectural Control |
| :--- | :--- | :--- | :--- | :--- |
| **Integrity** | Medical Report Immutability | Ensure signed medical reports cannot be altered | 100% of reports validated against a SHA-256 hash on load | ICP-Brasil X.509 signature with append-only storage in S3 Glacier Vault Lock |
| **Confidentiality** | PHI Privacy | Comply with LGPD Art. 11 (Sensitive Data) | Zero medical fields transmitted or stored in cleartext | Encryption at rest via AES-256-GCM + KMS with annual key rotation |
| **Availability** | Emergency Care Continuity | Uninterrupted medical care SLA | Availability >= 99.95% (MTTR < 15 min) | Multi-AZ Kubernetes deployment with replicas and automated failover |
| **Auditability** | Access Traceability | Know who accessed which medical record | 100% of medical-record lookups recorded in a structured log | Gateway interceptor generating logs with Physician ID, CRM, Patient, and Timestamp |
