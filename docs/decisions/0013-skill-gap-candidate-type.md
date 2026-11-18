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
  `kind: "route-miss"` **and** it comes from the `route-miss` source. For any other
  source (a transcript, an ai-memory export, a custom one) the field is ignored and the
  record is typed like any other, so a record cannot declare itself a gap. Words in the
  text never choose the type.
- The `route-miss` source (`engine/improve/sources/route_miss.py`) rebuilds every
  observation in code from the router's own log. The kind is fixed; the channel is
  `human-user-turn` only when the log line says the router ran with a terminal on both
  ends, and `model-assistant` otherwise, so a prompt composed by an agent can never
  support a gap; the session comes from the producer. Nothing else in a stored line is
  read.
- The producer is `scripts/coacus_route.py`: when no agent matches, it appends a line
  to `docs/temp/improvement/route-misses.jsonl` (git-ignored). It is off unless
  `COACUS_ROUTE_MISS_LOG=1`, because the line keeps the first 200 characters of the
  prompt; the log stops growing at 2000 lines or 1 MB, and a write failure never
  affects the router.
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

- The type stays inert until someone sets `COACUS_ROUTE_MISS_LOG=1` and runs the
  improvement loop with `--source route-miss`.
- A claim is compared after NFKC folding, case folding and whitespace collapse, so
  full-width letters, doubled spaces and capitals of one wording count as one claim; a
  paraphrase is still a different claim.
- A gap routed as a `note` because its evidence was not trusted keeps `downgraded` and
  `original_type` in the stored record, so a reviewer can tell where it started.
- The log is owner-local state. A record can no longer claim a channel or a kind it did
  not earn, but whoever can write the log file can still write three sessions and the
  interactive flag. Structure keeps free text from choosing the type; it is not a
  security control against the owner. The controls are that nothing is applied and that
  a person reviews every proposal.
- The session is the day and the parent process id, so three terminals on one day are
  three sessions, and one terminal reused over several days counts once per day.
- Only the router produces gaps. Other signals of a missing skill (an agent that says it
  found nothing) are not a source and would need their own, with the channel again
  assigned in code.
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
