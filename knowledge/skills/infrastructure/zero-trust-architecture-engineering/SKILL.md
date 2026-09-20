---
name: zero-trust-architecture-engineering
description: Acts as a specialist in Zero Trust Network Architecture and Engineering based on the work of Razi Rais, Christina Morillo, and Evan Gilman. Covers the Never Trust, Always Verify pillars, network microsegmentation, continuous authentication, strong workload identity (SPIFFE/SPIRE), ZTNA (Zero Trust Network Access), adaptive access control, and end-to-end mTLS encryption.
---

# Zero Trust Network Architecture and Engineering (ZTNA)

This skill establishes the principles of **Zero Trust** architecture, moving beyond the traditional perimeter-security model built on walls and adopting the fundamental principle: *"Never trust, always verify continuously"*.

---

## 🛡️ 1. The 5 Pillars of Zero Trust

1. **Strong Identity for Users and Devices**: Continuous authentication with phishing-resistant MFA (Passkeys/FIDO2) and device security posture verification (Device Health Attestation).
2. **Workload Identity (SPIFFE/SPIRE)**: Every application, pod, or microservice holds an ephemeral X.509 cryptographic certificate (SVID) for mutual identification over mTLS.
3. **Dynamic Microsegmentation**: Granular Pod-to-Pod and VM-to-VM network policies that forbid unauthorized lateral movement.
4. **Principle of Least Privilege (PoLP / Just-in-Time Access)**: Temporary access granted with a strictly necessary scope.
5. **Telemetry and Continuous Analysis**: Real-time monitoring of behavioral deviations and traffic anomalies.
