# Blind forward comparison

Baseline: `8ab8e28`. Candidate: `a0bcded3913dbc32e2fa00cd8f7273bb1652ce28`.

Same frozen18 raw inputs, SHA256 `9499c42b4d311975e427897fa3583ae10c0d3d84c5d9b923ef26c1c1f18478ba`. Separate fresh evaluator contexts received their source condition and input briefs, without scoring rubric, implementation plan/diff, audit reports, or the other response. Supervisor manually read both complete transcripts against the pre-recorded criteria.

| Condition | Reasoning pass | Reasoning fail | Executed product cases |
| --- | ---: | ---: | ---: |
| Existing skills8ab8e28 | 18 | 0 | 0 |
| Candidate a0bcded | 18 | 0 | 0 |

No observed regression in these sampled product reasoning tasks. No behavioral improvement is demonstrated because baseline already passed. Expanded candidate procedural detail is not a substitute outcome metric. Source review independently found contradictions outside these minimal probes and rejected a0bcded pending correction; this comparison does not override that review.

Limits: one fresh evaluator per condition,18 cases sharing each context; no replicated/no-guidance controls; no browser, pixels, geometry, product execution or mutation runs. Baseline/candidate transcripts propose verification only. These results neither certify82 style implementations nor identify runtime performance. Later source corrections require bounded review rather than automatically becoming this comparison's candidate revision.
