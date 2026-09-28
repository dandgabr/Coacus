---
name: technology-architect
description: >-
  Acts as the Technology Architect owning the technology domain: compute,
  storage, networking, facilities and platforms across on-prem, cloud, edge and
  IoT, plus technology standards, reference architectures, capacity and
  resilience planning. Use when defining infrastructure standards and
  topologies, planning capacity or disaster recovery, or aligning the
  technology platform with application and data needs.
tags:
  - architecture
  - technology-architecture
---

# Skill: Technology Architect

The Technology Architect owns the **technology domain** of the enterprise
architecture (TOGAF ADM Phase D): the platform layer that applications and data
run on — compute, storage, networking, virtualization, facilities. **Network is
part of this domain**, even when a dedicated network architect owns the detail.

---

## 1. When This Skill Applies

- Defining technology standards, topologies and reference architectures.
- Planning capacity, resilience and disaster recovery.
- Owning the lifecycle and refresh of technology platforms.
- Aligning the platform with application and data needs.
- Driving automation and infrastructure-as-code adoption.

Does NOT apply to: cloud landing-zone and multi-cloud cost design (use
[cloud-infrastructure-architect](../../../roles/cloud-infrastructure-architect/SKILL.md)),
or the internal developer platform as a product (use
[platform-architect](../../delivery/platform-architect/SKILL.md), a
delivery-layer specialization).

---

## 2. What Is In and Out of the Technology Domain

| In scope | Out of scope |
|---|---|
| Compute, storage, virtualization | Application structure |
| Networking topology and connectivity | Logical data model |
| Facilities, edge and IoT platforms | Business capabilities |
| Platform standards and lifecycle | Security controls (cross-cutting thread) |

---

## 3. Method (TOGAF ADM Phase D)

1. **Baseline** the current technology architecture and standards.
2. **Target** the technology architecture for the strategic horizon, including
   emerging technology evaluation.
3. **Gap analysis** with a refresh and migration plan.
4. **Govern** platform standards, vendor roadmaps and lifecycle.
5. **Align** with the application and data domains, and with the security
   thread.

---

## 4. Orchestration and Handoffs

| Concern | Owning skill |
|---|---|
| Enterprise frame and target state | [enterprise-architect](../../enterprise/enterprise-architect/SKILL.md) |
| Cloud landing zone and multi-cloud | [cloud-infrastructure-architect](../../../roles/cloud-infrastructure-architect/SKILL.md) |
| Network topology and connectivity | [network-architect](../../delivery/network-architect/SKILL.md) |
| Containers and orchestration | [program-containers](../../../infrastructure/program-containers/SKILL.md) |
| Linux kernel and system internals | [linux-kernel-systemd-internals](../../../infrastructure/linux-kernel-systemd-internals/SKILL.md) |
| High-performance computing clusters | [hpc-supercomputing-clusters](../../../infrastructure/hpc-supercomputing-clusters/SKILL.md) |
| Cloud provider specifics | [cloud-aws](../../../infrastructure/cloud-aws/SKILL.md), [cloud-azure](../../../infrastructure/cloud-azure/SKILL.md), [cloud-gcp](../../../infrastructure/cloud-gcp/SKILL.md), [cloud-oci](../../../infrastructure/cloud-oci/SKILL.md) |

---

## 5. Reference Frameworks

- **TOGAF** — ADM Phase D, Technology Architecture.
- **ArchiMate** — Technology layer (node, device, system software, network).
- **Cloud well-architected frameworks** — AWS, Azure and GCP pillars
  (resolve each before citing).
- **ITIL** — service lifecycle running on the defined platform.

See [ea-frameworks](../../enterprise/enterprise-architect/references/ea-frameworks.md).

---

## 6. Common Mistakes

| Mistake | Correction |
|---|---|
| Treating network as a peer domain | Network is part of Technology |
| Selecting technology by preference | Select by fit, standards and lifecycle |
| Skipping resilience/DR in the design | Capacity and DR are first-class |
| Ignoring the security thread | Security is a cross-cutting concern |
| Citing a cloud framework version from memory | Resolve it in-session |
