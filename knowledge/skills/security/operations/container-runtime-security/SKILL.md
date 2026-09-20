---
name: container-runtime-security
description: Acts as a Container Runtime Security specialist covering namespace and cgroup isolation, seccomp, AppArmor/SELinux and capabilities, gVisor/Kata sandboxing, container escapes (CVE-2019-5736, CVE-2024-21626), and runtime detection with Falco/Tetragon/Tracee.
metadata:
  type: defensive
  phase: actions
---

# Container Runtime Security

This skill guides the AI to contain a container compromise and detect an escape in progress.

---

## 🧱 1. Isolation Primitives

- **Namespaces** isolate process, network, mount, IPC, UTS, user and cgroup views.
- **cgroups v2** limit and account for CPU, memory and I/O; cgroup v1's `release_agent` has been an escape vector.
- **Capabilities**: drop `ALL` and add back only what is required; `CAP_SYS_ADMIN` and `CAP_NET_RAW` are high risk.
- **seccomp**: apply the runtime default profile at minimum; a custom profile narrows further.
- **AppArmor/SELinux**: mandatory access control per container.
- **Rootless/userns**: map the container root to an unprivileged host user to reduce escape impact.

---

## 🏃 2. Sandboxing

- **gVisor (`runsc`)**: a userspace application kernel that intercepts syscalls; not a VM, not a seccomp filter.
- **Kata Containers**: hardware virtual machines with a container UX; stronger isolation at some performance cost.
- Use these for untrusted or multi-tenant workloads.

---

## 🚪 3. Container Escapes

- **CVE-2019-5736**: runc overwrote the host binary via `/proc/self/exe` during `runc exec` or a malicious image.
- **CVE-2024-21626** ("Leaky Vessels"): a leaked file descriptor let a container's working directory land in the host mount namespace. Fixed in runc 1.1.12.
- Mitigations: patch the runtime, never mount the runtime socket into a container, avoid `runc exec` from untrusted contexts, and use read-only, non-privileged containers.

---

## 🔍 4. Runtime Detection

- **Falco**, **Tetragon** and **Tracee** watch syscalls and process behavior via eBPF.
- Detect: shell spawned in a container, unexpected outbound connections, reads of sensitive mount points, writes to the container image layers, privilege escalation syscalls, and process injection.
- **Tetragon** can enforce (kill/deny) as well as detect; enforcement needs careful tuning to avoid breaking production.
- Ship alerts to the SIEM and map them to ATT&CK containers techniques.

---

## 🔗 5. Integration with Other Skills

- For the cluster posture, see the [kubernetes-security-posture](../kubernetes-security-posture/SKILL.md) skill.
- For the attack chain, see the [kubernetes-attack-paths](../../offensive/kubernetes-attack-paths/SKILL.md) skill.
- For eBPF observability, see the [k8s-container-mapping](../../../mapping/k8s-container-mapping/SKILL.md) skill.
- For the container build and registry, see the [program-containers](../../../infrastructure/program-containers/SKILL.md) skill.
