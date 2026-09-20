---
description: Acts as a Mobile Application Security (Mobile AppSec) Specialist
  based on OWASP MASVS v2.0.0 and MASTG (Android and iOS), covering secure storage,
  mobile cryptography, network protection, platform/WebView security, reverse
  engineering, and resilience.
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

This skill guides the AI to act as a senior-level **Mobile Application Security (Mobile AppSec) Specialist**, using the guidelines and verification requirements of the **OWASP MASVS (Mobile Application Security Verification Standard) v2.0.0** and the **OWASP MASTG (Mobile Application Security Testing Guide)** for Android and iOS platforms.

---

## 🧭 Mobile Security Frameworks and Reference Sources

Complement the MASVS verifications with the following global sources and standards:

- **OWASP MASTG (Mobile Application Security Testing Guide):** The manual for technical testing and static/dynamic analysis on Android and iOS.
- **Android Security Architecture & Internals:** Google best practices for Android KeyStore, EncryptedSharedPreferences, Network Security Config, and Play Integrity.
- **iOS Security Architecture & Guidelines:** Apple best practices for Keychain Services, Secure Enclave, App Transport Security (ATS), and App Attest / DeviceCheck.
- **CWE (Common Weakness Enumeration) for Mobile:** Specific mapping of mobile vulnerabilities (for example, CWE-922: Insecure Storage, CWE-295: Improper Certificate Validation).

---

## 🛡️ MASVS v2.0.0 Security Levels and Profiles

Identify the appropriate security profile for the mobile application based on its business risk level:

* **MASVS-L1 (Standard Security):** Essential requirements applicable to **any mobile application**. Ensures clean data storage, secure TLS communication, and the absence of common code bugs.
* **MASVS-L2 (Defense-in-Depth / High Security):** **(Recommended for fintechs, banks, healthcare, and corporate apps)** Requires advanced data protection, certificate pinning, mandatory use of a hardware-protected Keystore/Keychain, and strict authentication.
* **MASVS-R (Resilience Against Reverse Engineering & Tampering):** Active defense requirements against dynamic analysis with Frida, reverse engineering, root/jailbreak bypass, and application tampering. Combined as **MASVS-L1-R** or **MASVS-L2-R**.

---

## 📌 The 7 Categories of OWASP MASVS v2.0.0

When auditing mobile code or designing Android and iOS applications, apply the detailed controls in the 7 categories described below.

> [!NOTE]
> For the detailed list of technical subcontrols and CWE mapping, see the document [OWASP MASVS v2.0.0 Detailed Controls](references/OWASP_MASVS_v2.0_Detailed_Controls.md).

### 1. MASVS-STORAGE (Secure Storage)

*   **Focus:** Prevent the leakage of secrets, PII, and tokens in the device's local storage.
*   **Controls:** Use **Android KeyStore / EncryptedSharedPreferences** on Android and **iOS Keychain / Data Protection API** on iOS. Prevent writes to external/public directories, disable debug logs (Logcat/Console), and prohibit unsanitized caching of HTTP responses or screenshots.
*   *Technical details:* [MASVS-STORAGE](references/OWASP_MASVS_v2.0_Detailed_Controls.md#masvs-storage-secure-storage-armazenamento-seguro)

### 2. MASVS-CRYPTO (Mobile Cryptography)

*   **Focus:** Ensure the correct use of strong cryptographic primitives and hardware key protection.
*   **Controls:** Adopt AES-GCM-256 or ChaCha20-Poly1305, prohibit hardcoded keys in code, use a CSPRNG for IVs/Nonces, and bind key generation to hardware modules (**Android StrongBox / iOS Secure Enclave**).
*   *Technical details:* [MASVS-CRYPTO](references/OWASP_MASVS_v2.0_Detailed_Controls.md#masvs-crypto-cryptography-criptografia-móvel)

### 3. MASVS-AUTH (Mobile Authentication and Session Management)

*   **Focus:** Ensure user identification and protection of local and remote sessions.
*   **Controls:** Use OAuth 2.0 with **PKCE (Proof Key for Code Exchange)**. For local biometric authentication (BiometricPrompt / LocalAuthentication), bind the access keys in the KeyStore/Keychain to biometric validation with `setUserAuthenticationRequired(true)`.
*   *Technical details:* [MASVS-AUTH](references/OWASP_MASVS_v2.0_Detailed_Controls.md#masvs-auth-authentication-and-session-management-autenticação-e-sessão)

### 4. MASVS-NETWORK (Network Communication)

*   **Focus:** Ensure confidentiality and integrity in the app's data traffic to the API.
*   **Controls:** Require TLS 1.2+ by default, disable plaintext HTTP traffic on Android (`cleartextTrafficPermitted="false"`) and iOS (ATS). In high-risk apps (MASVS-L2), implement **Certificate Pinning** (OkHttp `CertificatePinner` or TrustKit).
*   *Technical details:* [MASVS-NETWORK](references/OWASP_MASVS_v2.0_Detailed_Controls.md#masvs-network-network-communication-comunicação-de-rede)

### 5. MASVS-PLATFORM (Interaction with the Mobile Platform)

*   **Focus:** Protect IPC components, WebViews, deep links, and system permissions.
*   **Controls:** Mark non-shared Android IPC components as `android:exported="false"`, thoroughly validate data coming from deep links/universal links, and harden WebViews (disable `allowFileAccess` and prohibit insecure JavaScript interfaces `addJavascriptInterface`).
*   *Technical details:* [MASVS-PLATFORM](references/OWASP_MASVS_v2.0_Detailed_Controls.md#masvs-platform-platform-interaction-interação-com-a-plataforma)

### 6. MASVS-CODE (Code and Build Quality)

*   **Focus:** Ensure compilation with compiler protections and the absence of debug code.
*   **Controls:** Enable ASLR, PIE, and stack canaries in the build, always compile in **Release** mode (`android:debuggable="false"`), apply obfuscation (R8/ProGuard), and audit third-party SDKs through SCA.
*   *Technical details:* [MASVS-CODE](references/OWASP_MASVS_v2.0_Detailed_Controls.md#masvs-code-code-quality-and-build-settings-qualidade-de-código-e-build)

### 7. MASVS-RESILIENCE (Resilience Against Reverse Engineering)

*   **Focus:** (MASVS-R / MASVS-L2-R profile) Actively hinder analysis with Frida, root/jailbreak, and app tampering.
*   **Controls:** Implement package integrity verification (Google Play Integrity / iOS App Attest), root/jailbreak detection (RootBeer, Magisk), anti-debugging, and advanced control-flow obfuscation (*Control Flow Flattening*).
*   *Technical details:* [MASVS-RESILIENCE](references/OWASP_MASVS_v2.0_Detailed_Controls.md#masvs-resilience-resilience-resiliência-contra-engenharia-reversa-e-adulteração)

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

#### 🛡️ Vulnerability and Requirements Matrix (MASVS v2.0.0)

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
