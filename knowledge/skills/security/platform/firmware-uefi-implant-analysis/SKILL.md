---
name: firmware-uefi-implant-analysis
description: Acts as a Firmware and UEFI Implant specialist covering SPI flash and UEFI module analysis, bootkit and pre-OS persistence (LoJax, MoonBounce, BlackLotus-class), firmware SBOM and integrity verification, and recovery of a compromised boot chain.
metadata:
  type: defensive
  phase: weaponize
---

# Firmware and UEFI Implant Analysis

This skill guides the AI to analyze the layer below the operating system, where implants survive reinstalls and evade host-based defenses.

---

## 🧱 1. Platform Firmware Basics

- **UEFI** replaced legacy BIOS; the firmware initializes hardware and hands control to the bootloader.
- **SPI flash** stores the firmware image, including UEFI modules, NVRAM and often a management engine region.
- **Secure boot** verifies signatures along the chain; a compromised or misconfigured chain defeats it.
- **Firmware resiliency (NIST SP 800-193)**: the platform should protect the image, detect tampering and recover to a known-good image. That recovery capability is the defense against a persistent implant.

---

## 🦠 2. Pre-OS Implants

- **Bootkits** modify the boot process to load before the OS and hide from it.
- **UEFI implants** live as malicious DXE drivers or modified modules, surviving OS reinstalls.
- **SPI implants** rewrite the flash directly.
- Map these to ATT&CK **T1542** (Pre-OS Boot) sub-techniques.

---

## 🔬 3. Analysis Method

1. **Acquire** the firmware image (in-system read, external programmer, or vendor update package).
2. **Compare** the image against the vendor's known-good version; differences are the starting point.
3. **Extract and parse** the UEFI volumes and modules; look for unsigned or unexpected drivers.
4. **Check** NVRAM variables and boot order for tampering.
5. **Verify** secure boot state and firmware version.
6. **Report** with the exact offset, the module and the behavior.

---

## 🛡️ 4. Recovery

- Re-flash from a trusted image or use the platform's recovery mechanism.
- Re-enable secure boot and, where available, firmware attestation.
- Assume the OS was also compromised; reinstall from clean media.

---

## 🛰️ 4b. Embedded / Consumer-Device Backdoor Triage (defensive)

The same "implant below the OS" problem appears in consumer/embedded firmware as
**legal-but-hazardous engineering**, not a named implant. Report it with CWE
vocabulary, not as a deliberate backdoor.

**Indicators to record**
- Hardcoded/static credentials in the filesystem or binary (**CWE-798**), including
  accounts compiled into an executable.
- Undocumented vendor accounts (**CWE-912** Hidden Functionality).
- A serial/UART console that reaches a shell without credentials — physical access is
  then persistent access (extract keys/credentials).
- Unauthenticated management protocols (**CWE-306**): ONVIF, RTSP, UPnP/SSDP,
  telnet/debug ports answering with data instead of `401`.
- Device identity used as an authenticator (MAC/serial -> cloud ID) (**CWE-341/291**).
- Unsigned/unverified boot or update (**CWE-347**) and a plaintext update channel
  (**CWE-311**) that allows update-server impersonation.

**Known classes to recognise (cite the CVE, link CISA/NVD)**
- XiongMai/XMEye/ICSee lineage: ONVIF auth bypass (CVE-2025-65856, CISA
  ICSA-26-113-05), hardcoded plaintext default credentials (CVE-2026-79396),
  unauthenticated credential disclosure (CVE-2018-9995).
- The exploited camera/NVR set is dominated by **missing/improper authentication and
  pre-auth command injection**; check the CISA KEV catalog for the model.

**Response, in order**
1. **Inventory and identify** the OEM lineage (probe the documented fingerprint),
   since the same firmware ships under many brands.
2. **Harden**: replace every default/undocumented credential and the separate
   RTSP/ONVIF accounts; disable unused services (UPnP/P2P/ONVIF/telnet); expose the
   minimum ports.
3. **Contain**: if no fix exists, isolate the device on its own segment with an
   asymmetric policy and control egress — segmentation is the accepted compensating
   control (NIST IR 8259 Rev. 1). See the
   [iot-untrusted-device-isolation](../../operations/iot-untrusted-device-isolation/SKILL.md) skill.
4. **Decide update vs segment**: patch only if a vendor fix exists, the device is
   supported and you can verify signature + source; otherwise segment, or retire.
   Updates can silently re-enable P2P/UPnP, so stage and re-validate the feature set.
5. **Monitor**: baseline listening ports and outbound destinations; alert on new
   accounts, firmware changes/downgrades and P2P relay traffic.

**Egress note**: P2P/cloud relays reach the device through NAT with no port
forwarding, so LAN isolation does not remove vendor-cloud reachability; treat cloud
egress as a separate trust decision.

## 🔗 5. Integration with Other Skills

- For hardware extraction techniques, see the [hardware-hacking-embedded-security](../../../domains/industry/hardware-hacking-embedded-security/SKILL.md) skill.
- For memory analysis of rootkits, see the [memory-forensics](../memory-forensics/SKILL.md) skill.
- For the OS boot-chain controls, see the [os-hardening-baselines](../os-hardening-baselines/SKILL.md) skill.
- For firmware SBOM, see the [program-sbom-tooling](../../tooling/program-sbom-tooling/SKILL.md) skill.
