# ADR format

An architecture decision record captures that a decision was made and why. The
value is in the record, not in filling out sections.

## When to write one

All three must hold, or skip the record:

1. The decision is **hard to reverse**.
2. It is **surprising without context**.
3. It is the result of a **real trade-off**.

A reversible, obvious or forced decision does not need an ADR.

## Shape

A one-paragraph record is enough:

- **Title** — the decision, in the imperative ("Use a token bucket for the rate
  limiter").
- **Context** — the forces that made it a decision.
- **Decision** — what was chosen.
- **Consequences** — what it costs and what it makes easy, including the options
  it forecloses.

Create the decision directory lazily, when the first record is needed. Keep the
records where the project already keeps its committed decision records.
