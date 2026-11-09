---
name: agentic-state-sync-hitl
description: >-
  Provides patterns for human-in-the-loop state synchronization, external signal triage (email/MCP), and local-first workspace projection. Use when synchronizing external inbox feeds, updating local trackers with human confirmation, or projecting local state to third-party MCP workspaces.
---

# Agentic State Sync & Human-in-the-Loop (HITL)

This skill provides the architectural and operational guidelines for integrating external signals (such as email inboxes, calendar events, or MCP connectors) into local-first state repositories while ensuring human oversight, data sanitization, and deterministic execution boundaries.

---

## 📬 1. Idempotent External Signal Triage

When monitoring external streams (such as Gmail, Outlook, or webhook queues) to detect lifecycle updates (e.g. recruitment decisions, support tickets, lead statuses):

1. **Query Scope & Archive Preservation**:
   - Query external feeds with exclusion filters that avoid drafts and outbound messages without excluding labeled or archived mail (e.g., `-in:sent -in:drafts` rather than restrictive `in:inbox`).
   - Many users filter or auto-archive incoming correspondence; the sync process must discover relevant messages regardless of folder location.
2. **Deterministic Deduplication (`processed_message_ids`)**:
   - Maintain a local, append-only log of processed unique message IDs.
   - A message ID is committed to the processed log **only after** all associated actions or human-confirmed changes have been fully persisted.
3. **Full-Body Inspection Over Snippets**:
   - Never classify status or trigger state transitions based solely on subject lines or preview snippets.
   - Fetch and inspect the complete message body to detect subtle distinctions (e.g. an automated interview scheduling link vs. a final rejection notice).

---

## 🛑 2. Semantic Guardrails & Batch HITL Confirmation

Automated agents must not execute critical business decisions autonomously based on external signals.

### Guardrails on State Transitions
- **Sensitive transitions require human action:** When an external signal indicates an actionable outcome (e.g., a formal offer, a legal settlement, or a contract terms change), the agent must classify the event as `offer_received` or `review_pending`. The agent is strictly prohibited from autonomously choosing between `accept` or `decline`.
- **Conflict detection over silent overwrites:** If local state marks an entity with a final terminal status (e.g., `rejected` or `closed`) but an incoming message suggests an active stage (e.g., an invitation to an exploratory call), do not silently overwrite local state. Emit an explicit conflict notice:
  ```text
  CONFLICT: Item "Acme Corp" locally marked [rejected].
  External signal from "recruiter@acme.com" indicates [interview_invitation].
  Action paused: Manual resolution required.
  ```

### Batch Proposal Workflow
When synchronization discovers candidate updates:
1. Compile discovered actions into an interactive tabular proposal displaying the item identifier, current status, proposed new status, source snippet, and confidence rating.
2. Prompt the operator for explicit confirmation before touching files:
   - `all` — Apply all proposed transitions.
   - `<indices>` (e.g. `1, 3`) — Apply only specified transitions.
   - `none` — Discard proposals and leave local trackers untouched.

---

## 🛡️ 3. Unquoted CSV Column-Shift & Injection Defense

When appending user- or third-party-supplied text (such as email subjects, sender names, or contact notes) to local CSV or TSV tracking files:

- **The Column-Shift Vulnerability:** Unescaped commas, semicolons, double quotes, and unhandled newlines (`\r`, `\n`) cause downstream parsers (such as `csv.DictReader` or bash `awk`/`cut`) to split rows across multiple lines or misalign columns. A misplaced comma can silently shift a free-text note into a sensitive `status` or `deadline` column.
- **Sanitization Rule:** Before persisting any external text field into a delimited tracker:
  1. Strip all double quotes (`"`) and carriage returns (`\r`).
  2. Replace newlines (`\n`) and delimiters (`,` or `;`) with a sanitized separator (e.g. ` - ` or space).
  3. Trim leading and trailing whitespace.
  4. Ensure fields containing spaces are safely quoted according to RFC 4180 rules if using comma separation.

---

## 🌐 4. Local-First One-Way MCP Workspace Projection

When projecting local repository state to collaborative cloud platforms (such as Notion, Coda, or Jira via Model Context Protocol tools):

1. **Local Files Are the Single System of Record (SoR)**:
   - The local Git repository is authoritative. Cloud workspaces are secondary read projections.
   - Changes originate locally and flow outbound to the cloud projection, never by bidirectional unstructured syncing that could overwrite local versioned history.
2. **Metadata & Briefing Pages Only (Privacy Preservation)**:
   - Synchronize document references as filenames or relative paths (e.g., `cv_draft_v2.pdf`).
   - Never upload raw, unredacted candidate documents, resumes, or proprietary source files containing Personally Identifiable Information (PII) to third-party cloud workspaces without explicit operator authorization.
3. **Idempotent Upsert Logic**:
   - Tag projected cloud pages with a unique local item hash or slug.
   - Before creating new cloud entries, query existing pages by key to perform updates (`PATCH`), preventing duplicate cards or rows across repeated synchronization runs.
