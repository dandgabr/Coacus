---
name: program-ai-memory-routing-install
description: Specialist in the installation, update, inspection, and repair of ai-memory managed routing guidelines and skills across projects and AI agent environments.
metadata:
  type: management
  phase: operations
  tools:
    - ai-memory
---

<!-- ai-memory-managed: routing-skill -->

# ai-memory Routing & Skills Installation

This skill guides the installation and maintenance of the routing rules and skill packages of [ai-memory](https://github.com/akitaonrails/ai-memory) across local environments and projects.

---

## 🧰 Tools in This Cluster

- `memory_install_self_routing`: Returns the canonical instruction block, integrity markers, and managed skill payloads for clients that do not support direct writing by the MCP server.

---

## 📦 Managed Integrity Markers

To allow idempotent updates without corrupting developer-customized rules, the ai-memory ecosystem uses strict delimiters:

1. **Instruction Block (`AGENTS.md` / `GEMINI.md`)**:
   - Start: `<!-- ai-memory:start -->`
   - End: `<!-- ai-memory:end -->`
   - Only the content between these two delimiters (on isolated lines) is replaced during updates.
2. **Managed Skills (`SKILL.md`)**:
   - Ownership marker: `<!-- ai-memory-managed: routing-skill -->`
   - Only files that contain this explicit marker are safely overwritten.
