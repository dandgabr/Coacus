---
name: "ui-style-ai-native-generative-ui"
description: "Provides the AI-native / generative UI style (2023-present): interfaces where the model drives the UI itself — streaming answers, tool-call components, canvas workspaces and agentic step-throughs — covering the intent-based paradigm shift, Vercel AI SDK patterns, staged tool states, streaming a11y and provenance disclosure. Use when designing copilots, assistant surfaces or LLM-driven product UI."
---

# UI Style: AI-Native / Generative UI

Interfaces where the model drives not just text but the UI itself: streaming answers, tool calls that render real components, canvas workspaces, agentic step-throughs. Clock starts with ChatGPT (Nov 30, 2022); conceptual anchor: Jakob Nielsen's "AI: First New UI Paradigm in 60 Years" (June 18, 2023) — intent-based outcome specification reversing the locus of control. Synthesized from verified research; see Sources.

---

## 🧭 When to Activate

- Designing assistant surfaces, copilots, agentic tools, creation workspaces.
- Mapping tool-call state machines to UI states.
- Budgeting streaming text for CLS and screen-reader behavior.

---

## 🕰️ Definition and Timeline

- ChatGPT (Nov 30, 2022) → Nielsen's paradigm essay (Jun 18, 2023) → Vercel coins productized "Generative UI" (late 2023): tool-call results → React components → Anthropic Artifacts (Jun 2024) → OpenAI Canvas (Oct 3, 2024) → MCP open standard (Nov 25, 2024) → OpenAI Apps SDK (interactive apps inside chat).

---

## 🎨 Visual DNA

- Centered prompt field with generous whitespace (the "AI gradient" as genre marker); streaming token text with typing semantics; skeleton placeholders for tool latency; citation chips; split view — conversation left, artifact/canvas right; collapsed "thinking" accordions; render zones where components materialize from structured output.

---

## 🖱️ Interaction and Motion

- **Streaming-first:** first token fast (TTFT replaces "page load" as the budget); optimistic UI with staged tool states (`input-available` → `output-available` → `output-error` — the AI SDK's literal state machine); confirm-before-act for consequential actions (human-in-the-loop); undo/version rails in canvas surfaces; suggestion chips after completion.

---

## 🛠️ Implementation Notes

- AI SDK `useChat` + message `parts` array; typed tool parts (`tool-${toolName}`) mapped to React components; streaming via `streamText` + UI message streams (SSE/ReadableStream); structured output via Zod; MCP servers to expose data/tools; design-system-as-vocabulary — constrain generation to your component set instead of free HTML; `aria-live="polite"` regions for streaming text; visible plan steps with per-step status for agent loops.

---

## ♿ Accessibility and Performance

- Streaming text reflows constantly — reserve message row height or accept controlled shift only within the message container; virtualize long transcripts; batch streamed tokens per frame (no per-token DOM writes); don't steal focus on tool-result injection; disclose AI provenance and uncertainty in the UI itself (unverifiable output is the core usability problem); `prefers-reduced-motion` applies to "thinking" animations too.

---

## ✅ When to Use / ❌ When to Avoid

- **Use:** assistants, copilots, agentic tools, creation workspaces (writing/code/design).
- **Avoid:** high-stakes single-shot decisions without review; deterministic-UI requirements (payment forms, admin CRUD); adding a chatbot to a page that needed a form.

---

## ⚠️ Pitfalls

- Hallucination makes every generated UI a verification burden; chat-as-UI debated as a dead end for structured tasks (Nielsen himself predicts a hybrid GUI+intent future); "AI sparkle gradient" template slop; feigned confidence as a dark pattern; latency cliffs with no staged state; a11y regressions from dynamic DOM injection.

---

## 📚 Sources

- Vercel AI SDK, "Generative User Interfaces" (v7) — https://ai-sdk.dev/docs/ai-sdk-ui/generative-user-interfaces
- OpenAI, "Introducing canvas", Oct 3, 2024 — https://openai.com/index/introducing-canvas/
- Anthropic, "Introducing the Model Context Protocol", Nov 25, 2024 — https://www.anthropic.com/news/model-context-protocol
- Jakob Nielsen, "AI: First New UI Paradigm in 60 Years", NN/g, Jun 18, 2023 — https://www.nngroup.com/articles/ai-paradigm/
- Google PAIR, "People + AI Guidebook" — https://pair.withgoogle.com/guidebook
- OpenAI Apps SDK — https://developers.openai.com/apps-sdk

---

## 🔗 Integration with Other Skills

- Sibling styles: [ui-style-kinetic-typography](../ui-style-kinetic-typography/SKILL.md), [ui-style-micro-interactions](../ui-style-micro-interactions/SKILL.md), [ui-style-bento-grid](../ui-style-bento-grid/SKILL.md).
- For the underlying interaction paradigms, see [ai-application-engineering](../../industry/ai-application-engineering/SKILL.md) and [conversational-ai-chatbots](../../industry/conversational-ai-chatbots/SKILL.md).
