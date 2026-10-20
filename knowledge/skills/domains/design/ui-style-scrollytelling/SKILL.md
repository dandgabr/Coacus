---
name: "ui-style-scrollytelling"
description: "Provides the scrollytelling, narrative scroll and one-page continuous scroll UI style (2012-present): scroll-sequenced stories, pinned scenes, stepped annotations and unified narrative long-scroll pages. Covers NYT Snow Fall origins, CSS animation-timeline scroll()/view(), ScrollTrigger/scrollama tooling, single-page anchor navigation and reduced-motion fallbacks. Use when building investigative data stories, product explainers or continuous one-page narrative sites."
---

# UI Style: Scrollytelling & One-Page Continuous Scroll

Scroll position orchestrating a unified narrative experience: full-bleed background media, pinned scenes, stepped annotations, and seamless single-page continuous flow. Originates with NYT "Snow Fall" (2012) and single-page landing site architecture, standardized by native CSS scroll-driven animations (`animation-timeline: view()`). Synthesized from verified research; see Sources.

---

## 🧭 When to Activate

- Investigative journalism, data narratives, product explainers, annual reports, and cinematic landing pages.
- Converting complex multi-step stories or single-page portfolios into sequenced scroll chapters.
- Implementing sticky-pinned presentation decks or scroll-scrubbed interactive demos.

---

## 🕰️ Definition and Timeline

- **Origins:** NYT "Snow Fall" (John Branch, December 2012; Pulitzer Prize 2013) demonstrated the power of scroll position driving multi-media narrative flow. Industrialized by *The Pudding* (Russell Goldenberg, 2017) with the `scrollama` library.
- **One-Page Long Scroll Architecture:** The single-page portfolio and campaign site paradigm (2010s–present) that unifies navigation, storytelling, and conversion into an uninterrupted vertical journey with smooth anchor jumps (`scroll-behavior: smooth`).
- **Tooling Evolution:** ScrollMagic (2014) -> GSAP ScrollTrigger (2019) -> native CSS Scroll-Driven Animations API (Chrome 115+, Safari 26+).
- **Difference from neighbors:** Unlike [ui-style-parallax-scrolling](../ui-style-parallax-scrolling/SKILL.md), which is primarily a decorative background depth effect, Scrollytelling is fundamentally *narrative*: scroll position directly reveals content, shifts scenes, and communicates information sequentially.

---

## 🎨 Visual DNA

- **Layout Structure:** Full-viewport media canvases (`min-height: 100vh`), sticky background containers (`position: sticky; top: 0;`), and overlaid text narrative cards.
- **Typography:** Refined editorial serifs (Instrument Serif, Fraunces) paired with neutral sans-serif body text (Inter, Roboto).
- **Progress Trackers:** Persistent vertical or horizontal progress bars, chapter dots, and current-section indicators.
- **Cinematic Rhythm:** Deliberate pacing, generous vertical whitespace, and seamless transitions between chapter milestones.

---

## 🖱️ Interaction and Motion

- **Pin & Scrub:** Elements lock in place (`position: sticky`) while scroll progress scrubs a visual state (0% to 100%).
- **Step Transitions:** Stepped annotations fade and slide in when crossing viewport thresholds (`IntersectionObserver`).
- **Native Scroll First:** Choose continuous, scrubbed or explicitly requested scene presentation. Preserve native scrolling by default. For an authorized scene deck, scope input to its owner, preserve nested scrolling and zoom, and provide keyboard/touch navigation and exits. See [ui-scroll-driven-motion](../ui-scroll-driven-motion/SKILL.md) for narrative modes and stepped-presentation contracts.
- Under `prefers-reduced-motion: reduce`, disable all pinned scrub animations, displaying all content sequentially in standard static flow.

---

## 🛠️ Implementation Notes

- Resolve scene and observer selectors against the rendered component tree, including wrappers such as tabs or panels. Verify that every intended chapter is observed and that scrolling changes the active chapter and progress indicator.
- Assert that revealed content is actually visible and has rendered dimensions (for example, chart bars with positive height); state classes alone do not prove the narrative content appeared. Check cleanup on style changes and the static reduced-motion path.
- For broader responsive, dialog, and live-asset checks, use [rendered-interface verification](../../../engineering/practices/ui-design-craftsmanship/references/rendered-interface-verification.md).

