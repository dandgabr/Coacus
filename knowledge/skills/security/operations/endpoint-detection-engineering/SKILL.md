---
name: endpoint-detection-engineering
description: Acts as an Endpoint Detection Engineering specialist covering Windows Sysmon configuration, Sigma rule authoring and conversion, YARA, osquery and Velociraptor fleet hunting, ETW and eBPF telemetry pipelines.
metadata:
  type: defensive
  phase: actions
---

# Endpoint Detection Engineering

This skill guides the AI to build the endpoint telemetry and detection layer that a SOC relies on.

---

## 🔭 1. Telemetry Sources

- **Sysmon** (Windows): the de-facto endpoint schema - process creation with hashes, network connections, image loads, remote thread creation, process access (LSASS), registry and file events, WMI events, DNS queries and process tampering.
- **ETW / ETW-TI**: kernel and provider-level events, including threat-intelligence events used by EDR products.
- **Linux**: auditd, eBPF-based tracing (for example, Tetragon) and process accounting.
- **macOS**: the Endpoint Security framework is the supported kernel-adjacent telemetry path.
- **Fleet tooling**: osquery exposes the OS as queryable tables; Velociraptor collects artifacts at scale with VQL.

---

## 📝 2. Detection-as-Data

- Author in **Sigma** (vendor-neutral YAML) and convert to the SIEM query language; this keeps detections portable across platforms.
- Use the `logsource` contract (category, product, service) so the rule declares which telemetry it needs.
- Include `falsepositives`, `level` and a mapping to the ATT&CK technique.
- Keep rules version-controlled and tested against known-good and known-bad samples.

---

## 🔍 3. High-Value Endpoint Detections

- Process injection chains: allocate remote memory, write, then create a remote thread in a foreign process.
- Credential access: process access to LSASS, SAM hive reads, DPAPI use.
- Persistence: new services, scheduled tasks, WMI subscriptions, registry Run keys, systemd units and launch agents.
- LOLBins: signed system binaries used to download or execute (see the ATT&CK T1218 family and the LOLBAS catalogue).
- Defense impairment: security tooling stopped, logs cleared, ETW or AMSI tampering.

---

## ⚙️ 4. Operations

1. Deploy a tuned Sysmon configuration; the default is too noisy and too shallow.
2. Ship telemetry to the SIEM with a consistent schema and time source.
3. Tune continuously; measure false-positive rate per rule.
4. Validate coverage with Atomic Red Team or MITRE CAR analytics.
5. Feed detections to the SOC playbooks.

---

## 🔗 5. Integration with Other Skills

- For the EDR and evasion context, see the [edr-evasion-endpoint-security](../../platform/edr-evasion-endpoint-security/SKILL.md) skill.
- For SIEM/SOC operations, see the [detection-engineering](../../operations/detection-engineering/SKILL.md) skill.
- For YARA/Sigma depth, see the [detection-engineering-yara-sigma](../../operations/detection-engineering-yara-sigma/SKILL.md) skill.
- For endpoint forensics, see the [endpoint-forensics](../../operations/endpoint-forensics/SKILL.md) skill.
