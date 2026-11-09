# Independent final domain/source review

Candidate: `a0bcded`; baseline: `8ab8e28`. Verdict: **REJECT** pending correction of the source contradictions below. This verdict binds to the committed candidate, not concurrent working-tree fixes.

## Findings, ordered by severity

1. **Major — newly introduced identical hover ink and fill.** `knowledge/skills/domains/design/ui-style-art-deco/SKILL.md:233` uses `background-color: var(--deco-title-ink)` and the next line sets `color: #0D0E12`. The light appearance sets that title token to exactly `#0D0E12` at line 121. Thus the supplied light-theme hover recipe has identical foreground/background. This follows directly from the source; no browser measurement is claimed. Restore gold-core fill plus dark ink or introduce an explicit tested hover pair. The appended paragraph at line 279 does not repair the recipe.

2. **Major — acknowledged contrast guarantee remains authoritative.** `knowledge/skills/domains/design/ui-style-claymorphism/SKILL.md:207` still says outer drop shadows provide at least 3:1 luminance differential against light floors. The actual recipe uses blurred low-alpha colored shadows (lines 177–187); no substrate-independent ratio follows from that. The newly appended line 241 says to replace automatic guarantees, but the guarantee itself is unchanged. Replace the original assertion with verification of the actual essential boundary and states; strengthen a contour when needed. This was specifically identified in `style-audit.json`.

3. **Major — pointer-exclusive control discovery remains operative.** `knowledge/skills/domains/design/ui-style-calm-quiet-ui/SKILL.md:131` still says secondary controls fade from 0.2 to 1 opacity **only** when the pointer lingers. The appended verification note does not remove that exclusivity. Amend the original interaction recipe with focus-within/focus-visible discovery and a stable touch/no-hover path. Preserve quiet presentation without requiring pointer dwell to discover controls. This is a source contract contradiction, not a measured keyboard failure.

4. **Major — focus recipe still prescribes white over an intentionally binary appearance.** `knowledge/skills/domains/design/ui-style-brutalist-monochrome/SKILL.md:206` mandates a white offset outline while the skill supports black-on-white usage. The appended dual-ring suggestion leaves that original rule intact. Replace the original prescription with an appearance-aware ring or explicit dual ring; identify the surrounding surface. This remains the precise issue recorded by `style-audit.json`.

5. **Moderate — Frutiger tab recipe does not implement the extracted label protection.** `knowledge/skills/domains/design/ui-style-frutiger-aero/references/gloss-components.md:221` retains white active-tab ink on a gradient starting at `--aero-sky-300` (`#78cafc` in the parent at line 109). The new `.aero-label` opaque backing at reference line 106 is demonstrated only for a button at line 5; tabs have no markup instruction applying it. The parent at line 249 now explicitly requires protected button/tab labels, so users copying the active-tab recipe receive the old unprotected pairing. Demonstrate tab markup with the protected label, or supply a dedicated stable tab label backing/ink. Do not infer rendered compliance from the extraction. The extracted component reference also preserves the absolute sanctuary ratio claim in its line-180 comment and parent line 197; qualify numeric claims by actual composite/assumptions rather than treating translucent paint as opaque.

6. **Moderate — one earlier shared finding is only partially reconciled.** `knowledge/skills/domains/design/ui-motion-interaction/SKILL.md:38` still categorically describes cubic-bezier interruption as snapping/resetting and springs as naturally velocity-preserving; line 39 assigns mechanical versus organic quality by technique. The revised introduction at lines 15 and 31–33 correctly makes choice contextual, but the comparison still overstates behavior determined by implementation. Replace cells with conditional properties (retargeting/velocity behavior depends on implementation) and explain where the example presets apply. This is the remaining portion of the first shared-audit finding.

7. **Moderate — remaining original aesthetic universal contradicts its appended correction.** `knowledge/skills/domains/design/ui-style-collage-scrapbook/SKILL.md:35` says **every** container is tilted. The new note scopes tilt away from dense/long functional fragments. Amend the original Visual DNA bullet to scope tilt to selected decorative/readable fragments; do not leave competing operative instructions. Similarly, `ui-style-card-based-ui/SKILL.md:128` still unconditionally limits titles to two lines; integrate the new discoverable-full-title condition at that prescription. These are narrower source inconsistencies, not proof every implementation truncates content.

## Earlier shared-audit findings: individual disposition

The list below follows the order of the 22 findings actually present in `shared-audit.json`. “Resolved” means source reconciliation of that stated finding, not executed behavioral validation.

