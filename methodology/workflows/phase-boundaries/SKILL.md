---
name: phase-boundaries
description: Use when deciding whether to continue a session, clear it, hand it off, dispatch a subagent or compact it.
---

# Phase boundaries

Decide at a **boundary**, never mid-phase. Work the options in order and rule each
out before moving on.

1. **Continue** — rule it out first. It is the only move that keeps the
   conversation a primary source.
2. **Clear** — when the context is exhausted and the current work is genuinely
   done.
3. **Handoff** — narrow cases: a new harness, a new directory, a colleague, or a
   side task forked mid-phase. What a handoff buys is **portability**; use the
   [handoff](../handoff/SKILL.md) skill.
4. **Subagent** — when the work is fire-and-forget (can run unattended).
5. **Compact** — the default, not the first reach. Its failure mode is a fresh
   session that is confidently wrong about a decision the summary flattened.

## Tool-call-aware compaction (ChainAST rule)

When executing compaction across turns with tool calls and extended reasoning:

- **Preserve Header and Last Body Pair**: The system header and the most recent
  `BodyPair` (the latest AI reasoning + tool call + tool response) MUST NEVER be
  summarized into prose. Summarizing the active body pair destroys provider-specific
  reasoning signatures (`thought_signature` for Gemini, cryptographic signatures for
  Anthropic) and orphan tool call IDs, causing fatal HTTP 400 Bad Request errors.
- **`<summarized_content_handling>` Anti-Mimicry**: Agents reading compacted history
  must treat prior turns purely as declarative facts, never mimicking summarized
  response formats, hallucinating that skipped checks passed, or assuming unverified
  deliverables are complete.
- **Reflector Guard & Argument Fixer**: If an agent emits a free-form completion where
  a required tool call was expected, the harness must bounce the turn with a reflection
  prompt rather than losing the thread; malformed tool arguments should pass through
  a schema-repair pass before execution.

## The trade

Every move except Continue turns a **primary source** into a **secondary source**:
information is traded for noise reduction and room to move. Choose the move whose
secondary source loses the least for the task ahead, and make the decision where
the context naturally breaks.
