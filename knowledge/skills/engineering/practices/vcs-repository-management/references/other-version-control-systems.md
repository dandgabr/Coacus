# Other Version-Control Systems

Use this reference when administering or migrating Subversion (SVN), Mercurial
(Hg) or Perforce. Confirm server edition, repository layout, extension
availability and installed command versions before giving operational steps.

## Subversion

SVN uses central repository revisions and versioned properties. The common
`trunk/branches/tags` layout is a convention, not a requirement. Inspect
`svn:mergeinfo`, `svn:externals`, ignore and line-ending properties when
planning a migration. Use peg and operative revisions deliberately when tracing
renamed or deleted paths. For server administration, plan and verify repository
backup, restore, integrity checks and mirror synchronization using the
installed server's official documentation.

SVN hooks can reject a transaction. Review hook code and execution identity;
keep secrets out of command output and logs. A local hook or client-side rule is
not equivalent to an enforced server-side rule.

## Mercurial and Perforce

Mercurial is distributed and has different command and extension conventions
from Git. Perforce commonly uses a centralized server and workspace model.
Do not translate commands or assume branch, merge, locking or history semantics
are equivalent. Establish the source of truth, server permissions, workspace
state and migration goals first.

## Cross-system migration

Preserve an explicit map of users, branches, tags, labels, large-file storage,
subprojects, permissions and server-side automation. Trial the conversion and
compare representative histories and file contents. Schedule a write freeze or
final synchronization, verify the destination before switching users, and keep
the source read-only until rollback is no longer required.
