// Coacus governor gate for opencode (generated — do not edit).
// Install: copy to <harness config>/plugins/coacus-governor.js.
// It intercepts `task` and `subagent` spawns, acquires a slot from the
// Coacus governor and ABORTS the spawn when no slot is free (the
// cap is enforced, not advisory). For foreground spawns, the slot is
// released upon tool completion. For background spawns, the slot is
// retained and tracked until the child session terminal event
// (succeeded, failed, interrupted, or deleted). A rate-limit (429) in
// the result or failure event parks the caller as PAUSED for the
// orchestrator to retry with backoff (orchestration-governance).

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

// caller -> {token, calls, background, childSessionID, completing}; kept on the plugin instance, never in args.
const held = new Map();
// childSessionID -> Array<{caller, token}>
const bgHeld = new Map();
let eventStreamActive = false;
const instanceNonce = randomBytes(32).toString('hex');

const callerFor = (input) => {
  if (typeof input.sessionID !== 'string' || !input.sessionID ||
      typeof input.callID !== 'string' || !input.callID) return '';
  return 'oc-' + createHash('sha256').update(JSON.stringify([instanceNonce, input.tool, input.sessionID, input.callID])).digest('hex');
};

const isBackgroundCall = (input, output) => Boolean(
  input?.args?.background ||
  output?.args?.background ||
  input?.input?.background
);

const extractChildSessionID = (out, input) => {
  if (out && typeof out === 'object') {
    if (typeof out.sessionID === 'string' && out.sessionID) return out.sessionID;
    if (out.output && typeof out.output === 'object') {
      if (typeof out.output.sessionID === 'string' && out.output.sessionID) return out.output.sessionID;
      if (out.output.output && typeof out.output.output === 'object') {
        if (typeof out.output.output.sessionID === 'string' && out.output.output.sessionID) return out.output.output.sessionID;
      }
    }
    if (out.metadata && typeof out.metadata === 'object') {
      if (typeof out.metadata.sessionID === 'string' && out.metadata.sessionID) return out.metadata.sessionID;
      if (typeof out.metadata.childSessionID === 'string' && out.metadata.childSessionID) return out.metadata.childSessionID;
    }
  }
  const raw = typeof out?.output === 'string' ? out.output : JSON.stringify(out ?? '');
  const match = raw.match(/sessionID[:\s"']+([a-zA-Z0-9_-]+)/i);
  if (match) return match[1];
  return '';
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

const handleTerminalSessionEvent = async (event) => {
  const sid = event?.data?.sessionID;
  if (!sid || !bgHeld.has(sid)) return;
  const entries = bgHeld.get(sid) ?? [];
  bgHeld.delete(sid);
  for (const { caller, token } of entries) {
    const entry = held.get(caller);
    if (!entry || entry.completing) continue;
    entry.completing = true;
    try {
      if (event.type === 'session.execution.failed' && rateLimited(event.data?.error)) {
        await gov('fail', caller, '5', 'no', token);
      } else {
        await gov('release', caller, '5', 'no', token);
      }
    } catch {
      entry.completing = false;
    } finally {
      held.delete(caller);
    }
  }
};

export const startEventListener = (ctx) => {
  if (typeof ctx?.event?.subscribe !== 'function') return false;
  eventStreamActive = true;
  (async () => {
    try {
      const stream = ctx.event.subscribe({
        types: [
          'session.execution.succeeded',
          'session.execution.failed',
          'session.execution.interrupted',
          'session.deleted',
        ],
      });
      for await (const event of stream) {
        await handleTerminalSessionEvent(event);
      }
    } catch {
      // Event stream closed or aborted
    }
  })();
  return true;
};

/**
 * Governor gate plugin: enforce the concurrency cap on subagent spawns.
 *
 * Acquires a ledger slot before a `task` or `subagent` spawn and aborts it
 * when no slot is free; releases the slot after (or on terminal session event
 * for background spawns), parking the caller as PAUSED on a detected rate limit.
 *
 * @param {object} [ctx] - OpenCode plugin context for event subscription.
 * @returns {Promise<object>} The plugin hook map.
 */
export const CoacusGovernor = async (ctx) => {
  if (ctx) startEventListener(ctx);
  return {
    'tool.execute.before': async (input, output) => {
      if (!SPAWN_TOOLS.has(input.tool ?? '')) return;
      const caller = callerFor(input);
      if (!caller) throw new Error('Coacus governor: missing stable session or call ID; spawn denied.');
      if (held.has(caller)) throw new Error('Coacus governor: duplicate active call ID; spawn denied.');
      const background = isBackgroundCall(input, output);
      if (background && !eventStreamActive) {
        throw new Error('Coacus governor: background subagent spawn requires event subscription support.');
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
      held.set(caller, { token, calls: 0, background });
      // Do NOT mutate output.args (it would leak into the subagent payload).
    },
    'tool.execute.after': async (input, output) => {
      if (!SPAWN_TOOLS.has(input.tool ?? '')) return;
      const caller = callerFor(input);
      const entry = held.get(caller);
      if (!caller || !entry?.token || entry.completing) return;

      if (entry.background) {
        const isError = Boolean(input.status === 'error' || output.error || (output.output && typeof output.output === 'object' && output.output.status === 'error'));
        const childSessionID = extractChildSessionID(output, input);
        if (isError || !childSessionID) {
          entry.completing = true;
          try {
            if (rateLimited(output.output)) {
              await gov('fail', caller, '5', 'no', entry.token);
              output.metadata = output.metadata || {};
              output.metadata.coacus = 'paused_rate_limit';
            } else {
              await gov('release', caller, '5', 'no', entry.token);
            }
          } finally {
            held.delete(caller);
          }
          return;
        }
        entry.childSessionID = childSessionID;
        const list = bgHeld.get(childSessionID) ?? [];
        list.push({ caller, token: entry.token });
        bgHeld.set(childSessionID, list);
        return;
      }

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
  };
};

// ponytail: dual v1/v2 export; upgrade to pure v2 package directory when v1 dropped
export default {
  id: 'coacus-governor',
  server: CoacusGovernor,
  async setup(ctx) {
    startEventListener(ctx);
    const v1 = await CoacusGovernor(ctx);
    await ctx.tool.hook('execute.before', (e) => v1['tool.execute.before']({ ...e, callID: e.id }, { args: e.input }));
    await ctx.tool.hook('execute.after', (e) => {
      const out = { output: e.status === 'completed' ? e.result : String(e.error ?? ''), metadata: e.metadata };
      return v1['tool.execute.after']({ ...e, callID: e.id, args: e.input, status: e.status }, out);
    });
  },
};
