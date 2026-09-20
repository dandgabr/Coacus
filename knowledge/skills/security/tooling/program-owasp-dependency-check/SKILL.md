---
name: program-owasp-dependency-check
description: Provides definitive guidance and engineering standards for OWASP Dependency-Check (owasp.org/www-project-dependency-check), covering Software Composition Analysis (SCA), CLI, Maven and Gradle plugins, GitHub Actions, integration with the NVD API v2, centralized CVE database, complete suppressions.xml syntax, CPE hints, and CVSS-based Quality Gates.
metadata:
  type: defensive
  phase: testing
  mitre:
    - T1195.001
    - T1195.002
  tools:
    - owasp-dependency-check
    - maven
    - gradle
---

# AI Skill: Guide and Engineering with OWASP Dependency-Check (SCA Tool)

This skill provides canonical technical guidance, operational commands, and engineering standards for **OWASP Dependency-Check** ([owasp.org/www-project-dependency-check](https://owasp.org/www-project-dependency-check/)), the standard open-source tool for **Software Composition Analysis (SCA)**, designed to identify known vulnerabilities (CVEs) in third-party libraries and components in software projects.

---

## 🧭 Dependency-Check Overview and Operation

OWASP Dependency-Check collects evidence about the project's dependencies (Vendor, Product, Version) from manifests, file names, hashes, and package metadata, maps that information to **CPE (Common Platform Enumeration)** identifiers, and queries the **NVD (National Vulnerability Database)** and **GitHub Security Advisory (GHSA)** databases to report associated CVEs.

```
┌────────────────────────────────────────────────────────────────────────┐
│               FLUXO DE ANÁLISE DO OWASP DEPENDENCY-CHECK               │
└────────────────────────────────────────────────────────────────────────┘
  [ 1. Coleta de Evidências ]
         │  (Analisa JARs, package.json, pom.xml, go.mod, arquivos binários)
         ▼
  [ 2. Mapeamento de CPE ]
         │  (Gera identificadores: cpe:2.3:a:apache:log4j:2.14.1:*:*:*:*:*:*:*)
         ▼
  [ 3. Consulta NVD API v2 & Cache Local ]
         │  (Verifica banco de dados H2 local ou PostgreSQL centralizado)
         ▼
  [ 4. Aplicação de Supressões (suppressions.xml) ]
         │  (Descarta falsos positivos e vulnerabilidades com mitigação aceita)
         ▼
  [ 5. Avaliação de Quality Gate (failBuildOnCVSS) ]
            (Falha a compilação caso CVSS >= Limiar definido)
```

---

## 💻 Integration and Execution Modes

### 1. Command Line (CLI)

```bash
# Execução básica com exportação em múltiplos formatos (HTML, JSON, SARIF)
dependency-check.sh \
    --project "EcommerceApp" \
    --scan "./src" \
    --scan "./lib" \
    --out "./reports" \
    --format "ALL" \
    --nvdApiKey "SEU_NVD_API_KEY" \
    --failOnCVSS 7.0

# Execução utilizando arquivo de supressão de falsos positivos
dependency-check.sh \
    --project "EcommerceApp" \
    --scan "./target" \
    --suppression "./config/dependency-check-suppressions.xml" \
    --format "HTML" \
    --out "./reports"
```

---

### 2. Integration with Apache Maven (`pom.xml`)

Add the `dependency-check-maven` plugin in the `<build><plugins>` block:

```xml
<plugin>
    <groupId>org.owasp</groupId>
    <artifactId>dependency-check-maven</artifactId>
    <version>10.0.3</version>
    <configuration>
        <!-- Chave de API NVD v2 obrigatória para evitar rate-limits -->
        <nvdApiKey>${env.NVD_API_KEY}</nvdApiKey>
        
        <!-- Arquivo de supressão de falsos positivos -->
        <suppressionFiles>
            <suppressionFile>${project.basedir}/config/dependency-check-suppressions.xml</suppressionFile>
        </suppressionFiles>
        
        <!-- Falhar a compilação do Maven se houver vulnerabilidade High/Critical -->
        <failBuildOnCVSS>7.0</failBuildOnCVSS>
        
        <!-- Formatos de saída gerados -->
        <formats>
            <format>HTML</format>
            <format>JSON</format>
            <format>SARIF</format>
        </formats>
    </configuration>
    <executions>
        <execution>
            <goals>
                <goal>check</goal>
            </goals>
        </execution>
    </executions>
</plugin>
```

#### Execution Commands in Maven:

```bash
# Executar a verificação avulsa
mvn org.owasp:dependency-check-maven:check

# Executar apenas a atualização do banco de dados NVD em cache
mvn org.owasp:dependency-check-maven:update-only
```

---

### 3. Integration with Gradle (`build.gradle`)

```groovy
plugins {
    id 'org.owasp.dependencycheck' version '10.0.3'
}

dependencyCheck {
    nvd {
        apiKey = System.getenv('NVD_API_KEY')
    }
    suppressionFile = 'config/dependency-check/suppressions.xml'
    failBuildOnCVSS = 7.0f
    formats = ['HTML', 'JSON', 'SARIF']
    analyzers {
        assemblyEnabled = false
        nodeAudit {
            enabled = true
        }
    }
}
```

#### Execution Command in Gradle:

```bash
./gradlew dependencyCheckAnalyze
```

---

## 🔑 NVD API v2 Configuration and Centralized Database

Because of the strict *rate limiting* introduced in NIST's NVD API v2, obtaining a free **NVD API Key** is mandatory to avoid `403 Forbidden` errors or downloads that take more than 40 minutes in CI/CD pipelines.

### Centralized Database Configuration (PostgreSQL / MySQL)

In corporate pipelines with multiple concurrent runners, configure Dependency-Check to use a centralized relational database instead of individual H2 files:

```xml
<configuration>
    <databaseProperties>
        <driver>org.postgresql.Driver</driver>
        <url>jdbc:postgresql://db-sec.empresa.local:5432/dependencycheck</url>
        <user>dc_user</user>
        <password>${env.DB_PASSWORD}</password>
    </databaseProperties>
</configuration>
```

---

## 🛡️ False-Positive Management and the Suppression File (`suppressions.xml`)

The suppression file lets you ignore CVEs that do not affect the application (for example, when the vulnerable method is not executed or the CPE incorrectly matched a same-named library).

### Complete Syntax of the `dependency-check-suppressions.xml` File:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<suppressions xmlns="https://jeremylong.github.io/DependencyCheck/dependency-suppression.1.4.xsd">

    <!-- 1. Supressão de falso positivo por CPE incorreto -->
    <suppress>
        <notes><![CDATA[
            Falso positivo: O componente interno 'auth-module' foi incorretamente 
            identificado como o produto legado Apache Auth.
        ]]></notes>
        <packageUrl regex="true">^pkg:maven/com\.empresa/auth-module@.*$</packageUrl>
        <cpe>cpe:/a:apache:auth</cpe>
    </suppress>

    <!-- 2. Supressão de CVE específica com data de expiração (Until) -->
    <suppress until="2026-12-31Z">
        <notes><![CDATA[
            CVE-2022-1471 no SnakeYaml: Avaliada pelo time de AppSec. A aplicação não 
            utiliza deserialização genérica não confiável. Mitigação aceita até a migração v2.0.
        ]]></notes>
        <packageUrl regex="true">^pkg:maven/org\.yaml/snakeyaml@.*$</packageUrl>
        <vulnerabilityName>CVE-2022-1471</vulnerabilityName>
    </suppress>

    <!-- 3. Supressão por hash SHA-1 de arquivo binário específico -->
    <suppress>
        <notes><![CDATA[
            Supressão para binário de testes interno legado.
        ]]></notes>
        <sha1>66734244CE86857018B023A8C56AE0635C56B6A1</sha1>
        <cve>CVE-2020-99999</cve>
    </suppress>

</suppressions>
```

---

## 🚀 CI/CD Integration (GitHub Actions Workflow)

```yaml
name: SCA Dependency-Check Scan

on:
  push:
    branches: [ "main" ]
  pull_request:
    branches: [ "main" ]

jobs:
  dependency_check:
    name: OWASP Dependency-Check (SCA)
    runs-on: ubuntu-latest
    permissions:
      security-events: write
      contents: read

    steps:
      - name: Checkout Repository
        uses: actions/checkout@v4

      - name: Run OWASP Dependency-Check
        uses: dependency-check/Dependency-Check_Action@10.0.3
        with:
          project: 'EcommerceBackend'
          path: '.'
          format: 'SARIF'
          args: >
            --nvdApiKey ${{ secrets.NVD_API_KEY }}
            --failOnCVSS 7
            --suppression config/dependency-check-suppressions.xml

      - name: Upload SARIF to GitHub Security Tab
        if: always()
        uses: github/codeql-action/upload-sarif@v3
        with:
          sarif_file: 'reports/dependency-check-report.sarif'
```

---

## 🔗 Integration with Other Skills in the Repository

- **[software-supply-chain-security](../../appsec/software-supply-chain-security/SKILL.md)**: Dependency management theory, SBOM (CycloneDX/SPDX), VEX, and prioritization by EPSS/CISA KEV.
- **[sast-code-review](../../appsec/sast-code-review/SKILL.md)**: Complements SCA by auditing flaws in proprietary code.
- **[devsecops-engineer](../../operations/devsecops-engineer/SKILL.md)**: Orchestration of CI/CD pipelines and corporate Quality Gates.
- **[program-github-actions](../../../platforms/program-github-actions/SKILL.md)**: Configuration of automated workflows and SARIF upload in GitHub.
