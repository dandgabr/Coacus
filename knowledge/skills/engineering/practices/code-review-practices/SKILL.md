---
name: "code-review-practices"
description: "Provides constructive code review practice based on modern review-culture literature, covering review goals and adoption sequencing, great pull-request anatomy (title, description, prefixes, labels), team working agreements, review automation and gate checks, objective and specific comment patterns, review anti-patterns (lazy, mean, shape-shifting, stringent), emergency playbooks, metric pitfalls and human-AI review collaboration. Use when reviewing pull requests, designing a team review process, or improving review culture and throughput."
---

# AI Skill: Constructive Code Review

This skill guides the AI to run and improve code review as a socio-technical system: fast enough to route around, rigorous enough to matter, and humane enough to keep contributors. It synthesizes review-culture practice from Braganza's constructive-review literature.

---

## 🧭 When to Activate

- Authoring or reviewing a pull request.
- Designing or auditing a team's review process, templates or automation.
- Resolving review disputes or improving review culture and latency.
- Defining emergency bypass procedures or review metrics.
- Configuring human-AI review collaboration.

---

## 🎯 Goals and Adoption Sequence

- Five candidate goals: finding bugs, codebase stability and maintainability, knowledge transfer, mentoring, and recordkeeping.
- Adopt one goal at a time: start with stability/maintainability until review is habitual, then layer recordkeeping (PR preparation habits, prefixes, labels), then the rest.
- Select tooling by SCM, project-management and CI/CD integration plus review workflow features.

---

## 📦 Great Pull-Request Anatomy (Author Duties)

- **Title carries the "what"** — self-explanatory without opening the PR; **description carries the "why"**; labels add machine-readable context.
- **Categorization prefixes** (Conventional Commits style) prime the reviewer's mindset, feed automated changelogs and improve searchability. Reviewer expectations follow the prefix: a fix PR demands reproduction steps, before/after evidence, edge cases and regression tests.
- Small, focused PRs review better than large ones; stacked PRs destroy review scope.

---

## 📜 Team Working Agreement (TWA)

- Convert implicit social expectations into explicit, referenceable policy: response times, PR size norms, comment-vs-blocker conventions, self-approval policy, nitpick handling and consequences.
- Keep it as a living document in its own repository — and make it the first artifact to pass through the team's own review process.
- Anything automatable belongs in tooling; the TWA covers only what cannot be automated.
- Move disputes offline after roughly ten comment exchanges or multi-day stagnation; settle style debates with a ranked attribute list, not opinions.

---

## 🤖 Automation and Gate Checks

- Before human review: formatting, linting, static analysis and tests — fix known issue classes during development so they never reach a reviewer.
- During review: PR templates, validators, automatic reviewer assignment, quality gate checks (lint re-check, static analysis, inclusive-language scan, dependency and vulnerability scanning) that block merge on failure, and stale-review reminders.
- Offload low-stakes checks to machines so human attention concentrates on high-stakes, judgment-requiring problems.

---

## 💬 Effective Comments

- Three traits: **objectivity** (code-focused, not person-focused), **specificity** (concrete evidence, links to conventions), **focused outcome** (the reader knows exactly what happens next).
- **Triple-R pattern** for change requests: Request (what to do) + Rationale (why, with references) + Result (measurable end state or example code). This creates decision artifacts that outlive the PR.
- Vet each suggested change before commenting: filter preference from necessity; park nice-to-haves for team discussion or a follow-up ticket.
- For preference conflicts: professional tone, acknowledge the concern, seek mutual understanding, propose small modifications, find middle ground, escalate to team input. The decision criterion is maintainability for future developers, not winning.
- Compliments are mandatory cultural inputs, not decoration.

---

## 🚫 Anti-Pattern Catalog

- **Lazy:** "LGTM" on a huge diff; chat-channel approvals; buddy-system mutual approval.
- **Mean:** unfiltered rants; subjective insults piled on newcomers — direct retention and inclusion damage.
- **Shape-shifting:** stacked PRs; new commits resetting review state mid-review.
- **Stringent:** manual multi-step pre-review rituals; approval chains through every layer that turn the process into a bottleneck people route around.
- **Emergency abuse:** the hotfix that establishes "urgency voids process".
- **Metric gaming:** approval-rate or cycle-time targets optimized into rubber stamps. Treat metrics as signals, contextualize by complexity and urgency, and set team-level targets rather than individual competition.

---

## 🚨 Emergency Playbook

- Distinct from a runbook: strategic, multi-runbook, human-decision-bearing.
- Contains strict decision trees with few bypass paths, an authorization step, bypass mechanisms each paired with a cleanup task, and next-steps documentation.
- Deliberately tedious and rare — insurance, not shortcut; align it with security and compliance stakeholders.

---

## 🤝 Pair, Mob and AI-Assisted Review

- Pair and mob programming give real-time feedback and shared context but do not replace asynchronous review (independent eyes, durable record, scaling).
- AI reviewers expedite first passes and surface code smells at scale, and can pre-suggest fixes before a PR opens; limits are context and domain understanding, training-data dependence, and human-skill atrophy when over-relied on.
- Working division: AI takes the first pass; humans own architecture, design fit, domain correctness and mentorship. Verify every AI finding before acting on it.

---

## ⚠️ Pitfalls

- Reviewing the diff's shape instead of its consequences; missing the prefix-driven expectations.
- Letting the TWA go stale or exempting leadership from it.
- Skipping verification of AI reviewer findings (false positives and missed vulnerabilities both occur).
- Measuring review speed while quality quietly degrades.

---

## 🔗 Integration with Other Skills

- For the security-focused review lens, see [sast-code-review](../../../security/appsec/sast-code-review/SKILL.md).
- For commit message standards, see [git-conventional-commits](../git-conventional-commits/SKILL.md).
- For process discipline around automation gates, see [devsecops-engineer](../../../security/operations/devsecops-engineer/SKILL.md).
- For requesting review workflows, see [superpowers-requesting-code-review](../../../../../methodology/workflows/superpowers-requesting-code-review/SKILL.md).
