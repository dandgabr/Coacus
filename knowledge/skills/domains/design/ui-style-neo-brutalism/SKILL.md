---
name: "ui-style-neo-brutalism"
description: "Provides the neo-brutalism / neubrutalism UI style (2021-present): thick black borders, hard offset shadows, saturated flat color blocks and deliberate rawness, covering the token system, press-down interaction metaphor, WCAG failure pairs, component libraries and the Gumroad/Figma trend cycle. Use when designing blunt, high-contrast marketing surfaces or building neubrutalist component systems."
---

# UI Style: Neo-Brutalism (Neubrutalism)

Graphic bluntness as a UI system: high contrast, blocky layouts, thick borders and hard offset shadows rejecting polished neutrality. Crystallized 2021–2023 (Gumroad's 2021 rebrand; Michał Malewicz's March 2022 essay); formally documented by Nielsen Norman Group (April 2025). Synthesized from verified research; see Sources.

---

## 🧭 When to Activate

- Designing creator, SaaS or web3 marketing surfaces that must stand out from gradient-flat sameness.
- Building neubrutalist component systems (tokens, shadows, focus states).
- Assessing the style's accessibility debt before adopting it.

---

## 🕰️ Definition and Timeline

- Lineage: Hans Asplund's "nybrutalism" (1950), Banham's New Brutalism (1955), web brutalism (~2014–2016, Pascal Deville's brutalistwebsites.com).
- Wave: Gumroad rebrand 2021 → Dribbble tag clusters spring 2022 → Figma UI kits 2023 → marketplace categories 2024. Figma's own 2024 rebrand dropped the outlines — the trend-cycle cautionary case. NN/g documented it April 2025.
- Its own historians stress "no single originator" — a style crystallized by platforms (Figma Community files + Tailwind JIT), not invented by one author.

---

## 🎨 Visual DNA

- **Type:** display Syne 800 / Bebas Neue / Archivo Black; headings Space Grotesk; body deliberately calm (Inter, DM Sans); mono Space Mono / JetBrains Mono.
- **Color:** categorical, not ambient — black/off-white base (e.g. `#FFFDF5`) + 1–3 saturated flats (`#FFD23F`, `#FF6B6B`, `#74B9FF`); **no gradients**.
- **Shapes:** square corners (radius 0), 2–4px black borders, exposed grids; occasional Win98-style retro intrusions and pixel art.
- **Depth:** hard offset shadows, zero blur — "printed layers that don't fully align"; tiered shadow scale (3/5/8/12px) encodes hierarchy.
- **Texture:** sticker/emoji accents, rotated elements.

---

## 🖱️ Interaction and Motion

- Physical press metaphor: hover lifts (`translate -2px`, shadow grows), active presses into the shadow direction with the shadow removed; 0.1–0.15s transitions — mechanical feedback, not eased physics.

---

## 🛠️ Implementation Notes

```css
:root {
  --border: 3px solid #000;
  --shadow: 5px 5px 0 0 #000;
  --shadow-lg: 8px 8px 0 0 #000;
  --radius: 0;
}
.btn { border: var(--border); box-shadow: var(--shadow); }
.btn:hover { transform: translate(-2px, -2px); box-shadow: 7px 7px 0 0 #000; }
.btn:active { transform: translate(2px, 2px); box-shadow: none; }
.btn:focus-visible { outline: 3px solid #74B9FF; outline-offset: 3px; }
```

- Tailwind idiom: `border border-black rounded-none shadow-[5px_5px_0_0_#000]`.
- Layout rule: "broken but not random" — disrupt macro composition, keep micro mechanically aligned.
- neobrutalism.dev provides a shadcn/ui-based component library.

---

## ♿ Accessibility

- Yellow-on-white and pink-on-orange fail WCAG AA 4.5:1 — loud palettes do not guarantee compliance; test every pair.
- Color-only state violates 1.4.1; thick borders imply larger targets than real hit areas (2.5.8, 24px minimum); decorative shadows can swallow focus rings (2.4.7); border-as-semantics serves 1.4.11 non-text contrast (3:1).
- Strengths: strong edge definition aids scanning; borders improve control discoverability versus ultra-flat UI.

---

## ✅ When to Use / ❌ When to Avoid

- **Use:** creator portfolios, SaaS landing pages, web3; expressive marketing surface with a calm product flow.
- **Caution:** e-commerce (brand pages yes, checkout no), editorial mastheads, dashboards (token accents only).
- **Avoid:** banking, healthcare, government — trust plus mandatory accessibility.

---

## ⚠️ Pitfalls

- Hierarchy collapse when every component is equally loud; fast fatigue (Figma's exit); kit-driven homogenization; contested originality because the style is platform-reproducible.

---

## 📚 Sources

- Hayat Sheikh, "Neobrutalism: Definition and Best Practices", Nielsen Norman Group, Apr 11, 2025 — https://www.nngroup.com/articles/neobrutalism/
- "Neubrutalism — The Definitive Guide" — https://neubrutalism.com/
- Michał Malewicz, "Neubrutalism is taking over the web", UX Collective, Mar 2022 — https://uxdesign.cc/neubrutalism-is-taking-over-the-web-e9d09e0fe441
- Sahil Lavingia, "Introducing the new Gumroad", 2021 — https://sahil.gumroad.com/p/introducing-the-new-gumroad
- Brutalist Websites, Pascal Deville, 2014 — https://brutalistwebsites.com/
- neobrutalism.dev component library — https://www.neobrutalism.dev/
- Reyner Banham, "The New Brutalism", Architectural Review, Dec 1955 — https://www.architectural-review.com/essays/the-new-brutalism-by-reyner-banham

---

## 🔗 Integration with Other Skills

- For conformance discipline, see [web-accessibility-wcag](../../../engineering/practices/web-accessibility-wcag/SKILL.md).
- Sibling styles: [ui-style-web-brutalism](../ui-style-web-brutalism/SKILL.md), [ui-style-acid-anti-design](../ui-style-acid-anti-design/SKILL.md), [ui-style-maximalism](../ui-style-maximalism/SKILL.md).
