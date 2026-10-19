# Frozen-source behavioral responses

This is a proposed product review of the 18 independent fixtures. No fixture was changed, browser run, network request made, deployment performed, or product test executed. Verification below describes checks to perform, not results. Source versions are frozen historical inputs, not claims about current standards or libraries.

## Sources consulted

All skill paths below are relative to `docs/temp/reports/skill-learning-review/baseline-8ab8e28/`:

- `knowledge/skills/roles/frontend-developer/SKILL.md`
- `knowledge/skills/roles/frontend-developer/references/design-engineering-craft-guide.md`
- `knowledge/skills/domains/design/color-contrast-accessibility/SKILL.md`
- `knowledge/skills/domains/design/color-ui-systems/SKILL.md`
- `knowledge/skills/domains/design/ui-style-grain-noise-texture/SKILL.md`
- `knowledge/skills/domains/design/ui-style-scrollytelling/SKILL.md`
- `knowledge/skills/engineering/practices/ui-design-craftsmanship/SKILL.md`
- `knowledge/skills/engineering/practices/ui-design-craftsmanship/references/rendered-interface-verification.md`
- `knowledge/skills/roles/qa-engineer/SKILL.md`
- `knowledge/skills/roles/devops-engineer/SKILL.md`
- `methodology/workflows/superpowers-verification-before-completion/SKILL.md`
- `methodology/workflows/using-coacus/SKILL.md`

Also read the worktree `AGENTS.md` and `docs/temp/reports/skill-learning-review/blind-probes.json`. Source enumeration was confined to the frozen tree. The first combined source output was truncated; color, texture, scrollytelling, craftsmanship, QA and DevOps were subsequently read in smaller complete outputs. No current canonical catalog was consulted because this exercise restricts evidence to frozen sources and supplied fixtures.

## S01

**Diagnosis:** `background-color` paints below the existing opaque `linear-gradient(#111,#222)`, so paper ink is still drawn on a dark image. Changing ink alone would obscure the actual cause.

**Smallest action:** Replace only the theme-inappropriate image: `[data-theme=paper] .card{background-color:var(--surface);background-image:none}` if paper grain already lives on a separate pseudo-element. Preserve that grain layer. If grain is one layer of the card background, explicitly retain it: `background-image:var(--paper-grain)` instead of `none`. The fixture does not specify where grain lives, so inspect that before choosing the declaration; do not reset every background longhand unnecessarily.

**Verification:** In paper theme inspect the computed background layers and rendered surface, verify that the dark gradient is gone and subtle grain remains, and measure ink against the lightest/darkest composite grain regions. Repeat night/paper switching and relevant control states.

**Limits:** Exact grain CSS and a contrast result cannot be established from this snippet.

## S02

**Diagnosis:** Glyph paint is controlled by `-webkit-text-fill-color:#161616`; the bright computed `color` is insufficient evidence. The dark fill is close to `#111`.

**Smallest action:** `h1{-webkit-text-fill-color:currentColor}` or remove the overriding declaration at its source. The current bright title color can then paint the glyphs.

**Verification:** Check computed `webkitTextFillColor` as well as `color`, opacity, visibility, clipping and any background-clip text. Measure the effective fill against the actual background and inspect a rendered title in night theme. For this solid background, the expected effective pair after repair is `#eee`/`#111`; before repair the checker must reject the dark fill. Add a negative case restoring `#161616` while leaving `color:#eee`.

**Limits:** A style-only checker still cannot prove glyphs are visible when overlays or clipping exist; rendered inspection is needed.

## S03

**Diagnosis:** Native controls lack the approved accent binding; the custom switch has almost indistinguishable tracks and no additional state cue.

**Smallest action:** Bind `input[type=range],input[type=checkbox]{accent-color:var(--accent)}` with approved blue semantic values per theme. Set the appropriate `color-scheme` per theme. Use a labeled native checkbox for the switch where feasible, or a labeled button with `role="switch"` and synchronized `aria-checked`. Move its thumb between ends and expose visible On/Off text, with an accessible stable label. Bind the on track to the approved accent and choose a contrasting thumb/boundary rather than merely shifting gray by one step.

