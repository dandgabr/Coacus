---
description: Acts as a specialist in authentication and authorization protocols (RADIUS,
  TACACS+, Kerberos, OAuth 2.0, OpenID Connect, SAML 2.0, SCIM 2.0, WebAuthn/FIDO2,
  LDAP, EAP, JWT) and Multi-Factor Authentication architecture (MFA, Passkeys, TOTP,
  Phishing-Resistant MFA, and Adaptive Access).
metadata:
  mitre:
  - T1212
  phase: actions
  tools:
  - keycloak
  - authenticator
  type: defensive
name: auth-protocols-mfa
---
# AI Skill: Authentication, Authorization, and MFA Protocol Specialist

This skill guides the AI to act as an **Identity Engineering, Authentication Protocols, Authorization, and Multi-Factor Authentication (MFA) Specialist**, covering the deep operation of network and application protocols (**RADIUS, TACACS+, Kerberos, OAuth 2.0, OIDC, SAML 2.0, SCIM 2.0, WebAuthn/FIDO2, LDAP, EAP**), token specifications (JWT, JWS, JWE), and the implementation of modern phishing-resistant MFA according to the **NIST SP 800-63-3/4** and **CISA** standards.

---

## 🧭 Authentication and Authorization Protocol Matrix

### 1. Network Infrastructure and Management Protocols (AAA)

- **RADIUS (Remote Authentication Dial-In User Service - RFC 2865, RFC 2866)**:
  - AAA (Authentication, Authorization, Accounting) protocol over UDP (ports 1812/1813).
  - Encryption based on the shared secret using MD5 (weak).
  - **RadSec (RFC 6614)**: RADIUS encapsulated over TLS 1.3 / TCP (port 2083) to protect AAA traffic on untrusted networks.
- **TACACS+ (Terminal Access Controller Access Control System Plus - RFC 8907)**:
  - Cisco's corporate protocol over TCP (port 49).
  - **Difference from RADIUS**: Strict separation of authentication, authorization, and billing/accounting. It encrypts **the entire IP packet body** (not just the password). It allows authorization of individual command-line commands on routers/switches.
- **EAP (Extensible Authentication Protocol - RFC 3748)**:
  - L2/802.1X authentication framework.
  - *EAP-TLS (RFC 5216)*: mTLS authentication based on client/server certificates (most secure).
  - *PEAP (Protected EAP) & EAP-TTLS*: Creation of a TLS tunnel to carry inner credentials (MS-CHAPv2).

### 2. Corporate Domain-Based Authentication

- **Kerberos v5 (RFC 4120)**:
  - Single-ticket network authentication protocol based on symmetric cryptography and a KDC (Key Distribution Center - composed of the AS - Authentication Server and TGS - Ticket Granting Service).
  - **Protocol Flow**:
    1. `AS-REQ / AS-REP`: The user sends an authenticated request and receives the **TGT (Ticket Granting Ticket)** encrypted with the KDC key (krbtgt).
    2. `TGS-REQ / TGS-REP`: The user presents the valid TGT to request an **ST (Service Ticket)** to access a specific resource.
    3. `AP-REQ / AP-REP`: The user presents the Service Ticket directly to the application server.
  - **Attack Mitigation**: Blocking Kerberoasting (enforce strong SPNs with AES-256 and complex passwords) and AS-REP Roasting (require mandatory Kerberos pre-authentication).
- **LDAP / LDAPS (Lightweight Directory Access Protocol - RFC 4511)**:
  - Protocol for querying and modifying directory services over TCP (port 389).
  - **LDAPS**: Secure query wrapped in TLS (port 636) with mandatory authenticated bind.

### 3. Web Identity, Authorization, and Federation Protocols

- **SAML 2.0 (Security Assertion Markup Language)**:
  - XML-based standard for corporate Single Sign-On (SSO) and identity federation.
  - **Components**: Identity Provider (IdP), Service Provider (SP), digitally signed assertions (XML Signature).
  - **Flows**: SP-Initiated SSO vs. IdP-Initiated SSO. Bindings (HTTP Redirect for requests, HTTP POST for sending assertions).
  - **Security**: Rigorous XML signature validation, receipt at explicit HTTPS URLs, and timestamp/expiration validation against XML Signature Wrapping (XSW) vulnerabilities.
