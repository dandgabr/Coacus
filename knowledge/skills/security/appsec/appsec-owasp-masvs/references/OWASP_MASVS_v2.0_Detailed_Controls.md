# OWASP MASVS v2.0.0 Detailed Verification Requirements

This document serves as the technical security reference database for audits, penetration tests, and code reviews of mobile applications (Android and iOS). Every control below maps to the 7 categories of **OWASP MASVS (Mobile Application Security Verification Standard) v2.0.0**, integrated with the **MASTG (Mobile Application Security Testing Guide)**.

---

## 📊 MASVS v2.0.0 Security Profiles

- **MASVS-L1 (Standard Security):** Essential security requirements applicable to every mobile application. Focused on protection against common attacks and data leaks.
- **MASVS-L2 (Defense-in-Depth / High Security):** Advanced requirements for mobile applications that handle highly sensitive data (fintechs, banks, healthcare, digital identity).
- **MASVS-R (Resilience Against Reverse Engineering and Tampering):** Resilience requirements against reverse engineering, dynamic analysis, and tampering (root/jailbreak, hooking with Frida, deobfuscation). Combined as **MASVS-L1-R** or **MASVS-L2-R**.

---

## MASVS-STORAGE: Secure Storage (Armazenamento Seguro)
*Objective:* Ensure that sensitive data, credentials, and keys stored on the mobile device are protected against unauthorized access by other applications, malware, or physical memory extraction.

- **MASVS-STORAGE-1:** Store credentials, access tokens, and confidential data strictly in secure storage containers managed by the operating system (**Android Keystore / EncryptedSharedPreferences** on Android; **iOS Keychain / Data Protection API** on iOS).
- **MASVS-STORAGE-2:** Prevent the exposure of sensitive data in development logs, system debug messages (Logcat/Console), or third-party crash reports (Crashlytics, Sentry).
- **MASVS-STORAGE-3:** Prevent sensitive data leaks through temporary storage, HTTP response caches, autofill records (Autofill), application screenshots, or clipboard copies (Clipboard).
- **MASVS-STORAGE-4:** Do not store sensitive data in the device's external/public storage (such as shared SD Card directories) where other apps have read permission.

---

## MASVS-CRYPTO: Cryptography (Criptografia Móvel)
*Objective:* Ensure that cryptographic operations in the app follow modern industry standards and use secure keys protected by hardware.

- **MASVS-CRYPTO-1:** Use exclusively strong, industry-standard cryptographic primitives and algorithms (for example, AES-GCM-256, ChaCha20-Poly1305, RSA-2048+, ECDSA P-256), avoiding obsolete algorithms (DES, RC4, MD5, SHA1).
- **MASVS-CRYPTO-2:** Prohibit the use of static cryptographic keys hardcoded in the app source code (*hardcoded keys*), in property files, or in compiled native libraries (`.so` / `.dylib`).
- **MASVS-CRYPTO-3:** Generate cryptographic keys using cryptographically secure pseudo-random number generators (CSPRNG) and ensure the keys are protected by hardware modules (**Android KeyStore / Secure Element / StrongBox**; **iOS Secure Enclave**).
- **MASVS-CRYPTO-4:** Ensure that IVs (Initialization Vectors) and nonces are unique for each encryption operation and generated using a CSPRNG.

---

## MASVS-AUTH: Authentication and Session Management (Autenticação e Sessão)
*Objective:* Ensure robust verification of local user identities and the management of remote sessions through mobile APIs.

- **MASVS-AUTH-1:** Implement secure remote authentication using modern token-based protocols (OAuth 2.0 with **PKCE – Proof Key for Code Exchange** and OpenID Connect).
- **MASVS-AUTH-2:** When using local biometrics (Fingerprint, FaceID, TouchID), require the system's official API (**Android BiometricPrompt**; **iOS LocalAuthentication**) and bind the KeyStore/Keychain key to the requirement for biometric authentication (`setUserAuthenticationRequired(true)`).
- **MASVS-AUTH-3:** Invalidate session tokens both locally and remotely on logout, and enforce idle and absolute session expiry limits.
- **MASVS-AUTH-4:** Ensure the application adequately handles the invalidation of biometric keys when the user enrolls new fingerprints or faces in the operating system.

