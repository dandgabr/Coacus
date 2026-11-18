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
- Variable indirection (`x=name; $x`), an expansion or a glob anywhere in the command
  word (`blocked${x}bin`, `/usr/bin/blocked*`), a shell that reads its script from
  stdin (`| bash -s`, `| sudo -s`, `xargs -I{} sh -c`) and `source` of a pipe or a
  process substitution fail closed. `$HOME/`, `${HOME}/`, `$PWD/` and `~/` prefixes
  are read as literal so `$HOME/.local/bin/tool` is not denied.
- The `function name { ... }` form, assignment prefixes such as `A+=1` and `a[0]=x`,
  line continuations, `env -vS'...'`, a string argument given to `watch` or `script`,
  and `chroot`, `unshare`, `nsenter`, `strace` and similar launchers are walked.
- A here-document is read the way the shell reads it: its tag is parsed outside quotes
  and arithmetic, its body is consumed before any quote tracking (an apostrophe in the
  body cannot swallow the commands after it), and the body is data only for a known
  data reader (`cat`, `git`, `gh`, `tee`, `echo` and the like); for a shell, `source`,
  `eval` or any unknown reader it is scanned as a script.
- Policies are loaded one entry at a time: a file or an entry that is malformed is
  skipped alone and can no longer switch the other policies off, and a policy that
  raises while matching is skipped on its own. The walk is memoized and capped
  (5,000 steps, 2,000 words) so a hostile command cannot stall or exhaust the hook.
- Tool names are compared without regard to case, `Grep`, `Glob`, `MultiEdit`,
  `NotebookEdit`, `patch` and `WebSearch` are classified, and a multi-file patch is
  checked for every file it names.

## Consequences

- A shell-name rule cannot see inside another interpreter. `python3 -c 'os.system(...)'`,
  `perl -e`, `ruby -e`, `node -e` and similar run any program without a shell word the
  walk can read, and `ssh host 'cmd'` runs it elsewhere. Those need their own rule on
  the interpreter or an allow-list; this record does not claim to cover them.
- A command deny rule is best-effort, never a sandbox. This record narrows the gap;
  it does not close it. Two classes stay out of reach by design: a launcher the walk
  does not know (any program that runs another program from its arguments) and a tool
  the guard cannot classify (an MCP tool, for example), which has no verb and so no
  policy. A fresh review found no shape beyond those after the fixes above.
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
