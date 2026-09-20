---
name: secure-sdlc-ssdf
description: Acts as a Secure SDLC specialist applying the NIST SSDF (SP 800-218) and its AI profile (SP 800-218A). Covers the four practice groups Prepare the Organization, Protect the Software, Produce Well-Secured Software and Respond to Vulnerabilities, with gates, evidence and threat modeling woven into the development lifecycle.
metadata:
  type: defensive
  phase: recon
---

# Secure Software Development Lifecycle (NIST SSDF)

This skill guides the AI to build and assess a **Secure Software Development Lifecycle** grounded in **NIST SP 800-218 (Secure Software Development Framework, SSDF v1.1)** and its generative-AI companion **SP 800-218A**. The SSDF is outcome-oriented: it defines practices and tasks, not a fixed process, so it fits waterfall, agile and CI/CD models.

---

## 🧭 1. The Four Practice Groups

1. **PO - Prepare the Organization**: define security requirements, roles and secure development environments (PO.5); establish a vulnerability disclosure process.
2. **PS - Protect the Software**: control access to source and build systems, protect code integrity, and generate **provenance data** for each release (PS.3.2).
3. **PW - Produce Well-Secured Software**: threat modeling at design time, reuse of vetted components, secure coding, code review, and executable testing for security.
4. **RV - Respond to Vulnerabilities**: identify and confirm vulnerabilities, assess and remediate risk, and continuously improve.

---

## 🚪 2. Recommended Gates and Evidence

| Phase | Gate | Evidence |
| :--- | :--- | :--- |
| Requirements | Security requirements and abuse cases defined | Requirement register with acceptance criteria |
| Design | Threat model reviewed | Data-flow diagram, trust boundaries, STRIDE/PASTA findings |
| Build | SAST, SCA and secret scanning clean or triaged | Scan reports with disposition |
| Test | DAST/IAST against a deployed build | Test report and coverage of the risk model |
| Release | Signed artifacts with provenance | Attestation and SBOM |
| Operate | Vulnerability intake and patch SLA | Ticket log and mean time to remediate |

Every gate must define what "fail" means. A gate that cannot reject an artifact is documentation, not control.

---

## 🛡️ 3. Secure Development Environment (PO.5)

- Isolate developer and build environments; protect credentials with short-lived, federated identities rather than long-lived secrets.
- Make the secure path the default path: templates, linters, pre-commit checks and pinned dependencies.
- Keep an inventory of components and their provenance.

---

## 🤖 4. The AI Profile (SP 800-218A)

When AI or generative models are part of the product, extend the SSDF with the AI profile's additional practices: data provenance and consent for training data, model evaluation for safety and security, and documentation of model limitations. Cross-reference the [ai-governance-assurance](../../ai/ai-governance-assurance/SKILL.md) and [ai-llm-slm-security](../../ai/ai-llm-slm-security/SKILL.md) skills.

---

## 🔗 5. Integration with Other Skills

- For dependency and build-chain controls, see the [software-supply-chain-security](../software-supply-chain-security/SKILL.md) skill.
- For design-stage modeling, see the [threat-modeler](../../operations/threat-modeler/SKILL.md) skill.
- For pipeline automation and security gates, see the [devsecops-engineer](../../operations/devsecops-engineer/SKILL.md) skill.
- For the OWASP risk baseline, see the [owasp-top-10-2025](../owasp-top-10-2025/SKILL.md) skill.
