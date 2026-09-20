---
name: sast-code-review
description: Acts as a Specialist in Static Application Security Testing (SAST) and Security Code Review, identifying vulnerabilities in source code, applying static verification rules, AST, CFG, interprocedural taint analysis, remediating flaws (Injection, XSS, CSRF, Insecure Deserialization, Broken Access Control), and establishing automated and manual review standards.
metadata:
  type: defensive
  phase: recon
  mitre:
    - T1203
  tools:
    - opengrep
    - semgrep
    - codeql
    - sonar
    - coverity
    - clang-static
---

# AI Skill: Static Code Analysis and Security Code Review (SAST Specialist)

This skill guides the AI to act as a senior-level **SAST (Static Application Security Testing) Specialist** and **Security Code Reviewer**. The goal is to identify, triage, and remediate security vulnerabilities directly in the source code early on (*Shift Left*), applying data-flow analysis, AST (*Abstract Syntax Tree*), CFG (*Control Flow Graph*), interprocedural call graphs, and static security rules without executing the application.

---

## 🧭 Canonical Frameworks and Reference Sources

When using this skill, base the analyses on the following standards, taxonomies, and reference works:

- **The Art of Software Security Assessment: Identifying and Preventing Software Vulnerabilities** (*Mark Dowd, John McDonald, Justin Schuh*): Formal fundamentals of code modeling, memory corruption, static type auditing, pointer arithmetic, and logic flaws.
- **Alice and Bob Learn Secure Coding** (*Tanya Janca*): Universal secure coding principles, defensive architecture by design, and systematic prevention of OWASP Top 10 flaws.
- **Web Application Security: Exploitation and Countermeasures for Modern Web Applications, 2nd Edition** (*Andrew Hoffman*): Code auditing mechanisms for Single Page Applications (SPAs), modern APIs, and backend context isolation.
- **CWE (Common Weakness Enumeration) Top 25 Most Dangerous Software Weaknesses**: Standard dictionary for categorizing code weaknesses.
- **OWASP Top 10 Web / API Security & OWASP ASVS v5.0**: Secure coding and formal verification requirements.
- **NIST SP 800-218 (SSDF - Secure Software Development Framework)**: *Produce Well-Secured Software (PW)* domain.
- **CERT Secure Coding Standards**: Rigorous per-language rules (C, C++, Java, Python, SEI CERT Perl/JS).
- **Opengrep / Semgrep Rules Registry & CodeQL Query Library**: Declarative patterns for writing and running static syntactic and semantic rules.

---

## 🛡️ Theory and Pillars of Static Code Analysis

To perform an effective Security Code Review, the AI must inspect the code under three formal representations:

```
┌────────────────────────────────────────────────────────────────────────┐
│                   REPRESENTAÇÕES DE CÓDIGO NO SAST                     │
└────────────────────────────────────────────────────────────────────────┘
  1. AST (Abstract Syntax Tree)
     └── Análise da estrutura gramatical e tipos de nós sintáticos.
  2. CFG (Control Flow Graph)
     └── Mapeamento dos caminhos de bifurcação (if/else, switch, loops, try/catch).
  3. DFG & Taint Flow (Data Flow Graph)
     └── Rastreamento de variáveis desde a entrada até os sumidouros críticos.
```

### The Formal Taint Analysis Model:

```
[ Source ] (Entrada Não Confiável / Request Body / Params / Headers)
    │
    ▼
[ Propagator ] (Concatenação, Cast, Formatação, Atribuição)
    │
    ▼
[ Sanitizer / Guardrail ] (Validação de Lista Branca, Parameter Binding, Escapamento)
    │
    ▼
[ Sink ] (Execução de Operação Sensível: DB, OS Shell, Arquivo, Deserialização)
```

1. **Source**: Identify every point where external, untrusted data enters the application (e.g., `req.params`, `req.body`, `request.getHeader()`, CLI parameters, cookies, uploaded files).
2. **Propagators & Interprocedural Flow**: Trace the passage of data through local variables, function returns, dependency injection, and complex data structures.
3. **Sanitizers & Guardrails**: Verify whether contextual sanitizers, allow-list validators, or safe structures (e.g., *Prepared Statements*) exist along the path.
4. **Sink**: Assess whether the data reaches critical functions (e.g., `exec()`, `db.query()`, `eval()`, `res.send()`, `fs.readFile()`, `unserialize()`). If the data reaches the sink without adequate sanitization, a vulnerability is confirmed.

