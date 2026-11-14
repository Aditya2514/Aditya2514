import json
from pathlib import Path
import re
import sys
import tempfile
import unittest
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import atlas_data  # noqa: E402
import atlas_scenes as scenes  # noqa: E402
import build_atlas  # noqa: E402
from atlas_featured import FEATURED, featured  # noqa: E402
from atlas_hero import hero  # noqa: E402

ROW = {"repo": "Future-Project", "slug": "future-project", "title": "Future Project", "category": "OPEN-SOURCE PROJECT",
       "description": "A new system.", "stack": ["Rust"], "url": "https://github.com/Aditya2514/Future-Project"}


def every_scene():
    config = json.loads((ROOT / "profile.json").read_text())
    data = atlas_data.load()
    for mobile in (False, True):
        yield hero(mobile)
        for index in range(len(FEATURED)):
            yield featured(index, mobile)
        yield scenes.kit(config["build_kit"], mobile)
        yield scenes.pulse(data, mobile)
        yield scenes.route(mobile)
        yield scenes.contact(mobile)
    yield scenes.repo_card(ROW, 0)
    yield scenes.repo_mini(ROW, 0)
    yield scenes.browse_card()
    yield scenes.browse_card(True)
    yield scenes.button("EMAIL", "#5ed3e8")


