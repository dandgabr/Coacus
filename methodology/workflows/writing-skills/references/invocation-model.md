# Invocation model

How a skill is reached, and why that is a design decision rather than an
afterthought. Adapted for Coacus from the invocation model in the
`mattpocock/skills` collection (MIT).

## Two loads, not one

Every skill spends one of two budgets:

- **Context load** — material always loaded, spending tokens and attention every
  turn.
- **Cognitive load** — the human's cost of remembering that the skill exists. The
  human is the index; this is not a cost to minimise, it is the price of human
  agency.

## User-invoked vs model-invoked

| | User-invoked | Model-invoked |
|---|---|---|
| Reach | the human types its name only; no other skill calls it | the model **or** the human |
| Metadata | human-facing one-liner; trigger phrasing stripped | model-facing; carries the trigger phrasing |
| Pays | zero context load, some cognitive load | permanent context load, buys discoverability |

### The invariant

**A user-invoked skill may invoke model-invoked skills, but it can never reach
another user-invoked skill.** The test for keeping a skill model-invoked is
"could the model usefully reach for this on its own?" — and reuse is the reason to
extract a skill, not the test.

### The carve-out

When a step depends on a user-invoked skill, phrase it as an instruction **for the
human** ("tell the user to run the setup step"), never as a skill call. Only a
model-invoked target is named as something to invoke. Getting this wrong is how a
convention applied to the wrong target reaches many call sites at once.

## In Coacus

Coacus is harness-agnostic: the invocation policy is DATA in the canonical source
and is rendered per harness by the generators, never written as a native tool call
in the body. The canonical frontmatter field and its generated render are tracked
in the plan's backlog; until then, state the intent in prose and keep the body free
of tool names (skill-authoring).

- **One target per call.** A step needing two skills names two steps; it does not
  pack two names into one call.
- **A router skill** is a single user-invoked skill that names the others and when
  to reach for each — the human remembers one name instead of many. It can hint,
  never fire them.
- **Orchestrate, do not duplicate.** A user-invoked skill that only sequences
  others delegates to them; the reusable discipline lives in model-invoked skills.
