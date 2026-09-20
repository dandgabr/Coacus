---
name: ids-ips-ndr-engineering
description: Acts as a Detection Engineering specialist for IDS/IPS and Network Detection and Response, covering Suricata/Snort rule authoring, Zeek behavioral logging, beaconing and DNS-tunneling detection, PCAP workflows, eBPF runtime enforcement, and lateral-movement detection mapped to MITRE ATT&CK.
metadata:
  type: defensive
  phase: actions
---

# IDS/IPS and Network Detection and Response (NDR)

This skill guides the AI to detect malicious network activity - not just to enumerate assets (which the mapping skill covers).

---

## 🧰 1. Sensors and Data

- **Suricata/Snort**: signature engines for IDS (passive) and IPS (inline); support JA3/JA4 TLS fingerprints, protocol parsers and datasets.
- **Zeek**: a behavioral log generator, not a signature engine; produces per-protocol logs (conn, dns, http, ssl, files) for analytics.
- **Full-packet capture**: network sensors capture what flow records cannot; use flow data for breadth and PCAP for depth.
- **eBPF runtime**: kernel-level observation and enforcement (for example, Tetragon) blurs the network/host boundary and sees encrypted east-west traffic.

---

## 🔍 2. Detection Techniques

1. **Beaconing detection**: score connection regularity (interval, jitter, duration, byte symmetry) to surface command-and-control; RITA-style analysis.
2. **DNS tunneling**: detect via query entropy, label length, volume and rare record types.
3. **Lateral movement** (ATT&CK TA0008): correlate SMB/RDP/WinRM/SSH chains, pass-the-hash and pass-the-ticket behavior across hosts.
4. **Protocol anomalies**: unexpected protocol on a port, malformed packets, TLS certificate anomalies.
5. **Egress anomalies**: new external destinations, data volume shifts, DNS to rare domains.

---

## 🛠️ 3. Rule Lifecycle

- Author rules with a stable `sid`, a revision, a threshold and a documented false-positive profile.
- Test rules against known traffic before production; a rule that fires on everything is noise.
- Map each detection to an ATT&CK technique so coverage can be measured and gaps found.
- Tune continuously; alert fatigue destroys a detection program faster than any attacker.

---

## 🚦 4. IPS Considerations

- Run IPS inline only where a false positive will not break the business.
- Use fail-open vs fail-closed deliberately per segment; document the choice.
- Keep the rule set current and measure the performance impact of inline inspection.

---

## 🔗 5. Integration with Other Skills

- For the mapping/observability view, see the [network-flow-discovery](../../../mapping/network-flow-discovery/SKILL.md) skill.
- For the network architecture and segmentation, see the [network-security-onprem-cloud](../network-security-onprem-cloud/SKILL.md) and [network-segmentation-microsegmentation](../network-segmentation-microsegmentation/SKILL.md) skills.
- For detection authoring in Sigma/YARA, see the [detection-engineering-yara-sigma](../detection-engineering-yara-sigma/SKILL.md) skill.
- For the IR process that consumes these alerts, see the [secops-incident-responder](../secops-incident-responder/SKILL.md) skill.
