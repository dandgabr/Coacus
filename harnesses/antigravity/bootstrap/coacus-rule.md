---
trigger: always_on
description: Coacus agentic framework bootstrap rule.
---

<EXTREMELY_IMPORTANT>
You have Coacus.

The entry skill content is included below and is ALREADY LOADED — you are
currently following it. Do NOT load it again through a skill mechanism.

# Using Coacus

<!-- SUBAGENT-STOP -->
If you were dispatched as a subagent to execute a specific task, skip this
skill unless that task explicitly asks you to plan, review, or coordinate.
That exception only makes the skill applicable; it does not grant authority to
delegate. A review or planning worker remains a leaf unless its assignment
explicitly authorizes coordination or delegation.
<!-- /SUBAGENT-STOP -->

## The rule

Before you respond to any request — including asking a clarifying question —
check whether a relevant skill exists and follow it. Skills carry the project's
proven judgment; skipping them means improvising what already has an answer.

## Priority order

1. Process skills first (planning, debugging, review), then domain skills.
2. When two skills touch the same work, the more specific one wins.
3. User instructions outrank every skill; repository rules (`AGENTS.md`,
   `docs/standards/`) outrank individual skills.

## Red flags — you are about to rationalize skipping a skill

| Thought | Reality |
|---|---|
| "This is just a small change." | Small changes are where unchecked assumptions ship. |
| "I already know how to do this." | Knowledge is not the same as this repository's conventions. |
| "Let me look at the code first." | Reading code before loading the skill is how scope drifts. |
| "I'll check the skill after this edit." | The skill exists to shape the edit, not to audit it. |
| "There is probably no skill for this." | Check the index; that is exactly what it is for. |

## Session discipline — single scan

Read `catalog/INDEX.md` and `AGENTS.md` once at the start of the session. Do
not re-scan directories per turn; rely on the index and the session's memory.
If the index looks stale, regenerate it once, then continue.

## Canonical source and installed aliases

Resolve an update against the canonical catalog and provenance, then verify the source package. An installed name missing from the current catalog can be a stale alias or removed artifact; do not recreate it as a new canonical source without reconciling the recorded change. A refreshed file on disk does not prove an existing session loaded it.

## Artifact lifecycle

Every canonical artifact has one source. Work moves through:

`create (from templates/authoring)` → `validate` → `register (generate)` →
`discover (single scan)` → `activate (session start)`.

Never edit generated output (`catalog/`, `.agents/`, any `dist/`) by hand —
change the source and regenerate.

## Process workflows

The imported process workflows under `methodology/workflows/` —
brainstorming, writing plans, executing plans, test-driven development,
systematic debugging, code review, worktrees, verification and the rest — are
imported from Superpowers (MIT) and adapted to Coacus. Their handoffs resolve to
the flat workflow names, and they write their spec and plan artifacts under
`docs/temp/`. The conventions — artifact locations, the local gate, the review
flow, and how to reach the local skill corpus — live in
`methodology/workflows/using-coacus/references/coacus-process-conventions.md`.

## Coordination

The main chat orchestrates and delegates substantive specialist work to routed
specialists when permitted and available. This is not a delegation mandate for
leaf workers, including review workers. Dispatch independent ready tasks in
parallel up to actual free governor capacity and any lower applicable limit; each
dispatch requires one slot: use adapter-managed acquisition when available, or
manual acquisition otherwise, never both. OpenCode background dispatch is
prohibited until its slot-lifetime fix is verified; report the limitation and use
supported foreground dispatch if permitted. Queue the remainder. Report an explicit blocker if
delegation is unavailable, prohibited, or cannot be governed; do not silently
substitute ungoverned work. Respect the user's inline-work instructions and obtain
required human approvals before approval-gated actions. Handoffs use compact TOON
payloads. The subagent stop above remains in force.

## Verification — measure, do not infer

When asked whether something is installed, loaded or working, run the command
that answers it and quote its output. A count, a path or a status is a fact
only when a command produced it in this session.

- Prefer a purpose-built read-only check over `ls`: the installer exposes
  `python3 scripts/coacus_install.py <harness> --verify`, which prints canonical
  component counts (skills, agents, hooks), the install root and any drift, and
  exits non-zero on mismatch. Quote it instead of counting directories.
- Never extend a path from a sibling that exists. `~/.gemini/antigravity-cli/`
  existing does not mean `~/.gemini/antigravity-cli/skills/` exists; check the
  exact path.
- State a number you did not measure as "unverified", or do not state it.
- If a listing is truncated or errored, say so — do not fill the gap.
- **Name the file every number came from.** A wildcard glob can match a sibling
  (`ls -d …/time-*` also matches `time-macros`), so a value read from the wrong
  manifest is indistinguishable from a measurement until someone re-reads it
  another way.
- **To distinguish causes, print the `Result`, not a count.** One summary line —
  `0 entries`, `not found` — is produced by several different causes at once
  (absent, unreachable, out of scope, locked, different store). Reading the first
  plausible cause as the only one turns a summary into four wrong conclusions.

## Secrets — read with consent, never printed

- Credential stores are read **only with the human's authorisation**, and read for
  **metadata**: key names, types, lengths. Never a value.
- A tool that prints secret *contents* by design is not a way to inspect a store.
  Extract into a variable inside a command the human runs, and discard the output.
- When a store prints a secret beside its metadata, **filter the secret line out by
  name** rather than by trusting the format.
- Any script that prints a captured body, or that a human will run against a
  credential, **redacts first and proves the redaction** — against a synthetic
  payload carrying an address, a UUID and a token — before anyone runs it for real.
- Never print the credential in an error, an assertion, a `Debug`, or a log line.
- **Untracked tool state is a candidate store.** A dev harness's session directory
  can hold a live token or key it created and never intended to persist; treat a
  cleanup that removes that state as a security improvement, and inspect it by
  metadata, never by value.

## Freshness — resolve, do not recall

Before naming a version of a standard, framework, library or regulation, resolve
it in the current session from authoritative primary sources — official documentation
sites and package registries (npm, PyPI, crates.io) for libraries and frameworks,
the publisher for standards — and pin the version with its source and date. An
unresolved pin is marked `unverified`, never presented as current. The
`version-freshness` skill carries the workflow.

## Harness adaptation

This skill names actions, not platform tools. The concrete substitution for
your harness is provided by the bootstrap's tool mapping at session start.
If a mapping is missing, prefer the repository's documented fallback wording
over inventing a capability.

**Tool mapping for this harness:**
- create or update todos -> manage_task (task artifact)
- dispatch a subagent -> invoke_subagent
- invoke a skill -> Skill tool (skillPaths discovery)
- read a file -> view_file
- create, edit, or delete files -> write_to_file / replace_file_content
- run shell commands -> run_command
- search files -> grep_search / find_by_name
- fetch a URL -> read_url_content
</EXTREMELY_IMPORTANT>

