# ADR 0009: Absorb external agent patterns as Coacus-native content

* **Status**: accepted
* **Date**: 2026-11-17
* **Tags**: provenance, licensing, untrusted-content, verification, orchestration

## Context

An external project, the `ARTEX` repository, was reviewed for ideas Coacus could
adopt in agents, skills, behaviors and hooks. It is an autonomous
penetration-testing platform written in Go, not a skills framework, so nothing in it
is a drop-in artifact for Coacus. Its value is a set of design patterns.

All of its content (files, pull requests, comments) was treated as untrusted data and
read by a read-only ingestion worker under the `untrusted-content-security` skill.
The worker reported no prompt-injection payload in the files it read. That is not a
guarantee: the source was not checked independently, and every adopted idea is
rewritten rather than copied.

- **Pinned revision**: `https://github.com/BaaRai/ARTEX/tree/6337341602be6aa5860b1e83138f03bdd0b78f71`.
  The URL is for attribution only; agents must not fetch it (see
  `docs/standards/untrusted-content.md`), and any human re-verification reads it as
  untrusted data. It was checked on 2026-11-17 through the GitHub API only, with no
  clone and no execution.
- **License**: the `LICENSE` file at that revision is the GNU Affero General Public
  License v3.0. The upstream's right to license its content was not verified.
- **Lineage**: the repository describes itself as a translation of another project.
  The origin it names returned "Not Found" when queried on 2026-11-17, so the lineage
  and the original license are **reported, not verified**. The claimed origin is
  `Autumn-27/ARTEX`, named here for later re-checking only; it was not fetched.

## Decision

1. Adopt **ideas only**, rewritten in Coacus's own words as standards,
   references, eval scenarios and tests. No code, prompt sentence, distinctive label
   or section ordering from the source is reused. Every adopted idea carries its own
   reasoning or an independent reference; an idea without one is marked provisional.
2. A new `SKILL.md` or `agent.source.md` gets an `authoring` entry from `generate`;
   an edited imported one keeps its imported entry. Every adapted file, of any kind,
   cites this record and `THIRD-PARTY-NOTICES.md` in its own content, with the
   revision and the review date. An `authoring` lock entry does not record upstream
   lineage, and standards, references, evals, tests and helpers have no lock entry.
3. Keep the change data-only. Anything that needs a new engine concept is a separate
   core change with its own record: a model-judged policy evaluator, a protected
   surface manifest, a new ledger status, a change to how the guard handles `ask`.
4. Pin the source revision above. Nothing is fetched from the source at runtime, and
   no URL, executable, workflow or update channel from it is adopted.
5. Before a wave merges, an overlap check (longest shared token run against the
   source files listed below, lowercase word tokens, `difflib`) must show no run of
   eight tokens or more, apart from the exact title of a standard license. Only the
   scores are recorded, in the pull request description, never the compared text.

## Rejected sources

- The offensive-security skills, all Go code, the triage bot that forwards untrusted
  text to an external model, and the installer that pipes a download into a shell.
- Pull request #296, open on 2026-11-17, which rewrites maintainer identity, the
  vulnerability-report channel and the update-check address. Coacus treats it as a
  supply-chain signal and makes no finding about intent.

## Provenance ledger

| # | Source file at the pinned revision | Idea taken, in our words | Coacus name | Scope in Coacus |
|---|---|---|---|---|
| 1 | `agent/data_envelope.go` | Frame untrusted text with a per-use random marker; neutralize the marker if it appears in the data. | untrusted-data frame | Standard section, reference and library helper; defense in depth, never a trust boundary. |
| 2 | `intercept/closed_judge.go` | A model answers fixed closed questions; code decides; unusable answers fail closed. | closed-question judge | Reference only; no schema or evaluator change. |
| 3 | `agent/promptcatalog.go` | Validate a finding against its strongest counter-arguments before reporting; state impact as a ratio. | adversarial gate | Extension of the existing review pipeline and evidence fields. |
| 4 | `agent/coverage_ledger.go` | "No finding" must not read as "clean"; record per-surface outcomes with evidence. | coverage mapping | Mapping table onto existing ledger statuses; no new status. |
| 5 | `server/ask_operator.go` | Stop on a deterministic environmental blocker and ask the operator for one command. | environmental blocker | Refines an existing Coacus rule. |
| 6 | `agent/budget.go` | A child never exceeds the parent's remaining budget minus a reserve; one forced wrap-up. | hierarchical budget | Advisory prose standard. |
| 7 | `RSI.md` | Conditions for any loop that edits its own rules. | self-improvement addendum | Advisory addendum to an existing standard. |
| 8 | `scripts/benchmark/run_bench.py` | The judge differs from the subject; an empty answer is invalid. | independent-judge rule | Eval scenarios and probes. |
| 9 | `server/skill_gaps.go` | Record requests for missing skills. | deferred | Not adopted by this record. |
| 10 | `guard/guard.go` | Command-matching semantics for allow and deny rules. | regression tests | Tests pin that deny rules look through wrappers. |

These paths exist at the pinned revision. Names and summaries are Coacus's own
wording.

## Approval

The maintainer chose to proceed with the lineage marked as reported and unverified,
and approved this record on 2026-11-17, which opens the first content wave.

## Consequences

- Coacus gains rewritten standards, references, eval scenarios and tests for the
  adopted items.
- The engine, harness hooks and default policies do not change in this record.
- Two follow-ups are out of scope and need their own records: enforcing protected
  surfaces for the self-improvement loop, and correcting how the guard handles `ask`.
- If the original project's license is later shown to differ, the affected items are
  reviewed and, if needed, removed.

## Alternatives considered

1. **Import the source files**: licensing, language and dependency cost, and the
   importer only supports the `skills` and `superpowers` sources — rejected.
2. **Adopt nothing**: loses well-reasoned verification and trust-boundary patterns —
   rejected.
3. **Adopt only items with an independent public reference**: safer on lineage, but
   discards useful framing; kept as the fallback if the lineage proves a problem.
