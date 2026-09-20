---
name: supply-chain-threat-modeling
description: Acts as a specialist in threat modeling the software supply chain, structuring the SLSA A-I threat taxonomy, dependency and manifest confusion, typosquatting, maintainer account takeover, repo hijacking, protestware, build-cache poisoning and forged provenance into an attacker model.
metadata:
  type: defensive
  phase: recon
---

# Supply Chain Threat Modeling

This skill guides the AI to reason about *who* attacks the supply chain and *how*, complementing the controls in the related supply-chain skills.

---

## 🎯 1. The SLSA Threat Taxonomy (A-I)

| Group | Threats |
| :--- | :--- |
| **Source (A-C)** | A: producer compromise; B: source tampering; C: forged source metadata |
| **Build (D-F)** | D: compromised build platform; E: use of compromised dependencies; F: tampering with build parameters |
| **Distribution (G)** | G: artifact substitution or channel compromise |
| **Package selection (H)** | H: dependency confusion, typosquatting, namespace reuse |
| **Usage (I)** | I: consumption of malicious or vulnerable artifacts at runtime |

Dependency threats recurse: each dependency has its own A-I surface.

---

## 🧪 2. Attack Scenarios

- **Dependency confusion**: publish a public package with the same name as an internal one, hoping the resolver prefers the public registry.
- **Manifest confusion**: a package's published metadata disagrees with its own manifest, so scanners see different dependencies than the build uses.
- **Typosquatting / combosquatting**: names close to popular packages.
- **Maintainer account takeover**: compromise of a maintainer's credentials or of a dormant package.
- **Repo hijacking**: an abandoned repository is adopted and weaponized.
- **Protestware**: a legitimate maintainer ships destructive or telemetry code deliberately.
- **Build-cache poisoning**: a shared cache is poisoned so later builds inherit malicious artifacts.
- **Forged provenance**: attestations are fabricated to pass verification.

---

## 🛡️ 3. Mitigation Mapping

For each threat, name a preventive, detective and recovery control, and assign an owner. Examples:

| Threat | Preventive | Detective |
| :--- | :--- | :--- |
| Dependency confusion | Scoped registries, resolver policy | Audit logs of new public packages matching internal names |
| Maintainer takeover | MFA, least privilege, short-lived publish tokens | Monitor maintainer and release anomalies |
| Build-cache poisoning | Per-trust-boundary cache isolation | Verify provenance on every consumption |
| Forged provenance | Signed attestations with pinned builders | Transparency-log monitoring |

---

## 🔗 4. Integration with Other Skills

- For the controls, see the [software-supply-chain-security](../../appsec/software-supply-chain-security/SKILL.md) skill.
- For signing and verification, see the [program-sigstore-cosign](../../tooling/program-sigstore-cosign/SKILL.md) skill.
- For the general adversary model, see the [threat-modeler](../threat-modeler/SKILL.md) skill.
- For vendor risk, see the [third-party-risk-management](../../grc/third-party-risk-management/SKILL.md) skill.
