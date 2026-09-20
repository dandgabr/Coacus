---
name: my-mcp
description: >-
  Connects to <service> for <capability>. Use when <trigger condition>.
  Third person, trigger-oriented.
transport: stdio
command: npx
args:
  - -y
  - "@scope/my-mcp"
env_vars:
  - MY_API_KEY
capabilities:
  tools: true
  resources: false
  prompts: false
requires:
  - node>=20
docs: https://example.com/my-mcp
author: Example
license: MIT
version: 1.0.0
---

# My MCP

What the server exposes and when to use it. Names resolve to ACTIONS, never
harness tool names (skill-authoring). Secrets are referenced only as `{env:VAR}` and
declared (by NAME) in `env_vars`; values never live in the repository
(secrets-portability). Transport is one of `stdio`, `http`, `streamable-http`, `sse`.

The generator writes `dist/mcp.json` (server declaration for harnesses) and
`dist/mcp_config.json` (setup metadata for consumers). Keep the body lean; heavy
tool docs go in `references/` beside this file.
