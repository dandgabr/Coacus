import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from engine.improve import loop


class WindowsRecoveryTests(unittest.TestCase):
    def test_requires_preexisting_key_and_authenticates_entire_proposal(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / 'input.jsonl'
            data = ('{"channel":"human-user-turn","session_id":"a","text":"secret insight"}\n'
                    '{"channel":"human-user-turn","session_id":"b","text":"secret insight"}\n')
            source.write_text(data, encoding='utf-8')
            key = 'ab' * 32
            with patch.object(loop, '_windows', return_value=True), patch.dict('os.environ', {}, clear=True):
                missing = loop.run(root, {'transcript': str(source)})
                self.assertFalse(missing['ok'])
                self.assertFalse((root / 'docs').exists())
                with patch.dict('os.environ', {'COACUS_IMPROVE_RECOVERY_KEY': key}):
                    result = loop.run(root, {'transcript': str(source)})
            self.assertTrue(result['ok'], result)
            self.assertNotIn(key, json.dumps(result))
            proposal = result['proposals'][0]
            self.assertEqual(loop.recover(root, proposal, source, key)[0]['text'], 'secret insight')
            for altered in ({**proposal, 'status': 'approved'},
                            {**proposal, 'review': {**proposal['review'], 'source': 'other'}}):
                with self.assertRaises(ValueError):
                    loop.recover(root, altered, source, key)
            with self.assertRaises(ValueError):
                loop.recover(root, proposal, source, '00' * 32)
            source.write_text(data + ' ', encoding='utf-8')
            with self.assertRaises(ValueError):
                loop.recover(root, proposal, source, key)
            for path in (root / 'docs').rglob('*'):
                if path.is_file():
                    self.assertNotIn(key.encode(), path.read_bytes())
                    self.assertNotIn(b'secret insight', path.read_bytes())
