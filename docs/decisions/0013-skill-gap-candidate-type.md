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
  ends and no harness session marker (`session_markers` in the harness data) was set,
  and `model-assistant` otherwise; the session is the UTC date of the miss, so a gap
  needs the same request on three different dates. The reader trusts the `interactive`
  and `session` values the producer wrote and nothing else in a line, and a
  non-interactive miss never reaches a proposal at all.
- The producer is `scripts/coacus_route.py`: when no agent matches, it appends a line
  to the log. It is off unless `COACUS_ROUTE_MISS_LOG=1`, because the line keeps the
  first 200 characters of the prompt. On POSIX only.
- The log lives in the user's state directory (`COACUS_STATE_DIR`, else
  `$XDG_STATE_HOME/coacus`, else `~/.local/state/coacus`), never in a repository. A
  location that is relative or inside the repository being read is refused, so a
  variable set by a cloned repository cannot point the loop at a log it ships. The
  directory and the file must be owned by the user with no group or other access, and
  are opened without following a symlink or blocking on a FIFO; anything else is
  ignored. Writers take an exclusive lock. When the log reaches 2000 lines or 1 MB the
  oldest half is dropped, and the reader looks at the tail, so the newest lines count.

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
- Threat model: this keeps text an agent was fed, and a record in some other source,
  from becoming trusted evidence without a person at a terminal on three days. It does
  not stop an agent that has a shell and means to forge: the environment switch is the
  agent's to set and it could append to the log or edit a policy just as well. The terminal
  test is a heuristic: a harness that runs commands under a pseudo-terminal and sets no
  session marker passes it, so ordinary use of such a harness on three dates can produce a
  trusted gap. The controls are that nothing is applied and that a person reviews every
  proposal; a real user-turn signal needs a prompt hook (ADR 0012, rendering deferred).
- The session is the UTC date, so the same request over three dates counts as three,
  and a burst of misses in one date counts once; three misses around midnight can span
  about a day.
- The log keeps a raw prefix of a prompt and nothing redacts a secret typed into one;
  that is why it is opt-in, short, private and capped. Running the loop twice over one
  log proposes the same gap twice, as it does for any source read twice.
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
