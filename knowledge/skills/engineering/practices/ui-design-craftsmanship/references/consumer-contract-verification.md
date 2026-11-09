# Consumer Contract Verification

Use when a component-library update or shared style change may break existing markup. This is a consuming-project verification procedure, not an automatic Coacus runtime validator.

## Establish inputs and scope

Record the baseline and working revisions, selected consumer markup, generated CSS or authoritative component API, and each exception's reason and owner. Resolve dynamic class construction, plugin styles and conditional build inputs before declaring a class unknown.

For illustration, `.card` may be recognized in a selected library, while `tabler-imaginary-card` is absent. These names illustrate outcomes, not a CSS parser or universal class inventory.

Require distinct outcomes:
- A genuinely unknown class fails the selected consumer contract.
- An exception that still suppresses a documented valid finding remains necessary.
- An exception that suppresses nothing in the complete relevant consumer scope is stale and fails exception maintenance.

A class absent from one sampled page does not prove an exception obsolete across the application. Evaluate the exception's owning scope. An unresolved dynamic family needs investigation, not a blanket allowance or a false unknown-class result.

## Validate the comparison oracle first

Run the fixture's assertions against the pinned baseline before interpreting the working result.

| Baseline | Working | Interpretation |
| --- | --- | --- |
| Fails | Any result | Invalid baseline or fixture; stop the regression comparison and investigate |
| Passes | Fails | Candidate working regression; inspect the discriminating evidence |
| Passes | Passes | Compatible for the selected assertions and consumers |
| Passes | Intentionally different | Require an explicitly reviewed contract/fixture update and rerun both relevant checks |

If both revisions fail because a fixture references a nonexistent component class, the fixture cannot establish a newly introduced regression. Do not fix the fixture by weakening an assertion merely to obtain green output.

Source/API checks establish contract availability. Rendered geometry, visibility, keyboard behavior and focus require [rendered verification](rendered-interface-verification.md). Record the environments and selected cases; passing samples do not establish compatibility for every consumer.

Sources reviewed 2026-10-28:
- [Upstream stale-exception check](https://github.com/tabler/tabler/blob/7ec9589ba63da56be273a12d9da9b9dfce59f5ee/.build/check-markup-classes.ts#L97-L103).
- [Upstream baseline-first comparison](https://github.com/tabler/tabler/blob/7ec9589ba63da56be273a12d9da9b9dfce59f5ee/.build/check-compat-fixture.ts#L152-L165).

The procedures above are original Coacus synthesis; upstream scripts are not installed or executed by this reference.
