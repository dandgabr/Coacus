# Coacus rules for Command Code

Local behavior rules for Command Code (`cmd`) on this machine. They are installed
to `~/.commandcode/AGENTS.md` (the **user** memory tier, so they apply to every
project) by `python3 __COACUS_ROOT__/scripts/coacus_install.py command-code`, and
only ever written when that file does not already exist.

## Autonomous execution of inspection and read commands

To remove unnecessary interruptions, run diagnostic, inspection and read
commands immediately, without asking, as long as the safety safeguards below
hold. Configure this in `~/.commandcode/settings.json` under
`permissions.allow`, e.g. `Shell(ls:*)`, `Shell(git status:*)`,
`Shell(cat:*)`, `Read(**)`.

Covered categories: navigation and listing (`ls`, `tree`, `find`, `fd`, `pwd`);
identity and environment (`whoami`, `id`, `uname`, `hostname`, `env`, `printenv`);
binary and version checks (`which`, `whereis`, `type`, `command -v`, `--version`);
non-sensitive file reads (`cat`, `head`, `tail`, `grep`, `rg`, `wc`, `stat`,
`diff`, `strings`); hardware and resource inspection (`df`, `du`, `free`,
`lscpu`, `lsblk`, `lsof`, `ps`); read-only git (`git status`, `git diff`,
`git log`, `git show`, `git branch`, `git remote`); passive network diagnostics
(`ip addr`, `ss`, `ping -c`, `curl -I`, `dig`); and package queries (`dpkg -l`,
`rpm -qa`, `pip list`, `npm list`).

## Safety safeguards (always ask or deny)

The exemption above never covers:

- **Secrets and credentials**: `.env` / `.env.*` (except `.env.example`),
  `.secrets`, access tokens, API keys.
- **Cryptographic material**: private keys (`id_rsa`, `id_ed25519`, `*.pem`,
  `*.key`), `~/.ssh/` and `~/.gnupg/`.
- **Destructive or side-effecting commands**: removals (`rm`), edits to system
  files (`/etc/`, `/bin`), remote repository changes (`git push`), privilege
  escalation (`sudo`).

Express these as `permissions.ask` / `permissions.deny` rules (for example
`deny: ["Read(.env*)", "Read(~/.ssh/**)", "Shell(git push --force*)"]`). Deny
beats ask beats allow in every mode.

## Plan gating (mandatory phase-by-phase execution)

Never start executing the phases or steps of a plan without explicit
authorization.

1. **Present the plan in isolation.** When you produce a plan, roadmap or a
   phased task breakdown, structure it clearly (sequential phases, scope,
   deliverables, validation criteria), then **stop your turn immediately** —
   no file modifications, no write/build commands. Ask for approval explicitly
   ("Is the plan above acceptable? May I start Phase 1?").
2. **Execute strictly phase by phase.** One authorization covers exactly one
   phase. Do not chain into the next phase automatically. At the end of each
   phase, present a short summary (what changed, files touched, tests run) and
   stop to request permission for the next one.
3. **Only exception:** run multiple phases continuously when the user states so
   explicitly ("execute all phases", "do it all at once", or similar).
4. **Boundary:** purely exploratory/read commands (see the first section) stay
   autonomous, and so do read/write operations on the optional memory server.
   Anything with a direct side effect on the project's code or repository
   (creating/editing files, commits, builds, tests with side effects) is subject
   to the per-phase gate.

## Skill-first and specialist delegation

- **Consult skills first.** Before producing or refactoring code, check whether a
  relevant skill exists — Command Code auto-loads skills from
  `~/.agents/skills/` — and follow its conventions. Skills carry the proven
  judgment; skipping them means improvising what already has an answer. Process
  skills (planning, debugging, review) come before domain skills, and the more
  specific skill wins.
- **Delegation to specialists.** When a task needs a specific domain (QA,
  DevOps, DBA, security, frontend, backend, architecture, and so on), consult the
  agent inventory in `~/.commandcode/agents/` and prefer the matching specialist
  subagent over a generalist pass.

## Multi-agent governance (advisory)

Subagent concurrency is bounded at **5 active agents, the orchestrator included**
(you plus at most 4 subagents), to avoid provider rate limits (`429`). Command
Code hooks cannot intercept the `agent` tool, so this cap is **advisory**: the
ledger is maintained by the Coacus governor CLI at
`python3 __COACUS_ROOT__/scripts/coacus_governor.py`.

- **Orchestration is the main agent's job.** Command Code subagents cannot spawn
  subagents (the `agent` tool is removed from their toolset), so the main agent
  decomposes, delegates and synthesizes. Choose candidates with
  `python3 __COACUS_ROOT__/scripts/coacus_route.py "<prompt>" --top 4 --max-slots`
  or validate an explicit selection with `--agents a,b`.
- **Before delegating**, prefer `coacus_governor.py status` and stay under the
  cap; wrap delegations with `acquire`/`release` when you want the ledger
  recorded.
- **Rate-limit (`429`, "Too Many Requests", "Rate limit", "Quota exceeded",
  "RPM/TPM exceeded")**: kill the failed instance, mark it `PAUSED`
  (`coacus_governor.py fail <caller>`), wait until the active count drops below
  the cap, then relaunch with exponential backoff (2s, 4s, 8s … up to 60s). A
  non-rate-limit failure is a real `FAILED` — no automatic relaunch.
- **Handoffs** between agents use compact TOON payloads.

## Memory (optional)

If the `ai-memory` MCP server is configured for Command Code, treat it as the
long-term memory: consult history before proposing architectures or wide
refactors (`memory_query`, `memory_read_page`) and record accepted technical and
architectural decisions as ADRs (`memory_write_page`, `pinned: true`). Reading
and writing memory is pre-authorized and is not subject to the plan gate. When
`ai-memory` is not configured, skip this section — nothing else depends on it.
