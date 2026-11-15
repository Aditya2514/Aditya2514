import json
import sys
import unittest
from pathlib import Path
from xml.etree import ElementTree as ET

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import build_blueprint as bp  # noqa: E402

SPEC = json.loads(bp.SPEC_FILE.read_text())


class FakeRepo:
    def __init__(self, files):
        self.files, self.sha = files, "a" * 40

    def read(self, path):
        return self.files.get(path)

    def recent(self, n=2):
        return [{"sha": "b" * 40, "date": "2026-11-01", "subject": "feat: something | with a pipe"}]


def opener(files_by_repo, fail=()):
    def open_repo(owner, name):
        if name in fail:
            raise OSError("unreachable")
        return FakeRepo(files_by_repo.get(name, {}))
    return open_repo


def everything():
    files = {}
    for repo, claims in SPEC["projects"].items():
        for claim in claims:
            files.setdefault(repo, {}).setdefault(claim["path"], "")
            files[repo][claim["path"]] += "x\n" + claim["needle"] + "\n"
    return files


class BlueprintTest(unittest.TestCase):
    def test_found_snippets_link_to_their_line(self):
        state = bp.collect(SPEC, {}, opener(everything()))
        self.assertEqual(len(state["links"]), sum(len(c) for c in SPEC["projects"].values()))
        self.assertEqual(state["links"]["LexGuard#1"]["line"], 2)

    def test_missing_snippet_is_dropped_from_the_page(self):
        files = everything()
        files["LexGuard"][SPEC["projects"]["LexGuard"][0]["path"]] = "rewritten\n"
        state = bp.collect(SPEC, {}, opener(files))
        self.assertNotIn("LexGuard#1", state["links"])
        self.assertIsNone(bp.link_for(SPEC, state, "LexGuard", 1))
        self.assertIsNotNone(bp.link_for(SPEC, state, "LexGuard", 2))

    def test_unreachable_repo_keeps_last_links(self):
        good = bp.collect(SPEC, {}, opener(everything()))
        later = bp.collect(SPEC, good, opener(everything(), fail={"Pikina"}))
        self.assertEqual(later["links"]["Pikina#1"], good["links"]["Pikina#1"])
        self.assertTrue(any(r["repo"] == "Pikina" for r in later["recent"]))

    def test_readme_fills_every_placeholder_and_escapes(self):
        state = bp.collect(SPEC, {}, opener(everything()))
        readme = bp.render_readme(SPEC, state)
        self.assertNotIn("{{", readme)
        self.assertIn("&#124;", readme)

    def test_every_drawing_parses(self):
        state = bp.collect(SPEC, {}, opener(everything()))
        kit = json.loads(bp.KIT_FILE.read_text())["build_kit"]
        for mobile in (False, True):
            ET.fromstring(bp.draw_hero(mobile))
            ET.fromstring(bp.draw_kit(kit, mobile))
            for sheet in SPEC["sheets"]:
                ET.fromstring(bp.draw_sheet(sheet, state, SPEC["names"], mobile))

    def test_sheet_edges_point_at_real_stages(self):
        for sheet in SPEC["sheets"]:
            for e in bp.sheet_edges(sheet):
                self.assertLess(max(e[0], e[1]), len(sheet["stages"]))


if __name__ == "__main__":
    unittest.main()
