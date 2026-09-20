---
name: windows-internals-security
description: Acts as a Specialist in Windows internal architecture and security engineering based on Windows Security Internals (James Forshaw) and Windows Internals Part 2 (Mark Russinovich). Covers Security Tokens, Access Control (DACL/SACL, SIDs, privileges), Security Reference Monitor (SRM), IPC (ALPC, RPC, named pipes), LSASS, Kerberos/NTLM, and authentication through PowerShell.
---

# Windows Internal Architecture and Security (Windows Internals)

This skill lays out the security architecture foundations of the Microsoft Windows operating system, covering the kernel object model, the security subsystem (**SRM/LSASS**), and access control based on the works of **James Forshaw** and **Mark Russinovich**.

---

## 🏛️ 1. Windows Security Subsystem Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                       User Mode                             │
│  [ Processos / Apps ]  ──>  [ LSASS (Local Security Auth) ] │
│                                  │ (LSA Authentication)     │
└──────────────────────────────────┼──────────────────────────┘
                                   │ NtAccessCheck
┌──────────────────────────────────▼──────────────────────────┐
│                      Kernel Mode                            │
│  [ Security Reference Monitor (SRM) ]  <──> [ Objeto Kernel]│
│  (Valida Token contra Security Descriptor)   (DACL / SACL)  │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔑 2. Security Token Structure and Access Control

### A. Elements of an Access Token

- **User SID**: Unique security identifier for the user.
- **Group SIDs**: Groups the user belongs to (for example, `S-1-5-32-544` for Administrators).
- **Privileges**: Operating system rights (for example, `SeDebugPrivilege`, `SeImpersonatePrivilege`, `SeBackupPrivilege`).
- **Integrity Level**: Untrusted, Low (sandbox/browser), Medium (standard user), High (elevated admin), System (kernel/SYSTEM).

### B. Security Descriptor

- **Owner SID** and **Group SID**.
- **DACL (Discretionary Access Control List)**: List of ACEs (Access Control Entries) that grant or deny access to specific subjects.
- **SACL (System Access Control List)**: Controls auditing and the generation of security event logs.

---

## 📡 3. Secure Interprocess Communication (IPC)

- **ALPC (Advanced Local Procedure Call)**: High-performance kernel transport for fast communication between local processes (used heavily by LSASS, RPC, and CSRSS).
- **RPC (Remote Procedure Call)**: Communication between machines and local processes with Kerberos/NTLM authentication and authentication levels (`RPC_C_AUTHN_LEVEL_PKT_PRIVACY` for encryption).
