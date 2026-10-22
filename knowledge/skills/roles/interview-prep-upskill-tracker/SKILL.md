---
name: interview-prep-upskill-tracker
description: >-
  Provides stage-specific interview preparation, application lifecycle tracking, quiet follow-ups, and skill-gap heatmaps for targeted upskilling. Use when preparing for recruiter or technical interview rounds, managing application outcome states, or generating dependency-ordered learning plans from interview gaps.
---

# Interview Prep, Outcome Tracking & Upskill Heatmap

This skill guides stage-specific technical and behavioral interview preparation, application lifecycle and follow-up management, and data-driven upskilling derived from real hiring outcomes.

---

## 🎯 1. Stage-Specific Interview Preparation

Interview expectations shift radically between recruitment rounds. Tailor preparation packages to the active stage:

| Stage | Focus & Evaluator | Core Preparation Deliverable |
|:---|:---|:---|
| **Round 1: Recruiter Phone Screen** | Recruiter / Talent Acquisition (15–30 min) | High-level narrative, motivation, compensation alignment, work authorization, communication fluency. |
| **Round 2: Technical Deep-Dive** | Peer Engineers (45–60 min) | Whiteboard architecture, live coding, concurrency, edge cases, deep defense of project bullets on CV. |
| **Round 3: System Design / Case** | Staff / Principal Architects | Trade-off analysis, scalability bottlenecks, failure modes, CAP theorem trade-offs, database choices. |
| **Round 4: Final / Cultural Fit** | Engineering Director / VP | Cross-functional collaboration, mentorship philosophy, conflict resolution, strategic product vision. |

### The Consistency Brief
Before any interview, compile a **Consistency Brief** linking submitted materials to anticipated room questions:
- *"No claim in the room that isn't on the paper, and every claim on the paper must be defensible in depth."*
- Review the exact version of the CV and cover letter submitted to the employer.
- Prioritize anticipated questions:
  1. Doubts or flags surfaced during previous rounds.
  2. Identified technical gaps from the initial fit score, equipped with honest bridge responses.
  3. Non-negotiable posting requirements.
- **Interviewer Reconnaissance:** Public research on interviewers (recent talks, open-source projects, tech stack blogs) to calibrate examples to their technical domain.
- **Behavioral Roleplay:** Simulated mock Q&A aligned with candidate behavioral profiles (PI, DISC) and the company's communication register.

---

## 🔄 2. Application Lifecycle, Follow-Ups & Stale Sweep

Maintain a clean, auditable record of every submission.

### Canonical Lifecycle States
Track applications through an explicit state machine:
`drafted` $\longrightarrow$ `applied` $\longrightarrow$ `interview` $\longrightarrow$ `offer` $\longrightarrow$ `hired`
*(Terminal branches: `rejected`, `no_response`, `offer_declined`, `withdrawn`)*

### Immutable Application Directory Archiving
Store application artifacts in an isolated per-application directory:
- `job_posting.md` (Sanitized original job description)
- `cv_submitted.pdf` & source (`.tex` / `.typ`)
- `cover_letter.md`
- `consistency_brief.md`
- `outcome.md` (Stage notes, dates, questions asked, feedback received)

### Quiet Follow-Up Protocol
- **Timing:** Trigger follow-up proposals after **10 business days** of silence following an application or round.
- **Length & Tone:** 60–120 words, professional, respectful of recruiter bandwidth.
- **The No-New-Claims Rule:** Never introduce new qualifications, projects, or sudden resume changes in a follow-up note; doing so undermines the credibility of the original application. Reiterate enthusiasm and offer availability for questions.
- **Cap:** Strict limit of **2 follow-up attempts** per opportunity. If silence continues after two follow-ups, transition state to `no_response`.
- **Post-Interview Thank You:** Dispatch a focused 50–100 word thank-you note within 24 hours of each interview round referencing a specific technical discussion from the session.

### Stale Sweep & Model Calibration
- **Stale Sweep:** Batch-resolve applications with no response after 60 days to `no_response`.
- **Calibration Loop:** When 3 or more final outcomes are recorded, analyze conversion rates against predicted fit scores to calibrate future screening filters.

---

## 📈 3. Skill-Gap Heatmap & Targeted Upskill Plans

Turn rejection feedback and screening gaps into a strategic technical curriculum:

### The Skill-Gap Heatmap
- Aggregate identified missing skills across all applied and shortlisted positions.
- Calculate priority score for each competency:
  $$\text{Priority} = \text{Frequency in Postings} \times \text{Average Job Fit Score} \times \text{Recency Weight}$$
- Classify gaps into **Critical**, **High**, **Medium**, or **Low** priority tiers.

### Dependency-Ordered Upskill Plan
Generate a personalized, actionable learning roadmap:
1. **Verified Current-Year Resources:** Recommend authoritative, current primary sources (official documentation, books, accredited courses, RFCs), explicitly rejecting deprecated tutorials.
2. **Personalized Scope (What to Skip vs. Where to Start):** Anchor learning to the candidate's existing strengths (e.g., *"Since you already master PostgreSQL transactions, skip relational fundamentals and focus directly on distributed consensus in CockroachDB/Spanner"*).
3. **Prerequisite-Ordered Sequences:** Order modules with architectural dependencies first, followed by rapid quick wins.
4. **Longitudinal Progress Tracking:** Track closed gaps over time (*Gaps Closed* vs. *New Gaps Emerged*), updating candidate capability profiles as milestones are completed.
