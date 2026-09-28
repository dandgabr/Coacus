---
name: program-dongtai-iast
description: Provides definitive guidance and engineering standards for DongTai IAST (github.com/HXSecurity/DongTai), covering the open-source passive Interactive Application Security Testing framework, DongTai Server deployment with Docker Compose, agent installation (Java, Python, Go, PHP, Node.js), Taint Tracking rules (Sources, Propagators, Sanitizers, Sinks), and integration with QA test suites in CI/CD.
metadata:
  type: defensive
  phase: testing
  mitre:
    - T1190
  tools:
    - dongtai-iast
    - docker-compose
---

# AI Skill: Guide and Engineering with DongTai IAST

This skill provides canonical technical guidance, operational commands, and engineering standards for **DongTai IAST** ([github.com/HXSecurity/DongTai](https://github.com/HXSecurity/DongTai)), the first open-source passive **Interactive Application Security Testing (IAST)** framework, developed by Huoxian Security (HXSecurity).

---

## 🧭 DongTai IAST Overview and Architecture

DongTai IAST uses a **Passive IAST** approach, in which instrumentation agents installed inside the application monitor data flow in memory as real or automated test requests arrive, without generating additional invasive traffic and without the need for external crawlers.

```
┌────────────────────────────────────────────────────────────────────────┐
│                       DONGTAI IAST ARCHITECTURE                        │
└────────────────────────────────────────────────────────────────────────┘
  [ QA TESTS / REAL TRAFFIC ] (Playwright, Cypress, Postman, JMeter)
                 │ (Normal functional HTTP requests)
                 ▼
  [ INSTRUMENTED ENVIRONMENT (Java, Python, Go, PHP, Node.js Application) ]
  ┌────────────────────────────────────────────────────────────────────┐
  │ DONGTAI AGENT (dongtai-agent.jar / dongtai-agent-python)           │
  │                                                                    │
  │  1. Request Ingestion     ──► SOURCE (Tags data as tainted)        │
  │  2. Internal Methods      ──► PROPAGATOR (Tracks contamination)    │
  │  3. Sanitizers            ──► FILTER (Checks if neutralized)       │
  │  4. Critical Calls        ──► SINK (Detects security violation)    │
  └─────────────────────────────────┬──────────────────────────────────┘
                                    │ (Asynchronous report via OpenAPI)
                                    ▼
  [ DONGTAI SERVER ] (Orchestrator & Analysis Engine)
  ┌────────────────────────────────────────────────────────────────────┐
  │  - DongTai OpenAPI Gateway: Receives telemetry and node heartbeats │
  │  - DongTai Engine: Analyzes the contamination graphs and stack trace│
  │  - DongTai Web UI: Vulnerability and rule management dashboard     │
  │  - Storage: MySQL + Redis                                          │
  └────────────────────────────────────────────────────────────────────┘
```

---

## 🚀 DongTai Server Deployment (Docker Compose)

The DongTai Server is deployed centrally using Docker containers.

### 1. Cloning and Initialization:

```bash
# Clone the official DongTai repository
git clone https://github.com/HXSecurity/DongTai.git
cd DongTai

# Bring up the complete server infrastructure
docker-compose -f docker-compose.yml up -d
```

### 2. Running Ports and Components:

- **Web Panel (DongTai Web UI)**: `http://localhost:80` or `http://localhost:8888`
- **OpenAPI Gateway**: `http://localhost:8888/openapi`
- **Default Credentials**: `admin` / `admin` (change them immediately on first login).
- **Token Generation**: In the web panel, go to **System Settings ➔ Agent Deployment** to obtain the unique agent authentication `Token`.

---

## 💻 Agent Installation and Execution by Language

### 1. Java Agent (Spring Boot, Tomcat, WildFly)

The DongTai Java agent is composed of three internal modules (`dongtai-agent.jar`, `dongtai-core.jar`, and `dongtai-spy.jar`).

```bash
# Download the compiled Java agent
curl -X GET "http://dongtai-server:8888/openapi/api/v1/agent/download?url=http://dongtai-server:8888/openapi&language=java" \
     -H "Authorization: Token ${DONGTAI_TOKEN}" -o dongtai-agent.jar

# Run the Java application with the agent attached
java -javaagent:/opt/dongtai/dongtai-agent.jar \
     -Ddongtai.server.url=http://dongtai-server:8888/openapi \
     -Ddongtai.server.token=YOUR_TOKEN_HERE \
     -Ddongtai.app.name=EcommerceBackend \
     -Ddongtai.app.version=v1.2.0 \
     -Ddongtai.app.create=true \
     -jar app.jar
```

### 2. Python Agent (Django, Flask, FastAPI)

The Python agent uses dynamic *monkey patching* to intercept methods in the CPython runtime.

```bash
# Install the agent package via pip
pip install dongtai-agent-python

# Set environment variables for automatic initialization
export DONGTAI_IAST_SERVER_URL="http://dongtai-server:8888/openapi"
export DONGTAI_IAST_SERVER_TOKEN="YOUR_TOKEN_HERE"
export DONGTAI_IAST_PROJECT_NAME="FinanceAPI"
export DONGTAI_IAST_PROJECT_VERSION="v2.0.0"

# Initialize the Django / Flask application
python manage.py runserver 0.0.0.0:8000
```

### 3. Go Agent (Golang)

The Go agent performs dynamic rewriting of function addresses and symbol hooking at runtime:

```bash
# Integrate the dongtai-agent-go package into the main.go file
import _ "github.com/HXSecurity/dongtai-agent-go"
```

---

## 🔬 Rule Configuration and Hook Strategy

DongTai classifies methods into four categories within its rule engine:

```
┌────────────────────────────────────────────────────────────────────────┐
│                     NODE TYPES IN THE TAINT GRAPH                      │
└────────────────────────────────────────────────────────────────────────┘
  1. SOURCE: Data entry (e.g., javax.servlet.ServletRequest.getParameter)
  2. PROPAGATOR: Concatenation (e.g., java.lang.StringBuilder.append)
  3. FILTER: Validation (e.g., org.apache.commons.lang3.StringEscapeUtils.escapeHtml4)
  4. SINK: Dangerous consumption (e.g., java.sql.Statement.execute, java.lang.Runtime.exec)
```

### Example of a Sink Rule Structure in DongTai:

- **Target Class**: `java.lang.ProcessBuilder`
- **Method**: `start()`
- **Signature**: `()Ljava/lang/Process;`
- **Vulnerability Type**: `Command Injection (CWE-78)`
- **Condition**: If any argument that reached the `ProcessBuilder` carries an active contamination label coming from a `SOURCE` without passing through an approved `FILTER`, DongTai records the vulnerability with a full stack trace.

---

## 🔄 Integration with DevSecOps and QA Pipelines

The great benefit of DongTai IAST is its ability to turn the existing QA test suite into a continuous security audit with no additional execution time.

### CI/CD Workflow (GitHub Actions / GitLab CI):

```
┌────────────────────────┐
│ 1. Application Build   │
└───────────┬────────────┘
            ▼
┌────────────────────────┐
│ 2. Start in Staging    │ ──► (Starts the application with dongtai-agent attached)
└───────────┬────────────┘
            ▼
┌────────────────────────┐
│ 3. E2E QA Execution    │ ──► (Runs Playwright / Cypress / Newman / Selenium)
└───────────┬────────────┘
            ▼
┌────────────────────────┐
│ 4. Quality Gate Check  │ ──► (Queries the DongTai Server API: Are there vulnerabilities?)
└───────────┬────────────┘
            ▼
┌────────────────────────┐
│ 5. Approve or Block    │
└────────────────────────┘
```

### Quality Gate Check Script via API:

```bash
#!/usr/bin/env bash
set -euo pipefail

DONGTAI_URL="http://dongtai-server:8888/openapi"
TOKEN="YOUR_TOKEN_HERE"
PROJECT_NAME="EcommerceBackend"

# Query the total number of critical or high vulnerabilities in the project
FINDINGS=$(curl -s -X GET "${DONGTAI_URL}/api/v1/vulns?project_name=${PROJECT_NAME}&level=1,2" \
     -H "Authorization: Token ${TOKEN}" | jq '.data | length')

echo "Total serious vulnerabilities found by IAST: ${FINDINGS}"

if [ "${FINDINGS}" -gt 0 ]; then
    echo "❌ Quality Gate FAILED: DongTai identified critical vulnerabilities at runtime."
    exit 1
else
    echo "✅ Quality Gate PASSED: No active critical vulnerabilities detected."
fi
```

---

## 🔗 Integration with Other Skills in the Repository

- **[iast-interactive-testing](../../appsec/iast-interactive-testing/SKILL.md)**: Formal theory of Interactive Application Security Testing and comparison with SAST/DAST.
- **[program-opengrep](../program-opengrep/SKILL.md)**: Complements the prior static analysis of taint rules.
- **[qa-engineer](../../../roles/qa-engineer/SKILL.md)**: Direct connection with functional test automation (Playwright, Cypress, Pytest).
- **[devsecops-engineer](../../operations/devsecops-engineer/SKILL.md)**: Configuration of automated Quality Gates in the CI/CD pipeline.