---

## MASVS-NETWORK: Network Communication (Comunicação de Rede)
*Objective:* Ensure the confidentiality and integrity of all data transmitted over the network between the mobile app and backend services.

- **MASVS-NETWORK-1:** Encrypt all network traffic using TLS 1.2 or TLS 1.3 by default. Explicitly disable plaintext HTTP traffic in the system configuration file (**Android Network Security Configuration** `cleartextTrafficPermitted="false"`; **iOS App Transport Security – ATS**).
- **MASVS-NETWORK-2:** Strictly validate the TLS certificate chain and host name, and disable any option that accepts self-signed certificates or disables verification in production.
- **MASVS-NETWORK-3:** In high-risk applications (MASVS-L2), implement **Certificate Pinning** (pinning of certificates/public keys) using native OS mechanisms or well-established libraries (OkHttp `CertificatePinner`, TrustKit) to prevent Man-in-the-Middle (MitM) attacks via a malicious CA on the device.

---

## MASVS-PLATFORM: Platform Interaction (Interação com a Plataforma)
*Objective:* Protect the application against attack vectors based on Inter-Process Communication (IPC) mechanisms, WebViews, and system permissions.

- **MASVS-PLATFORM-1:** Request only the system permissions strictly necessary (*Principle of Least Privilege*) and validate permission grants at runtime.
- **MASVS-PLATFORM-2:** Protect IPC components exposed on Android (Activities, Services, Broadcast Receivers, Content Providers) by marking them `android:exported="false"` unless they are explicitly intended for access by other apps.
- **MASVS-PLATFORM-3:** Strictly validate all data inputs received via IPC, Intents, Deep Links, and Universal Links before processing them or forwarding them to the backend.
- **MASVS-PLATFORM-4:** Harden the **WebView** configuration: disable local file support (`setAllowFileAccess(false)`), disable cross-origin access, and do not expose insecure JavaScript interfaces (`addJavascriptInterface`) without strict annotations and restrictions.

---

## MASVS-CODE: Code Quality and Build Settings (Qualidade de Código e Build)
*Objective:* Ensure the application is compiled with all system protections active and without debug artifacts or symbols.

- **MASVS-CODE-1:** Compile the application with the system's compiler protections enabled (ASLR, PIE, Stack Canaries, ARC on iOS).
- **MASVS-CODE-2:** Ensure the final compiled code is produced in **Release** mode without active debug flags (`android:debuggable="false"` on Android; a `Release` build on iOS).
- **MASVS-CODE-3:** Remove test code, development backdoors, debug logs, and unused code from the final distribution package.
- **MASVS-CODE-4:** Keep all third-party dependencies (Android SDKs, iOS Pods, Swift Packages) up to date and check for known vulnerabilities through software composition analysis (SCA).

---

## MASVS-RESILIENCE: Resilience (Resiliência contra Engenharia Reversa e Adulteração)
*Objective:* (Required for the **MASVS-R / MASVS-L2-R** profile) Actively hinder dynamic analysis, reverse engineering, the use of hooking frameworks, and tampering with the mobile application.

- **MASVS-RESILIENCE-1 (Root / Jailbreak Detection):** Detect whether the application is running in an unprotected environment with active root/jailbreak access (Android Magisk, RootBeer; iOS Cydia, ElleKit) and react safely by terminating execution or restricting functionality.
- **MASVS-RESILIENCE-2 (Anti-Debugging & Dynamic Analysis):** Implement mechanisms to detect and prevent the attachment of debuggers (ptrace, lldb) and dynamic instrumentation frameworks (**Frida**, Xposed, Substrate).
- **MASVS-RESILIENCE-3 (Integrity & Anti-Tampering):** Verify the integrity of the source code and the digital signature of the APK/IPA (for example, **Google Play Integrity API**; **iOS App Attest / DeviceCheck**) to detect unauthorized modifications or *re-signing* of the package.
- **MASVS-RESILIENCE-4 (Obfuscation):** Apply advanced code obfuscation techniques (R8/ProGuard, DexGuard, OLLVM) to encrypt sensitive strings, rename identifiers, and flatten control flow (*Control Flow Flattening*).
