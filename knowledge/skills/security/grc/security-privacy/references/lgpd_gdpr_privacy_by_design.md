# Privacy Engineering and LGPD / GDPR Guide

Regulatory requirements for software architecture compliant with the LGPD (Brazilian General Data Protection Law, Law 13.709/2018).

## 1. Classification of Personal Data (LGPD Art. 5 and Art. 11)

- **Common Personal Data (Art. 5, I)**: Name, CPF, email, phone number, IP address, device identifier.
- **Sensitive Personal Data (Art. 5, II and Art. 11)**: Health data, medical records, genetic data, biometrics, sexual orientation, religious conviction. These require additional security measures and restricted legal bases.

## 2. Main Legal Bases in Architecture
- **Consent**: Requires a record of unequivocal acceptance and an endpoint for easy withdrawal.
- **Performance of a Contract**: Data strictly necessary to provide the contracted service.
- **Health Protection**: Exclusive to health professionals and health services in medical procedures.
- **Compliance with a Legal / Regulatory Obligation**: For example, retention of connection logs for 6 months (Brazilian Civil Rights Framework for the Internet) or medical records for 20 years (CFM).
