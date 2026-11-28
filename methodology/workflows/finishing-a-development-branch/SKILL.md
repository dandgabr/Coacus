---
name: finishing-a-development-branch
description: Use when implementation is complete, all tests pass, and you need to decide how to integrate the work
---

<!--
Coacus adaptation of a Superpowers workflow (MIT).
Upstream: https://github.com/obra/superpowers @ 5bf4e78011075bcfc0dc295f0724994cd123ee71
Process artifacts are written under docs/temp/.
Conventions: ../using-coacus/references/coacus-process-conventions.md
-->

# Finishing a Development Branch

## Overview

**Core principle:** Verify tests → Detect environment → Present options → Execute choice → Clean up.

**Announce at start:** "I'm using the finishing-a-development-branch skill to complete this work."

## Step 1: Verify Tests

Run the project's full test suite (`npm test` / `cargo test` / `pytest` / `go test ./...`).

**If tests fail**, report the failures and stop — the menu comes after a green suite:

```
Tests failing (<N> failures). Must fix before completing:

[Show failures]
```

**If tests pass:** continue to Step 2.

## Step 2: Detect Environment

```bash
GIT_DIR=$(cd "$(git rev-parse --git-dir)" 2>/dev/null && pwd -P)
GIT_COMMON=$(cd "$(git rev-parse --git-common-dir)" 2>/dev/null && pwd -P)
# Capture now, while still inside the workspace — Step 5 changes directory
# before cleanup (Step 6) needs this value
WORKTREE_PATH=$(git rev-parse --show-toplevel)
```

This determines which menu to show and how cleanup works:

| State | Menu | Cleanup |
|-------|------|---------|
| `GIT_DIR == GIT_COMMON` (normal repo) | Standard 3 options | No worktree to clean up |
| `GIT_DIR != GIT_COMMON`, named branch | Standard 3 options | Provenance-based (see Step 6) |
| `GIT_DIR != GIT_COMMON`, detached HEAD | Reduced 2 options (no merge) | Externally managed — leave in place |

## Step 3: Determine Base Branch

The base branch is whatever this work forked from — usually named in the
plan, the conversation, or the branch's upstream. If it is not already
known, ask: "This branch split from <your best guess> - is that correct?"
Confirm before merging: merging into the wrong base is expensive to undo.

## Step 4: Present Options

**Normal repo and named-branch worktree — present exactly these 3 options:**

```
Implementation complete. What would you like to do?

1. Merge back to <base-branch> locally
2. Push and create a Pull Request (archive the Coacus worktree when eligible)
3. Keep the branch as-is (I'll handle it later)

Which option?
```

**Detached HEAD — present exactly these 2 options:**

```
Implementation complete. You're on a detached HEAD (externally managed workspace).

1. Push as new branch and create a Pull Request
2. Keep as-is (I'll handle it later)

Which option?
```

