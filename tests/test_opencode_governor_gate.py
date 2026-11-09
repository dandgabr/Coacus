"""Exercise the OpenCode gate against an isolated governor ledger."""
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


@unittest.skipUnless(shutil.which('node'), 'Node is required')
class OpenCodeGovernorGateTests(unittest.TestCase):
    def test_v2_hook_correlates_call_id(self):
        with tempfile.TemporaryDirectory() as tmp:
            from engine.generators.plugins import _opencode_governor_gate
            source = _opencode_governor_gate().replace('"__COACUS_ROOT__"', json.dumps(str(ROOT)))
            source = source.replace('"__COACUS_PYTHON__"', json.dumps(sys.executable))
            (Path(tmp) / 'gate.mjs').write_text(source)
            script = '''
import assert from 'node:assert/strict';
import plugin from './gate.mjs';
const hooks = {};
await plugin.setup({tool:{hook: async (name, fn) => {hooks[name] = fn;}}});
const call = {tool:'subagent', sessionID:'session', id:'call-1', input:{}};
await hooks['execute.before'](call);
await assert.rejects(hooks['execute.before'](call), /duplicate/);
await hooks['execute.after']({...call, status:'completed', result:''});
await hooks['execute.before'](call);
await hooks['execute.after']({...call, status:'completed', result:''});
'''
            result = subprocess.run([shutil.which('node'), '--input-type=module', '-e', script],
                cwd=tmp, env=dict(os.environ, GOVERNOR_STATE_DIR=tmp, ORCH_MAX_CONCURRENT='1'),
                text=True, capture_output=True, timeout=20)
            self.assertEqual(result.returncode, 0, result.stderr)

    def test_separate_processes_do_not_share_slot(self):
        with tempfile.TemporaryDirectory() as tmp:
            from engine.generators.plugins import _opencode_governor_gate
            source = _opencode_governor_gate().replace('"__COACUS_ROOT__"', json.dumps(str(ROOT)))
            source = source.replace('"__COACUS_PYTHON__"', json.dumps(sys.executable))
            (Path(tmp) / 'gate.mjs').write_text(source)
            (Path(tmp) / 'child.mjs').write_text('''
import { CoacusGovernor } from './gate.mjs';
const hooks = await CoacusGovernor();
const call = {tool:'task', sessionID:'same', callID:'same'};
await hooks['tool.execute.before'](call, {args:{}});
process.send('acquired');
process.on('message', async () => {
  await hooks['tool.execute.after'](call, {output:''});
  process.exit(0);
});
''')
            driver = '''
import assert from 'node:assert/strict';
import { fork } from 'node:child_process';
const first = fork('./child.mjs', [], {stdio:['ignore','ignore','inherit','ipc'], execArgv:[]});
await new Promise(r => first.once('message', r));
const second = fork('./child.mjs', [], {stdio:['ignore','ignore','inherit','ipc'], execArgv:[]});
let acquired = false;
second.on('message', () => { acquired = true; });
await new Promise(r => setTimeout(r, 500));
assert.equal(acquired, false);
first.send('release');
await new Promise(r => second.once('message', r));
second.send('release');
await Promise.all([first, second].map(p => new Promise(r => p.exitCode !== null ? r() : p.once('exit', r))));
'''
            result = subprocess.run([shutil.which('node'), '--input-type=module', '-e', driver],
                cwd=tmp, env=dict(os.environ, GOVERNOR_STATE_DIR=tmp, ORCH_MAX_CONCURRENT='1'),
                text=True, capture_output=True, timeout=20)
            self.assertEqual(result.returncode, 0, result.stderr)

    def test_stale_completion_and_failed_release(self):
        with tempfile.TemporaryDirectory() as tmp:
            from engine.generators.plugins import _opencode_governor_gate
            source = _opencode_governor_gate().replace('"__COACUS_ROOT__"', json.dumps(str(ROOT)))
            source = source.replace('"__COACUS_PYTHON__"', json.dumps(sys.executable))
            wrapper = Path(tmp) / 'wrapper.py'
            wrapper.write_text('''import os, runpy, sys
if sys.argv[1] == "release" and os.path.exists(os.environ["FAIL_MARKER"]):
    sys.exit(1)
sys.argv[0] = os.environ["REAL_GOVERNOR"]
runpy.run_path(sys.argv[0], run_name="__main__")
''')
            source = source.replace("COACUS_ROOT + '/scripts/coacus_governor.py'", json.dumps(str(wrapper)))
            (Path(tmp) / 'gate.mjs').write_text(source)
            marker = Path(tmp) / 'fail'
            script = r'''
import assert from 'node:assert/strict';
import { execFileSync } from 'node:child_process';
import { writeFileSync, unlinkSync } from 'node:fs';
import { CoacusGovernor } from './gate.mjs';
const hooks = await CoacusGovernor();
const before = hooks['tool.execute.before'], after = hooks['tool.execute.after'];
const call = {tool:'task', sessionID:'session', callID:'stale'};
const ledger = (code) => execFileSync(process.env.PYTHON_TEST, ['-c', code], {encoding:'utf8'}).trim();
const prefix = "from engine.governor.ledger import Ledger; l=Ledger(scope='opencode', max_total=1); ";
await before(call, {args:{}});
const replacement = ledger(prefix + "_, rows=l._read(); p=rows[0].split(); l.release(p[1], token=p[3]); print(l.acquire(p[1], timeout=0))");
await after(call, {output:''});
assert.equal(ledger(prefix + "_, rows=l._read(); print(rows[0].split()[3])"), replacement);
ledger(prefix + "_, rows=l._read(); p=rows[0].split(); l.release(p[1], token=p[3])");
const fail = {...call, callID:'failure'};
await before(fail, {args:{}});
writeFileSync(process.env.FAIL_MARKER, '');
await assert.rejects(after(fail, {output:''}), /slot retained/);
await assert.rejects(before(fail, {args:{}}), /duplicate/);
assert.equal(ledger(prefix + "print(l.status()['running'])"), '1');
unlinkSync(process.env.FAIL_MARKER);
await after(fail, {output:''});
assert.equal(ledger(prefix + "print(l.status()['running'])"), '0');
'''
            env = dict(os.environ, GOVERNOR_STATE_DIR=tmp, ORCH_MAX_CONCURRENT='1',
                       FAIL_MARKER=str(marker), PYTHON_TEST=sys.executable,
                       REAL_GOVERNOR=str(ROOT / 'scripts/coacus_governor.py'), PYTHONPATH=str(ROOT))
            result = subprocess.run([shutil.which('node'), '--input-type=module', '-e', script],
                                    cwd=tmp, env=env, text=True, capture_output=True, timeout=20)
            self.assertEqual(result.returncode, 0, result.stderr)

    def test_call_lifetime_and_denials(self):
        with tempfile.TemporaryDirectory() as tmp:
            from engine.generators.plugins import _opencode_governor_gate
            source = _opencode_governor_gate()
            source = source.replace('"__COACUS_ROOT__"', json.dumps(str(ROOT)))
            source = source.replace('"__COACUS_PYTHON__"', json.dumps(sys.executable))
            plugin = Path(tmp) / 'gate.mjs'
            plugin.write_text(source)
            script = r'''
import assert from 'node:assert/strict';
import { CoacusGovernor } from './gate.mjs';
const hooks = await CoacusGovernor();
const before = hooks['tool.execute.before'];
const after = hooks['tool.execute.after'];
const call = {tool:'task', sessionID:'session', callID:'first'};
await assert.rejects(before({tool:'task',sessionID:'session'}, {args:{}}), /missing stable/);
await assert.rejects(before({...call, callID:'background'}, {args:{background:true}}), /background/);
await before(call, {args:{}});
await assert.rejects(before(call, {args:{}}), /duplicate/);
const other = {...call, callID:'other'};
const waiting = before(other, {args:{}});
await new Promise(resolve => setTimeout(resolve, 300));
await after(call, {output:''});
await waiting;
await after(other, {output:''});
await before(call, {args:{}});
assert.equal(hooks['chat.message'], undefined);
await after({...call, callID:'unknown'}, {output:''});
await after(call, {output:''});
await before(call, {args:{}});
await after(call, {output:{error:{message:'HTTP 429'}}});
'''
            result = subprocess.run(
                [shutil.which('node'), '--input-type=module', '-e', script],
                cwd=tmp, env=dict(os.environ, GOVERNOR_STATE_DIR=tmp, ORCH_MAX_CONCURRENT='1'),
                text=True, capture_output=True, timeout=30,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            from engine.governor.ledger import Ledger
            status = Ledger(Path(tmp), scope='opencode').status()
            self.assertEqual(status['running'], 0)
            self.assertEqual(status['paused'], 1)

    def test_background_subagent_lifecycle_tracking(self):
        with tempfile.TemporaryDirectory() as tmp:
            from engine.generators.plugins import _opencode_governor_gate
            source = _opencode_governor_gate()
            source = source.replace('"__COACUS_ROOT__"', json.dumps(str(ROOT)))
            source = source.replace('"__COACUS_PYTHON__"', json.dumps(sys.executable))
            plugin_path = Path(tmp) / 'gate.mjs'
            plugin_path.write_text(source)
            script = r'''
import assert from 'node:assert/strict';
import plugin from './gate.mjs';

const hooks = {};
let pushEvent;
const eventStream = {
  [Symbol.asyncIterator]() {
    const queue = [];
    const resolvers = [];
    pushEvent = (item) => {
      if (resolvers.length > 0) {
        resolvers.shift()({ value: item, done: false });
      } else {
        queue.push(item);
      }
    };
    return {
      next: () => {
        if (queue.length > 0) {
          return Promise.resolve({ value: queue.shift(), done: false });
        }
        return new Promise(resolve => resolvers.push(resolve));
      }
    };
  }
};

await plugin.setup({
  tool: {
    hook: async (name, fn) => { hooks[name] = fn; }
  },
  event: {
    subscribe: () => eventStream
  }
});

const before = hooks['execute.before'];
const after = hooks['execute.after'];

// 1. Successful background subagent dispatch
const bgCall1 = { tool: 'subagent', sessionID: 'parent-1', id: 'call-bg-1', input: { background: true } };
await before(bgCall1);

// Tool executes and returns immediately with child session ID
await after({
  ...bgCall1,
  status: 'completed',
  result: { output: { sessionID: 'child-ses-1', status: 'running' } }
});

// Since concurrency cap is 1, a second spawn must be blocked / timeout
const otherCall = { tool: 'subagent', sessionID: 'parent-1', id: 'call-other', input: {} };
const blockedWait = before(otherCall);
let otherAcquired = false;
blockedWait.then(() => { otherAcquired = true; }).catch(() => {});
await new Promise(r => setTimeout(r, 300));
assert.equal(otherAcquired, false, 'Second subagent must not acquire slot while background subagent runs');

// Terminal event: child session succeeds!
pushEvent({ type: 'session.execution.succeeded', data: { sessionID: 'child-ses-1' } });

// Now blockedWait should resolve and acquire slot!
await blockedWait;
assert.equal(otherAcquired, true, 'Second subagent must acquire slot after background subagent completes');
await after({ ...otherCall, status: 'completed', result: '' });

// 2. Background subagent that fails with rate limit during execution
const bgCall2 = { tool: 'subagent', sessionID: 'parent-1', id: 'call-bg-2', input: { background: true } };
await before(bgCall2);
await after({
  ...bgCall2,
  status: 'completed',
  result: { output: { sessionID: 'child-ses-2', status: 'running' } }
});

pushEvent({
  type: 'session.execution.failed',
  data: { sessionID: 'child-ses-2', error: 'HTTP 429 Too Many Requests: quota exceeded' }
});
await new Promise(r => setTimeout(r, 300));

// 3. Background subagent spawn failure (error status on tool return)
const bgCall3 = { tool: 'subagent', sessionID: 'parent-1', id: 'call-bg-3', input: { background: true } };
await before(bgCall3);
// Spawn failed at startup (e.g. invalid model) -> slot released immediately
await after({
  ...bgCall3,
  status: 'error',
  error: 'Model not available'
});
'''
            env = dict(os.environ, GOVERNOR_STATE_DIR=tmp, ORCH_MAX_CONCURRENT='1')
            result = subprocess.run([shutil.which('node'), '--input-type=module', '-e', script],
                cwd=tmp, env=env, text=True, capture_output=True, timeout=20)
            self.assertEqual(result.returncode, 0, result.stderr)
            from engine.governor.ledger import Ledger
            status = Ledger(Path(tmp), scope='opencode').status()
            self.assertEqual(status['running'], 0)
            self.assertEqual(status['paused'], 1)


if __name__ == '__main__':
    unittest.main()
