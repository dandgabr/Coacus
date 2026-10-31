---
name: gtm-positioning-strategy
description: "Provides Go-To-Market (GTM) strategy, market positioning, competitive differentiation, value proposition design, and ICP definition based on April Dunford (Obviously Awesome), Geoffrey Moore (Crossing the Chasm), and Jobs-to-be-Done (JTBD). Use when defining product positioning, launching new offerings, choosing target segments, designing pricing packaging, or mapping competitive alternatives."
---

# Go-To-Market & Market Positioning Strategy

Establish rigorous frameworks for product positioning, category design, Ideal Customer Profile (ICP) definition, competitive alternative isolation, and commercial packaging.

---

## 🎯 1. The 5-Component Positioning Engine (April Dunford Framework)

Positioning defines how a product is the best in the world at delivering something that a specific target audience cares deeply about.

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                              THE POSITIONING CASCADE                                   │
├────────────────────────────┬─────────────────────────────┬─────────────────────────────┤
│ 1. Competitive Alternatives│ What would buyers use if your product did not exist?      │
│ 2. Differentiated Features │ Capabilities you have that alternatives lack.             │
│ 3. Value & Benefit Proof   │ What those capabilities enable for the customer.          │
│ 4. Target Customer Segment │ Who cares most about that specific value? (ICP)           │
│ 5. Market Category Context │ Frame of reference making your value obvious.             │
└────────────────────────────┴─────────────────────────────┴─────────────────────────────┘
```

### Component Analysis:
1. **Competitive Alternatives (Status Quo First):**
   - Identify true alternatives: DIY manual spreadsheets, legacy enterprise software, hiring interns, or doing nothing.
   - Do not compare features against direct competitors until customer status-quo alternatives are mapped.
2. **Differentiated Capabilities:**
   - Features, architectural decisions, and integrations that alternatives cannot replicate without structural redesign.
3. **Value Demonstration:**
   - Translate capabilities into business metrics: reduced cycle time, risk mitigation, developer velocity, margin expansion.
4. **Ideal Customer Profile (ICP) Characteristics:**
   - Defining attributes of customers who realize maximum value fastest (e.g., tech stack, regulatory burden, team topology).
5. **Market Category Choice:**
   - *Head-to-head:* Taking on an incumbent in an established market (requires $10\times$ advantage on one metric).
   - *Big fish, small pond (Sub-segment):* Dominating an underserved niche in an existing category.
   - *New category creation:* Defining a completely new paradigm (requires substantial market education budget).

---

## 👥 2. Ideal Customer Profile (ICP) & Buyer Persona Architecture

Distinguish company-level ICP from individual Buyer Personas:

### A. Firmographic & Technographic ICP Matrix
| Criterion | Discovery Trigger | Disqualification Indicator |
| :--- | :--- | :--- |
| **Org Complexity** | Cross-functional dependencies, distributed teams | Single founder, zero compliance needs |
| **Tech Stack** | Modern cloud-native infrastructure, GitOps, CI/CD | Monolithic on-prem legacy with locked egress |
| **Pain Urgency** | Active budget allocated to solve security/performance audit | Exploring solutions casually without timeline |
| **Regulatory Bound** | Subject to GDPR, HIPAA, DORA, PCI-DSS | Unregulated experimental hobby projects |

### B. Decision-Making Unit (DMU) Mapping
1. **Economic Buyer:** Controls budget; cares about ROI, total cost of ownership (TCO), and time-to-value.
2. **Technical Evaluator / Gatekeeper:** Assesses compliance, security, architectural debt, and maintainability.
3. **End User Champion:** Uses the product daily; cares about ergonomic workflows, reduced toil, and friction-free interface.
4. **Executive Sponsor:** Protects the initiative against internal political friction; aligns with board-level goals.

---

## 🚀 3. Go-To-Market Motion Selection

Match product complexity and pricing to the appropriate distribution motion:

```
ACV / Contract Value
▲
│                                          [Enterprise Sales-Led]
│                                           High ACV, Long Cycle, RFP,
│                                           Security Audits, Custom SLA
│
│                 [Product-Led Growth + Sales Assist]
│                  Self-serve adoption with expansion triggers,
│                  PQL detection, usage-based tiers
│
│  [Pure Self-Serve PLG]
│   Zero-touch onboarding,
│   Instant time-to-value,
│   Transparent pricing
│
└──────────────────────────────────────────────────────────► Buyer Complexity
```

### The PLG-to-Enterprise Bridge (Product-Qualified Leads - PQL):
- Define explicit telemetry indicators that signal enterprise readiness:
  - Multi-user workspace creation within 48 hours.
  - Hitting free-tier capacity limits (e.g. data ingest, seat counts).
  - Repeated visits to enterprise security pages (SSO, SAML, audit logs).

---

## 💰 4. Pricing & Packaging Architecture

1. **Value Metric Selection:**
   - The pricing metric must align directly with customer value perception (e.g., active monitored nodes, completed transactions, monthly active users).
   - Avoid charging for vanity metrics or arbitrary user seats when seat gating discourages product adoption.
2. **Tier Structuring (Good-Better-Best):**
   - **Starter / Free:** Friction-free evaluation; single-project constraint; community support.
   - **Pro / Growth:** Uncapped volume; team collaboration; standard integrations; standard SLA.
   - **Enterprise:** SSO/SAML enforcement; custom data retention; dedicated VPC; audit logs; 24/7 SLA.
3. **Grandfathering & Pricing Evolution:**
   - When raising prices, isolate legacy customers with explicit grandfathering terms or phased transition discounts to protect retention metrics.

---

## 📚 References & Authority

- Dunford, April. *Obviously Awesome: How to Nail Product Positioning so Customers Get It, Buy It, Love It*. Ambient Press, 2019.
- Moore, Geoffrey A. *Crossing the Chasm: Marketing and Selling High-Tech Products to Mainstream Customers*. HarperCollins, 1991.
- Christensen, Clayton M. *Competing Against Luck: The Story of Innovation and Customer Choice (Jobs to be Done)*. Harper Business, 2016.
