---
name: "ui-style-scrollytelling"
description: "Provides the scrollytelling / narrative scroll style (2012-present): scroll-sequenced stories from NYT Snow Fall to native CSS scroll-driven animations, covering pin/scrub/stepped patterns, ScrollTrigger and scrollama tooling, the scroll-driven animations API, performance rules and reduced-motion cuts. Use when building data stories, explainers or product narratives sequenced by scroll."
---

# UI Style: Scrollytelling (Narrative Scroll)

Scroll position sequences a narrative: full-bleed media, pinned scenes, stepped annotations. Origin: NYT "Snow Fall" (John Branch, December 20, 2012; 2013 Pulitzer); industrialized by The Pudding (2017); standardized by native CSS scroll-driven animations (Chrome 115, July 2023). Synthesized from verified research; see Sources.

---

## 🧭 When to Activate

- Building investigative/data narratives, explainers, annual reports.
- Converting a product story with genuine sequence into scroll steps.
- Choosing between GSAP ScrollTrigger, scrollama and native CSS animation timelines.

---

## 🕰️ Definition and Timeline

- "Snow Fall" (Dec 20, 2012) — original URL now dead; archived. Follow-ups: "A Game of Shark and Minnow" (2013); The Pudding founded 2017; term "scrollytelling" commonly attributed to Brian Boyer (NPR Visuals) [unverified attribution].
- Tooling eras: ScrollMagic (2014) → GSAP ScrollTrigger (2019) → scrollama (IntersectionObserver, 2017+) → **CSS `animation-timeline: scroll()/view()`** (Chrome/Edge 115+; Safari 26+; Firefox in preview).

---

## 🎨 Visual DNA

- Full-viewport media backdrops; sticky canvas with overlaid text cards; editorial serif display + neutral sans body; stepped scene rhythm (1→2→3); generous vertical whitespace; progress indicators; cinematic aspect ratios.

---

## 🖱️ Interaction and Motion

- **Pin:** element fixed between scroll positions; **scrub:** animation progress tied 1:1 to scroll (or smoothed, `scrub: 1`); stepped scenes fire at IntersectionObserver thresholds; parallax layers at different rates; horizontal sections driven by vertical scroll (`containerAnimation`); velocity-aware effects.

---

## 🛠️ Implementation Notes

- Zero-JS baseline: `position: sticky` + opacity/transform-only animation.
- Native CSS: `animation-timeline: view(); animation-range: entry 0% entry 100%;` — runs off the main thread; JS `ScrollTimeline`/`ViewTimeline` via WAAPI; demo suite at scroll-driven-animations.style.
- GSAP ScrollTrigger for pin/scrub/snap (`anticipatePin`, matchMedia-responsive); scrollama for stepwise charts.
- Rules: animate only `transform`/`opacity`; lazy-load below-fold media; hero video risks LCP — provide a poster; CLS < 0.1; **never hijack scroll** (ScrollTrigger docs position themselves as "no scroll-jacking").

---

## ♿ Accessibility and Performance

- Provide a reduced-motion cut: skip scrub, show final states (`prefers-reduced-motion`, Baseline Jan 2020).
- Ensure all content is keyboard-reachable — stepped reveals hidden from non-scroll input are a common failure.

---

## ✅ When to Use / ❌ When to Avoid

- **Use:** stories with genuine sequence; data narratives; annual reports.
- **Avoid:** shallow marketing padding 3 sentences across 10 viewports; pages with interstitial ads; anything users must search within.

---

## ⚠️ Pitfalls

- Post-Snow-Fall "style over substance" imitation; scroll-jacking backlash; graphics rot when libraries age; readers losing their place.

---

## 📚 Sources

- John Branch, "Snow Fall: The Avalanche at Tunnel Creek", NYT, Dec 20, 2012 — https://www.nytimes.com/newsgraphics/2012/12/30/snow-fall/ (original URL now 404; Internet Archive copy)
- Bramus, "Animate elements on scroll with Scroll-driven animations", Chrome for Developers, 2023 — https://developer.chrome.com/docs/css-ui/scroll-driven-animations
- GSAP ScrollTrigger docs (v3.15) — https://gsap.com/docs/v3/Plugins/ScrollTrigger/
- MDN, "`prefers-reduced-motion`" — https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion
- MDN, "Intersection Observer API" — https://developer.mozilla.org/en-US/docs/Web/API/Intersection_Observer_API
- Russell Goldenberg, scrollama, The Pudding, 2017 — https://github.com/russellsamora/scrollama

---

## 🔗 Integration with Other Skills

- Sibling styles: [ui-style-parallax-scrolling](../ui-style-parallax-scrolling/SKILL.md), [ui-style-3d-immersive-webgl](../ui-style-3d-immersive-webgl/SKILL.md), [ui-style-one-page-long-scroll](../ui-style-one-page-long-scroll/SKILL.md).
