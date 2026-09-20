---
name: program-sbom-tooling
description: Acts as an operational specialist for SBOM generation, consumption and conversion (Syft, Grype, cdxgen, Trivy, OSV-Scanner, protobom/bomctl), covering CycloneDX and SPDX formats, VEX authoring, format conversion and continuous SBOM management.
metadata:
  type: defensive
  phase: recon
---

# SBOM Tooling Operations

This skill guides the AI to generate, convert, verify and continuously manage Software Bills of Materials across languages, container images and firmware.

---

## 🧰 1. Generation

- **Syft**: catalogues packages and files across images, directories and archives; emits CycloneDX and SPDX.
- **cdxgen**: deep dependency resolution per ecosystem, including transitive and container layers.
- **Trivy**: image, filesystem, repository, VM and Kubernetes scanning with SBOM, CVE, misconfiguration, secret and license output.
- **Protobom / bomctl**: format-neutral intermediate representation and CLI for pushing, pulling and merging SBOMs.

Always generate the SBOM from the actual artifact, not from the manifest alone.

---

## 🔄 2. Conversion and Interoperability

- **SPDX 3.0.1** uses a modular profile model; **CycloneDX 1.7 (ECMA-424)** is optimized for security use cases.
- Convert between formats deliberately and record the conversion; conversions lose fields.
- Keep the SBOM attached to the artifact (for example, as an OCI attachment) so the inventory travels with the software.

---

## ⚠️ 3. VEX Authoring

- VEX states: `not_affected`, `affected`, `fixed`, `under_investigation`.
- `not_affected` requires a justification: `code_not_reachable`, `vulnerable_code_cannot_be_controlled_by_adversary`, or `inline_mitigations_already_exist`.
- Publish VEX alongside the SBOM so consumers can triage without re-deriving reachability.
- Keep VEX claims current; a stale VEX is worse than none.

---

## 🔍 4. Continuous Management

1. Inventory every artifact and its SBOM.
2. Re-scan on new advisories, not only at build time.
3. Track component provenance and ownership.
4. Alert on new critical components or license changes entering the estate.

---

## 🔗 5. Integration with Other Skills

- For signing and attestation, see the [program-sigstore-cosign](../program-sigstore-cosign/SKILL.md) skill.
- For the SCA methodology, see the [software-supply-chain-security](../../appsec/software-supply-chain-security/SKILL.md) skill.
- For the dependency-check tool, see the [program-owasp-dependency-check](../program-owasp-dependency-check/SKILL.md) skill.
