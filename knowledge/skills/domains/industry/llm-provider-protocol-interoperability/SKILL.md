---
name: llm-provider-protocol-interoperability
description: >-
  Provides protocol compatibility patterns across LLM providers for extended
  thinking, tool calling, and prompt caching. Use when switching between
  Anthropic, Google Gemini, OpenAI, and local Ollama or vLLM models, normalizing
  tool-call IDs, preserving reasoning signatures across turns, or tuning small
  local models for structured tool use.
tags:
  - ai
  - llm
  - interoperability
  - tool-calling
  - extended-thinking
---

# LLM Provider Protocol Interoperability (Thinking, Tools & Caching)

This skill specifies engineering patterns for seamless interoperability across foundation model providers (**Anthropic, Google Gemini, OpenAI, DeepSeek, and local inference engines such as Ollama and vLLM**), preventing fatal HTTP 400 errors during multi-turn conversations and model migrations.

---

## 🧠 1. Reasoning Signatures & Extended Thinking Compatibility

Providers treat reasoning and extended thinking with incompatible wire schemas:

| Provider | Signature Requirement | Wire Location | Temperature Rule |
| :--- | :--- | :--- | :--- |
| **Anthropic** | Mandatory cryptographic binary signature | `choice.Reasoning.Signature` (message level) | `Temperature = 1.0` (budget thinking); No sampling params for adaptive thinking |
| **Google Gemini** | Mandatory thought signature for tools | Embedded in `ToolCall[0].Reasoning.Signature` | Flexible (works at any temperature) |
| **OpenAI / DeepSeek**| No signature required | Tag `<think>` in content or `reasoning_tokens` metric | Auto-enforces deterministic reasoning |

### Critical Rules
1. **Preserve Signatures on Continuation**: When continuing multi-turn dialogues with Anthropic or Gemini, never strip reasoning blocks from previous assistant turns. Missing signatures cause immediate `400 Bad Request` rejections.
2. **Clear Reasoning on Provider Switch**: When migrating a conversation history from Anthropic to Gemini or OpenAI, strip all provider-specific signatures and reasoning objects via AST before submitting to the new provider.
3. **Sequential vs. Parallel Gemini Signatures**:
   - In parallel tool calls, Gemini places the thought signature **only** on the first `ToolCall`.
   - In sequential tool calls, each sequential step receives an independent signature.

---

## 🔧 2. Cross-Provider Tool-Call ID Normalization

Providers enforce divergent regex validation on tool-call identifiers:

- **OpenAI / Gemini**: Hexadecimal strings formatted as `call_[a-zA-Z0-9]{24}`.
- **Anthropic**: Base62 identifiers matching `^toolu_[a-zA-Z0-9_-]+$`.

### Normalization Workflow
When restoring conversation chains across providers:
1. Parse the message chain into a structured AST (`ChainAST`).
2. Validate each tool-call ID against the target provider's regex template.
3. Map mismatched IDs to target-compliant identifiers across both the tool invocation part and its corresponding tool response message.

---

## 🗄️ 3. Prompt Caching Hierarchy & Invalidation Rules

Prompt caching operates on a cumulative prefix principle:

```text
Tools Definitions  --->  System Prompt  --->  Message 1  --->  Message 2
   (Prefix 1)               (Prefix 2)          (Prefix 3)       (Prefix 4)
```

- **Prefix Invalidation**: Modifying `Tools` invalidates everything downstream (system and messages). Modifying the `System Prompt` invalidates all message caches.
- **Minimum Token Thresholds**:
  - Anthropic: 1,024 tokens (Sonnet) / 4,096 tokens (Haiku).
  - Gemini: 1,024 tokens (Gemini 2.5 Flash ephemeral) / 32,768 tokens (explicit `CachingHelper`).
  - OpenAI: 1,024 tokens (automatic implicit cache).
- **Gemini Implicit Cache Signature Dependency**: In Gemini multi-turn interactions, cache hits for conversation prefixes require preserving the thinking signature byte-for-byte.

---

## 💻 4. Local Model Optimization (Ollama & vLLM < 32B)

When executing smaller open-weight models (e.g., Llama 3.1 8B, Qwen 2.5 7B/14B/32B, DeepSeek-R1 Distill):

1. **Role-Specific Temperature Tuning**:
   - `coder`: `0.1` (deterministic logic, syntax accuracy).
   - `searcher / retriever`: `0.2` (precise query formulation).
   - `pentester / security`: `0.3` (measured exploration within bounds).
2. **Grammar-Constrained Decoding**: Enforce JSON schemas using tool-call grammars to eliminate malformed arguments in models with parameter counts under 32B.
3. **Preflight Capability Matrix**: Verify function-calling reliability and context window limits before promoting local models to production agent tiers.
