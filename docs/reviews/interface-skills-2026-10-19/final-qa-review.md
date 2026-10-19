# Independent final QA review — initial candidate

Verdict: REJECT final delivery pending durable-record finalization. No new blocking canonical tooling defect was established in this QA scope. Minor reference correction remains. This is not approval of a later correction revision.

## Revision and scope

Baseline: `8ab8e28d8ea69c9c6653c88cf6777bb08c4278c8`. Candidate diff: `a0bcded3913dbc32e2fa00cd8f7273bb1652ce28`. HEAD remained that candidate during review; root corrections and durable record/tests were concurrently uncommitted. Read current AGENTS, using-coacus, testing/mutation/QA/clean-code instructions, approved plan, changed-file inventory, helper/test implementation, authoring support, representative eval, interface oracle/fixture guidance, temporary fixture probe/results, comparison and durable record. This review independently examined testing/evidence/authorization aspects; it does not claim a second full read of all visual packages or all 22 shared findings.

## Findings, by severity

1. **Major delivery evidence gap, pending root finalization:** `docs/reviews/interface-skills-2026-10-19.json:5` binds candidate source to a0bcded while ongoing corrections differ; line 9 leaves candidate comparison pending. Shared finding entries retain unresolved historical resolution statuses (first at line 1931). Final record needs the actual final source binding and explicit resolution evidence, preserving old review results. A read-only SHA256 check of all 191 listed reviewed-file entries found 10 mismatches against the concurrent tree: art-deco, brutalist-monochrome, calm-quiet-ui, card-based-ui, claymorphism, collage-scrapbook, frutiger-aero body and gloss-components reference, ui-motion-interaction, and coacus-process-conventions. This is expected during correction, but cannot become final exact-source approval. Recheck after stabilization.
2. **Minor stale helper description:** `methodology/workflows/superpowers-systematic-debugging/root-cause-tracing.md:101` calls the helper a bisection script. The new implementation performs sorted sequential execution, as its own docstring accurately states. Replace the support description with sequential search.

## Testing and acceptance traceability

| Acceptance area | Evidence examined | Result and limit |
| --- | --- | --- |
| Truthful diagnostic outcome | find_polluter.py plus its unittest | Empty selection, preexisting pollution, failed runner, clean execution and creation distinguish inconclusive/clean/polluter. Four tests pass. No deletion or content printing; no shell invocation. |
| Deterministic gate without browser | eval validation and test imports | Local eval validation passes; new unit tests use stdlib and no browser. Render execution remains explicit outside CI. |
| Historical review integrity | test_interface_skill_review.py | Three tests pass. Frozen inventory/schema/hash syntax are checked; future unrelated source edits are not forced to retain historical bytes. Actual current-delivery digest checking remains a separate release check. |
| Behavioral comparison | forward-comparison.md and scenario contract | Baseline and a0bcded each 18/18 reasoning passes, zero executed product cases. No demonstrated improvement; comparison correctly does not approve later fixes automatically. Regex is only a routing signal, not behavioral acceptance. |
| Rendered oracle controls | temporary probe/results and canonical fixture instructions | Recorded 24 standalone combinations and six selected controlled defects; no independent browser replay in this review. Computed contrast is explicitly bounded. No corpus-wide mutation score or 82-style certification follows. |
| Authorization and evidence boundaries | verification reference, current debugging diagnostic, review mutation boundary and process-conventions | Explicit preservation of existing authorization, non-secret diagnostic metadata, authorized disposable mutation scope and selected installation targets resolve the relevant previously reported risks inspected here. No unauthorized side effect was executed. |
| Agnostic authoring and references | behavior-validation and worked-comparison routing | Old/candidate blind comparison and passing baseline are explicit; removed Node renderer has no remaining reference found in methodology/templates/catalog/provenance search. Stale polluter description remains above. |

## Executed commands and observed results

All commands ran from the review worktree. No browser, network, credentials, installer, deployment, generated-output mutation or canonical mutation was performed.

- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p 'test_polluter_evidence.py' -v` — exit 0, four tests pass.
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p 'test_interface_skill_review.py' -v` — exit 0, three tests pass.
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/coacus_eval.py validate` — exit 0, `eval scenarios OK`.
- Read-only Python JSON/path/SHA256 comparison — 191 reviewed-file entries, 10 mismatches at the concurrent snapshot described above.
- `git rev-parse HEAD` — a0bcded3913dbc32e2fa00cd8f7273bb1652ce28.

No full-suite, generator, provenance validation, browser, mutation or fuzzing execution is claimed here. Existing root evidence must be assessed at its own recorded revision. Remaining nonblocking helper test opportunities include unavailable runner, dangling symlink target, explicit runner forwarding and deterministic file ordering. No mutation score is claimed for that helper suite.

## Required bounded recheck

Inspect the correction revision, stale reference fix, finalized durable conclusions, exact source digest agreement and final generated/provenance gate evidence. Preserve a0bcded behavioral comparison as historical evidence; explain which unaffected conclusions transfer and which corrected examples received fresh review. Do not make permanent historical-record tests compare against mutable live source bytes.