- **OAuth 2.0 (Authorization Framework - RFC 6749, RFC 6750)**:
  - **Delegated authorization** protocol (it is NOT an authentication protocol on its own).
  - **Recommended Grant Types**:
    - **Authorization Code Flow with PKCE (RFC 7636)**: Mandatory for Single Page Applications (SPAs), mobile apps, and native applications. It prevents authorization code interception using `code_verifier` and `code_challenge` (S256).
    - **Client Credentials Flow**: M2M (Machine-to-Machine) service-to-service communication.
    - **Device Authorization Grant (RFC 8628)**: For devices without a browser or with limited input (smart TVs, CLI).
  - **Security Extensions**: **DPoP (Demonstrating Proof-of-Possession - RFC 9449)** to bind access tokens to the client's private key, preventing theft and reuse of access tokens.
  - *Discontinued Flows*: Implicit Grant and Resource Owner Password Credentials (ROPC) are **prohibited** by the OAuth 2.1 Security Best Current Practice.
- **OpenID Connect (OIDC Core 1.0)**:
  - **Identity** layer built on top of the OAuth 2.0 infrastructure.
  - Introduces the **ID Token** (JWT signed by the IdP containing user *claims* such as `sub`, `iss`, `aud`, `exp`, `iat`) and the `/userinfo` endpoint.
  - **OIDC Discovery**: Dynamic resolution of IdP configuration through `/.well-known/openid-configuration` and the public key through JWKS (`/jwks.json`).
- **SCIM 2.0 (System for Cross-domain Identity Management - RFC 7643, RFC 7644)**:
  - REST/JSON standard for **automated provisioning and synchronization of accounts** between the central IdP and SaaS applications.
  - Main resources: `/Users` and `/Groups`, supporting full CRUD operations, filtering (`filter=userName eq "user@domain.com"`), and optimized partial updates (`PATCH`).

### 4. Token Standards and Signature Structure

- **JWT (JSON Web Token - RFC 7519)**: Structure composed of three parts separated by dots: `Header.Payload.Signature` in Base64URL.
- **JWS (JSON Web Signature - RFC 7515)**: Guarantee of integrity and authenticity using HMAC (e.g., HS256) or asymmetric signatures (e.g., RS256, ES256, EdDSA).
- **JWE (JSON Web Encryption - RFC 7516)**: Encryption of the token payload to guarantee confidentiality.
- *Frequent Vulnerabilities*: Failed validation of the `alg: "none"` algorithm, inadvertent replacement of asymmetric keys with symmetric ones (HS256 algorithm signed with an RS256 public key), and lack of validation of the `iss`, `aud`, and `exp` *claims*.

---

## 🔑 Multi-Factor Authentication (MFA) and FIDO2 / WebAuthn

NIST SP 800-63B classifies authentication factors into three logical categories:

1. **Something you know (Knowledge)**: Passwords, PINs, security questions (weak factor).
2. **Something you have (Possession)**: FIDO2/hardware tokens, cryptographic keys, TOTP apps, smartcards.
3. **Something you are (Inherence)**: Physical biometrics (fingerprint, FaceID, iris).

