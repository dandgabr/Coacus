---
name: "clean-architecture"
description: "Provides expert patterns for clean/hexagonal architecture and decoupling from frameworks based on Clean Architectures in Python (Giordani), covering the dependency rule (talk inwards with simple structures, outwards through interfaces), entities and use cases, ports and adapters, dependency injection, repositories and unit of work, request/response objects, and the functional core / imperative shell split, with TDD-driven construction."
---

# AI Skill: Clean / Hexagonal Architecture

This skill guides the AI to build systems whose business logic is testable and independent of frameworks, databases and delivery mechanisms. It builds on *Clean Architectures in Python* (Giordani), the concrete Python realization of ports-and-adapters.

The defining rule: **talk inwards with simple structures, talk outwards through interfaces.**

---

## 🧭 When to Activate

- Decoupling business logic from Django/Flask, an ORM, or a message broker.
- Designing use cases / application services and their boundaries.
- Introducing dependency injection, repositories or unit of work.
- Making core logic testable without a database or HTTP.
- Refactoring a framework-coupled application toward a hexagonal shape.

---

## 🧅 The Layered Dependency Rule

Inner layers are more abstract and **oblivious** to outer layers; communication within a layer is unrestricted. Data crosses boundaries as **simple structures** (dataclasses/dicts), never as framework objects.

- **Entities / domain models** — lightweight business objects; no storage, JSON, or presentation coupling (not ORM models).
- **Use cases** — small processes operating on real data; may call each other; they own the application transaction.
- **External systems / adapters** — frameworks, databases, HTTP, CLI; they **implement interfaces defined inward**.

**Data flow is inviolable.** If performance forces a use case to reach directly into a specific DB API, document it loudly in code and docs — replacing that adapter later requires knowing the direct access exists. Consistent, pervasive breakage means the layers should merge.

---

## 🔌 Ports, Adapters and DI

Use cases receive their dependencies through construction (**dependency injection**). A **repository** interface is a *reduced set of endpoints tailored to business needs* — at a higher abstraction than an ORM.

```python
class RoomListUseCase:
    def __init__(self, repo):        # injected
        self.repo = repo
    def execute(self, request):
        ...
```

Swap `MemRepo` → `PostgresRepo` → `MongoRepo` behind the same interface without touching the use case. Delivery mechanisms (CLI, Flask) are thin adapters over the use cases; use an **app factory** (`create_app`) with per-environment config (`TestConfig`/`DevConfig`/`ProdConfig`).

---

## 📨 Request / Response Objects and Errors

Use cases never throw framework exceptions outward. Accept validated **request objects** and return **response objects**:

- `ValidRequestObject` / `InvalidRequestObject` validate parameters before the use case runs.
- `ResponseSuccess` / `ResponseFailure` with typed errors (`PARAMETERS_ERROR`, `RESOURCE_ERROR`, `SYSTEM_ERROR`) and a `build_from_invalid_request_object` helper.

This keeps the boundary testable and the HTTP layer a pure translator.

---

## 🧪 TDD and Testing Discipline

- Tests are **fast, idempotent, isolated**; avoid external systems (use fakes/mocks).
- **Focus on messages**, not internals. The **testing grid** distinguishes *incoming queries* (assert the returned value) from *outgoing commands* (assert the message was sent).
- `unittest.mock` for patching external collaborators; patch immutable objects carefully; mock at the adapter boundary, not inside the domain.
- Build the core **test-first**: define behavior, then implement.

---

## 🧬 Functional Core / Imperative Shell

Realize the split concretely: a **pure domain + use-case core** surrounded by **repositories, serializers and HTTP/CLI adapters**. Purity makes the core deterministic and trivial to test; the shell holds all I/O and framework contact.

---

## ⚠️ Pitfalls

- Leaking ORM models or framework request objects into use cases and entities.
- Making the repository an ORM wrapper (leaky abstraction) instead of a business-shaped interface.
- Throwing exceptions across layer boundaries rather than returning typed responses.
- Business logic in the delivery layer (controllers doing orchestration).
- Silent, undocumented violations of the dependency rule.

---

## 🔗 Integration with Other Skills

- For boundaries, aggregates and context mapping, see [architecture-ddd](../architecture-ddd/SKILL.md).
- For the language-level idioms, see [lang-python](../../../languages/lang-python/SKILL.md).
- For dependency inversion and design patterns, see the [dp-* pattern skills](../../patterns/dp-structural-patterns/SKILL.md).
- For persistence performance, see [jpa-hibernate-performance](../../../data/jpa-hibernate-performance/SKILL.md) and [db-postgresql](../../../data/db-postgresql/SKILL.md).
