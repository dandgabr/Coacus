# Accounts and API reporting

Use this reference for multi-account preferences, authentication, deletion and
quota or spending adapters. It records transferable practices; provider endpoints
and permissions still require current primary documentation.

## Connector state is separate from authentication

A connector identifies one configured account, not an entire provider. Distinguish
no connectors, configured but disconnected, authenticating, connected, paused and
failed. Saving its metadata does not prove authentication. An empty quota view with
a saved disconnected connector should direct the user to that existing editor,
rather than ask for another account. Announce credential changes across processes
and refresh the popup without requiring extension restart.

Keep an immutable connector identifier across renames. Scope credentials, cache,
status and in-flight work to that identifier; provider identity selects the adapter.
Test two accounts from one provider and ensure deleting one preserves its sibling.
Decode identifiers and registries using the active data source: a synthetic-only
provider must not invalidate the whole Demo registry or lose its label/icon.

Share authentication controllers between onboarding and account editors. Serialize
sign-in, retain explicit terms consent, cancel on close and suppress secret values
in status/error text. A completed save and its announcement must settle once.

## Deletion invalidates work, not just stored metadata

Separate configuration restoration from deleting connectors; name each action by
what it changes. Apply the skill's settings-classification rule. Synthetic accounts,
including monetary examples, belong in their own persisted registry and are
removable. An explicitly empty list must stay empty after restart or scenario
changes; default seeding must not resurrect deleted examples.

Capture identity and an operation generation before asynchronous credential work;
recheck them after lookup, before HTTP dispatch and before persistence. Deletion
must fence refresh, rotation and late callbacks. Associate promise cleanup with the
operation that created it: an older completion must not clear a newer pending
operation or re-enable a disposed view.

Where deletion spans processes and persistent stores, coordinate it durably. Use
atomic generation/lease transitions, exact owned credential scopes and confirmed
writes. Drain or fence issued mutations before removal. Rejected settings writes,
unavailable keyrings and partial deletion are failures with retained fences and a
retry path, not successful absence. Expand coordination metadata without losing
existing epochs, blocked scopes or issued leases; incompatible older writers must
not silently reopen them. Do not reclaim a same-boot orphaned mutation merely
because a timeout elapsed; recovery needs an authority that establishes its owner
cannot still write.

