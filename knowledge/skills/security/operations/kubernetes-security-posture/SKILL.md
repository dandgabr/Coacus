---
name: kubernetes-security-posture
description: Acts as a Kubernetes Security Posture specialist covering CIS Kubernetes Benchmark conformance, Pod Security Standards and Admission, RBAC least privilege, NetworkPolicy, secrets and etcd encryption, API-server and kubelet hardening, admission policy engines and KSPM tooling.
metadata:
  type: defensive
  phase: recon
---

# Kubernetes Security Posture

This skill guides the AI to harden a Kubernetes cluster against both misconfiguration and attack, aligned with the **CIS Kubernetes Benchmark** and the **NSA/CISA Kubernetes Hardening Guide**.

---

## 📋 1. Benchmarks and Guides

- **CIS Kubernetes Benchmark** and its managed variants (EKS, AKS, GKE, OKE, OpenShift) define the auditable checks.
- **NSA/CISA Kubernetes Hardening Guidance** frames the priorities: scan and harden the supply chain, scan workloads, use Pod Security, network separation and firewalls, harden authentication and authorization, and log and audit.
- **OWASP Kubernetes Top 10 (2025)** names the risk categories, including **K08 cluster-to-cloud lateral movement**.

---

## 🔐 2. Control Plane and Node Hardening

- **API server**: disable anonymous auth, restrict insecure ports, enable audit logging, limit who can reach it.
- **etcd**: encrypt secrets at rest with a KMS provider, restrict access, back up securely.
- **kubelet**: disable anonymous auth, restrict the read-only and write ports, require authorization.
- **Nodes**: patch the OS, restrict node access, and use a minimal OS where possible.

---

## 🧱 3. Workload and Namespace Controls

- **Pod Security Admission** with the Baseline or Restricted profile per namespace; do not leave it unset.
- **RBAC least privilege**: no wildcard verbs/resources for human or workload roles; audit ClusterRoleBindings.
- **Service accounts**: disable automount where not needed and use projected short-lived tokens.
- **NetworkPolicy**: default-deny ingress and egress; block metadata access (169.254.169.254) to prevent cluster-to-cloud movement.
- **Admission policy engines**: OPA/Gatekeeper, Kyverno or ValidatingAdmissionPolicy to enforce image signing, resource limits and forbidden capabilities.

---

## 🛠️ 4. Assessment Tooling

- **kube-bench** for CIS checks; **Kubescape** for NSA-CISA/CIS/MITRE frameworks; **Trivy** and its operator for image, config, secret and RBAC scanning; **KSPM** for continuous posture.
- Run in audit mode first, then enforce; a policy that breaks workloads gets disabled by operators.

---

## 🔗 5. Integration with Other Skills

- For runtime isolation and escapes, see the [container-runtime-security](../container-runtime-security/SKILL.md) skill.
- For the attack chain, see the [kubernetes-attack-paths](../../offensive/kubernetes-attack-paths/SKILL.md) skill.
- For IaC scanning of the cluster manifests, see the [iac-security-scanning](../../cloud/iac-security-scanning/SKILL.md) skill.
- For cloud identity boundaries, see the [cloud-workload-identity-federation](../../cloud/cloud-workload-identity-federation/SKILL.md) skill.
