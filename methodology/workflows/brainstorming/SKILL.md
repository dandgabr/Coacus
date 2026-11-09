---
name: brainstorming
description: "You MUST use this before any creative work - creating features, building components, adding functionality, or modifying behavior. Explores user intent, requirements and design before implementation."
---

<!--
Coacus adaptation of a Superpowers workflow (MIT).
Upstream: https://github.com/obra/superpowers @ 5bf4e78011075bcfc0dc295f0724994cd123ee71
Process artifacts are written under docs/temp/.
Conventions: ../using-coacus/references/coacus-process-conventions.md
-->

# Brainstorming Ideas Into Designs

Scale design discussion to uncertainty and risk. Preserve the user's existing authorization: a clear request to implement a bounded change is permission to proceed, not a request to approve a second design.

## Choose the depth

- **Clear, bounded work:** inspect the relevant context, choose the smallest sound approach, and implement through the normal development and verification workflow. State consequential assumptions in the result; do not demand a separate approval.
- **Material ambiguity or consequential alternatives:** ask a focused question when the answer could change the outcome. Present options and trade-offs when a decision is needed. Do not ask again for decisions already made.
- **Architectural or broad work:** explore purpose, constraints, success criteria, boundaries, dependencies, error handling and verification. Compare viable approaches and record decisions in a spec or plan when appropriate. Request review when the user asks for it, when an irreversible or explicitly approval-gated action is involved, or when a material unresolved choice requires the user's decision. A request for a plan alone does not authorize implementation; explicit implementation authorization remains valid through planning.
- **Investigation or spike:** define the question, scope and safe probe; do not turn an investigation request into implementation. Obtain permission for destructive, externally visible or otherwise gated actions.

Reassess if new evidence makes the original scope materially broader. Explain the changed decision and ask only if it cannot be resolved within the authorized scope. Follow repository rules and higher-priority user instructions on artifacts, reviews and commits; do not commit merely because a spec was written.

## Design discipline

Inspect existing project context and reuse established components before proposing new structure. Prefer the simplest viable approach; avoid unrelated refactoring. Consider accessibility, security, failure handling and tests where relevant. Keep assumptions and unresolved risks visible. For complex designs, review the written artifact for placeholders, inconsistent requirements and ambiguous boundaries before using it as an implementation input.

## Visual Companion

A browser-based companion for showing mockups, diagrams, and visual options during brainstorming. Available as a tool — not a mode. Accepting the companion means it's available for questions that benefit from visual treatment; it does NOT mean every question goes through the browser.

**Offering the companion (just-in-time):** Do NOT offer it upfront. Wait until a question would genuinely be clearer shown than told — a real mockup / layout / diagram question, not merely a UI *topic*. The first time that happens, offer it then, as its own message:
> "This next part might be easier if I show you — I can put together mockups, diagrams, and comparisons in a browser tab as we go. It's still new and can be token-intensive. Want me to? I'll open it for you."

**This offer MUST be its own message.** Only the offer — no clarifying question, summary, or other content. Wait for the user's response. If they accept, start the server with `--open` so their browser opens to the first screen automatically. If they decline, continue text-only and don't offer again unless they raise it.

**Per-question decision:** Even after the user accepts, decide FOR EACH QUESTION whether to use the browser or the terminal. The test: **would the user understand this better by seeing it than reading it?**

- **Use the browser** for content that IS visual — mockups, wireframes, layout comparisons, architecture diagrams, side-by-side visual designs
- **Use the terminal** for content that is text — requirements questions, conceptual choices, tradeoff lists, A/B/C/D text options, scope decisions

A question about a UI topic is not automatically a visual question. "What does personality mean in this context?" is a conceptual question — use the terminal. "Which wizard layout works better?" is a visual question — use the browser.

If they agree to the companion, read the detailed guide before proceeding:
`visual-companion.md`
