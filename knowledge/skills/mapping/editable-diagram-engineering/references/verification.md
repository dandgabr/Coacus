# Editable Diagram Verification

Reviewed 2026-10-27. This acceptance procedure is an original Coacus convention.
Choose representative checks from the change, notation and actual tool scope;
report results as observed, not run or not applicable with a reason.

## Separate evidence layers

| Layer | What to check | What it does not prove |
|---|---|---|
| Parsing and schema | Supported version, valid structure and preserved supported extension fields | Correct architectural meaning |
| Model consistency | IDs, endpoint resolution, membership, notation constraints and scope | Actual deployment or runtime traffic |
| Rendered output | Labels, relationship direction, clipping, overlaps, contrast and relevant viewing size | Reopenable editability |
| Reopen and roundtrip | Edit representative nodes, edges, containers and presentation state after saving/importing | Lossless conversion of unsupported meaning |
| Runtime evidence | Actual traces, observations or tool readback under named conditions | Unobserved systems, future runs or general conformance |

Cycles, isolated elements and bidirectional relationships can be valid. Check the
chosen notation and intended meaning rather than imposing a generic graph rule.
A dangling endpoint is an integrity defect; a legitimate isolated actor is not
necessarily an orphan to remove.

## Record conversion loss

For each relevant dimension, mark preserved, approximated, flattened, dropped or
unverified, and state the evidence:

- Meaning and notation, relationship types/directions and abstraction level.
- Stable identity, page/container hierarchy and endpoint membership.
- Geometry, edge routing, typography and assets.
- Editability, metadata, links, tooltips, animation and ordered presentation.

Compare meaning separately from layout movement. Keep the original when a target
cannot express a required feature. Matching screenshots do not prove retained
IDs or editable structure, and reopening successfully does not prove the model's
meaning survived.

## Discriminating probes

- Rename an element while retaining its ID; ensure manually placed neighbors and
  unaffected pages remain intact. Include a conflicting source/manual rename and
  a case with no reliable baseline.
- Give a first-page-only adapter a compressed multipage file; require a scope
  limitation rather than an unsupported whole-document success claim.
- Convert a rich notation to a flowchart, and import a PNG without embedded data;
  verify the loss report and preserve source evidence.
- Reopen a supported document containing extension fields; check they survive.
  Pair it with an unsupported future version and a dangling endpoint.
- Delete a parent with children and edit during an asynchronous asset fetch;
  inspect actual tool guarantees and the readback rather than assuming a lock.
- Request a security view or animated walkthrough; require evidence labels and
  an accessible equivalent, not a claim of deployed security or observed traffic.

Inspect published artifacts for unintended embedded model data and source
metadata. Follow the existing untrusted-content and privacy procedures when
external diagrams, assets or links are involved. Keep checks proportional to the
change and identify tools or renderers that were unavailable.

Static scenario validation checks the scenario's structure. Reasoning evaluations
assess the agent's proposed decisions. Only actual project execution can establish
successful editing, reopening, rendering or export; never report these from a
source review alone.

## Primary references

- [C4 checklist](https://c4model.com/diagrams/checklist): notation, scope and communication.
- [C4 dynamic diagrams](https://c4model.com/diagrams/dynamic): interaction explanations complement structural views.
- [draw.io PNG export](https://www.drawio.com/docs/manual/export/export-to-png/): embedded editable data is optional.
- [DrawCMS document format snapshot](https://github.com/drawcms/drawcms/blob/c53c914df2758c0cf105ff56daa8c6b5526e9dc6/docs/document-format.md): format-specific preservation and version boundaries.
