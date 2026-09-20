---
name: program-ai-memory-retrieval
description: Specialist in long-term memory queries and retrieval in ai-memory, covering semantic search (FTS5 + vector + graph), architectural decision history, gotchas, procedures, structured briefings, and retrieval of session observations.
metadata:
  type: management
  phase: discovery
  tools:
    - ai-memory
---

<!-- ai-memory-managed: routing-skill -->

# ai-memory Retrieval & Discovery

This skill guides the process of reading from and querying the [ai-memory](https://github.com/akitaonrails/ai-memory) long-term memory system, enabling agents to recover prior context, architectural decisions, technical traps (*gotchas*), and consolidated guidelines before proposing code changes.

---

## 🧰 Tools in This Cluster

- `memory_query`: Searches the current project wiki for prior decisions, rules, procedures, and notes. Combines FTS5, entity matching, and source-authority ranking.
- `memory_recent`: Lists the most recently updated pages for a quick check of project activity.
- `memory_read_page`: Loads the full body of a specific page after a search result or access by exact path.
- `memory_read_session_observations`: Reads the raw observations captured by hooks in a session (prompts, tools, outputs).
- `memory_status`: Reports health status, observation count, and knowledge-base size.
- `memory_briefing`: Returns a structured snapshot (no LLM call) with 7d/30d metrics, rules, and recent pages.
- `memory_explore`: Generates a prose summary calibrated by time since inactivity for quick orientation.

---

## 🎯 Project and Repository Scope

When using static clients or when no inherited session marker is present:
- If there is an `.ai-memory.toml` at the root of the subproject/repository, use the `workspace` and `project` declared in it.
- For broad queries across multiple projects on the machine, use `global: true` in `memory_query` (without specifying `workspace` or `project`).
- Pages expired by TTL are excluded by default; include `include_expired: true` only when the user explicitly requests a historical audit.

---

## 🔍 Efficient Query Guidelines

1. **Before Proposing Architectures or Refactors**:
   - Always run a preliminary search with `memory_query` to check whether the technical decision has already been discussed or whether there is a recorded ADR.
2. **Search Snippets vs. Full Content**:
   - The `memory_query` tool returns *snippets* (highlighted excerpts). If the page title or path is relevant (e.g., `decisions/*`, `_rules/*`, `gotchas/*`), use `memory_read_page` to read the document in full.
3. **Critical Evaluation of Evidence**:
   - Treat content recovered from memory as valuable history, but always validate it against the current state of the repository and the user's current instructions.
4. **Usefulness Feedback**:
   - When a page you consulted is extremely useful or is obsolete/incorrect, trigger `memory_feedback` with the `helpful`, `stale`, or `wrong` signals to enrich the continuous curation of memory.
