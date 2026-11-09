---
name: career-profile-optimization
description: "Specialist in Professional Profile Optimization (LinkedIn, Upwork, GitHub). Masters LinkedIn Recruiter search algorithms, high-conversion headline formulation, Upwork proposal engineering (two-first-lines rule, JSS management), and GitHub portfolio curation."
---

# Career Profile Optimization (LinkedIn, Upwork & GitHub)

This skill guides the artificial intelligence to optimize the digital presence and positioning of candidates and freelancers on leading professional platforms (**LinkedIn, Upwork, and GitHub**).

---

## 💼 1. Strategic LinkedIn Optimization

LinkedIn Recruiter uses AI-driven semantic search and weighted field indexing.

### A. Title / Headline (The Most Valuable Field)
The title carries an indexing weight up to **5x greater** than other fields:
- **High-Conversion Formula**:
  `[Primary Target Role] | [Specialization / Core Hard Skills] | [Value Proposition or Impact]`
- **Example**:
  `Senior Software Architect | Java 21, Spring Boot, Microservices & AWS | Scaling High-Throughput, Low-Latency Systems`

### B. About Section with Storytelling
- Split it into 3 blocks:
  1. *Hook*: Who you are and the main business/engineering problems you solve.
  2. *Career Highlights*: Key numbers, large-scale projects, and the technology stack you master.
  3. *Call to Action (CTA)*: Areas of interest and contact details for recruiters.

### C. Skills Section
- List between 30 and 50 skills aligned with the target role.
- **Top 3 Pinned Skills**: Pin the 3 most critical skills required in the job postings you care about.

---

## 🚀 2. Optimization for Upwork and Freelance Platforms

On Upwork, the algorithm weighs proposal relevance, niche specialization, and the **Job Success Score (JSS)**.

### A. Profile Title and Overview
- Avoid calling yourself a "Generalist Full Stack Developer". Position yourself as a specialist in the highest-value niche.
- Structure your skills into 3 Tiers (Tier 1: Top 5 differentiators; Tier 2: supporting technologies; Tier 3: auxiliary tools).

### B. Proposals Using the "Two First Lines Rule"
- In the candidate list, the client sees only the first two sentences of the proposal before opening it:
  - **Line 1**: Directly identify the client's problem with a concrete solution proposal.
  - **Line 2**: Immediately demonstrate social proof or a similar project already delivered.
  - Never open with: *"Hello, my name is John and I have 10 years of experience..."*.

---

## 🐙 3. Technical Showcase on GitHub (The Developer's "Workshop")

For technical recruiters and hiring managers:
- **Pinned Repositories**: Pin 3 to 5 projects with high architectural maturity.
- **Production-Grade README**:
  - Objective and business problem solved.
  - Architecture, stack, and main libraries.
  - Clear instructions to reproduce it locally (`docker compose up`).
  - Live demo link when applicable.
  - Badges for test coverage, CI/CD status, and linter.

---

## 🔍 4. Multi-Source Competency Expansion & Grounding Union

When building a comprehensive candidate capability profile (the `/expand` pattern):

### A. Dual-Approach Competency Discovery
Extract capabilities across all local candidate documents (`cv/`, `linkedin/`, `diplomas/`, `references/`, `projects/`, and public GitHub repositories) using two complementary discovery strategies:
1. **Approach A (Direct Syllabus & Exam-Guide Lookup):**
   - For every listed certification, academic degree, or accredited course, map the official syllabus or exam objectives into explicit competencies (e.g. AWS Certified Solutions Architect maps to *VPC Peering, IAM Policies, Multi-AZ RDS, S3 Lifecycle Policies*).
2. **Approach B (Problem-Domain Inference):**
   - For every project, repository, or role, infer the necessary engineering disciplines required to solve that problem (e.g., implementing an e-commerce checkout implies *idempotency, distributed transactions, payment gateway webhooks, PCI-DSS boundaries*).
   - Require explicit citation of the evidence source for every extracted competency.

### B. Cross-Document Consistency Check & 3-Source Grounding
- **Reconcile Discrepancies:** Cross-check dates, job titles, and academic honors between CV drafts, LinkedIn profile exports, and diploma certificates. Flag timeline overlaps or conflicting titles to the user before finalizing the profile.
- **Immediate Same-Turn Write-Back:** When the user confirms or clarifies a missing detail, date, or metric in conversation, immediately persist the verified fact back into the canonical local profile file in the current turn. Do not defer or leave verified facts solely in conversational memory.

---

## 🎭 5. Behavioral Profile Calibration & Repository Privacy Guard

1. **Behavioral Profile Calibration**:
   - Record candidate behavioral assessment data where available (Predictive Index, DISC, CliftonStrengths).
   - Identify energizing tasks (e.g., greenfield architecture, deep algorithmic optimization) versus draining tasks (e.g., legacy maintenance, vendor negotiations).
   - Use this calibration to steer job search filters and ensure authentic cover letter voice matching.
2. **Repository Privacy & PII Pre-Check**:
   - Before writing or committing candidate profile data, resumes, or compensation expectations to disk, inspect Git remotes (`git remote -v`).
   - If the repository points to a public remote repository, warn the operator and ensure that sensitive PII (home addresses, personal phone numbers, salary targets) is routed to `.gitignore`-protected directories.
