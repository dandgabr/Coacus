# The closed-question judge

Adapted from design patterns recorded in ADR 0009 (see `THIRD-PARTY-NOTICES.md`,
revision `6337341602be6aa5860b1e83138f03bdd0b78f71`, reviewed 2026-11-17), rewritten
in Coacus's own words.

**Status: reference only.** Coacus ships no policy key, schema field or evaluator
path for a model-judged decision. Running a model while a policy is evaluated is a new
kind of evaluation, so implementing it is a core change that needs its own record.
This page describes the pattern so a policy author can reason about it.

## The pattern

A guard sometimes needs a judgment that a pattern cannot make. Instead of asking a
model "should this call run?", split the work:

1. The policy fixes a short list of closed questions, each answerable with `yes`,
   `no` or `unknown`. Example questions: does the call only read? Could it delete or
   overwrite data? Does it reach a host outside the declared scope?
2. The model answers each question about one call. It never decides.
3. Code turns the answers into a decision with a fixed table. Any `yes` on a
   destructive question denies; anything the table does not cover goes to the
   failure rules below.

The questions belong to the policy author. They are never built from the content
under review, because content that writes its own questions controls the judge.

## Failure rules

Use the two failure domains already defined in the
[lifecycle guardrails standard](../../../../../../docs/standards/lifecycle-guardrails.md):

- An answer that is missing, empty, malformed or `unknown` is a **decision failure**.
  The default for a decision failure is `deny`.
- The judge process crashing or timing out is a **mechanism failure**. By design a
  mechanism failure allows the call and surfaces an advisory, so a broken helper
  never blocks a session. Record this as a known residual risk of the pattern.
- "Ask the human" only works on a harness that can ask. Where it cannot, the
  decision degrades to the policy's `on_ask_unavailable` value, which defaults to
  `deny`.

## Handling the text under review

The call, its arguments and any file excerpts are untrusted content. Put them in an
[untrusted-data frame](../../../../security/operations/untrusted-content-security/references/untrusted-data-frame.md)
before the judge reads them, and treat the answers as selection data: an answer is
never authorization by itself.

## Limits

- A judge reduces risk; it does not replace a deterministic deny rule. Keep the
  pattern layer first and the judge as a later, switchable layer.
- Cap the size of what the judge reads. If the arguments are larger than the cap,
  do not truncate them silently; send the call to the failure rules.
- Test the decision table with a fixed set of answers, including empty, malformed
  and `unknown` ones, and assert the result code-side.
