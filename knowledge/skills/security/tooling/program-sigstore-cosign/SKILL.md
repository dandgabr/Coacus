---
name: program-sigstore-cosign
description: Acts as an operational specialist for artifact signing and attestation with Sigstore (Fulcio, Rekor, Cosign). Covers keyless OIDC signing, self-managed keys, bundle format, attestations, verification by identity and issuer, gitsign and admission policy enforcement.
metadata:
  type: defensive
  phase: weaponize
---

# Sigstore and Cosign Operations

This skill guides the AI to sign, attest and verify software artifacts so consumers can prove who built them and from what source.

---

## ✍️ 1. Keyless Signing

- A workload obtains an OIDC identity token, exchanges it with **Fulcio** for a short-lived signing certificate, signs the artifact, and records the signature in the append-only **Rekor** transparency log.
- Verification is by **identity and issuer**, not by a pre-shared key: the verifier checks that the signature came from the expected identity (for example, a specific CI workflow) via the expected OIDC issuer.
- Signatures are distributed as a **bundle** (signature, certificate, inclusion proof, timestamp) so verification is offline-capable.

---

## 🔑 2. Self-Managed Keys

- Use a long-lived keypair when keyless identity is not available, and store the private key in an HSM or KMS.
- Support PKCS#11 and cloud KMS backends.
- Publish the public key where consumers can retrieve it, and rotate on a schedule.

---

## 📎 3. Attachments and Attestations

- Attach the **SBOM** to the image and sign the attachment.
- Emit **attestations** (in-toto statements) for build provenance, vulnerability scans and test results.
- Sign commits with `gitsign` so the source history itself is attributable.

---

## 🚪 4. Verification in the Pipeline and at Admission

1. Verify the signature against the pinned identity and issuer, not a wildcard.
2. Verify the attestation predicates you actually depend on (provenance, SBOM).
3. Enforce at admission (a policy controller in Kubernetes, or a gate in the registry) so an unsigned or unverified artifact cannot run.
4. Fail closed: an unreachable transparency log or verifier must not silently pass.

---

## 🔗 5. Integration with Other Skills

- For the SBOM content and formats, see the [program-sbom-tooling](../program-sbom-tooling/SKILL.md) skill.
- For the supply-chain threat model, see the [supply-chain-threat-modeling](../../operations/supply-chain-threat-modeling/SKILL.md) skill.
- For the overall SCA approach, see the [software-supply-chain-security](../../appsec/software-supply-chain-security/SKILL.md) skill.
