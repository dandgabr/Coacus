# Git Scale and Migration

Use this reference when repository size, binary assets, component boundaries or
history migration affect day-to-day work. Measure the repository and workload
before selecting a scaling technique.

## Large repositories

- Partial clones defer selected object content; shallow clones limit history.
  They solve different problems and can constrain history-based tools.
- Sparse checkout limits the working-tree paths. Confirm the selected patterns
  still include build, test and shared files required for the task.
- Git LFS stores large-file content outside ordinary Git objects. Review the
  server, authentication, retention and collaborator requirements before
  migrating tracked files; the committed pointer file alone is not the asset.
- Git maintenance and garbage collection can affect recovery and storage. Do not
  run aggressive pruning while diagnosing lost objects or before backups are
  verified.

## Subprojects

Submodules record a specific external commit and require consumers to initialize
and update them. Subtrees place subproject content inside the parent repository
and can combine or squash history. Choose based on update ownership, consumer
workflow and the need to inspect upstream history; document the update procedure
for contributors.

## Migration

1. Inventory branches, tags, authors, large files, subprojects, hooks and
   repository policies.
2. Map identities and branches explicitly, and choose which history and refs
   must be preserved.
3. Run a trial migration into a separate repository and verify commit counts,
   tags, representative file histories and build behavior.
4. Plan the freeze, final synchronization, remote cutover, access policy and
   rollback path before publishing the migrated repository.

For SVN, Mercurial and Perforce-specific concepts, conversion choices and
administration, use [Other version-control systems](other-version-control-systems.md).
