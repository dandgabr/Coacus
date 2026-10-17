# Product and Design Truth

**Status:** normative
**Scope:** separation of durable business/product context from visual design systems and surface modes across projects and workflows.

## Rule

AI coding agents and human contributors MUST strictly separate durable product facts from visual direction and UI styling:

1. **`PRODUCT.md` (Durable Product Truth)**:
   Lives at the project root and captures business facts, operating reality and constraints that remain true regardless of styling changes:
   - **Audience & Users**: Who the product serves and what problems they bring.
   - **Product Purpose**: The core problem solved and measurable value delivered.
   - **Operating Context & Deployment**: Runtime environments, platforms (web, mobile, CLI, desktop) and ecosystem boundaries.
   - **Hard Constraints**: Regulatory compliance, supported browsers/devices, technical non-negotiables.
   - **Brand Voice & Personality**: Authoritative tone principles (e.g. decisive, editorial, empathetic) without surface styling rules.
   - **Evidence on Hand**: Documented facts, measured benchmarks and committed artifacts. Claims without evidence MUST NOT be fabricated.

2. **`DESIGN.md` (Living Design System & Visual Authority)**:
   Lives at the project root and documents the visual authority and design tokens of the project:
   - **Design Tokens**: Concrete semantic variables (preferring `oklch()` color ramps, surface contrasts and intentional ink colors).
   - **Typography Ratios**: Explicit type scales (e.g. Major Third 1.25 or Perfect Fourth 1.333), line-height inversely proportional to font size, font pairings.
   - **Surface & Elevation Craft**: Multi-layered discrete shadows, 1px semi-transparent borders, tactile depth recipes.
   - **Spatial System**: Base grid units (4px/8px), structural breathing room (minimum 24px-32px between sections).

3. **Surface & Visitor Modes**:
   When designing or modifying a UI surface, agents MUST classify the surface into one of four intentional visitor modes rather than applying a generic template:
   - **`Persuade`**: The visitor evaluates, decides and acts (landing pages, marketing, conversion, pricing). Design carries the brand proposition with punchy visual hierarchy and purposeful imagery.
   - **`Operate`**: The visitor completes a task or workflow (applications, dashboards, data tables, editors, admin panels, settings). Scannability, task ergonomics, information density and predictable keyboard/pointer interactions outrank decoration.
   - **`Read`**: The visitor absorbs information (documentation, knowledge bases, long-form articles, changelogs). Generous line length (45-75 characters), comfortable measure, structural headings and zero visual friction.
   - **`Experience`**: The visitor explores creative work (portfolios, interactive galleries, simulations). The interface recedes, allowing the artifact itself to command the viewport.

## Anti-AI Slop Mandate

UI generation MUST actively avoid generic LLM design clichés:
- **No Icon Tiles**: Never place an icon inside a rounded pastel square above every heading or feature card.
- **No Isolated Italic Serif Words**: Never interlace single italic serif words inside modern sans-serif headlines.
- **No Hero Eyebrow Pills**: Avoid formulaic pill badges with sparkle icons at the top of landing heroes.
- **No Gray Ink on Chromatic Fills**: Never pair low-contrast muted gray text (`text-gray-400`/`text-slate-400`) over saturated chromatic backgrounds (`bg-blue-600`, `bg-red-500`).
- **No Nested Card Syndrome**: Never nest cards inside cards inside cards; rely on typography and whitespace before adding structural boxes.
- **No Cartoonish Spring Easing**: Never use bounce or elastic curves for serious interface transitions.
- **No Ungrounded Ambient Drops**: Never apply uniform, blurred 0-distance black drop shadows to cards without a defined physical lighting model.
- **No Style Cross-Contamination**: Never conflate distinct aesthetic traditions into hybrid compromises (e.g. converting Atompunk into pastel soda fountain kitsch, or Neo-Brutalism into raw unstyled HTML). All canonical UI styles must adhere strictly to [`ui-style-architecture.md`](ui-style-architecture.md).

## Rationale

LLMs systematically converge toward homogeneous, generic visual patterns ("AI slop") because they are trained on vast volumes of undifferentiated SaaS templates. Furthermore, models frequently confuse product requirements (why something exists) with visual preferences (which colors to use). By enforcing the separation of `PRODUCT.md` and `DESIGN.md` and requiring explicit surface mode classification, Coacus ensures that interfaces are designed with deliberate human craft, high utility and uncompromising accessibility.

## Enforcement

- Canonical skill `ui-design-craftsmanship` instructs agents on these rules and provides actionable design directives.
- Agent `design-qa-specialist` audits pull requests and components against this standard.
- Python linter `scripts/coacus_design_lint.py` deterministically scans frontend code for prohibited anti-patterns.
- `engine/validators/docs.py` reconciles living documentation counts.
