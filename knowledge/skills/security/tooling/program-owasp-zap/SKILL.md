---
name: program-owasp-zap
description: Provides definitive guidance and engineering standards for OWASP ZAP (zaproxy.org), covering the dynamic web application and API security scanner (DAST), the ZAP Automation Framework (AF plans in YAML), Docker-packaged scans (zap-baseline, zap-full-scan, zap-api-scan), the Ajax Spider for SPAs, advanced authentication, the REST API, and CI/CD integration.
metadata:
  type: defensive
  phase: testing
  mitre:
    - T1190
  tools:
    - zaproxy
    - zap-cli
    - docker
---

# AI Skill: Guide and Engineering with OWASP ZAP (Zed Attack Proxy)

This skill provides canonical technical guidance, operational commands, and engineering standards for **OWASP ZAP (Zed Attack Proxy)** ([zaproxy.org](https://www.zaproxy.org/)), the world's most widely used open-source tool for **Dynamic Application Security Testing (DAST)** and HTTP/HTTPS traffic inspection.

---

## 🧭 ZAP Overview and Operating Modes

OWASP ZAP operates as an intercepting proxy and dynamic vulnerability scanner, in three main modes:

```
┌────────────────────────────────────────────────────────────────────────┐
│                        MODOS DE EXECUÇÃO DO ZAP                        │
└────────────────────────────────────────────────────────────────────────┘
  1. Desktop GUI / HUD: Auditoria interativa, exploração manual e depuração.
  2. Headless Daemon: Serviço de segundo plano expondo REST API (porta 8080).
  3. ZAP Automation Framework (AF): Execução headless dirigida por arquivo YAML.
  4. Docker Packaged Scans: Contêineres efêmeros para pipelines de CI/CD.
```

---

## 📄 ZAP Automation Framework (AF) — Canonical YAML Standard

The **Automation Framework (AF)** is the modern standard recommended by the ZAP team for orchestrating complete scans without the need for external scripts.

### 1. Canonical Structure of an Automation Plan (`zap-scan-plan.yaml`)

```yaml
---
env:
  contexts:
    - name: "Ecommerce-Staging"
      urls:
        - "https://staging.empresa.com"
      includePaths:
        - "https://staging.empresa.com/.*"
      excludePaths:
        - "https://staging.empresa.com/logout.*"
        - "https://staging.empresa.com/admin/delete.*"
      authentication:
        method: "json"
        parameters:
          loginUrl: "https://staging.empresa.com/api/v1/auth/login"
          loginRequestData: '{"username": "{%username%}", "password": "{%password%}"}'
        verification:
          method: "response"
          loggedInRegex: '"authenticated":\s*true'
          loggedOutRegex: '"error":\s*"unauthorized"'
      users:
        - name: "test-user"
          credentials:
            username: "qa-sec-user"
            password: "${ZAP_AUTH_PASSWORD}"
  parameters:
    failOnError: true
    failOnWarning: false
    progressToStdout: true

jobs:
  # 1. Spider Tradicional (Crawling de HTML)
  - type: spider
    parameters:
      context: "Ecommerce-Staging"
      user: "test-user"
      maxDuration: 10
      maxDepth: 5

  # 2. Ajax Spider (Navegação Headless em SPAs React/Vue via Chromium)
  - type: spiderAjax
    parameters:
      context: "Ecommerce-Staging"
      user: "test-user"
      maxDuration: 15
      browserId: "firefox-headless"

  # 3. Configuração de Varredura Passiva
  - type: passiveScan-config
    parameters:
      maxAlertsPerRule: 5
      scanOnlyInScope: true

  # 4. Aguardar Conclusão da Análise Passiva
  - type: passiveScan-wait
    parameters:
      maxDuration: 10

  # 5. Varredura Ativa (Fuzzing de Parâmetros e Injeções)
  - type: activeScan
    parameters:
      context: "Ecommerce-Staging"
      user: "test-user"
      policy: "Default Policy"
      maxRuleDurationInMins: 5
      maxScanDurationInMins: 30

  # 6. Geração de Relatórios (HTML, JSON e SARIF)
  - type: report
    parameters:
      template: "traditional-html"
      reportDir: "/zap/wrk/reports"
      reportFile: "zap-report.html"
  - type: report
    parameters:
      template: "sarif-json"
      reportDir: "/zap/wrk/reports"
      reportFile: "zap-report.sarif"
```

### 2. Running the Plan via CLI:

```bash
# Executar o plano YAML em modo headless
./zap.sh -cmd -autorun zap-scan-plan.yaml

# Gerar template mínimo de plano YAML
./zap.sh -cmd -autogenmin template-min.yaml

# Gerar template com todos os parâmetros possíveis
./zap.sh -cmd -autogenmax template-max.yaml
```

---

## 🐳 Execution via Docker-Packaged Scans

For fast CI/CD pipelines, ZAP provides three scripts packaged in its official `zaproxy/zap-stable` image:

### 1. Baseline Scan (`zap-baseline.py`)

Runs a quick spider and **passive analysis** (headers, cookies, CSP, SSL). It does not send aggressive payloads.

```bash
docker run --rm -v $(pwd):/zap/wrk:rw -t zaproxy/zap-stable zap-baseline.py \
    -t https://staging.empresa.com \
    -r zap-baseline-report.html \
    -J zap-baseline-report.json \
    -I
```

### 2. Full Active Scan (`zap-full-scan.py`)

Runs a full spider, Ajax spider, and **deep active scanning** with parameter injection.

```bash
docker run --rm -v $(pwd):/zap/wrk:rw -t zaproxy/zap-stable zap-full-scan.py \
    -t https://staging.empresa.com \
    -r zap-full-report.html \
    -n zap.context \
    -m 30
```

### 3. API Scan (`zap-api-scan.py`)

Designed specifically for REST APIs (OpenAPI/Swagger), GraphQL, and SOAP.

```bash
# Varredura de contrato OpenAPI v3
docker run --rm -v $(pwd):/zap/wrk:rw -t zaproxy/zap-stable zap-api-scan.py \
    -t https://staging.empresa.com/api/v3/openapi.json \
    -f openapi \
    -r zap-api-report.html

# Varredura de endpoint GraphQL
docker run --rm -v $(pwd):/zap/wrk:rw -t zaproxy/zap-stable zap-api-scan.py \
    -t https://staging.empresa.com/graphql \
    -f graphql \
    -r zap-graphql-report.html
```

---

## 🔑 Advanced Authentication and Header Injection

### 1. Static Bearer Token / API Key Injection:

```bash
# Injetar cabeçalho Authorization em todas as requisições disparadas pelo ZAP
docker run --rm -v $(pwd):/zap/wrk:rw -t zaproxy/zap-stable zap-api-scan.py \
    -t https://api.empresa.com/openapi.json \
    -f openapi \
    -z "-config replacer.full_list(0).description=AuthHeader \
        -config replacer.full_list(0).enabled=true \
        -config replacer.full_list(0).matchtype=REQ_HEADER \
        -config replacer.full_list(0).matchstr=Authorization \
        -config replacer.full_list(0).regex=false \
        -config replacer.full_list(0).replacement='Bearer eyJhbGciOiJIUzI1Ni...'"
```

---

## 🚀 CI/CD Integration (GitHub Actions Workflow)

```yaml
name: DAST Dynamic Security Scan (OWASP ZAP)

on:
  schedule:
    - cron: '0 2 * * *' # Execução noturna diária às 02:00
  workflow_dispatch:

jobs:
  dast_scan:
    name: OWASP ZAP Full Scan
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Code
        uses: actions/checkout@v4

      - name: Create Reports Directory
        run: mkdir -p reports

      - name: Run OWASP ZAP Automation Plan
        uses: zaproxy/action-full-scan@v0.12.0
        with:
          target: 'https://staging.empresa.com'
          rules_file_name: '.zap/rules.tsv'
          cmd_options: '-a'

      - name: Upload ZAP HTML Report
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: zap-scan-report
          path: report_html.html
```

---

## 🔗 Integration with Other Skills in the Repository

- **[dast-application-testing](../../appsec/dast-application-testing/SKILL.md)**: Theory and formal methodology of Dynamic Application Security Testing.
- **[pentester-owasp-wstg](../../appsec/pentester-owasp-wstg/SKILL.md)**: Applying ZAP together with the OWASP WSTG pentest methodology.
- **[program-containers](../../../infrastructure/program-containers/SKILL.md)**: Safe execution of isolated Docker containers in CI/CD runners.
- **[devsecops-engineer](../../operations/devsecops-engineer/SKILL.md)**: Quality Gate management and DAST vulnerability mitigation.
