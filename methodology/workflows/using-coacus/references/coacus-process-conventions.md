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

After the local gate is green, two steps complete the change:

- **Push and open the PR.** Push the branch and create the pull request:

  ```bash
  git push -u origin <branch>
  gh pr create --title "<type>(<scope>): <summary>" \
    --body "<what changed; how it was verified; the regenerated diffs>"
  ```

  The PR body must carry the regenerated diffs (`catalog/`,
  `knowledge/**/dist/`, `harnesses/*/bootstrap/`, `sources.lock.json`) alongside
  the source change. `--fill` is not enough: it derives the body from the commit
  messages and cannot state the diff set or the verification commands.

- **Reinstall locally.** Refresh the artifacts in the harnesses present on this
  machine, then verify them:

  ```bash
  python3 scripts/coacus_install.py all
  python3 scripts/coacus_install.py all --verify
  ```

  Quote the `--verify` output (canonical component counts, install root, drift).
  `--verify` exits non-zero on drift AND on a harness with no manifest, so a
  harness absent from this machine is reported as `harness_present: false` and
  still fails the run; read the per-harness records rather than the exit code
  alone. Run `--verify` for the harnesses you actually installed when you want a
  clean exit.

## Reach the local corpus

The process workflows are the method; the local corpus is the knowledge. Every
process skill should consult it rather than improvise:

- Find the agent or skill a task needs with the routing index:
  `python3 scripts/coacus_route.py "<task>" --top 4`.
- Browse what exists once per session in `catalog/INDEX.md` and `AGENTS.md`.
- Prefer a local skill over an invented approach: brainstorming routes to the
  design and domain skills, planning cites the standards that constrain the
  change, and test-driven development uses the local gate above.

## Select agents for a task (roster)

When a task or a plan is prepared, route its own text to the agent corpus and let
the user pick who executes. This is the roster step; it is the one place a
workflow may call the router automatically.

1. Compose the routing prompt from the task's own text: its title, its
   deliverable and the interfaces it produces.
2. Rank the agents for that text:

   ```bash
   python3 scripts/coacus_route.py "<task text>" --top 5
   ```

   Add `--max-slots` when a concurrency cap is in play. Each row is
   `score <TAB> name <TAB> category <TAB> matched`.
3. Present a NUMBERED list, one row per candidate, carrying the agent name,
   category, score and `matched` terms. Showing `matched` matters: a lexical
   false positive (a word matched in another sense) is visible and can be
   rejected instead of trusted.
4. The user answers in the conversation: `1,3`, `all`, or agent names.
5. Validate the choice before relying on it:

   ```bash
   python3 scripts/coacus_route.py --agents <name1>,<name2>
   ```

   An unknown name exits non-zero. When a close match exists it also prints
   suggestions; a bare trigger alias resolves to its agent. Read the output and
   correct the name — never guess.
6. Hold the validated roster in session memory, keyed by task. The roster is
   NEVER written to the plan or to any tracked or generated file.

Select agents per task. The step proposes and validates; it never spawns.
Concurrency stays the governor's job (`docs/standards/orchestration-governance.md`).

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
