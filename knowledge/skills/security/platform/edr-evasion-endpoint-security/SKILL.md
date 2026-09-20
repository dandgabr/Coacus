---
name: edr-evasion-endpoint-security
description: Acts as a Specialist in Endpoint Defense Architecture (EDR/XDR) and evasion/detection mechanisms based on Evading EDR (Matt Hand). Covers telemetry sources (kernel callbacks, ETW, AMSI, API hooking in ntdll), stack inspection techniques (call stack spoofing, synthetic frames), direct/indirect system calls, and defensive hardening of EDR agents.
---

# Endpoint Defense and Evasion Mechanism Analysis (EDR Security)

This skill builds a deep understanding of how Endpoint Detection and Response (**EDR**) solutions work, their telemetry sources, architectural limits, and the offensive/defensive engineering techniques documented in **Evading EDR: The Definitive Guide to Defeating Endpoint Detection Systems** by Matt Hand.

---

## 🛡️ 1. Pillars of EDR Telemetry

```
┌─────────────────────────────────────────────────────────────┐
│ 1. User-Mode Hooking (Inline Patches na ntdll.dll / APIs)   │
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│ 2. Kernel Callbacks (PsSetCreateProcessNotifyRoutine, etc.) │
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│ 3. Event Tracing for Windows (ETW / ETW-Ti no Kernel)       │
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│ 4. AMSI (Antimalware Scan Interface em Scripts/Runtimes)    │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔬 2. Telemetry Mechanisms and Blind Spots

### A. User-Mode API Hooking

- **How It Works**: The EDR injects a DLL into the process and inserts `JMP` instructions at the prologue of `ntdll.dll` functions (for example, `NtAllocateVirtualMemory`, `NtWriteVirtualMemory`, `NtCreateThreadEx`) to inspect parameters before execution.
- **Bypass and Detection Techniques**:
  - **Direct Syscalls (Syswhispers/Hell's Gate/Halo's Gate)**: Invoke the `syscall` instruction directly in code without going through the `ntdll` hooks.
  - **Indirect Syscalls**: Jump to the `syscall; ret` instruction located inside the legitimate `ntdll.dll` itself, preserving the origin module's signature in kernel logs.
  - **Module Unhooking**: Read a clean copy of the `ntdll.dll` `.text` section from disk (`\KnownDlls\` or the physical file) and overwrite the process memory to remove the EDR patches.

### B. Call Stack Analysis

- **Synthetic Call Stacks and Spoofing**: Modern EDRs inspect the return address on the stack. Direct calls from unbacked memory raise alerts. Call stack spoofing techniques build synthetic frames that mimic legitimate execution flows (for example, calling through `RtlUserThreadStart` -> `BaseThreadInitThunk`).

### C. Kernel ETW-Ti (Threat Intelligence)

- Telemetry generated directly from the kernel by the EDR driver subscribed to the ETW-Ti channel. It cannot be disabled from user mode without driver/kernel permissions.

---

## 📋 3. Hardening and Threat Hunting Matrix

| Execution Vector | Telemetry Generated | Detection Rule / Mitigation |
| :--- | :--- | :--- |
| **RWX Memory Allocation** | `PAGE_EXECUTE_READWRITE` | Alert on memory transitions from `PAGE_READWRITE` to `PAGE_EXECUTE_READ` in regions not mapped by DLLs. |
| **Remote Process Injection** | `OpenProcess` with `PROCESS_VM_WRITE` | Restrict handle opening on critical processes (lsass, svchost) with kernel drivers and PPL (Protected Process Light) rules. |
| **AMSI Patching** | Protected memory in `amsi.dll` | Monitor the integrity of `AmsiScanBuffer` and intercept changes through hardware breakpoints. |
