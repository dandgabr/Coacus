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
  limit (8), needs more than 5,000 steps to walk, contains a line the lexer cannot
  parse (an unbalanced quote), puts an expansion in command position (a word that
  starts with `$`, `$'...'` quoting, brace expansion such as `{a,b}`), or pipes into a
  bare shell that reads its script from stdin. An unresolved command matches every
  `match: command` policy, so a deny rule fails closed. The cost is a false deny on
  such a command; the message names the policy that matched.
- Newlines inside quotes do not split a command, so a multi-line commit message
  parses. The body of a here-document is data unless the command that reads it is a
  shell, in which case it is scanned.
- The walk also looks through brace groups and shell control keywords (`if`, `then`,
  `elif`, `else`, `do`, `while`, `until`, `!`, `coproc`), leading redirections and
  `--`, process substitution, `eval`, here-strings to a shell,
  `find -exec/-execdir/-ok/-okdir`, `env -S/--split-string`, `busybox`, `toybox`,
  `builtin`, `watch`, `runuser`, `su -c`, and a shell started behind a wrapper
  (`sudo sh -c '...'`). These only add candidates: against the previous walk,
  random inputs lose no executable name except the bracket tokens that are now
  separators.
- An unknown or misspelled `decision` value denies.
- Variable indirection (`x=name; $x`) now fails closed because the command name is an
  expansion. Three shapes remain open and are pinned in the corpus: sourcing a process
  substitution (`. <(...)`), the `function name { ...; }` definition, and `env` with a
  combined `-S` option such as `-vS'...'`.

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
