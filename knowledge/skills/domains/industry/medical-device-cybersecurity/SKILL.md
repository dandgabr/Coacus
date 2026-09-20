---
name: medical-device-cybersecurity
description: Acts as a Medical Device Cybersecurity specialist covering FDA §524B premarket requirements, the FDA February 2026 guidance, SBOM/CBOM for devices, postmarket vulnerability management, legacy-device risk and the safety impact of medical device compromise.
metadata:
  type: defensive
  phase: report
---

# Medical Device Cybersecurity

This skill guides the AI to secure medical devices across their lifecycle, where a cybersecurity failure is a patient-safety event.

---

## 📜 1. Regulatory Framework

- **FD&C Act §524B**: premarket cybersecurity requirements for "cyber devices" - a plan to monitor, identify and address vulnerabilities and exploits, including coordinated vulnerability disclosure.
- **FDA guidance (February 2026)** on cybersecurity in premarket submissions supersedes earlier versions; align submissions with its quality-management and content expectations.
- **Postmarket**: monitoring, vulnerability intake, patching and coordinated disclosure continue for the device's supported life.
- **SBOM/CBOM**: a software and component inventory is expected as part of the submission and the ongoing program.

---

## 🏥 2. Risk Context

- **Safety impact first**: a compromised infusion pump, ventilator or imaging device can physically harm a patient; risk scoring must include clinical impact, not only data confidentiality.
- **Legacy devices**: deployed for years, often unpatchable; manage with compensating controls (network segmentation, monitoring) and a documented risk decision.
- **Third-party components and RTOS**: many device vulnerabilities arrive through the real-time OS, protocol stacks (for example, URGENT/11 or SweynTooth-class issues) and libraries such as Log4j.

---

## 🛡️ 3. Controls

1. **Secure the design**: authentication, encryption, secure boot and signed updates from the start; no hardcoded credentials.
2. **Segment** clinical networks from enterprise IT; med-tech devices should not be reachable from the general network.
3. **Inventory** devices and their software; you cannot patch what you do not know.
4. **Monitor** for anomalous device behavior and unexpected network traffic.
5. **Patch or isolate** on a risk- and clinician-informed schedule.
6. **Disclose** vulnerabilities through a coordinated process and keep the SBOM current.

---

## 🔗 4. Integration with Other Skills

- For the interoperability and PHI standards (HL7/FHIR/DICOM, HIPAA), see the [healthtech-standards-security](../../../domains/industry/healthtech-standards-security/SKILL.md) skill.
- For the embedded/firmware layer, see the [hardware-hacking-embedded-security](../../../domains/industry/hardware-hacking-embedded-security/SKILL.md) skill.
- For SBOM tooling, see the [program-sbom-tooling](../../../security/tooling/program-sbom-tooling/SKILL.md) skill.
- For network segmentation, see the [network-segmentation-microsegmentation](../../../security/operations/network-segmentation-microsegmentation/SKILL.md) skill.
