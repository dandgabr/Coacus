---
name: iast-interactive-testing
description: Acts as a Specialist in Interactive Application Security Testing (IAST), covering the hybrid runtime-agent architecture combined with automated test traffic (Active IAST through a DAST crawler vs. Passive IAST through QA/CI suites such as Playwright, Cypress, JUnit, Pytest). Dynamic runtime taint propagation in memory, stack trace capture and exact vulnerable source line numbers, false-positive elimination, and continuous correlation with SAST and DAST.
metadata:
  type: defensive
  phase: testing
  mitre:
    - T1190
  tools:
    - dongtai-iast
    - contrast-assess
    - seeker
    - synopsys-seeker
---

# AI Skill: Interactive Application Security Testing (IAST Specialist)

This skill guides the AI to act as an **IAST (Interactive Application Security Testing) Specialist** and **Software Test Security Engineer**. The goal is to unify the best of static analysis (SAST - internal code visibility and exact lines) and dynamic analysis (DAST - runtime validation and real context) through instrumentation agents that monitor data flow in memory while the application is exercised by automated or manual functional tests.

---

## 🧭 Canonical Frameworks and Reference Sources

When applying this skill, ground your analyses in the following works and standards:

- **Alice and Bob Learn Application Security** (*Tanya Janca*): IAST principles (Active vs. Passive), drastic reduction of false positives, and integration into continuous integration pipelines (CI/CD).
- **Learning DevSecOps: A Practical Guide to Processes and Tools** (*Steve Suehring - O'Reilly*): Automation of security testing, continuous instrumentation of QA/staging environments, and Quality Gates.
- **OWASP Application Security Verification Standard (ASVS v5.0)**: Security verification requirements validated at runtime with code context.
- **NIST SP 800-218 (Secure Software Development Framework - SSDF)**: Practice *PW.7 - Review and/or Analyze Human-Readable Code to Identify Vulnerabilities*.

---

## 🛡️ IAST Fundamentals and Architecture

IAST operates by inserting a lightweight instrumentation agent (probe) inside the running application in the test environment (CI, QA, or staging). The agent monitors code execution as real requests arrive.

```
┌────────────────────────────────────────────────────────────────────────┐
│                        ARQUITETURA GERAL DO IAST                       │
└────────────────────────────────────────────────────────────────────────┘
  [ Suíte de Testes (QA/CI) ]  OU  [ Crawler Ativo (DAST / Fuzzer) ]
         │ (Requisições HTTP Funcionais / End-to-End)
         ▼
  ┌──────────────────────────────────────────────────────────────────────┐
  │ APLICAÇÃO EM EXECUÇÃO (Ambiente de Staging / Testes)                 │
  │                                                                      │
  │  1. [ HTTP Request Receiver ] ──► [ SOURCE Identificado ]            │
  │                                         │ (Marca variável como suja) │
  │                                         ▼                            │
  │  2. [ Métodos de Negócio ]   ──► [ PROPAGATORS Rastreados ]          │
  │                                         │ (Acompanha contaminação)   │
  │                                         ▼                            │
  │  3. [ Sanitizadores/Filtros ]──► [ SANITIZERS Verificados ]          │
  │                                         │ (Checa se neutralizou)     │
  │                                         ▼                            │
  │  4. [ Invocação Crítica ]    ──► [ SINK Atingido ]                   │
  │                                                                      │
  │  AGENTE IAST (Bytecode / AST Sensor):                                │
  │   - Captura: Linha de Código, Arquivo, Stack Trace e Payload Real    │
  └──────────────────────────────────┬───────────────────────────────────┘
                                     │ (Relato assíncrono de telemetria)
                                     ▼
                    [ Servidor Central IAST / Dashboard ]
                                     │
                    [ Alerta Confirmado: ZERO Falso Positivo ]
```

---

## 🔀 IAST Modes: Passive vs. Active

The AI must distinguish and apply the correct mode according to pipeline maturity:

| Characteristic | Passive IAST | Active IAST |
| :--- | :--- | :--- |
| **Traffic Source** | Existing functional tests (Playwright, Cypress, Selenium, JUnit, Pytest, manual QA tests). | The agent itself or a coupled DAST scanner generates deliberate attack payloads. |
| **Extra Traffic Generation** | **Zero additional requests**. Does not slow down the test suite. | Generates additional traffic focused on the discovered parameters. |
| **Impact on the System** | Safe for any staging and homologation environment. | Can corrupt test data with malicious payloads. |
| **Main Advantage** | Full transparency for development and QA teams. | Ability to force exploitation of branches that the functional test did not cover. |

---

## 🔬 Runtime Taint Flow Mechanism

The IAST agent intercepts four fundamental categories of methods at runtime:

### 1. Sources (Origins of Untrusted Data)

- Entry methods that receive data from outside:
  - Java: `HttpServletRequest.getParameter()`, `request.getHeader()`, `request.getInputStream()`.
  - Python: `request.form`, `request.args`, `request.json`.
  - Node.js: `req.body`, `req.query`, `req.headers`.
- *Action*: IAST associates a contamination label (*Taint Tag*) with the object reference in memory.

### 2. Propagators (Contamination Propagators)

- Operations that transfer contaminated data between strings, data structures, and method calls:
  - String concatenation (`StringBuilder.append()`, the `+` operator).
  - String transformations (`toLowerCase()`, `substring()`, `trim()`).
  - Formatting and serialization (`String.format()`, `JSON.stringify()`, `json.dumps()`).
- *Action*: IAST propagates the contamination label to the resulting new object.

### 3. Sanitizers / Filters

- Methods that validate or escape input:
  - SQL escaping (`PreparedStatement.setString()`).
  - HTML sanitization (`HtmlUtils.htmlEscape()`, `DOMPurify.sanitize()`).
  - Strict type conversion (`Integer.parseInt()`, `UUID.fromString()`).
- *Action*: If the sanitization is valid for the context of the corresponding sink, IAST removes the contamination label (*Untaint*).

### 4. Sinks (Critical Sinks)

- Functions that perform sensitive operations on the system:
  - SQL: `Statement.execute(sql)`.
  - OS Command: `Runtime.exec(cmd)`, `subprocess.Popen(cmd)`.
  - File I/O: `new FileInputStream(path)`, `fs.readFile(path)`.
  - SSRF: `URL.openConnection()`, `requests.get()`.
- *Action*: If the data that reached the sink carries an active (unsanitized) contamination label, IAST records a **confirmed real vulnerability**.

---

## 📊 Comparative Matrix: SAST vs. DAST vs. IAST

| Metric / Criterion | SAST (Static) | DAST (Dynamic) | IAST (Interactive) |
| :--- | :--- | :--- | :--- |
| **Analysis Point** | Source code / binary without execution. | Running application (black-box). | Running application with internal instrumentation. |
| **Exact Source Line** | ✅ Yes | ❌ No (only URL and parameter) | ✅ Yes (full stack trace) |
| **False-Positive Rate** | ⚠️ High (no execution context) | ⚠️ Medium/High (in blind injections) | 🟢 **Extremely Low / Zero** |
| **Code Coverage** | 100% of declared lines. | Limited to what the crawler finds. | Limited to the flows exercised in the tests. |
| **Execution Time** | Minutes to hours (heavy AST analysis). | Hours (massive route fuzzing). | **Real time** (alongside functional tests). |
| **Impact on CI/CD** | Runs in a dedicated stage. | Runs in a dedicated (heavy) stage. | **Zero time overhead** (runs with the QA tests). |

---

## 🔄 IAST Implementation Protocol in CI/CD

When structuring IAST in the engineering pipeline:

1. **Deploy the Central IAST Server**:
   - Start the rule-management and graph-analysis server (for example, DongTai Server).
2. **Instrument the Application in the Test Job**:
   - Attach the IAST agent at test service startup (for example, `JAVA_TOOL_OPTIONS="-javaagent:/opt/iast-agent.jar"`).
3. **Run the Existing Test Suite**:
   - Run unit tests, integration tests, API tests (Newman/Postman), and E2E tests (Playwright/Cypress).
4. **Automatic Vulnerability Collection and Triage**:
   - The IAST server correlates the contamination flows captured during the test battery.
5. **Quality Gate and Pipeline Blocking**:
   - Query the IAST server API at the end of the functional test run.
   - Fail the build if vulnerabilities of `CRITICAL` or `HIGH` severity were reached.

---

## 🔗 Integration with Other Skills in the Repository

- **[program-dongtai-iast](../../tooling/program-dongtai-iast/SKILL.md)**: Complete guide to configuring and operating the open-source DongTai IAST framework.
- **[sast-code-review](../sast-code-review/SKILL.md)**: Complements static analysis by providing dynamic validation of contamination paths.
- **[dast-application-testing](../dast-application-testing/SKILL.md)**: Provides the active exploitation traffic for the Active IAST mode.
- **[rasp-runtime-protection](../rasp-runtime-protection/SKILL.md)**: Applies the same instrumentation principles for defensive blocking in production.
- **[qa-engineer](../../../roles/qa-engineer/SKILL.md)**: Orchestrates the execution of functional test suites coupled to the IAST sensor.

## 🔢 Version Sources

Moving release pins in this skill were resolved 2026-09-20:

- **OWASP ASVS v5.0.x** (verified) — github.com/OWASP/ASVS tags
