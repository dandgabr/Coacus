---
name: "program-windbg"
description: "Provides expertise in low-level debugging on Windows using WinDbg, CDB, and dbgeng.dll. Covers memory dump analysis, call stack inspection, crash evaluation (!analyze -v), and debugging script automation."
---

# AI Skill: WinDbg Automation and Low-Level Debugging

This skill guides the AI to act as a specialist in advanced process debugging and crash analysis in the Windows ecosystem, using **WinDbg**, **CDB (Console Debugger)**, and the native **dbgeng.dll** API.

---

## 🎯 Objective

Provide technical guidelines to:
- Debug running processes and analyze memory dumps (`.dmp`, `.mdmp`).
- Automate debugging tasks via WinDbg commands and JavaScript/WinDbg Preview scripts.
- Interact programmatically with the debugging engine through `dbgeng.dll`.

---

## 🧭 When to Activate

Activate this skill when the user requests:
- Analysis of a **crash dump** or **BSOD** (blue screen).
- Inspection of **call stacks**, **registers**, or **internal runtime structures**.
- Automation of WinDbg/CDB commands to capture process state.
- Debugging scripts that use the `dbgeng.dll` API.

---

## 🛠️ WinDbg Commands and Patterns

### 1. Crash Dump Analysis

Always begin dump analysis with the automatic evaluation command:

```windbg
!analyze -v
```

This command provides an overview of the exception, call stack, involved modules, and a suggested root cause.

### 2. Call Stack Inspection

To view the complete call stack of all threads:

```windbg
~* k
```

To focus on a specific thread (e.g., thread 0):

```windbg
~0 s
k
```

### 3. Reading and Writing Memory

- Read memory at an address:
  ```windbg
  dd <address> L8
  ```
- Search for byte patterns in memory:
  ```windbg
  s -b 0x0 L?0xFFFFFFFFFFFFFFFF <byte_pattern>
  ```

### 4. Breakpoints

- Simple breakpoint:
  ```windbg
  bp <module>!<function>
  ```
- Conditional breakpoint:
  ```windbg
  bp <address> "<command>; gc"
  ```

---

## ⚙️ Automation via CDB and Scripts

### Non-Interactive Execution with CDB

To automatically capture a process state and generate a dump:

```bash
cdb -p <PID> -c ".dump /ma C:\dumps\process.dmp; q" -G
```

To analyze an existing dump and export the result to a file:

```bash
cdb -z <dumpfile.dmp> -lines -c "!analyze -v; k; q" > C:\reports\analysis.txt
```

### JavaScript Scripts in WinDbg Preview

WinDbg Preview supports JavaScript scripts to automate the extraction of complex data:

```javascript
// script.js: Imprime todas as threads e seus IDs
function initializeScript() {
    return [new host.apiVersionSupport(1, 3)];
}

function invokeScript() {
    var threads = host.currentProcess.Threads;
    for (var t of threads) {
        host.diagnostics.debugLog("Thread ID: " + t.Id + "\n");
    }
}
```

To load and run:
```windbg
.scriptload C:\scripts\script.js
!invokeScript
```

---

## 🔗 Integration with dbgeng.dll

For native programmatic interaction (C/C++), use the COM interface of `dbgeng.dll`:

1. **Create a Debug Client instance**:
   ```cpp
   IDebugClient* client;
   DebugCreate(__uuidof(IDebugClient), (void**)&client);
   ```

2. **Attach to a process or open a dump**:
   ```cpp
   client->AttachProcess(0, pid, DEBUG_ATTACH_DEFAULT);
   client->WaitForEvent(0, INFINITE);
   ```

3. **Execute commands and capture output**:
   Use `IDebugControl::Execute` to send commands such as `!analyze -v` and `IDebugOutputCallbacks` to capture the output text.

---

## 🔗 Related Skills

- [program-cheat-engine](../program-cheat-engine/SKILL.md): For runtime memory manipulation via Cheat Engine.
- [memory-manipulation](../../security/platform/memory-manipulation/SKILL.md): For memory corruption vulnerabilities.
- [sast-code-review](../../security/appsec/sast-code-review/SKILL.md): For secure code review.
- [appsec-owasp-asvs](../../security/appsec/appsec-owasp-asvs/SKILL.md): For application security controls.
