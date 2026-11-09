# Candidate behavioral responses

Candidate revision observed: `a0bcded3913dbc32e2fa00cd8f7273bb1652ce28`.

This is independent reasoning from the supplied briefs and current source guidance. All repairs and verification procedures below are proposals. No product tests, browser rendering, performance recording, deployment, installation or fixture mutations were executed. Cases are independent; no case authorizes actual publication or product edits.

## S01

**Diagnosis.** `background-color` does not replace the opaque `linear-gradient` background image. The paper ink consequently lands on dark paint even though the surface token is light. The supplied snippet does not identify where the desired paper texture resides.

**Smallest action.** Override the unwanted image for the paper card while retaining the actual texture layer. If texture is a separate pseudo-element, use `[data-theme=paper] .card { background-image:none; background-color:var(--surface); }`. If texture shares the image stack, replace only the dark gradient with the existing paper texture recipe, for example `background:var(--paper-texture) var(--surface)` after defining `--paper-texture` from that existing asset. Do not erase the paper layer merely to clear the gradient.

**Verification and limits.** Inspect the winning background image, color, pseudo-elements and ink in a paper card; inspect an unmodified rendering to establish that texture remains and the text is readable. Measure effective contrast including texture extremes, then switch away and back to catch cascade leakage. Tokens alone cannot establish the painted result, and the exact preservation selector depends on the real texture owner.

## S02

**Diagnosis.** The visible glyph fill is `#161616`; computed `color:#eee` is not its painted foreground. Against `#111`, the fill explains the absent-looking title.

**Smallest action.** Remove the stale fill declaration if unnecessary, or set `h1 {-webkit-text-fill-color:currentColor}` in the appropriate theme scope. Retain intentional text effects elsewhere.

**Verification and limits.** Check text fill as well as color, opacity, ancestors and actual background; wait for font readiness and inspect title pixels. The contrast check must use the effective fill and composed background. Use this overriding-fill example as a failing control and a light-fill title as a passing control. A computed fill check still cannot resolve arbitrary masks, images or blending without rendering evidence.

## S03

**Diagnosis.** Native controls lack the approved accent binding; the two almost equal switch tracks offer no understandable visible state. Accessible semantics and behavior also need checking rather than inferring them from appearance.

**Smallest action.** Bind native controls with `input[type=range],input[type=checkbox]{accent-color:var(--action)}` and bind `--action` to the approved blue in each theme. Set the intended `color-scheme` for each appearance. Prefer a labeled native checkbox for the switch, or a labeled button with `role="switch"`, synchronized `aria-checked`, and Space activation. Add a thumb position change and visible On/Off feedback; e.g. `.switch[aria-checked=true]::before{transform:translateX(var(--thumb-travel))}`. Choose track/thumb/focus roles with measured contrast rather than asserting any blue is sufficient.

**Verification and limits.** In both themes inspect checked/unchecked, range endpoints and keyboard increments, hover-free settled on/off, focus and disabled states. Assert actual state/output changes for pointer and keyboard; accessible name remains clear while state updates. Check visible boundary/indicator/focus contrast and forced-color behavior. Native painting varies by platform; declaration presence alone does not verify it.

## S04

**Diagnosis.** Dark words encounter a locally dark background; a global average or median contrast hides those failures. The checker pattern itself is part of the intended textile language.

**Smallest action.** Add an opaque local reading plate behind the words, with compatible textile color, sufficient padding and no clipping of wrapped lines. For example `.textile-copy{background:var(--reading-surface);color:var(--reading-ink);padding:.25em .4em;box-decoration-break:clone}` where the plate is inline and wraps. Preserve the checker elsewhere. Relocation to a reliably readable region is another small option when composition allows it.

**Verification and limits.** Examine actual glyph regions over both extremes and transitions, in all supported states/sizes. An opaque plate permits a deterministic foreground/plate contrast calculation once its paint is confirmed; translucent plates require compositing and worst-region checks. Preserve suspicious samples instead of averaging them away. A background-only capture must preserve layout and currentColor-driven surfaces. One attractive screenshot does not establish every region or motion frame.

