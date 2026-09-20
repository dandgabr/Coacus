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

## 🔗 5. Integration with Other Skills

- For hardware extraction techniques, see the [hardware-hacking-embedded-security](../../../domains/industry/hardware-hacking-embedded-security/SKILL.md) skill.
- For memory analysis of rootkits, see the [memory-forensics](../memory-forensics/SKILL.md) skill.
- For the OS boot-chain controls, see the [os-hardening-baselines](../os-hardening-baselines/SKILL.md) skill.
- For firmware SBOM, see the [program-sbom-tooling](../../tooling/program-sbom-tooling/SKILL.md) skill.
