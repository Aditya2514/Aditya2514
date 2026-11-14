import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import build_mission as mission


class MissionTests(unittest.TestCase):
    def test_partial_api_failure_retains_snapshot_and_timestamp(self):
        with tempfile.TemporaryDirectory() as directory:
            cache = Path(directory) / 'activity.json'
            original = '{"refreshed_at":"2026-01-01T00:00:00Z","commits":[]}'
            cache.write_text(original)
            calls = []
            def fetch(url):
                calls.append(url)
                if len(calls) == 2:
                    raise OSError('offline')
                return []
            self.assertFalse(mission.refresh(cache, fetch))
            self.assertEqual(cache.read_text(), original)

    def test_external_commit_text_cannot_inject_markdown_or_html(self):
        payload = {'refreshed_at': '2026-11-06T00:00:00Z', 'commits': [{
            'repo': 'LexGuard', 'sha': 'a' * 40, 'date': '2026-11-01T00:00:00Z',
            'title': '<script>x</script> | [link](bad) `code` *bold*',
            'url': 'javascript:alert(1)'}]}
        block = mission.feed_block(payload)
        self.assertNotIn('<script>', block)
        self.assertNotIn('[link]', block)
        self.assertNotIn('javascript:', block)
        self.assertIn('&#124;', block)
        self.assertIn('https://github.com/Aditya2514/LexGuard/commit/' + 'a' * 40, block)

    def test_refresh_preserves_readme_and_catalog_markers(self):
        readme = (mission.ROOT / 'README.md').read_text()
        block = mission.feed_block(json.loads(mission.CACHE.read_text()))
        after = mission.replace_feed(readme, block)
        self.assertEqual(mission.replace_feed(after, block), after)
        for marker in ('<!-- PROJECT-LOBBY:START -->', '<!-- PROJECT-LOBBY:END -->'):
            self.assertEqual(after.count(marker), 1)
        self.assertEqual(after.split('<!-- MISSION-FEED:START -->')[0],
                         readme.split('<!-- MISSION-FEED:START -->')[0])
        self.assertEqual(after.split('<!-- MISSION-FEED:END -->')[1],
                         readme.split('<!-- MISSION-FEED:END -->')[1])

    def test_every_scene_parses_and_can_stand_still(self):
        from xml.etree import ElementTree as ET
        import mission_art as art
        kit = json.loads((mission.ROOT / 'profile.json').read_text())['build_kit']
        scenes = [art.hero(m, s) for m in (False, True) for s in (False, True)]
        scenes += [art.project(i, m) for i in range(3) for m in (False, True)]
        scenes += [f(m) for f in (art.outro, art.results) for m in (False, True)]
        scenes += [art.chapter('02', 'FEATURED MISSIONS', 'Three systems.', m) for m in (False, True)]
        scenes += [art.arsenal(kit, m) for m in (False, True)]
        for image in scenes:
            ET.fromstring(image)
            self.assertNotIn('<script', image)
            # every moving layer is switched off for people who ask for less motion
            self.assertIn('.fx{display:none}', image)
        for still in (art.hero(False, True), art.hero(True, True)):
            self.assertNotIn('@keyframes', still)
        self.assertEqual(art.hero(False), art.hero(False))

    def test_commit_feed_in_the_hero_is_escaped_and_bounded(self):
        from xml.etree import ElementTree as ET
        import mission_art as art
        commits = [{'repo': '<b>x</b>' * 9, 'title': '<script>alert(1)</script> ' * 20}] * 5
        image = art.hero(False, False, commits)
        ET.fromstring(image)
        self.assertNotIn('<script>', image)
        self.assertNotIn('<b>', image)
        self.assertEqual(image.count('class="kf fx"'), 3)
        ET.fromstring(art.hero(False, False, []))


if __name__ == '__main__':
    unittest.main()
