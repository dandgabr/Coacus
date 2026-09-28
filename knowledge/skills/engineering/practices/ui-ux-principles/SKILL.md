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

## 🧠 AI-Native UX Patterns (Nudelman; Pilot)

- **Use-case selection heuristic:** any project premised on "AI will tell domain experts how to do their job" is a red flag; reframe as which question, answered by AI, makes the expert's decision better. The best AI is augmented intelligence.
- **Copilot layout framework:** task importance scales screen real estate — side panel (page-local, never obscures), large overlay (almost always worst: close/reload cycles), or full page (an AI-first alternative experience with its own navigation). SaaS copilots need stateful multi-conversation sessions, proprietary-data grounding, and simple hub-and-spokes IA (landing → session list → chat terminal).
- **Seven LLM interaction patterns:** restating the interpreted query, auto-complete, talk-back, initial suggestions, next-steps continuation, regeneration tweaks (the opposite workflow), and guardrails.
- **Value Matrix:** multiply each confusion-matrix outcome (TP/TN/FP/FN) by its dollar benefit or cost and by the human cost side; select models by real-world ROI, not data-science metrics. Conservative and recall-optimized models each win under different cost assumptions.
- **Anomaly UIs:** separate anomaly from alert; occurrence timers gate alerting; dynamic thresholds suit seasonal metrics and static thresholds suit compliance or hard-limit metrics; always preview history before saving threshold changes and keep a manual override.
- **Agentic UX:** supervisor-agent loops need flexible, multi-stage workflows where humans accept or reject suggested observations; recall-optimized "aggressive" agents attempt costly or consent-requiring actions — design explicit approval flows and cost awareness.
- **New UCD process:** iterate UI + AI + data simultaneously; the "spike" is a rough proof of concept answering "does the model produce the desired outcome?"; modern Wizard-of-Oz testing pairs a design shell with live spiked AI output. Treat developers as handoff customers; AI products are trained, not programmed — never done.
- **Shift-left prototyping (Pilot):** when making is cheap, prototypes become thinking tools — learn by making, match fidelity to the learning goal, avoid premature visual polish; treat every AI output as a hypothesis to validate with humans; prompting is a design brief (user, goal, constraints, success criteria).

---

## 🗂️ Information Architecture Classics (Morville & Rosenfeld)

- IA is the structural design of shared information environments through four interlocking systems: **organization, labeling, navigation and search**.
- **Organization schemes:** exact (alphabetical, chronological, geographical) versus ambiguous (topic, task, audience, metaphor) — ambiguous is harder yet more valuable because users rarely know what they want; it demands user testing and maintenance.
- **Structures:** hierarchy/taxonomy as default; database model (metadata + controlled vocabulary) for homogeneous chunks; hypertext layered for nonlinear relations; social classification as a supplement.
- **Labeling consistency:** across style, presentation, syntax, granularity, comprehensiveness and audience register; language ambiguity is irreducible, so narrow scope and test.
- **Navigation:** embedded (global, local, contextual) plus supplemental (site maps, indexes); provide you-are-here cues and respect browser navigation.
- **Search:** zones (by audience, topic, content type) reduce apples-and-oranges results; index content components, not boilerplate; sorting serves decision tasks and ranking serves learning tasks; show result counts and never overload the first screen.
- **Faceted classification:** facets (topic, product, type, audience, geography, price) enable faceted search, faceted sorting and guided navigation — multiple simultaneous paths to the same content on an enduring metadata foundation; controlled vocabularies follow ANSI-NISO thesaurus standards.
- **Research loop:** context, content and users overlap; start with business context — ignoring business realities is as dangerous as ignoring users. The value case: lower cost of finding, of finding wrong information, and of not finding at all.

---

## ⚠️ Pitfalls

- Forcing users to think; inconsistent terminology or placement (doubles think time).
- Cluttered home pages; vague or hostile error messages.
- Relying on subtle cues (make them ~2× more prominent); over-simplifying into uselessness.
- Unverified AI output presented as authoritative; false-precision confidence.
- Ignoring accessibility, motion sensitivity and universal usability.

---

## 🎨 Design Style Library (per-style deep dives)

The catalog now carries one canonical skill per style with visual DNA, motion, CSS techniques, accessibility trade-offs and a verified bibliography:

- [3d immersive webgl](../../../domains/design/ui-style-3d-immersive-webgl/SKILL.md)
- [acid anti design](../../../domains/design/ui-style-acid-anti-design/SKILL.md)
- [ai native generative ui](../../../domains/design/ui-style-ai-native-generative-ui/SKILL.md)
- [aurora mesh gradient](../../../domains/design/ui-style-aurora-mesh-gradient/SKILL.md)
- [bento grid](../../../domains/design/ui-style-bento-grid/SKILL.md)
- [card based ui](../../../domains/design/ui-style-card-based-ui/SKILL.md)
- [claymorphism](../../../domains/design/ui-style-claymorphism/SKILL.md)
- [cyberpunk hud](../../../domains/design/ui-style-cyberpunk-hud/SKILL.md)
- [dark mode first](../../../domains/design/ui-style-dark-mode-first/SKILL.md)
- [editorial archive luxury](../../../domains/design/ui-style-editorial-archive-luxury/SKILL.md)
- [expressive variable typography](../../../domains/design/ui-style-expressive-variable-typography/SKILL.md)
- [flat design](../../../domains/design/ui-style-flat-design/SKILL.md)
- [frutiger aero](../../../domains/design/ui-style-frutiger-aero/SKILL.md)
- [glassmorphism](../../../domains/design/ui-style-glassmorphism/SKILL.md)
- [gradient duotone](../../../domains/design/ui-style-gradient-duotone/SKILL.md)
- [kinetic typography](../../../domains/design/ui-style-kinetic-typography/SKILL.md)
- [material you](../../../domains/design/ui-style-material-you/SKILL.md)
- [maximalism](../../../domains/design/ui-style-maximalism/SKILL.md)
- [metro modern ui](../../../domains/design/ui-style-metro-modern-ui/SKILL.md)
- [micro interactions](../../../domains/design/ui-style-micro-interactions/SKILL.md)
- [neo brutalism](../../../domains/design/ui-style-neo-brutalism/SKILL.md)
- [neumorphism](../../../domains/design/ui-style-neumorphism/SKILL.md)
- [one page long scroll](../../../domains/design/ui-style-one-page-long-scroll/SKILL.md)
- [organic biophilic](../../../domains/design/ui-style-organic-biophilic/SKILL.md)
- [parallax scrolling](../../../domains/design/ui-style-parallax-scrolling/SKILL.md)
- [scrollytelling](../../../domains/design/ui-style-scrollytelling/SKILL.md)
- [skeuomorphism](../../../domains/design/ui-style-skeuomorphism/SKILL.md)
- [swiss web minimalism](../../../domains/design/ui-style-swiss-web-minimalism/SKILL.md)
- [web brutalism](../../../domains/design/ui-style-web-brutalism/SKILL.md)
- [y2k revival](../../../domains/design/ui-style-y2k-revival/SKILL.md)

---

## 🔗 Integration with Other Skills

- For the design-engineering and anti-slop visual craft, see [ui-ux-designer](../../../roles/ui-ux-designer/SKILL.md) and [frontend-developer](../../../roles/frontend-developer/SKILL.md).
- For accessibility conformance, see [ui-ux-designer](../../../roles/ui-ux-designer/SKILL.md).
- For AI feature trust and safety, see [ai-application-engineering](../../../domains/industry/ai-application-engineering/SKILL.md).
