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
