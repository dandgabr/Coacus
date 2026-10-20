---
name: "web-accessibility-wcag"
description: "Provides inclusive web accessibility practice based on WCAG 2.2 and inclusive design patterns, covering semantic HTML5 landmarks and headings, the first rule of ARIA, accessible forms and navigation, alt-text composition, captions and transcripts, contrast and color-independence, motion and animation accessibility (pause controls, flash thresholds, reduced-motion house policy, accessible animated text), keyboard and screen-reader verification, AI-generated accessibility audits and alt text, and inclusive meetings and presentations. Use when building, auditing or reviewing web interfaces for disabled users or when generating accessible code with AI."
---

# AI Skill: Web Accessibility and Inclusive Design

This skill guides the AI to build interfaces that work for disabled users by construction, and to audit and remediate existing ones, treating accessibility as a foundational practice rather than a compliance afterthought. It synthesizes the practices of illustrated accessibility field guides and inclusive design pattern literature (Pickering; Gupta and Grossman-Kahn).

Resolve the current WCAG 2.x publication and the WAI-ARIA specification from the W3C before pinning levels or criteria.

For layered surfaces and appearance changes, use [painted contrast audits](../../../domains/design/color-contrast-accessibility/references/painted-contrast-audits.md). Validate native and custom control states, not only theme tokens. A sampled visual scan, a zero-error runtime check and a conformance assessment establish different claims; keep their coverage and unsupported cases explicit.

---

## 🧭 When to Activate

- Building or reviewing any user-facing web surface (pages, forms, components, emails, documents).
- Generating UI code with AI assistants and needing accessible output.
- Auditing an existing site or component library for conformance.
- Producing alt text, captions, transcripts or accessible social content.
- Planning inclusive meetings, presentations and shared media.

---

## 🧱 Semantics First: The Inclusive Baseline

- **Native elements beat ARIA patches.** The first rule of ARIA: prefer the native HTML element or attribute that already carries semantics and keyboard behavior; add roles and states only where native semantics are missing. Native behavior is also faster and more robust than custom JavaScript.
- **Document-level hygiene:** always declare the doctype (its absence triggers quirks mode); set the `lang` attribute — it drives screen-reader voice selection, translation, spell-check and `:lang()` styling; switch language per element for quoted content.
- **Heading structure:** one `<h1>` per page, never skip levels, real sectioning elements (`<section>`, `<nav>`, `<article>`, `<aside>`, `<header>`, `<footer>`) with landmarks and skip links. Do not rely on the HTML5 outline algorithm — browsers did not implement it; rely on explicit heading levels.
- **Design for extremes first:** the average user does not exist. Screen-reader support implies keyboard support, which also serves motor-impaired, RSI and situational users. Prefer conventions over invention — a familiar convention is inclusive; novelty in standard controls is exclusion.
- **Evaluation is by pattern, not pixel review:** judge each pattern by what it does without JavaScript, without CSS, on keyboard, in a screen reader and in high-contrast mode.

---

## 🧭 Responsive and Adaptive Foundations

- Design fully fluid; insert content breakpoints ("tweakpoints") only where content breaks, not per device.
- Never ship a viewport that disables zoom (`user-scalable=no`); zoom is an accessibility feature.
- Prefer source-order-friendly layout over absolute/fixed positioning, which breaks under magnification and content growth.
- Render icons robustly (inline SVG with `currentColor`) so Windows High Contrast Mode — which strips background images — keeps meaning.
- A visible border, label and perceived affordance on interactive controls is a cognitive-accessibility cornerstone and enables voice control.

---

## 🖼️ Text Alternatives

- **Alt-text formula:** subject + action + key details + the image's tone or intent; omit the "image of" prefix (screen readers already announce it); keep it to roughly one or two short sentences; summarize charts by their main insight, not bar by bar; never bake text into images — it locks out screen readers, braille displays, resizing and translation.
- Include demographic descriptors only when relevant to meaning; ask photographed people how they want to be identified.
- Alt text doubles as the fallback when images fail to load.
- At scale with AI: give the model a style guide in the prompt (what matters, length, tone, chart-summary behavior) and review output for offense or inaccuracy.

---

## 🎬 Captions, Transcripts and Audio

- Captions include non-speech sound cues and speaker identification; treat auto-generated captions as drafts that miss context and sound cues.
- Provide transcripts with timestamps so content is searchable and jumpable; remember many deaf users read the majority language as a second language.
- Never rely on color alone to encode meaning; pair color with underline, bold, patterns or position. Roughly one in twelve men is color-blind.
- Contrast minimums: 4.5:1 for normal text, 3:1 for large text; verify both light and dark modes.

---

## 🎞️ Motion and Animation

This section is the canonical source of motion accessibility obligations in Coacus; other skills link here instead of restating levels. Duration bands and springs live in [motion-timing-engines](../../../domains/design/ui-motion-interaction/references/motion-timing-engines.md).

