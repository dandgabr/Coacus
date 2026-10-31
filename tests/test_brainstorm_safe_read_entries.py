import importlib.util
import os
from pathlib import Path
import tempfile
import unittest
from unittest import mock

SCRIPT = Path(__file__).resolve().parents[1] / 'methodology/workflows/brainstorming/scripts/server.py'


class SafeReadEntriesTests(unittest.TestCase):
    def setUp(self):
        spec = importlib.util.spec_from_file_location('brainstorm_entry_test', SCRIPT)
        self.module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.module)
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.module.CONTENT = self.root / 'content'
        self.module.CONTENT.mkdir()

    @unittest.skipUnless(os.open in os.supports_dir_fd and hasattr(os, 'O_NOFOLLOW') and hasattr(os, 'O_DIRECTORY'), 'requires secure dirfd support')
    def test_entries_and_links(self):
        content = self.module.CONTENT
        (content / 'file name.txt').write_bytes(b'allowed')
        (self.root / 'secret').write_bytes(b'secret')
        self.assertEqual(self.module.safe_read('file name.txt')[0], b'allowed')
        for name in ('missing', '../secret', '/secret', '.', '..', '.hidden', 'bad\0name'):
            with self.subTest(name=name), self.assertRaises(OSError):
                self.module.safe_read(name)
        (content / 'link').symlink_to(self.root / 'secret')
        with self.assertRaises(OSError):
            self.module.safe_read('link')
        os.link(self.root / 'secret', content / 'hardlink')
        with self.assertRaises(OSError):
            self.module.safe_read('hardlink')

    @unittest.skipUnless(os.open in os.supports_dir_fd and hasattr(os, 'O_NOFOLLOW') and hasattr(os, 'O_DIRECTORY'), 'requires secure dirfd support')
    def test_swap_to_symlink_between_listing_and_open(self):
        target = self.module.CONTENT / 'file'
        target.write_bytes(b'allowed')
        (self.root / 'secret').write_bytes(b'secret')
        real_listdir = os.listdir
        def swap(directory):
            entries = real_listdir(directory)
            target.unlink()
            target.symlink_to(self.root / 'secret')
            return entries
        with mock.patch.object(self.module.os, 'listdir', side_effect=swap):
            with self.assertRaises(OSError):
                self.module.safe_read('file')

    def test_unsupported_platform_fails_closed(self):
        with mock.patch.object(self.module.os, 'supports_dir_fd', set()):
            with self.assertRaises(OSError):
                self.module.safe_read('file')


if __name__ == '__main__':
    unittest.main()
