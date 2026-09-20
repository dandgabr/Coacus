---
name: software-supply-chain-security
description: "Acts as a Specialist in Software Supply Chain Security, Software Composition Analysis (SCA), and Dependency Management based on Cassie Crossley and NIST SSDF / SP 800-161. Covers SBOM generation and auditing (CycloneDX v1.5/v1.6 and SPDX v2.3/v3.0), VEX, SLSA v1.0 provenance, cryptographic signing with Sigstore/Cosign and in-toto, vulnerability mitigation (CVEs, GHSA, EPSS, CISA KEV), open-source license auditing (GPL, AGPL, Apache, MIT), lockfile pinning, call-graph reachability analysis, and defense against typosquatting and dependency confusion."
metadata:
  type: defensive
  phase: recon
  tools: [owasp-dependency-check, syft, grype, trivy, snyk, cosign, slsa-verifier]
  mitre: [T1195, T1195.001, T1195.002, T1140]
---

# Software Supply Chain Security (Supply Chain Security & SCA)

This skill establishes the canonical guidelines for auditing, protecting, and managing vulnerabilities in third-party libraries (*Software Composition Analysis - SCA*), reachability analysis, license compliance, and end-to-end integrity verification in the software and firmware supply chain, grounded in the work of **Cassie Crossley** (*Software Supply Chain Security: Securing the End-to-end Supply Chain for Software, Firmware, and Hardware*), the **SLSA (Supply-chain Levels for Software Artifacts v1.0)** framework, **NIST SP 800-161 Rev. 1**, and the **NIST SSDF (SP 800-218)**.

---

## 🛡️ 1. Pillars of the Software Supply Chain

```
┌────────────────────────────────────────────────────────────────────────┐
│ 1. Fonte & Upstream (Manifestos, Lockfiles, Dependências Diretas/Trans) │
└──────────────────────────────────┬─────────────────────────────────────┘
                                   │
┌──────────────────────────────────▼─────────────────────────────────────┐
│ 2. Pipeline de Build CI/CD (Hermetic Builds, Runners Efêmeros, SLSA)   │
└──────────────────────────────────┬─────────────────────────────────────┘
                                   │
┌──────────────────────────────────▼─────────────────────────────────────┐
│ 3. Pacotes & Artefatos (SBOM CycloneDX/SPDX, Assinatura Sigstore/Cosign)│
└──────────────────────────────────┬─────────────────────────────────────┘
                                   │
┌──────────────────────────────────▼─────────────────────────────────────┐
│ 4. Runtime & Deploy (Admission Controllers, VEX, Attestation, Guardrail)│
└────────────────────────────────────────────────────────────────────────┘
```

---

## 🔬 2. Advanced Software Composition Analysis (SCA) Methodology

SCA is not just about matching versions against a string list. Modern SCA analysis operates at four levels of depth:

### 2.1 Graph Resolution and Transitive Dependencies

- **Direct Dependency**: Explicitly declared in the project manifest (`package.json`, `pom.xml`, `pyproject.toml`).
- **Transitive (Indirect) Dependency**: Dependencies of dependencies, which make up more than 80% of third-party code in modern applications.
- **Lockfile Pinning & Immutability**: In automated pipelines, always require resolution locked by cryptographic hashes (`npm ci`, `poetry install --sync`, `cargo build --locked`) to prevent silent package substitution (*Lockfile Poisoning*).

### 2.2 Reachability Analysis

- A vulnerability in a third-party library is exploitable only if the application invokes the vulnerable function, class, or method.
- **Classification**:
  - *Present in the Package*: The `.jar` file or npm package is in the `node_modules` / `target` folder.
  - *Reachable via Call-Graph*: The proprietary code executes calls that reach the vulnerable library method.
- SCA tools with *Reachability* support (such as OWASP Dependency-Check with advanced analyzers or Snyk/Trivy) reduce by up to 70% the noise of alerts that do not require immediate production stoppage.

### 2.3 Multidimensional Prioritization: CVSS + EPSS + CISA KEV

The AI must compute real risk based on the threat intelligence triad:

1. **CVSS v3.1 / v4.0 (Intrinsic Severity)**: Measures the theoretical impact on confidentiality, integrity, and availability (CIA).
2. **EPSS (Exploit Prediction Scoring System - FIRST)**: Measures the statistical probability (percentage from 0% to 100%) that the CVE will be exploited on the internet in the next 30 days. Vulnerabilities with EPSS > 0.36 must be handled with immediate priority.
3. **CISA KEV (Known Exploited Vulnerabilities Catalog)**: Official catalog of vulnerabilities with active evidence of exploitation by criminal groups (*Wild Exploits*). If a CVE is in CISA KEV, its remediation is mandatory regardless of the CVSS score.

