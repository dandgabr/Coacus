---
name: repository-artifact-hygiene
description: >-
  Provides repository curation practice for separating durable documentation from
  development artifacts. Use when cleaning a repository, deciding what is source
  versus generated versus working material, repairing references after a removal,
  or auditing untracked local state.
tags:
  - repository
  - hygiene
  - documentation
  - cleanup
---

# Repository Artifact Hygiene

A repository accumulates four kinds of file, and only some belong in the
committed tree. Curation is the discipline of telling them apart, removing the
ones that do not ship, and repairing whatever pointed at what was removed.

## 1. Classify before deleting

Every file is exactly one of these. The classification, not the file's location,
decides whether it is committed.

| Kind | Committed? | Examples |
|---|---|---|
| **Source** | yes | code, canonical docs, test fixtures that the suite reads |
| **Generated** | yes, if the project commits it | build from a source; regenerated, never hand-edited |
| **Working material** | no | design specs, plans, exploration notes, scratch |
| **Local state** | no | caches, build output, dependency trees, tool sessions |

- A **fixture** the test suite reads is source, even though it is "test data".
  Do not sweep it up with the working material.
- A **generated file the project commits** must be regenerated, never edited and
  never deleted by hand.
- Working material and local state both leave the tree; they differ in where they
  live and why they are removable.

## 2. Keep working material out of the committed tree

Process documents — a design spec before building, an implementation plan per
feature, per-run scratch — are intermediate. Give them one conventional,
**ignored** location rather than the documentation root.

- The ignored working directory is the convention; a durable conclusion is
  **promoted** out of it into a committed document or a standard, and the working
  copy stays where it is.
- Do not commit working material "for history". It drifts out of date, dilutes
  the committed documentation, and its dates lie about the current design.
- When a committed document is the only remaining rationale for a decision, that
  rationale belongs in the documentation, not in a working plan.

## 3. Local state is removable — and may hold a live secret

Untracked, ignored state is regenerable or ephemeral. Before deleting it, treat
it as a place a secret can be hiding.

- **A tool's session state can carry a live credential.** A dev harness's state
  directory may hold a session token, a port file, a server key — created during
  a session and never meant to persist. Deleting the state is a security
  improvement, not only a cleanup.
- **Read metadata, never print a value.** To decide whether a store is safe to
  delete, list names and types; do not dump contents into a log or a transcript.
- **State is reproducible or worthless.** Build output and dependency trees are
  rebuilt by the toolchain; a cache is refilled on demand. If neither is true,
  it is not local state — it is source that was misplaced.

## 4. Repair the references you orphan

Removing files without fixing what pointed at them leaves a repository that
looks curated and is broken.

- **Search before you finish.** Grep the whole tree for each removed path — in
  prose links, code, config and manifests — and repair every hit. A link is not
  repaired because the file that held it "probably" is fine.
- **Rewrite, do not dangle.** Point the reference at the durable document that
  now holds the rationale, or remove the sentence that needed it. A dead link in
  shipped documentation is worse than no link.
- **Distinguish a reference from a mention.** A path inside a fenced code block
  or a provenance record may be illustrative or historical; a markdown link in a
  README is a promise.

## 5. Leave the gate green

Curation is a structural change and ships like one.

- After a removal or a move, **regenerate** any committed generated output and
  run the repository's own checks (drift, links, counts) before declaring done.
- **Update measured counts** in prose when the corpus changes. A count copied
  from memory drifts; the generator is the contract.
- Commit a removal with the reference repairs and the regenerated artifacts in
  the same change, so the tree is never committed in a broken intermediate state.

## Verification checklist

- Every file left in the tree is source or committed generated output.
- Working material is under the ignored working directory, not the docs root.
- No reference in any tracked file points at a removed path.
- No secret remains in the removed local state; it was inspected by metadata, not
  by value.
- The project's gate passes, and prose counts match the freshly generated corpus.

## Related Skills

- [documentation-designer](../documentation-designer/SKILL.md): Diátaxis keeps
  the durable docs coherent once the working material is gone.
- [vcs-repository-management](../vcs-repository-management/SKILL.md): history
  operations when a removal must be expunged rather than committed.
- [clean-code-reusability](../clean-code-reusability/SKILL.md): the same
  one-source, no-duplication instinct applied to files instead of functions.
