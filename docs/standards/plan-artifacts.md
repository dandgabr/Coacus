# Plan Artifacts

**Status:** normative
**Scope:** the ephemeral process artifacts written by the imported process
workflows — design specs, implementation plans and execution scratch.

## Rule

Process artifacts are working documents, not repository content. They live under
`docs/temp/`, which is ignored by version control.

- Design specs: `docs/temp/specs/YYYY-MM-DD-<topic>-design.md`.
- Implementation plans: `docs/temp/plans/YYYY-MM-DD-<feature-name>.md`.
- Execution scratch: anywhere else under `docs/temp/`.

- The imported process workflows (`superpowers-brainstorming`,
  `superpowers-writing-plans`, `superpowers-executing-plans` and the rest) write
  there. The upstream `docs/superpowers/` default they shipped with is
  superseded; no process artifact is written under the `docs/` root or a
  `docs/superpowers/` directory.
- A durable conclusion is promoted out of `docs/temp/` into a committed document
  or a standard; the working copy stays where it is.
- `docs/temp/` is OUTSIDE the documentation count surface
  (`engine/validators/docs.py` reconciles only the living docs), and outside the
  prose, link and count checks — its contents are not validated.

## Rationale

The process workflows emit many intermediate documents: a design spec before
building, an implementation plan per feature, and per-run scratch. Tracking them
would fill `docs/` with one-off material that drifts out of date and dilutes the
committed documentation. One ignored `docs/temp/` gives every workflow a stable,
conventional location and keeps the committed tree to durable content — the same
"disk is the truth, but only for what ships" split the repository already applies
to generated output.

## Enforcement

- `.gitignore` ignores `docs/temp/`.
- `engine/validators/completeness.py` requires this standard to be present.
- `methodology/workflows/using-coacus/references/coacus-process-conventions.md`
  states the convention to the process workflows, and each adapted workflow
  carries it in its attribution footer.
