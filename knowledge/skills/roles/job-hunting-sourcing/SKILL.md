---
name: job-hunting-sourcing
description: "Specialist in Active Job Mining and Strategic Job Search. Masters Google Dorks for direct ATS portals (Greenhouse, Lever, Workday, Ashby), boolean operators for location and seniority, and direct outreach techniques to hiring managers."
---

# Job Hunting & Sourcing Intelligence (Boolean & ATS Dorks)

This skill establishes advanced intelligence and active job-mining techniques on the internet, letting you find opportunities directly on corporate ATS platforms before they are reposted on aggregators.

---

## 🔍 1. Google Dorks for Direct ATS Platforms

Many companies publish jobs on their own ATS portals before feeding paid platforms. Use the boolean syntaxes below:

| ATS Platform | Search Operator | Example Query |
| :--- | :--- | :--- |
| **Greenhouse** | `site:boards.greenhouse.io` | `site:boards.greenhouse.io ("software engineer" OR "backend") "remote" "brazil"` |
| **Lever** | `site:jobs.lever.co` | `site:jobs.lever.co ("java" OR "spring") "remote" -internship` |
| **Workday** | `site:myworkdayjobs.com` | `site:myworkdayjobs.com "cloud architect" ("aws" OR "gcp") "latam"` |
| **Ashby** | `site:jobs.ashbyhq.com` | `site:jobs.ashbyhq.com "tech lead" "remote"` |

### A. Grouped Multi-Platform Search
```text
(site:boards.greenhouse.io OR site:jobs.lever.co OR site:jobs.ashbyhq.com OR site:myworkdayjobs.com) ("software engineer" OR "developer") "remote" after:2026-08-01
```

### B. Exclusion Filters and Seniority Level
- For mid-level/senior roles without executive leadership:
  `site:boards.greenhouse.io "backend developer" -senior -principal -director -intern`

---

## 🛡️ 2. Source Host Provenance & Anti-Spoofing Verification

When sourcing opportunities from scraped feeds, search results, or candidate leads, verify the authenticity of the target URL before fetching or parsing:

1. **Canonical ATS Apex Domain Verification**:
   - Validate that URLs claiming to belong to major ATS platforms resolve strictly to recognized apex domains:
     - `greenhouse.io` (e.g. `boards.greenhouse.io`)
     - `lever.co` (e.g. `jobs.lever.co`)
     - `myworkdayjobs.com` / `workday.com`
     - `ashbyhq.com` (e.g. `jobs.ashbyhq.com`)
     - `smartrecruiters.com` (e.g. `jobs.smartrecruiters.com`)
     - `workable.com` (e.g. `apply.workable.com`)
   - **Anti-Spoofing Suffix Check:** Enforce strict domain boundary checks. Reject spoofed lookalikes (e.g., `evil-greenhouse.io`, `greenhouse.io.attacker.com`, or `user@greenhouse.io`). If the host does not match a verified ATS or trusted employer portal, tag the source as `⚠ Unverified source host` and route through untrusted content guards.

---

## 👻 3. Employer-Canonical Resolution & Ghost-Job Detection

1. **Employer-Canonical Resolution Over Aggregators**:
   - Job boards and third-party aggregators frequently alter job descriptions, strip official requisition IDs, or obscure salary ranges. Always trace aggregator listings back to the employer's official career portal.
   - Reject search result URLs containing client-side fragment identifiers (`#...`) which point to transient search pages rather than permanent, stable job entities.
2. **Ghost-Job & Stagnation Triage**:
   - **Stagnation Flag:** Flag postings where `posted_date > 30 days` with a warning (`Stale posting: verify team is actively screening`).
   - **Distinguish Expired vs. Unreachable:**
     - *Expired:* The page explicitly displays closure indicators ("This job is no longer available", "Position filled", HTTP 404/410). Mark as permanently closed.
     - *Unreachable:* Transient network timeout, server error (5xx), or bot-filter block (403). Mark as `unreachable` and schedule up to 3 retry attempts over 48 hours before abandoning.
   - **Mass-Posting Consolidation:** Detect duplicate requisition IDs posted across dozens of geographic locations. Consolidate these into a single primary record referencing a multi-region posting.

---

## 🔑 4. Deterministic Deduplication Keys & Referral Discovery

1. **Canonical Deduplication Keys (`job_key`)**:
   - Avoid duplicate tracking entries across multiple boards by generating a deterministic key:
     $$\text{job\_key} = \text{slugify}(\text{company}) + \text{"\_"} + \text{hash}(\text{canonical\_title} + \text{requisition\_id})[:8]$$
2. **Referral Link & Peer Discovery**:
   - For every shortlisted opportunity, construct direct LinkedIn search URLs to locate 1st/2nd-degree connections, engineering leads, or alumni:
     `https://www.linkedin.com/search/results/people/?keywords={company}+"engineering"+OR+"recruiter"`
3. **Pre-Application Clarification Call**:
   - When a posting carries contradictory requirements (e.g. "Entry-level" requiring 5+ years of experience), reach out directly to the listed talent acquisition partner or submit a brief inquiry before customizing the application package.

---

## 📨 5. Direct Outreach Strategy (Cold Outreach)

For competitive roles, supplement the formal ATS application with targeted contact with the Hiring Manager or technical Recruiter:

1. **Locating the Decision-Maker**: Identify on LinkedIn who leads the team for the role (e.g., Engineering Manager, Head of Tech).
2. **Short, Objective Message (Max 75 words)**:
   - Present how your specific experience solves an immediate team bottleneck.
   - Reference the application you submitted on the portal.
   - Provide quick links to your resume and GitHub portfolio.
