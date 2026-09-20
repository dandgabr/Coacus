---
name: arch-bce-pattern
description: "Acts as a specialist in the Boundary-Control-Entity architectural pattern (BCE / ECB, Ivar Jacobson). Defines a clean separation between external interfaces (Boundary), business logic (Control), and domain entities (Entity), with strategies for incremental legacy-code migration."
---

# Boundary-Control-Entity (BCE) Architecture Pattern

This skill defines the engineering guidelines and modeling strategies for the **Boundary-Control-Entity (BCE / ECB)** pattern, formulated by Ivar Jacobson for use-case-driven development and decoupled business components.

---

## 🏛️ 1. The Three Canonical BCE Layers

```
[ Cliente Externo / UI ]
          │
          ▼
┌──────────────────┐
│     BOUNDARY     │  <-- Entrada, APIs REST/gRPC, Web, Mensageria, Tradução DTO
└─────────┬────────┘
          │
          ▼
┌──────────────────┐
│     CONTROL      │  <-- Coordenação do Caso de Uso, Regras de Negócio, Transações
└─────────┬────────┘
          │
          ▼
┌──────────────────┐
│      ENTITY      │  <-- Modelo de Domínio, Invariantes, Estado e Persistência
└──────────────────┘
```

### A. Boundary
- Isolates the component from the outside world (network protocols, JSON format, HTTP controllers, messaging queues).
- Responsibility: structural input validation, request routing, and conversion of DTOs into domain models.
- **Rule**: Boundaries talk only to Controls or to Entities through DTOs. They never call Entities directly for mutation operations.

### B. Control (Use Case)
- Orchestrates business use cases and the sequence of operations.
- Responsibility: flow rules, transaction management, business policies, and emission of domain events.
- **Rule**: Controls know nothing about transport details (no HTTP annotations or servlets); they depend only on interfaces and Entities.

### C. Entity (Business Entity)
- Encapsulates the state, identity, and fundamental business invariants.
- Responsibility: internal computation of atomic rules, persistence, and data consistency.

---

## 🔄 2. Incremental Migration Procedure (Migrate-to-BCE)
To refactor a legacy project onto the BCE architecture without production breaks:
1. **Identify Business Components**: Group classes by domain capability, not by technical layer alone.
2. **Extract Boundaries**: Isolate `@RestController` or `@Path` classes by moving them into the `boundary` package.
3. **Decouple Service Logic into Controls**: Move orchestration flow out of monolithic `@Service` classes into atomic control classes focused on one use case each.
4. **Isolate Entities**: Keep persistence entities in the `entity` package and protect their invariants.
