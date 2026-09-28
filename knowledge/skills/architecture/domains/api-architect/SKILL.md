---
name: api-architect
description: >-
  Acts as the API Architect owning API strategy, productization and governance:
  design-first style guides, versioning policy, security, the API catalog and
  lifecycle, and consumer experience. Use when setting API standards, governing
  the API lifecycle, defining API security or assessing API monetization.
tags:
  - architecture
  - api-architecture
---

# Skill: API Architect

The API Architect owns the **API as a product**: strategy, design standards,
lifecycle and governance. It is a specialization that sits between integration
architecture (how systems talk) and solution architecture (what one delivery
needs).

---

## 1. When This Skill Applies

- Defining API style guides and design-first standards.
- Governing the API lifecycle and the API catalog/marketplace.
- Setting API security (auth, rate limiting) and observability standards.
- Assessing monetization and consumer experience.
- Deciding versioning and deprecation policy.

Does NOT apply to: the integration patterns between systems (use
[integration-architect](../integration-architect/SKILL.md)), or the internal
design of one service (use [software-architect](../../../roles/software-architect/SKILL.md)).

---

## 2. The API Governance Surface

| Concern | Decision |
|---|---|
| Style | REST, gRPC, GraphQL, events — one standard per context |
| Contract | Design-first; the contract is the source of truth |
| Versioning | Explicit policy; additive changes preferred |
| Security | Auth model, scopes, rate limits, quotas |
| Lifecycle | Discover, design, publish, deprecate, retire |
| Observability | Metrics, tracing, usage analytics |

---

## 3. Method

1. **Set** the API style guide and the design-first workflow.
2. **Govern** contracts through review before implementation.
3. **Secure** every API with an explicit auth and quota model.
4. **Catalog** and publish APIs for discoverability.
5. **Manage** versioning, deprecation and retirement.

---

## 4. Orchestration and Handoffs

| Concern | Owning skill |
|---|---|
| Enterprise frame and standards | [enterprise-architect](../../enterprise/enterprise-architect/SKILL.md) |
| Integration patterns and messaging | [integration-architect](../integration-architect/SKILL.md) |
| REST contract semantics | [framework-rest-api](../../../frameworks/framework-rest-api/SKILL.md) |
| gRPC/protobuf contracts | [framework-grpc](../../../frameworks/framework-grpc/SKILL.md) |
| GraphQL schemas | [framework-graphql](../../../frameworks/framework-graphql/SKILL.md) |
| API security testing | [pentester-owasp-api-security-2023](../../../security/appsec/pentester-owasp-api-security-2023/SKILL.md) |
| API security controls | [api-protocol-security](../../../security/appsec/api-protocol-security/SKILL.md) |

---

## 5. Reference Frameworks

- **OpenAPI Specification** — REST contracts (resolve the version before
  citing).
- **gRPC / Protocol Buffers** and **GraphQL** — alternative contract styles.
- **AsyncAPI** — event-driven API contracts.
- **OWASP API Security Top 10** — the API risk baseline.

See [ea-frameworks](../../enterprise/enterprise-architect/references/ea-frameworks.md)
for the EA method.

---

## 6. Common Mistakes

| Mistake | Correction |
|---|---|
| Code-first with the contract as an afterthought | Design-first; the contract leads |
| Breaking changes without a version | Govern versioning and deprecation |
| No auth or quota model | Secure every API explicitly |
| Inconsistent styles across teams | One governed style guide per context |
| No catalog or discoverability | Publish and catalog APIs |
