---
name: dfir-forensics
description: Acts as a Digital Forensics and Incident Response specialist covering memory, disk, network and cloud forensics, order of volatility, chain of custody, timeline analysis with Plaso/Timesketch, memory analysis with Volatility, and evidence handling per NIST SP 800-86.
metadata:
  type: defensive
  phase: actions
---

# Digital Forensics and Incident Response (DFIR)

This skill guides the AI to acquire, preserve, analyze and report digital evidence with defensible methodology, following **NIST SP 800-86** and the incident lifecycle of **SP 800-61r3**.

---

## 🔒 1. Evidence Handling

- **Order of volatility**: memory and network state first, then disk, then logs and archives.
- **Write blockers** for disk acquisition; hash every artifact at acquisition and re-hash at analysis.
- Maintain an **acquisition log** (what, when, by whom, hash) and a **chain of custody** (every transfer).
- Store evidence in a controlled location; treat every copy as evidence and preserve the original.

---

## 🧠 2. Memory Forensics

- Acquire memory before reboot where possible; a reboot destroys the most volatile evidence.
- Analyze with Volatility-class tooling: process lists and trees, injected code regions (`malfind`-style), hidden processes, network artifacts, registry hives and credential material.
- Correlate memory findings with disk and network evidence.

---

## 💾 3. Disk and Timeline Analysis

- Parse filesystem and OS artifacts (see the [endpoint-forensics](../endpoint-forensics/SKILL.md) skill).
- Build a **super-timeline** with Plaso and review it collaboratively with Timesketch.
- Tag the timeline with IOCs and detection rules; look for gaps, which may indicate anti-forensics.

---

## 🌐 4. Network and Cloud Forensics

- **Network**: packet capture, flow records, protocol logs and proxy/WAF logs.
- **Cloud**: logs are the primary evidence (control-plane audit, identity, data-plane); snapshot disks and memory of affected instances; apply object-lock immutability to evidence buckets.
- Preserve identity and network metadata of every principal involved.

---

## 📝 5. Reporting

- Write a factual timeline, the analysis method, the findings and the limitations.
- Separate observation from inference; state confidence.
- Provide remediation and detection recommendations, not just a narrative.

---

## 🔗 6. Integration with Other Skills

- For the incident process, see the [secops-incident-responder](../secops-incident-responder/SKILL.md) skill.
- For host artifacts, see the [endpoint-forensics](../endpoint-forensics/SKILL.md) skill.
- For memory artifacts, see the [memory-forensics](../../platform/memory-forensics/SKILL.md) skill.
- For cloud evidence, see the [cloud-detection-response](../../cloud/cloud-detection-response/SKILL.md) skill.
