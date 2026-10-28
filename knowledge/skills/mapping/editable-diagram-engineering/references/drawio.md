# draw.io Editable Artifacts

Reviewed 2026-10-27. This is an original Coacus adapter guide, not a vendored
implementation. Source facts refer to the immutable snapshot below.

## Inspect the artifact before editing

Identify all pages and whether each payload is compressed or expanded XML.
Retain page IDs, element IDs, parent membership, geometry, styles and edge
endpoints. Do not equate a node's label with its identity. Use a supported parser
or editor path for the actual format rather than modifying encoded payloads as
if they were ordinary XML.

Before choosing an external operation, record its accepted input, selected page,
compression support, output format and preservation limits. An operation that
supports only an expanded first page is unsuitable for silently synchronizing
an entire compressed multipage document. Offer an explicit supported conversion
or a proposed change while preserving the original.

The examined drawio-skill reconciliation patches the first uncompressed page,
retains matching layout/style and reports certain label conflicts. Do not extend
that evidence to arbitrary compressed pages or general conflict-free merges.
Its view projection uses model metadata and heuristics; a view name such as
security does not establish that every relevant trust boundary was collected.

## Editable export versus visual export

Keep the native file when continuing editing matters. XML export can preserve
the graph; PNG and SVG exports can carry embedded diagram data when that option
is used. Verify the actual file by reopening it and editing a representative
node and relationship. A screenshot or flattened image without embedded data
is not a structural model.

Embedded model data can publish more than visible pixels: inspect metadata,
links, tooltips, hidden pages and labels for unintended disclosure. Use relative
source locators and exclude secrets. Refer to the existing untrusted-content
and privacy procedures instead of treating diagram metadata as safe by default.

## Conversion and image reconstruction

The inspected Mermaid exporter skips compressed pages and maps supported content
into flowcharts. It does not establish lossless roundtrip for UML, C4, BPMN or
other notations. Use the [conversion record](verification.md) and preserve the
original when the target cannot express its meaning or editability.

For a whiteboard photo or legacy image, first extract a proposed graph with
uncertain labels and arrow direction marked explicitly. The upstream raster
reconstruction path consumes an extracted graph; it does not guarantee image
recognition. Keep the image as evidence and resolve ambiguity instead of
manufacturing certainty from an attractive redraw.

Model rules test declarations. A rule about an Internet-to-database edge can
find a declared violation; its absence does not prove deployed isolation.
Rendered overlap, contrast and label clipping require rendered inspection even
when an architecture rule reports success.

## Sources

- [drawio-skill](https://github.com/Agents365-ai/drawio-skill/tree/57270820d3cd71cbdf4fb6b2f7091d4fb37bb019), MIT; source and tests informed this guide, with no runtime success claimed.
- [Model and rules](https://github.com/Agents365-ai/drawio-skill/blob/57270820d3cd71cbdf4fb6b2f7091d4fb37bb019/skills/drawio-skill/scripts/diagram_ir.py#L794).
- [Mermaid exporter](https://github.com/Agents365-ai/drawio-skill/blob/57270820d3cd71cbdf4fb6b2f7091d4fb37bb019/skills/drawio-skill/scripts/drawio2mermaid.py#L43).
- [XML export](https://www.drawio.com/docs/manual/export/export-to-xml/).
- [PNG export](https://www.drawio.com/docs/manual/export/export-to-png/) and [SVG export](https://www.drawio.com/docs/manual/export/export-to-svg/): embedded data is an export choice, not a property of every image.
