# ASVS Level 2 Audit Checklist (Corporate Standard)

Use this quick checklist to audit backend repositories and projects.

| ASVS Domain | Audited Control | Evidence / Inspected File | Status |
| :--- | :--- | :--- | :--- |
| **V2 Authentication** | Password hashing with Argon2id or bcrypt | `src/auth/password_hasher.py` | Compliant |
| **V4 Authorization** | Tenancy and object ownership validation | `src/controllers/patient_controller.py` | Compliant |
| **V5 Validation** | Schema validation via Pydantic / DTOs | `src/schemas/request_schemas.py` | Compliant |
| **V6 Cryptography** | Keys read from KMS via an injected variable | `infra/terraform/kms.tf` | Compliant |
| **V7 Logs** | Regex filter for masking CPF and passwords | `src/utils/logger.py` | Compliant |
| **V9 Communication** | TLS 1.3 enforced on NGINX / Gateway | `infra/k8s/ingress.yaml` | Compliant |
| **V13 APIs** | Rate limiting active per IP / Token | `infra/gateway/kong.yaml` | Compliant |
