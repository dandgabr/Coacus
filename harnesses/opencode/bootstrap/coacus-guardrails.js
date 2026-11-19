// Coacus guardrail plugin for opencode (generated — do not edit).
// Install: copy to <harness config>/plugins/coacus-guardrails.js.
// Delegates the decision to scripts/coacus_guard.py (PAER). A deny throws
// (OpenCode's only blocking mechanism); an ask is raised only through the
// V2 permission evaluate hook and never loosens a decision it is handed.

import { execFileSync } from 'node:child_process';

const COACUS_ROOT = "__COACUS_ROOT__";
const PYTHON = "__COACUS_PYTHON__";
const GUARD = COACUS_ROOT + '/scripts/coacus_guard.py';
const RANK = { allow: 0, ask: 1, deny: 2 };

let evaluateRegistered = false;

/** Run the guard once; return its parsed effect, or null on any failure. */
function callGuard(channel, payload) {
  try {
    const out = execFileSync(PYTHON, ['-I', GUARD, '--harness', 'opencode', '--event', 'tool.pre',
      '--channel', channel, '--root', COACUS_ROOT], { input: JSON.stringify(payload),
      encoding: 'utf8', timeout: 5000, stdio: ['pipe', 'pipe', 'ignore'] }).trim();
    const parsed = JSON.parse(out || '{}');
    return parsed && typeof parsed === 'object' ? parsed : null;
  } catch { return null; }
}

/**
 * Guardrail plugin: evaluate a tool call and abort it on a deny.
 *
 * @returns {Promise<object>} The plugin hook map.
 */
export const CoacusGuardrails = async () => ({
  'tool.execute.before': async (input, output) => {
    const channel = evaluateRegistered ? 'before' : 'default';
    const effect = callGuard(channel, { tool: input.tool, tool_input: output.args });
    if (effect && effect.decision === 'deny') {
      throw new Error('Coacus guardrail denied this tool call.');
    }
  },
});

/** Return the stricter of two effects; unknown values count as the current one. */
function stricter(current, proposed) {
  const a = RANK[current] ?? 0;
  const b = RANK[proposed] ?? 0;
  return b > a ? proposed : current;
}

// ponytail: dual v1/v2 export; upgrade to pure v2 package directory when v1 dropped
export default {
  id: 'coacus-guardrails',
  server: CoacusGuardrails,
  async setup(ctx) {
    const v1 = await CoacusGuardrails();
    await ctx.tool.hook('execute.before', (e) => v1['tool.execute.before'](e, { args: e.input ?? {} }));
    try {
      if (ctx.permission && typeof ctx.permission.hook === 'function') {
        await ctx.permission.hook('evaluate', async (e) => {
          try {
            const effect = callGuard('evaluate', { action: e.action, resources: e.resources });
            const proposed = effect && effect.decision;
            if (proposed) e.effect = stricter(e.effect, proposed);
          } catch { /* leave the effect as it came */ }
          return e;
        });
        evaluateRegistered = true;
      }
    } catch { /* no permission API: asks degrade in the guard */ }
  },
};
