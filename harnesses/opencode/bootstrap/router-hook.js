// Coacus router hook for opencode (generated — do not edit).
// OPT-IN: install by copying to <harness config>/plugins/coacus-router.js.
// On each user message it runs the offline router over the prompt and
// appends the ranked candidate agents, so the orchestrator proposes
// the right specialists without a manual lookup (routing). It never
// spawns an agent; concurrency stays the governor's job.

import { execFileSync } from 'node:child_process';

const COACUS_ROOT = '__COACUS_ROOT__';
const ROUTE = COACUS_ROOT + '/scripts/coacus_route.py';
const TOP = String(process.env.COACUS_ROUTE_TOP ?? 4);

/**
 * Run the router for one prompt and return its candidate lines.
 *
 * @param {string} prompt - The user's message text.
 * @returns {string[]} Candidate rows (score, name, category, matched).
 */
const route = (prompt) => {
  try {
    return execFileSync('python3', [ROUTE, '--stdin', '--top', TOP],
      { input: prompt, encoding: 'utf8', stdio: ['pipe', 'pipe', 'ignore'],
        timeout: 20000 },
    ).trim().split('\n').filter(Boolean);
  } catch { return []; }
};

/**
 * Router hook plugin: suggest agents for the incoming message.
 *
 * @returns {Promise<object>} The plugin hook map.
 */
export const CoacusRouter = async () => ({
  'chat.message': async (input, output) => {
    const textPart = (output.parts ?? []).find((p) => p.type === 'text');
    if (!textPart || !textPart.text?.trim()) return;
    const candidates = route(textPart.text);
    if (!candidates.length) return;
    const suggestion = [
      '\n\n<coacus-routing>',
      'Deterministic agent candidates for this request (routing):',
      ...candidates.map((c) => '- ' + c),
      'Confirm or adjust; do not spawn more than the free governor slots.',
      '</coacus-routing>',
    ].join('\n');
    textPart.text += suggestion;
  },
});
