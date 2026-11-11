import importlib.util
import os
from pathlib import Path
import tempfile
import unittest


@unittest.skipUnless(os.name == 'nt', 'Windows-specific secure filesystem support')
class WindowsSecureIOTests(unittest.TestCase):
    def test_regular_file_read_and_write(self):
        script = Path(os.environ.get('BRAINSTORM_SERVER_FILE', Path(__file__).resolve().parents[1] / 'methodology/workflows/brainstorming/scripts/server.py'))
        spec = importlib.util.spec_from_file_location('brainstorm_windows_io', script)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        with tempfile.TemporaryDirectory() as tmp:
            module.CONTENT = module.STATE = Path(tmp)
            module.safe_state_write('screen', 'hello')
            self.assertEqual(module.safe_read('screen')[0], b'hello')
            module.safe_state_write('screen', ' world', append=True)
            self.assertEqual(module.safe_read('screen')[0], b'hello world')
