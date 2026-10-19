# 0008. Canonical UI Styles Expansion (82 Pure Styles), Decoupling and Showcase Integration

Date: 2026-10-17

## Status

accepted

## Context

Coacus maintains a comprehensive domain of user interface design styles in `knowledge/skills/domains/design/ui-style-*`. Over successive iterations, two architectural issues emerged:
1. **Taxonomic Ambiguity & Cross-Contamination:** Seven legacy directories grouped two distinct aesthetic traditions into hybrid composites (`vaporwave-synthwave`, `art-nouveau-arts-crafts`, `weirdcore-dreamcore`, `dungeon-synth-dark-fantasy`, `constructivism-propaganda`, `risograph-zine`, `retro-computing-pixel`). This compromised stylistic purity, obscured historical lineage, and diluted actionable guidance for generative agents.
2. **Visual Distortion & Style Drifting (AI Slop):** Certain styles experienced severe drift from their authentic historical foundations. Most notably, `ui-style-atompunk` degenerated into 1950s candy-pastel soda fountain tropes instead of Cold War nuclear futurism (Raygun Gothic, vacuum tubes, CRT phosphor displays, brushed naval steel, analog dials, and fallout shelter telemetry). Furthermore, major digital design benchmarks were absent: `windows-xp` (Luna Blue 2001), `dracula` (the official specification by Zeno Rocha), and `nordic` (the Arctic Nord palette).
3. **Showcase Incoherence:** The partner visual showcase repository (`/home/daniel/Code/estilos-visuais`) lacked isolation: the top navigation menu reset the viewport to the first style upon clicking tabs due to legacy `href="#"` links, external CDN dependencies created network fragility, and animation effects lacked a deterministic teardown lifecycle.

## Decision

1. **Decouple Hybrid Styles into 14 Pure Standalone Skills:**
   All 7 composite styles are abolished and replaced by 14 distinct, authoritative canonical skills:
   - `vaporwave` & `synthwave`
   - `art-nouveau` & `arts-and-crafts`
   - `weirdcore` & `dreamcore`
   - `dungeon-synth` & `dark-fantasy`
   - `constructivism` & `agitprop-poster`
   - `risograph` & `zine-independent`
   - `retro-computing` & `pixel-art`
2. **Expand the Canonical Corpus to 82 Pure Styles:**
   Reconstruct `ui-style-atompunk` to authentic nuclear futurism and introduce `ui-style-windows-xp`, `ui-style-dracula`, and `ui-style-nordic`. The design domain expands from 72 to **82 canonical UI styles**.
3. **Standardize on the 14-Part Canonical Content Architecture:**
   Every UI style skill adopts the 14-part structure established by `ui-style-frutiger-aero`: Frontmatter, Title & Epigraph, When to Activate, Definition & Timeline, Visual DNA & Subgenre Taxonomy, Lighting Physics & Surfaces, Design Tokens, Typography Architecture, Interaction & Motion, four Concrete Component Specifications, WCAG 2.2 Accessibility, When to Use / Avoid, Sources, and Dialect Relations.
4. **Showcase Engineering Overhaul:**
   The `estilos-visuais` showcase is upgraded with:
   - Locally vendorized [Driver.js](https://driverjs.com/) (zero external CDN dependency) for tool onboarding and per-style interactive tours.
   - Semantic WAI-ARIA `role="tablist"` navigation presenting 4 distinct demonstrative views: `Painel` (Metrics), `Projetos` (Kanban Board), `Equipe` (Team Grid), and `Relatórios` (Dense Telemetry Table).
   - Modular FX engine with strict `mount(stage) -> cleanup()` lifecycle and immediate `prefers-reduced-motion` short-circuiting.
5. **Anti-AI Slop Mandate:**
   Enforce the Anti-AI Slop manifesto across all styles: prohibit generic floating pastel pills, sparkle emojis, ungrounded ambient drop shadows, and non-semantic borders. Enforce mathematical WCAG 2.2 Level AA/AAA contrast compliance.

## Consequences

- **Corpus & Catalog Precision:** The knowledge design domain expands to 144 skills (totaling 430 knowledge skills, 27 workflows, and 457 catalog entries). All D5 prose counts across living documentation are reconciled against `catalog/catalog.json` and `sources.lock.json`.
- **Zero Cross-Contamination:** Agents selecting UI styles receive uncompromised historical DNA, accurate design tokens, and production-ready HTML/CSS components.
- **Showcase Synchronization:** The partner showcase reflects the exact 82 styles with deep-linking (`#<slug>/<view>`), verified responsive behavior, and robust visual verification.

## Alternatives Considered

- *Retaining composite dual styles with internal subsections:* Rejected because agents frequently conflated tokens and aesthetic rules when generating code from a single dual-named skill.
- *External CDN loading for Driver.js:* Rejected to maintain strict offline local operation and security integrity.
