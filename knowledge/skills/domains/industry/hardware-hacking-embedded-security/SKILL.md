---
name: hardware-hacking-embedded-security
description: "Specializes in Hardware, IoT, and Embedded Systems Security Auditing building on The Hardware Hacking Handbook (Jasper van Woudenberg) and The IoT Hacker's Handbook (Aditya Gupta). Covers physical bus identification (UART, JTAG, SWD, I2C, SPI), firmware extraction and dumping (Flash chips, eMMC, NAND), fault injection attacks (Fault Injection/Clock & Voltage Glitching), side-channel attacks (Side-Channel DPA/CPA), and Secure Boot bypass."
---

# Hardware and IoT Security Auditing (Hardware Hacking)

This skill establishes procedures for physical analysis, firmware extraction, non-invasive testing, and resilience assessment of embedded hardware and IoT devices against physical and electronic attacks.

---

## 🔍 1. PCB Reconnaissance

- **Chip Identification**: Reading integrated circuit markings (MCU, SoC, SPI Flash, RAM, PMIC).
- **Test Point & Header Mapping**:
  - **UART (Universal Asynchronous Receiver-Transmitter)**: Identification of `GND`, `TX`, `RX`, `VCC` pins using a multimeter and logic analyzer. Obtaining a serial console / root shell (`baudrate 115200`).
  - **JTAG / SWD**: Identification of `TMS`, `TCK`, `TDI`, `TDO`, `TRST` pins via **JTAGulator** or a multimeter. Extraction of RAM and registers at runtime via OpenOCD.
  - **SPI / I2C Flash**: Direct connection with SOIC-8/SOIC-16 clips and programmers (CH341A, Bus Pirate) for firmware dumping with `flashrom`.

---

## ⚡ 2. Fault Injection and Side-Channel Attacks

| Attack Type | Mechanism | Objective |
| :--- | :--- | :--- |
| **Voltage Glitching** | Abrupt drop (brownout) on the CPU's `VCC` power line for a few nanoseconds. | Skip signature validation instructions (`CMP` / `JNE`) in the bootloader. |
| **Clock Glitching** | Insertion of ultra-fast anomalous clock pulses. | Corrupt registers and disable memory restrictions. |
| **DPA (Differential Power Analysis)** | Measurement of micro-variations in electrical current consumption during cryptographic operations. | Reconstruction of AES/RSA keys through mathematical correlation of power traces. |
| **CPI (Correlation Power Analysis)** | Statistical correlation between a hypothetical power model and the measured traces. | Key recovery with fewer traces than DPA. |
| **Electromagnetic FI (EMFI)** | Localized electromagnetic pulses near the die. | Instruction skipping without physical contact. |

---

## 🔐 3. Secure Boot, Root of Trust and Key Storage

- **Chain of trust / secure boot**: immutable ROM → first-stage bootloader → verified OS; each stage verifies the signature of the next. A break anywhere in the chain invalidates the guarantee.
- **Firmware resiliency (NIST SP 800-193)**: protect the firmware image, detect corruption or tampering, and recover to a known-good image.
- **Hardware roots of trust**: TPM 2.0, discrete HSM, secure element, and TEE (TrustZone / SEV / SGX). Attestation of the measured boot state is the evidence artifact.
- **PUF (Physically Unclonable Function)**: derives a device-unique key from silicon variation; useful for key generation and device identity without stored secrets.
- **Firmware SBOM**: inventory firmware components (including third-party libraries and RTOS) and monitor CVEs across the lifecycle.

---

## 🧰 4. Firmware Extraction and Analysis Tooling

- **Extraction**: SPI flash via CH341A / Bus Pirate / flashrom; eMMC/NAND via direct read; UART/JTAG/SWD dumps where available.
- **Static analysis**: `binwalk` for filesystem and signature carving, `Firmwalker` for secrets and script discovery, **EMBA** for automated extraction, emulation, SBOM generation and vulnerability reporting, and Ghidra for binary RE.
- **Dynamic analysis**: emulate the firmware or run it on real hardware to observe network, bus and debug behavior.
- **RTOS awareness**: Zephyr (CNA/PSIRT disclosure process), FreeRTOS, and Yocto-based images have distinct update, attestation and patching models.

---

## 🔗 5. Integration with Other Skills

- To analyze extracted firmware binaries and implants, see the [firmware-uefi-implant-analysis](../../../security/platform/firmware-uefi-implant-analysis/SKILL.md) skill.
- For the OT/ICS context in which many embedded devices operate, see the [ot-ics-security](../../../security/operations/ot-ics-security/SKILL.md) skill.
- For secure boot and platform protections on general-purpose hosts, see the [os-hardening-baselines](../../../security/platform/os-hardening-baselines/SKILL.md) skill.
