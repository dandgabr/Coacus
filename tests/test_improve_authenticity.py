import copy
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from engine.improve import loop


@unittest.skipUnless(os.name == 'posix', 'POSIX security checks')
class AuthenticityTests(unittest.TestCase):
    def test_complete_proposal_is_authenticated_and_new_review_alone_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / 'input.jsonl'
            source.write_text('\n'.join(json.dumps({'channel': 'human-user-turn', 'session_id': s, 'text': 'insight'}) for s in ('a', 'b')))
            result = loop.run(root, {'transcript': str(source)})
            self.assertTrue(result['ok'], result)
            proposal = result['proposals'][0]
            self.assertEqual(len(loop.recover(root, proposal)), 2)
            with self.assertRaises(ValueError):
                loop.recover(root, proposal['review'])
            for field, value in [('status', 'approved'), ('statement', 'forged'), ('trusted', not proposal['trusted']), ('support', 999), ('routing', {}), ('verification', {})]:
                altered = copy.deepcopy(proposal)
                altered[field] = value
                with self.subTest(field=field), self.assertRaises(ValueError):
                    loop.recover(root, altered)

    def test_legacy_review_only_association_remains_readable(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / 'input.jsonl'
            source.write_text('\n'.join(json.dumps({'channel': 'human-user-turn', 'session_id': s, 'text': 'insight'}) for s in ('a', 'b')))
            proposal = loop.run(root, {'transcript': str(source)})['proposals'][0]
            association = root / '.ai-memory' / 'improve-sources' / (proposal['review']['run_id'] + '.json')
            saved = json.loads(association.read_text())
            del saved['proposals']
            association.write_text(json.dumps(saved))
            self.assertEqual(loop.recover(root, proposal['review'])[0]['text'], 'insight')
            with self.assertRaises(ValueError):
                loop.recover(root, proposal)

    def test_recover_fifo_does_not_block(self):
        with tempfile.TemporaryDirectory() as tmp:
            fifo = Path(tmp) / 'fifo'
            os.mkfifo(fifo)
            code = "from pathlib import Path; from engine.improve.loop import _read_source; _read_source(Path(%r))" % str(fifo)
            result = subprocess.run([sys.executable, '-c', code], capture_output=True, timeout=2)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn(b'not a regular file', result.stderr)