## S05

**Diagnosis.** The author `display:grid` rule can override the browser's hidden styling, exposing the inactive panel and focusable inputs.

**Smallest action.** Make the layout selector conditional: `.workspace .panel:not([hidden]){display:grid}` and enforce `.workspace .panel[hidden]{display:none}` if other panel declarations require a guard. Keep one active panel and matching tab selected state; use proper tab/panel associations and roving tab focus. On a change that hides the focused panel, place focus appropriately on the selected tab rather than leaving it inside hidden content.

**Verification and limits.** Toggle each tab and assert exactly the intended panel is displayed; inactive inputs have no layout box, are excluded from keyboard traversal and accessibility navigation, and cannot retain active effects. Seed the original grid override to ensure the visibility test detects it. Attribute assertions alone are insufficient. Native tab keyboard details must follow the chosen tab activation model.

## S06

**Diagnosis.** Missing keys retain previous-language strings and inactive panels remain stale. The Arabic placeholder can remain Spanish, and returning to English does not necessarily restore source values.

**Smallest action.** Retain stable keys and a complete English source catalog for every localized text/attribute. Resolve each key afresh on each language change: `catalog[locale]?.[key] ?? sourceEnglish[key]`; never use current DOM text as fallback. Apply to all mounted panels, including inactive settings, and apply the current locale when lazy panels mount. Cover placeholders, accessible names, titles and injected strings. Update `document.documentElement.lang` and `dir` (`rtl` for Arabic, `ltr` for English/Spanish), with directional isolation for codes where needed. Keep stored choice distinct from auto-negotiated resolution.

**Verification and limits.** Cycle English→Spanish→Arabic→English with settings hidden, then open it at each step; assert Arabic missing placeholders become English, never Spanish, and English fully restores text and attributes. Repeat with settings active, reload, missing keys, long strings and unavailable storage. Assert route, selection/data and sensible focus survive. Catalog key equality cannot prove reversible DOM behavior; wording quality requires language review.

## S07

**Diagnosis.** A's late completion overwrites B and can mount an obsolete effect. Immediate persistence violates Cancel's transactional contract. Failures can leave selection, style and storage inconsistent.

**Smallest action.** Assign a generation/request token to every theme selection and invalidate it on newer selection, close or teardown. Abort the prior fetch where possible, but also check ownership after every await and immediately before stylesheet installation, state commit and effect mount. Stage the stylesheet until ready; atomically activate only the current result and dispose superseded resources. At t90 A is discarded; B stays active. Track `requested`, `loading`, `applied` and error separately. Keep last valid appearance on essential style load failure, clear pending status and show useful retry feedback. Optional decorative failure may keep a complete static theme.

Open preferences with `draft=copy(committed)`. Inputs update draft and, if product requires, reversible preview only. Accept commits ready values and persists once; Cancel, Escape and close invalidate pending work, discard draft and restore committed preview/focus. A storage failure needs an honest unsaved/session-only outcome rather than false persistence success.

**Verification and limits.** Use controlled promises for the exact A/B order and assert B paint/effect/storage after both resolve. Include the positive path proving the latest successful theme really applies, plus latest-request failure, stale rejection, close during loading, optional effect failure, reopen after Cancel and Accept/reload. Assert cleanup counts as well as output. Abort alone is not proof against already completed work.

## S08

**Diagnosis.** Horizontal overflow checks miss vertical inaccessibility. At 480px, 200px of header/footer leave only 280px; the 600px panel cannot fit under hidden overflow. A 320px embedded owner leaves still less usable space.

**Smallest action.** Reject acceptance at these supported dimensions. Remove the fixed minimum and give a deliberate vertical scroll owner: `.shell{block-size:100%;min-block-size:0;display:grid;grid-template-rows:auto minmax(0,1fr) auto}.panel{min-block-size:0;overflow:auto}` when the host provides a definite height. For a normal document use natural page growth/scrolling rather than forcing a bounded shell. Reduce or wrap chrome if it leaves no usable content area.

