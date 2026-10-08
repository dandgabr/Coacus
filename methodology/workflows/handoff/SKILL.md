---
name: handoff
description: Use when the current session should be compacted into a handoff document so a fresh agent can continue the work in a new session.
---

# Handoff

Write a handoff document summarising the current conversation so a fresh agent
can continue the work.

## Rules

1. **Save outside the workspace.** Write the document to the operating system's
   temporary directory, never into the repository — a handoff is working
   material, not a committed artifact.
2. **Name the next agent's skills.** Include a "Suggested skills" section naming
   the skills the next agent should reach for, with a one-line reason each.
3. **Reference, do not duplicate.** Do not restate what specs, plans, ADRs,
   commits or diffs already capture; cite them by path or URL.
4. **Redact.** Remove secrets, tokens, credentials and personal data before
   writing.

## Sections

- **Goal** — what the work is trying to achieve.
- **State** — what is done, in progress and blocked, with the evidence for each.
- **Next steps** — the ordered actions for the next session.
- **Suggested skills** — the skills to reach for, with a reason each.
- **Pointers** — the paths and URLs that hold the detail.

## Why a handoff, not a summary

A handoff is portable across a harness, a directory or a colleague, and it
preserves the primary source by pointing at it. Prefer it to a lossy inline
summary whenever the next session might not share this context.
