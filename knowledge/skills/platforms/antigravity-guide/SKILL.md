---
name: antigravity-guide
description: "Complete guide and canonical reference for Google Antigravity (AGY), covering the Antigravity CLI (agy), Antigravity 2.0 Desktop, IDE, Python SDK, slash commands, keybindings, and the Customization System (Skills, Rules, Plugins, Hooks, Sidecars, and MCP Servers). Use this skill when asked to explain, configure, or customize the Antigravity ecosystem."
---

# Google Antigravity (AGY) Guide, Architecture & Customizations

**Google Antigravity** is an AI-assisted pair-programming platform (*AI-first pair programming*). This skill unifies the operational guide for Antigravity's surfaces with the **Complete Customization System** (Skills, Rules, Plugins, Hooks, and MCP Servers).

---

## 🖥️ 1. Ecosystem Surfaces (Local Documentation)

- **Antigravity CLI (`agy`)**: [`references/cli.md`](references/cli.md) — Slash commands, command-line flags, terminal configuration, and best practices.
- **Antigravity IDE**: [`references/ide.md`](references/ide.md) — Standalone IDE, chat side panels, inline code lenses, and keyboard shortcuts.
- **Antigravity 2.0**: [`references/app.md`](references/app.md) — Parallel desktop application, Chat Canvas, HTML Side Panel (Subagents, Background Tasks, Artifacts, Changed Files, and Persistent Terminals).
- **Antigravity Python SDK**: [`references/sdk.md`](references/sdk.md) — Official SDK for agent hosting, orchestration, and exposing custom tools.

---

## ⚙️ 2. Customization System (Extensibility)

The customization system lets you adapt agent behavior, teach procedures, apply coding rules, and integrate external services:

| Type | Configuration / Directory | Scope | Primary Application | Local Reference |
| :--- | :--- | :--- | :--- | :--- |
| **Rules** | `GEMINI.md`, `AGENTS.md` | Contextual / Hierarchical | Code standards, architecture constraints, and local guidelines | [`references/customizations/rules.md`](references/customizations/rules.md) |
| **Skills** | `skills/<name>/SKILL.md` | On Demand (*Progressive*) | Multi-step procedures, runbooks, tool orchestration | [`references/customizations/skills.md`](references/customizations/skills.md) |
| **Plugins** | `plugins/<name>/plugin.json` | Integrated Package | Unified packaging of skills, rules, and MCP servers | [`references/customizations/plugins.md`](references/customizations/plugins.md) |
| **Hooks** | `hooks.json` | Lifecycle Events | Execution of scripts before/after tool runs | [`references/customizations/hooks.md`](references/customizations/hooks.md) |
| **MCP Servers** | `mcp_config.json` | Tool Integration | Connection to external services via Model Context Protocol | [`references/customizations/mcp_servers.md`](references/customizations/mcp_servers.md) |

---

## 📍 3. Discovery Locations and Load Precedence

1. **Workspace (Project) Customizations**:
   - `.agents/` or `.agent/` folders at the project root (versioned in Git).
2. **Hierarchical Directory Rules**:
   - `GEMINI.md`, `AGENTS.md`, `.agents/rules/*.md`. The agent walks recursively up to the repository root, aggregating the rules.
3. **Global Configuration (Local Machine)**:
   - `~/.gemini/config/` for rules and MCPs shared across every project on the machine.

---

## 🌐 4. Up-to-Date Online Documentation

For news and Vertex AI integrations:
- Main Documentation: `https://antigravity.google/docs`
- Customizations (Skills/Rules/MCP): `https://antigravity.google/docs/skills`
- Changelog: `https://antigravity.google/changelog`
