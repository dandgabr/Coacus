# Coacus process conventions

How Coacus adapts the imported Superpowers process workflows, and the local
conventions every process skill follows. Companion reference for the
`superpowers-*` workflow family.

## Artifact locations

Process artifacts are working documents. They live under `docs/temp/`, which is
ignored by version control:

- Design specs: `docs/temp/specs/YYYY-MM-DD-<topic>-design.md`
- Implementation plans: `docs/temp/plans/YYYY-MM-DD-<feature-name>.md`
- Execution scratch: anywhere else under `docs/temp/`

Do not use the upstream `docs/superpowers/` default — it is superseded here.
Promote a durable conclusion out of `docs/temp/` into a committed document or a
standard; leave the working copy where it is.

## The local gate

A change is done only when the repository's own gate passes:

```bash
python3 scripts/coacus.py generate
python3 scripts/coacus.py validate
python3 scripts/coacus.py check
python3 -m unittest discover -s tests
```

`generate` refuses to write while source validation fails; `check` must report
no drift. CI runs `validate` → `check` → `completeness` → tests and never
`generate`, so a drift failure means regenerate locally and commit the result.

## Ship through review

- Branch from `main`; never commit structural change straight onto `main`.
- One logical change per commit, Conventional Commits, imperative summary.
- Commit the regenerated artifacts together with the source change that produced
  them.
- The pull request carries the generated diff; the repository squashes on merge.

## Reach the local corpus

The process workflows are the method; the local corpus is the knowledge. Every
process skill should consult it rather than improvise:

- Find the agent or skill a task needs with the routing index:
  `python3 scripts/coacus_route.py "<task>" --top 4`.
- Browse what exists once per session in `catalog/INDEX.md` and `AGENTS.md`.
- Prefer a local skill over an invented approach: brainstorming routes to the
  design and domain skills, planning cites the standards that constrain the
  change, and test-driven development uses the local gate above.

## Namespace mapping

Upstream Superpowers addresses its siblings with a colon namespace. The Coacus
skill namespace is FLAT, so every reference resolves to the installed name:

| Upstream reference | Coacus skill |
|---|---|
| `superpowers:<name>` | `superpowers-<name>` |

The imported bodies were rewritten at import time to use the flat form, so a
handoff always names a skill that exists. `using-superpowers` is not imported;
the `using-coacus` skill replaces it.

## The workflow family

| Workflow | Use it to |
|---|---|
| `superpowers-brainstorming` | explore intent and produce a design spec before building |
| `superpowers-writing-plans` | turn a spec into a bite-sized implementation plan |
| `superpowers-executing-plans` | implement a plan task by task in one session |
| `superpowers-subagent-driven-development` | implement a plan with a fresh subagent per task, plus review |
| `superpowers-test-driven-development` | write the failing test first, then the minimal code |
| `superpowers-systematic-debugging` | find a root cause instead of guessing |
| `superpowers-requesting-code-review` | ask for a review at a defined checkpoint |
| `superpowers-receiving-code-review` | evaluate and act on review feedback |
| `superpowers-verification-before-completion` | prove a change works before claiming success |
| `superpowers-using-git-worktrees` | isolate work in a worktree |
| `superpowers-finishing-a-development-branch` | close out a branch for integration |
| `superpowers-dispatching-parallel-agents` | fan out independent work |
| `superpowers-writing-skills` | author and pressure-test a new skill |
| `superpowers-diagnosing-superpowers` | diagnose the workflow collection itself |

## Attribution

The workflows are derived from Superpowers by Jesse Vincent
(<https://github.com/obra/superpowers>), MIT-licensed, imported at a recorded
commit. Attribution is kept in `THIRD-PARTY-NOTICES.md`, in each workflow's
provenance entry in `sources.lock.json`, and in a footer on every adapted
`SKILL.md`. The import record is in `docs/migration.md`.
