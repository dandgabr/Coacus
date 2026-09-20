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
| **Lever** | `site:jobs.lever.co` | `site:jobs.lever.co ("java" OR "spring") "remoto" -estágio` |
| **Workday** | `site:myworkdayjobs.com` | `site:myworkdayjobs.com "cloud architect" ("aws" OR "gcp") "latam"` |
| **Ashby** | `site:jobs.ashbyhq.com` | `site:jobs.ashbyhq.com "tech lead" "remote"` |

### A. Grouped Multi-Platform Search
```text
(site:boards.greenhouse.io OR site:jobs.lever.co OR site:jobs.ashbyhq.com OR site:myworkdayjobs.com) ("software engineer" OR "developer") ("remote" OR "remoto") after:2026-08-01
```

### B. Exclusion Filters and Seniority Level
- For mid-level/senior roles without executive leadership:
  `site:boards.greenhouse.io "backend developer" -senior -principal -director -intern`

---

## 📨 2. Direct Outreach Strategy (Cold Outreach)

For competitive roles, supplement the formal ATS application with targeted contact with the Hiring Manager or technical Recruiter:

1. **Locating the Decision-Maker**: Identify on LinkedIn who leads the team for the role (e.g., Engineering Manager, Head of Tech).
2. **Short, Objective Message (Max 75 words)**:
   - Present how your specific experience solves an immediate team bottleneck.
   - Reference the application you submitted on the portal.
   - Provide quick links to your resume and GitHub portfolio.
