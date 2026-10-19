# Git History and Recovery

Use this reference when changing commit history, recovering lost work or
locating the change that introduced a regression. First inspect the repository,
the refs involved and whether the commits have been shared.

## Choose the operation by intent

| Goal | Starting point |
|---|---|
| Add an inverse change to shared history | `git revert <commit>` |
| Move a private branch pointer while preserving working files | Inspect `git reset --soft` or `--mixed` and the target range |
| Discard local index and working-tree changes | `git reset --hard` only after explicit confirmation and a verified backup or recovery path |
| Copy one existing change onto another branch | Inspect `git cherry-pick`, including conflicts and resulting commit identity |
| Reorder or combine private commits | Use interactive rebase after confirming the range and clean working state |
| Temporarily set aside local edits | Inspect `git stash list` and include untracked files only when intended |

These commands are not interchangeable. Before running one, show the commit
range, affected paths and whether the ref is published. Do not recommend a hard
reset, forced update or history rewrite merely to make status appear clean.

## Recover a commit or branch

The reflog records local ref movement for a configurable period. Inspect it and
identify the desired commit before changing any ref:

```text
git reflog --date=local
git show <candidate>
git branch rescue/<topic> <candidate>
```

Creating a rescue branch preserves the candidate while the recovery is
reviewed. Do not use an ordinal such as `HEAD@{2}` without checking what it
resolves to in the current repository. If the object is unreachable, inspect
`git fsck --no-reflogs --unreachable` output before attempting recovery. Avoid
pruning or aggressive garbage collection during recovery.

## Find regressions

- Use `git log` and `git blame` to understand relevant history, not as proof of
  intent by themselves.
- Use `git bisect` only when a repeatable good/bad test exists. Mark
  untestable commits as skipped and verify the final result against the
  suspected change.
- Use pickaxe or path-limited diffs to narrow a search; confirm the actual
  behavior in the relevant revision.

## Rewrite a repository history

History filtering affects every downstream clone and reference. Before using a
history-rewrite tool, make a verified backup, enumerate affected paths and refs,
coordinate the maintenance window, and prepare collaborator resynchronization
instructions. If credentials were present, revoke and replace them before the
rewrite. Verify the resulting refs and objects; a successful filter does not
prove the secret was never copied elsewhere.
