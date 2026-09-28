---
name: "api-design"
description: "Provides expert patterns for API design and lifecycle management based on API Design Patterns (Geewax) and Continuous API Management. Covers resource-oriented design and standard methods, custom methods, long-running operations and rerunnable jobs, partial updates and field masks, associations and singletons, pagination/filtering/import-export, versioning and soft deletion, request deduplication and idempotency, the five API styles, the ten API pillars, and API governance."
---

# AI Skill: API Design and API Lifecycle Management

This skill guides the AI to design APIs that are predictable, evolvable and safe to retry, and to manage APIs as products across their lifecycle. It builds on *API Design Patterns* (Geewax) and *Continuous API Management* (Medjaoui, Wilde, Mitra & Amundsen).

Resolve current versions of the relevant specifications (OpenAPI, AsyncAPI, GraphQL, gRPC) from their publishers before citing them.

---

## 🧭 When to Activate

- Designing a new HTTP/REST, GraphQL, gRPC or event API.
- Choosing between standard methods and a custom/RPC-style method.
- Specifying pagination, filtering, long-running operations, or errors.
- Planning versioning, deprecation, or the API lifecycle.
- Auditing an API landscape for consistency and governance.

---

## 🧱 Resource-Oriented Design (Geewax)

Model resources and apply **standard methods** — knowing five methods plus a resource name is learning five RPCs at once. Standard set: **List / Get / Create / Update / Delete**, plus semi-standard **Replace** (`PUT`, full replacement — risks clobbering unknown fields) versus partial **Update** (field masks).

- **Principles:** naming; resource scope and hierarchy; data types and defaults.
- **Standard methods must be predictable, side-effect-free and (mostly) idempotent**; `get`/`list` are strictly read-only. Never reuse an identifier, even after deletion.
- **Partial updates/retrievals** via `FieldMask`.
- **Custom methods** for side effects or non-standard operations (on resources or collections); keep genuinely stateless operations as custom methods.
- **Long-running operations:** `Operation<ResultT, MetadataT>` with `done`, `result`, `metadata`, plus wait/cancel/pause/resume and error handling.
- **Rerunnable jobs:** a job resource + a `run` custom method + a job-execution resource.

**Resource relationships:**
- **Singleton sub-resources** isolate part of a resource with an exactly-one invariant (atomic reset).
- **Cross references** vs embedded values (reference field names; data integrity).
- **Association resources** (`Membership` with `userId`/`groupId`/`role`/`expireTime`) carry relationship metadata; **add/remove custom methods** cover relationships without metadata.
- **Polymorphism** via dynamically typed attributes.

**Collective operations:** copy/move; **batch** (atomic, e.g. batch get); criteria-based deletion; anonymous writes; **pagination** (`maxPageSize` + `pageToken` → `nextPageToken`, idempotent, safe to re-request); **filtering** (prefer string filter expressions over strictly typed structures for evolvability); import/export (direct storage interaction, request IDs for dedup).

---

## 🛡️ Safety and Evolvability

- **Versioning and compatibility:** semantic versioning; additive, backward-compatible field additions; a versioning policy; extending soft delete across versions.
- **Soft deletion** ("API recycle bin"): mark `deleted:true`, retention policy, permanent after N days, restore path.
- **Request deduplication** for non-idempotent methods: a client **request ID** cached with the response, plus a **request fingerprint** of the body to detect **request ID collisions**.
- **Request validation** ("safe mode"): validate by default, execute only on request.
- **Resource revisions:** revision identifiers with create/retrieve/list/restore/delete and snapshot-timestamp reads.
- **Request retrial:** safe retry algorithms with **exponential back-off and jitter**; **request authentication** by signing (fingerprint included in the signature).

---

## 🧭 The Five API Styles and the Ten Pillars

**Styles** (interaction patterns, not technologies): **Tunnel** (RPC/SOAP; exposes implementation, hard to scale), **Resource** (REST-like), **Hypermedia** (resource + machine-readable links for main workflows), **Query** (GraphQL-style schema abstraction), **Event-Based** (pub-sub). **Constraints, style and technology must align** — mismatch yields poor design or poor implementation. No style is universally best.

**The ten pillars:** Strategy, Design, Documentation, Development, Testing, Deployment, Security, Monitoring, Discovery, Change management.

**Maturity and lifecycle:** a product moves **Create → Publish → Realize → Maintain → Retire**; right-size investment per stage. Manage the **landscape** (all APIs across domains), not just individual APIs.

**Governance:** decision-making authority, not power. Patterns: **Design Authority**, **Embedded Centralized Experts**, **Influenced Self-Governance**. Centralize where safety matters, distribute where speed matters. Publish guidance as code (version-controlled Markdown) over read-only PDFs; aggregate public guides (Google, Microsoft, PayPal). As a landscape grows, governance shifts to a portfolio of standards and **landing zones**/golden paths.

---

## ⚠️ Pitfalls

- Bespoke RPC verbs where a standard method + resource would be learnable.
- `PUT` replacing fields the client never knew about (use field masks / partial update).
- Non-idempotent methods without deduplication — retries create duplicates.
- Strictly typed filter structures that block evolvability.
- Versioning without a deprecation policy; breaking changes smuggled into "minor" releases.
- Style/technology mismatch (e.g. a hypermedia promise on a tunnel implementation).

---

## 🔗 Integration with Other Skills

- For HTTP/REST specifics, see [framework-rest-api](../../../frameworks/framework-rest-api/SKILL.md); for GraphQL/gRPC, see [framework-graphql](../../../frameworks/framework-graphql/SKILL.md) and [framework-grpc](../../../frameworks/framework-grpc/SKILL.md).
- For distributed guarantees behind the API, see [distributed-systems](../distributed-systems/SKILL.md).
- For API security, see [api-protocol-security](../../../security/appsec/api-protocol-security/SKILL.md).
- For lifecycle documentation, see [architecture-documentation](../architecture-documentation/SKILL.md).
