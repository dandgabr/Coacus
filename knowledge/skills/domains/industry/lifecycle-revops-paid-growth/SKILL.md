---
name: lifecycle-revops-paid-growth
description: "Provides customer lifecycle marketing, revenue operations (RevOps), SaaS unit economics (CAC, LTV, NRR, Magic Number), paid acquisition modeling, and email retention architectures based on Brian Balfour (Four Fits), David Skok (SaaS Metrics 2.0), and Mark Roberge (The Science of Scaling). Use when designing email drip sequences, modeling unit economics, tracking pipeline velocity, optimizing ad spend return, or auditing churn cohorts."
---

# Customer Lifecycle, Revenue Operations & Paid Growth

Establish rigorous quantitative models for SaaS unit economics, retention cohorts, pipeline attribution, lifecycle email sequences, and paid acquisition channel efficiency.

---

## 📊 1. Core SaaS Unit Economics & Revenue Formulae (David Skok Framework)

Growth is sustainable only when customer acquisition costs generate profitable lifetime customer value.

### Key Metrics & Mathematical Formulations:

1. **Customer Acquisition Cost (CAC):**
   $$\text{CAC} = \frac{\text{Total Sales \& Marketing Expenses in Period } t}{\text{New Customers Acquired in Period } t}$$

2. **Customer Lifetime Value (LTV):**
   $$\text{LTV} = \frac{\text{Average Revenue Per Account (ARPA)} \times \text{Gross Margin \%}}{\text{Customer Churn Rate}}$$

3. **LTV:CAC Ratio (The Health Gate):**
   - **Target:** $3.0\times$ to $5.0\times$.
   - **$< 3.0\times$:** Unsustainable economics; spending too much to acquire customers or churn is too high.
   - **$> 5.0\times$:** Under-investing in growth; leaving market share on the table.

4. **CAC Payback Period:**
   $$\text{Payback Months} = \frac{\text{CAC}}{\text{Monthly Recurring Revenue (MRR)} \times \text{Gross Margin \%}}$$
   - **Target:** $\le 12\text{ months}$ for SMB/Mid-market; $\le 18\text{ months}$ for Enterprise.

5. **Net Revenue Retention (NRR):**
   $$\text{NRR} = \frac{(\text{Beginning ARR} + \text{Expansion ARR} - \text{Contraction ARR} - \text{Churn ARR})}{\text{Beginning ARR}} \times 100$$
   - **Target:** $> 100\%$ indicates natural compounding revenue from the existing customer base without acquiring new logos. Top-tier SaaS benchmarks achieve $115\%$–$130\%$.

---

## 🔄 2. Customer Lifecycle & Retention Drip Sequences

Lifecycle communication must be triggered by customer telemetry milestones, not arbitrary calendar timers:

```
Sign-up ──► Day 0: Setup Welcome ──► Day 1: First Milestone ──► Day 3: Expansion Tip ──► Day 7: Pro Feature Demo
              (Acknowledge goal)      (Prompt Core Action)       (Celebrate Value)       (Contextual Upgrade)
```

### Event-Driven Email Archetypes:
1. **The Behavioral Nudge:**
   - Trigger: User signed up but did not complete the initial setup within 24 hours.
   - Content: Acknowledge the barrier, provide a 1-minute video or offer human assistance. Do not pitch sales.
2. **The Milestone Celebration:**
   - Trigger: User completed their first pipeline run, sent their first invoice, or created their first database table.
   - Content: Validate the accomplishment with specific metric evidence, suggest the next logical workflow.
3. **The At-Risk Re-engagement (Inactivity Trigger):**
   - Trigger: Telemetry shows active user logins dropped to zero for 14 consecutive days.
   - Content: Highlight new releases or direct outreach from a customer success engineer asking for feedback.

---

## 🎯 3. Paid Acquisition Modeling & Channel-Model Fit (Brian Balfour)

Products do not fit channels arbitrarily; channels dictate product and pricing constraints:

```
ARPU / Price Point
▲
│                                          [Outbound Enterprise Sales]
│                                           Requires high ARPU ($20k+)
│                                           to support SDR + AE comp
│
│                 [Paid Search & Performance Marketing]
│                  Requires medium ARPU ($1k–$10k)
│                  and high search intent (Google Ads, Capterra)
│
│  [Virality / Organic SEO]
│   Low ARPU ($0–$100),
│   Broad market consumer/prosumer
│
└──────────────────────────────────────────────────────────► Market Size & Intent
```

### Channel Efficiency Metrics:
- **ROAS (Return on Ad Spend):** $\text{ROAS} = \frac{\text{Revenue Generated}}{\text{Ad Spend}}$.
- **Blended CAC vs. Paid CAC:** Always separate blended CAC (which includes organic word-of-mouth users) from paid CAC (strictly paid traffic acquisition costs) to prevent subsidized ad budget waste.

---

## ⚙️ 4. RevOps Pipeline Velocity & Lead Routing

Pipeline Velocity measures the speed at which revenue moves through the sales funnel:

$$\text{Pipeline Velocity} = \frac{\text{Number of Qualified Opportunities} \times \text{Average Deal Size} \times \text{Win Rate \%}}{\text{Sales Cycle Length (Days)}}$$

### Tactical Levers:
- Shortening the sales cycle by 15% increases pipeline velocity more effectively than increasing lead volume by 15%, with zero additional ad spend.
- Implement strict SLA agreements between Marketing and Sales: inbound high-intent leads must be contacted within 5 minutes (leads contacted within 5 minutes are $21\times$ more likely to enter the sales pipeline than those contacted after 30 minutes).

---

## 📚 References & Authority

- Skok, David. *SaaS Metrics 2.0: A Guide to Measuring and Improving What Matters*, For Entrepreneurs, 2010–2024.
- Balfour, Brian. *The Four Fits Growth Framework*, Reforge, 2017.
- Chen, Andrew. *The Cold Start Problem: How to Start and Scale Network Effects*. Harper Business, 2021.
- Roberge, Mark. *The Science of Scaling: A Data-Driven Approach to Building a Scalable Sales Engine*. John Wiley & Sons, 2015.
