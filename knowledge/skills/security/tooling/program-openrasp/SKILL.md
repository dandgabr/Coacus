---
name: program-openrasp
description: Provides definitive guidance and engineering standards for Baidu OpenRASP (github.com/baidu/openrasp), covering the open-source Runtime Application Self-Protection (RASP) framework, Java and PHP agent installation, the OpenRASP Cloud panel, JavaScript (V8 engine) detection plugin development, SQLi, RCE, SSRF, and deserialization interception, and SOC/SIEM integration.
metadata:
  type: defensive
  phase: operations
  mitre:
    - T1190
    - T1059
  tools:
    - openrasp
    - javaagent
    - zend-extension
---

# AI Skill: Guide and Engineering with Baidu OpenRASP

This skill provides in-depth technical guidance, operational commands, and implementation standards for **OpenRASP** ([github.com/baidu/openrasp](https://github.com/baidu/openrasp)), the leading open-source **Runtime Application Self-Protection (RASP)** solution developed by Baidu, designed to protect Java and PHP web servers directly in the runtime environment.

---

## 🧭 OpenRASP Overview and Architecture

OpenRASP operates by injecting instrumentation probes directly into the runtimes of supported languages, inspecting execution parameters before critical operating system or database methods are invoked.

```
┌────────────────────────────────────────────────────────────────────────┐
│                     GENERAL OPENRASP ARCHITECTURE                      │
└────────────────────────────────────────────────────────────────────────┘
  [ APPLICATION NODE (Java / PHP) ]
  ┌────────────────────────────────────────────────────────────────────┐
  │  1. Sensitive Method Invocation (e.g., Statement.executeQuery)     │
  │     │                                                              │
  │     ▼                                                              │
  │  2. OpenRASP Probe Hook Intercepts the Call                        │
  │     │                                                              │
  │     ▼                                                              │
  │  3. Embedded Google V8 Engine Executes the JavaScript Plugin       │
  │     │ (Parses SQL query AST, tokenization, regex, and stack trace) │
  │     │                                                              │
  │     ├──► Action: BLOCK  ──► Aborts execution + Throws HTTP 403     │
  │     ├──► Action: LOG    ──► Logs an alert and allows the call      │
  │     └──► Action: IGNORE ──► Allows the operation normally          │
  └─────────────────────────────────┬──────────────────────────────────┘
                                    │ (Heartbeat + JSON Alert Logs)
                                    ▼
  [ OPENRASP CLOUD MANAGEMENT CONSOLE ] (Web Panel + API)
  ┌────────────────────────────────────────────────────────────────────┐
  │  - Backend: Go / Python                                            │
  │  - Database: MongoDB / MySQL                                       │
  │  - Logs & Analytics: Elasticsearch + Kibana                        │
  │  - Policy Management and Automatic JS Plugin Updates               │
  └────────────────────────────────────────────────────────────────────┘
```

---

## 💻 Agent Installation and Configuration

### 1. Java Agent (Spring Boot, Tomcat, JBoss, WebLogic)

#### Package Installation:

Download the latest version of the OpenRASP Java Agent and unpack it into the `/opt/rasp` directory.

#### Directory Structure:

```
/opt/rasp/
├── conf/
│   └── openrasp.yml      # Agent configuration and Cloud connection
├── plugins/
│   └── official.js       # Default JavaScript detection plugin
├── logs/                 # JSON alarm and audit logs
└── rasp.jar              # Main Java Agent binary
```

#### Configuration of the `conf/openrasp.yml` File:

```yaml
# Connection to the OpenRASP Cloud Management
cloud:
  enable: true
  backend_url: "http://openrasp-cloud.empresa.local:8086"
  app_id: "a1b2c3d4e5f6g7h8i9j0"
  app_secret: "secret-token-generated-in-the-panel"
  heartbeat_interval: 180

# Protection modes (true = Active Blocking, false = Log Only)
block:
  status: true

# Logging settings
logger:
  max_size: 500MB
  max_backup: 10
```

#### Application Startup with the Agent:

```bash
# Running a Spring Boot application (.jar)
java -javaagent:/opt/rasp/rasp.jar -Dfile.encoding=UTF-8 -jar app.jar

# Configuration for Apache Tomcat (in the catalina.sh or setenv.sh file)
export JAVA_OPTS="$JAVA_OPTS -javaagent:/opt/rasp/rasp.jar"
```

---

### 2. PHP Agent (Zend Engine Extension)

#### Module Installation:

```bash
# Compilation or installation via the official script
cd /tmp && git clone https://github.com/baidu/openrasp.git
cd openrasp/agent/php && phpize
./configure --with-php-config=/usr/bin/php-config
make && sudo make install
```

#### Configuration in `php.ini`:

```ini
; Loading the OpenRASP extension
extension=openrasp.so

; Root directory for settings and plugins
openrasp.root_dir=/opt/rasp

; Enable active protection
openrasp.inject_urlprefix=/
openrasp.block_status=1
```

---

## 📜 Developing JavaScript Detection Plugins (V8 Engine)

OpenRASP's great differentiator is the ability to extend its policies through JavaScript scripts executed in a native high-speed V8 sandbox inside the process.

### 1. Structure of an OpenRASP Plugin (`custom-security.js`)

```javascript
'use strict';

var plugin = new RASP('custom-security-rules');

// =========================================================================
// 1. Interception of Operating System Command Injection (RCE)
// =========================================================================
plugin.register('command', function (params, context) {
    var command = params.command;
    
    // Block reverse shell invocations or destructive commands
    var dangerousPatterns = [
        /nc\s+-e/i,
        /bash\s+-i/i,
        /rm\s+-rf\s+\//i,
        /curl.*\|\s*sh/i,
        /wget.*\|\s*sh/i
    ];

    for (var i = 0; i < dangerousPatterns.length; i++) {
        if (dangerousPatterns[i].test(command)) {
            return {
                action: 'block',
                message: 'Critical Command Injection blocked by OpenRASP: ' + command,
                confidence: 100
            };
        }
    }

    return { action: 'ignore' };
});

// =========================================================================
// 2. Interception of SQL Injection with Syntactic Analysis
// =========================================================================
plugin.register('sql', function (params, context) {
    var query = params.query;
    
    // Detect classic boolean or union injections
    if (/union(\s+all)?\s+select/i.test(query) || /or\s+1\s*=\s*1/i.test(query)) {
        return {
            action: 'block',
            message: 'SQL Injection detected at runtime: ' + query,
            confidence: 95
        };
    }

    return { action: 'ignore' };
});

// =========================================================================
// 3. Interception of SSRF (Server-Side Request Forgery)
// =========================================================================
plugin.register('ssrf', function (params, context) {
    var url = params.url;

    // Block access to cloud metadata (AWS/GCP/Azure) and loopback interfaces
    if (/169\.254\.169\.254/i.test(url) || /127\.0\.0\.1/i.test(url) || /localhost/i.test(url)) {
        return {
            action: 'block',
            message: 'SSRF request to an internal address/metadata blocked: ' + url,
            confidence: 100
        };
    }

    return { action: 'ignore' };
});
```

---

## 📊 List of Hooks Supported by OpenRASP

| Hook ID | Intercepted Resource | Examples of Mitigated Threats |
| :--- | :--- | :--- |
| `sql` | JDBC / MySQL / PostgreSQL / Oracle drivers | SQL Injection (CWE-89), Stacked Queries |
| `command` | `ProcessBuilder`, `Runtime.exec()`, `system()`, `exec()` | OS Command Injection (CWE-78), Web Shells |
| `readFile` / `writeFile` | `FileInputStream`, `fopen()`, `file_get_contents()` | Path Traversal (CWE-22), Arbitrary File Overwrite |
| `fileUpload` | `MultipartResolver`, `$_FILES` | Web Shell Upload (`.jsp`, `.php`, `.phtml`) |
| `deserialization` | `ObjectInputStream.readObject()`, `unserialize()` | Insecure Deserialization / Java Gadgets (CWE-502) |
| `ssrf` | `HttpURLConnection`, `HttpClient`, `curl_exec()` | SSRF to internal networks or cloud metadata (CWE-918) |
| `xss_userinput` | HTML output manipulation in the response buffer | Stored & Reflected XSS (CWE-79) |
| `ognl` | OGNL evaluators (Apache Struts) | Struts RCE (CVE-2017-5638, CVE-2018-11776) |

---

## 📈 Alert Log Format and SIEM Integration

When an attack is intercepted, OpenRASP writes a complete JSON entry containing the full context to the `/opt/rasp/logs/alarm/alarm.log` file:

```json
{
  "event_type": "attack",
  "app_id": "a1b2c3d4e5f6g7h8i9j0",
  "server_hostname": "app-prod-01",
  "server_ip": "10.0.1.50",
  "attack_type": "sql",
  "plugin_name": "custom-security-rules",
  "action": "block",
  "confidence": 95,
  "client_ip": "198.51.100.42",
  "request_method": "POST",
  "request_url": "https://app.empresa.com/api/v1/search",
  "attack_params": {
    "query": "SELECT * FROM users WHERE id = 1 UNION SELECT null, username, password FROM admin"
  },
  "stack_trace": [
    "com.mysql.cj.jdbc.StatementImpl.executeQuery(StatementImpl.java:115)",
    "com.empresa.app.dao.UserDAO.findUser(UserDAO.java:45)",
    "com.empresa.app.controller.UserController.search(UserController.java:28)"
  ],
  "timestamp": "2026-08-29T17:30:00.123Z"
}
```

---

## 🔗 Integration with Other Skills in the Repository

- **[rasp-runtime-protection](../../appsec/rasp-runtime-protection/SKILL.md)**: Theory and architectural governance guidelines for runtime protection.
- **[sast-code-review](../../appsec/sast-code-review/SKILL.md)**: Prior static validation of the same sinks protected by OpenRASP.
- **[secops-incident-responder](../../operations/secops-incident-responder/SKILL.md)**: Ingestion of OpenRASP alerts and creation of incident response playbooks.
