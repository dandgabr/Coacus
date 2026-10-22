# Task Loop Mechanics: Dispatch, Review, and Escalation

This reference supplements [SKILL.md](../SKILL.md) with deep operational mechanics for running the subagent task loop, handling edge cases, and executing the fix/breaker protocols.

---

## 1. Implementer Dispatch Contract

### Context Isolation & Handover
- Every task must be dispatched to an isolated subagent context. Never paste accumulated prior-task chat logs or history into the dispatch.
- Supply only:
  1. The role/placement of the task in the project (single line).
  2. The brief path generated via `python3 scripts/task-brief.py PLAN_FILE N`. Instruct the subagent to read the brief first as its binding authority.
  3. Concrete interface signatures or architectural decisions from earlier tasks that are not yet committed or documented in the repo tree.
  4. The dedicated report file path (`…/task-N-report.md`).
- **No-Subagents Contract:** Implementers must never spawn helper agents or secondary reviewers. All reviews are coordinated by the orchestrator controller.

### Handling Implementer Questions & Statuses
- If the implementer asks clarifying questions before starting or mid-flight, answer directly and provide concrete specification details.
- Status triage:
  - **DONE:** Generate review package (`python3 scripts/review-package.py PLAN_FILE BASE HEAD`) and dispatch the task reviewer.
  - **DONE_WITH_CONCERNS:** Inspect flagged doubts. If they affect correctness, resolve them immediately; if they are observations, note them in the ledger and proceed to review.
  - **NEEDS_CONTEXT:** Provide missing inputs and re-dispatch.
  - **BLOCKED:** If context-related, supply context; if reasoning-constrained, escalate model tier; if plan defect, record a ruling in the ledger and re-dispatch. Never force a stuck model to retry without changes.

---

## 2. Task Review & Diff Packaging

### Reviewer Inputs & Attention Lens
- The task reviewer evaluates two non-negotiable gates: **Spec Compliance** and **Task Quality**.
- Inputs provided to the reviewer:
  1. The task brief file (`task-N-brief.md`).
  2. The implementer report file (`task-N-report.md`).
  3. The packaged review diff file (`review-package.py PLAN_FILE BASE HEAD`).
  4. Project-specific Global Constraints from the plan or spec.
- Never dispatch a task reviewer without a packaged diff file. Do not tell reviewers to ignore issues or pre-judge findings.

### Unverifiable Items ("⚠️ Cannot verify from diff")
- When reviewers report requirements that cannot be verified solely from the diff (e.g. cross-task invariants, untouched code paths), the controller must inspect the repo and resolve them.
- If verified as an actual gap, treat it as a failed spec review and route it into the fix loop.

---

## 3. The 5-Round Fix Loop Protocol

When a review returns spec failure, Critical findings, or Important defects:
1. **Deferred Minors:** Minor findings never enter the loop. Ledger them as deferred minors (`Task <N>: minor (deferred): <one-liner>`) for branch-level triage.
2. **Plan-Mandated Conflicts:** If a finding is required by the plan text but flagged as an issue, adjudicate against the spec, record the ruling in the ledger, and instruct the fixer accordingly.

### Round Progression
- **Rounds 1–3 (Resume):** Resume the existing implementer subagent with the open findings list. Context is retained, minimizing re-reading costs.
- **Rounds 4–5 (Escalate):** If findings persist after round 3, dispatch a fresh implementer on a higher-capability model tier with the brief, report file, and full failure history.
- **Fix Verification:** The implementer appends covering tests and command output to the report file. Re-review is strictly scoped using `review-package.py PLAN_FILE FIX_BASE HEAD`.

---

## 4. The Circuit Breaker (Round 5 Cap)

If open findings remain after round 5's re-review, stop dispatching. Adjudicate each open item:
- **Contestable or False Positive:** Park in the ledger: `Task <N>: parked — <finding> — Ruling: <why the code stands>`.
- **Real, Non-blocking:** Park and defer: `Task <N>: parked — <finding> — Ruling: <deferred to post-merge backlog>`.
- **Real and Load-Bearing:** Formulate the minimal viable fix to unblock dependent tasks, ledger the ruling (`Task <N>: Ruling: <finding> — <decision and rationale>`), and pass it into subsequent task dispatches. Stop only if all paths forward are pure conjecture.