```css
:root {
  --story-bg: #0f1115;
  --story-fg: #f0f2f5;
  --story-accent: #2e6ff2;
}
body { background: var(--story-bg); color: var(--story-fg); scroll-behavior: smooth; }
.scene-container {
  position: relative;
  min-height: 300vh;
}
.sticky-stage {
  position: sticky;
  top: 0;
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
}
.story-card {
  position: relative;
  margin: 80vh auto;
  max-width: 520px;
  background: rgba(15, 17, 21, 0.85);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 16px;
  padding: 2rem;
}
@media (prefers-reduced-motion: reduce) {
  body { scroll-behavior: auto; }
  .scene-container { min-height: auto; }
  .sticky-stage { position: relative; height: auto; }
  .story-card { margin: 2rem auto; }
}
```

- Prefer native CSS `animation-timeline: view()` where supported; fall back gracefully to `IntersectionObserver`. Timelines, ScrollTrigger pinning, sticky stages, snapping and image sequences are specified in [ui-scroll-driven-motion](../ui-scroll-driven-motion/SKILL.md); this skill owns the narrative style.
- Scrollama 3.2.0 has not been published since 2022; prefer a plain `IntersectionObserver` step tracker or ScrollTrigger for new work.
- Ensure all narrative chapters are directly accessible via standard keyboard navigation (Tab and Page Down) and anchor links.

---

## ♿ Accessibility

- **Keyboard Reachability:** Never conceal information that can only be unlocked via mousewheel events. Keyboard users must be able to step through every scene.
- **Skip Link (2.4.1 Bypass Blocks):** Place a "Skip the story" link before a long pinned or scrubbed narrative, visible on focus, that moves focus to the first content after it. SC 2.4.1 strictly targets blocks repeated across pages; treat the skip link as required here regardless, because a multi-screen narrative costs keyboard and screen-reader users dozens of steps to pass.
- **Reduced Motion Alternatives:** Respect `prefers-reduced-motion: reduce` by laying out scenes sequentially without sticky pins or scrubbing.
- **Scroll Contrast:** Ensure overlaid narrative text cards have sufficient background opacity to meet WCAG 1.4.3 (4.5:1 ratio) regardless of underlying media.

---

## ✅ When to Use / ❌ When to Avoid

- **Use:** Product launch walkthroughs, data investigations, annual company reports, and story-driven creative agency portfolios.
- **Avoid:** Search engines, e-commerce product catalogs, documentation references, and administrative data entry.

---

## 📚 Sources

- John Branch, "Snow Fall: The Avalanche at Tunnel Creek", *The New York Times*, 2012.
- Bramus, "Scroll-driven Animations", Chrome Developer Documentation, 2023.
- Russell Goldenberg, *Scrollama*, The Pudding, 2017 — https://github.com/russellsamora/scrollama
- W3C, *Web Content Accessibility Guidelines 2.2* — https://www.w3.org/TR/WCAG22/

---

## 🔗 Integration with Other Skills

- Sibling narrative and motion styles: [ui-style-parallax-scrolling](../ui-style-parallax-scrolling/SKILL.md), [ui-style-3d-immersive-webgl](../ui-style-3d-immersive-webgl/SKILL.md), [ui-style-editorial-archive-luxury](../ui-style-editorial-archive-luxury/SKILL.md).
- Scroll mechanics, support matrix and fallbacks: [ui-scroll-driven-motion](../ui-scroll-driven-motion/SKILL.md).
## Appearance and Interaction Verification

Choose continuous/reveal, pin/scrub or explicitly requested scene presentation before implementation; keep native behavior by default, scope any requested input handling with keyboard/touch exits, make oversized scenes reachable at actual usable height and verify progress over local stacking contexts.

## Version Sources

Moving release pins in this file were resolved 2026-10-20:

- **scrollama 3.2.0** (verified) — stale: it is the latest npm release, last published 2022-06-17 (https://registry.npmjs.org/scrollama)
