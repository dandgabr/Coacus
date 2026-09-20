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
│                      ARQUITETURA GERAL DO OPENRASP                     │
└────────────────────────────────────────────────────────────────────────┘
  [ NÓ DE APLICAÇÃO (Java / PHP) ]
  ┌────────────────────────────────────────────────────────────────────┐
  │  1. Invocação de Método Sensível (Ex: Statement.executeQuery)      │
  │     │                                                              │
  │     ▼                                                              │
  │  2. Sonda OpenRASP Hook Intercepta a Chamada                       │
  │     │                                                              │
  │     ▼                                                              │
  │  3. Motor Google V8 Embutido Executa o Plugin JavaScript           │
  │     │ (Analisa AST da query SQL, tokenização, regex e stack trace) │
  │     │                                                              │
  │     ├──► Ação: BLOCK  ──► Aborta execução + Lança Erro HTTP 403    │
  │     ├──► Ação: LOG    ──► Registra alerta e permite a chamada      │
  │     └──► Ação: IGNORE ──► Permite a operação normalmente           │
  └─────────────────────────────────┬──────────────────────────────────┘
                                    │ (Heartbeat + Logs de Alerta JSON)
                                    ▼
  [ OPENRASP CLOUD MANAGEMENT CONSOLE ] (Painel Web + API)
  ┌────────────────────────────────────────────────────────────────────┐
  │  - Backend: Go / Python                                            │
  │  - Banco de Dados: MongoDB / MySQL                                 │
  │  - Logs & Analytics: Elasticsearch + Kibana                        │
  │  - Gestão de Políticas e Atualização Automática de Plugins em JS   │
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
│   └── openrasp.yml      # Configurações do agente e conexão com o Cloud
├── plugins/
│   └── official.js       # Plugin JavaScript padrão de detecção
├── logs/                 # Logs de alarmes e auditoria em JSON
└── rasp.jar              # Binário principal do Java Agent
```

#### Configuration of the `conf/openrasp.yml` File:

```yaml
# Conexão com o OpenRASP Cloud Management
cloud:
  enable: true
  backend_url: "http://openrasp-cloud.empresa.local:8086"
  app_id: "a1b2c3d4e5f6g7h8i9j0"
  app_secret: "secret-token-gerado-no-painel"
  heartbeat_interval: 180

# Modos de proteção (true = Bloqueio Ativo, false = Apenas Log)
block:
  status: true

# Configurações de logging
logger:
  max_size: 500MB
  max_backup: 10
```

#### Application Startup with the Agent:

```bash
# Executando aplicação Spring Boot (.jar)
java -javaagent:/opt/rasp/rasp.jar -Dfile.encoding=UTF-8 -jar app.jar

# Configuração para Apache Tomcat (no arquivo catalina.sh ou setenv.sh)
export JAVA_OPTS="$JAVA_OPTS -javaagent:/opt/rasp/rasp.jar"
```

---

### 2. PHP Agent (Zend Engine Extension)

#### Module Installation:

```bash
# Compilação ou instalação via script oficial
cd /tmp && git clone https://github.com/baidu/openrasp.git
cd openrasp/agent/php && phpize
./configure --with-php-config=/usr/bin/php-config
make && sudo make install
```

#### Configuration in `php.ini`:

```ini
; Carregamento da extensão OpenRASP
extension=openrasp.so

; Diretório raiz de configurações e plugins
openrasp.root_dir=/opt/rasp

; Habilitar proteção ativa
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
// 1. Interceptação de Injeção de Comandos do Sistema Operacional (RCE)
// =========================================================================
plugin.register('command', function (params, context) {
    var command = params.command;
    
    // Bloquear invocações de shells reversas ou comandos destrutivos
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
                message: 'Injeção de Comando Crítica bloqueada pelo OpenRASP: ' + command,
                confidence: 100
            };
        }
    }

    return { action: 'ignore' };
});

// =========================================================================
// 2. Interceptação de SQL Injection com Análise Sintática
// =========================================================================
plugin.register('sql', function (params, context) {
    var query = params.query;
    
    // Detectar injeções booleanas ou de união clássicas
    if (/union(\s+all)?\s+select/i.test(query) || /or\s+1\s*=\s*1/i.test(query)) {
        return {
            action: 'block',
            message: 'SQL Injection detectada em tempo de execução: ' + query,
            confidence: 95
        };
    }

    return { action: 'ignore' };
});

// =========================================================================
// 3. Interceptação de SSRF (Server-Side Request Forgery)
// =========================================================================
plugin.register('ssrf', function (params, context) {
    var url = params.url;

    // Bloquear acesso aos metadados de nuvem (AWS/GCP/Azure) e interfaces de loopback
    if (/169\.254\.169\.254/i.test(url) || /127\.0\.0\.1/i.test(url) || /localhost/i.test(url)) {
        return {
            action: 'block',
            message: 'Requisição SSRF para endereço interno/metadados bloqueada: ' + url,
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
