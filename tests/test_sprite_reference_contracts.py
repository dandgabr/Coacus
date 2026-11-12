import json
import math
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / 'knowledge/skills/domains/industry/game-asset-pipeline/references'


class SpriteContracts(unittest.TestCase):
    def test_motion_guidance_links_and_contact_directives(self):
        skill = ROOT.parent.parent / 'game-animation-qa-motion' / 'SKILL.md'
        text = skill.read_text()
        references = [skill, skill.parent / 'references/motion-continuity-checks.md',
                      ROOT.parents[2] / 'design/game-sprite-design/references/genre-pose-libraries.md']
        for source in references:
            for target in re.findall(r'\]\(([^)]+\.md)\)', source.read_text()):
                self.assertTrue((source.parent / target).is_file(), f'{source}: {target}')
        agent = ROOT.parents[4] / 'agents/specialized-domains/game-art-director/agent.source.md'
        for body in (text, agent.read_text()):
            self.assertIn('artist-reviewed', body)
            self.assertNotIn('zero ground-sliding', body)
            self.assertNotIn('zero foot-sliding', body)
        stride = (skill.parent / 'references/seam-pop-and-stride-measurement.md').read_text()
        self.assertIn('moving support', stride)
        self.assertIn('relative to the support', stride)

    def test_attack_frame_counts_are_rate_qualified_examples(self):
        poses = ROOT.parents[2] / 'design/game-sprite-design/references/genre-pose-libraries.md'
        text = poses.read_text()
        self.assertIn('illustrative', text)
        self.assertIn('60 simulation frames per second', text)

    def test_known_foreground_alpha_example(self):
        text = (ROOT / 'chroma-soft-alpha-unmix.md').read_text()
        code = re.search(r'```python\n(.*?)```', text, re.S).group(1)
        scope = {}
        exec(code, scope)
        estimate = scope['estimate_alpha']
        key, foreground = (0, 1, 0), (0, 0.5, 0)
        for alpha in (0, 0.5, 1):
            observed = tuple(alpha * f + (1 - alpha) * k for f, k in zip(foreground, key))
            self.assertTrue(math.isclose(estimate(observed, foreground, key), alpha))
        self.assertIsNone(estimate(key, key, key))

    def test_legacy_frame_layout_remains_documented(self):
        text = (ROOT / 'runtime-manifest-contracts.md').read_text()
        examples = re.findall(r'```json\n(.*?)```', text, re.S)
        legacy = json.loads(examples[1])
        frame = legacy['frame_layout']['rows']['idle'][0]
        self.assertEqual([frame[k] for k in ('x', 'y', 'w', 'h', 'anchor_x', 'anchor_y')], [0, 0, 256, 256, 128, 240])
        self.assertIn('must not use tight packing', text)

    def test_pivot_registration_and_duration_playback(self):
        text = (ROOT / 'runtime-manifest-contracts.md').read_text()
        manifest = json.loads(re.search(r'```json\n(.*?)```', text, re.S).group(1))
        frames = manifest['frames']
        # Atlas texel locations in world space when each source pivot is at (10, 20).
        def registered(frame):
            x, y = frame['trim_offset']
            px, py = frame['pivot']
            return (10 + x - px, 20 + y - py)
        self.assertEqual(registered(frames['a']), (10, 18))
        self.assertEqual(registered(frames['b']), (11, 19))
        def at(animation, time):
            steps = animation['steps']
            total = sum(s['duration_ms'] for s in steps)
            if animation['playback'] == 'loop':
                time %= total
            elif time >= total:
                return steps[-1]['frame']
            for step in steps:
                if time < step['duration_ms']:
                    return step['frame']
                time -= step['duration_ms']
        walk = manifest['animations']['walk']
        for time, expected in [(0, 'a'), (99, 'a'), (100, 'b'), (299, 'b'), (300, 'a'), (400, 'empty'), (450, 'a')]:
            self.assertEqual(at(walk, time), expected)
        attack = manifest['animations']['attack']
        self.assertEqual(at(attack, 0), 'b')
        self.assertEqual(at(attack, 199), 'b')
        self.assertEqual(at(attack, 200), 'a')
        self.assertEqual(at(attack, 1000), 'a')

    def test_manifest_reconstructs_trimmed_duplicate_and_empty_frames(self):
        text = (ROOT / 'runtime-manifest-contracts.md').read_text()
        manifest = json.loads(re.search(r'```json\n(.*?)```', text, re.S).group(1))
        frames = manifest['frames']
        self.assertEqual([s['frame'] for s in manifest['animations']['walk']['steps']], ['a', 'b', 'a', 'empty'])
        self.assertEqual([s['duration_ms'] for s in manifest['animations']['walk']['steps']], [100, 200, 100, 50])
        atlas = [['R', 'B']]
        expected = {'a': [['.', 'R', '.'], ['.', '.', '.']], 'b': [['.', '.', '.'], ['.', '.', 'B']], 'empty': [['.', '.', '.'], ['.', '.', '.']]}
        for frame_id, frame in frames.items():
            w, h = frame['source_size']
            canvas = [['.'] * w for _ in range(h)]
            rect = frame['rect']
            if rect is not None:
                x, y, rw, rh = rect
                ox, oy = frame['trim_offset']
                for j in range(rh):
                    for i in range(rw):
                        canvas[oy + j][ox + i] = atlas[y + j][x + i]
            self.assertEqual(canvas, expected[frame_id])
            self.assertEqual(frame['pivot'], [1, 2])
        self.assertEqual(manifest['animations']['walk']['playback'], 'loop')
        self.assertEqual(manifest['animations']['attack']['playback'], 'once')
        for animation in manifest['animations'].values():
            for step in animation['steps']:
                self.assertIn(step['frame'], frames)
                self.assertGreater(step['duration_ms'], 0)


if __name__ == '__main__':
    unittest.main()
