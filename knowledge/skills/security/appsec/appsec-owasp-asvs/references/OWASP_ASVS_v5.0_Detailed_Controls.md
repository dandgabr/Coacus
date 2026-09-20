# OWASP ASVS v5.0.0 Detailed Verification Requirements

This document serves as the technical security reference database for all audits, code reviews, and architectural proposals. Every control below maps to the 17 categories of **OWASP ASVS v5.0.0**.

> Version resolved 2026-09-20 from github.com/OWASP/ASVS (tag v5.0.0_release).

---

## 📊 ASVS Verification Levels
- **Level 1 (Opportunistic):** Focuses on easily exploitable vulnerabilities. Automatable in CI/CD.
- **Level 2 (Standard):** The recommended baseline for most business applications that process sensitive or personal data (PII).
- **Level 3 (Advanced):** Required for critical high-security systems (for example, critical infrastructure, high-risk financial transactions, medical data).

---

## V1: Encoding and Sanitization (Codificação e Sanitização)
*Objective:* Ensure every data output is properly encoded for its respective context (HTML, JavaScript, SQL, LDAP, and so on) before the destination interprets it.
- **ASVS 1.1.1 (CWE-79):** Contextually encode every user input reflected on web pages (HTML body, attributes, `<script>` tags, and so on) with well-established libraries (for example, OWASP Java Encoder, DOMPurify).
- **ASVS 1.1.2 (CWE-116):** Sanitize strings against parameter injection in system commands and shell scripts using robust escaping APIs.
- **ASVS 1.1.3 (CWE-93):** Validate and sanitize line-break characters (`CRLF`) before writing data to HTTP headers or log files, mitigating HTTP Response Splitting and Log Injection.

---

## V2: Validation and Business Logic (Validação e Lógica de Negócio)
*Objective:* Structurally validate every data input before processing it, and ensure logical flows cannot be bypassed or abused.
- **ASVS 2.1.1 (CWE-20):** Validate all input against strict allow-lists. Define data types, maximum and minimum lengths, and rigid regular expressions.
- **ASVS 2.1.2 (CWE-89):** Use parameterized queries (prepared statements) or ORMs that are secure by default to interact with the database. Never concatenate user data directly into SQL strings.
- **ASVS 2.1.3 (CWE-20):** Validate data on both sides: frontend (usability) and backend (mandatory security).
- **ASVS 2.2.1 (CWE-840):** Ensure logical transactions follow strict steps in the correct order, preventing checkout-step bypass, checkout without payment, and similar abuses.
- **ASVS 2.2.2 (CWE-601):** Prevent open redirects by validating that every destination URL belongs to an allow-list of trusted domains.

---

## V3: Web Frontend Security (Segurança do Frontend Web)
*Objective:* Protect the client against browser-based attacks through strict security policies and headers.
- **ASVS 3.1.1 (CWE-1021):** Implement a strict `Content-Security-Policy (CSP)` to restrict the origin from which scripts and resources may execute (`script-src 'self' 'nonce-...'`).
- **ASVS 3.1.2 (CWE-1021):** Configure anti-clickjacking protection headers (`Frame-Options: DENY` or `SAMEORIGIN`, or the `frame-ancestors` directive in the CSP).
- **ASVS 3.1.3 (CWE-523):** Configure HTTP Strict Transport Security (`HSTS`) headers with an expiry of at least one year (`max-age=31536000; includeSubDomains; preload`).
- **ASVS 3.2.1 (CWE-918):** Restrict frontend script communication (CORS) by allowing only explicit authorized origins instead of the `*` wildcard in authenticated environments.

---

## V4: API and Web Service (APIs e Web Services)
*Objective:* Ensure the integrity, authentication, and rate control of REST, SOAP, and GraphQL API buses or WebSocket channels.
- **ASVS 4.1.1 (CWE-20):** Validate inbound payloads against an explicit JSON/XML schema before processing.
- **ASVS 4.1.2 (CWE-770):** Implement rate limiting per IP and per user token to mitigate application-level denial-of-service (DoS) attacks.
- **ASVS 4.2.1 (CWE-943):** Disable GraphQL query introspection (Introspection Query) in production environments.
- **ASVS 4.2.2 (CWE-285):** Ensure WebSocket requests undergo origin validation (Origin Header Check) and continuous connection authorization.

---

## V5: File Handling (Manipulação de Arquivos)
*Objective:* Protect the server against remote code execution (RCE) and denial of service resulting from uploading or downloading malicious files.
- **ASVS 5.1.1 (CWE-434):** Store files uploaded by users outside the web root and without execution permission at the server/OS level.
- **ASVS 5.1.2 (CWE-434):** Rename files uploaded to the server using secure random name generators (for example, UUIDv4) to prevent overwrites and path traversal.
- **ASVS 5.1.3 (CWE-434):** Validate file types by inspecting the file's magic byte signature (magic numbers/file signatures) instead of relying solely on the extension supplied in the HTTP form.
- **ASVS 5.2.1 (CWE-400):** Limit the maximum upload size to prevent disk overflow and memory exhaustion in the server parser (Zip Bomb, and so on).

