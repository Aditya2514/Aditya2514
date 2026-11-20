import json
import sys
import unittest
from datetime import date, timedelta
from pathlib import Path
from xml.etree import ElementTree as ET

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import aurora_art as art  # noqa: E402
import aurora_data as data  # noqa: E402
import build_aurora as build  # noqa: E402

SPEC = json.loads(build.SPEC.read_text())


def calendar(pattern):
    start = date(2025, 11, 16)  # a Sunday, like GitHub's calendar
    return [{"date": (start + timedelta(days=i)).isoformat(), "count": pattern(i)} for i in range(365)]


SYNTHETIC_GH = {  # test fixture only: never written to data/
    "fetched_at": "2026-11-15T06:00:00Z", "login": "x", "followers": 4,
    "totals": {"contributions": 500, "commits": 400, "prs": 0, "issues": 0},
    "days": calendar(lambda i: (i * 7) % 13 if i % 5 else 0),
    "repos": [{"name": n, "created": f"2025-{m:02d}-10", "pushed": "2026-10-01", "kb": kb, "stars": 0, "archived": False,
               "lang": "Python", "languages": [["Python", kb * 900], ["TypeScript", kb * 300]]}
              for n, m, kb in [("LexGuard", 6, 9000), ("Pikina", 8, 4000), ("Noesis", 9, 2500), ("Vidya", 11, 300)]],
}


class FakeRepo:
    def __init__(self, files):
        self._files, self.sha = files, "a" * 40

    def read(self, path):
        return self._files.get(path)

    def files(self):
        return list(self._files)

    def recent(self, n=3):
        return [{"sha": "b" * 40, "date": "2026-11-01", "subject": 'feat: "quoted" <thing> & more'}]


def opener(fail=()):
    files = {}
    for card in SPEC["cards"]:
        for c in card["claims"]:
            files.setdefault(card["repo"], {}).setdefault(c["path"], "")
            files[card["repo"]][c["path"]] += "x\n" + c["needle"] + "\n"
    files.setdefault("Pikina", {})["src/pikina/registry/capabilities/a.json"] = "{}"

    def open_repo(owner, name):
        if name in fail:
            raise OSError("unreachable")
        return FakeRepo(files.get(name, {}))
    return open_repo


class AuroraTest(unittest.TestCase):
    def test_streaks_and_weeks(self):
        days = calendar(lambda i: 1 if 10 <= i < 20 or i == 364 else 0)
        active, longest, current = data.streaks(days)
        self.assertEqual((active, longest, current), (11, 10, 1))
        self.assertEqual(sum(w["count"] for w in data.weekly(days)), 11)

    def test_language_shares_sum_to_one(self):
        shares = data.language_shares(SYNTHETIC_GH["repos"])
        self.assertAlmostEqual(sum(s for _, s in shares), 1.0, places=6)

    def test_collect_links_metrics_and_carry_over(self):
        ev = data.collect(SPEC, {}, opener())
        self.assertIn("LexGuard#1", ev["links"])
        later = data.collect(SPEC, ev, opener(fail={"Pikina"}))
        self.assertEqual(later["links"]["Pikina#1"], ev["links"]["Pikina#1"])
        self.assertEqual(ev["metrics"]["Pikina"], "1")
        self.assertEqual(later["metrics"]["Pikina"], "1")

    def test_every_scene_parses(self):
        ev = data.collect(SPEC, {}, opener())
        gh = SYNTHETIC_GH
        active, longest, current = data.streaks(gh["days"])
        scenes = [art.hero("0° N"), art.basecamp(build.LOOP_RULES), art.flare(),
                  art.expeditions(SPEC["flagships"], SPEC["systems"], ev["metrics"], SPEC["categories"], len(ev["links"])),
                  art.trail(ev["recent"], {}, SPEC["categories"], ev["generated_at"]),
                  art.sky(gh, data.weekly(gh["days"]), active, longest, current, 4),
                  art.terrain(gh["repos"], SPEC["categories"], ["LexGuard"], gh["fetched_at"]),
                  art.bedrock(data.language_shares(gh["repos"]), 4), art.channel("Email", "x", "mail", art.AMBER)]
        import aurora_fx as fx
        from datetime import datetime, timezone, timedelta as td
        commits = [{"repo": "LexGuard", "sha": str(i), "message_first_line": 'fix: "x" & y',
                    "authored_at": datetime(2026, 5, 1, tzinfo=timezone.utc) + td(minutes=37 * i)} for i in range(300)]
        r = data.rhythm(commits)
        self.assertEqual(sum(r["hours"]), 300)
        self.assertIn(r["chronotype"], {"Night Owl", "Early Riser", "Afternoon Climber", "Evening Climber"})
        scenes += [fx.hero("0° N", ["a", "b", "c"]), fx.rhythm(r, "2026-11-15T00:00:00Z"), fx.divider("", 1)]
        for s in scenes:
            ET.fromstring(s)

    def test_entrances_never_start_hidden(self):
        # The first frame is what a link preview or a quick scroller sees, so content must not start invisible.
        import re
        for name in ("up", "fade", "slide", "rise"):
            frames = re.search(r"@keyframes %s\{from\{([^}]*)\}" % name, art.CSS)
            self.assertIsNotNone(frames, name)
            self.assertNotRegex(frames.group(1), r"opacity\s*:\s*0(?![.\d])", name)
            self.assertNotIn("scaleY(0)", frames.group(1), name)

    def test_countup_rests_on_the_real_value(self):
        import aurora_fx as fx
        for final in ("117", "1,234", "7"):
            root = ET.fromstring(f'<svg xmlns="http://www.w3.org/2000/svg">{fx.countup(0, 0, final, 20, "#fff")}</svg>')
            shown = [el.text for el in root if el.get("opacity") != "0"]
            self.assertEqual(shown, [final])

    def test_curtains_are_coloured_by_height(self):
        # red-magenta crown, green body, pink-violet fringe on the lower edge
        for key in ("em", "te", "ic"):
            grad = art.BASE_DEFS.split(f'id="ray-{key}"')[1].split("</linearGradient>")[0]
            self.assertIn("#ff4f86", grad)
            self.assertIn("#b47cff", grad)

    def test_only_full_brightness_curtains_surge(self):
        self.assertIn('class="surge"', art.aurora(600, 200, 120, 1))
        self.assertNotIn('class="surge"', art.aurora(600, 200, 120, 1, opacity=.4))

    def test_every_built_scene_has_unique_ids(self):
        import re
        for path in sorted((Path(__file__).resolve().parent.parent / "assets" / "aurora").glob("*.svg")):
            ids = re.findall(r'\bid="([^"]+)"', path.read_text())
            self.assertEqual(len(ids), len(set(ids)), path.name)

    def test_template_placeholders_all_known(self):
        text = build.TEMPLATE.read_text()
        for token in ("{{cards}}", "{{kit}}", "{{generated}}"):
            self.assertIn(token, text)


if __name__ == "__main__":
    unittest.main()
