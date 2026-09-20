---
name: program-ai-memory-durable-pages
description: Specialist in deliberate mutations and durable page writes in the ai-memory wiki, covering permanent annotations, architectural decisions (ADR), global-scope rules, and precise removal of obsolete pages.
metadata:
  type: management
  phase: implementation
  tools:
    - ai-memory
---

<!-- ai-memory-managed: routing-skill -->

# ai-memory Durable Pages & Wiki Management

This skill guides the deliberate, structured writing of durable knowledge into the [ai-memory](https://github.com/akitaonrails/ai-memory) wiki. Deliberate writes should be used to store lessons learned, definitive rules, and ADRs, distinguishing them from the automatic log and tool captures made by hooks.

---

## 🧰 Tools in This Cluster

- `memory_write_page`: Creates or updates a durable page in the project wiki or in the global scope.
- `memory_delete_page`: Removes obsolete or revoked pages using their exact relative path.

---

## 📝 Writing and Title Conventions

1. **H1 Title Convention**:
   - Start the document body (`body`) with the title as `# Page Title` on the first line. `ai-memory` infers the title automatically from that heading, avoiding character-escaping problems in the tool call.
2. **Recommended Canonical Paths**:
   - `notes/<topic>.md`: General engineering notes and business context.
   - `decisions/<topic>.md`: Architectural decisions with ADR structure.
   - `concepts/<topic>.md`: Domain models, entities, and conceptual architecture.
   - `_rules/<topic>.md`: Project guidelines and policies.
3. **Temporary Pages with TTL (`expires_at`)**:
   - If information has a limited lifetime (e.g., a temporary migration, a test credential, or a one-off sprint), set `expires_at` (RFC3339 or `YYYY-MM-DD` format). The page is hidden after that date and cleaned up in the next *forget sweep*.

---

## 🏛️ Architectural Decision Records (ADR)

To record technical decisions with guaranteed durability, use `path: "decisions/<slug>.md"`, set `pinned: true`, and follow the canonical structure:

```markdown
# [Título da Decisão]

**Status:** accepted <!-- proposed | accepted | superseded by [[decisions/outro]] -->

## Contexto
Qual problema forçou a tomada de decisão e quais restrições eram relevantes.

## Decisão
O que foi decidido, declarado de forma afirmativa e objetiva.

## Consequências
Vantagens obtidas, desvantagens assumidas e alternativas rejeitadas (com justificativa para evitar retrabalho futuro).
```

---

## 🌐 Global Preferences and Rules (`scope: "global"`)

When a technical standard is cross-cutting and applies to **every project** on the machine (e.g., commit conventions, tool preferences, or machine security rules):
- Call `memory_write_page` with the `scope: "global"` parameter.
- The content is stored in the reserved `_global` scope and returned automatically in queries from any subproject as `global_scope_hits`.
