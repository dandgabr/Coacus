---
name: "ui-style-parallax-scrolling"
description: "Provides the parallax scrolling design era (2011-2016): layered depth via differential scroll motion, covering the Silverback/Nike lineage, skrollr and ScrollMagic tooling, the Purdue nausea findings, scroll-hijacking criticism and the native CSS successors. Use when building scroll-depth effects responsibly or studying the era's usability evidence."
---

# UI Style: Parallax Scrolling

Background layers move slower than foreground, creating 2.5D depth purely through differential scroll motion. Web origin: Brett Taylor's 2007 blog experiment; popularized by Paul Annett's Silverback technique (2008); mainstream breakout with Nike "Better World" (2011); peak 2011–2016. Synthesized from verified research; see Sources.

---

## 🧭 When to Activate

- Building campaign/launch storytelling with scroll-driven depth.
- Choosing between legacy libraries and native CSS scroll-driven animations.
- Reviewing parallax pages for vestibular safety and mobile performance.

---

## 🕰️ Definition and Timeline

- Inherited from Disney's multiplane camera and arcade games (Moon Patrol, 1982).
- Web: Brett Taylor ("Glutnix") first browser implementation (JS + CSS2, Mar 20, 2007); Paul Annett's pure-CSS Silverback parallax (Think Vitamin, Feb 2008, demoed at SXSW 2009); *Handcrafted CSS* (2010) cites Silverback as the first known example.
- Peak 2011–2016 (single-page campaigns, Apple product pages); declined under mobile performance, scroll-hijacking fatigue and vestibular accessibility norms (`prefers-reduced-motion` Baseline-wide since Jan 2020).

---

## 🎨 Visual DNA

- Full-viewport fixed backgrounds; layered 2.5D scenes (sky/mid/foreground); large hero typography over imagery; long single-page narratives with pinned sections; depth communicated by motion, not shadows.

---

## 🖱️ Interaction and Motion

- Scroll-position keyframes (skrollr's `data-N` attributes); smooth-scroll easing; mobile fake-scrolling (skrollr disables native scroll and translates the body — iOS halts JS during scroll); mouse-move parallax; pin/scrub sections (ScrollMagic); the era's scroll-hijacking antipattern.

---

## 🛠️ Implementation Notes

- Legacy: scroll listeners writing `transform: translate3d()` inside `requestAnimationFrame`; jQuery+GSAP timelines (ScrollMagic); Keith Clark's pure-CSS 3D approach with `perspective` + `translateZ` (2014).
- `background-attachment: fixed` is unreliable on mobile Safari.
- Modern native successor: CSS scroll-driven animations (`animation-timeline`); accessibility gate: `@media (prefers-reduced-motion: reduce)`.

---

## ♿ Accessibility and Evidence

- Purdue study (Frederick et al., 2013): parallax "did not necessarily improve the overall user experience" and "may cause certain people to experience nausea"; scaling/panning large objects are documented vestibular triggers (MDN).
- skrollr's own maintainer: mobile support "always sucked… you shouldn't compromise UX for some fancy UI effects" (library archived 2018).

---

## ✅ When to Use / ❌ When to Avoid

- **Use:** campaign storytelling, portfolio one-pagers, product showcases where the narrative is the content.
- **Avoid:** content/SEO-critical pages, mobile-first utility products, low-end devices, vestibular-sensitive audiences.

---

## ⚠️ Pitfalls

- Scroll-jacking breaks expectations; jank from non-composited effects; SEO risk when content renders only inside animation timelines.

---

## 📚 Sources

- Wikipedia, "Parallax scrolling" — https://en.wikipedia.org/wiki/Parallax_scrolling
- Brett Taylor, "Parallax Backgrounds — a multi-layered javascript experiment", Mar 20, 2007 (archived) — https://web.archive.org/web/20190128230104/https://inner.geek.nz/archives/2007/03/20/parallax-backgrounds/
- Paul Annett, "How to Recreate Silverback's Parallax Effect", Think Vitamin, Feb 2008 (archived) — https://web.archive.org/web/20100719124948/http://thinkvitamin.com/design/how-to-recreate-silverbacks-parallax-effect/
- Dede M. Frederick, "The Effects Of Parallax Scrolling On User Experience And Preference In Web Design", Purdue University, 2013 — https://docs.lib.purdue.edu/cgttheses/27/
- Alexander Prinzhorn, skrollr (archived 2018) — https://github.com/Prinzhorn/skrollr
- MDN, "`prefers-reduced-motion`" — https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion
- The A11Y Project, "Understanding Vestibular Disorders" — https://www.a11yproject.com/posts/understanding-vestibular-disorders/

---

## 🔗 Integration with Other Skills

- Sibling styles: [ui-style-scrollytelling](../ui-style-scrollytelling/SKILL.md), [ui-style-scrollytelling](../ui-style-scrollytelling/SKILL.md).
