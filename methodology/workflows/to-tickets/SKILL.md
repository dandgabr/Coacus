---
name: to-tickets
description: Use when a plan or specification should be broken into a set of tracer-bullet tickets with explicit blocking edges, ready to work in order.
---

# To tickets

Break a plan, a spec or a conversation into tracer-bullet tickets.

## Vertical slices

Each ticket cuts a narrow but **complete** path through every layer — vertical,
never a horizontal slab of one layer. Each ticket is demoable on its own and sized
to fit one fresh context window.

## Prefactoring

When a change is easier once the code is shaped differently, add the prefactoring
as its own earlier ticket: make the change easy, then make the easy change.

## Blocking edges

Each ticket declares the tickets that block it. Order blockers first so the ids
exist to reference. Work the **frontier** — the tickets with no unresolved
blocker.

## The wide-refactor exception

A single mechanical change that breaks thousands of call sites at once cannot land
as a green vertical slice. Sequence it **expand–contract**:

1. **Expand** — add the new form beside the old.
2. **Migrate** in batches sized by blast radius.
3. **Contract** — delete the old form.

Each batch is blocked by expand and blocks contract. If even batches cannot stay
green, they share an integration branch and everything blocks a final
integrate-and-verify ticket.

## Before publishing

Quiz the user on granularity, the edges, and whether to merge or split. Then
publish — one file per ticket when local, or native blocking links on a real
tracker.
