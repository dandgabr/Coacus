# Coacus tool mapping — antigravity

Skills name ACTIONS. In this harness they resolve to:

| Action in a skill | Antigravity tool |
|---|---|
| Create or update todos | task artifact |
| Dispatch a subagent | `invoke_subagent` |
| Invoke a skill | `skillPaths` discovery |
| Read a file | `read_file` |
| Create, edit, or delete files | `write_to_file` / `replace_file_content` |
| Run shell commands | `run_command` |
| Search files | search files |
| Fetch a URL | fetch URL |

The bootstrap is delivered through the extension's declared context file
(`contextFileName` → `ANTIGRAVITY.md`) installed via `agy plugin install`; the
content is loaded as-is at session start.