The store must provide a cross-process atomic read/check/write transaction and
exclusive ownership for an issued external credential mutation. Plain settings
read/modify/write and a process-local mutex do not establish these guarantees.
The [example coordination store](https://github.com/dandgabr/elfvision/blob/93b17f5192290e10de834125061735f3b9e3a270/lib/services/disconnectStore.js)
and [state machine](https://github.com/dandgabr/elfvision/blob/93b17f5192290e10de834125061735f3b9e3a270/lib/core/disconnect.js)
illustrate a concrete implementation; inspect its transaction and crash-recovery
assumptions before reusing it. Another coordination primitive is suitable if it
provides equivalent fencing, ownership and persistence guarantees.

## Recover transport ownership without erasing durable fences

A session-bus identity is not a boot identity. Logout/login on the same boot can
replace the D-Bus GUID; a boot-specific pin to the old GUID then rejects healthy
accounts before credential lookup. Treat an empty popup plus preserved account
rows as a reason to inspect coordination admission, not proof that credentials
were lost. Clearing settings or deleting coordination metadata destroys evidence.

A mutex on one session bus does not serialize another bus using the same state
directory. Acquire a shared authority before replacing a stale session pin. In
the observed Linux implementation, a permanent private regular lock file carries
a kernel lock over each metadata transaction. Reject unsafe file types and keep
the lock inode stable: replacing or unlinking it permits callers to lock different
files under the same name. Preserve epoch, transaction and issued credential
leases when recovering the transport pin; an orphaned external mutation stays
fenced under the state machine's recovery policy.

When a short helper obtains a Linux file lock, keep its open-file description
owned by the parent for the whole transaction. The helper inherits a duplicate of
the parent's retained descriptor; closing the helper does not end exclusion while
that descriptor remains open. Release launcher-owned duplicates promptly and close
the retained stream in every completion/failure path. See
[flock semantics](https://man7.org/linux/man-pages/man2/flock.2.html) and
[descriptor transfer](https://docs.gtk.org/gio/method.SubprocessLauncher.take_fd.html).
Declare the deployed helper dependency and verify its availability rather than
assuming it exists on every desktop or filesystem.

Keep a compatible legacy mutex where needed. Before stale-session takeover,
check recorded participants, lease owners and transaction coordinator separately,
using boot, PID and process start identity. An unregistered old client paused on a
still-running different bus may ignore the new kernel lock; recorded-owner checks
cannot establish safety for that mixed-version race. The observed migration is
scoped to completed session turnover, not arbitrary concurrent old versions.

Test two independent private buses sharing state, live owners in each category
alone, clean turnover, callback errors, helper exit, holder death, acquisition
timeout, unsafe lock files and unchanged lock inode. Compare complete metadata
before/after recovery, including epoch. A fixture with both a live participant and
a live lease can mask omission of either check. Kill isolated single-edit mutants
of each owner check and metadata preservation. See the
[session-recovery evidence](https://github.com/dandgabr/elfvision/blob/93b17f5192290e10de834125061735f3b9e3a270/docs/temp/session-coordination-recovery.md).

## Prove the state transition

In isolated native preferences and Shell sessions, exercise delete all → add only
→ connect → visible card, then rename, pause/resume, cancel, remove and restart.
Assert the intermediate text and editor target as well as the final card. Use
deferred synthetic operations to resolve a lookup or save after deletion and after
a newer operation starts. Inject persistence rejection and keyring unavailability.
An invalid synthetic OAuth encoding can exercise local credential detection
without dispatching a provider request; it does not verify real OAuth login.

## API keys do not imply quota APIs

Verify the published reporting endpoint and required authorization before exposing
a connector as supported. A normal inference key, organization admin key,
management key and team admin key can have different access. Unsupported public
reporting is an explicit limitation or deferral, not invented quota data. Research
whether a balance is per key, organization or team; label that scope honestly.

Keep request hosts and methods fixed, clamp response sizes and pagination, reject
repeated cursors, obey reporting cadence, and check cancellation between pages.
Normalize data before serializing cache so raw identities and extra fields do not
persist. User-facing failures must not repeat response bodies or credentials.

Represent reported spend, capped allowance and prepaid balance separately. Convert
units at the boundary (including decimal cent strings); account for pagination and
the reporting window. Unknown limits produce no percentage, meter or threshold
alert. A reported zero allowance is valid, but division by zero is not. Preserve
the complete currency text in both panel and card. Test body and top-bar behavior
for capped, uncapped, exhausted and error states.

## Reporting a problem

Keep public bug reporting and private vulnerability reporting as separate actions.
Use fixed destinations, reviewed forms and a safe launcher failure message. Do not
fall back from a failed private route to a public issue or silently collect logs,
account metadata or secrets. On GitHub, issue forms and private vulnerability forms
have distinct repository locations; validate their current schemas and confirm
private reporting is enabled before promising that route. Templates in a pull
request do not become the default-branch forms until merged.

## Evidence and limits

Derived from the [shipped provider contract](https://github.com/dandgabr/elfvision/blob/223edf5fa9b6df886144e754ffd4955bed08a048/docs/providers.md),
[credential-race record](https://github.com/dandgabr/elfvision/blob/223edf5fa9b6df886144e754ffd4955bed08a048/docs/temp/reviews/2026-10-08-credential-race-fixes.md)
and [connector regression](https://github.com/dandgabr/elfvision/blob/223edf5fa9b6df886144e754ffd4955bed08a048/docs/temp/reviews/2026-10-08-connector-refresh-theme-defaults.md),
recorded on 2026-10-08. These synthetic and boundary tests do not establish real
provider authentication or future API compatibility.
