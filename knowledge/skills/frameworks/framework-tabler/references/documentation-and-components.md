# Documentation and Component Contracts

Start with [the documentation index](https://docs.tabler.io/llms.txt), then request the needed page's Markdown mirror, such as [cards](https://docs.tabler.io/ui/components/card.md). Avoid loading the full documentation for a single component. The published documentation can describe a newer release than the consuming application.

Compare the installed package's assets and exported interfaces with the selected example. When public content returns an error or cannot establish release compatibility, inspect the matching tag/commit and local package files. Record what was retrieved and what remains unverified. Never describe a failed request as successful documentation access.

## Representative composition

The inspected source uses a page shell with `.page`, a `.page-wrapper` content region, and a `.page-body` containing the selected container. Cards compose header, body and footer regions. A vertical navigation region precedes the wrapper. Verify these names against the selected release; they are examples, not a frozen universal API.

Use existing utilities and components before adding local CSS. Preserve semantic headings and landmarks rather than copying a demo's content hierarchy blindly. A decorative icon is hidden from assistive technology; an icon-only action still needs an accessible name.

Forms need explicit label relationships, validation messages and reachable submit/error states. A `.table-responsive` wrapper supplies overflow treatment, not sorting, server pagination or accessible selection behavior. Verify those application contracts independently; see [data tables](../../../domains/design/ui-data-tables-dashboards/SKILL.md).

## Documentation extraction lesson

The upstream Markdown exporter obtains example HTML from rendered documentation and preserves code fences. When consuming MDX, avoid discarding component-held examples or exposing documentation-only component tags as application HTML. A fallback to source MDX must be labeled; it may not be equivalent to the rendered example.

Sources reviewed 2026-10-28:
- [Tabler skill](https://github.com/tabler/tabler/blob/7ec9589ba63da56be273a12d9da9b9dfce59f5ee/skills/tabler/SKILL.md).
- [Markdown exporter](https://github.com/tabler/tabler/blob/7ec9589ba63da56be273a12d9da9b9dfce59f5ee/docs/lib/llms.ts).
