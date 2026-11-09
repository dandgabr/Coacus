# Glossary format

A glossary pins the project's vocabulary. It is a glossary and nothing else: no
implementation detail, no design, no narrative.

## Entries

- **Be opinionated.** Pick one term and list the rejected synonyms under
  `_Avoid_:`. `**Order** — a confirmed request to buy. _Avoid_: Purchase,
  transaction.`
- **Keep definitions tight.** One or two sentences. Define what the term **is**,
  not what it does.
- **Only project-specific concepts.** General programming ideas (timeouts, error
  types, utility patterns) do not belong, even when the project uses them a lot.
- **Group when clusters emerge** under a subheading; a flat list is fine
  otherwise.

## Lifecycle

- Create the file lazily, when the first term is resolved — not up front.
- Update it as terms resolve, never in a batch at the end.
- Keep a **Flagged ambiguities** section: record a collision that was resolved and
  the meaning that won, so the loser never returns.
  `**backlog** was used for both the tool and the body of work. Resolved: the tool
  is the Issue tracker; backlog is no longer a domain term.`
