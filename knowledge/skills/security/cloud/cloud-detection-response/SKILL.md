---
name: cloud-detection-response
description: Acts as a Cloud Detection and Response specialist covering cloud-native threat detection (GuardDuty, Defender for Cloud, Security Command Center, Cloud Guard), control-plane vs data-plane telemetry, cloud forensics, and automated response in multi-cloud environments.
metadata:
  type: defensive
  phase: actions
---

# Cloud Detection and Response

This skill guides the AI to detect and respond to attacks that live in the cloud control plane, where there is no disk to acquire and the evidence is in audit logs.

---

## 🔭 1. Telemetry Sources

- **Control plane**: audit logs (CloudTrail, Azure Activity Log, GCP Audit Logs, OCI Audit) - who changed what.
- **Data plane**: VPC flow logs, WAF logs, load-balancer logs, database audit logs.
- **Workload**: runtime process/file/network telemetry from CWPP agents.
- **Identity**: sign-in logs, token issuance, role activation.
- **Native detectors**: guard services that flag anomalous API calls, credential abuse and crypto-mining.

Ship all of it to a central SIEM; a cloud account whose logs are not centralized is flying blind.

---

## 🚨 2. High-Signal Cloud Detections

- New access key created for a long-lived principal, or key used from a new geography.
- IAM policy attached that grants `*` or privilege-escalation actions.
- Security-group or firewall rule opened to 0.0.0.0/0 on a management port.
- Storage made public or a bucket policy changed.
- Logging disabled or a trail deleted (defense impairment).
- Instance metadata queried from an unusual source.
- Role chained across accounts from an unexpected principal.

---

## 🧪 3. Cloud Forensics

- Cloud evidence is **log-first**: preserve and snapshot logs before they rotate out.
- Snapshot the disk and memory of the affected instance for offline analysis.
- Capture the identity and network metadata of the compromised principal.
- Maintain an evidence chain in object storage with immutability (object lock) to prevent tampering.

---

## ⚡ 4. Automated Response

- Isolate the instance (security-group quarantine) and revoke credentials automatically on high-confidence detections.
- Disable a compromised access key and force re-authentication.
- Snapshot before remediation so evidence is not lost.
- Escalate to the human IR process for anything ambiguous; automation should contain, not adjudicate.

---

## 🔗 5. Integration with Other Skills

- For posture management, see the [cloud-security-posture-cnapp](../cloud-security-posture-cnapp/SKILL.md) skill.
- For the incident process, see the [secops-incident-responder](../../operations/secops-incident-responder/SKILL.md) skill.
- For detection authoring, see the [detection-engineering](../../operations/detection-engineering/SKILL.md) skill.
- For forensics, see the [dfir-forensics](../../operations/dfir-forensics/SKILL.md) skill.
