import re
import unittest
from pathlib import Path


class Web3DExampleIntegrityTests(unittest.TestCase):
    def test_direct_and_transitive_modules_have_integrity_pins(self):
        example = Path(__file__).resolve().parents[1] / 'knowledge/skills/engineering/practices/web-3d-object-modeling/examples/lamp-and-mug.html'
        html = example.read_text(encoding='utf-8')
        pins = dict(re.findall(r"'(three\.(?:module|core)\.js)': '(sha384-[^']+)'", html))
        self.assertEqual(pins, {
            'three.module.js': 'sha384-wyxAlyAVVsyc7KN24a4+m1tMTC2BwrjQyLgLStDaUBDmwK+gWUMULWHSS0NRoZKv',
            'three.core.js': 'sha384-r1q8Si7xFBrvMv3Q4yjQkKhkYZ2lp+wn/bPPzNZTsc8DY4uPJmm2vheuz1Yn+8m8',
        })
        self.assertIn("request.integrity !== integrity", html)
        self.assertIn("fetch(request)", html)


if __name__ == '__main__':
    unittest.main()