**Verification and limits.** At actual 1280×480 and a real 320px-high host, measure all four edges against the owner after chrome, then scroll and keyboard-focus the last action; confirm no obscured hit target or unreachable final field. Include zoom, narrow screens and content expansion. A scrollable control need not begin onscreen, but must become fully reachable. `scrollWidth===clientWidth` establishes no vertical acceptance.

## S09

**Diagnosis.** Global wheel prevention replaces natural reading with an uncontrolled event-driven deck. Trackpad momentum can jump scenes; keyboard/touch lack equivalent movement, and the long form is clipped. Editable controls can lose normal wheel/key behavior.

**Smallest action.** Remove global wheel interception and fixed clipping. Use normal document flow with scenes `min-block-size:100svh;block-size:auto`, adjusted for fixed chrome where relevant. Trigger timed reveals with intersection/visibility state while scroll stays native; never gate essential information on an elapsed animation. Keep the long form naturally scrollable. Reduced motion exposes all content immediately without forced displacement or timing.

**Verification and limits.** Exercise wheel, slow/fast trackpad momentum, touch, PageDown/Space/arrows, Tab, reverse navigation, nested scrolling and focus inside fields/ranges. Reach and submit the final ticket controls; test resize mid-reveal and reduced motion. Check actual reveal opacity/geometry and cleanup, not scene classes alone. Discrete stepping would require a separate explicit product requirement and local input design.

## S10

**Diagnosis.** Progress is confined to its transformed parent's z0 stacking context and cannot outrank the root header z100 through z9999. Transform can also make its fixed positioning relative to that parent. The CRT covers only one screen of four. RAF/listeners leak across mounts.

**Smallest action.** Put viewport-owned progress beside the header at the root with an intentional order (for example header100, progress110, dialogs above both), or remove the unnecessary parent stacking context if compatible with layout. Do not escalate the child z-index blindly. Declare CRT ownership: for full-article texture use a positioned article with an absolute `inset:0` decoration covering its actual content extent; for viewport CRT use a root fixed `inset:0` layer. Set `pointer-events:none` and appropriate decorative accessibility semantics.

Teardown must cancel the current RAF handle, prevent rescheduling, remove the exact resize callback, disconnect observers, release drawing resources and remove owned nodes/styles. Make it idempotent and safe after partial initialization; clean superseded async initialization too.

**Verification and limits.** Inspect the visible header/progress intersection at start/middle/end and after resize; verify full chosen coverage and underlying control access. Repeatedly mount/unmount, change views and interrupt initialization; assert no old callback/listener continues and new mounts work once. Check reduced-motion static output. Heap noise alone cannot prove no retention; numeric layers alone cannot prove visible ordering.

## S11

**Diagnosis.** The capture changed the measured interface. A `100vh` scene grows from 480px to 2600px and resize-dependent behavior may change; a reachable action there does not establish reachability in the original window.

**Smallest action.** Preserve 1200×480, record scene/control geometry first, wait for style/font/state readiness, and capture the actual viewport. Scroll through the unchanged viewport and show/assert that the footer action becomes visible and operable. A full-page method is acceptable only if it preserves relevant layout dimensions; otherwise label it supplementary and disclose the modification.

**Verification and limits.** Record original viewport and owning-container bounds, scroll position, action rectangle and overlap/hit-target checks. Include the unmodified bottom state and actual activation outcome. Restore any capture adaptations. A stitched image is still not evidence for every intermediate interaction state.

## S12

**Diagnosis.** The test verifies markers, while unresolved `--n` invalidates the height declaration. Depending on other CSS the bar can be auto/zero-height; no useful rendered value is established.

**Smallest action.** Bind the numeric value into the real property, e.g. `.bar` receives `style="--n:42"` after validating the data, using the supplied 1px/unit contract. After readiness assert computed height and `getBoundingClientRect().height` are approximately 42px under that contract, width is positive, opacity/display/visibility permit painting, and the bar falls within its chart's visible region. Verify accessible value/label and value changes affect geometry; use the actual scale if the chart contract differs.

