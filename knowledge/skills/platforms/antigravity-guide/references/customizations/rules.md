# Antigravity Rules

Rules are persistent constraints and operating guidance. Rules differ from
skills: a rule shapes behavior within its scope; a skill provides a procedure
that the agent loads when relevant. See the [official Rules guide](https://www.antigravity.google/docs/rules-workflows?tab=ide)
for current locations and size limits.

## Rule frontmatter

Every Markdown rule inside a `rules/` directory needs YAML frontmatter with a
valid `trigger`. Supported values are `always_on`, `model_decision`, `glob`,
and `manual`. `description` is required for `model_decision`; `globs` is
required for `glob`.

```markdown
---
trigger: model_decision
description: Apply these constraints when reviewing database migrations.
---

# Migration Rules

Keep this rule focused on durable constraints.
```

Standalone `AGENTS.md` and `GEMINI.md` files do not use this frontmatter.

## Budgets

The current vendor guide documents a 24,000-byte per-file rule limit and a
20,000-token aggregate budget for active rules. The aggregate rules budget is
separate from the customization budget. Keep always-on rules short and use
`model_decision`, `glob`, or `manual` when the rule does not need to be active
for every task.

Coacus's generated shape-C rule retains a conservative 12,000-character cap.
Its Antigravity on-demand rule is a separate, compact plugin source that routes
to the local Coacus catalog MCP server.
