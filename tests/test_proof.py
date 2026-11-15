import json
import sys
import unittest
from pathlib import Path
from xml.etree import ElementTree as ET

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import build_proof as proof  # noqa: E402

SPEC = json.loads(proof.CLAIMS.read_text())


class FakeRepo:
    def __init__(self, files, sha="a" * 40):
        self.files, self.sha, self.branch = files, sha, "main"

    def read(self, path):
        return self.files.get(path)


def opener_for(files_by_repo, fail=()):
    def open_repo(owner, name):
        if name in fail:
            raise OSError("unreachable")
        return FakeRepo(files_by_repo.get(name, {}))
    return open_repo


def all_present():
    files = {}
    for ex in SPEC["exhibits"]:
        for claim in ex["claims"]:
            files.setdefault(ex["repo"], {}).setdefault(claim["path"], "")
            files[ex["repo"]][claim["path"]] += "x\n" + claim["needle"] + "\n"
    return files


class ProofTest(unittest.TestCase):
    def test_every_claim_found_is_verified_with_its_line(self):
        state = proof.check(SPEC, {}, opener_for(all_present()))
        self.assertTrue(all(c["status"] == "verified" for c in state["claims"]))
        self.assertEqual(state["claims"][0]["line"], 2)

    def test_missing_needle_is_stale(self):
        files = all_present()
        first = SPEC["exhibits"][0]
        files[first["repo"]][first["claims"][0]["path"]] = "rewritten\n"
        state = proof.check(SPEC, {}, opener_for(files))
        self.assertEqual(state["claims"][0]["status"], "stale")
        self.assertIn("STALE", proof.ledger(SPEC, state))

    def test_unreachable_repo_carries_last_result(self):
        good = proof.check(SPEC, {}, opener_for(all_present()))
        repo = SPEC["exhibits"][0]["repo"]
        later = proof.check(SPEC, good, opener_for(all_present(), fail={repo}))
        self.assertEqual(later["claims"][0]["status"], "verified")
        self.assertTrue(later["claims"][0]["carried"])
        self.assertEqual(later["repos"][repo], good["repos"][repo])

    def test_ledger_replacement_is_idempotent_and_escapes(self):
        state = proof.check(SPEC, {}, opener_for(all_present()))
        readme = "top\n" + proof.START + "\nold\n" + proof.END + "\nbottom\n"
        block = proof.ledger(SPEC, state)
        once = proof.replace_block(readme, block)
        self.assertEqual(proof.replace_block(once, block), once)
        self.assertTrue(once.startswith("top\n") and once.endswith("\nbottom\n"))
        self.assertEqual(proof.md_cell("a|b <c>"), "a&#124;b &lt;c&gt;")

    def test_art_parses(self):
        state = proof.check(SPEC, {}, opener_for(all_present()))
        for mode in ("dark", "light"):
            for mobile in (False, True):
                ET.fromstring(proof.hero(SPEC, state, mode, mobile))
        for ex in SPEC["exhibits"]:
            ET.fromstring(proof.tag(ex, state))

    def test_readme_has_one_ledger(self):
        readme = proof.README.read_text()
        self.assertEqual(readme.count(proof.START), 1)
        self.assertEqual(readme.count(proof.END), 1)


if __name__ == "__main__":
    unittest.main()
