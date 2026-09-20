---
name: kubernetes-attack-paths
description: Acts as an offensive Kubernetes specialist covering privileged-pod escape, hostPath and host-mount abuse, service-account token theft, cluster-admin escalation, SSRF to kubelet and etcd, and cluster-to-cloud lateral movement.
metadata:
  type: offensive
  phase: exploitation
---

# Kubernetes Attack Paths

This skill guides the AI to emulate and assess the Kubernetes-internal kill chain, from a compromised pod to cluster and cloud control.

---

## 🎯 1. From Pod to Node

- **Privileged pod**: a container with `privileged: true` can access host devices and often escape to the node.
- **hostPath / host mounts**: mounting the host filesystem or the container runtime socket (`docker.sock`, `containerd.sock`) gives direct host control.
- **hostPID / hostNetwork**: sharing the host namespaces enables process and network attacks.
- **Runtime escapes**: known vulnerabilities (for example, CVE-2019-5736 and CVE-2024-21626 in runc) allow escaping to the host; patch the runtime.

---

## 🔑 2. From Pod to Cluster

- **Service-account token theft**: every pod has a token mounted by default; stolen tokens grant whatever RBAC the account holds.
- **cluster-admin bindings**: over-broad roles (wildcard verbs/resources) turn any token into cluster control.
- **SSRF to kubelet (10250) or etcd (2379)**: an in-cluster SSRF can reach the kubelet API or the datastore.
- **Admission bypass**: permissive admission policies or a controller that can be tricked allow privileged workloads to be created.

---

## ☁️ 3. Cluster to Cloud (Lateral Movement)

- **Instance metadata (169.254.169.254)**: pods that can reach the metadata endpoint may steal node credentials; block it with NetworkPolicy egress and enforce authenticated metadata.
- **Workload identity abuse**: a pod with a highly privileged cloud role can act in the cloud account (OWASP K8s Top 10 2025, K08).
- **Secrets in the cluster**: mounted cloud credentials, service-account JSON keys and Helm values are common findings.

---

## 🛡️ 4. Defensive Mapping

| Attack step | Control |
| :--- | :--- |
| Privileged pod | Pod Security Admission (Restricted), admission policy |
| hostPath | Deny host mounts; use CSI with scoped volumes |
| Token theft | Disable automount, use projected short-lived tokens, least-privilege RBAC |
| Metadata access | Egress NetworkPolicy, IMDSv2/Workload Identity |
| Runtime escape | Patch runc/containerd; gVisor/Kata for untrusted workloads |

---

## 🔗 5. Integration with Other Skills

- For the defensive posture, see the [kubernetes-security-posture](../../operations/kubernetes-security-posture/SKILL.md) skill.
- For container runtime defense, see the [container-runtime-security](../../operations/container-runtime-security/SKILL.md) skill.
- For cloud lateral movement, see the [pentest-cloud-aws-azure-gcp](../../offensive/pentest-cloud-aws-azure-gcp/SKILL.md) skill.
- For entitlement analysis, see the [ciem-cloud-entitlements](../../iam/ciem-cloud-entitlements/SKILL.md) skill.
