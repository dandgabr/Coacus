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


if __name__ == '__main__':
    unittest.main()
