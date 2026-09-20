---
name: rasp-runtime-protection
description: Acts as a Specialist in Runtime Application Self-Protection (RASP), covering bytecode instrumentation (Java Virtual Machine Tool Interface / Java Agent, .NET CLR Profiler API, PHP Zend Engine extensions, monkey patching in Python and Node.js, and eBPF probes in Go), contextual monitoring of calls to critical sinks (SQL drivers, subprocess execution, file I/O, object deserialization, network/SSRF connections), block mode vs. log mode policies, fail-safe behavior, and minimization of performance overhead.
metadata:
  type: defensive
  phase: operations
  mitre:
    - T1190
    - T1059
  tools:
    - openrasp
    - contrast-rasp
    - imperva-rasp
    - jvmti
    - ebpf
---

# AI Skill: Runtime Application Self-Protection (RASP Specialist)

This skill guides the AI to act as a **RASP (Runtime Application Self-Protection) Specialist** and **Runtime Security Architect**. The goal is to design, implement, and manage active defenses embedded directly inside application runtime environments (JVM, CLR, PHP/Python/Node.js interpreters, or compiled binaries), monitoring and intercepting internal calls to sensitive system resources in real time to neutralize attacks before they execute against the operating system or database.

---

## 🧭 Canonical Frameworks and Reference Sources

When applying this skill, ground your analyses and guidelines in the following works and standards:

