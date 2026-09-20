// Coacus bootstrap for harness 'opencode' (generated — do not edit).
// Install: copy to <harness config>/plugins/coacus.js. The installer
// substitutes __COACUS_ROOT__ with the repository path; the plugin then
// injects the bootstrap into the first user message with an anti-
// reinjection guard (session-start-bootstrap). Skills are NOT registered
// from the repo root: the harness discovers the installed skills tree
// natively, so registering the repo root would bypass a partial install.

const COACUS_ROOT = '__COACUS_ROOT__';
const BOOTSTRAP = "<EXTREMELY_IMPORTANT>\nYou have Coacus.\n\nThe entry skill content is included below and is ALREADY LOADED \u2014 you are\ncurrently following it. Do NOT load it again through a skill mechanism.\n\n# Using Coacus\n\n<!-- SUBAGENT-STOP -->\nIf you were dispatched as a subagent to execute a specific task, skip this\nskill unless that task explicitly asks you to plan, review, or coordinate.\n<!-- /SUBAGENT-STOP -->\n\n## The rule\n\nBefore you respond to any request \u2014 including asking a clarifying question \u2014\ncheck whether a relevant skill exists and follow it. Skills carry the project's\nproven judgment; skipping them means improvising what already has an answer.\n\n## Priority order\n\n1. Process skills first (planning, debugging, review), then domain skills.\n2. When two skills touch the same work, the more specific one wins.\n3. User instructions outrank every skill; repository rules (`AGENTS.md`,\n   `docs/standards/`) outrank individual skills.\n\n## Red flags \u2014 you are about to rationalize skipping a skill\n\n| Thought | Reality |\n|---|---|\n| \"This is just a small change.\" | Small changes are where unchecked assumptions ship. |\n| \"I already know how to do this.\" | Knowledge is not the same as this repository's conventions. |\n| \"Let me look at the code first.\" | Reading code before loading the skill is how scope drifts. |\n| \"I'll check the skill after this edit.\" | The skill exists to shape the edit, not to audit it. |\n| \"There is probably no skill for this.\" | Check the index; that is exactly what it is for. |\n\n## Session discipline \u2014 single scan\n\nRead `catalog/INDEX.md` and `AGENTS.md` once at the start of the session. Do\nnot re-scan directories per turn; rely on the index and the session's memory.\nIf the index looks stale, regenerate it once, then continue.\n\n## Artifact lifecycle\n\nEvery canonical artifact has one source. Work moves through:\n\n`create (from templates/authoring)` \u2192 `validate` \u2192 `register (generate)` \u2192\n`discover (single scan)` \u2192 `activate (session start)`.\n\nNever edit generated output (`catalog/`, `.agents/`, any `dist/`) by hand \u2014\nchange the source and regenerate.\n\n## Coordination\n\nCap concurrent work at the repository's governor limit and hand off between\nagents with compact TOON payloads. Never spawn ungoverned parallel work.\n\n## Verification \u2014 measure, do not infer\n\nWhen asked whether something is installed, loaded or working, run the command\nthat answers it and quote its output. A count, a path or a status is a fact\nonly when a command produced it in this session.\n\n- Prefer a purpose-built read-only check over `ls`: the installer exposes\n  `python3 scripts/coacus_install.py <harness> --verify`, which prints canonical\n  component counts (skills, agents, hooks), the install root and any drift, and\n  exits non-zero on mismatch. Quote it instead of counting directories.\n- Never extend a path from a sibling that exists. `~/.gemini/antigravity-cli/`\n  existing does not mean `~/.gemini/antigravity-cli/skills/` exists; check the\n  exact path.\n- State a number you did not measure as \"unverified\", or do not state it.\n- If a listing is truncated or errored, say so \u2014 do not fill the gap.\n\n## Harness adaptation\n\nThis skill names actions, not platform tools. The concrete substitution for\nyour harness is provided by the bootstrap's tool mapping at session start.\nIf a mapping is missing, prefer the repository's documented fallback wording\nover inventing a capability.\n\n**Tool mapping for this harness:**\n- create or update todos -> todowrite\n- dispatch a subagent -> task\n- invoke a skill -> skill\n- read a file -> read\n- create, edit, or delete files -> write / edit\n- run shell commands -> bash\n- search files -> grep / glob\n- fetch a URL -> webfetch\n</EXTREMELY_IMPORTANT>\n";
const GUARD = 'EXTREMELY_IMPORTANT';

/**
 * Inject the Coacus entry guidance into the first user message.
 *
 * @param {object} _input - The transform input (unused).
 * @param {{ messages: Array<{ info: { role: string }, parts: Array<object> }> }} output
 *   - The message list to mutate in place; the bootstrap is unshifted onto
 *     the first user message unless the anti-reinjection guard is present.
 * @returns {Promise<void>} Resolves after the (possibly) mutated list is written.
 */
export const CoacusPlugin = async () => ({
  'experimental.chat.messages.transform': async (_input, output) => {
    if (!output.messages.length) return;
    const firstUser = output.messages.find((m) => m.info.role === 'user');
    if (!firstUser || !firstUser.parts.length) return;
    if (firstUser.parts.some((p) => p.type === 'text' && p.text.includes(GUARD))) return;
    const ref = firstUser.parts[0];
    firstUser.parts.unshift({ ...ref, type: 'text', text: BOOTSTRAP });
  },
});