| # | Earlier finding | Candidate disposition and current evidence |
| --- | --- | --- |
| 1 | Motion introduction/default springs | **Partial**: purpose-based introduction/hover corrected; categorical comparison remains at `ui-motion-interaction/SKILL.md:38–39` (finding 6). |
| 2 | Transform/opacity-only; global near-zero reset | **Resolved**: same skill accessibility section replaces both with measured rendering cost and explicit complete static result. |
| 3 | Craft animate requires <200ms springs | **Resolved**: `ui-design-craftsmanship/SKILL.md:45` now chooses timing by task and complete reduced-motion states. |
| 4 | Craft mandates white ink on saturated fill | **Resolved**: same file line 85 requires verified pairs allowing dark/light ink. |
| 5 | Craft inaccurate directive count | **Resolved**: same file line 27 removes the fixed count. |
| 6 | Mutation reference Portuguese | **Resolved**: `framework-testing/references/mutation-and-fault-based-testing.md:31,93` translates comment and hash label. |
| 7 | DevOps monolithic body/Portuguese diagram | **Resolved for stated concern**: `roles/devops-engineer/SKILL.md:15` routes conditional platform material to focused references; former diagram no longer lives in the body. Full operational reference correctness was not independently re-audited here. |
| 8 | Frontend mandatory wrapper | **Resolved**: `roles/frontend-developer/references/design-engineering-craft-guide.md:9` explicitly permits direct accessible reuse. |
| 9 | Grain fixed viewport/arbitrary layer | **Resolved**: same reference lines 63–80 declares ownership and uses positioned local isolated owner; fixed viewport/high numeric recipe removed. |
| 10 | UI/UX universal palette/type/motion handoff | **Resolved for stated prescriptions**: `roles/ui-ux-designer/SKILL.md:30–31,121` supplies purpose-based type/palette and duration/spring/static handoff. Other historical art-direction defaults were not exhaustively assessed. |
| 11 | Executing plans repeated authorization | **Resolved**: `superpowers-executing-plans/SKILL.md:48` preserves existing authorization. |
| 12 | Single fix pass/no re-review ceiling | **Resolved**: same file line 289 requires invalidated gates and renewed independent review when assumptions change. |
| 13 | Mutation replay versus read-only review | **Resolved**: `superpowers-requesting-code-review/SKILL.md:146` and template execution boundary require authorized disposable copy. |
| 14 | Debugging credential-bearing diagnostic | **Resolved in source**: `superpowers-systematic-debugging/SKILL.md:96` replaces the block with metadata/presence/redaction guidance. No real credentials inspected. |
| 15 | Polluter false-clean/runner handling/nonportable ls | **Resolved by source inspection**: `find_polluter.py:29–52` distinguishes preexisting state, no matches, unavailable/failed runner and clean executed cases; uses pathlib metadata. Helper not executed by this reviewer. |
| 16 | Verification fresh-in-message conflict | **Resolved**: `superpowers-verification-before-completion/SKILL.md:29,37` explicitly permits unaffected revision-bound evidence. |
| 17 | Plan confirmation despite authorization | **Resolved**: `superpowers-writing-plans/SKILL.md:195` proceeds within already authorized scope. |
| 18 | Pressure reference forces failure/compliance | **Resolved**: rewritten `testing-skills-with-subagents.md` preserves passing baseline, fixed rubric, authorized boundary, outcome and unknowns. |
| 19 | Node/Graphviz helper | **Resolved by removal** in candidate diff; no claim of replacement executable capability. |
| 20 | Lost instruction-form selection | **Resolved substantially**: `superpowers-writing-skills/references/behavior-validation.md:31` restores positive procedure, structural slot, observable completion predicate and counterexample/context control, linked from body. |
| 21 | Vendor-specific worked compliance test | **Resolved**: removed historical example replaced by `examples/guidance-comparison.md`, including a passing baseline and already-correct control with illustrative outcomes clearly labelled. |
| 22 | Implicit all-target install/merge | **Resolved**: `using-coacus/references/coacus-process-conventions.md:122,135` scopes merge and installation to existing authorization and selected targets. |

## Source ownership and positive changes

The painted-contrast and surface-state procedures have clear owners and reciprocal routing. They cover actual text fill, opaque-layer stopping, pseudo layers, small worst regions missed by medians, capture changes to currentColor, native/custom states, unsupported measurements and preserving texture. These are substantive reusable procedures rather than copied style checklists. Motion owner references distinguish viewport/container/content/scene coverage, lifecycle resources, callback cadence versus render cost, and continuous/reveal/scrub/step narratives.

The normative architecture now separates showcase API/variant counts from reusable style guidance, preserves functional/accessibility precedence and contextual material language. Workbench adaptation clearly labels proposed accessible colors rather than sampled historical colors, with a primary-reference anchor and explicit dialect limits. Frutiger extraction retains six subgenre descriptions and bibliography routing, and materially improves the button example with a higher unfiltered label layer; the tab gap above prevents treating that extraction as complete recipe reconciliation.

## Coverage and limitations

Read AGENTS, catalog index, using-coacus, the approved plan, retrospective, relevant architecture/product-truth standards, craft/accessibility/clean-code skill guidance; inspected shared-audit findings, style-audit structure/inventory (82 records measured from that JSON), targeted original style paragraphs and candidate diffs; read the painted-contrast, surface-state, motion coverage/narrative, Frutiger component/subgenre, Workbench, frontend craft, authoring validation/pressure/example material, and targeted workflow diffs.

Large aggregate outputs were truncated. This review does **not** claim a second full-file/full-reference independent reading of all 82 style packages or every changed DevOps reference. The prior full-package style audit is a coverage input, not delegated proof that each correction is implemented. The contradictions above were verified against actual sources; generic appended notes were not counted as repaired recipes. Non-domain code and generated artifacts were considered only insofar as needed to resolve the listed shared source findings. No network, browser, installation, deployment, credential access, subagent dispatch, mutation replay or behavioral experiment was performed. No rendered WCAG certification, hardware-performance claim or measured agent improvement follows from this review.

Concurrent working-tree changes were visible (including an Art Deco fix). They are intentionally excluded from the candidate verdict until reviewed at an identified correction revision.
