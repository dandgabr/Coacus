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

## Reproduce the other machine

The gate above passes on the machine that ran it. CI does not: a check that is green
here can drift there when the two environments differ. When CI disagrees with the local
gate, clone the pushed commit into a clean directory and run the failing step there
before changing anything; the difference is usually the environment (a compressor, a
locale, an ignored file), not the code. An artifact whose bytes depend on any of these
cannot be drift-checked: build it from normalized inputs and pin one known value.

## Measure the environment before a command

The gate above, and every command a skill or a workflow presents, rest on an
environment nobody has checked. Probe it first — these are read-only, so they stay
in the autonomous tier:

```bash
grep -E '^ID=' /etc/os-release         # the distribution, and so the package family
rpm -q <pkg> | dpkg -s <pkg>           # is it installed
pkg-config --modversion <module>       # is its development metadata installed
command -v <tool> && <tool> --version  # is the tool there, and which version
```

- **Name the family, not one member.** Where a command must be given, it is given
  per family (`dnf`, `apt`, `brew`, `winget`) with the probe that selects among
  them — or marked as specific to one family, to be adapted.
- **A measured value carries the machine it came from.** A version, a path or a
  package list written into a document says that it was measured, and where. A value
  brought from memory is marked `unverified` and never presented as current — the
  rule `version-freshness` applies to upstream pins, extended to the machine.
- **A runtime is not its development metadata.** `pkg-config --exists` failing while
  the package manager reports the library installed is the signature of a missing
  `-devel` / `-dev` package, not of a missing library. An instruction that says
  "install the library" when the compiler wants the headers sends the agent to the
  wrong fix.

The cost of skipping this was measured: a plan repeated
`sudo apt install libwebkit2gtk-4.1-dev …` across several turns on a **Fedora 44**
machine — no apt, no package list, no source at all — where the runtime libraries
were already installed and only the `-devel` halves were missing. One
`grep /etc/os-release` would have replaced the whole detour.

## Working material is not the committed tree

Curation is part of the work, not a later chore. Before a session's artifacts
accumulate in the tree, classify every file as source, committed generated output,
working material or local state, and keep the last two out of the commit.

- Process documents — specs, plans, scratch — live under `docs/temp/`, which is
  ignored. A durable conclusion is promoted into a committed document or a
  standard; the working copy stays where it is.
- Untracked local state is regenerable or ephemeral. It is also a place a **live
  secret** can hide: a dev harness's session directory may hold a token, a port
  file or a server key created during a session and never meant to persist.
  Deleting such state is a security improvement, and it is inspected by metadata,
  never by printing a value.
- Removing a file orphans whatever pointed at it. Search the whole tree for each
  removed path and repair the reference — rewrite it to the document that now
  holds the rationale, or remove the sentence that needed it.
- The `repository-artifact-hygiene` skill carries the full procedure.

## Work that is not yours

When the tree holds uncommitted work you did not write (another agent's, or the owner's
in another tool), do not edit, stash or regenerate in place.

- Make a separate worktree on a new branch from the committed head and load a snapshot
  there: the tracked diff as a patch, and the untracked files copied. The original tree
  stays exactly as it was.
- Validate the snapshot as a stranger would: regenerate, refresh the provenance lock,
  run every gate and the whole suite. Work that was written ahead of its generated
  artifacts fails the count and drift checks until they are regenerated; that is its
  normal state, not a defect.
- Check what the work claims against what it contains: licenses and attribution (measure
  the longest verbatim overlap with a source it says it paraphrased), the cost of any
  pattern it runs on every call, and what its commands can write.
- Open a pull request, let CI judge it, and read the failures: CI found a determinism
  defect in an artifact that every local check had accepted. After it merges, tell the
  owner that the uncommitted copy is redundant; never delete it for them.

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
| `grilling` | interview the user in frontier rounds until the design tree is resolved |
| `grill-me` / `grill-with-docs` | the grilling interview, plain or with documents |
| `handoff` | compact a session for the next agent |
| `domain-modeling` | build and sharpen the glossary; record ADRs sparingly |
| `diagnosing-bugs` | build a tight feedback loop before any hypothesis |
| `to-spec` | synthesize a spec and confirm the test seams |
| `to-tickets` | vertical tracer-bullet tickets with blocking edges |
| `implement-spec` | parallel implementers over the ready frontier |
| `two-axis-code-review` | isolated Standards and Spec review |
| `retro` | turn a session into environment improvements |
| `phase-boundaries` | decide continue / clear / handoff / subagent / compact |

## Attribution

The workflows are derived from Superpowers by Jesse Vincent
(<https://github.com/obra/superpowers>), MIT-licensed, imported at a recorded
commit. Attribution is kept in `THIRD-PARTY-NOTICES.md`, in each workflow's
provenance entry in `sources.lock.json`, and in a footer on every adapted
`SKILL.md`. The import record is in `docs/migration.md`.
