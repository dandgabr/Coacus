---
name: vcs-repository-management
description: >-
  Guides safe Git operations, repository recovery, collaboration, scaling and
  migration, and administration of Subversion, Mercurial and Perforce. Use when
  a task changes shared history, repairs a repository, handles large repositories
  or migrates version-control systems.
---

# Version Control and Repository Management

Use this skill when a task needs repository operations beyond routine staging and
committing. It covers Git internals and collaboration, repository recovery,
scaling and migration, plus non-Git version-control systems.

## Safe operating procedure

1. Establish the repository root, current branch, working-tree state, index
   state, remotes and relevant upstream before choosing a command. Do not infer
   the target branch from its name.
2. Determine whether the affected commits are local or already shared. Ask
   before an irreversible operation or a rewrite that changes published history.
3. Prefer the least destructive operation that reaches the requested outcome.
   Preview path and commit ranges before changing files or refs; preserve staged,
   unstaged and untracked work.
4. After acting, inspect status, the resulting diff and relevant commit or remote
   refs. Report what was verified and what remains uncertain.

For everyday Git collaboration, branch and remote selection, fetch/push, and
conflict handling, read [Git collaboration and recovery](references/git-collaboration-and-recovery.md).
For reset, revert, rebase, reflog, bisect and history rewriting, read
[Git history and recovery](references/git-history-and-recovery.md). For large
repositories, storage, subprojects and migrations, read
[Git scale and migration](references/git-scale-and-migration.md). For SVN,
Mercurial and Perforce administration and migration, read
[Other version-control systems](references/other-version-control-systems.md).

## Core concepts

Git records snapshots in a content-addressable object database. Commits point
to trees, trees point to blobs and subtrees, and branches are movable refs to
commits. The index records the next snapshot; it is distinct from both the
working tree and committed history. Use these distinctions to explain a status,
diff or recovery plan before changing state.

The repository may use SHA-1 or SHA-256 object formats. Do not assume object IDs
have a fixed length or compare them across repositories without checking the
repository format.

## Branching and governance

Choose a branching model that matches release cadence, team size and deployment
constraints. Keep branches short-lived where practical, make commits reviewable,
and keep protected branch rules, required checks and ownership aligned with the
repository's actual risk. Signing and a branch naming convention do not replace
review or access controls.

## Limits and safety notes

- A reflog is a local recovery aid with configurable retention, not a backup or
  a remote history service.
- Rewriting history can invalidate collaborators' refs and signatures. Prefer
  `revert` for a change already shared; coordinate any required rewrite and
  verify the exact ref range before publishing it.
- Removing a secret from Git history does not revoke the exposed credential.
  Rotate it first, then plan and communicate the rewrite and its downstream
  effects.
- Git hooks are local execution points unless provisioned and enforced by a
  trusted system. They are not a security boundary on their own.
- Treat example commands as patterns. Check the installed Git and extension
  behavior before relying on a recent option or a platform-specific detail.
