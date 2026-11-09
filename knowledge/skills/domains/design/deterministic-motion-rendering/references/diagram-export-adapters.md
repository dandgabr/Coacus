# Diagram Export Adapters

Use when exporting an authored diagram animation. Reviewed 2026-10-27 against
[DrawCMS schedule source](https://github.com/drawcms/drawcms/blob/c53c914df2758c0cf105ff56daa8c6b5526e9dc6/src/editor/motion/schedule.ts).
These are adapter lessons, not a maintained exporter or a claim that the
application was executed.

## Inspect any exporter by capability

Identify the editor's time unit, accepted rate representation, sample domain,
endpoint rule, frame cap, per-sample delay and output timing. Compare these with
the delivery contract before choosing an adapter. Some tools produce a final
pose sample for preview without intending an additional playback frame; others
encode every captured sample. Inspect the actual path rather than inferring
behavior from a shared clock or a file extension.

For a different editor, use its documented or observed schedule. If its schema
or export API is unavailable, return a proposed adaptation and the missing
capability; do not translate it through a named product merely to fit an example.
The principles below apply to any editor; this snapshot is a worked case study.

## Worked case: endpoint-inclusive schedule

The inspected `planFrames` accepts positive integer fps. Without a frame cap it
uses `ceil(durationSeconds * fps) + 1`, samples from zero and clamps each sample
to the requested duration. Its equal frame delay is `1000 / fps` milliseconds.
A `maxFrames` cap can truncate the planned samples before the endpoint.

For a one-second scene at 30 fps without a cap, the schedule has 31 samples,
including both endpoints. This differs from an export contract declaring 30
frames indexed 0 through 29. If every sample receives a full output frame delay,
playback duration can differ from the scene's requested duration; encoded GIF
delays may also be quantized. Do not silently remove an endpoint, round a
rational rate to an integer, or change delay to disguise a mismatch.

Record source schedule, desired delivery duration/rate/frame count, endpoint
policy and any conversion. Choose an adapter that supports the requested
contract, or state its limitation and propose a reviewed conversion. Follow
[timeline and sampling](timeline-and-sampling.md) for the Coacus frame-domain
convention and [media review](reproducibility-and-review.md) for inspecting the
actual encoded result. Inspect beginning, endpoint, cuts and any truncated
sequence, not only the reported average frame rate.

## Keep explanation and observation distinct

Ordered story steps and connector motion explain the authored diagram. They do
not establish that messages traveled that path in production. Keep extracted,
inferred, proposed and unknown relations visible in the explanation. Refer to
[editable diagram engineering](../../../../mapping/editable-diagram-engineering/SKILL.md)
for graph identity, authoring state and format-conversion losses. This reference
owns only the export adaptation; notation and live editor changes remain with
the diagram owners.

A static/textual explanation and accessible player controls follow the existing
accessibility owner. Do not require animation when a static diagram already
answers the reader's question.