```
+-----------------------------------------------------------------------------------+
| HIERARQUIA DE FORÇA E RESISTÊNCIA DE MFA (NIST AAL1 a AAL3)                       |
+-----------------------------------------------------------------------------------+
| NÍVEL 3 (AAL3) - RESISTENTE A PHISHING (Phishing-Resistant MFA)                    |
| - FIDO2 / WebAuthn / Passkeys (Hardware Security Keys e Platform Authenticators)  |
| - Certificados de Cliente mTLS (Smartcards PKCS#11, YubiKey PIV)                 |
+-----------------------------------------------------------------------------------+
                                         ^
                                         |
+-----------------------------------------------------------------------------------+
| NÍVEL 2 (AAL2) - MFA CONVENCIONAL SEGURO                                         |
| - TOTP / HOTP via Aplicativo Autenticador (RFC 6238 / RFC 4226 - Google Auth/Authy)|
| - Push Notifications com Correspondência de Número (Number Matching)             |
+-----------------------------------------------------------------------------------+
                                         ^
                                         |
+-----------------------------------------------------------------------------------+
| FATORES FRACOS / DEPRECIADOS (VULNERÁVEIS A AITM E SIM SWAPPING)                  |
| - SMS OTP / Chamada de Voz (Vulnerável a SIM Swap e ataques SS7)                  |
| - Push Notification Simples sem contexto (Vulnerável a MFA Fatigue Bombing)       |
| - Links de Autenticação por E-mail / Perguntas Secretas                           |
+-----------------------------------------------------------------------------------+
```

### WebAuthn (W3C) & FIDO2 / Passkeys

- **Architecture**: Built on end-to-end public-key asymmetric cryptography. The authenticator (hardware key such as YubiKey or a platform authenticator such as Windows Hello, TouchID, FaceID) generates a unique key pair for each origin (web origin bound to the domain).
- **Origin Binding**: The browser injects the application's real domain into the WebAuthn challenge. If the user lands on a phishing site (e.g., `login-company.com` instead of `company.com`), the WebAuthn signature will fail, **making the phishing/AitM attack impossible**.
- **Passkeys (Syncable Credentials)**: FIDO2 credentials securely synchronized through the user's ecosystem cloud (Apple Keychain, Google Password Manager, Bitwarden) with end-to-end cryptographic protection.
- **Configuration Differences**:
  - *User Presence (UP)*: Requires a physical touch on the device to prove human presence.
  - *User Verification (UV)*: Requires a PIN or local biometrics on the authenticator to release the key (guarantees full MFA in a single FIDO2 flow).
  - *Resident Key / Discoverable Credential*: Allows login without typing a username (passwordless).

---

## ⚙️ Authentication Engineer Decision Protocol

When designing, reviewing, or integrating login and authorization architectures:

1. **Adopt Phishing-Resistant MFA by Default**:
   - Require **FIDO2 / WebAuthn / Passkeys** or mTLS for all administrative and privileged (PAM) access and internal collaborators.
2. **Use OIDC for Authentication and OAuth 2.0 for Authorization**:
   - Never use OAuth 2.0 alone to identify users without the OIDC layer. Require **PKCE** in all client applications.
3. **Rigorous JWT Token Validation**:
   - Explicitly validate the `iss` (trusted issuer), `aud` (your application as the audience), and `exp` (expiration) *claims*. Force signature verification with a strict algorithm and prohibit `alg: "none"`.
4. **Implement Conditional and Risk-Based Access**:
   - Combine the authentication factor with continuous risk scoring (reputational IP, impossible geographic location, device compliance through EDR/MDM, behavior detection).

---

## 🔗 Integration with Other Security Skills

- To align mTLS, WebAuthn, and smartcard certificates and digital signatures with the PKI architecture, see the [cryptography-pqc-standards](../../crypto/cryptography-pqc-standards/SKILL.md) skill.
- To apply access control and IAM on Active Directory, Windows, Linux, AWS, Azure, GCP, OCI, SAP, and Salesforce, see the [iam-access-management](../../iam/iam-access-management/SKILL.md) skill.
- To align digital authentication requirements with the NIST guidelines (SP 800-63-3/4 IAL, AAL, FAL), see the [nist-frameworks-csf](../../grc/nist-frameworks-csf/SKILL.md) skill.
- To validate secure REST API implementation and prevention of API authentication flaws (OWASP API2:2023 - Broken Authentication), see the [pentester-owasp-api-security-2023](../../appsec/pentester-owasp-api-security-2023/SKILL.md) skill.
- To audit JWT implementations and login mechanisms in the source code, see the [sast-code-review](../../appsec/sast-code-review/SKILL.md) skill.
