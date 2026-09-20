---
name: software-supply-chain-security
description: "Acts as a Specialist in Software Supply Chain Security, Software Composition Analysis (SCA), and Dependency Management based on Cassie Crossley and NIST SSDF / SP 800-161. Covers SBOM generation and auditing (CycloneDX v1.7.2 / ECMA-424 and SPDX v3.0.1), VEX, SLSA v1.2 provenance (Build and Source tracks), cryptographic signing with Sigstore/Cosign and in-toto, vulnerability mitigation (CVEs, GHSA, EPSS, CISA KEV), open-source license auditing (GPL, AGPL, Apache, MIT), lockfile pinning, call-graph reachability analysis, and defense against typosquatting, dependency confusion and protestware."
metadata:
  type: defensive
  phase: recon
  tools: [owasp-dependency-check, syft, grype, trivy, snyk, cosign, slsa-verifier]
  mitre: [T1195, T1195.001, T1195.002, T1140]
---

# Software Supply Chain Security (Supply Chain Security & SCA)

This skill establishes the canonical guidelines for auditing, protecting, and managing vulnerabilities in third-party libraries (*Software Composition Analysis - SCA*), reachability analysis, license compliance, and end-to-end integrity verification in the software and firmware supply chain, grounded in the work of **Cassie Crossley** (*Software Supply Chain Security: Securing the End-to-end Supply Chain for Software, Firmware, and Hardware*), the **SLSA (Supply-chain Levels for Software Artifacts v1.2)** framework, **NIST SP 800-161 Rev. 1**, and the **NIST SSDF (SP 800-218)**.

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

- **CycloneDX (OWASP Foundation / ECMA-424)**: Specialized in application security, inventory of direct and transitive dependencies, cloud services, VEX (*Vulnerability Exploitability eXchange*) formulation, and compliance forms. Version 1.7.2 is the current release (github.com/CycloneDX/specification, resolved 2026-09-20) and is standardized as ECMA-424.
- **SPDX (Linux Foundation / ISO/IEC 5962:2021, SPDX v3.0.1)**: International standard for open-source license compliance and file and package provenance. SPDX 3.0.1 uses a modular profile model (Core, Software, Security, Licensing, Dataset, AI, Build) with native VEX relationships and CVSS v4.0 / EPSS / SSVC vocabularies.

### 3.2 SBOM Minimum Elements (CISA 2026)

The **CISA 2026 Minimum Elements for an SBOM** replaced the 2021 NTIA guidance:

1. **Supplier Name**.
2. **Component Name**.
3. **Component Version**.
4. **Unique Identifiers**: Package URL (`purl`) and Common Platform Enumeration (`CPE`).
5. **Dependency Relationship**: Direct vs. transitive (*DependsOn*).
6. **SBOM Metadata Author**.
7. **Generation Timestamp**.
8. **SBOM Data Fields, Practices and Processes** as defined by the 2026 CISA guidance, plus the supplemental **SBOM for AI** minimum elements.

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

### 5.1 SLSA v1.2 Tracks and Levels

SLSA v1.2 is the current specification (v1.0/v1.1 are retired) and organizes requirements into two tracks:

- **Build Track**:
  - **SLSA Build L1**: Automated build process generating a basic provenance attestation.
  - **SLSA Build L2**: Build run on a managed CI/CD platform producing authenticated, signed provenance.
  - **SLSA Build L3**: Hardened, isolated and ephemeral build producing unforgeable provenance.
  - Note: "Isolated" is NOT "Hermetic". A hermetic (no-network) build and byte-level reproducibility are explicit future directions and MUST NOT be presented as an L3 guarantee. Consumers can rely on a **VSA (Verification Summary Attestation)** from a trusted intermediary instead of re-verifying provenance themselves.
- **Source Track** (new in v1.2): L1 version-controlled source, L2 history and provenance, L3 continuous technical controls, L4 two-party review.
- **Threat model (A–I)**: Source (A–C), Build (D–F), Distribution (G), Package selection (H: dependency confusion, typosquatting) and Usage (I).

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

1. **Dependency Confusion**: Register private scopes `@company` in the public registry (npm/PyPI), or configure the package manager to query only the internal private registry for corporate packages.
2. **Typosquatting**: Use phonetic and string similarity checking tools in PR pipelines before accepting new libraries.
3. **Maintainer Account Takeover**: Use tools that assess the *OpenSSF Scorecard* (maintainer MFA, branch protection, recent commit activity).
4. **Manifest Confusion**: Validate that the dependency metadata a registry serves matches the package's own manifest; a package can lie about its dependencies.
5. **Protestware and Repo Hijacking**: Pin dependencies, monitor maintainer changes, and treat unexpected telemetry or destructive updates as an incident.
6. **Build-Cache Poisoning and Forged Provenance**: Isolate build caches per trust boundary and verify provenance with a fixed builder identity; never reuse caches across unreviewed inputs.
7. **Trusted Publishing**: Replace long-lived registry tokens with OIDC-based trusted publishing (npm, PyPI) so CI mints short-lived credentials bound to the repository identity.

---

## 🔗 Integration with Other Skills in the Repository

- **[program-owasp-dependency-check](../../tooling/program-owasp-dependency-check/SKILL.md)**: Complete operational guide to the OWASP Dependency-Check tool (CLI, Maven, Gradle, and NVD API v2).
- **[sast-code-review](../sast-code-review/SKILL.md)**: Complements library analysis with vulnerability auditing in proprietary code.
- **[devsecops-engineer](../../operations/devsecops-engineer/SKILL.md)**: Orchestration of SCA pipelines, SBOM generation, and Quality Gates in CI/CD.
- **[program-containers](../../../infrastructure/program-containers/SKILL.md)**: Auditing and signing of container images and operating system base packages.

## 🔢 Version Sources

Moving release pins in this skill were resolved 2026-09-20:

- **CVSS v3.1** (verified) — first.org/cvss
- **CVSS v4.0** (verified) — first.org/cvss
- **CycloneDX 1.7.2** (verified) — github.com/CycloneDX/specification (latest release)
- **NIST SP 800-161 Rev. 1** (verified) — csrc.nist.gov/pubs/sp/800/161/r1/final
- **NIST SP 800-218 v1.1** (verified) — csrc.nist.gov/pubs/sp/800/218/final
- **SLSA v1.2** (verified) — slsa.dev/spec/v1.2
- **SPDX 3.0.1** (verified) — github.com/spdx/spdx-spec (latest release)
