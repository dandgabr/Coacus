---
name: network-segmentation-microsegmentation
description: Acts as a Network Segmentation specialist covering macro-segmentation (VLAN, VRF, firewall zones), microsegmentation (host, identity and label based), overlay networks (VXLAN), Kubernetes NetworkPolicy and the zero-trust policy tiers of NIST SP 800-207A.
metadata:
  type: defensive
  phase: actions
---

# Network Segmentation and Microsegmentation

This skill guides the AI to design segmentation that actually prevents lateral movement, rather than drawing zones on a diagram that traffic ignores.

---

## 🧱 1. Macro-Segmentation

- **VLAN/VRF** separate broadcast domains and routing tables; **firewall zones** mediate between them.
- Design around **data sensitivity and function**, not org chart.
- The IT/OT boundary (the industrial DMZ) is a specialized macro-segment; see the [ot-ics-security](../ot-ics-security/SKILL.md) skill.
- Verify with traffic analysis: a segment that is not enforced is decoration.

---

## 🧬 2. Microsegmentation

- **Host/agent-based**: a local firewall policy on each workload, independent of the network.
- **Identity/label-based**: policy expressed over workload identity or tags (for example, Kubernetes labels) rather than IP addresses.
- **Service-mesh based**: mTLS plus policy at the sidecar, enforced per service identity.
- **Default deny**: the baseline rule is deny; access is explicitly granted.
- Microsegmentation is the implementation of the zero-trust "assume breach" principle at the network layer.

---

## 🌐 3. Overlay Networks (VXLAN)

- VXLAN encapsulates L2 frames over L3, enabling segmentation across a routed underlay.
- An overlay is **not** a security boundary by itself: the underlay and the VTEP endpoints must be trusted and hardened, and overlay traffic must still be policy-filtered.
- Segmenting with an overlay does not encrypt; add IPsec/MACsec if confidentiality is required.

---

## ☸️ 4. Kubernetes NetworkPolicy

- Default-deny ingress and egress per namespace, then allow explicitly.
- Note that NetworkPolicy requires a CNI that enforces it; the API object alone does nothing on a CNI that ignores it.
- Block egress to the instance metadata endpoint (169.254.169.254) to prevent cluster-to-cloud lateral movement (OWASP K8s Top 10 2025, K08).

---

## 📐 5. Zero Trust Policy Tiers (NIST SP 800-207A)

- **Identity-tier policy** is enforced on workload identity and is preferred.
- **Network-tier policy** is enforced on the overlay and is used when identity is unavailable or as defense in depth.
- Both tiers should express the same intent so a failure in one does not silently widen access.

---

## ✅ 6. Validation

1. Enumerate expected flows (a flow matrix per segment).
2. Test that everything else is denied - not just that the expected flows work.
3. Re-test after every change; segmentation decays without verification.

---

## 🔗 7. Integration with Other Skills

- For the broader network controls, see the [network-security-onprem-cloud](../network-security-onprem-cloud/SKILL.md) skill.
- For the zero-trust architecture, see the [zero-trust-architecture-engineering](../../../infrastructure/zero-trust-architecture-engineering/SKILL.md) skill.
- For Kubernetes hardening, see the [kubernetes-security-posture](../kubernetes-security-posture/SKILL.md) skill.
