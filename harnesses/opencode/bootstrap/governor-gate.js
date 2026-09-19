// Coacus governor gate for opencode (generated — do not edit).
// Install: copy to <harness config>/plugins/coacus-governor.js.
// It intercepts `task` (subagent spawn), acquires a slot from the
// Coacus governor and ABORTS the spawn when no slot is free (the
// cap is enforced, not advisory). A rate-limit (429) in the result
// parks the caller as PAUSED for the orchestrator to retry with
// backoff (D6/ADR-0007).

import { execFileSync } from 'node:child_process';

const COACUS_ROOT = '__COACUS_ROOT__';
const GOVERNOR = COACUS_ROOT + '/scripts/coacus_governor.py';
const MAX_TOTAL = String(process.env.ORCH_MAX_CONCURRENT ?? 5);
const MAX_CALLS = 3;
const SPAWN_TOOLS = new Set(['task']);
const RATE_LIMIT_RE = /(429|Too Many Requests|rate.?limit|quota exceeded|RPM|TPM)/i;

// caller -> {token, calls}; kept on the plugin instance, never in args.
const held = new Map();

const gov = (action, caller, timeout = '5', orchestrator = 'no') => {
  try {
    return execFileSync(
      'python3',
      [GOVERNOR, action, caller, orchestrator, timeout, MAX_TOTAL],
      { encoding: 'utf8', stdio: ['ignore', 'pipe', 'ignore'], timeout: 70000 },
    ).trim();
  } catch { return ''; }
};

export const CoacusGovernor = async () => ({
  'tool.execute.before': async (input, output) => {
    if (!SPAWN_TOOLS.has(input.tool ?? '')) return;
    const caller = `${input.tool}-${input.sessionID ?? 'sess'}-${input.callID ?? Date.now()}`;
    const token = gov('acquire', caller, '30');
    if (!token) {
      throw new Error(
        'Coacus governor: concurrency cap reached; no slot free. ' +
        'Retry after a running agent completes (cap = ' + MAX_TOTAL + ').',
      );
    }
    held.set(caller, { token, calls: 0 });
    // Do NOT mutate output.args (it would leak into the subagent payload).
  },
  'tool.execute.after': async (input, output) => {
    if (!SPAWN_TOOLS.has(input.tool ?? '')) return;
    const caller = `${input.tool}-${input.sessionID ?? 'sess'}-${input.callID ?? Date.now()}`;
    const entry = held.get(caller) ?? { token: '', calls: 0 };
    const text = `${output.output ?? ''} ${input.args?.prompt ?? ''}`;
    if (RATE_LIMIT_RE.test(text)) {
      held.delete(caller);
      gov('fail', caller);
      output.metadata = output.metadata || {};
      output.metadata.coacus = 'paused_rate_limit';
    } else {
      held.delete(caller);
      gov('release', caller);
    }
  },
  // Safety net: release any slot still held when a new turn begins,
  // so a cancelled/errored spawn (after-hook never ran) cannot leak it.
  'chat.message': async () => {
    for (const [caller] of held) gov('release', caller);
    held.clear();
  },
});