---

## V6: Authentication (Autenticação)
*Objective:* Ensure robust user identity verification by managing passwords and MFA with modern practices.
- **ASVS 6.1.1 (CWE-521):** Require passwords with a minimum length of 12 characters (and a maximum of at least 64 characters) without arbitrary complexity rules that hinder the use of password managers.
- **ASVS 6.1.2 (CWE-521):** Validate passwords against lists of known or breached weak passwords, or dictionaries of common terms, during registration and password changes.
- **ASVS 6.2.1 (CWE-307):** Hash passwords with modern algorithms that resist offline GPU attacks and have an adaptive cost: Argon2id (recommended), scrypt, or bcrypt with suitable factors.
- **ASVS 6.3.1 (CWE-308):** Offer and encourage Multifactor Authentication (MFA) based on secure standards, preferably FIDO2/WebAuthn or TOTP generators (RFC 6238), over SMS/email.

---

## V7: Session Management (Gerenciamento de Sessão)
*Objective:* Ensure a secure lifecycle for session tokens and cookies, preventing hijacking or leakage of login state.
- **ASVS 7.1.1 (CWE-613):** Generate session IDs with high entropy using cryptographically secure pseudo-random number generators (CSPRNG) with at least 128 bits of entropy.
- **ASVS 7.1.2 (CWE-613):** Implement idle session timeouts (for example, 15–30 minutes) and absolute session expiry (for example, 24 hours).
- **ASVS 7.2.1 (CWE-1004):** Add the `HttpOnly`, `Secure`, and `SameSite=Lax` (or `SameSite=Strict`) directives to every cookie that carries session identifiers.
- **ASVS 7.2.2 (CWE-384):** Destroy the existing server-side session and issue a new session ID immediately after any privilege-state change (for example, anonymous to authenticated, or two-step authentication just completed).

---

## V8: Authorization (Autorização e Controle de Acesso)
*Objective:* Enforce least privilege and deny by default across all transactions, logical resources, and objects.
- **ASVS 8.1.1 (CWE-276):** Adopt a deny-by-default policy. Every system route and function must require explicit authorization unless it is explicitly marked public.
- **ASVS 8.1.2 (CWE-639):** Mitigate Broken Object Level Authorization (BOLA/IDOR) by validating on every request whether the authenticated user actually has the right to read, update, or delete the corresponding database record.
- **ASVS 8.2.1 (CWE-285):** Centralize access controls in a single service or module within the system architecture to avoid inconsistent ad-hoc implementations.

---

## V9: Self-contained Tokens (Tokens Autocontidos / JWT)
*Objective:* Ensure the integrity, confidentiality, and revocability of digitally signed bearer tokens.
- **ASVS 9.1.1 (CWE-347):** Validate JWT token signatures using secure asymmetric algorithms (RS256, ES256) rather than weak symmetric algorithms, and explicitly reject the `none` algorithm.
- **ASVS 9.1.2 (CWE-613):** Mandatorily set and verify the JWT token's expiration date (`exp`), keeping the token lifetime as short as possible.
- **ASVS 9.2.1 (CWE-287):** Implement a mechanism to revoke or invalidate tokens before their natural expiry on logout or credential reset (for example, by keeping a fast revocation list/blocklist in Redis).

---

## V10: OAuth and OIDC (OAuth e OpenID Connect)
*Objective:* Validate identity-federation and authority-delegation flows between the application and external identity providers.
- **ASVS 10.1.1 (CWE-20):** Strictly validate the redirect URL (`redirect_uri`) against an exact, static list registered with the Identity Provider, preventing redirects to malicious domains.
- **ASVS 10.1.2 (CWE-352):** Use the `state` parameter or the PKCE mechanism (Proof Key for Code Exchange) to prevent Cross-Site Request Forgery (CSRF) attacks and authorization-code theft in OAuth flows.
- **ASVS 10.2.1 (CWE-287):** Verify the ID Token signature and claims (`iss`, `aud`, `exp`, `nonce`) locally or through an introspection endpoint before accepting the user's identity.

---