**Verification and limits.** Negative control: temporarily force `height:0!important` in a synthetic test instance and require the rendered-height assertion to fail while class/data assertions still pass; restore afterward. Also omit `--n` to test this original failure. A passing attribute or a nonzero box alone does not establish correct scale, unclipped paint or all data values. These mutations are proposed, not executed here.

## S13

**Diagnosis.** Candidate-only selection excludes the two approved variants from regression coverage; the fixed candidate count encodes an accidental inventory snapshot.

**Smallest action.** Derive cases from the current authoritative inventory, preserving status metadata. Assert unique IDs and that every inventory ID is represented by the common checks, including both approved and candidate variants. Keep status-specific requirements explicit rather than filtering approved entries out. Fixed counts are appropriate only for an intentionally frozen synthetic fixture.

**Verification and limits.** Build a matrix of variant × relevant appearance/state/view and responsive height/width, locale and motion axes. Exhaust common invariants across all variants; sample expensive combinations by documented risk and pair interactions, with known fragile cases mandatory. Record each axis as exhaustive/sampled/not run. Seed a defect in an approved synthetic variant and add an inventory entry to ensure checks neither omit it nor fail solely because count changed. Coverage of IDs is a bookkeeping gate, not proof of rendered readability or behavior.

## S14

**Diagnosis.** Differences of RAF timestamps describe callback cadence over three intervals, approximately 16.7ms. They do not measure frame processing cost, GPU execution or comprehensive effect performance.

**Smallest action.** Replace the claim with: “Four RAF timestamps yielded three approximately 16.7ms callback intervals in this sample. Hardware frame timing was unavailable. Render processing cost and GPU budget compliance were not measured.” Remove “all effects meet GPU budget.”

**Verification and limits.** Record target refresh budget, environment/rendering backend, effect/workload and baseline. Collect adequately long idle, scroll and interrupted workloads with supported main-thread work/long-task instrumentation, callback duration, frame observations and resource teardown measurements. Obtain hardware traces on an appropriate supported environment for hardware claims. Callback duration itself excludes work outside that callback and asynchronous GPU work; aggregate CPU metrics cannot stand in for GPU cost. Preserve unsupported as unknown.

## S15

**Diagnosis.** Delivery is not verified: r2 HTML is serving an r1 JavaScript→CSS dependency chain. HTTP200 and job success prove reachability/job completion, not revision consistency.

**Smallest action.** Inspect the configured preview delivery route and compare served response bytes/digests with the intended r2 manifest/package. Follow static and dynamic imports, styles, catalogs/registries and any service-worker caching involved. Repair version propagation across the graph using existing content hashes/manifest or consistent cache keys, rather than adding a version only to the HTML. Invalidate the relevant cache through the configured route where authorized.

**Verification and limits.** Re-fetch normal public-origin responses and verify the complete relevant graph against r2 digests, recording URLs, headers, revision and artifact identity; replay an important flow at that origin. A cache-busted diagnostic response alone cannot prove ordinary users get r2. Scope remediation/rollback to this release and do not affect unrelated sites. This brief authorizes an analysis, not actual deployment or cache mutation.

## S16

**Diagnosis/disposition.** “Approval refers to digest A. Current candidate is B and is not covered by that approval without a documented equivalence or renewed review. Six of 18 states were observed; their individual results must be recorded. Two gradient checks were skipped; remaining checks were not run. These are incomplete results and do not establish all-state success.” Do not infer the skipped-check relationship to those six states beyond supplied evidence.

**Smallest action.** Freeze/identify B, classify changes for impact, and rerun checks/review invalidated by those changes plus outstanding required checks. Reuse unaffected A evidence only with its revision, scope and concrete reason documented. Finish the remaining matrix and gradient verification, or report a verifier capability gap distinctly from a product failure. Seek renewed review/authorization only where required by the changed artifact and actual release authority.

**Verification and limits.** Record per-check revision, method, status (pass/fail/skipped/not run/unsupported), evidence path and coverage axes. Preserve the old report rather than rewriting it as B evidence. Source reasoning cannot supply the missing rendered observations; authorization with limitations would not convert unknown measurements into passes.

