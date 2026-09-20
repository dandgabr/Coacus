# Tutorials

Step-by-step walkthroughs. Each one is a task you finish, with every command
verified against the repository and its expected output shown. They assume a
checkout and `python3`; run the commands from the repository root.

| Tutorial | You learn |
|---|---|
| [Choose agents manually (Mode M)](routing-manual.md) | Browse the index and validate an explicit agent selection by name or alias. |
| [Choose agents automatically (Mode A)](routing-automatic.md) | Route a prompt to ranked candidates, cap at the governor's slots, add an optional reranker, and make it automatic with the opt-in hook. |
| [Tune the routing lexicon](routing-tuning.md) | Fix a wrong route by editing the curated bilingual triggers, then prove it with the gate. |

For the rules behind these, read [routing](../standards/routing.md). For the
day-to-day command surface, see [usage](../usage.md); installing Coacus into a
harness is [install](../install.md).
