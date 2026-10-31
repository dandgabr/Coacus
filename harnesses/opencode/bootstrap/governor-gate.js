// Coacus governor gate for opencode (generated — do not edit).
// Install: copy to <harness config>/plugins/coacus-governor.js.
// It intercepts `task` (subagent spawn), acquires a slot from the
// Coacus governor and ABORTS the spawn when no slot is free (the
// cap is enforced, not advisory). A rate-limit (429) in the result
// parks the caller as PAUSED for the orchestrator to retry with
// backoff (orchestration-governance).

import { execFile } from 'node:child_process';
import { promisify } from 'node:util';
import { createHash, randomBytes } from 'node:crypto';

const COACUS_ROOT = "__COACUS_ROOT__";
const PYTHON = "__COACUS_PYTHON__";
const GOVERNOR = COACUS_ROOT + '/scripts/coacus_governor.py';
const MAX_TOTAL = String(process.env.ORCH_MAX_CONCURRENT ?? 5);
const MAX_CALLS = 3;
const SPAWN_TOOLS = new Set(['task', 'subagent']);
const RATE_LIMIT_RE = /(429|Too Many Requests|rate.?limit|quota exceeded|RPM|TPM)/i;

// caller -> {token, calls}; kept on the plugin instance, never in args.
const held = new Map();
const instanceNonce = randomBytes(32).toString('hex');

const callerFor = (input) => {
  if (typeof input.sessionID !== 'string' || !input.sessionID ||
      typeof input.callID !== 'string' || !input.callID) return '';
  return 'oc-' + createHash('sha256').update(JSON.stringify([instanceNonce, input.tool, input.sessionID, input.callID])).digest('hex');
};

/**
 * Invoke the Coacus governor CLI.
 *
 * @param {string} action - Governor action (acquire, release, fail, ...).
 * @param {string} caller - Stable caller identity for the ledger slot.
 * @param {string} [timeout='5'] - Seconds to wait for a free slot.
 * @param {string} [orchestrator='no'] - 'yes' if the caller orchestrates.
 * @returns {string} The governor token on success, or '' on failure/cap.
 */
// Inspect bounded values locally; never log tool output.
const rateLimited = (value, depth = 0, seen = new Set()) => {
  if (typeof value === 'string') return RATE_LIMIT_RE.test(value.slice(0, 8192));
  if (!value || typeof value !== 'object' || depth >= 4 || seen.has(value)) return false;
  seen.add(value);
  try {
    let count = 0;
    for (const key in value) {
      if (++count > 64) break;
      if (Object.hasOwn(value, key) && rateLimited(value[key], depth + 1, seen)) return true;
    }
  } catch { return false; }
  return false;
};
const exec = promisify(execFile);
const gov = async (action, caller, timeout = '5', orchestrator = 'no', token = '') => {
  const { stdout } = await exec(PYTHON,
    [GOVERNOR, action, caller, orchestrator, timeout, MAX_TOTAL, '--scope', 'opencode', ...(token ? ['--token', token] : [])],
    { encoding: 'utf8', timeout: 70000 });
  return stdout.trim();
};

/**
 * Governor gate plugin: enforce the concurrency cap on subagent spawns.
 *
 * Acquires a ledger slot before a `task` spawn and aborts it when no slot
 * is free; releases the slot after, parking the caller as PAUSED on a
 * detected rate limit.
 *
 * @returns {Promise<object>} The plugin hook map.
 */
export const CoacusGovernor = async () => ({
  'tool.execute.before': async (input, output) => {
    if (!SPAWN_TOOLS.has(input.tool ?? '')) return;
    const caller = callerFor(input);
    if (!caller) throw new Error('Coacus governor: missing stable session or call ID; spawn denied.');
    if (held.has(caller)) throw new Error('Coacus governor: duplicate active call ID; spawn denied.');
    if (output.args?.background || input.args?.background) {
      throw new Error('Coacus governor: background subagent spawn is not supported.');
    }
    held.set(caller, { pending: true });
    let token;
    try { token = await gov('acquire', caller, '30'); }
    catch { throw new Error('Coacus governor: slot acquisition failed; spawn denied; state may require reconciliation.'); }
    if (!token) {
      held.delete(caller);
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
    const caller = callerFor(input);
    const entry = held.get(caller);
    if (!caller || !entry?.token || entry.completing) return;
    entry.completing = true;
    try {
    if (rateLimited(output.output)) {
      await gov('fail', caller, '5', 'no', entry.token);
      held.delete(caller);
      output.metadata = output.metadata || {};
      output.metadata.coacus = 'paused_rate_limit';
    } else {
      await gov('release', caller, '5', 'no', entry.token);
      held.delete(caller);
    }
    } catch {
      entry.completing = false;
      throw new Error('Coacus governor: completion failed; slot retained for reconciliation.');
    }
  },
});

// ponytail: dual v1/v2 export; upgrade to pure v2 package directory when v1 dropped
export default {
  id: 'coacus-governor',
  server: CoacusGovernor,
  async setup(ctx) {
    const v1 = await CoacusGovernor();
    await ctx.tool.hook('execute.before', (e) => v1['tool.execute.before'](e, { args: e.input }));
    await ctx.tool.hook('execute.after', (e) => {
      const out = { output: e.status === 'completed' ? e.result : String(e.error ?? ''), metadata: e.metadata };
      return v1['tool.execute.after']({ ...e, args: e.input }, out);
    });
  },
};
