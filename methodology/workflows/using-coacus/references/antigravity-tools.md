# Coacus tool mapping — antigravity

Skills name ACTIONS. In this harness they resolve to:

| Action in a skill | Antigravity tool |
|---|---|
| Create or update todos | `manage_task` (task artifact) |
| Dispatch a subagent | `invoke_subagent` |
| Invoke a skill | `Skill` tool (`skillPaths` discovery) |
| Read a file | `view_file` |
| Create, edit, or delete files | `write_to_file` / `replace_file_content` |
| Run shell commands | `run_command` |
| Search files | `grep_search` / `find_by_name` |
| Fetch a URL | `read_url_content` |

The bootstrap is delivered as an always-on **rule** (`coacus-rule.md`,
`activation: always_on`) shipped with the plugin, or via a `PreInvocation` hook
returning `injectSteps` with an `ephemeralMessage`. Plugins activate by
directory (`.agents/plugins/` or `~/.gemini/config/plugins/`) or
`agy plugin install <dir>`; the `plugin.json` manifest accepts only `name` and
`description`.
