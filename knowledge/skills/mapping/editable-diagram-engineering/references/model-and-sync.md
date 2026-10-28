# Model and Synchronization

Reviewed 2026-10-27. The contract and reconciliation procedure here are original
Coacus conventions informed by the source snapshots below.

## Meaning, geometry and presentation

Keep semantic identity, properties and relationships distinct from coordinates,
routing and style, and from an authored story or animation. These layers can live
in one native file; separation does not require another source of truth.

For an important element or relationship, record its source locator/revision and
whether it is extracted, inferred, proposed or unknown. Prefer repository-relative
locators. A desired infrastructure configuration is not deployed state; a live
snapshot observes one time and scope; an import dependency is not network traffic.
A security view selected from labels cannot supply missing security evidence.

Use stable IDs independently of display labels. Match renames through source
identity or an explicit mapping rather than similarity alone. Distinguish a
missing element from incomplete extraction, changed scope or an actual removal.

## Reconcile without discarding human work

When available, compare three inputs: the previous source/model baseline, current
manually edited artifact and incoming source/model. Identify semantic changes
separately from moved nodes, routed edges and presentation edits. Preserve
unaffected pages, positions, styles, annotations and format-specific properties.

| Situation | Decision |
|---|---|
| Source changed; current artifact still matches baseline | Propose the source change and retain unrelated manual geometry |
| Artifact changed; source still matches baseline | Preserve the human change unless the task directs otherwise |
| Both changed the same meaning or property | Record a conflict and expose the competing values |
| No trustworthy baseline | Compare what can be established; do not claim a proven three-way merge |
| Element absent from incoming extraction | Check extraction coverage and deletion intent before removal |

No universal source-wins or editor-wins precedence applies. Use the task's
established authority; ask only if an unresolved consequential conflict requires
an owner decision. A recoverable proposed file or patch can make the conflict
reviewable without replacing the live artifact.

## Capability-based adapter selection

For any editor or format, inspect the operations actually available. This is a
capability checklist, not a mandatory shared schema or invented integration API.

| Capability | Establish before relying on it |
|---|---|
| State access | Full document or partial view; pages, groups and hidden content included |
| Identity | Stable IDs or an explicitly reviewed mapping; labels alone are insufficient |
| Editing | Patch versus replacement, supported properties and cascading effects |
| Recovery | Undo, versioned save, export or another recoverable original; do not assume any exists |
| Concurrency | Actual revision/precondition guarantees and their operation scope |
| Persistence | Editable native save/export and what survives reopening |
| Verification | Readback scope, rendered preview and observable losses |

When capabilities are absent, narrow the operation and its claims. A tool with
only image export can supply a preview, not an editable handoff. Without stable
identity, use a reviewed correspondence or surface uncertain matches; without
undo or snapshots, do not promise rollback. If no persistent editable document
is available, supply a proposed artifact in an appropriate supported format or
explain the missing deliverable rather than claiming the live canvas was saved.

Apply this checklist to a third editor without borrowing another product's
command names, schemas, cloud requirements or protection guarantees. Keep any
necessary adapter-specific recipe with verified documentation for that adapter.

## Read, minimal patch, readback

Inspect the tool's actual document, edit scope, deletion semantics and undo
behavior. Prefer targeted changes over replacing an entire document. Snapshot
or otherwise retain a recoverable original before destructive transformations.
Use revision tokens or transactional preconditions only when the tool supplies
them. A save succeeding is not proof that no concurrent human edit was lost.

Read back the affected IDs and their surrounding membership/relationships. If a
human edit makes the basis stale, re-read and reconcile rather than blindly
replaying a replacement. When the tool cannot protect a live update adequately,
return a proposed patch/file with the limitation instead of inventing a lock or
compare-and-swap guarantee.

## Source boundaries

- [drawio-skill snapshot](https://github.com/Agents365-ai/drawio-skill/tree/57270820d3cd71cbdf4fb6b2f7091d4fb37bb019), MIT: useful separation of provenance and geometry; its metadata normalization is not a portable Coacus metadata contract.
- [Reconciliation implementation](https://github.com/Agents365-ai/drawio-skill/blob/57270820d3cd71cbdf4fb6b2f7091d4fb37bb019/skills/drawio-skill/scripts/diagram_ir.py#L1137): adapter-specific scope, not a general merge engine.
- [C4 review checklist](https://c4model.com/diagrams/checklist): reader-oriented structure, notation and relationship clarity.

These are reviewed references, not an adopted upstream ruleset. Recheck the
installed tool and input format before applying a recipe to a project.