**Verification:** Test both themes, checked/unchecked, range endpoints and keyboard steps, hover/focus/active/disabled states, label activation, Space toggling and announced state. Check meaningful boundaries/thumb/checked mark against adjacent colors, text contrast and a visible unobscured focus ring. Confirm the browser actually renders the requested accent; inspect native controls visually because CSS tokens alone do not establish their rendered colors.

**Limits:** Blue shades and final surface colors are missing, so numeric contrast acceptance cannot be asserted. Native appearance varies by platform.

## S04

**Diagnosis:** A single dark foreground cannot remain readable across black and white squares. Averaging square luminance hides the failing black regions.

**Smallest action:** Preserve the checker textile outside text; give text a stable light backing, for example `.copy{color:#222;background:#faf8f0;padding:.25em .5em;box-decoration-break:clone}`. Use a block backing for paragraphs, or cloned inline backing for wrapping short phrases. Keep any texture beneath the text plate sufficiently faint and measurable.

**Verification:** Confirm the backing covers every glyph and wrapped line at narrow widths, larger text and altered spacing. Measure the effective foreground/background at the worst underlying point, including any transparency. Inspect real rendered text at both square colors and intersections; verify normal text reaches 4.5:1, or the applicable large-text criterion. Retain a visual comparison showing the surrounding textile.

**Limits:** A screenshot glance or average contrast does not establish readability throughout. A translucent plate needs compositing against both extremes before acceptance.

## S05

**Diagnosis:** Author `display:grid` can override the default hidden styling. The attribute may be true while the panel still renders and its inputs remain in keyboard navigation.

**Smallest action:** Add `.workspace .panel[hidden]{display:none}` and scope grid to `.workspace .panel:not([hidden])` if convenient. Maintain tab selection, `aria-selected`, `aria-controls`, tabpanel labeling and roving tab focus together. If changing panels while focus is inside the outgoing panel, move it to an appropriate active tab or panel entry before hiding.

**Verification:** For each tab, assert exactly its panel is rendered; hidden panels have no client rectangles and their inputs cannot receive sequential keyboard focus. Exercise arrow keys, Tab/Shift+Tab and programmatic tab changes; inspect the accessibility tree and focus destination.

**Limits:** Setting `aria-hidden` alone would not solve focusability or display. The complete tab implementation is absent.

## S06

**Diagnosis:** Missing keys inherit previously translated DOM text; only translating the active panel leaves hidden settings stale. Arabic also requires document language and direction changes.

**Smallest action:** Render every translatable property from immutable catalogs on each language change: `resolve(locale,key)=catalogs[locale]?.[key] ?? catalogs.en[key]`. Never derive fallback from current DOM text. Apply this resolver to all panels or render each panel from current locale when mounted. Include text nodes, placeholders, accessible names and titles; avoid overwriting rich child markup through parent `textContent`. Set `document.documentElement.lang=locale` and `dir=locale==='ar'?'rtl':'ltr'`, with explicit support for any other RTL locales in the real catalog.

**Verification:** Cycle English→Spanish→Arabic→English while opening settings before and after each transition. Spanish placeholder must be Spanish; absent Arabic placeholder must be English, never Spanish. English restores all source strings, including hidden settings. Verify RTL layout, labels and logical spacing; test missing keys with visible diagnostic logging in development.

**Limits:** English fallback may intentionally produce mixed-language content; native speakers must validate translations and layout. Missing English keys require a defined diagnostic fallback, not silent stale text.

## S07

**Diagnosis:** A stale A completion can overwrite B and mount obsolete effects. Immediate storage mutation contradicts Cancel semantics.

**Smallest action:** Give each selection a monotonically increasing request token and abort the previous fetch. Load and validate the candidate stylesheet without activating it; after every asynchronous boundary compare its token to the current token. Only the latest successful request may atomically install the stylesheet, dispose the previous effect and mount the new effect. If stale, discard its resources. Keep the last working theme on failure; only the current request may clear loading or set an error. Expose retry and avoid an unhandled rejection. On unmount abort requests and invalidate tokens.

