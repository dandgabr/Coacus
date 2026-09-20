# Tutorial — choose agents manually (Mode M)

**Time:** about 5 minutes. **Prereqs:** a checkout, `python3`, and the generated
index present (`python3 scripts/coacus.py generate` if `.agents/routing.json` is
missing). Run every command from the repository root.

Mode M is the manual path: **you** decide which agents run, and the tool validates
your choice instead of guessing. Nothing here spawns an agent — selection only.

## 1. Browse what exists

List every routable agent with its category and one-line purpose:

```bash
python3 scripts/coacus_route.py --list
```

Output is tab-separated: `name<TAB>category<TAB>description`. There are as many
rows as there are canonical agents.

Narrow it down when the list is long:

```bash
python3 scripts/coacus_route.py --list --category cybersecurity
python3 scripts/coacus_route.py --list --grep kafka
```

`--category` filters on the agent's category; `--grep` is a case-insensitive
substring over the name and description. Both compose:

```bash
python3 scripts/coacus_route.py --list --category data-cloud-devops --grep pipeline
```

## 2. Confirm one agent by name

You already know the agent you want; confirm it resolves:

```bash
python3 scripts/coacus_route.py --agents dba-specialist
```

```
dba-specialist	data-cloud-devops
```

Exit code 0 means the name is valid. This is the check to run before you write an
agent name into a plan, a prompt or a hand-off — it turns a typo into an error
instead of a silent no-op.

## 3. Select several at once

Pass a comma-separated list; order is preserved and each name is validated:

```bash
python3 scripts/coacus_route.py --agents "dba-specialist,pentester-agent"
```

```
dba-specialist	data-cloud-devops
pentester-agent	cybersecurity
```

## 4. Use an alias from the lexicon

A curated bilingual trigger works as a shortcut, so you do not have to recall the
canonical name:

```bash
python3 scripts/coacus_route.py --agents "banco de dados"
```

```
dba-specialist	data-cloud-devops
```

Aliases are the trigger terms in
[`knowledge/routing/lexicon.json`](../../knowledge/routing/lexicon.json). A
multi-word alias must match whole (`banco de dados`, not `banco`) — that
strictness is what keeps a generic word from pulling the wrong agent.

## 5. Handle an unknown name

A bad name fails loudly, with suggestions:

```bash
python3 scripts/coacus_route.py --agents "dba-specialst"
```

```
[error] unknown agent 'dba-specialst' (did you mean: dba-specialist, iam-specialist, moodle-specialist?)
```

The command exits non-zero. Correct the name and re-run; the error is the point —
an unknown agent is never dropped silently.

## What you learned

- `--list`, `--category`, `--grep` to discover.
- `--agents` to validate an explicit selection by canonical name or alias.
- Unknown names are errors with suggestions.

Next: [choose agents automatically (Mode A)](routing-automatic.md) when you want
the tool to propose candidates from a prompt.
