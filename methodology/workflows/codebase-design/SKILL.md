---
name: codebase-design
description: Use when designing or restructuring module boundaries, to create deep modules with simple interfaces and hide internal complexity.
---

# Codebase design

Design deep modules that maximize functionality while presenting minimal,
ergonomic interfaces. Grounded in John Ousterhout's *A Philosophy of Software Design*.

## Deep vs. shallow modules

- **Deep module:** An interface that is simple relative to the power of the
  underlying implementation. It hides substantial internal complexity, data
  structures, and edge-case handling behind a few clean entry points.
- **Shallow module:** An interface that exposes nearly as much complexity as its
  implementation. It adds indirection and cognitive load without reducing cognitive
  burden.

## The deletion test

Before confirming a module boundary or class extraction, apply the deletion test:
1. Mentally delete the proposed module boundary and inline the logic directly into
   the caller.
2. If complexity concentrates and the caller becomes cleaner and more cohesive, the
   boundary was shallow and should be deleted.
3. If the caller becomes overwhelmed with details that obscure its primary purpose,
   the boundary is genuine and deep.

## Design-it-twice protocol

Do not settle on the first interface design that comes to mind:
1. State the core contract in plain domain terms.
2. Draft at least two radically different interface sketches:
   - **Variant A (Minimal surface):** Absolute minimum functions and parameters,
     handling edge cases internally.
   - **Variant B (Fluent / Ergonomic):** Optimized for caller readability and common
     composition patterns.
   - **Variant C (Data-driven / Declarative):** Input configurations or descriptors
     driving execution.
3. When using subagents, dispatch two parallel reviewers under contrasting
   constraints to evaluate caller ergonomic trade-offs before authoring code.

## Git hotspot targeting

Focus architectural restructuring where it yields the highest return:
- Query churn history with git revision logs to identify files with high commit
  frequency and frequent defect fixes.
- Refactor high-churn shallow modules. Leave stable, low-churn code untouched
  unless an active feature strictly requires modification.

## Rules of thumb

- **Information hiding:** Variables, internal states, and temporary data must not
  leak through method signatures or public configuration.
- **Pass-through methods:** A method that merely forwards its parameters to another
  method with no transformation is a warning sign of shallow design.
- **Pull complexity down:** Move error handling, validation, and normalization inside
  the module boundary rather than forcing every caller to repeat them.
