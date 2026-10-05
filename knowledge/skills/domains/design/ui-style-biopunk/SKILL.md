---
name: "ui-style-biopunk"
description: "Provides the biopunk UI and UX style (1988-present): synthetic-biology science fiction and DIY-bio culture as specimen-lab visuals, lab-notebook information architecture, protocol and data-entry flows, provenance cues and ethical microcopy, covering palette, type, components and accessibility. Use when designing biotech, citizen-science, open-lab or health-data interfaces."
---

# UI Style: Biopunk

The genre in which biotechnology, not cyberware, is the site of power and resistance: engineered DNA, bio-hackers, megacorporations and black clinics. Translated to UI as specimen-lab aesthetics with flesh-and-membrane texture. Synthesized from the sources below; see Sources.

---

## 🧭 When to Activate

- Designing components, patterns and flows (sample tracking, protocol steps, data entry, sequence views) for biotech, genomics, synthetic-biology, health-data or DIYbio community products.
- Speculative-fiction, game, film or editorial experiences about genetic engineering.
- Open-science and citizen-lab projects that adopt the biopunk manifesto's ethos of access and literacy.

---

## 🕰️ Definition and Timeline

- Coinage: per Wikipedia, Czech writer and biologist Eva Hauserova first used "biopunk" in 1988 as a response to cyberpunk in post-communist Eastern Europe; her English fanzine description (December 1990) had limited reach and became widely available online only in 2018.
- Canon named in the sources: Paul Di Filippo's *Ribofunk* collection (his term "ribofunk"); precursors Wells's *The Island of Doctor Moreau*, Greg Bear's *Blood Music*, Cordwainer Smith. Signature trope: the "black clinic".
- "Punk" meaning: bio-hackers and individuals against governments or corporations misusing biotech. A real-world strand: Meredith Patterson's "A Biopunk Manifesto" (UCLA Outlaw Biology Symposium, January 2010), modeled on Eric Hughes's cypherpunk manifesto, claims freedom of inquiry and scientific literacy as rights; see also the DIYbio community.
- Versus [ui-style-cyberpunk](../ui-style-cyberpunk/SKILL.md): same dystopian friction, but the substrate is wet and organic, not neon and chrome. Versus [ui-style-organic-biophilic](../ui-style-organic-biophilic/SKILL.md): biophilic soothes with nature; biopunk exposes and unsettles with engineered life. Versus [ui-style-solarpunk](../ui-style-solarpunk/SKILL.md): optimism versus risk-aware tension.

---

## 🎨 Visual DNA

- **Color:** petri-dish and chlorophyll greens (`#7CFF6B`, `#2BB673`), bile yellow (`#C7D63B`), flesh and magenta (`#E0457B`), dark sterile slate (`#0F1A17`), cold lab white (`#EEF5F1`); sparse UV or fluorescent accents mimicking GFP.
- **Type:** clinical mono or grotesque for labels (IBM Plex Mono, Space Mono, Inter) paired with an unsettling organic display face; nucleotide strings (A, C, G, T), plate IDs and lot numbers as texture.
- **Texture and form:** translucent membranes, cell and hex lattices, DNA helices, microscopy vignettes, gel-electrophoresis band patterns, veins and branching, blobby metaball shapes (SVG `feTurbulence` plus threshold filters).
- **Layout:** specimen sheets and lab notebooks: ruled grids, callout lines, scale bars, annotated figures; asymmetry created by overlapping organic masses over a strict data grid.
- **Iconography:** biohazard-adjacent hazard marks (decorative only), pipettes, vials, plasmids, hands with grafted growth.

---

## 🖱️ Interaction and Motion

- Living motion: slow pulsing (2-4s) on glow elements, cell-division splits, membrane wobble via animated displacement, helix rotation on scroll.
- Data states as lab outcomes: "culturing..." loaders, bands migrating in a gel for progress.
- Keep microinteractions precise and clinical; the unease comes from imagery, not laggy UI.

---

## 🧩 UX Patterns

- **IA and navigation:** a lab-notebook model (Projects, Samples, Protocols, Results, Lab log); entities are first-class with stable IDs and breadcrumbs. Metaphor gives way to convention for global nav, search, account, export and settings; scientific users expect standard table, filter and sort behavior (Nielsen heuristics 4 and 7).
- **Flows:** onboarding as a first protocol run with sample data; data entry in short steps with units, validation and defaults (heuristic 5), never re-asking known values (WCAG 3.3.7); destructive actions (discard sample, delete dataset) need undo or a confirmation naming the object (heuristic 3).
- **Search and settings:** search by ID, tag, organism or sequence fragment with saved filters; settings cover units, data sharing scope and audit-log visibility.
- **Voice:** precise, plain, non-sensational ("Sample 14 failed QC: low yield. Retry or flag."); explain jargon on first use; biosafety notes appear inline where risk arises.
- **States:** empty = an instruction ("No samples yet. Log your first."); loading = "culturing" or progress with real elapsed or estimated time, never fake precision (heuristic 1); error = cause, impact on data, next step (heuristic 9); success = what was recorded and where, with timestamp.
- **Trust and provenance:** show source, version, who edited and when for every value; mark inferred versus measured data; honest uncertainty beats polished certainty. Sci-fi visuals must not imply clinical validity.
- **Cognitive load:** dense data needs chunking, sticky headers and plain-language summaries; disgust imagery stays optional and out of task paths.
- **Checks:** task success for logging a sample, finding a result and exporting data at or above 90 percent; data-entry error rate and time on task versus baseline; SUS; comprehension of provenance labels (unverified synthesis targets).

---

## 🛠️ Implementation Notes

