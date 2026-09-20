# Privacy Impact Assessment Example (DPIA / RIPD)

Summary of a privacy assessment for a new telemedicine and medical-report feature.

| Assessed Item | Technical Analysis | Residual Risk | Mitigating Control |
| :--- | :--- | :--- | :--- |
| **Facial Biometrics Collection** | Used to validate the physician's identity when signing the medical report | MEDIUM | Storage of a biometric vector hash (template), with no persistence of the original photo to disk |
| **Consultation Video Streaming** | Peer-to-peer WebRTC traffic | LOW | End-to-end DTLS/SRTP encryption with no recording on intermediary servers |
| **Medical Record Storage** | Sensitive health data (LGPD Art. 11) | LOW | AES-256 column encryption in the database + per-tenant database segregation |
| **Audit Logs** | Record of attendant accesses | LOW | Anonymization of the patient's CPF in the log, keeping only a pseudonymized ID |
