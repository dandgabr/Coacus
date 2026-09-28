---
name: platform-architect
description: >-
  Acts as the Platform Architect owning the internal developer platform as a
  product: platform capabilities, golden paths, self-service provisioning,
  tenancy and reliability. Use when defining a developer platform, designing
  golden paths and self-service, or balancing platform opinionation against team
  autonomy.
tags:
  - architecture
  - platform-architecture
---

# Skill: Platform Architect

The Platform Architect treats the **internal platform as a product**: the
capabilities product teams consume, the golden paths they follow and the
self-service that makes secure, fast delivery the default. It is a delivery
specialization of the technology domain.

---

## 1. When This Skill Applies

- Defining the platform's capabilities and golden paths.
- Owning platform standards, tenancy and self-service provisioning.
- Balancing platform opinionation against team autonomy.
- Managing platform reliability and cost-to-serve.
- Deciding what is a platform capability versus a team responsibility.

Does NOT apply to: the underlying technology platforms and facilities (use
[technology-architect](../../domains/technology-architect/SKILL.md)), or CI/CD
pipeline design within a team (use the DevOps discipline).

---

## 2. The Platform as a Product

| Concern | Decision |
|---|---|
| Capabilities | What the platform offers as a service |
| Golden paths | The paved road that is also the secure road |
| Self-service | Provisioning without a ticket |
| Tenancy | Isolation and quotas |
| Reliability | Platform SLOs |
| Cost-to-serve | Unit economics of platform capabilities |

The platform makes the **safe path the default path**: a golden path that is
slower or less convenient than the unsafe one will be bypassed.

---

## 3. Method

1. **Discover** the recurring needs across product teams (the platform's users).
2. **Define** capabilities and the golden paths that satisfy them.
3. **Design** self-service provisioning and tenancy.
4. **Instrument** platform SLOs and cost-to-serve.
5. **Evolve** the platform from real adoption data, not from feature requests
   alone.

---

## 4. Orchestration and Handoffs

| Concern | Owning skill |
|---|---|
| Technology domain and standards | [technology-architect](../../domains/technology-architect/SKILL.md) |
| Enterprise frame | [enterprise-architect](../../enterprise/enterprise-architect/SKILL.md) |
| Container platform | [program-containers](../../../infrastructure/program-containers/SKILL.md) |
| Cloud platform and landing zone | [cloud-infrastructure-architect](../../../roles/cloud-infrastructure-architect/SKILL.md) |
| CI/CD pipelines and delivery | the DevOps discipline |
| Supply-chain security of the platform | [software-supply-chain-security](../../../security/appsec/software-supply-chain-security/SKILL.md) |
| Observability of the platform | [observability-correlation](../../../mapping/observability-correlation/SKILL.md) |

---

## 5. Reference Frameworks

- **Team topologies** — the platform-team interaction model (resolve the
  edition before citing).
- **CNCF landscape and whitepapers** — cloud-native platform components.
- **Cloud well-architected guidance** — for platform reliability and cost.
- **TOGAF / ArchiMate** — for placement in the enterprise description.

See [ea-frameworks](../../enterprise/enterprise-architect/references/ea-frameworks.md).

---

## 6. Common Mistakes

| Mistake | Correction |
|---|---|
| Building features nobody adopts | Start from recurring team needs |
| A golden path slower than the unsafe path | Make the safe path the easy path |
| Platform without SLOs | Define and measure platform reliability |
| No cost-to-serve view | Track platform unit economics |
| Treating the platform as infrastructure only | It is a product with users |