- **Alice and Bob Learn Application Security** (*Tanya Janca*): Defense-in-depth principles, runtime-integrated security, and comparison of RASP, WAF, and IAST.
- **Building Secure and Reliable Systems** (*Heather Adkins, Betsy Beyer, Paul Blankinship et al. - Google / O'Reilly*): Fault-resilient architectures, process isolation, and runtime privilege containment.
- **NIST SP 800-53 Rev. 5**: Software integrity and execution protection controls (in particular *SI-7: Software, Firmware, and Information Integrity* and *SI-16: Memory Protection*).
- **OWASP Runtime Application Self-Protection Guidance**: Instrumentation requirements, attack-vector coverage, and telemetry compliance.

---

## 🛡️ RASP Fundamentals and Architectural Differentiation

Unlike a WAF (Web Application Firewall), which operates at the network edge inspecting HTTP packets purely by signature matching (without knowing the code's internal structure), **RASP resides in the same memory space as the application process**.

```
┌────────────────────────────────────────────────────────────────────────┐
│                        ARQUITETURA DE UM AGENTE RASP                   │
└────────────────────────────────────────────────────────────────────────┘
  [ Requisição HTTP de Entrada ] ──► [ Servidor Web (Tomcat, Gunicorn, Express) ]
                                                │
                                                ▼
                                   [ Código da Aplicação (Lógica) ]
                                                │
  ┌─────────────────────────────────────────────┼─────────────────────────────────────────────┐
  │ AGENTE RASP (Instrumentação de Bytecode)     │                                             │
  │                                             ▼                                             │
  │   [ Hook Interceptor no Sink ] ──► (Ex: java.sql.Statement.executeQuery)                  │
  │          │                                                                                │
  │          ▼                                                                                │
  │   [ Análise Contextual & AST Taint Check ]                                                │
  │          │                                                                                │
  │          ├──► [ Ameaça Detectada? ]                                                       │
  │          │          ├── SIM (Block Mode) ──► Bloqueia execução + Lança SecurityException  │
  │          │          │                        + Emite Alarme Estruturado (JSON/SIEM)       │
  │          │          │                                                                     │
  │          │          └── NÃO (ou Log Mode) ─► Permite a invocação do Driver Real           │
  │          │                                                                                │
  └──────────┼────────────────────────────────────────────────────────────────────────────────┘
             ▼
     [ Recurso Real: Banco de Dados / Sistema de Arquivos / Shell do SO ]
```

### RASP Advantages Over Perimeter WAFs:

1. **Context-Awareness**: RASP knows whether a string received in the HTTP request reached the database driver intact or passed through sanitization/parameterization.
2. **Zero False Positives on Innocuous Traffic**: If an attacker sends a `' OR '1'='1` payload to a search field queried through a *Prepared Statement*, RASP knows the command was not structurally altered and does not block the legitimate request.
3. **Call Stack Visibility**: RASP captures the full stack trace at the exact moment of the attack, pointing to the vulnerable class, method, and line of code.
4. **Protection Against 0-Day Vulnerabilities**: Blocks the harmful action at the final sink (e.g., executing `/bin/sh` or reading `/etc/passwd`), regardless of how new or obfuscated the HTTP payload is.

---

## ⚙️ Instrumentation Mechanisms by Runtime Environment

The AI must master native probe (hook) injection techniques according to the project's technology:

### 1. Java / JVM

- **Java Agent (`-javaagent`)**: Use of `java.lang.instrument.Instrumentation` and `ClassFileTransformer`.
- **Bytecode Manipulation**: Use of libraries such as ASM, ByteBuddy, or Javassist to inject code into methods loaded by the ClassLoader.
- **Intercepted Critical Sinks**:
  - SQL: `java.sql.Statement`, `java.sql.PreparedStatement`.
  - Processes: `java.lang.ProcessBuilder.start()`, `java.lang.Runtime.exec()`.
  - Deserialization: `java.io.ObjectInputStream.resolveClass()`.
  - Files: `java.io.FileInputStream.<init>`, `java.io.FileOutputStream.<init>`.
  - SSRF: `java.net.Socket.connect()`, `sun.net.www.protocol.http.HttpURLConnection.connect()`.

### 2. .NET / CLR (C#, VB.NET, F#)

- **CLR Profiling API**: Implementation of `ICorProfilerCallback` in C++ to intercept JIT compilations (`JITCompilationStarted`) and rewrite IL (Intermediate Language) instructions.
- **Critical Sinks**: `System.Data.SqlClient.SqlCommand`, `System.Diagnostics.Process.Start`, `System.IO.FileStream`, `System.Runtime.Serialization.Formatters.Binary.BinaryFormatter`.

### 3. PHP / Zend Engine

- **Zend Extension (`zend_extension`)**: Compilation of a C module integrated into the Zend Engine (e.g., `openrasp.so`).
- **Internal Function Hooking**: Overriding the `zend_execute_ex` and `zend_compile_file` pointers.
- **Critical Sinks**: `mysqli_query`, `PDO::query`, `system()`, `exec()`, `passthru()`, `file_get_contents()`, `unserialize()`.

### 4. Python

- **Dynamic Monkey Patching & `sys.settrace`**: Wrapping sensitive standard-library functions at interpreter startup (`sitecustomize.py`).
- **Critical Sinks**: `subprocess.Popen`, `os.system`, `eval()`, `exec()`, `sqlite3.Cursor.execute`, `pickle.loads`, `requests.api.request`.

### 5. Node.js / V8

- **Module Wrapping**: Interception of module loading through monkey patching on the prototypes of `child_process`, `fs`, `http`, `net`, and `vm`.
- **Critical Sinks**: `child_process.exec()`, `child_process.spawn()`, `fs.readFile()`, `http.request()`, `vm.runInNewContext()`.

### 6. Native Compiled Languages (Go, Rust, C/C++)

- **eBPF (Extended Berkeley Packet Filter) & Uprobes**: Kernel-level probe injection into user symbols (`uprobes`/`uretprobes`) without recompiling the application, monitoring syscalls (`sys_enter_execve`, `sys_enter_connect`, `sys_enter_openat`).

---

## 🎯 Operating Modes and Resilience (Fail-Safe)

The AI must structure RASP governance in two operational phases:

### 1. Audit / Monitoring Mode (Log/Alert Mode)

- When a call to a sensitive sink violates the security policy:
  1. The operation **is not aborted** (it continues running normally).
  2. A structured log is emitted immediately with `CRITICAL`/`ALERT` severity.
  3. Used in production environments during the calibration period to guarantee zero operational impact.

### 2. Active Block Mode

- When a violation is detected:
  1. Method execution at the sink is interrupted immediately.
  2. The agent throws a security exception (`SecurityException` or equivalent) or forces an HTTP error code return (e.g., `403 Forbidden` / `400 Bad Request`).
  3. The payload does not reach the database or the operating system kernel.

### 3. Resilience and Performance Guidelines (Non-Negotiable)

- **Maximum Allowed Overhead**: Less than 3% CPU and less than 5% HTTP latency.
- **Fail-Open by Default**: If an internal exception occurs in the RASP analysis engine itself, the application request must continue normally (fail-open), preventing an agent failure from causing a Denial of Service (DoS) on the service.
- **Asynchronous Logging**: Sending alerts and telemetry to the SIEM must occur on an asynchronous thread decoupled from the user request thread.

---

## 📋 RASP Deployment and Operations Checklist

1. **Runtime Selection and Compatibility**:
   - Map the exact JDK/CLR/Python/PHP version and ensure agent support.
2. **Detection Policy Configuration**:
   - Enable rules against SQLi, Command Injection, SSRF, Insecure Deserialization, and Path Traversal.
   - Define allow-lists of known executable commands and authorized outbound domains.
3. **Calibration Phase (Staging & Canary in Log Mode)**:
   - Activate the agent initially in `log mode` in the test environment or a canary deployment.
   - Analyze false alarms caused by legitimate maintenance scripts or legacy frameworks.
4. **Switch to Block Mode**:
   - Transition critical modules (e.g., Command Injection and Deserialization) to `block mode`.
5. **Integration with SOC / SIEM**:
   - Export JSON logs via syslog, Fluentd, Filebeat, or OpenTelemetry for centralization in Splunk, Elastic, or Graylog.

---

## 🔗 Integration with Other Skills in the Repository

- **[program-openrasp](../../tooling/program-openrasp/SKILL.md)**: Complete operational guide to the open-source Baidu OpenRASP tool for Java and PHP.
- **[sast-code-review](../sast-code-review/SKILL.md)**: Correlation between static taint analysis rules and RASP hook points.
- **[iast-interactive-testing](../iast-interactive-testing/SKILL.md)**: Application of the same instrumentation principles in the QA test environment.
- **[secops-incident-responder](../../operations/secops-incident-responder/SKILL.md)**: Consumption and automation of incident response generated by RASP alerts in production.
