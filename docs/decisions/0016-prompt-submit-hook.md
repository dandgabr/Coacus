# ADR 0016: Prompt-submit hook on Claude Code

* **Status**: accepted
* **Date**: 2026-11-18
* **Tags**: guardrails, events, prompt.submit, claude-code

## Context

ADR 0012 deferred rendering a hook for any event except `tool.pre`, because each
harness needs a verified payload shape, a native hook name in the capability data, and
a rule that no process starts for nothing. `prompt.submit` is the one gate event whose
meaning is clear: block the prompt, or let it through. Claude Code documents it
(https://code.claude.com/docs/en/hooks, resolved 2026-11-18): the stdin JSON carries
the text in `prompt`, `{"decision": "block", "reason": "..."}` stops the prompt and
shows the reason to the user, and the event takes no matcher. `turn.stop` and
`tool.post` stay deferred: a stop block means "keep going", and an observe event cannot
deny, so neither is a rule a policy can express with today's verbs.

## Decision

- A new verb, `prompt`, whose resource is a pattern over the text of the submitted
  prompt, compared case-insensitively (a prompt is prose). It is meaningful only on
  `prompt.submit`; a policy with another verb bound to that event, or a `prompt` policy
  bound to `tool.pre`, never fires, because the guard decides one event at a time
  (ADR 0012).
- The capability data names the native hook: `native` (and `payload`) on the event
  entry in `harnesses/<harness>/harness.json`. Only `claude-code` `prompt.submit` has it
  today. A harness without it gets no hook and answers "no opinion".
- The hook is rendered by the installer, not by `generate`, and only while an enabled
  policy (repository, user directory or generated this run) binds the event. The
  installer adds the entry to the guard fragment with the `tool.pre` command and the
  event swapped. When no policy binds it the entry is added empty, so a re-install
  removes a hook an earlier run left, and the merge no longer leaves an empty event
  array in a user's settings.
- A block answers `{"decision": "block", "reason": <policy message>}` with
  `suppressOriginalPrompt`, so Claude Code does not print the blocked text back; a policy
  with no message gets a generic reason. The text still stays in the transcript and the
  prompt history, which the vendor documents. A payload whose `hook_event_name` is not
  `UserPromptSubmit` is not judged.
- A prompt rule compares after NFKC folding and removal of invisible format characters,
  so full-width letters and zero-width spaces do not dodge it. A prompt is never asked about: no channel reaches a
  person from this hook, so an `ask` degrades to its `on_ask_unavailable` (deny blocks,
  allow lets the prompt through), as on every harness that cannot ask.
- The size cap of the evaluator holds: a prompt over 100,000 characters matches every
  `prompt` rule and is blocked by a deny rule, as an oversize value is for every verb.
  The reason says so and names the cap, because the policy message would point at the
  wrong cause; the vendor discards a blocked prompt, so the paste is lost.

## Consequences

- Nothing changes for an installed policy: they were all `tool.pre`, no shipped policy
  binds `prompt.submit`, and the generated `guardrail-hooks.json` files are unchanged.
- A prompt rule is only as good as its pattern. The harness expands pasted text before
  the hook, which helps a secret tripwire; attachments read later by a tool and text the
  model produces are not prompts. The event also fires for scheduled tasks, `/loop`,
  background subagent reports and messages from other sessions, so a deny pattern can end
  those turns. It is a tripwire, not DLP.
- A pattern is a glob like every other resource: `?` and `[...]` are wildcards, so a prose
  pattern that needs them literally has to avoid those characters.
- Enabling a `prompt` policy after installing needs a re-install, because the hook exists
  only while a policy binds the event (`--verify` reports the missing entry). Disabling
  one leaves the hook until the next re-install, which only costs a process per prompt.
- The hook lives in the user-wide settings and runs the guard by its path. The prompt
  command goes through a small launcher (`@optional` in the template) that runs the guard
  when the file exists and exits 0 with a warning on stderr when it does not, so a moved
  repository or a removed worktree cannot refuse every prompt. The `tool.pre` hook keeps
  the plain command on purpose: a missing guard there blocks the tool, which is the safe
  side for a tool call, and the agent can still answer. A guard that exists but fails
  inside still follows D4 and allows.
  The launcher runs `python -I`, so a file named like a standard module in the project
  the hook starts from cannot be imported in its place; the Windows launcher of this hook
  has it too. The plain `tool.pre` launcher on Windows (`python -c`) does not yet, and the
  decision to harden every hook is still open. The cost: when the guard is gone the prompt rules stop without
  any message the user is likely to see, because Claude Code may show the stderr of a hook
  that exits 0 only in verbose mode (not verified). `--verify` does not yet report a hook
  whose guard file is missing.
- The plugin `hooks.json` and `settings.json` both carry the entry, so the guard may run
  twice per prompt, as it does for `tool.pre`.
- A failure or the 30 s default timeout lets the prompt through (D4). The vendor offers
  `onFailure: "block"` for anyone who wants the opposite.
- This is an explicit exception to D3: a deny policy bound to `prompt.submit` on a
  harness with no native hook still installs and is inert there.
- A deny policy bound to `prompt.submit` on a harness with no native hook still installs
  and is inert there, as ADR 0012 accepted; the installer does not refuse it.
- Another harness needs its own verified payload and a `native` name. Codex documents the
  same event, payload and answer, so the mechanism would carry over, but Codex ignores a
  new non-managed hook until the user trusts it in `/hooks`, and it was not run live, so
  it stays out.
- `turn.stop` (a block keeps the agent going) and `tool.post` (observe only) need verbs
  and semantics and are still deferred, with the rest of ADR 0012's list.

## Alternatives considered

- Render the hook always: one process per prompt for nothing, rejected.
- Render it in `generate`: shipped policies are all disabled, so it would never render,
  and enabling a user policy would then need a regeneration, rejected.
- Treat a prompt as a `read` or `exec` resource: mixes prose with paths and commands and
  the case rule, rejected.
