---
name: "ui-ux-principles"
description: "Provides expert patterns for user-interface and interaction design based on Designing the User Interface (Shneiderman & Plaisant), Don't Make Me Think (Krug), Laws of UX (Yablonski), and Designing AI Interfaces (Macfadyen). Covers the eight golden rules, interaction styles, information visualization, usability testing, scanning and navigation, applied UX laws (Fitts, Hick, Jakob, Miller, Peak-End, Doherty), the Hook Model, and human-AI interaction with autonomy, trust and shared control."
---

# AI Skill: UI/UX and Human-Computer Interaction Principles

This skill guides the AI to design interfaces users can operate without instruction: self-evident, forgiving, consistent, and — for AI features — honest about their limits. It builds on *Designing the User Interface* (Shneiderman & Plaisant), *Don't Make Me Think* (Krug), *Laws of UX* (Yablonski), *Hooked* (Eyal), and *Designing AI Interfaces* (Macfadyen).

---

## 🧭 When to Activate

- Designing any screen, flow, form or navigation.
- Reviewing usability, clarity, or accessibility.
- Applying behavioral psychology (habit formation, motivation).
- Designing human-AI interaction (chat, agents, generative features).
- Planning usability testing.

---

## 📜 Shneiderman's Eight Golden Rules

1. **Strive for consistency** — sequences, terminology, layout, color; make the few exceptions (destructive confirmations) comprehensible.
2. **Cater to universal usability** — novices, experts, age, disability, technology diversity; add plasticity, explanations for novices, shortcuts for experts.
3. **Offer informative feedback** — modest for frequent/minor actions, substantial for infrequent/major.
4. **Design dialogs to yield closure** — beginning/middle/end; completion feedback (e.g. checkout confirmation) lets users drop contingency plans.
5. **Prevent errors** — gray out invalid options, constrain input; on error, give specific constructive recovery and preserve state.
6. **Permit easy reversal** — reversibility relieves anxiety and encourages exploration.
7. **Support internal locus of control** — users initiate; surprising actions build anxiety.
8. **Reduce short-term memory load** — keep displays simple; recognition over recall; working memory ≈ 7±2 chunks.

**Three usage classes** (novice, knowledgeable intermittent, expert frequent) reconciled by **multi-layer learning** and user-steerable feedback.

**Interaction styles** with trade-offs: **direct manipulation** (easy to learn, errors avoided; needs graphics), **menu selection** (shortens learning; may slow experts), **form fillin** (simplifies data entry), **command language** (flexible, macro-capable; memorisation), **natural language** (relieves syntax; unpredictable). The **Object-Action Interface** model mirrors real-world objects (nouns) and actions (verbs).

**Information visualization taxonomy:** data types (1D–3D/multidimensional, temporal, tree, network) × seven tasks: **Overview, Zoom, Filter, Details-on-demand, Relate, History, Extract**. Response-time thresholds: ~0.1 s feels instantaneous, ~2 s is a limit for most tasks, ~10 s loses attention.

---

## 👁️ Krug's Usability Heuristics

- **First Law:** don't make me think. **Three facts:** we **scan**, we **satisfice** (Back is the most-used button), we **muddle through**.
- **Billboard Design 101:** clear visual hierarchy (prominence relates to importance; visually nested areas), **conventions** (break one only when clearly better), minimize noise, **omit needless words** (remove half, then half again). Kill happy talk and instructions.
- **Mindless choices:** "three mindless, unambiguous clicks equal one difficult click."
- **Navigation:** persistent Site ID, Sections, Utilities, Page name, "you are here", local nav, Search. Page names must **match the words clicked** (the implicit social contract). Pass the **Trunk Test**: what site, what page, what sections, options here, where am I, how do I search?
- **Home page:** a 6–8 word differentiating tagline and a clear "where do I start?"; guard against the **tragedy of the commons** (promotion overload).
- **Usability testing ("10 cents a day"):** one user at a time, think-aloud, 3 users early, iterative; focus groups ≠ usability tests; fix the most serious problems first.
- **Goodwill reservoir:** problems drain it, courtesies replenish it. Accessibility benefits everyone.

