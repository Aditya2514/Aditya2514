import json
from pathlib import Path
import sys
import tempfile
import unittest
from xml.etree import ElementTree as ET

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"scripts"))
import build_catalog as catalog
import build_ranked_grind as grind

class CatalogTests(unittest.TestCase):
    def config(self):
        return {"owner":"Aditya2514","featured":["LexGuard"],"exclude":["hidden"],"order":[],"overrides":{}}

    def test_new_public_repo_is_included_with_no_custom_design(self):
        repos=[{"name":"Future-Project","description":"A new system","language":"Rust"}]
        row=catalog.selected(self.config(),repos)[0]
        self.assertEqual(row["stack"],["Rust"])
        self.assertIn("Future-Project",catalog.lobby_block([row],"Aditya2514"))
        ET.fromstring(catalog.project_card(row,0))

    def test_private_forks_archives_featured_and_profile_are_excluded(self):
        repos=[{"name":"private","private":True},{"name":"fork","fork":True},{"name":"old","archived":True},{"name":"LexGuard"},{"name":"Aditya2514"},{"name":"hidden"},{"name":"keep"}]
        self.assertEqual([r["repo"] for r in catalog.selected(self.config(),repos)],["keep"])

    def test_pagination_fetches_more_than_100(self):
        pages=[]
        def fetch(url):
            pages.append(url)
            return [{"name":f"repo-{i}"} for i in range(100)] if len(pages)==1 else [{"name":"last"}]
        self.assertEqual(len(catalog.fetch_repositories("Aditya2514",fetch)),101)
        self.assertTrue(pages[-1].endswith("page=2"))

    def test_partial_fetch_failure_does_not_replace_cache(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"repos.json";p.write_text('{"original":true}')
            calls=[]
            def fetch(url):
                calls.append(url)
                if len(calls)==2:raise OSError("offline")
                return [{"name":f"repo-{i}"} for i in range(100)]
            self.assertFalse(catalog.refresh_cache(self.config(),p,fetch))
            self.assertEqual(p.read_text(),'{"original":true}')

    def test_text_is_escaped_and_long_content_is_bounded(self):
        row=catalog.selected(self.config(),[{"name":"long-project","description":'<script>alert("x")</script> & '*100,"language":"Rust"}])[0]
        rendered=catalog.project_card(row,0)
        ET.fromstring(rendered)
        self.assertNotIn("<script>",rendered)
        self.assertIn("…",rendered)
        self.assertLess(len(rendered),12000)

    def test_readme_update_preserves_other_sections_and_is_idempotent(self):
        before="Intro\n"+catalog.START+"\nold\n"+catalog.END+"\nOutro"
        block=catalog.lobby_block([],"Aditya2514")
        after=catalog.replace_block(before,block)
        self.assertTrue(after.startswith("Intro\n"))
        self.assertTrue(after.endswith("\nOutro"))
        self.assertEqual(catalog.replace_block(after,block),after)
        with self.assertRaises(ValueError):catalog.replace_block("no markers",block)

    def test_build_kit_can_grow_without_project_columns(self):
        groups=[{"name":"NEW CATEGORY","purpose":"New capability","tools":["tool "+str(i) for i in range(30)]}]
        root=ET.fromstring(catalog.build_kit(groups))
        self.assertGreater(int(root.attrib["height"]),300)

    def test_weekly_map_uses_source_totals(self):
        source='<svg xmlns="http://www.w3.org/2000/svg"><title>Week of 2026-10-11: 10 contributions</title><title>Week of 2026-10-18: 9 contributions</title><text>updated 2026-10-30</text></svg>'
        weeks,stamp=grind.read_weeks(source)
        self.assertEqual(sum(c for _,c in weeks),19)
        self.assertEqual(stamp,"2026-10-30")
        ET.fromstring(grind.render(weeks,stamp))
        ET.fromstring(grind.render([],stamp))

if __name__=="__main__":unittest.main()
