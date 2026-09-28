---
name: program-opengrep
description: Provides definitive guidance and engineering standards for Opengrep (opengrep.dev), covering the open-source static code analysis (SAST) engine, complete YAML rule syntax, syntactic and semantic patterns, advanced Taint Analysis mode, CLI, rule testing, CI/CD integration with SARIF export, and secure code governance.
metadata:
  type: defensive
  phase: testing
  mitre:
    - T1203
  tools:
    - opengrep
    - semgrep
---

# AI Skill: Guide and Engineering with Opengrep (SAST Engine)

This skill provides canonical guidance, operational commands, and engineering standards for using **Opengrep** ([opengrep.dev](https://www.opengrep.dev/)), a high-performance open-source static code analysis (SAST) engine, compatible with the Semgrep OSS declarative rule syntax, designed to identify vulnerabilities, apply architecture best practices, and automate security checks throughout the software development lifecycle (SDLC).

---

## 🧭 Opengrep Overview and Philosophy

Opengrep analyzes source code through abstract syntax tree (AST - *Abstract Syntax Tree*) matching, allowing developers and security analysts to write rules that look like the source code itself, avoiding the complexity and fragility of pure regular expressions.

### Key Advantages:

1. **Friendly Semantic Syntax**: Rules use the target language's own syntax with special operators such as ellipses (`...`) and metavariables (`$VAR`).
2. **High Performance**: An engine compiled to fast native code, capable of scanning millions of lines of code in seconds.
3. **Native Taint Analysis Mode**: Interprocedural tracking of contaminated data flow (*Sources* ➔ *Propagators* ➔ *Sanitizers* ➔ *Sinks*).
4. **Full Interoperability**: Native compatibility with legacy YAML rules and the standard SARIF (*Static Analysis Results Interchange Format*) output format.

---

## 💻 Opengrep CLI Commands

### 1. Installation and Verification

```bash
# Run the version and integrity check
opengrep --version

# Display help and the options catalog
opengrep --help
```

### 2. Scan Commands (`opengrep scan`)

```bash
# Basic scan using a local or automatic rule set
opengrep scan --config auto .

# Scan pointing to a specific YAML rule directory or file
opengrep scan --config ./rules/security.yaml src/

# Scan with multiple rule sets
opengrep scan --config ./rules/sast/ --config ./rules/custom/ src/

# Filter by minimum severity (INFO, WARNING, ERROR)
opengrep scan --config auto --severity ERROR .

# Force a non-zero exit code when vulnerabilities are found (ideal for a CI/CD Quality Gate)
opengrep scan --config auto --error .

# Exclusion and inclusion of specific directories/files
opengrep scan --config auto --exclude "tests/" --exclude "vendor/" --exclude "*.min.js" .
```

### 3. Output Formats and Export

```bash
# Export the report in a structured JSON format
opengrep scan --config auto --json --output opengrep-report.json .

# Export the report in the OASIS SARIF standard (for ingestion into GitHub Security Tab / SonarQube / DefectDojo)
opengrep scan --config auto --sarif-output=opengrep.sarif .

# Quiet mode with only the final summary
opengrep scan --config auto --quiet .
```

### 4. Custom Rule Testing (`opengrep test`)

```bash
# Run the unit test suite for YAML rules against test files
opengrep test ./rules/
```

---

## 📜 Syntax for Creating Declarative Rules in YAML

All Opengrep rules follow the standard YAML schema, split into syntactic pattern matching rules (*Pattern Matching*) or contamination tracking rules (*Taint Mode*).

### 1. Fundamental Matching Operators

- **Ellipses (`...`)**: Match zero or more arguments, statements, expressions, or parameters.
- **Metavariables (`$VAR`)**: Capture and reference any variable, function, or expression in the code. Every occurrence of the same metavariable name within a pattern must match the same literal/symbolic value.

### 2. Example: Detecting Command Injection with Simple Patterns

```yaml
rules:
  - id: nodejs-command-injection-child-process
    languages:
      - javascript
      - typescript
    message: "Possible command injection detected. Using child_process.exec with dynamic data can allow arbitrary code execution on the operating system. Use execFile or spawn with a fixed argument list."
    severity: ERROR
    metadata:
      cwe: "CWE-78: Improper Neutralization of Special Elements used in an OS Command"
      owasp: "A03:2021 - Injection"
      confidence: HIGH
      category: security
    patterns:
      - pattern: child_process.exec($CMD, ...)
      - pattern-not: child_process.exec("...", ...)
      - pattern-not: child_process.exec(`...`, ...)
```

### 3. Example: Complete Taint Analysis in Python (SQL Injection)

In `taint` mode, Opengrep tracks the origin of the data to the critical consumption point:

```yaml
rules:
  - id: python-flask-sql-injection-taint
    mode: taint
    languages:
      - python
    message: "SQL Injection detected: untrusted input originating from the Flask request reaches SQL query execution without parameterization."
    severity: ERROR
    metadata:
      cwe: "CWE-89: SQL Injection"
      owasp: "A03:2021 - Injection"
      category: security
    
    # 1. Untrusted data sources
    pattern-sources:
      - pattern: flask.request.args.get(...)
      - pattern: flask.request.form[...]
      - pattern: flask.request.json[...]
      - pattern: flask.request.headers.get(...)
      - pattern: flask.request.get_json(...)
    
    # 2. Propagation through concatenations or string formatting
    pattern-propagators:
      - pattern: $TARGET = f"...{$SOURCE}..."
        from: $SOURCE
        to: $TARGET
      - pattern: $TARGET = "...".format(..., $SOURCE, ...)
        from: $SOURCE
        to: $TARGET
      - pattern: $TARGET = $A + $SOURCE
        from: $SOURCE
        to: $TARGET

    # 3. Sanitizers (neutralize the taint)
    pattern-sanitizers:
      - pattern: int(...)
      - pattern: float(...)
      - pattern: uuid.UUID(...)
      - pattern: sqlalchemy.text(...)

    # 4. Critical sinks (Sinks)
    pattern-sinks:
      - pattern: $DB.session.execute($QUERY, ...)
      - pattern: $CURSOR.execute($QUERY, ...)
      - pattern: sqlite3.connect(...).cursor().execute($QUERY, ...)
```

---

## 🧪 Rule Unit Test Structure

To guarantee that a rule produces neither false positives nor misses real cases, create a test file with the same language extension next to the rule `.yaml` file.

### Unit Test Example (`nodejs-command-injection.js`):

```javascript
const child_process = require('child_process');

function testVulnerable(req, res) {
    let userInput = req.query.cmd;
    // ruleid: nodejs-command-injection-child-process
    child_process.exec("ping -c 1 " + userInput, (err, stdout) => {
        console.log(stdout);
    });
}

function testSafe() {
    // ok: nodejs-command-injection-child-process
    child_process.exec("ls -la /tmp", (err, stdout) => {
        console.log(stdout);
    });
}
```

When running `opengrep test ./rules/`, the engine validates that the line commented with `// ruleid:` triggers the alert and the line with `// ok:` is ignored.

---

## 🚀 CI/CD Pipeline Integration

### 1. GitHub Actions Workflow with SARIF Upload

```yaml
name: Opengrep Security Scan

on:
  push:
    branches: [ "main", "develop" ]
  pull_request:
    branches: [ "main" ]

jobs:
  opengrep:
    name: Opengrep SAST Scan
    runs-on: ubuntu-latest
    permissions:
      security-events: write
      contents: read
      actions: read

    steps:
      - name: Checkout Repository
        uses: actions/checkout@v4

      - name: Install Opengrep
        run: |
          curl -fsSL https://github.com/opengrep/opengrep/releases/latest/download/opengrep-linux-x86_64 -o /usr/local/bin/opengrep
          chmod +x /usr/local/bin/opengrep

      - name: Run Opengrep SAST
        run: |
          opengrep scan --config auto --sarif-output=results.sarif --error .

      - name: Upload SARIF to GitHub Security Tab
        if: always()
        uses: github/codeql-action/upload-sarif@v3
        with:
          sarif_file: results.sarif
```

### 2. Pre-commit Hook Configuration

Add to the `.pre-commit-config.yaml` file:

```yaml
repos:
  - repo: https://github.com/opengrep/opengrep
    rev: v1.0.0
    hooks:
      - id: opengrep
        args: ['scan', '--config', 'auto', '--error']
```

---

## 🔗 Integration with Other Skills in the Repository

- **[sast-code-review](../../appsec/sast-code-review/SKILL.md)**: Applies the vulnerability taxonomy and triage best practices together with the Opengrep engine.
- **[program-github-actions](../../../platforms/program-github-actions/SKILL.md)**: Complete workflow automation, binary caching, and Quality Gates in GitHub Actions.
- **[devsecops-engineer](../../operations/devsecops-engineer/SKILL.md)**: Centralized governance of security pipelines and remediation metrics.