Maintain `committedPreferences` and a separate dialog `draft`. Inputs update the draft and optional reversible preview only. Accept commits a successfully prepared selection and persists once; Cancel, Escape and close discard the draft, invalidate pending preview loads and restore committed appearance. Handle storage failure explicitly rather than reporting persistence succeeded.

**Verification:** Resolve B before A as in the fixture, including an A failure after B succeeds; B must remain active with exactly one mounted effect. Test latest request failure, retry, cancel during fetch, cancel after preview, reopening, accepted persistence and storage rejection.

**Limits:** Fetch abortion alone does not prevent already completed callbacks from committing; token checks are required. Effect setup failure also needs disposal of partial resources and rollback to the last working state.

## S08

**Diagnosis:** Reject acceptance: horizontal overflow equality says nothing about vertical clipping. At 480px, header/footer leave only 280px for a 600px panel; a 320px host is more constrained.

**Smallest action:** For the embedded workspace use a definite host-sized shell: `.workspace{height:100%;min-height:0;display:flex;flex-direction:column}.header,.footer{flex:none}.panel{flex:1;min-height:0;overflow:auto}`. Remove the panel minimum of 600px and ensure ancestors allow shrinking. If the shell itself can exceed host height (large text or chrome), allow outer scrolling or collapse chrome so every action remains reachable. For ordinary documents prefer content flow and document scrolling over a constrained shell.

**Verification:** At 1280×900, 1280×480 and an actual 320px-high host, compare all four bounds, scrollHeight/clientHeight, scroll ownership, visible focus and ability to reach every field and footer action by pointer and keyboard. Test zoom/text enlargement and narrow widths too.

**Limits:** Overflow inside a deliberately scrollable panel is acceptable; hidden overflow that makes content unreachable is not. The embedding height contract must be confirmed in the real host.

## S09

**Diagnosis:** Global wheel interception replaces native scrolling and turns trackpad momentum into uncontrolled scene jumps. Keyboard/touch paths cannot reliably reach hidden scenes or the long form; fixed viewport clipping cuts content.

**Smallest action:** Remove the global preventDefault handler and scene-per-wheel navigation. Let scenes use document flow, `min-height:100svh;height:auto;overflow:visible`, and give the form its natural height. Drive optional timed reveals from IntersectionObserver on real scenes while preserving native scrolling. Content should default to visible if enhancement fails. Provide chapter anchors; use sticky visual stages only where they cannot trap or cover the form. Reduced motion exposes sequential static content and removes timed spatial movement.

**Verification:** Traverse with wheel, momentum trackpad, touch, PageDown/Home/End, Tab/Shift+Tab and chapter anchors. Enter and submit the entire form, including validation errors, at short heights and enlarged text. Check reveals produce visible content, hash links reach targets and reduced-motion/no-script paths retain information.

**Limits:** Reveal duration and observer thresholds need real content testing. No scroll or device behavior was executed here.

## S10

**Diagnosis:** The transformed story is its own stacking context and fixed-position containing block; a z9999 child cannot escape above a root z100 header. The CRT only covers one viewport of a longer article. RAF and listener leaks persist after canvas removal.

**Smallest action:** Put viewport progress in an untransformed root overlay sibling at an intentional layer above the header, or below it with a measured inset, depending on intended hierarchy. Do not solve this by increasing the child's z-index. For a viewport CRT use a root `position:fixed;inset:0;pointer-events:none` layer. If it must cover article coordinates instead, use `position:absolute;inset:0` on the full article wrapper without `height:100vh`. Keep focus and dialogs unobscured.

Each mount returns idempotent cleanup that marks the loop disposed, cancels its latest RAF id, removes the exact resize callback, disconnects observers, frees graphics resources and removes the canvas. The RAF callback checks disposal before scheduling again.

