---
name: context7
description: >-
  Provides up-to-date library and framework documentation through Context7.
  Use when a task needs current API references or code examples for a library,
  framework, SDK, CLI tool or cloud service.
transport: streamable-http
remote_url: https://mcp.context7.com/mcp
capabilities:
  tools: true
  resources: false
  prompts: false
docs: https://context7.com
license: MIT
version: 1.0.0
---

# Context7

Hosted documentation server exposing a documentation-resolution tool. Prefer it
over searching when a question concerns a library or framework API. It requires
no secret; the endpoint is public.

This is the framework's **recommended** external dependency: hosted, keyless and
optional. Registering it with a harness is not required — the scripts and
generated artifacts run without it — but the corpus skills assume current
library/framework documentation when a task needs it.
