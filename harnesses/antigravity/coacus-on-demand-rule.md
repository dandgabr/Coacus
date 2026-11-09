---
trigger: always_on
description: >-
  Routes Antigravity tasks to the complete Coacus catalog through its local MCP
  server, loading only selected skill and agent instructions.
---

# Coacus on-demand router

Before acting on a task, search the `coacus-catalog` MCP server for relevant
skills and agents. Load selected entries with `get` and follow their canonical
instructions. When an agent is selected, load its associated skills as well.
Use `get_reference` only when a retrieved instruction points to a supporting
file. Do not assume the Coacus repository is open in the workspace.