## S17

**Diagnosis/action.** The next operational step would be deployment of the checked, prepared artifact to `preview.example.test/gallery` through the already configured route, followed by served-asset and user-flow verification and a revision-bound report. No repeated confirmation is needed for that existing authorization. Do not actually deploy in this reasoning exercise.

**Scope and limits.** Authority covers that artifact and preview destination after checks; sharing the account grants no authority to change `production.example.test`, unrelated paths, DNS/provider configuration, install globally or merge code. Confirm the deploy configuration targets that path, preserve the prior preview rollback artifact and verify relevant production identity remains unchanged through read-only evidence. Material artifact/destination/scope changes require appropriate renewed authority; ordinary execution within scope does not.

## S18

**Diagnosis.** The installed old name is a derived/stale local copy, while the canonical catalog and provenance establish the new canonical identity. Installed presence alone does not make the old source authoritative.

**Smallest action.** Resolve the catalog's `ui-style-new-name` entry to its canonical `SKILL.md`, inspect that source and rename provenance, and use it for the requested canonical-guidance update. Reconcile references/aliases and documentation according to the recorded migration, preserving intentional compatibility. Classify the old installation as drift; any later authorized installation should regenerate/synchronize through the repository lifecycle rather than editing generated or installed copies directly.

**Verification and limits.** Validate canonical links/identity and provenance, regenerate outputs and run appropriate validation when actual edits are authorized, then separately verify installation drift if installation becomes part of scope. Do not silently delete the old installation or invent an alias policy. Here no installation, source update or generator run was performed.

## Consulted sources

Repository paths below refer to the observed candidate tree. The session-level Coacus routing skill was also read at `<installed-skill-root>/using-coacus/SKILL.md`; it supplied routing/session discipline, not product evidence. The initial catalog output was truncated, so no corpus totals or completeness claims are made from that output. An attempted read of `knowledge/skills/roles/qa-testing-specialist/SKILL.md` found no such file; testing guidance was resolved to `framework-testing` instead.

- `AGENTS.md`
- `catalog/INDEX.md` (routing scan)
- `docs/temp/reports/skill-learning-review/blind-probes.json` (case inputs)
- `knowledge/skills/roles/frontend-developer/SKILL.md`
- `knowledge/skills/roles/ui-ux-designer/SKILL.md`
- `knowledge/skills/domains/design/color-contrast-accessibility/SKILL.md`
- `knowledge/skills/domains/design/color-ui-systems/SKILL.md`
- `knowledge/skills/roles/devops-engineer/SKILL.md`
- `methodology/workflows/superpowers-executing-plans/SKILL.md` (workflow boundaries; no implementation plan executed)
- `methodology/workflows/superpowers-verification-before-completion/SKILL.md`
- `methodology/workflows/superpowers-verification-before-completion/references/interface-evidence.md`
- `knowledge/skills/engineering/practices/ui-design-craftsmanship/SKILL.md`
- `knowledge/skills/engineering/practices/ui-design-craftsmanship/references/rendered-interface-verification.md`
- `knowledge/skills/domains/design/color-ui-systems/references/theme-surface-states.md`
- `knowledge/skills/domains/design/color-contrast-accessibility/references/painted-contrast-audits.md`
- `knowledge/skills/roles/frontend-developer/references/runtime-localization.md`
- `knowledge/skills/roles/frontend-developer/references/interface-state-lifecycle.md`
- `knowledge/skills/domains/design/ui-motion-interaction/SKILL.md`
- `knowledge/skills/domains/design/ui-motion-interaction/references/effect-coverage-lifecycle.md`
- `knowledge/skills/domains/design/ui-motion-interaction/references/scroll-narrative-modes.md`
- `knowledge/skills/frameworks/framework-testing/SKILL.md`
- `knowledge/skills/frameworks/framework-testing/references/rendered-ui-oracles.md`
- `knowledge/skills/roles/devops-engineer/references/published-artifact-verification.md`

Publication normalization: the operator-specific installed skill root above is replaced with a placeholder; task answers and evaluation outcomes are unchanged.