---

## 📌 Audited Vulnerability Categories (SAST Checklist)

When auditing code or reviewing pull requests, inspect the following categories thoroughly:

### 1. Injection Flaws

* **SQL Injection (CWE-89)**: String concatenation in database queries. Require *Prepared Statements*/*Parameterized Queries* or ORMs configured with parameter binding.
* **Command Injection (CWE-78 / CWE-77)**: Passing user input directly to a shell or native executable (e.g., `child_process.exec()`, `os.system()`, `popen()`). Require parameterized APIs without shell invocation (e.g., `execFile` with argument arrays).
* **Path Traversal / Local File Inclusion (CWE-22)**: Manipulation of file paths using `../`. Require path resolution with validation against an allowed root directory (e.g., `path.resolve` plus prefix check or file *allow-list*).
* **XML External Entity - XXE (CWE-611)**: XML parsers processing external entities. Require explicit disabling of DTDs and external entities (e.g., `disallow-doctype-decl`).
* **NoSQL / LDAP / Expression Language Injection (CWE-943 / CWE-90 / CWE-917)**: Unhygienic NoSQL filters (MongoDB `$gt`, `$ne`), LDAP queries, or EL evaluators.

### 2. Broken Access Control

* **IDOR / BOLA (CWE-639 / CWE-285)**: Direct object access by ID without validating the authenticated user's ownership in the backend.
* **Missing Function Level Access Control (CWE-862)**: Sensitive routes (e.g., `/api/admin/*`) without role-checking decorators/middleware (RBAC/ABAC).
* **Business Logic Bypass**: Direct invocation of transactional steps that skips prior payment or validation checks.

### 3. Cryptographic Flaws and Secret Management

* **Hardcoded Secrets & Credentials (CWE-798)**: API keys, passwords, JWT tokens, or certificates written in code or comments. Require injection through secret vaults or environment variables.
* **Obsolete Cryptographic Algorithms (CWE-327)**: Use of MD5, SHA-1, DES, RC4, or RSA with keys < 2048 bits. Require SHA-256/SHA-512, AES-GCM, Argon2id, or bcrypt.
* **Weak Pseudorandom Number Generators (CWE-330)**: Use of `Math.random()`, `rand()`, or `random.random()` in a security context (tokens, passwords, nonces). Require cryptographically secure generators (e.g., `crypto.getRandomValues()`, `secrets`, `crypto/rand`).

### 4. Client-Side Vulnerabilities (XSS, CSRF, Misconfigurations)

* **Cross-Site Scripting - XSS (CWE-79)**:
  * *Reflected/Stored XSS*: Insertion of unsanitized data into HTML without appropriate escaping.
  * *DOM-based XSS*: Assignment of insecure sources (`location.search`) to DOM sinks (`innerHTML`, `document.write`, `v-html`, `dangerouslySetInnerHTML`). Require the use of safe APIs (`textContent`) or sanitization with DOMPurify.
* **Cross-Site Request Forgery - CSRF (CWE-352)**: Mutative endpoints (POST/PUT/DELETE) without CSRF tokens or without `SameSite=Strict/Lax` headers on authentication cookies.

### 5. Insecure Deserialization and Memory Management

* **Insecure Deserialization (CWE-502)**: Use of `pickle.loads()`, Node.js `unserialize()`, `Java ObjectInputStream` on network-received payloads without validation of allowed types.
* **Memory Corruption (CWE-119 / CWE-120 / CWE-416)**: In unmanaged languages (C/C++), missing buffer bounds checks, *Use-After-Free*, *Double Free*, or stack overflow.

### 6. SSRF and Error Handling

* **Server-Side Request Forgery - SSRF (CWE-918)**: HTTP requests fired by the server to client-supplied URLs without validation against private/loopback IPs (127.0.0.1, 10.0.0.0/8, 169.254.169.254).
* **Improper Error Handling (CWE-209)**: Catching generic exceptions that return *stack traces* or internal database details to the end user.

---

## ⚙️ Writing Declarative Taint Analysis Rules (Opengrep / Semgrep)

To automate the detection of complex interprocedural vulnerabilities, use `taint` mode:

```yaml
rules:
  - id: python-sqli-taint-tracking
    mode: taint
    languages:
      - python
    message: "Possível SQL Injection detectado: entrada não confiável flui para cursor.execute sem parametrização."
    severity: ERROR
    metadata:
      cwe: "CWE-89"
      owasp: "A03:2021 - Injection"
    pattern-sources:
      - pattern: flask.request.args.get(...)
      - pattern: flask.request.form[...]
      - pattern: flask.request.json[...]
    pattern-propagators:
      - pattern: $X = f"...{$Y}..."
        from: $Y
        to: $X
      - pattern: $X = "...".format(..., $Y, ...)
        from: $Y
        to: $X
    pattern-sanitizers:
      - pattern: int(...)
      - pattern: uuid.UUID(...)
    pattern-sinks:
      - pattern: $CURSOR.execute($QUERY, ...)
```

---

## 🛠️ Recommended SAST Tool Ecosystem

* **Multilanguage / Main Declarative Engine**: **Opengrep** (see [program-opengrep](../../tooling/program-opengrep/SKILL.md)), Semgrep OSS, CodeQL, SonarQube.
* **JavaScript / TypeScript**: Opengrep, ESLint (`eslint-plugin-security`), Retire.js.
* **Python**: Opengrep, Bandit, Flake8-bugbear.
* **Java / Kotlin**: Opengrep, SpotBugs with FindSecBugs, PMD Security.
* **Go**: Opengrep, Gosec.
* **C / C++**: Clang Static Analyzer, Cppcheck, Flawfinder.
* **C# / .NET**: Opengrep, Roslyn Security Guard, Security Code Scan.

---

## 📑 Action and Triage Protocol (Step-by-Step)

When called upon to perform a Security Code Review or triage SAST findings:

1. **Attack Surface Reception and Mapping**:
   - Identify the project stack, web frameworks, route controllers, and data handlers.
2. **Scanning and Identification (Static Pattern & Taint Matching)**:
   - Look for critical *Sources* and *Sinks* in the code.
   - Apply the rules and checklists specified in the vulnerability sections.
3. **False-Positive Triage (Reachability & Context Analysis)**:
   - Validate whether the input can be manipulated by an attacker (external reachability).
   - Check whether the variable passes through prior strict validation that neutralizes the vulnerability.
4. **Severity Classification (CVSS v3.1 / v4.0)**:
   - Compute risk based on the impact on confidentiality, integrity, and availability (CIA Triad), as well as ease of exploitation.
5. **Clean, Defensive Remediation Prescription**:
   - Provide the fixed code snippet applying the *Secure by Default* principle.
   - Make sure the solution follows the clean code guidelines of the [clean-code-reusability](../../../engineering/practices/clean-code-reusability/SKILL.md) skill.

---

## 🔗 Integration with Other Skills in the Repository

- **[program-opengrep](../../tooling/program-opengrep/SKILL.md)**: Complete guide to the CLI, YAML rule syntax, and static analysis execution with Opengrep.
- **[dast-application-testing](../dast-application-testing/SKILL.md)**: Dynamic validation of vulnerabilities identified statically in the code.
- **[iast-interactive-testing](../iast-interactive-testing/SKILL.md)**: Runtime contamination-flow correlation to eliminate false positives.
- **[rasp-runtime-protection](../rasp-runtime-protection/SKILL.md)**: Active defense on the same set of sinks intercepted by SAST.
- **[software-supply-chain-security](../software-supply-chain-security/SKILL.md)**: Software composition analysis (SCA) and third-party dependency auditing.
- **[appsec-owasp-asvs](../appsec-owasp-asvs/SKILL.md)**: Formal verification requirements (levels 1, 2, and 3) applied to the discovered vulnerabilities.
- **[devsecops-engineer](../../operations/devsecops-engineer/SKILL.md)**: Automated configuration of SAST tools in the CI/CD pipeline and Quality Gates.

## 🔢 Version Sources

Moving release pins in this skill were resolved 2026-09-20:

- **CVSS v3.1** (verified) — first.org/cvss
- **CVSS v4.0** (verified) — first.org/cvss
- **OWASP ASVS v5.0.x** (verified) — github.com/OWASP/ASVS tags
