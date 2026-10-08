# Verification, packaging and the running session

Use this reference for native test harnesses, ZIP distribution, release verification
and installation into a real desktop. Commands below are GNOME examples, not
permission to publish or restart a session.

## Isolate before testing

A throwaway compositor needs its own session bus, display, keyring and data,
configuration, cache, state and runtime directories. A private bus alone does not
protect host runtime sockets or files. Use synthetic accounts and an in-memory
settings backend; an empty configuration must actually be empty rather than a
copy of the user's client configuration. An empty file is not valid JSON: prefer
an absent file when exercising the unconfigured path.

Apply the skill's generated-input build rule before native checks. Await
asynchronous probes; follow the current indicator after rebuild rather
than retaining a destroyed instance. Destroy only processes/resources owned by
the harness. Probes that delete data must verify their private settings/directories
before the first mutation, not merely check that Demo is selected.

The Shell evaluation channel returns a success flag and payload. A wrapper exit
code of zero can accompany `(false, "assertion failed")`. Parse that result,
require the explicit final success marker and inspect native diagnostics. Seed an
assertion failure to prove the gate rejects it. Treat allocation warnings, actual
JavaScript/critical errors and expected shutdown messages distinctly; neither a
silent log nor a generic nonzero exit replaces the behavioral assertion.

Define the final marker as a structured result tied to the expected source and
cases, for example `{"finished":true,"ok":true,"revision":"expected-digest",
"cases":["delete-add-connect"],"error":null}`. A successful evaluation that only
starts an async job is not completion. Poll for `finished` with a bounded deadline,
then evaluate and validate the final result: reject transport failure, native
success flag false, unfinished/timed-out jobs, `ok` false, unexpected revision,
missing cases or a non-null error. A text marker alone must not hide those states.

## Verify the standard archive itself

Confirm supported Shell versions and user-facing version metadata. Use the
standard extension packer; ship root metadata/code, runtime assets, schema,
translations, necessary helper and licenses. Exclude development tools, tests,
reports, credentials and local state. Website-assigned numeric version metadata
is separate from a release's user-facing version name.

Audit archive paths, duplicate entries, checksums, expected runtime files and byte
equality against the exact committed source and its generated catalogs. Install
the actual ZIP in a private data directory, check the compiled schema, and enable
it from that installed directory rather than a symlink to the checkout. Exercise
its Demo cards and preferences before reporting the package loaded.

For an authorized release, synchronize a clean branch, identify the exact commit,
and tie the tag, package, source manifest and checksum to it. Keep installation
instructions accurate for the published asset. After upload, download the public
assets and check the downloaded archive against the published checksum and tag.
A locally generated archive does not prove uploaded content or publication.

## Installed files are not necessarily loaded code

An existing desktop can retain old extension modules and metadata after new files
are installed. Check both the on-disk package and the running Shell's reported
identity/version/state. `ACTIVE` confirms activity, not that the intended version
is running. Disabling and enabling is not evidence of module reload.

For example, this delivery installed version 0.1 while the current GNOME Shell
50.5 still reported an active older version. The appropriate report separated
verified installed files from the pending fresh-session load. On Wayland, advise
logout/login when needed; do not restart the user's desktop automatically.

```sh
gnome-shell --version
gnome-extensions info <extension-uuid>
gnome-extensions install --force <release-archive>.zip
gnome-extensions enable <extension-uuid>
```

Interpret the output and installed metadata before claiming which version runs.
Read-only version and file-digest checks need no credential inspection.

## Evidence and limits

Practices were validated in the [v0.1 release](https://github.com/dandgabr/gnome-ai-quota/releases/tag/v0.1)
on 2026-10-08. The [source commit](https://github.com/dandgabr/gnome-ai-quota/tree/223edf5fa9b6df886144e754ffd4955bed08a048)
and release build manifest identify the delivered artifact. Synthetic integration,
unit tests and private installed-package loading do not establish real provider
login, human screen-reader acceptance or every physical GPU configuration.
