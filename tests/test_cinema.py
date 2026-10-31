import json
from pathlib import Path
import sys
import tempfile
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from build_cinema import scenes_for, encode_scenes

class CinemaTests(unittest.TestCase):
    def test_future_repo_becomes_a_scene_without_art_direction(self):
        config={'scenes':[{'insert':'project_lobby','seconds_per_project':7}]}
        profile={'owner':'Aditya2514','featured':['LexGuard']}
        rows=[{'name':'FutureBuild','description':'A future tool','language':'Rust'},{'name':'LexGuard'}]
        scenes=scenes_for(config,profile,rows)
        self.assertEqual(len(scenes),1)
        self.assertEqual(scenes[0]['assets'],['assets/catalog/futurebuild.svg'])
        self.assertEqual(scenes[0]['tags'],['Rust'])
        self.assertEqual(scenes[0]['seconds'],7)

    def test_repository_text_cannot_break_out_of_json_script(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);(root/'safe.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg"/>')
            title='</script><script>alert("x")</script> & café'
            payload=encode_scenes([{'title':title,'assets':['safe.svg']}],root)
            self.assertNotIn('<',payload)
            self.assertEqual(json.loads(payload)[0]['title'],title)

    def test_unsafe_asset_paths_and_links_are_rejected(self):
        with self.assertRaises(ValueError):
            encode_scenes([{'assets':['../outside.svg']}])
        config={'scenes':[{'assets':['safe.svg'],'seconds':10,'url':'javascript:alert(1)'}]}
        with self.assertRaises(ValueError):scenes_for(config,{},[])

    def test_all_current_scenes_have_assets_and_positive_duration(self):
        root=Path(__file__).resolve().parents[1]
        scenes=scenes_for(json.loads((root/'cinema.json').read_text()),json.loads((root/'profile.json').read_text()),json.loads((root/'data/repos.json').read_text())['repositories'])
        self.assertGreater(len(scenes),10)
        for scene in scenes:
            for asset in scene['assets']:self.assertTrue((root/asset).is_file(),asset)
            self.assertGreater(scene['seconds'],0)
        self.assertEqual(len(json.loads(encode_scenes(scenes))),len(scenes))
