# Agnostic Interface Skills Update — Delivery Review

Date: 2026-10-19. Baseline: `8ab8e28`. Initial candidate: `a0bcded`; corrected source: `e3e8e32`. Authorization: execute the approved plan and open a PR for human review. No merge, production publication or user-profile installation is part of this delivery.

## Scope and decisions

The [coverage record](interface-skills-2026-10-19.json) enumerates 82 visual packages and 21 shared packages, 24 transferred lessons and 18 evaluation cases. Independent baseline package curation read all 82 visual packages (83 files) and the 21 shared packages. It proposed 75 individual visual updates and seven justified no-change decisions. Source curation is not rendered conformance.

The seven unchanged visual packages are Glitch, Grain/Noise, Indie Web Revival, Isometric, Neo-Brutalism, Sandalpunk and Terminal/TUI. Their existing style-specific protections already addressed the relevant lessons. Shared procedures remain with their owners rather than being copied into every style.

The update separates complete painted surfaces and semantic state roles from appearance labels. It preserves chosen patterns and historical identities; it does not impose a beige light palette, remove intentional black, ban blue controls, require new layouts or force motion into every alternative. A Workbench-inspired light desktop is explicitly a separate period GUI adaptation, with primary documentation and proposed rather than falsely sampled historical colors.

## Ten-task implementation trace

| Task | Delivered result |
| --- | --- |
| T1 Evidence and inventory | Frozen source inventory, requirement disposition and traceable lesson mapping; historical project results distinguished from new evaluation. |
| T2 Normative contracts | Style identity, consumer integration, functional semantics and contextual taste separated; current inventory replaces fixed showcase counts. |
| T3 Surface/state systems | Owner references for inherited backgrounds, effective text fill, alpha layers, patterns, native/custom controls and state distinctions. |
| T4 Interface state | Reversible localization, hidden-panel semantics, asynchronous ownership, contextual help and preference cancellation. |
| T5 Motion/narratives | Viewport/content ownership, stacking, resource teardown, available height, continuous/scrubbed/scene modes and complete static access. |
| T6 Testing | Rendered output oracles, capture-condition fidelity, controlled mutants, inventory/stage fixtures and bounded temporary storage. |
| T7 Review/delivery | Revision-bound evidence, persistent authorization, served asset graphs and explicit PR/install/publish boundaries. |
| T8 Visual corpus | 75 individually reviewed deltas, concrete contradictory recipe corrections, seven reasoned no-change decisions; conditional Frutiger depth extracted. |
| T9 Authoring/transfer | Lean authoring owner, blind fixed-rubric comparisons, legitimate counterexamples, passing-baseline worked example and 18 reusable scenarios. |
| T10 Integration | Provenance refresh, regenerated discovery/bootstrap artifacts, repository gates, isolated two-adapter installation checks and independent review. |

## Verification and its limits

- Baseline suite: 511 tests passed. Final local suite: **518 tests passed**. Four new helper tests were observed failing before correction and passing afterward; three review-record tests check historical integrity, not agent behavior or immutable future source bytes.
- `coacus.py validate`, `check` and `completeness`: passed; generated output has no drift. `coacus_eval.py validate`: passed. The pinned secrets runner reported no leaks. The existing unrelated oversized subagent-workflow warning remains a warning, not a newly introduced source error.
- [Blind comparison](interface-skills-2026-10-19/forward-comparison.md): old and `a0bcded` candidate agents each passed **18/18 reasoning cases**. No observed reasoning regression; **no demonstrated behavioral improvement**. One sample per condition, no no-guidance control, no repeated trials and no product execution. Later source corrections received bounded review rather than silently inheriting this result.
- [Standalone fixture results](interface-skills-2026-10-19/render-fixture-results.json): 24 combinations of four viewports, three container types and two appearances; six controlled defects detected. Reduced-motion path exercised. Computed contrast over solid backing is not exhaustive painted sampling. This is not a runtime matrix of the 82 styles or a corpus mutation score.
- [Targeted recipe results](interface-skills-2026-10-19/style-recipe-results.json): 20 opaque ink/fill pairs from actual component CSS, including corrected Art Deco hover, Calm mode pairs and Frutiger label backing. These checks do not certify full pages, gradient extrema, focus, other engines or assistive technology.
- [Isolated installation verification](interface-skills-2026-10-19/isolated-install-results.json): Codex and Claude Code each verified 103 selected skills, two agents and one hook file, with no missing or drifted files. Explicit temporary config roots and copy mode preserved user profiles. This is installation-content evidence, not live behavioral evaluation across both harnesses.
- Delivery-time SHA256 comparison: all **191** listed source bindings agreed with the corrected source. Historical record tests intentionally do not freeze the mutable corpus forever.

## Independent review and corrections

The [initial domain review](interface-skills-2026-10-19/final-domain-review.md) rejected `a0bcded` for seven groups of actual source contradictions; the [initial QA review](interface-skills-2026-10-19/final-qa-review.md) rejected final delivery while evidence finalization was pending. Those reports are preserved rather than rewritten as approvals.

Corrections in `e3e8e32` repair Art Deco hover ink/fill, Clay boundary guarantees, Calm keyboard/touch discovery, binary focus rings, Collage/Card universals, Frutiger tab label protection and translucent claims, and the motion interruption comparison. QA also prompted correction of a stale polluter-helper description. The [domain addendum](interface-skills-2026-10-19/final-domain-recheck.md) and [QA addendum](interface-skills-2026-10-19/final-qa-recheck.md) both accept the bounded corrections at `e3e8e32`, naming their limited scope. The original rejection reports remain historical evidence.

## Language, references and provenance

Canonical additions and the migrated execution plan/retrospective are English. Residual Portuguese in Dracula guidance, mutation examples/formula and the DevOps diagram was translated. Current update filenames and local references were reconciled; original historical project records were preserved. A targeted check found no remaining Portuguese instruction matches across the 103 reviewed packages and no broken changed-file local Markdown links.

Conditional DevOps examples moved into named references; inherited platform/version samples are explicitly not represented as currently verified pins. Frutiger component/subgenre extraction preserves bibliography routing. The obsolete unused Node/Graphviz helper was removed, along with its active provenance target; its upstream history remains in Git. The portable worked example retains upstream provenance with the renamed/adapted target. No new framework runtime dependency was introduced.

## Decisions and remaining limits

An isolated Coacus worktree preserved unrelated edits in the original checkout; the task-native worktree tool was attached to another repository. Scratch task headings were normalized for the plan helper. Framework automation remains Python stdlib; the HTML/CSS fixture is an example, and local browser probes are execution evidence rather than framework dependencies. Governed independent agents evaluated and reviewed; the primary implementer owned canonical edits.

No exhaustive browser/assistive-technology certification, hardware render-cost measurement or live two-harness reliability claim is made. CI provides the remote operating-system checks at the PR revision. The reviewable PR is the requested end state; merge and activation remain separate decisions.
