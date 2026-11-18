# ADR 0013: Skill-gap candidate type

* **Status**: accepted
* **Date**: 2026-11-18
* **Tags**: improve, candidates, taint, untrusted-content

## Context

The improvement loop turns observations into typed candidates and proposes changes
that a person reviews. It has no way to say "a request matched no skill or agent".
Adding one is risky: a gap is derived from what users and models wrote, so a naive
version would let any text choose the type, store free text, and turn repeated
model output into a request for new skills.

## Decision

- A candidate is a `skill-gap` only when its observation carries the structured field
  `kind: "route-miss"`. Words in the text never choose the type.
- It needs a trusted-channel unit like a `gotcha` or `procedure`; otherwise it is
  staged as a `note`. The list of types that need trust is one constant,
  `taint.TRUST_REQUIRED`, used by the loop.
- On every routing branch, including "improve", a gap needs a trusted unit from at
  least three distinct sessions (`taint.MIN_SUPPORT`, `taint.trusted_sessions`).
  Several channels inside one session count once, and untrusted units add nothing.
- The claim is stripped of control and format characters and hashed in full; only the
  statement is capped at 200 characters. Like every other proposal, the stored record
  keeps `[observation withheld]`, never the text.
- A skill-gap is an ordinary proposal. The loop still never applies anything, and
  promotion stays a human pull request (ADR 0005). No promote command is added.

## Consequences

- The `kind`, the `channel` and the `session_id` of an observation are all read from
  the record, so whoever writes the record can write a convincing gap, including
  three invented session ids. Structure keeps free text from choosing the type; it is
  not a security control. The controls are that nothing is applied and that a person
  reviews every proposal. Assigning channel and session in code at capture is a
  separate change to every source and is recorded as a gap.
- The private snapshot under `.ai-memory/improve-sources/` keeps the raw
  observations, as it does for every type; that is owner-only and unchanged. The
  routing record names the closest catalogue target, which can hint at the subject.
- The routing index describes a skill by its name only, so a gap can be a false gap
  when a skill covers the need under another name. The proposal is advice for a person.
- The runtime ledger still lives under `docs/temp/improvement`, which git ignores;
  moving it outside the repository is a separate change.
- `generate` and `check` still do not import `engine.improve`; a test asserts it.

## Alternatives considered

- Derive the type from text markers: rejected, anyone can write them.
- A new ledger and a promote command: rejected, it contradicts ADR 0005.
- Store the user's wording in the proposal: rejected, it would persist untrusted text
  in the ledger (the private snapshot already holds the raw record).
