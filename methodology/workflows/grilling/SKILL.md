---
name: grilling
description: Use when a plan, design or decision has unresolved branches, to interview the user in frontier rounds until every branch is resolved before any work starts.
---

# Grilling

Interview the user about a plan, decision or idea until the design tree is
resolved. Finding facts is your job; making decisions is theirs.

## The design tree and the frontier

- Model the subject as a **design tree**: every decision is a node, and its
  children are the decisions that depend on it.
- The **frontier** is every decision whose prerequisites are already settled —
  the questions you can ask now without guessing at answers you have not heard.
- Work in **rounds**. Ask the whole frontier in one round, then wait.

## Round format

Number every question, give your recommended answer, and let the user answer by
number:

```text
Q1 — <title>: <the decision>
   recommended: <your answer and why>
```

Separate rounds with a horizontal rule.

## Facts versus decisions

- Finding **facts** is your job, never the user's. Dispatch a subagent to look it
  up; do not block the round on it — only the questions downstream of it wait.
- The **decisions** are the user's. Never answer a decision for them.
- Recompute the frontier after each round: new answers expose new questions and
  retire old ones.

## Done

The frontier is empty **and** the user confirms a shared understanding. Until
then, do not act on the plan.

## Red flags

- Asking one question at a time when several are independent — batch the frontier.
- Asking the user for a fact you could have found yourself.
- Acting on a decision the user never made.
