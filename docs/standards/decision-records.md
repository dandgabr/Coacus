# Decision Records

**Status:** normative
**Scope:** architectural and technical decisions that bind the repository.

## Rule

A durable decision that changes how components fit together is recorded as an
Architecture Decision Record (ADR) under `docs/decisions/`, in MADR 3.0 format,
and committed with the change it governs.

- File name: `docs/decisions/NNNN-<kebab-title>.md`, zero-padded, sequential.
- The record carries, at minimum: title, status
  (`proposed | accepted | superseded`), context, decision, consequences, and the
  alternatives considered.
- A decision is not "made" until its ADR is accepted. A later decision that
  reverses an accepted one supersedes it (status `superseded`, link to the new
  record) — the old record is never deleted.
- Ephemeral reasoning stays out of this directory; working notes live under
  `docs/temp/` (plan-artifacts).

## Rationale

The repository already ships a MADR template
(`templates/domains/architecture_si/adr.template.md`) and records phase history
in `docs/roadmap.md`, but it had no home for per-decision rationale. Without one,
the reasoning behind a structural choice is lost and the same debate repeats. One
committed record per decision makes the choice reviewable and reversible.

## Enforcement

- `engine/validators/completeness.py` requires this standard to be present.
- The ADR index is the directory listing; new records are plain content, not
  generated output.
