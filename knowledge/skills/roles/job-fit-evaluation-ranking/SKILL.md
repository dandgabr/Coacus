---
name: job-fit-evaluation-ranking
description: >-
  Provides structured job-fit scoring, pre-scoring eligibility and language gates, multi-dimensional weighted rubrics, and batch shortlist ranking. Use when evaluating job postings against candidate profiles, scoring job compatibility, or ranking active opportunities.
---

# Job-Fit Evaluation & Ranking

This skill defines the analytical framework for evaluating job opportunities against candidate profiles, applying deterministic elimination gates before scoring, calculating multidimensional weighted fit scores, and managing batch shortlist queues.

---

## 🚫 1. Pre-Scoring Deterministic Hard Gates

Before expending computational or model effort on scoring, every job posting must pass two non-negotiable elimination gates:

### A. Eligibility Gate (Legal & Work Authorization)
- Review citizenship, security clearance, and visa sponsorship requirements verbatim from the posting.
- **Rule of Strict Interpretation ("Silence is not permission"):** In government, defense, aerospace, financial institutions, and graduate programs, the absence of explicit sponsorship language indicates sponsorship is not offered.
- Distinguish between general right-to-work and specific constraints (e.g. valid work authorization versus non-extendable student visa hourly limits).
- **Outcomes:** `PASS`, `FLAG` (ambiguous phrasing requiring pre-application inquiry), or `FAIL` (immediate veto; archive job without scoring).

### B. Language Gate (Operational Working Proficiency)
- Compare the required operational working language of the team (which may differ from the language the job posting was authored in) against the candidate's verified language proficiencies:
  - `PASS`: Candidate holds verified native, bilingual, or professional working proficiency (C1/C2 or fluent).
  - `FLAG`: Posting requests professional fluency while candidate profile indicates intermediate or conversational competency (B1/B2). Cite the exact requirement and ask operator for confirmation.
  - `FAIL`: Posting mandates a working language entirely absent from the candidate's profile. Issue an immediate veto.

---

## ⚖️ 2. 5-Dimension Weighted Evaluation Rubric

When both hard gates pass, compute an overall fit score ($0 - 100\%$) across five structured dimensions:

| Dimension | Weight | Evaluation Criteria |
|:---|:---:|:---|
| **1. Technical Skills Match** | **30%** | Overlap between mandatory/preferred tech stacks, libraries, architectures, and the candidate's verified tools. |
| **2. Experience Match (Functional)** | **25%** | Evaluated by functional scope, team size, scale of systems, and nature of problems solved — **never by literal job title matching alone**. |
| **3. Behavioral & Culture Fit** | **15%** | Alignment with organizational velocity, autonomy expectations, and team collaboration model calibrated against candidate behavioral profiles. |
| **4. Career Alignment & Task Energy** | **30%** | Proportion of daily responsibilities matching the candidate's **energizing tasks** versus **draining tasks**. High alignment with long-term professional trajectory. |
| **5. Location & Logistics** | **Veto / Gate** | Commute feasibility, time-zone overlap (minimum 4-hour working window for remote roles), and travel expectations. Evaluated as `PASS`, `FLAG`, or `FAIL`. |

### Optional Salary Benchmark Index
When salary or compensation bands are disclosed, calculate a compensation index relative to candidate baseline expectations:
$$\text{Salary Index} = \frac{\text{Posting Midpoint}}{\text{Candidate Target Base}}$$
Scores $\ge 1.0$ meet or exceed baseline; scores $< 0.85$ require explicit user flagging.

---

## 📋 3. Batch Shortlist Triage & Queue Management

When evaluating multiple opportunities concurrently (the `/rank` pattern):

1. **Isolated Subagent Scoring**:
   - Evaluate each posting independently in an isolated context to eliminate cross-posting bias.
2. **Urgency & Deadline Tie-Breaking**:
   - In cases of comparable fit scores, prioritize roles with imminent application cutoffs (`deadline <= 7 days` tagged with `🔥 Deadline`).
3. **Automated Sweep (`sweep`)**:
   - Filter out postings older than 60 days or confirmed closed before presenting active recommendations.
4. **Empirical Model Calibration**:
   - When 3 or more final recruitment outcomes are recorded (`interview`, `offer`, `rejected`), compare real recruiter conversion against predicted fit scores to calibrate dimensional weights.
