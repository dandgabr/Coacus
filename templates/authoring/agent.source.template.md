---
name: my-agent
category: software-engineering
description: >-
  Does <what the agent does> when <trigger condition>. Third person,
  trigger-oriented.
skills:
  - knowledge/skills/roles/example-skill/SKILL.md
tags:
  - example
---

# My Agent

Instruction body: the durable behavior contract. Prescribe ACTIONS, never
harness tool names (skill-authoring). Paths must be relative (secrets-portability). Secrets
only as {env:VAR} (secrets-portability). Everything in English (english-only).

## Responsibility boundaries

| Concern | Owner |
|---|---|
| A neighbouring duty this agent does not own | `existing-agent-name` |

State in one sentence what this agent owns and what it does not own
(agent-roles). Every owner in backticks MUST be an existing agent.