```css
:root { --slate: #0F1A17; --lab: #EEF5F1; --gfp: #7CFF6B; --flesh: #E0457B; --bile: #C7D63B; }
body { background: var(--slate); color: var(--lab); font-family: "IBM Plex Mono", ui-monospace, monospace; }
.specimen { border: 1px solid rgb(124 255 107 / .6); position: relative; }
.specimen::before { content: "LOT 07 / ACGT-4412"; position: absolute; top: -.7em; left: 1rem;
  background: var(--slate); padding: 0 .5rem; font-size: .75rem; letter-spacing: .1em; }
.cell { border-radius: 58% 42% 55% 45% / 48% 56% 44% 52%;
  background: radial-gradient(circle at 35% 30%, rgb(124 255 107 / .55), rgb(43 182 115 / .15) 70%);
  animation: pulse 3.2s ease-in-out infinite; }
@keyframes pulse { 50% { transform: scale(1.04); } }
@media (prefers-reduced-motion: reduce) { .cell { animation: none; } }
```

```html
<svg width="0" height="0" aria-hidden="true"><filter id="goo">
  <feGaussianBlur in="SourceGraphic" stdDeviation="8"/>
  <feColorMatrix values="1 0 0 0 0  0 1 0 0 0  0 0 1 0 0  0 0 0 18 -7"/></filter></svg>
```

- Apply `filter: url(#goo)` to a container of circles for metaball membranes; test performance on mid-range phones.
- Show real scientific content (sequence viewers, protocols, provenance) rather than only helix clipart.

---

## ♿ Accessibility

- Acid green on dark slate is high contrast; green or magenta on white fails 1.4.3. Test every pair, and avoid saturated green on magenta (vibration and color-blind confusion; 1.4.1: add shape or text cues).
- Texture and microscopy backgrounds behind text need a solid or scrim layer (1.4.3, 1.4.11); keep nucleotide-string decoration `aria-hidden`.
- Pulsing and morphing: honor `prefers-reduced-motion`; no flashing above 3 per second (2.3.1); provide pause for ambient loops (2.2.2). Gooey SVG filters can blur text, so never filter text containers.
- Gel and sequence visualizations need text alternatives or data tables (1.1.1, 1.3.1); targets at least 24px (2.5.8).
- Imagery of bodies, wounds or surgery can distress some users: content warning and non-autoplay.

---

## ✅ When to Use / ❌ When to Avoid

- **Use:** biotech and open-science branding, game and film microsites, editorial on genetic ethics, DIYbio communities, lab-notebook tools.
- **Caution:** health and patient-facing products (trust and calm matter); medical claims must not ride on sci-fi visuals.
- **Avoid:** clinical decision support, pharmacy, anything where eugenic-coded or "disgust" imagery could stigmatize people with disabilities or genetic conditions.

---

## ⚠️ Pitfalls

- Gross-out for its own sake; DNA-helix cliche on every landing page; filter-heavy pages that jank.
- Ethics blind spot: the genre exists to question biotech power; a style that glamorizes unregulated experimentation misreads it. Any real-world DIY protocol content needs biosafety framing.
- Fan-wiki claims about origin are low-authority; prefer the primary manifesto and Wikipedia-cited sources.

---

## 📚 Sources

- "Biopunk" (Wikipedia), accessed 2026 — https://en.wikipedia.org/wiki/Biopunk
- "Cyberpunk derivatives" (Wikipedia), accessed 2026 — https://en.wikipedia.org/wiki/Cyberpunk_derivatives
- Meredith Patterson, "A Biopunk Manifesto", UCLA Outlaw Biology Symposium, January 29-30, 2010, as listed on Hackteria Wiki, "Manifestos" — https://hackteria.org/wiki/Manifestos (page read; quoted line: "Scientific literacy empowers everyone who possesses it to be active contributors to their own health care, the quality of their food, water, and air.")
- "Meredith L. Patterson" (Wikipedia), accessed 2026-10-05 — https://en.wikipedia.org/wiki/Meredith_L._Patterson (described as "a leading figure in the biopunk movement"; the page gives no manifesto details)
- "DIYbio (organization)" (Wikipedia), accessed 2026-10-05 — https://en.wikipedia.org/wiki/DIYbio_(organization) (founded 2008 by Jason Bobe and Mackenzie Cowell as a network for citizen scientists and amateur biologists)
- Jakob Nielsen, "10 Usability Heuristics for User Interface Design" (Nielsen Norman Group), 1994, reviewed 2024 — https://www.nngroup.com/articles/ten-usability-heuristics/ (page read)
- W3C, "Web Content Accessibility Guidelines (WCAG) 2.2", 12 December 2024 — https://www.w3.org/TR/WCAG22/ (3.3.7 text read)
- Palette and filter values are design recommendations, not sourced facts; UX patterns beyond the cited heuristics and criteria are unverified synthesis.

---

## 🔗 Integration with Other Skills

- For conformance discipline, see [web-accessibility-wcag](../../../engineering/practices/web-accessibility-wcag/SKILL.md).
- Neighbors: [ui-style-cyberpunk](../ui-style-cyberpunk/SKILL.md), [ui-style-nanopunk](../ui-style-nanopunk/SKILL.md), [ui-style-organic-biophilic](../ui-style-organic-biophilic/SKILL.md), [ui-style-solarpunk](../ui-style-solarpunk/SKILL.md), [ui-style-glitch](../ui-style-glitch/SKILL.md), [ui-style-3d-immersive-webgl](../ui-style-3d-immersive-webgl/SKILL.md), [ui-style-grain-noise-texture](../ui-style-grain-noise-texture/SKILL.md).
