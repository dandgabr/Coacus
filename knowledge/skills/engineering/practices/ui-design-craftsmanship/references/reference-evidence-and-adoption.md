# Reference Evidence and Adoption

Use when interpreting screenshots, URLs, recordings or a visual reference before changing a surface. This is an original Coacus synthesis, not an imported design system.

## Observe before adopting

Record the source, capture date, viewport or owner-container dimensions, theme, interaction state and capture method. Separate:

- **Observed:** sampled pixels, inspected computed values or behavior exercised in the source.
- **Inferred:** a probable grid, font category or implementation technique, with the evidence supporting it.
- **Unknown:** unobserved breakpoints, keyboard behavior, exact fonts, animation curves or implementation technology.

A screenshot cannot establish hover behavior, a font identity or which rendering library produced an effect. A sampled composite pixel is not necessarily the original color token. Do not fill missing fields with invented precision. If a source is unavailable, report the gap and use an explicitly proposed decision.

For each meaningful transfer, record the observation, product reason, existing token/component, and decision: reuse, adapt or author. Preserve existing semantics rather than introducing a second token merely because a reference uses a different value. General tokens belong to [UI design](../../../../roles/ui-designer/SKILL.md); color roles belong to [color UI systems](../../../../domains/design/color-ui-systems/SKILL.md). `DESIGN.md` remains the visual authority; an optional JSON extraction is analysis evidence, not another design system.

Choose a prototype that answers the highest-impact unresolved question: a flow sketch for task structure, a style frame for composition, an interactive slice for behavior. Reuse the [UX research discipline](../../../../roles/ux-designer/SKILL.md); a local repair need not rediscover the product.

## Commercial and asset evidence

Maintain a compact project record for claims and source materials:

| Item | Evidence to retain |
|---|---|
| Claim or metric | Exact wording, source, date, measurement conditions, limits and intended audience |
| Testimonial | Authentic source and permission; never invent customers or results |
| Font, image, audio or other asset | Source, rights holder or license, permitted use and attribution obligations |
| Synthetic illustration | Its illustrative purpose and disclosure where confusion with a real person, product or endorsement is likely |

Public access to an asset does not grant reuse rights. A synthetic decorative character is different from a fictitious endorser. Leave unsupported claims out or label a demonstrative example accurately. Route legal interpretation to [GRC compliance](../../../../security/grc/security-grc-compliance/SKILL.md).

## Sources and boundaries

Reviewed 2026-10-27. These references inform the synthesis; they do not prescribe Coacus policy.

- [Design DNA](https://github.com/zanwei/design-dna): structured reference analysis; retain unknowns rather than requiring every field to be guessed.
- [Garden Skills](https://github.com/ConardLi/garden-skills), [Elaya design skills](https://github.com/elayadesign/ai-design-skills), [Meng To skills](https://github.com/MengTo/Skills): reference study, purposeful structure and original application; no bulk adoption of their operational rules.
- [DTCG format](https://www.designtokens.org/tr/2025.10/format/): typed values and aliases; a Community Group specification, not a W3C Standard. Resolve the applicable edition before implementing a converter.
- [GOV.UK prototyping](https://www.gov.uk/service-manual/design/making-prototypes): match prototype fidelity to the learning question.
- [FTC review guidance](https://www.ftc.gov/business-guidance/resources/consumer-reviews-testimonials-rule-questions-answers), also readable through the [official search host](https://search.ftc.gov/business-guidance/resources/consumer-reviews-testimonials-rule-questions-answers): US-specific distinctions around false testimonials and stock imagery; not a global prohibition on synthetic illustrations. During this review the primary URL returned HTTP errors; the official alternate supplied the readable FAQ, but direct retrieval there was also intermittent.

- [Genjutsu](https://github.com/AThevon/genjutsu): explicit interaction intent; timing and interruption remain with the existing motion owner.
- [Emil Kowalski skills](https://github.com/emilkowalski/skills) and [Jakub Krehel skills](https://github.com/jakubkrehel/skills): animation critique and change-scoped interface review; use the existing rendered-verification owner rather than copying another audit framework.
