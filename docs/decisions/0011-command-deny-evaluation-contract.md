# ADR 0011: Command deny evaluation contract

* **Status**: accepted
* **Date**: 2026-11-18
* **Tags**: guardrails, evaluator, deny, fail-closed

## Context

A deny rule with `"match": "command"` compares its patterns with the executable
names a shell string would run. Measuring the evaluator showed three ways a hard
input turned into an allow: a regex fallback that took exponential time on a pattern
with several `*` (the hook then timed out, and a timeout is a mechanism failure that
allows), commands nested deeper than the depth limit or too long to scan (the walk
returned no names, so there was nothing to block), and shell constructs the walk did
not look through (brace groups, process substitution, `eval`, here-strings,
`find -exec`, `env -S`, control keywords).

## Decision

- Resource matching never uses a backtracking regex. `*` is matched by a two-pointer
  scan whose work is bounded by pattern length times value length. A value longer
  than 100,000 characters matches every pattern, and one trailing newline is ignored.
- A command is **unresolved** when it exceeds that size, nests deeper than the depth
  limit (8), or contains a line the lexer cannot parse (an unbalanced quote or a
  quoted argument that spans lines). An unresolved command matches every
  `match: command` policy, so a deny rule fails closed. The cost is a false deny on
  a pathological command; the message names the policy that matched.
- The walk also looks through brace groups and shell control keywords (`if`, `then`,
  `elif`, `else`, `do`, `while`, `until`, `!`, `coproc`), process substitution,
  `eval`, here-strings to a shell, `find -exec/-execdir/-ok/-okdir` and
  `env -S/--split-string`. These only add candidates: against the previous walk,
  random inputs lose no executable name except the bracket tokens that are now
  separators.
- An unknown or misspelled `decision` value denies.
- Variable indirection (`x=name; $x`) is undecidable without running the shell and
  stays out of scope; the corpus pins it as a known gap.

## Consequences

- A command deny rule is best-effort, never a sandbox. This record narrows the gap;
  it does not close it.
- Two known false positives remain: a prefix wrapper reads its first words as
  candidates, so `sudo grep NAME file` still matches. They are pinned in the corpus.
- The tests in `tests/test_guardrail_command_corpus.py`,
  `tests/test_guardrail_command_constructs.py` and
  `tests/test_guardrail_fail_closed.py` lock the contract, including the shipped
  browser policy over the real catalogue.

## Alternatives considered

- Keep the regex fallback with a timeout: a timeout still allows, so rejected.
- Treat an unresolved command as allow with a warning: that is the failure being
  fixed, so rejected.
- Execute the command in a sandbox to learn what it runs: out of scope and unsafe.
