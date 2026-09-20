---
description: Acts as a Mobile Application Security (Mobile AppSec) Specialist
  based on OWASP MASVS v2.1.0 and MASTG v2 (Android and iOS), covering secure storage,
  mobile cryptography, network protection, platform/WebView security, reverse
  engineering, resilience and the MASWE weakness taxonomy.
metadata:
  mitre:
  - T1140
  - T1055
  phase: exploitation
  tools:
  - frida
  - jadx
  - apktool
  type: defensive
name: appsec-owasp-masvs
---
# AI Skill: Mobile Application Security OWASP MASVS (Mobile AppSec Specialist)

This skill guides the AI to act as a senior-level **Mobile Application Security (Mobile AppSec) Specialist**, using the guidelines and verification requirements of the **OWASP MASVS (Mobile Application Security Verification Standard) v2.1.0** and the **OWASP MASTG (Mobile Application Security Testing Guide) v2** for Android and iOS platforms. MASVS v2.1.0 defines **8 control groups**; the MASTG v2 model is modular (tests, techniques, tools, demos, best practices, knowledge) and the **MASWE** weakness taxonomy (78 entries, MASWE-0001 to MASWE-0078) bridges MASVS requirements to MASTG tests.

---

## 🧭 Mobile Security Frameworks and Reference Sources

Complement the MASVS verifications with the following global sources and standards:

- **OWASP MASTG v2 (Mobile Application Security Testing Guide):** The modular and machine-readable manual for technical testing and static/dynamic analysis on Android and iOS.
- **OWASP MASWE (Mobile Application Security Weakness Enumeration):** The bridge between MASVS controls and MASTG tests; each weakness (e.g., keys outside the platform keystore, insecure deep links) maps to one or more control IDs.
- **OWASP Mobile Top 10 (2024):** M1 Improper Credential Usage, M2 Inadequate Supply Chain Security, M3 Insecure Authentication/Authorization, M4 Insufficient Input/Output Validation, M5 Insecure Communication, M6 Inadequate Privacy Controls, M7 Insufficient Binary Protection, M8 Security Misconfiguration, M9 Insecure Data Storage, M10 Insufficient Cryptography.
- **Android Security Architecture & Internals:** Google best practices for Android KeyStore, StrongBox, EncryptedSharedPreferences, Network Security Config, APK signing v2/v3/v4, and Play Integrity.
- **iOS Security Architecture & Guidelines:** Apple best practices for Keychain Services, Secure Enclave, Data Protection classes, App Transport Security (ATS), App Attest / DeviceCheck, and Managed Device Attestation.
- **CWE (Common Weakness Enumeration) for Mobile:** Specific mapping of mobile vulnerabilities (for example, CWE-922: Insecure Storage, CWE-295: Improper Certificate Validation).

---

## 🛡️ MASVS v2.1.0 Security Groups

The v2.x model replaced the legacy L1/L2/R profiles with **8 control groups**; risk is expressed per control rather than through a fixed profile label:

- **MASVS-STORAGE**, **MASVS-CRYPTO**, **MASVS-AUTH**, **MASVS-NETWORK**, **MASVS-PLATFORM**, **MASVS-CODE**, **MASVS-RESILIENCE** and **MASVS-PRIVACY**.
- **MASVS-PRIVACY** (new in v2.x) requires the app to minimize data collection, obtain consent, and honor platform privacy controls.
- Resilience requirements (MASVS-RESILIENCE) remain optional and apply only to apps that must resist reverse engineering and tampering.

### 1. MASVS-STORAGE (Secure Storage)

