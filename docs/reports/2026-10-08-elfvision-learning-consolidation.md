# Elfvision learning consolidation

## Scope and source authority

Transfer reusable practices into the GNOME extension skill rather than copying
the product's task history or inventing cross-desktop support. Source authority:
[Elfvision at the delivered commit](https://github.com/dandgabr/elfvision/tree/93b17f5192290e10de834125061735f3b9e3a270),
observed on 2026-10-08. The source records distinguish controlled native replays,
actual installation checks and limitations; their historical observations are not
new provider-login or physical-GPU verification in this Coacus task.

## Canonical destinations

- `references/native-preferences-lifecycle.md`: presentation is not ownership;
  verify action, saved IDs and visible rows, then actual signal disconnection.
- `references/accounts-and-api-reporting.md`: session identity can change within a
  boot; recover transport admission under shared authority while preserving fences.
- `references/verification-and-release.md`: preserve persistent IDs and settings
  through public renames; inspect published assets and distinguish disk from loaded
  code; exercise account admission during upgrade tests.
- `references/native-layout-and-effects.md`: whole-popup bounds, independent
  display state, shadow/scrollbar clearance, individual theme variants, effective
  native fonts, dynamic reading protection and honest performance measurements.

All paths above are relative to
`knowledge/skills/engineering/practices/gnome-shell-extension-development/`.
The skill entry links the new lifecycle reference; generated discovery and authored
provenance are refreshed through the repository commands, never edited manually.
Existing historical source links retain their commit identity under Elfvision's
renamed repository.

## Behavioral baseline and forward evaluation

A read-only skill auditor received the previous skill and public pre-fix source
fixtures, with three tasks: diagnose ineffective ordering arrows despite a green
test; recover same-boot session coordination without account loss; deliver a public
rename/update when installed and running versions differ.

The baseline found the vacuous manually assigned order assertion and recommended
visible-row/action coverage. It did not identify premature `unmap` disposal and
suggested handler counts without proving native signal disconnection. It recognized
the stale GUID and need for shared recovery authority but had no concrete
parent-held file-lock technique. Release/identity guidance was already substantially
correct; that scenario is retained as regression coverage, not claimed as a new
capability.

A fresh read-only auditor received the updated skill and the same pre-fix fixtures,
without the baseline's proposed diagnoses. It identified `unmap` disposal, manual
expected-order assignment and bookkeeping-only cleanup in the actual source. It
also traced the boot-specific GUID pin's rejection before admission and verified
the new shared-lock guidance against the delivered implementation and primary
descriptor/lock documentation. No technical blocker was found in the additions.

The authoring audit also flagged the existing discovery description and narrative
opening; both were rewritten as trigger conditions and execution constraints. Its
suggestion to relocate the remaining main-body rules is deferred: these pre-existing
rules passed the repository's enforced word budget, and wholesale restructuring
would require broader invocation evaluation than this targeted learning transfer.
New depth remains in disclosed references.

This is a qualitative, controlled authoring evaluation, not a statistical model
benchmark. It does not prove behavior in every harness or constitute a rerun of
Elfvision's native/provider tests. The fixtures contain public source only; no
credential store was read for this task.

## Verification

Commands run on the edited Coacus tree:

```text
python3 scripts/coacus.py refresh
python3 scripts/coacus.py generate
python3 scripts/coacus.py validate
python3 scripts/coacus.py check
python3 scripts/coacus.py completeness
python3 -m unittest discover -s tests
git diff --check
```

Generation, validation, drift checking, completeness and the deterministic suite
passed. Validation retains pre-existing body-size warnings in
`superpowers-subagent-driven-development` and `superpowers-writing-skills`, outside
this change. Negative-fixture error output within the deterministic suite is
expected; its final unittest result is the outcome, not an isolated diagnostic.
