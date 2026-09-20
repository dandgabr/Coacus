---
name: program-ai-memory-handoff
description: Specialist in the session-continuity (Handoff) lifecycle with ai-memory, covering consumption of pending handoffs at SessionStart, creation of transition batons for the next session, and disposal of expired handoffs.
metadata:
  type: management
  phase: governance
  tools:
    - ai-memory
---

<!-- ai-memory-managed: routing-skill -->

# ai-memory Session Continuity & Handoffs

This skill guides the baton pass (*handoff*) between sessions and AI agents using [ai-memory](https://github.com/akitaonrails/ai-memory). Handoffs are transient and single-use, intended to preserve the mental state and next steps for the following session, and must not be confused with durable wiki documentation.

---

## 🧰 Tools in This Cluster

- `memory_handoff_accept`: Consumes the pending handoff when the user asks "where did we leave off?" and the block injected at the start of the session is not visible.
- `memory_handoff_begin`: Creates a concise transition handoff when the session is being wrapped up or when the user explicitly asks to save context for the next run.
- `memory_handoff_cancel`: Invalidates a pending handoff created by mistake using its exact `handoff_id`.

---

## 🔄 Handoff Lifecycle

1. **Automatic Injection at Session Start**:
   - Lifecycle hooks (`session-start`) automatically fetch and consume the pending handoff, injecting it into the model's initial context with the `📥 ai-memory: pending handoff` marker.
   - If that message is already present in context, answer from it directly and do **not** call `memory_handoff_accept` again (because handoffs are single-use).
2. **Creation at Session End**:
   - Call `memory_handoff_begin` only when wrapping up the conversation or on explicit request.
   - Keep the summary ultra-concise (2 to 3 sentences) and concentrate the details in the open questions and next steps.
3. **Sharing**:
   - By default, the handoff belongs to the operator who created it. Use `shared: true` only when it is expressly requested that any operator in the project may receive the transition.