Tell the user they can choose option 2 and ask to keep the worktree at its
current path. Present the menu exactly as written, with every option coming
from the list above. Discarding the work happens only in response to your
human partner explicitly asking for it (see "If your human partner asks to
discard the work" below). Wait for their answer; the integration decision
is theirs.

## Step 5: Execute Choice

### Option 1: Merge Locally

```bash
# Get main repo root for CWD safety
MAIN_ROOT=$(git -C "$(git rev-parse --git-common-dir)/.." rev-parse --show-toplevel)
cd "$MAIN_ROOT"

# Merge first — verify success before removing anything
git checkout <base-branch>
git pull
git merge <feature-branch>

# Verify tests on merged result
<test command>
```

If tests fail on the merged result: stop, leave the worktree and branch in
place, and investigate — nothing has been pushed, so the merge is local
and recoverable.

Once the merged result is green: clean up the worktree (Step 6), then
delete the branch:

```bash
git branch -d <feature-branch>
```

### Option 2: Push and Create PR

Prepare a concise PR body with these review cues, following any repository
template:

```markdown
## Summary
- <user-visible behavior or problem solved>

## Visual summary
<!-- For interface changes, include before/after captures or a short visual
     explanation of the before and after. Omit this section when the change
     has no visual surface. -->

## Evidence
- <verification command and actual result>
- <before/after behavior or generated-artifact scope, when relevant>

## Merge risk
- Decision type: <One-way door (irreversible schema/protocol break) | Two-way door (isolated logic change)>
- Blast radius: <affected components, consumers, or state persistence>
- Reversibility: <exact rollback command or migration reversal procedure>
- <migration, rollout, or compatibility concerns; state none when checked>
```

Describe only evidence collected on the branch being submitted. The merge-risk
section informs review; it does not authorize merging or deployment.

For a final delivery from a named-branch worktree, prepare cleanup before push:

```text
python3 <using-git-worktrees-skill-directory>/scripts/pr-worktree.py prepare <worktree-path> --remote <push-remote>
```

Keep the returned delivery ticket with the session handoff. It identifies the
worktree instance and the resolved push destination used for this delivery. If
preparation fails, or a resumed delivery lacks its original ticket, continue
with the PR and retain the worktree. Never regenerate a ticket to retry an
already published delivery.

```bash
git push -u origin <feature-branch>
# From a detached HEAD, name the new branch on the remote:
# git push origin HEAD:refs/heads/<new-branch>
```

Then create the pull/merge request against <base-branch> with the forge's
tooling — its CLI if one is available, or the creation URL most forges
print when you push — following the repo's PR template and conventions if
present. After a successful push, reuse an existing open request for the same
delivery when resuming. Check the actual PR in the forge and report its URL to
your human partner. A link to the PR creation form is insufficient.

This is the "Push and open the PR" step of
`../using-coacus/references/coacus-process-conventions.md`; run its
"Reinstall locally" step (`python3 scripts/coacus_install.py <harness> --verify`)
once the change is merged into a branch the harnesses consume.

For a final delivery, verify that the open PR targets the intended repository
and base branch and that its source repository, branch, and full head commit
match the remote used to prepare and push the delivery, the feature branch, and
local HEAD. Inspect the resolved remote privately and compare its host and
repository path with the forge's source repository. For GitHub, query the
specific PR by URL with `gh pr view <pr-url> --json url,state,baseRefName,headRepository,headRepositoryOwner,headRefName,headRefOid`.
Use the equivalent forge metadata when available. If the push or PR cannot be
verified, or the owner requested keeping the workspace, retain the worktree and
report the reason. Otherwise follow the PR cleanup path in Step 6.

### Option 3: Keep As-Is

Report: "Keeping branch <name>. Worktree preserved at <path>."

### If your human partner asks to discard the work

This path exists only as a response to an explicit request to throw the
work away. Confirm first:

```
This will permanently delete:
- Branch <name>
- All commits: <commit-list>
- Worktree at <path>

Type 'discard' to confirm.
```

Wait for that exact confirmation. When it arrives:

```bash
MAIN_ROOT=$(git -C "$(git rev-parse --git-common-dir)/.." rev-parse --show-toplevel)
cd "$MAIN_ROOT"
```

Then clean up the worktree (Step 6) and force-delete the branch:

```bash
git branch -D <feature-branch>
```

## Step 6: Cleanup Workspace

### After a confirmed PR

For a named-branch linked worktree, finish all work in that checkout before
cleanup, including any background jobs that can write there. Run the helper
from the main checkout, outside the worktree being removed. Resolve the helper
under the canonical or installed `using-git-worktrees` skill directory:

```text
python3 <using-git-worktrees-skill-directory>/scripts/pr-worktree.py cleanup <worktree-path> --remote <push-remote> --head-ref refs/heads/<pr-source-branch> --head-oid <confirmed-pr-head-commit> --ticket <original-delivery-ticket>
```

Use the absolute `WORKTREE_PATH` captured in Step 2. The helper requires the
original ticket, checks the published and local commits, and preserves blocked
worktrees in place. The remote probe disables interactive Git credential prompts.
If cleanup can proceed, the helper moves the checkout and its Git registration
to a private recovery directory under Git's common directory. Moving the whole
checkout preserves every file, including local writes Git may have missed. The
recovery directory retains disk usage and has no automatic expiration.

Report the PR URL and the cleanup result, including the recovery directory if
the checkout moved. When a move stops partway, report the exact recovery
location and use the restore command once the cleanup process has exited,
before attempting cleanup again. Keep the
worktree if the helper is unavailable or the session cannot leave the workspace.
The local and remote branches remain available for review. To restore the
original checkout while its branch and path are available, run this from the
main checkout:

```text
python3 <using-git-worktrees-skill-directory>/scripts/pr-worktree.py restore <recovery-directory>
```

You can also use `git worktree add <new-path> <feature-branch>` to create a new
checkout. The recovery copy preserves the previous checkout's local files.

### After a local merge or confirmed discard

The caller has already changed directory to the main repo root. Use the
`GIT_DIR`/`GIT_COMMON`/`WORKTREE_PATH` values captured in Step 2, from before that
directory change. Option 3 preserves the worktree.

**If `GIT_DIR == GIT_COMMON`:** Normal repo, no worktree to clean up. Done.

**If `WORKTREE_PATH` is under `.worktrees/` or `worktrees/`:** The workflow
created this worktree — we own cleanup:

```bash
git worktree remove "$WORKTREE_PATH"
git worktree prune  # Self-healing: clean up any stale registrations
```

**If removal is refused** (`contains modified or untracked files`): the
worktree holds files that exist nowhere else — uncommitted plans, notes,
or scratch work. Never `--force` on your own initiative. Show your human
partner what is at stake and ask:

```bash
git -C "$WORKTREE_PATH" status --porcelain -uall
```

```
Worktree removal refused — these files were never committed:

<file list>

1. Commit them to <branch> before cleanup
2. Move them into <main repo root>
3. Delete them (unrecoverable)

Which?
```

Carry out the choice, then remove the worktree.

**Otherwise:** The host environment owns this workspace — leave it in
place. If your platform provides a workspace-exit tool, use it.

## Quick Reference

| Option | Merge | Push | Keep Worktree | Cleanup Branch |
|--------|-------|------|---------------|----------------|
| 1. Merge locally | yes | - | - | yes |
| 2. Create PR | - | yes | only when cleanup is skipped | - |
| 3. Keep as-is | - | - | yes | - |
| Discard (explicit request only) | - | - | - | yes (force) |

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "Tests passed earlier this session" | Run the suite on the tree you are about to integrate. A green run only proves the tree it ran on. |
| "They obviously want it merged" | Integration is your human partner's decision. Present the menu and wait. |
| "They seem done with this feature — I'll offer to discard it" | The menu is complete as written. Discard happens only when your human partner asks for it in so many words. |
| "'Yeah, get rid of it' counts as confirmation" | Only the typed word `discard` authorizes deletion. |
| "The push printed a PR link, so cleanup can run" | Confirm the open PR and its source commit first. |
| "This other worktree looks stale — I'll clean it too" | Cleanup applies only to the worktree used for this delivery. |
| "Removal refused — `--force` is just finishing the cleanup" | The refusal means files exist only in that worktree. `--force` destroys them permanently. Show your human partner and ask. |
| "The merged-result failure is probably flaky" | A failing merged result stops everything. Branch and worktree stay put while you investigate. |
| "The base branch is obviously main" | Confirm the fork point or ask. Merging into the wrong base is expensive to undo. |
| "The push was rejected — force-push will fix it" | A rejected push means the remote moved. Investigate; force-push only on your human partner's explicit request. |
