# Coacus tool mapping — codex

Codex surfaces skills natively and runs no session-start hook, so no bootstrap
is rendered. Skills are discovered from the installed skill paths; ACTIONS
resolve to Codex's own tools at use time.

| Action in a skill | Codex tool |
|---|---|
| Read a file | `read` |
| Create, edit, or delete files | `apply_patch` |
| Run shell commands | `shell` |
| Search files | `grep` / `glob` |