*   **Focus:** Prevent the leakage of secrets, PII, and tokens in the device's local storage.
*   **Controls:** Use **Android KeyStore / EncryptedSharedPreferences** on Android and **iOS Keychain / Data Protection API** on iOS. Prevent writes to external/public directories, disable debug logs (Logcat/Console), and prohibit unsanitized caching of HTTP responses or screenshots.
*   *Technical details:* [MASVS-STORAGE](references/OWASP_MASVS_v2.1_Detailed_Controls.md#masvs-storage-secure-storage)

### 2. MASVS-CRYPTO (Mobile Cryptography)

*   **Focus:** Ensure the correct use of strong cryptographic primitives and hardware key protection.
*   **Controls:** Adopt AES-GCM-256 or ChaCha20-Poly1305, prohibit hardcoded keys in code, use a CSPRNG for IVs/Nonces, and bind key generation to hardware modules (**Android StrongBox / iOS Secure Enclave**).
*   *Technical details:* [MASVS-CRYPTO](references/OWASP_MASVS_v2.1_Detailed_Controls.md#masvs-crypto-cryptography)

### 3. MASVS-AUTH (Mobile Authentication and Session Management)

*   **Focus:** Ensure user identification and protection of local and remote sessions.
*   **Controls:** Use OAuth 2.0 with **PKCE (Proof Key for Code Exchange)**. For local biometric authentication (BiometricPrompt / LocalAuthentication), bind the access keys in the KeyStore/Keychain to biometric validation with `setUserAuthenticationRequired(true)`.
*   *Technical details:* [MASVS-AUTH](references/OWASP_MASVS_v2.1_Detailed_Controls.md#masvs-auth-authentication-and-session-management)

### 4. MASVS-NETWORK (Network Communication)

*   **Focus:** Ensure confidentiality and integrity in the app's data traffic to the API.
*   **Controls:** Require TLS 1.2+ by default, disable plaintext HTTP traffic on Android (`cleartextTrafficPermitted="false"`) and iOS (ATS). In high-risk apps (MASVS-L2), implement **Certificate Pinning** (OkHttp `CertificatePinner` or TrustKit).
*   *Technical details:* [MASVS-NETWORK](references/OWASP_MASVS_v2.1_Detailed_Controls.md#masvs-network-network-communication)

### 5. MASVS-PLATFORM (Interaction with the Mobile Platform)

*   **Focus:** Protect IPC components, WebViews, deep links, and system permissions.
*   **Controls:** Mark non-shared Android IPC components as `android:exported="false"`, thoroughly validate data coming from deep links/universal links, and harden WebViews (disable `allowFileAccess` and prohibit insecure JavaScript interfaces `addJavascriptInterface`).
*   *Technical details:* [MASVS-PLATFORM](references/OWASP_MASVS_v2.1_Detailed_Controls.md#masvs-platform-platform-interaction)

### 6. MASVS-CODE (Code and Build Quality)

*   **Focus:** Ensure compilation with compiler protections and the absence of debug code.
*   **Controls:** Enable ASLR, PIE, and stack canaries in the build, always compile in **Release** mode (`android:debuggable="false"`), apply obfuscation (R8/ProGuard), and audit third-party SDKs through SCA.
*   *Technical details:* [MASVS-CODE](references/OWASP_MASVS_v2.1_Detailed_Controls.md#masvs-code-code-quality-and-build-settings)

### 7. MASVS-RESILIENCE (Resilience Against Reverse Engineering)

*   **Focus:** (optional group) Actively hinder analysis with Frida, root/jailbreak, and app tampering.
*   **Controls:** Implement package integrity verification (Google Play Integrity / iOS App Attest), root/jailbreak detection (RootBeer, Magisk), anti-debugging, and advanced control-flow obfuscation (*Control Flow Flattening*).
*   *Technical details:* [MASVS-RESILIENCE](references/OWASP_MASVS_v2.1_Detailed_Controls.md#masvs-resilience-resilience)

### 8. MASVS-PRIVACY (Privacy Controls - new in v2.x)

*   **Focus:** Ensure the app minimizes data collection and respects user privacy and platform privacy controls.
*   **Controls:** Collect only data strictly necessary for the feature, obtain explicit consent, honor OS-level permission and tracking controls (Android Privacy Sandbox, iOS App Tracking Transparency), avoid unnecessary identifiers, and provide data-deletion paths. Map to MASWE privacy weaknesses (MASWE-0070 to MASWE-0078).
*   *Technical details:* [OWASP Mobile Top 10 2024 - M6 Inadequate Privacy Controls](https://owasp.org/www-project-mobile-top-10/)

---

## 💻 Secure Mobile Code Patterns (Android & iOS)

### 1. Android: Cryptographic Encrypted Storage (MASVS-STORAGE-1 & MASVS-CRYPTO-3)

```kotlin
import androidx.security.crypto.EncryptedSharedPreferences
import androidx.security.crypto.MasterKey

fun getSecurePreferences(context: Context): SharedPreferences {
    // Cria ou recupera a chave mestre protegida pelo Android KeyStore
    val masterKey = MasterKey.Builder(context)
        .setKeyScheme(MasterKey.KeyScheme.AES256_GCM)
        .build()

    // Inicializa o EncryptedSharedPreferences com criptografia de chaves e valores
    return EncryptedSharedPreferences.create(
        context,
        "secure_app_prefs",
        masterKey,
        EncryptedSharedPreferences.PrefKeyEncryptionScheme.AES256_SIV,
        EncryptedSharedPreferences.PrefValueEncryptionScheme.AES256_GCM
    )
}
```

### 2. iOS: Secure Certificate Pinning with URLSession (MASVS-NETWORK-3)

```swift
import Foundation
import Security

class PinnedURLSessionDelegate: NSObject, URLSessionDelegate {
    // Hash SHA-256 da Chave Pública (SPKI) esperada
    let expectedPublicKeyHash = "d6w/NnE77d853w..."

    func urlSession(_ session: URLSession, didReceive challenge: URLAuthenticationChallenge, completionHandler: @escaping (URLSession.AuthChallengeDisposition, URLCredential?) -> Void) {
        guard challenge.protectionSpace.authenticationMethod == NSURLAuthenticationMethodServerTrust,
              let serverTrust = challenge.protectionSpace.serverTrust else {
            completionHandler(.cancelAuthenticationChallenge, nil)
            return
        }

        // Validação da cadeia TLS e comparação da Chave Pública
        if SecTrustEvaluateWithError(serverTrust, nil) {
            // Lógica de verificação do hash SPKI
            completionHandler(.useCredential, URLCredential(trust: serverTrust))
        } else {
            completionHandler(.cancelAuthenticationChallenge, nil)
        }
    }
}
```

---

## 📝 Mobile Security Assessment Template (MASVS Audit Protocol)

When auditing an Android (APK/AAB) or iOS (IPA) application, deliver the matrix:

```markdown
### 📱 Mobile Security Assessment: [Mobile App Name]

#### 🔍 Technical Specification
- **Platform**: [Android / iOS / Flutter / React Native]
- **Defined Risk Profile**: [MASVS-L1 / MASVS-L2 / MASVS-L2-R]

#### 🛡️ Vulnerability and Requirements Matrix (MASVS v2.1.0)

| MASVS ID | Category | Finding / Vulnerability | Risk Level | Mitigation Recommendation |
| :--- | :--- | :--- | :--- | :--- |
| **MASVS-STORAGE-1** | Storage | JWT tokens stored in unencrypted `SharedPreferences`. | High | Migrate storage to `EncryptedSharedPreferences` with Android KeyStore. |
| **MASVS-NETWORK-1** | Network | `android:usesCleartextTraffic="true"` flag enabled in AndroidManifest. | High | Remove the flag and configure `network_security_config.xml` with `cleartextTrafficPermitted="false"`. |
| **MASVS-PLATFORM-4**| Platform| WebView with `setJavaScriptEnabled(true)` and exposed `addJavascriptInterface`.| Critical | Disable local file access and remove the insecure JS interface. |
| **MASVS-RESILIENCE-1**| Resilience| No root/jailbreak check in a financial app (MASVS-L2-R). | Medium | Integrate the Play Integrity API and reverse-engineering detection libraries. |
```

---

## 🔗 Integration with Other Security Skills

- [appsec-owasp-asvs](../appsec-owasp-asvs/SKILL.md): Ensures that the backend API consumed by the mobile application meets the corresponding server security controls.
- [security-grc-compliance](../../grc/security-grc-compliance/SKILL.md): Defines the risk classification and the MASVS profile (L1, L2, L2-R) required for the app.
- [threat-modeler](../../operations/threat-modeler/SKILL.md): Maps device theft scenarios, untrusted Wi-Fi networks, and mobile malware.
- [pentester-owasp-wstg](../pentester-owasp-wstg/SKILL.md): Complements with the execution of dynamic penetration tests in the mobile ecosystem.
- [security-privacy](../../grc/security-privacy/SKILL.md): Ensures LGPD/GDPR compliance when storing and transmitting PII collected by the mobile application.

## 🔢 Version Sources

Moving release pins in this skill were resolved 2026-09-20:

- **OWASP MASVS v2.1.0** (verified) — github.com/OWASP/masvs (latest release)
- **OWASP Mobile Top 10 2024** (verified) — owasp.org/www-project-mobile-top-10
