#!/usr/bin/env python3
"""Build the self-contained movie résumé from shared profile data; no dependencies."""
import base64
import json
from html import escape
from pathlib import Path
from build_catalog import selected
ROOT = Path(__file__).resolve().parents[1]

def scenes_for(config, profile, repositories):
    scenes = []
    for item in config['scenes']:
        if item.get('insert') == 'project_lobby':
            for row in selected(profile, repositories):
                scenes.append(dict(chapter='05 / THE EXPANDING LOBBY', title=row['title'],
                    line=row['description'], assets=['assets/catalog/'+row['slug']+'.svg'],
                    seconds=item.get('seconds_per_project', 7), url=row['url'], tags=row['stack']))
        else:
            scenes.append(dict(item))
    if not scenes:
        raise ValueError('At least one scene is required')
    for scene in scenes:
        if not isinstance(scene['seconds'], (int, float)) or not 1 <= scene['seconds'] <= 120:
            raise ValueError('Scene durations must be between 1 and 120 seconds')
        if not scene.get('assets'):
            raise ValueError('Every scene needs artwork')
        url = scene.get('url', '')
        if url and not url.startswith(('https://', 'mailto:')):
            raise ValueError('Only HTTPS and mailto links are allowed')
    return scenes

def encode_scenes(scenes, root=ROOT):
    result=[]
    for scene in scenes:
        encoded=dict(scene)
        encoded['images']=[]
        for name in scene['assets']:
            path=(root/name).resolve()
            if not path.is_relative_to(root.resolve()) or path.suffix != '.svg':
                raise ValueError('Scene artwork must be an SVG inside the project')
            encoded['images'].append('data:image/svg+xml;base64,'+base64.b64encode(path.read_bytes()).decode())
        result.append(encoded)
    # Prevent text in repository descriptions from closing the script element.
    return json.dumps(result, ensure_ascii=True).replace('<', '\\u003c').replace('>', '\\u003e').replace('&','\\u0026')

def main():
    config=json.loads((ROOT/'cinema.json').read_text())
    profile=json.loads((ROOT/'profile.json').read_text())
    cache=json.loads((ROOT/'data/repos.json').read_text())
    scenes=scenes_for(config, profile, cache['repositories'])
    template=(ROOT/'scripts/cinema-template.html').read_text()
    html=template.replace('%%TITLE%%',escape(config['title'])).replace('%%SCENES%%',encode_scenes(scenes)).replace('%%PLAYER%%',(ROOT/'scripts/cinema-player.js').read_text())
    (ROOT/'CINEMA.html').write_text(html)
    print(f'Cinema: {len(scenes)} scenes, {sum(s["seconds"] for s in scenes):g} seconds; self-contained HTML.')
if __name__=='__main__': main()
