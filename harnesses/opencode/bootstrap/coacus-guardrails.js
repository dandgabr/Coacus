// Coacus guardrail plugin for opencode (generated — do not edit).
// Install: copy to <harness config>/plugins/coacus-guardrails.js.
// Delegates the decision to scripts/coacus_guard.py (PAER) and throws on
// a deny (OpenCode's only blocking mechanism — orchestration-governance).

import { execFileSync } from 'node:child_process';

const COACUS_ROOT = "__COACUS_ROOT__";
const PYTHON = "__COACUS_PYTHON__";
const GUARD = COACUS_ROOT + '/scripts/coacus_guard.py';

/**
 * Guardrail plugin: evaluate a tool call and abort it on a deny.
 *
 * @returns {Promise<object>} The plugin hook map.
 */
export const CoacusGuardrails = async () => ({
  'tool.execute.before': async (input, output) => {
    const payload = JSON.stringify({ tool: input.tool, tool_input: output.args });
    let effect = '{}';
    try {
      effect = execFileSync(PYTHON, [GUARD, '--harness', 'opencode', '--event', 'tool.pre',
        '--root', COACUS_ROOT], { input: payload, encoding: 'utf8', timeout: 5000,
        stdio: ['pipe', 'pipe', 'ignore'] }).trim();
    } catch { return; }
    // OpenCode has no native effect JSON: only a throw blocks.
    if (effect.includes('"deny"')) {
      throw new Error('Coacus guardrail denied this tool call.');
    }
  },
});