| SC | Name | Level | Requirement for motion | Test |
|---|---|---|---|---|
| 2.2.2 | Pause, Stop, Hide | A | Auto-moving content lasting over 5 s beside other content gets a pause, stop or hide control; hover-only pause fails; motion started by scrolling into view counts as automatic | Inventory loops, marquees, carousels; operate each control by keyboard |
| 2.3.1 | Three Flashes or Below Threshold | A | No more than three flashes in any one second | Frame-step the animation; run a flash analyser on large strobing areas |
| 2.3.3 | Animation from Interactions | AAA | Interaction-triggered motion can be disabled unless essential | Set reduced motion; trigger every interaction |
| 1.4.13 | Content on Hover or Focus | AA | Animated tooltips and popovers are dismissible, hoverable and persistent | Escape dismisses; pointer can move onto the content |
| 2.4.11 | Focus Not Obscured (Minimum) | AA | Sticky, pinned or sliding layers never fully hide the focused element | Tab through with every sticky and pinned state active |
| 2.5.7 | Dragging Movements | AA | Drag gestures (sliders, reorder, swipe carousels) have a single-pointer non-drag alternative | Complete each task with taps or clicks only |
| 1.4.12 | Text Spacing | AA | Split-text spans survive user spacing overrides without clipping or overlap | Apply spacing overrides after the split runs |
| 4.1.3 | Status Messages | AA | Tickers, counters and typewriters expose only the final value | Screen reader hears one announcement per completed change |
| 1.4.10 | Reflow | AA | Horizontal-scroll sections collapse to one column at 320 CSS px | Zoom to 400 %; no two-dimensional scrolling |
| 2.4.3 | Focus Order | A | After a view transition, focus lands on the new view's heading or the logical next control | Cross every transition by keyboard |
| 2.5.8 / 2.5.5 | Target Size (Minimum / Enhanced) | AA / AAA | Animated targets measure at least 24×24 CSS px (AA); 44×44 is the enhanced level and the house target for primary touch controls | Measure the hit box at rest and mid-motion |

**House policy.** Honouring `prefers-reduced-motion` is WCAG technique C39 and a Coacus house policy, not an AA requirement.

- Author no-motion first: base styles are static; add motion inside `@media (prefers-reduced-motion: no-preference)`.
- `reduce` replaces spatial motion (translate, scale, zoom, parallax) with a cross-fade or an instant change. Never delete feedback, state or content.
- In script, read `matchMedia('(prefers-reduced-motion: reduce)')` and subscribe to its `change` event. Server rendering starts from the no-motion state and upgrades after hydration.
- `prefers-reduced-transparency` has no Safari support: ship opaque defaults and add translucency as an enhancement. Honour `prefers-contrast: more` with solid fills and stronger borders, and keep state legible under `forced-colors: active`.

**Vestibular triggers.** Treat large-area parallax, zoom, spin and scroll-linked motion of viewport-sized layers as vestibular triggers: gate them behind `no-preference` and offer an in-page motion toggle on scroll narratives.

**Animated text and hidden content.**

- Never put `aria-label` on a generic `span`, `div` or `p` (prohibited in ARIA 1.2). Render one visually hidden full-text copy and mark animated fragments `aria-hidden="true"`.
- Never attach `aria-live` to intermediate values; announce the final value only.
- Make collapsed or clipped content `inert`.
- Mark marquee clones `aria-hidden="true"` and `inert`, and render a visible pause control.

WCAG 3.0 is a W3C Working Draft (10 September 2026) and does not replace WCAG 2; keep conformance claims on WCAG 2.2.

---

## 📝 Forms, Navigation and Interaction

- Surface login-versus-register choices up front; sequential readers miss small post-submit links.
- Implement filters as fieldsets with legends and radio buttons submitted via GET (shareable, keyboard-friendly); mark selected states without color alone.
- If a navigation has fewer than about five items, show it — hiding content behind a menu button is a last resort, and when used must pair the icon with a visible text label.
- Use the simplest interactive pattern that meets the need; complexity must match necessity.
- Apply test-driven markup: write CSS selectors that intentionally match malformed ARIA structures and flag them visually, keeping complex widget patterns honest as they evolve.

---

## 🤖 AI-Assisted Accessibility Work

- **Generated code is inaccessible by default** — the training corpus is largely inaccessible. Escalate prompt specificity: name the component, the required semantics, the contrast and focus requirements, and the target conformance level and success criteria. Treat accessibility like security: foundational, not retrofitted.
- **AI audits catch only a minority of issues and hallucinate in both directions** (false pass and false fail). Require the specific WCAG success criterion for every finding; validate each claim manually or with real contrast tooling; keep a versioned audit log (flagged / fixed / verified).
- **Challenge generated defaults** in imagery of people — audit for the missing diversity and prompt to reinforce it (survivorship thinking: interrogate what is absent).

---

## 👥 Beyond the Screen: Meetings and Media

- Shorten meetings, schedule breaks, enable captions and chat, keep video optional for lip reading, mute by default with digital hand-raising, even speaking pace, and never touch a person's assistive device or service animal.
- In slide decks: limit palette, keep fixed color roles, avoid flashing or moving content, chunk information, write plainly and provide a summary up front.

---

## ⚠️ Pitfalls

- Treating conformance as the goal instead of the floor; a passing contrast pair can still fail in practice.
- Patching inaccessible markup with ARIA instead of using the native element.
- Encoding meaning in color alone or inside images.
- Trusting an AI audit without verification, or an auto-caption without review.
- Shipping AI-generated UI without accessible-by-construction prompts and review.

---

## 🔗 Integration with Other Skills

- For visual craft and design-system rigor, see [ui-ux-designer](../../../roles/ui-ux-designer/SKILL.md) and [frontend-developer](../../../roles/frontend-developer/SKILL.md).
- For the underlying UX principles, see [ui-ux-principles](../ui-ux-principles/SKILL.md).
- For trustworthy AI feature behavior, see [ai-application-engineering](../../../domains/industry/ai-application-engineering/SKILL.md).

---

## Version Sources

Moving standard pins in this file were resolved 2026-10-20:
- **WCAG 2.2** (verified) — W3C Recommendation, 12 December 2024 edition — https://www.w3.org/TR/WCAG22/
- **WCAG 3.0** (verified) — W3C Working Draft, 10 September 2026 — https://www.w3.org/TR/wcag-3.0/
