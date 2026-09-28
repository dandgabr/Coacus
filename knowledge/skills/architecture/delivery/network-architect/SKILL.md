---
name: network-architect
description: >-
  Acts as the Network Architect owning the network topology: LAN/WAN/WLAN,
  data-center fabric, routing and switching, addressing, SD-WAN, DNS, load
  balancing, QoS and network resilience. Use when designing network topology and
  segmentation, planning addressing and routing, or specifying network capacity
  and vendor roadmaps.
tags:
  - architecture
  - network-architecture
---

# Skill: Network Architect

The Network Architect owns the **network layer** inside the Technology domain:
topology, connectivity, addressing, routing and resilience. It is a delivery
specialization of the technology domain, coordinated with the network security
architect for control points.

---

## 1. When This Skill Applies

- Designing network topology, segmentation and addressing.
- Defining routing, QoS and resiliency strategies.
- Specifying hardware/software and capacity.
- Owning network standards and vendor roadmaps.
- Ensuring network observability and performance.

Does NOT apply to: security control points on the network (use the security
thread — [network-security-onprem-cloud](../../../security/operations/network-security-onprem-cloud/SKILL.md)),
or the overall technology domain (use [technology-architect](../../domains/technology-architect/SKILL.md)).

---

## 2. Design Axes

| Axis | Decision |
|---|---|
| Topology | Campus, data center, WAN, cloud interconnect, edge |
| Segmentation | VLAN/VRF zones, trust boundaries, microsegmentation |
| Routing | Interior/exterior protocols, summarization, failover |
| Addressing | IP plan, dual-stack, NAT strategy |
| Performance | QoS classes, bandwidth, latency budgets |
| Resilience | Redundancy, convergence, DDoS absorption |

---

## 3. Method

1. **Baseline** the current topology, addressing and performance.
2. **Target** the topology for the required capacity, resilience and
   segmentation.
3. **Gap analysis** with a migration and refresh plan.
4. **Govern** network standards and vendor roadmaps.
5. **Observe**: flows, latency, errors and capacity headroom.

---

## 4. Orchestration and Handoffs

| Concern | Owning skill |
|---|---|
| Technology domain and standards | [technology-architect](../../domains/technology-architect/SKILL.md) |
| Enterprise frame | [enterprise-architect](../../enterprise/enterprise-architect/SKILL.md) |
| Network security controls | [network-security-onprem-cloud](../../../security/operations/network-security-onprem-cloud/SKILL.md) |
| Segmentation and microsegmentation | [network-segmentation-microsegmentation](../../../security/operations/network-segmentation-microsegmentation/SKILL.md) |
| Cloud network architecture | [cloud-infrastructure-architect](../../../roles/cloud-infrastructure-architect/SKILL.md) |
| Network flow discovery and monitoring | [network-flow-discovery](../../../mapping/network-flow-discovery/SKILL.md) |
| DNS security | [dns-security-protective-dns](../../../security/operations/dns-security-protective-dns/SKILL.md) |

---

## 5. Reference Frameworks

- **Vendor design guides** — the reference network architectures (resolve the
  edition before citing).
- **TOGAF / ArchiMate** — Technology layer placement.
- **Zero-trust network access** — for the security posture of connectivity.

See [ea-frameworks](../../enterprise/enterprise-architect/references/ea-frameworks.md).

---

## 6. Common Mistakes

| Mistake | Correction |
|---|---|
| Treating network as a peer EA domain | It is part of Technology |
| No addressing or segmentation plan | Both are first-class design artifacts |
| Ignoring convergence and failover | Resilience must be designed, not assumed |
| No observability | Flows and latency are measured continuously |
| Confusing network with network security | Coordinate, do not conflate |
