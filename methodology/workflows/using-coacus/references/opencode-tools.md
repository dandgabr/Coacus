# Coacus tool mapping — opencode

Skills name ACTIONS. In this harness they resolve to:

| Action in a skill | opencode tool |
|---|---|
| Create or update todos | `todowrite` |
| Dispatch a subagent | `task` |
| Invoke a skill | `skill` |
| Read a file | `read` |
| Create, edit, or delete files | `write` / `edit` |
| Run shell commands | `bash` |
| Search files | `grep` / `glob` |
| Fetch a URL | `webfetch` |

Load skills through the native `skill` tool; it lists and resolves every
catalogued skill by name.
