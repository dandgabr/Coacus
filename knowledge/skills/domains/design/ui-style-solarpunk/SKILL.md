---
name: "ui-style-solarpunk"
description: "Provides the solarpunk UI and UX style (2008-present): optimistic, sustainable futures expressed as sunlit visuals, garden-like navigation, low-data flows, hopeful microcopy and community patterns, covering palette, type, components, low-energy design and accessibility. Use when designing climate, civic, cooperative, education or sustainability products that need an honest, hopeful interface language."
---

# UI Style: Solarpunk

The "-punk" genre that answers cyberpunk with hope: renewable energy, community resilience, DIY culture and nature woven into the built environment. Translated to the web as sunlit, plant-rich, human-scale interfaces. Synthesized from the sources below; see Sources.

---

## 🧭 When to Activate

- Designing components, patterns and flows (navigation, onboarding, forms, states) for climate, renewable-energy, urban-farming, cooperative, mutual-aid or civic-tech products with an optimistic, non-doom voice.
- Design systems and brand for regenerative or community-owned organizations, including low-data and low-energy performance budgets.
- Reviewing whether a "green" experience is substantive or decorative.

---

## 🕰️ Definition and Timeline

- Coinage: Wikipedia dates the term to 2008, from an anonymous blog post "From Steampunk to Solarpunk"; a Brazilian anthology (2012) marked early explicit genre entries; momentum grew through the 2010s. Adam Flynn's "Solarpunk: Notes toward a manifesto" (Project Hieroglyph, 2014) and the 2019 "A Solarpunk Manifesto" consolidated the ethos.
- "Punk" meaning: DIY, anti-capitalist and decolonial values; the question "what does a sustainable civilization look like, and how can we get there?" Described as the inverse of cyberpunk.
- Canonical works named in the sources: Le Guin, *The Dispossessed* (1974, precursor); Becky Chambers, *A Psalm for the Wild-Built* (2021).
- Versus [ui-style-organic-biophilic](../ui-style-organic-biophilic/SKILL.md): biophilic is a calm, wellness-led nature-imitation language with no politics; solarpunk adds visible technology (panels, wind, mesh networks), community and activism as content, and a brighter, higher-energy palette.
- Versus its night sibling [ui-style-lunarpunk](../ui-style-lunarpunk/SKILL.md): this skill is daylight, openness and abundance.

---

## 🎨 Visual DNA

- **Color:** leaf and moss greens (`#2F7D4F`, `#8CC084`), sky blue (`#4FA3D1`), sun gold (`#F2B632`), terracotta (`#C8643B`), warm cream ground (`#FBF6E9`); ink in deep forest (`#1B3A2A`), not pure black.
- **Type:** humanist and slightly quirky: Fraunces, Recoleta-style soft serifs or Bricolage Grotesque for display; Source Sans / Nunito for body. Hand-lettered accents sparingly.
- **Ornament:** Art Nouveau-influenced curving vines, leaf-and-circuit hybrids, sun rays, hexagonal cells; solar panels and wind turbines drawn as friendly icons, not hardware photography.
- **Layout:** soft asymmetry, rounded organic blobs (`border-radius` with mixed values), layered sections that overlap like terraces; abundant whitespace around dense "garden" clusters of cards.
- **Imagery:** illustrated rooftop gardens, bikes, trams, communal kitchens; diverse people shown doing, not posing.
- **Texture:** light paper grain or watercolor wash; avoid glossy chrome.

---

## 🖱️ Interaction and Motion

- Growth metaphors: sections unfold like sprouts (scale 0.96 to 1, 300-500ms ease-out), vines draw with `stroke-dashoffset`, sun-position hero lighting that shifts with time or scroll.
- Gentle, breathing loops (leaf sway under 4deg, slow cloud drift) only as ambience; pause on hover of text and honor reduced motion.
- Feedback is warm and tactile: buttons soften and brighten, never snap or glitch.

---

## 🧩 UX Patterns