**Verification:** Inspect stacking/containing contexts and overlays throughout all four screens. Repeatedly mount, switch themes and unmount; assert one active loop/listener while mounted and none afterward, no detached canvases and no callbacks after cleanup. Test reduced motion and input hit targets.

**Limits:** Desired CRT attachment and progress/header relationship are product decisions not specified in the fixture.

## S11

**Diagnosis:** Insufficient evidence. Resizing height from 480 to 2600 changes `100vh`, media queries, layout and potentially observer behavior. It no longer tests the original short viewport.

**Smallest action:** Keep the viewport at 1200×480 throughout the run. Capture the initial viewport, scroll through the actual owning scroller, focus/activate the footer action and capture its reachable state. Use a full-page capture mode that does not resize layout, or stitch viewport captures while preserving dimensions. Measure `innerHeight` and relevant element rectangles before/after capture to detect harness changes.

**Verification:** Assert header, content and footer action reachability at the fixed original dimensions, with keyboard focus not clipped or obscured. Record viewport dimensions and scroll positions with screenshots. Treat a document-wide image as complementary evidence only.

**Limits:** Some capture mechanisms can affect sticky content or trigger lazy rendering; report the method and verify it did not change the target geometry.

## S12

**Diagnosis:** The test proves metadata, while the missing CSS variable can leave the bar with an invalid intended height. Its actual fallback depends on layout.

**Smallest action:** Set the rendering input, for example `style="--n:42"`, preserving the specified one-pixel scale. Add assertions after reveal/layout that the bar is visible, opacity is nonzero, rendered height is positive and approximately 42 CSS pixels within a justified subpixel tolerance. Verify its baseline/container and clipping so height alone cannot pass an invisible bar. Cover zero and negative values according to the chart contract and provide an accessible value label.

**Verification:** Keep the data assertion as a separate semantic check. Temporarily remove `--n` or force `.bar{height:0!important}` and demonstrate the geometry assertion fails; restore and require it to pass. Test reduced-motion rendering too.

**Limits:** A DOM emulator cannot establish layout dimensions; these assertions require a real rendering engine. No red/green execution occurred here.

## S13

**Diagnosis:** Candidate-only selection leaves the two existing variants uncovered and the count assertion can pass while identities drift.

**Smallest action:** Parameterize baseline smoke and critical interaction checks over all five current inventory entries. Compare unique inventory IDs to exercised IDs as sets, fail missing/duplicate coverage, and report approved versus candidate status separately. Apply deeper changed-feature checks to the three candidates while retaining regressions for approved variants. Use a matrix of variant, theme, locale, representative viewport, and critical state; prioritize high-risk combinations and explicitly list any sampled dimensions.

**Verification:** Every inventory entry must have a visible render, reachable main actions, relevant contrast/focus and short-height checks; unique effects get behavior/cleanup checks. Seed a failure in an approved variant and verify the suite rejects it. Add a new inventory ID temporarily and confirm missing coverage is detected.

**Limits:** Full Cartesian coverage may be excessive; risk-based sampling must remain explicit and must not exclude an entire current variant. Five is supplied by this fixture, not a measured repository count.

## S14

**Diagnosis:** The three intervals are 16.7ms; they describe callback cadence, not JavaScript processing duration or GPU execution. Four timestamps provide no evidence that all effects meet a budget.

**Smallest action:** Replace the report with: “Four RAF timestamps produced three approximately 16.7ms intervals in this sample. Processing cost and GPU time were not measured; hardware timing is unsupported. No per-effect GPU-budget conclusion is available.”

**Verification:** Collect a longer per-effect session with device, viewport, refresh context, warmup, active interactions and sample counts. Report interval distribution and missed-cadence observations separately. Measure callback CPU duration with start/end performance marks, labeling its scope; use an appropriate browser performance trace for rendering/compositor work and supported GPU timer queries for actual GPU time. Record unsupported or disjoint samples as unavailable.

**Limits:** CPU callback duration excludes asynchronous GPU completion. RAF intervals alone cannot establish exact dropped-frame counts without a justified refresh baseline, and no hardware timing can be fabricated.

