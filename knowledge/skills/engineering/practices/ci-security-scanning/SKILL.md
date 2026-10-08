---
name: ci-security-scanning
description: >-
  Provides practice for adding free security scanning to a GitHub repository:
  secrets over the whole history, code scanning, a scanner for each language the
  repository holds and an audit of the workflows themselves. Use when adding or
  repairing CI scanning, pinning actions, choosing between CodeQL's default and
  advanced setup, or deciding whether to suppress a scanner finding or change the
  code.
tags:
  - ci
  - security
  - sast
  - github-actions
  - supply-chain
---

# CI security scanning

Scanning is cheap to add and easy to get subtly wrong: a workflow that was never run
proves nothing, a scanner pointed at the wrong thing stays green, and the workflows
that run the scanners are themselves attack surface. Treat the setup as code that
must be exercised, not as configuration.

For the mechanics of workflows in general, see the
[GitHub Actions skill](../../../platforms/program-github-actions/SKILL.md).

## 1. Choose by what the repository holds

| Holds | Scan with |
|---|---|
| Any history | A secret scanner over the whole history, with the repository's own rules for the formats it handles. |
| Any code | The platform's code scanning, on the default setup, with the extended query suite. |
| Python | A Python security linter. |
| JavaScript | A rule-pack scanner whose packs you checked exist. |
| Shell | A shell linter. |
| Workflows | A workflow auditor: it finds unpinned actions, excessive permissions and injection in expressions. |

Add the dependency updater for the actions and for the scanners' own pinned versions,
with a cooldown (a week) so a newly published, compromised release is rarely the one
proposed.

## 2. Run it locally first, with the CI's versions

- Install the same versions that CI will use, run every scanner over the repository and
  fix what is reported before the first push. A first run that is red because of
  something a local run would have shown wastes a review.
- **Prove the scanner detects.** Plant a fake secret in a copy of the tree and see the
  rules find it; a scanner that was never seen to fire is a hypothesis.
- Keep one script that runs the same commands as CI, skipping a tool that is not
  installed, so the habit costs one command.
- Check that every rule pack, query suite or action exists before relying on it: a
  pack name recalled from memory returned a 404 and failed the whole scan.
- Resolve action and tool versions from the publisher's release data in the current
  session, and pin the commit with the version in a comment, never from memory.

## 3. Harden the workflows themselves

- Pin every action to a full commit. Start every workflow with no permissions and give
  each job only what it needs.
- Do not persist the checkout credentials. Set a timeout and a concurrency group.
- Fetch the whole history for the secret scan, or a leak in an old commit is invisible.
- Pin the scanners' versions in a requirements file the updater understands, and install
  them from it.
- Audit the workflows with the auditor, and give it a token so its online checks run.
- The secret-scanning action is free for a personal account and needs a license for an
  organization: check which one the repository is before it fails.

## 4. One code-scanning setup, not two

An advanced CodeQL workflow cannot upload results while the default setup is on: the
platform rejects them with a clear message, and every language fails. Do not keep both.
Raise the default setup to what the workflow was for (the extended suite and the extra
languages, through the repository's code-scanning API or settings), delete the redundant
workflow and document where the setting lives.

## 5. Fix the code, not the finding

- When two scanners flag the same call, the code is telling you something. A function
  that opens an address from a constant should use an opener that only speaks the
  scheme it needs, so the dangerous scheme is impossible by construction; an annotation
  would only hide it.
- Where a suppression is right, put the reason in a comment above it, and write the
  annotation in the exact form the scanner reads (free text after the rule code can turn
  the annotation into a different, wrong one).
- Verify the fix with a test that tries the dangerous input and sees it refused.
- Inspect findings in tests as well as runtime code. An address substring assertion
  proves presence, not a fixed destination or permitted host. When that is the
  intended guarantee, compare the complete expected constant or parsed destination
  and test hostile prefixes/suffixes where input is accepted. Inspect the production
  opener separately; neither a test-file location nor a fixed runtime constant is
  enough evidence to dismiss the alert.

## 6. The first run on the real branch is a test too

Local runs cannot show everything: a check that passes on your machine can drift in CI
because the machines differ (see the process conventions on reproducing the other
machine). After pushing, wait for **every** workflow to finish, read each failure,
reproduce it from a fresh clone of the pushed commit, fix the cause and push again. Then
confirm the remote branch holds the commit you think it does before saying the change is
ready.

Successful language analysis/upload jobs do not establish a clean security result.
An aggregate alert check can still fail. Read its annotations, rule, path and data
flow; distinguish a runtime defect, a weak security assertion and an inapplicable
query. Fix the appropriate boundary or justify a narrow suppression with evidence,
then verify the alert result for the actual candidate commit rather than counting
green analysis jobs.
