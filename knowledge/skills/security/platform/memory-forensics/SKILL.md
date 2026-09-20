---
name: memory-forensics
description: Acts as a Memory Forensics specialist covering volatile memory acquisition, Volatility-class analysis (process listing, injected code, hidden processes, credential material, network artifacts), rootkit detection in memory and the correlation of memory findings with disk and network evidence.
metadata:
  type: defensive
  phase: actions
---

# Memory Forensics

This skill guides the AI to extract and interpret evidence from volatile memory, where fileless malware, keys and injected code reside and disk analysis cannot reach.

---

## 📥 1. Acquisition

- Acquire memory **before** shutdown or reboot; volatility is the point and the limitation.
- Use a trusted acquisition tool; its integrity matters because it runs on a potentially compromised host.
- Record the acquisition hash and the exact tool and version.
- On virtual machines, snapshot memory through the hypervisor where possible for a cleaner image.

---

## 🔬 2. Analysis (Volatility-Class)

- **Processes**: list and build the process tree; compare against the image's actual process list to find hidden or unlinked processes.
- **Injected code**: find memory regions that are executable but have no backing file, a strong injection signal.
- **Rootkits**: detect hooking of system tables and callbacks; compare in-memory structures with what the OS reports.
- **Network artifacts**: recover connections, sockets and listening ports as they were at capture.
- **Credentials and keys**: recover cached credentials, hashes and cryptographic material (handle with care and legal authority).
- **Registry and files**: extract hives and cached files from memory when disk access is unavailable.

---

## 🔗 3. Correlation

Memory findings are hypotheses until correlated with disk and network evidence. A suspicious memory region becomes a confirmed finding when its hash matches a known payload or its behavior matches telemetry.

---

## 🛡️ 4. Rootkit and Bootkit Awareness

Kernel-mode and boot-level malware can hide from standard APIs; memory analysis that compares raw structures with API-reported structures is the way to find them. For pre-OS implants, see the [firmware-uefi-implant-analysis](../firmware-uefi-implant-analysis/SKILL.md) skill.

---

## 🔗 5. Integration with Other Skills

- For the DFIR process, see the [dfir-forensics](../../operations/dfir-forensics/SKILL.md) skill.
- For host artifacts, see the [endpoint-forensics](../../operations/endpoint-forensics/SKILL.md) skill.
- For the analysis methodology, see the [malware-analysis-multios](../../appsec/malware-analysis-multios/SKILL.md) skill.
- For memory exploitation primitives (distinct concept), see the [memory-manipulation](../memory-manipulation/SKILL.md) skill.