class AtlasTests(unittest.TestCase):
    def test_every_scene_is_valid_and_self_contained(self):
        for image in every_scene():
            root = ET.fromstring(image)
            self.assertTrue(root.attrib["viewBox"].startswith("0 0 "))
            # GitHub shows these through <img>: scripts, external files and embedded pages would not load.
            for banned in ("<script", "<foreignObject", "<image", "@import", "url(http", 'href="http'):
                self.assertNotIn(banned, image)
            self.assertIn("prefers-reduced-motion", image)

    def test_builds_are_deterministic(self):
        self.assertEqual(list(every_scene()), list(every_scene()))

    def test_readme_images_exist_and_markers_are_single(self):
        readme = (ROOT / "README.md").read_text()
        paths = set(re.findall(r'(?:src|srcset)="([^"]+)"', readme))
        self.assertTrue(paths)
        for path in paths:
            self.assertFalse(path.startswith("http"), path)
            self.assertTrue((ROOT / path).is_file(), path)
        for marker in build_atlas.LOBBY + build_atlas.FEED:
            self.assertEqual(readme.count(marker), 1)

    def test_repository_text_is_escaped_and_bounded(self):
        row = dict(ROW, title="<b>x</b> " * 30, description='<script>alert("x")</script> & ' * 80,
                   category="<i>" * 40, stack=["<svg onload=x>"] * 12)
        for image in (scenes.repo_card(row, 3), scenes.repo_mini(row, 3)):
            ET.fromstring(image)
            self.assertNotIn("<script>", image)
            self.assertNotIn("<svg onload", image)
            self.assertIn("…", image)
            self.assertLess(len(image), 16000)

    def test_commit_titles_cannot_inject_markdown_or_html(self):
        data = {"refreshed_at": "2026-11-13T00:00:00Z", "recent": [
            {"repo": "LexGuard", "sha": "a" * 40, "date": "2026-11-01", "title": '<script>x</script> | [link](bad) `code` *bold* _em_ ~~no~~'}]}
        block = build_atlas.feed_block(data, "Aditya2514")
        for banned in ("<script>", "[link]", "`code`", "*bold*", "~~no~~", " | [link"):
            self.assertNotIn(banned, block)
        self.assertIn("https://github.com/Aditya2514/LexGuard/commit/" + "a" * 40, block)
        bad = {"refreshed_at": "", "recent": [{"repo": "x/../y", "sha": "a" * 40, "date": "2026-11-01", "title": "t"}]}
        with self.assertRaises(ValueError):
            build_atlas.feed_block(bad, "Aditya2514")

    def test_lobby_pairs_cards_and_fills_an_odd_row(self):
        block = build_atlas.lobby_block([ROW], "Aditya2514")
        self.assertIn("assets/atlas/repo/future-project.svg", block)
        self.assertIn("assets/atlas/repo/future-project-mini.svg", block)
        self.assertIn("assets/atlas/repo/browse.svg", block)
        self.assertNotIn("browse.svg", build_atlas.lobby_block([ROW, ROW], "Aditya2514"))

    def test_readme_blocks_replace_cleanly_and_idempotently(self):
        before = "Intro\n" + build_atlas.LOBBY[0] + "\nold\n" + build_atlas.LOBBY[1] + "\nOutro"
        block = build_atlas.lobby_block([], "Aditya2514")
        after = build_atlas.replace_block(before, build_atlas.LOBBY, block)
        self.assertTrue(after.startswith("Intro\n") and after.endswith("\nOutro"))
        self.assertEqual(build_atlas.replace_block(after, build_atlas.LOBBY, block), after)
        with self.assertRaises(ValueError):
            build_atlas.replace_block("no markers", build_atlas.LOBBY, block)

    def _cache(self, directory):
        cache = Path(directory) / "atlas.json"
        cache.write_text((ROOT / "data" / "atlas.json").read_text())
        return cache

    def test_failed_refresh_keeps_the_snapshot_and_its_date(self):
        def offline():
            raise OSError("offline")
        with tempfile.TemporaryDirectory() as directory:
            cache = self._cache(directory)
            original = cache.read_text()
            self.assertFalse(atlas_data.refresh("Aditya2514", cache, {"signal": offline, "commits": offline}))
            self.assertEqual(cache.read_text(), original)

    def test_partial_refresh_updates_only_what_was_fetched(self):
        def offline():
            raise OSError("offline")
        with tempfile.TemporaryDirectory() as directory:
            cache = self._cache(directory)
            old = json.loads(cache.read_text())
            fresh = dict(old["signal"], total=old["signal"]["total"] + 1)
            self.assertTrue(atlas_data.refresh("Aditya2514", cache, {"signal": lambda: fresh, "commits": offline}))
            new = json.loads(cache.read_text())
            self.assertEqual(new["signal"]["total"], old["signal"]["total"] + 1)
            self.assertEqual(new["rhythm"], old["rhythm"])
            self.assertEqual(new["recent"], old["recent"])

    def test_unchanged_or_malformed_data_does_not_touch_the_cache(self):
        with tempfile.TemporaryDirectory() as directory:
            cache = self._cache(directory)
            original = cache.read_text()
            old = json.loads(original)
            same = {"signal": lambda: old["signal"], "commits": lambda: (old["rhythm"], old["recent"])}
            self.assertFalse(atlas_data.refresh("Aditya2514", cache, same))
            junk = {"signal": lambda: {"total": "many"}, "commits": lambda: (old["rhythm"], old["recent"])}
            self.assertFalse(atlas_data.refresh("Aditya2514", cache, junk))
            self.assertEqual(cache.read_text(), original)


    def test_live_sections_compose_with_the_existing_summarisers(self):
        from collections import Counter
        from datetime import datetime, timezone
        import build_signal
        import github_activity
        weeks = [[(f"2026-10-{4 + 7 * w + d:02d}", (w + d) % 3) for d in range(7)] for w in range(3)]
        calendar = {"weeks": weeks, "public_repos": 17, "source": "stub",
                    "languages": Counter({"Python": 500, "JavaScript": 300, "TypeScript": 100, "HTML": 50, "CSS": 30, "Shell": 15, "C++": 5})}
        commits = [{"repo": "Aditya2514" if n == 0 else "Pikina", "sha": f"{n:040x}", "message_first_line": f"change {n}",
                    "authored_at": datetime(2026, 11, 10, n % 24, 5, tzinfo=timezone.utc)} for n in range(30)]
        real = build_signal.from_github, github_activity.from_github
        build_signal.from_github, github_activity.from_github = (lambda login: calendar), (lambda login: commits)
        try:
            with tempfile.TemporaryDirectory() as directory:
                cache = self._cache(directory)
                self.assertTrue(atlas_data.refresh("Aditya2514", cache))
                data = atlas_data.validate(json.loads(cache.read_text()))
        finally:
            build_signal.from_github, github_activity.from_github = real
        self.assertEqual(data["signal"]["total"], sum(c for week in weeks for _, c in week))
        self.assertEqual(data["signal"]["languages"][-1][0], "Other")
        self.assertAlmostEqual(sum(share for _, share in data["signal"]["languages"]), 100, delta=0.3)
        self.assertEqual(sum(data["rhythm"]["per_hour"]), 30)
        self.assertEqual(len(data["recent"]), atlas_data.RECENT)
        self.assertNotIn("Aditya2514", [c["repo"] for c in data["recent"]])
        for mobile in (False, True):
            ET.fromstring(scenes.pulse(data, mobile))
        self.assertIn("change 1", build_atlas.feed_block(data, "Aditya2514"))


if __name__ == "__main__":
    unittest.main()
