---
name: coacus-catalog
description: >-
  Discovers and loads canonical Coacus skills and agent instructions from the
  installed local catalog without requiring the Coacus repository as a workspace.
transport: stdio
command: python3
args:
  - coacus_catalog_mcp.py
capabilities:
  tools: true
  resources: false
  prompts: false
requires:
  - Python 3.10+
docs: https://antigravity.google/docs/mcp
author: Coacus
license: MIT
version: 1.0.0
---

# Coacus Catalog MCP

The stdio server exposes a bounded catalog search, exact skill or agent
retrieval, and supporting-file retrieval. It reads a generated index from the
installed plugin and loads canonical text only when requested. It uses only the
Python standard library and does not scan the installed corpus per request.

## Tools

- `search`: return up to eight matching skills or agents by query and kind.
- `get`: return the full canonical source for one exact skill or agent name.
- `get_reference`: return one supporting file confined to that capability's
  installed directory.

Agents returned by `get` include their associated skill names so the caller can
load those instructions separately. Search results are deterministic and
bounded; source content is returned only by exact retrieval.
