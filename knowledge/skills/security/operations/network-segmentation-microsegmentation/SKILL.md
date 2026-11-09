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

## 🧯 6b. Macro-Segmenting an Untrusted Device (asymmetric policy)

The most common macro-segmentation task is containing a device you cannot trust
(consumer IoT, camera, printer, an EOL appliance) while still letting the owner
reach it.

- **Dedicated segment**: put the device on its own VLAN/SSID/subnet, never on the
  user LAN. Bind a **separate SSID to that VLAN** so wireless devices join the
  untrusted segment by association.
- **Asymmetric policy**: allow `trusted -> untrusted`, and **deny
  `untrusted -> trusted` initiation**. A **stateful** firewall keeps the reply
  traffic of allowed sessions flowing (state `Established`), while a device-initiated
  connection matches state `New` and is denied. Express this as a default-deny,
  stateful policy (NIST SP 800-41 Rev. 1); in IEC 62443-3-3 terms it is FR 5
  "Restricted data flow" (SR 5.1/SR 5.2) on the conduit between the two zones.
- **Enforcement point matters**: a gateway ACL only inspects traffic that *traverses*
  the gateway; same-VLAN device-to-device traffic needs a switch ACL or port/AP
  client isolation.
- **Isolation is mitigation, not remediation**: it bounds who can reach the device;
  the vulnerability remains and the segment usually keeps internet access. Pair it
  with minimal exposed ports, disabled unused services and egress control.
- **Egress is a second boundary**: cloud/P2P relays traverse NAT with no port
  forwarding, so LAN isolation does not remove vendor-cloud reachability; decide
  egress separately.

## ⚠️ 6c. Re-segmentation Gotchas (VLAN and DHCP)

- **Moving an SSID/port to another VLAN orphans clients that keep their DHCP
  lease.** Association and IP state are independent; a client renews only at T1
  (half the lease) and per RFC 2131 (§3.2) may keep the old-subnet address for the
  rest of the lease — associated, but with no L3 path. **Force re-association**
  (kick/deauth or toggle Wi-Fi); if the client re-requests the stale address, clear
  the server-side lease in the wrong pool and reconnect again (`release`/`renew` or a
  reboot also work). Do it outside business hours; as hygiene, shorten the lease
  before the change.
- **A DHCP reservation is scoped to a subnet *and* an identity (MAC or client-id).**
  A reservation in the wrong subnet is **inert** and the client gets a dynamic lease
  from the correct pool; randomized client MACs silently break MAC-keyed
  reservations.
- **Reservations are per-host; "blocks" are not a reservation feature.** Use an
  **exclusion range** or a **DHCP policy/class** (vendor class, OUI, relay) to give a
  class of devices its own range — addressing hygiene, not a security boundary.
- **Rule order is load-bearing**: a broad allow placed above the isolation deny
  silently kills it; put the block first. An "internet-only" segment needs two rules
  (deny other VLANs *and* deny the gateway management page).
- **Asymmetric routing breaks stateful inspection**: keep both directions through the
  same gateway or replies are dropped as unsolicited.

## ✅ 6d. Verification (bidirectional, layered)

- Test by **layer**: L2 (neighbor/ARP), L3 (reachability) and service (the exact TCP
  port responds).
- Test **both directions**: assert the allowed flow *and* issue the disallowed flow
  from **inside the untrusted segment**, asserting a deny — rather than inferring
  safety from the absence of observed traffic. IEC 62443-3-3 SR 3.3 makes proving
  that the security function operates part of the requirement set; CISA's
  microsegmentation planning guidance treats validation as a precondition to
  deployment.

## 🖥️ 6e. Automating Vendor Controllers

- Prefer the controller's **Open API / CLI** over GUI automation. Omada exposes an
  Open API; UniFi a Network Integration API; pfSense's REST API is a third-party
  package.
- Controller GUIs are data-driven SPAs: DOM handles go stale on re-render, some
  controls are custom, and editing one field can clear others. When scripting the UI,
  re-locate the element each iteration (stable locators, no cached reference) and
  **read state back after every action** instead of trusting the panel.

## 🔗 7. Integration with Other Skills

- For the broader network controls, see the [network-security-onprem-cloud](../network-security-onprem-cloud/SKILL.md) skill.
- For the zero-trust architecture, see the [zero-trust-architecture-engineering](../../../infrastructure/zero-trust-architecture-engineering/SKILL.md) skill.
- For the end-to-end isolation of a specific untrusted consumer/IoT device, see the [iot-untrusted-device-isolation](../iot-untrusted-device-isolation/SKILL.md) skill.
- For Kubernetes hardening, see the [kubernetes-security-posture](../kubernetes-security-posture/SKILL.md) skill.

## 🔢 Version Sources

Moving release pins in this skill were resolved 2026-09-20:

- **OWASP Kubernetes Top 10 2025** (verified) — owasp.org/www-project-kubernetes-top-ten

Segmentation references re-resolved 2026-10-13:

- **NSA/CISA AA23-278A — Top Ten Cybersecurity Misconfigurations** (2023-10-05) — cisa.gov/news-events/cybersecurity-advisories/aa23-278a
- **NSA — Segment Networks and Deploy Application-Aware Defenses** (2019-09) — media.defense.gov
- **NIST SP 800-41 Rev. 1 — Guidelines on Firewalls and Firewall Policy** (final) — csrc.nist.gov/pubs/sp/800/41/r1/final
- **IEC 62443-3-3:2013** (FR 5 Restricted data flow) — webstore.iec.ch/en/publication/7033
- **RFC 2131 — Dynamic Host Configuration Protocol** (DHCP lease/renewal behavior) — rfc-editor.org/rfc/rfc2131.html
