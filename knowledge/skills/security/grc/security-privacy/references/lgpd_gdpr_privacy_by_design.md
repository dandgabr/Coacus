# Privacy Engineering and LGPD / GDPR Guide

For Brazilian software reviews, use `lgpd-privacy-engineering` to verify the
current law, identify applicable obligations and document the evidence.

## 1. Classification of Personal Data (LGPD Art. 5 and Art. 11)

- **Common Personal Data (Art. 5, I)**: Name, CPF, email, phone number, IP address, device identifier.
- **Sensitive Personal Data (Art. 5, II and Art. 11)**: Health data, medical records, genetic data, biometrics, sexual orientation, religious conviction. These require additional security measures and restricted legal bases.

## 2. Main Legal Bases in Architecture
- **Consent**: Requires a record of unequivocal acceptance and an endpoint for easy withdrawal.
- **Performance of a Contract**: Data strictly necessary to provide the contracted service.
- **Health Protection**: Exclusive to health professionals and health services in medical procedures.
- **Compliance with a legal or regulatory obligation** applies only within the specific record class, provider role and retention rule. Under the [Marco Civil](https://www.planalto.gov.br/ccivil_03/_ato2011-2014/2014/lei/l12965.htm) (resolved 2026-11-27), Article 13 addresses connection records and Article 15 addresses qualifying application-access records. Verify other retention rules against the applicable authority.
