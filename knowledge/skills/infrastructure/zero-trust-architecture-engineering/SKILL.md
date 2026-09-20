---
name: zero-trust-architecture-engineering
description: Acts as a specialist in Zero Trust Network Architecture and Engineering based on NIST SP 800-207/207A and the work of Razi Rais, Christina Morillo, and Evan Gilman. Covers the Never Trust Always Verify tenets, Policy Engine/Administrator/Enforcement Point, CISA Zero Trust Maturity Model v2.0, network microsegmentation, continuous authentication, strong workload identity (SPIFFE/SPIRE and IETF WIMSE), ZTNA (Zero Trust Network Access), Policy-as-Code, and end-to-end mTLS encryption.
---

# Zero Trust Network Architecture and Engineering (ZTNA)

This skill establishes the principles of **Zero Trust** architecture, moving beyond the traditional perimeter-security model built on walls and adopting the fundamental principle: *"Never trust, always verify continuously"*. It is grounded in **NIST SP 800-207** (Zero Trust Architecture), **NIST SP 800-207A** (cloud-native multi-cloud ZTA), and the **CISA Zero Trust Maturity Model v2.0**.

---

## 🛡️ 1. The 5 Pillars of Zero Trust

1. **Strong Identity for Users and Devices**: Continuous authentication with phishing-resistant MFA (Passkeys/FIDO2) and device security posture verification (Device Health Attestation).
2. **Workload Identity (SPIFFE/SPIRE)**: Every application, pod, or microservice holds an ephemeral X.509 cryptographic certificate (SVID) for mutual identification over mTLS.
3. **Dynamic Microsegmentation**: Granular Pod-to-Pod and VM-to-VM network policies that forbid unauthorized lateral movement.
4. **Principle of Least Privilege (PoLP / Just-in-Time Access)**: Temporary access granted with a strictly necessary scope.
5. **Telemetry and Continuous Analysis**: Real-time monitoring of behavioral deviations and traffic anomalies.

---

## 🧭 2. NIST SP 800-207: Logical Components and Tenets

Zero Trust is enforced by three logical components that operate per session and per request:

```
+-----------------------------------------------------------------------------+
| POLICY ENGINE (PE) - the decision brain                                     |
| - Evaluates every request against enterprise policy, identity, device      |
|   posture, threat intel and continuous analytics. Outputs grant/deny.       |
+-----------------------------------------------------------------------------+
                                   |
                                   v
+-----------------------------------------------------------------------------+
| POLICY ADMINISTRATOR (PA) - the control plane                               |
| - Translates the PE decision into the session-specific configuration and    |
|   instructs the PEP; manages credential/token issuance and revocation.      |
+-----------------------------------------------------------------------------+
                                   |
                                   v
+-----------------------------------------------------------------------------+
| POLICY ENFORCEMENT POINT (PEP) - the data plane                             |
| - Inline component (proxy, gateway, sidecar, agent) that actually allows    |
|   or blocks the connection to the resource.                                 |
+-----------------------------------------------------------------------------+
```

The **7 NIST tenets**: all data sources and services are resources; all communication is secured regardless of network location; access is granted per-session; access policy is dynamic and computed from identity, device and context; the enterprise monitors and measures integrity/security posture continuously; authentication and authorization are strictly enforced before access; and telemetry is collected to improve policy.

---

## ☁️ 3. NIST SP 800-207A: Cloud-Native, Multi-Cloud ZTA

For cloud-native environments the architecture maps onto ingress/egress gateways, sidecars and service mesh, with two explicit policy tiers:

- **Identity-tier policy**: enforced on workload identity (SPIFFE ID / SVID), independent of network address.
- **Network-tier policy**: enforced on the overlay network (L3–L7), used when identity cannot be established or as defense in depth.

Multi-cloud deployments require a common identity fabric, consistent policy semantics across providers, and a single decision plane (PE/PA) even when PEPs are provider-specific.

---

## 📈 4. CISA Zero Trust Maturity Model v2.0

The federal reference organizes maturity across **5 pillars** (Identity, Devices, Networks, Applications & Workloads, Data) plus **3 cross-cutting capabilities** (Visibility & Analytics, Automation & Orchestration, Governance), each with **4 stages**: *Traditional → Initial → Advanced → Optimal*. Use the model as a gap-assessment instrument, not as a binary certification.

---

## 🪪 5. Workload Identity: SPIFFE/SPIRE and IETF WIMSE

- **SPIFFE**: defines the SPIFFE ID and short-lived **SVIDs** (X.509, JWT, and WIT-SVID), trust domains and bundles, and the Workload API / Broker API; **SPIRE** is the production implementation, including federation and OIDC federation.
- **IETF WIMSE** (Workload Identity in Multi-System Environments): defines the architecture and a JOSE-based workload token for chained HTTP/REST calls, local token issuance and token exchange (RFC 8693), closing the SPIFFE/OAuth/JWT interop gap and modeling trust-boundary crossings.
- **Non-human identity (NHI) governance**: replace static CI/CD secrets with OIDC federation and short-lived credentials; inventory, scope and rotate machine identities as first-class assets.

---

## 🧱 6. Policy-as-Code and Segmentation Mechanics

- **Policy-as-Code**: express access policy in OPA/Gatekeeper (Rego), Kyverno (CEL), Cilium network policies, or cloud policy engines; version it, test it and review it like application code.
- **Continuous verification**: verify artifact and workload identity with Sigstore/Cosign and SPIFFE/SPIRE at admission and at runtime.
- **ZTNA vs VPN**: ZTNA replaces the flat, network-level trust of a VPN with per-application, identity-and-context-aware access brokered by an outbound-only connector; the resource is never exposed to the public internet.
- **Microsegmentation**: default-deny, L3–L7 policy, identity-aware proxies, and no implicit east-west trust; validate that policy actually blocks lateral movement rather than merely documenting it.
- **Maturity path**: (1) identity and MFA basics, (2) device posture and least privilege, (3) dynamic policy and segmentation, (4) continuous verification and automation.

---

## 🔗 Integration with Other Skills

- To enrich policy decisions with adversary behavior mapping, see the [threat-modeler](../../security/operations/threat-modeler/SKILL.md) skill.
- To implement identity controls and federation across providers, see the [iam-access-management](../../security/iam/iam-access-management/SKILL.md) skill.
- To harden the network components that host the PEPs, see the [network-security-onprem-cloud](../../security/operations/network-security-onprem-cloud/SKILL.md) skill.
- To engineer the workload identity certificates and mTLS, see the [cryptography-pqc-standards](../../security/crypto/cryptography-pqc-standards/SKILL.md) skill.
- For the SABSA/TOGAF strategic view of trust domains, see the [security-architect-sabsa](../../security/operations/security-architect-sabsa/SKILL.md) skill.
