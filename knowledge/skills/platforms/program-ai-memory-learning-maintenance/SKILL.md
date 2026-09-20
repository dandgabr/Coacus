---
name: program-ai-memory-learning-maintenance
description: Specialist in the maintenance, consolidation, and curation of the ai-memory knowledge base, covering consolidation of observations into the wiki, session self-improvement, auditing (linting), purging of cold pages, and feedback processing.
metadata:
  type: management
  phase: maintenance
  tools:
    - ai-memory
---

<!-- ai-memory-managed: routing-skill -->

# ai-memory Learning, Consolidation & Knowledge Maintenance

This skill guides the governance, consolidation, and cleanup procedures for the [ai-memory](https://github.com/akitaonrails/ai-memory) knowledge base. It enables turning raw observations from previous sessions into structured knowledge, identifying contradictions, and eliminating obsolete data.

---

## 🧰 Tools in This Cluster

- `memory_consolidate`: Compiles raw observations from a completed session into thematic wiki pages on demand.
- `memory_auto_improve`: Reviews recent sessions for lessons learned and proposals for durable project rules.
- `memory_lint`: Audits the project knowledge base for contradictions, outdated rules, and pages flagged via feedback.
- `memory_forget_sweep`: Cleans up pages with an expired TTL and decays un-pinned episodic pages (*dry-run* supported).
- `memory_feedback`: Records a signal for useful (`helpful`), useless (`not_helpful`), outdated (`stale`), or wrong (`wrong`) pages.

---

## 🧹 Maintenance and Curation Practices

1. **Handling Flagged Pages (`feedback_flagged`)**:
   - Pages that received a `stale` or `wrong` signal appear highlighted in the `memory_lint` report. Prioritize updating the page content to restore its technical accuracy; updating the document clears the flag automatically.
2. **Self-Improvement and Continuous Learning**:
   - At the end of complex tasks or development cycles, trigger `memory_auto_improve` to extract durable lessons learned during execution.
3. **Safety and Preview (Dry-Run)**:
   - For purge operations with `memory_forget_sweep`, always run first with a simulation (*dry run*) to inspect what would be affected before confirming the deletion.