## V11: Cryptography (Criptografia)
*Objective:* Ensure confidential data is protected with strong cryptography and well-managed keys.
- **ASVS 11.1.1 (CWE-327):** Use robust industry-standard cryptographic algorithms (for example, AES-GCM, ChaCha20-Poly1305) with keys of at least 128 bits (preferably 256 bits).
- **ASVS 11.1.2 (CWE-328):** Disable the use of obsolete, insecure, or broken cryptographic algorithms (for example, DES, 3DES, RC4, MD5, SHA1).
- **ASVS 11.2.1 (CWE-320):** Store cryptographic keys outside the application source code (for example, in AWS KMS, HashiCorp Vault, Azure Key Vault) and ensure secrets are never committed to version-control repositories.
- **ASVS 11.2.2 (CWE-320):** Implement processes and automated mechanisms for the periodic rotation of cryptographic keys.

---

## V12: Secure Communication (Comunicação Segura)
*Objective:* Ensure that all external and internal network channels are protected against traffic interception and eavesdropping.
- **ASVS 12.1.1 (CWE-319):** Encrypt all network communication using TLS 1.2 or TLS 1.3 by default, explicitly disabling older versions of the protocol (SSLv3, TLS 1.0, TLS 1.1).
- **ASVS 12.1.2 (CWE-319):** Configure high-security cipher suites that support Forward Secrecy (for example, ECDHE-RSA-AES256-GCM-SHA384).
- **ASVS 12.2.1 (CWE-295):** Strictly validate TLS certificates on the client side for external connections (for example, microservice HTTP calls), checking the trust chain, expiry, and revocation.

---

## V13: Configuration (Configuração Segura)
*Objective:* Ensure the hardening of the infrastructure and servers on which the application runs.
- **ASVS 13.1.1 (CWE-16):** Disable unused features, services, and ports on production containers and servers.
- **ASVS 13.1.2 (CWE-489):** Disable debug tools and interactive developer consoles in production.
- **ASVS 13.2.1 (CWE-2):** Replace all default and factory credentials of external dependencies (such as databases, queue servers, and cache tools) before the first deploy.

---

## V14: Data Protection (Proteção de Dados e Privacidade)
*Objective:* Ensure confidential user data and PII are stored securely end to end and discarded in line with compliance requirements (LGPD/GDPR).
- **ASVS 14.1.1 (CWE-311):** Encrypt sensitive user data at rest in corporate databases (for example, CPF, email, credit cards, phone numbers) using symmetric encryption with independently managed keys.
- **ASVS 14.1.2 (CWE-538):** Ensure sensitive data is not exposed in the URL (query string) and prevent browser caching of those pages by setting the `Cache-Control: no-store` and `Pragma: no-cache` headers.
- **ASVS 14.2.1 (CWE-244):** Clear RAM buffers that hold confidential data (for example, passwords and decrypted cryptographic keys) as soon as processing finishes, preventing leakage through out-of-bounds read flaws.

---

## V15: Secure Coding and Architecture (Codificação e Arquitetura Seguras)
*Objective:* Ensure the system design supports defense in depth and mitigates the risk of vulnerable third-party dependencies.
- **ASVS 15.1.1 (CWE-1104):** Maintain an up-to-date list of external dependencies (Software Bill of Materials – SBOM) and submit every third-party library package to automated software composition analysis (SCA) scanners in CI/CD to detect and block vulnerable packages.
- **ASVS 15.2.1 (CWE-1008):** Organize the software into isolated, decoupled trust zones, preventing a compromised low-privilege component from gaining immediate access to critical system data.

---

## V16: Security Logging and Error Handling (Logs de Segurança e Tratamento de Erros)
*Objective:* Ensure auditing and early detection of malicious activity without exposing confidential data in log files.
- **ASVS 16.1.1 (CWE-778):** Log significant security events with structured, contextual metadata (JSON log) including: who performed the action (user ID), when (ISO 8601 standard timestamp), what (event/action ID), and the outcome (success or failure).
- **ASVS 16.1.2 (CWE-117):** Ensure log sanitization so that PII (LGPD), plaintext passwords, cryptographic keys, and session tokens are never written.
- **ASVS 16.2.1 (CWE-209):** Handle every system exception and return generic failure messages to end users, storing full stack traces and native errors only in the internal, restricted-access logging system.

---

## V17: WebRTC (Web Real-Time Communication)
*Objective:* Protect real-time peer-to-peer media channels against eavesdropping and unwanted tracking.
- **ASVS 17.1.1 (CWE-200):** Hide users' local IP addresses in WebRTC connections using mDNS for ICE candidate resolution, preventing physical network tracking of the user.
- **ASVS 17.1.2 (CWE-319):** Require robust end-to-end encryption on every WebRTC transmission through the DTLS (Datagram Transport Layer Security) and SRTP (Secure Real-time Transport Protocol) protocols.
- **ASVS 17.2.1 (CWE-285):** Ensure WebRTC signaling servers require prior authentication and authorization before allowing the flow of SDP (Session Description Protocol) messages.