## S15

**Diagnosis:** Delivery is not verified. The supplied evidence positively shows mixed revisions: r2 HTML referencing r1 application and CSS bytes. HTTP 200 and a successful job establish availability, not intended content.

**Smallest action:** Trace the intended release manifest/digests through served HTML, JavaScript, CSS and dynamic imports at the exact target. Use content-addressed asset filenames or propagate a release version through the entire reference graph; configure HTML revalidation and immutable caching for hashed assets. Invalidate stale mutable assets only as required by the hosting strategy.

**Verification:** Compare response bytes/digests against the prepared r2 artifact for every referenced dependency, including nested CSS assets and lazy modules. Record final URLs, response cache headers and revision/digest evidence. Check normal cached delivery as well as a cold fetch and confirm visible r2 behavior in a subsequent runtime smoke test. Investigate CDN and service-worker caches if applicable.

**Limits:** A query on only HTML does not version downstream URLs, and one fresh edge response does not prove all cache populations are fresh. No remote requests are authorized or executed in this exercise.

## S16

**Diagnosis/disposition:** “Digest B differs from approved digest A. Evidence covers 6 of 18 states; the remaining 12 states have no observation. Two gradient checks were skipped; other required checks were not run. A universal pass and release readiness are unsubstantiated.” Do not assume the skipped checks map one-to-one onto unobserved states or that observed states passed unless their results say so.

**Smallest action:** Freeze B, document the difference from A and complete a state/check matrix with pass/fail/skipped/not-run and reasons. Verify B against every required acceptance criterion, including the skipped gradient worst points. Rerun checks affected by B even if they were previously performed on A. Present the exact B digest, changes and evidence for renewed artifact approval if approval was specifically bound to A.

**Verification:** Tie every result to digest, environment, state and fresh output. Recompute B before any authorized release to ensure it has not changed again. Unresolved skips remain explicit release gaps.

**Limits:** An approved plan may still guide implementation, but it does not establish approval of a different prepared artifact. Six observations cannot support eighteen-state coverage.

## S17

**Diagnosis/action:** The user has authorized the prepared artifact to the confirmed preview target after checks; the stated conditions are satisfied. The operational next step is to deploy that exact checked artifact to `preview.example.test/gallery`, then verify remote content digests and smoke behavior. No additional confirmation is needed for that same scope.

**Verification:** Bind deployment inputs to the checked digest and exact host/path; after deployment compare served HTML and its asset graph to that digest and record the resulting preview URL and checks.

**Limits:** Authorization does not cover `production.example.test`, other paths, replacement artifacts or unrelated account settings. Account access is not permission for other hosted sites. This response is a proposed action only, as the fixture explicitly forbids an actual deploy.

## S18

**Diagnosis:** The installed old name is a stale installed artifact according to the supplied catalog/provenance facts; its continued presence does not make it canonical authority.

**Smallest action:** Select the source for `ui-style-new-name` referenced by the current canonical catalog and confirm the provenance rename from `ui-style-old-name`. In real follow-up, edit that single canonical source and reconcile canonical references to the new name, retaining a documented alias/deprecation only if compatibility policy calls for it. Regenerate discovery/rendered artifacts via the lifecycle rather than editing generated output. Report the installed old-name copy as drift to reconcile in a separately authorized installation operation.

**Verification:** Check the exact catalog entry, source path and provenance rename, then validate and generate after a proposed edit and check references for dangling old IDs. A read-only installer verification can later distinguish stale installs from canonical absence.

**Limits:** This exercise supplies those catalog facts and prohibits current-source inspection, installation and modification. I therefore make no claim to have independently confirmed the actual current catalog, installed copy or rename; no path is guessed from the old name.

## Summary

The proposals preserve approved visual identity while repairing actual paint, state, layout and lifecycle behavior. Acceptance requires evidence from the rendered result, complete declared coverage, measured metric scope and the exact delivered artifact. All 18 fixtures received a diagnosis, smallest proposed intervention, verification procedure and limits; no product execution or external change is claimed.