---

## 🧠 Laws of UX (Yablonski)

**Jakob's Law** (users expect your site to work like others — leverage conventions); **Fitts's Law** (target time varies with distance/size — touch targets ≥44×44 CSS px, well spaced; `ID = log₂(2D/W)`); **Miller's Law** (7±2 chunks — chunk and offload); **Hick's Law** (decision time grows with choices — reduce/simplify when speed matters, but don't over-simplify); **Postel's Law** (be conservative in what you send, liberal in what you accept); **Peak–End Rule** (judge by the peak and the end — design the emotional peak); **Aesthetic–Usability Effect** (attractive feels more usable — and can mask problems in testing); **Von Restorff Effect** (the distinct item is remembered — emphasise key actions with restraint); **Tesler's Law** (irreducible complexity must live in the system or the user); **Doherty Threshold** (<400 ms keeps attention).

Supporting: **Gestalt** (proximity, similarity, closure, figure/ground), **mental models**, **flow** (balance challenge vs skill), progressive disclosure, cognitive load, selective attention.

---

## 🔁 The Hook Model (Eyal)

Habits = behaviors done with little conscious thought; frequency is a prerequisite. Cycle: **Trigger** (external → internal emotion; the 5 Whys surface it) → **Action** (Fogg: trigger + ability + motivation; three core motivators, six ability factors) → **Variable Reward** (tribe, hunt, self) → **Investment** (stored value makes the product better with use). Habit Testing: identify devotees → codify → spread. The **Manipulation Matrix** forces the ethics question (does it materially improve lives?).

---

## 🤖 Designing AI Interfaces (Macfadyen)

Reject "the model is the interface"; a bare chat box lowers the barrier to **misplaced trust**. Framework: **Input → Computation → Output**.

- **Input:** three channels (implicit context, explicit prompting, direct manipulation); the **CARE** prompt framework (Context, Action, Results, Examples); starter prompts are product positioning.
- **Computation:** manage latency (<400 ms feedback, progress), design error messages (what happened, recoverable?, what next) and momentum.
- **Output:** the output is not the answer. Six principles — **Clarity, Verifiability, Grounding, Actionability, Adjustability, Multiturn**. Ground by declaring model/version, tools, jurisdiction, timeframe; provide forward actions and iterate rather than restart.
- **Overreliance:** skill atrophy, automation bias, confirmation bias, ordering effects — use cognitive forcing functions, honest capability claims, progressive disclosure, and space for disagreement (anti-**sycophancy**). Avoid **false-precision confidence indicators**.
- **Agentic AI:** patterns (Reflection, Tool Use, Planning, Multiagent Collaboration, ReAct) plus three principles: **Reveal the Plan** (show interpretation before acting), **Prioritize What Matters Most** (layered progress), **Design for Shared Control** (adjustable autonomy, interruptibility, checkpoints, rollback).

---

## ⚠️ Pitfalls

- Forcing users to think; inconsistent terminology or placement (doubles think time).
- Cluttered home pages; vague or hostile error messages.
- Relying on subtle cues (make them ~2× more prominent); over-simplifying into uselessness.
- Unverified AI output presented as authoritative; false-precision confidence.
- Ignoring accessibility, motion sensitivity and universal usability.

---

## 🔗 Integration with Other Skills

- For the design-engineering and anti-slop visual craft, see [ui-ux-designer](../../../roles/ui-ux-designer/SKILL.md) and [frontend-developer](../../../roles/frontend-developer/SKILL.md).
- For accessibility conformance, see [ui-ux-designer](../../../roles/ui-ux-designer/SKILL.md).
- For AI feature trust and safety, see [ai-application-engineering](../../../domains/industry/ai-application-engineering/SKILL.md).
