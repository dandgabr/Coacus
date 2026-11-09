# Git Collaboration and Recovery

Use this reference for routine local changes, branch coordination, remotes and
merge conflicts. Start with the safe operating procedure in the parent skill.

## Inspect before changing state

Establish the full picture before acting:

```text
git status --short --branch
git diff
git diff --cached
git branch -vv
git remote -v
git log --graph --oneline --decorate --all -n 30
```

Check ignored and untracked files when the requested operation may affect them.
Confirm the intended repository, remote and base branch from the request and
repository state. A remote-tracking ref can be stale; fetch before relying on it.

## Local changes and commits

- Stage only the intended paths; inspect the staged diff before committing.
- Use interactive patch staging when a file contains unrelated changes.
- Use `git restore --staged <path>` to unstage while preserving the working-tree
  copy. Use `git restore <path>` only after confirming that discarding the
  unstaged changes is intended.
- Prefer `git switch` for branch changes and `git restore` for restoring files;
  use `checkout` only when an existing workflow or compatibility requirement
  calls for it.
- Keep commits focused and explain the reason in the message. Conventional
  Commit formatting is governed by the `git-conventional-commits` skill.

## Branches and remotes

- Use `git fetch <remote>` to update remote-tracking refs without integrating
  changes into the current branch.
- Inspect `git branch -vv` and the commit graph before choosing merge, rebase or
  cherry-pick. Confirm the upstream relationship rather than assuming `origin`
  or `main` is the requested target.
- A fast-forward, merge commit, rebase and squash produce different history.
  Choose based on repository policy and whether the commits are already shared.
- Before pushing, compare the local branch with its intended remote base. Avoid
  force-pushing shared branches; if a rewrite is explicitly required, coordinate
  it and use the safest lease-based form supported by the installed Git.

## Merge conflicts

1. Identify the operation in progress and list the conflicted paths.
2. Read the base and both sides of each conflict; do not resolve by blindly
   accepting one side or copying unrelated code.
3. Edit and stage each resolution, then review the complete resulting diff.
4. Run the checks appropriate to the affected files.
5. Complete the operation only after confirming the staged result. Abort when
   the correct resolution cannot be established safely.

Use `git merge --abort` or `git rebase --abort` only for the matching operation
and after confirming the current work can be preserved by that operation.

## Patches and hooks

Patches can transfer a reviewable change without sharing a branch; inspect their
metadata and content before applying. Git hooks can automate local checks, but
are not guaranteed to exist on another clone and can execute arbitrary code.
Inspect hook sources before enabling them and use enforced server or CI checks
for repository policy.
