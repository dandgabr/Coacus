# Antigravity Agent Skills

An Agent Skill is a directory with a `SKILL.md` file and optional references,
examples, scripts, or other assets. Antigravity documents progressive
disclosure: the agent sees skill names and descriptions at conversation start,
then reads a relevant `SKILL.md` when activating that skill. See the [official Skills guide](https://www.antigravity.google/docs/skills?tab=ide)
for current paths and behavior on each surface.

## Authoring

Use YAML frontmatter with a unique `name` and a clear `description` that says
what the skill does and when it applies. Keep the main instructions focused;
place detailed supporting material in the skill's own references and link to
those files with relative paths.

```markdown
---
name: schema-review
description: Reviews database schema changes for compatibility and migration risk.
---

# Review database schemas

Describe the workflow and link any supporting references below.
```

## Coacus catalog access

Coacus's default Antigravity profile stores the complete skill corpus as local
plugin data rather than registering every skill as a native customization. The
compact always-on rule routes tasks through the `coacus-catalog` MCP server:
search for relevant entries, load one selected skill with `get`, then fetch
supporting files with `get_reference` only when needed. The explicit `full`
profile installs skills natively and uses Antigravity's native progressive
disclosure instead.