- **IA and navigation:** a "garden" metaphor (plots, seasons, paths) for top-level groups of community, projects and impact; labels stay plain ("Projects", "Energy", "Join"). Metaphor gives way to convention for header nav, search, cart, account, settings and legal links: keep standard names and positions (Nielsen heuristics 2 and 4).
- **Flows:** onboarding as a short local-first path (pick your place, pick your goal, see one real result), skippable; forms ask only what is needed and never re-ask (WCAG 3.3.7); progressive disclosure for impact data; checkout and donation show cost and recurrence before commitment.
- **Search and settings:** filters by place, energy type and participation; settings include a "Low-data mode" (no autoplay, static illustration, system fonts), default on for slow or save-data connections.
- **Voice:** warm, concrete, collective ("we", "your neighborhood"), no guilt, no doom counters; claims carry a figure and a source.
- **States:** empty = an invitation ("Nothing planted yet. Start a plot."); loading = a short sprout with plain text status, skeleton over spinner (heuristic 1); error = say what happened and how to fix it, calm tone (heuristic 9); success = one specific outcome ("12 kWh shared this week"), not confetti.
- **Sustainability UX:** treat page weight, requests and media as design constraints: compress and lazy-load images, avoid autoplay video, reuse system fonts, measure with a carbon calculator (Sustainable Web Design's guidelines cover UX design, development, hosting and strategy).
- **Risks:** greenwashing erodes trust; ornamental abundance raises cognitive load; whimsical labels slow scanning. Offsets and "eco" badges need verifiable detail.
- **Checks:** task success rate on 3 core tasks (join, find a project, change a setting) at or above 90 percent; time on task versus a conventional baseline; SUS at or above 80 (target, unverified synthesis); page weight and CO2 per view budgeted per template.

---

## 🛠️ Implementation Notes

```css
:root {
  --sun: #F2B632; --leaf: #2F7D4F; --moss: #8CC084;
  --sky: #4FA3D1; --clay: #C8643B; --paper: #FBF6E9; --ink: #1B3A2A;
}
body { background: var(--paper); color: var(--ink); font-family: "Nunito", system-ui, sans-serif; }
.card { background: #fff; border: 2px solid var(--leaf);
  border-radius: 28px 12px 32px 14px / 14px 30px 12px 28px; }
.sun-glow { background: radial-gradient(circle at 80% 0%, rgb(242 182 50 / .45), transparent 55%); }
.vine path { stroke: var(--leaf); stroke-dasharray: 1; stroke-dashoffset: 1; animation: grow 1.6s ease-out forwards; }
@keyframes grow { to { stroke-dashoffset: 0; } }
@media (prefers-reduced-motion: reduce) { .vine path { animation: none; stroke-dashoffset: 0; } }
```

- Use `pathLength="1"` on SVG paths so the dash trick is length-independent.
- Ship real sustainability data (energy mix, carbon figures) in the interface; ornament alone is the greenwashing failure.
- Prefer lightweight inline SVG and system-friendly fonts; a sustainable brand with a 4 MB hero video undermines its message.

---

## ♿ Accessibility

- Pale greens, gold and sky blue on cream commonly fail 1.4.3 (4.5:1 text, 3:1 large). Use `--ink` or dark leaf for text; gold is for fills and decoration only. Verify each pair.
- 1.4.11 non-text contrast (3:1) for borders, icons and chart colors; do not rely on green versus red alone (1.4.1), add icons or labels.
- Ornamental vines and rays: `aria-hidden="true"` / empty alt (1.1.1); never place text over busy illustration without a solid scrim.
- Looping and scroll-driven growth: honor `prefers-reduced-motion`; provide a pause control for loops over 5s (2.2.2); keep targets at least 24px (2.5.8); focus ring visible against organic shapes (2.4.7, 2.4.11).

---

## ✅ When to Use / ❌ When to Avoid

- **Use:** energy and climate products, co-ops, community platforms, education, regenerative or B-corp brands, civic futures storytelling.
- **Caution:** fintech and e-commerce (credibility versus whimsy); data-dense dashboards (apply tokens, not ornament).
- **Avoid:** brands whose practices contradict the claim; high-stakes safety-critical UI where decoration competes with signal.

---

## ⚠️ Pitfalls

- Greenwashing: scholars quoted by Wikipedia warn the genre can look sustainable aesthetically while avoiding systemic change; pair the look with verifiable claims.
- Cottagecore drift into twee pastel sameness; leaf-icon clipart on generic SaaS layouts.
- Low-contrast pastel text; heavy illustration weight; techno-utopian erasure of labor and justice themes the genre is built on.

---

## 📚 Sources

- "Solarpunk" (Wikipedia), accessed 2026 — https://en.wikipedia.org/wiki/Solarpunk
- "Cyberpunk derivatives" (Wikipedia), accessed 2026 — https://en.wikipedia.org/wiki/Cyberpunk_derivatives
- Adam Flynn, "Interview with Adam Flynn on Solarpunk" (Dragonfly: An exploration of eco-fiction), July 2, 2015 — https://dragonfly.eco/interview-with-adam-flynn-on-the-solarpunk-movement/ (page read; Flynn's "Solarpunk: Notes toward a manifesto" appeared on ASU's Hieroglyph project in 2014, describing solarpunk as "ingenuity, generativity, independence, and community"; the original Hieroglyph page was not fetched)
- Jakob Nielsen, "10 Usability Heuristics for User Interface Design" (Nielsen Norman Group), 1994, reviewed 2024 — https://www.nngroup.com/articles/ten-usability-heuristics/ (page read)
- Web Sustainability Guidelines (Sustainable Web Design, Mightybytes and Wholegrain Digital) — https://sustainablewebdesign.org/ (page read; specific techniques in UX Patterns are unverified synthesis)
- W3C, "Web Content Accessibility Guidelines (WCAG) 2.2", 12 December 2024 — https://www.w3.org/TR/WCAG22/ (3.3.7 and 2.5.8 text read)
- Low authority lead: Aesthetics Wiki and fan blogs; palette values above are design recommendations, not sourced facts.

---

## 🔗 Integration with Other Skills

- For conformance discipline, see [web-accessibility-wcag](../../../engineering/practices/web-accessibility-wcag/SKILL.md).
- Neighbors: [ui-style-organic-biophilic](../ui-style-organic-biophilic/SKILL.md), [ui-style-lunarpunk](../ui-style-lunarpunk/SKILL.md), [ui-style-art-nouveau-arts-crafts](../ui-style-art-nouveau-arts-crafts/SKILL.md), [ui-style-aurora-mesh-gradient](../ui-style-aurora-mesh-gradient/SKILL.md), [ui-style-cyberpunk](../ui-style-cyberpunk/SKILL.md) (the genre it inverts), [ui-style-biopunk](../ui-style-biopunk/SKILL.md).