---

## 📦 3. SBOM (Software Bill of Materials) and VEX Standards

### 3.1 Official Formats

- **CycloneDX (OWASP Foundation)**: Specialized in application security, inventory of direct and transitive dependencies, cloud services, VEX (*Vulnerability Exploitability eXchange*) formulation, and compliance forms.
- **SPDX (Linux Foundation / ISO/IEC 5962:2021)**: International standard for open-source license compliance and file and package provenance.

### 3.2 NTIA Minimum Elements for SBOM

1. **Supplier Name**.
2. **Component Name**.
3. **Component Version**.
4. **Unique Identifiers**: Package URL (`purl`) and Common Platform Enumeration (`CPE`).
5. **Dependency Relationship**: Direct vs. transitive (*DependsOn*).
6. **SBOM Metadata Author**.
7. **Generation Timestamp**.

### 3.3 VEX (Vulnerability Exploitability eXchange) Forms

VEX lets maintainers formally declare whether a vulnerability discovered in a dependency affects the application or not:

- `not_affected`: The vulnerable code is neither imported nor executed (with justification: `code_not_reachable`, `vulnerable_code_cannot_be_controlled_by_adversary`, `inline_mitigations_already_exist`).
- `affected`: The vulnerability is exploitable in the application context.
- `fixed`: The vulnerability has been fixed in the current version.
- `under_investigation`: Under analysis by the security team.

---

## 📜 4. Open-Source License Compliance (OSS License Compliance)

| License Category | Examples | Impact / Restrictions |
| :--- | :--- | :--- |
| **Permissive** | MIT, Apache 2.0, BSD-2/3-Clause, ISC | Allows commercial and closed-source use with preservation of the copyright notice. |
| **Weak Copyleft** | LGPL v2.1/v3, MPL 2.0, EPL 2.0 | Modifications to the library itself must be opened; client code may remain proprietary if dynamically linked. |
| **Strong Copyleft (Viral)** | GPL v2/v3, AGPL v3 | Requires any derived or distributed software that uses the library to open its full source code under the same license. |

---

## 🔒 5. SLSA Provenance and Cryptographic Signing (Sigstore / Cosign)

### 5.1 SLSA v1.0 Levels

- **SLSA Build L1**: Automated build process generating a basic provenance attestation.
- **SLSA Build L2**: Build run on a managed CI/CD runner with version control and cryptographically signed provenance.
- **SLSA Build L3**: Hermetic and ephemeral build in an isolated environment, preventing tampering and guaranteeing strict reproducibility.

### 5.2 Image Signing and SBOM Attachment

```bash
# Assinar imagem de contêiner usando OIDC (Keyless via Sigstore)
cosign sign --yes ghcr.io/empresa/app:v1.0.0

# Anexar e assinar o SBOM CycloneDX à imagem no registro OCI
cosign attach sbom --sbom sbom.cyclonedx.json ghcr.io/empresa/app:v1.0.0
cosign sign --yes --attachment sbom ghcr.io/empresa/app:v1.0.0

# Verificar assinatura no Kubernetes Admission Controller
cosign verify --certificate-identity-regexp "https://github.com/empresa/.*" \
              --certificate-oidc-issuer "https://token.actions.githubusercontent.com" \
              ghcr.io/empresa/app:v1.0.0
```

---

## 🛑 6. Protection Against Specific Supply Chain Vectors

1. **Dependency Confusion**: Register private scopes `@empresa` in the public registry (npm/PyPI), or configure the package manager to query only the internal private registry for corporate packages.
2. **Typosquatting**: Use phonetic and string similarity checking tools in PR pipelines before accepting new libraries.
3. **Maintainer Account Takeover**: Use tools that assess the *OpenSSF Scorecard* (maintainer MFA, branch protection, recent commit activity).

---

## 🔗 Integration with Other Skills in the Repository

- **[program-owasp-dependency-check](../../tooling/program-owasp-dependency-check/SKILL.md)**: Complete operational guide to the OWASP Dependency-Check tool (CLI, Maven, Gradle, and NVD API v2).
- **[sast-code-review](../sast-code-review/SKILL.md)**: Complements library analysis with vulnerability auditing in proprietary code.
- **[devsecops-engineer](../../operations/devsecops-engineer/SKILL.md)**: Orchestration of SCA pipelines, SBOM generation, and Quality Gates in CI/CD.
- **[program-containers](../../../infrastructure/program-containers/SKILL.md)**: Auditing and signing of container images and operating system base packages.
