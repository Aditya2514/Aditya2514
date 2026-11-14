#!/usr/bin/env python3
"""Build the dark Drop Zone README assets; --refresh updates public commit links.

Standard library only. The operator JPEG is embedded so SVGs work as GitHub images.
On API failure retain the last successful activity snapshot and its timestamp.
"""
import argparse
import base64
from datetime import datetime, timezone
from html import escape
import json
import os
from pathlib import Path
import re
import textwrap
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets/mission'
CACHE = ROOT / 'data/mission-activity.json'
OWNER = 'Aditya2514'
REPOS = ('LexGuard', 'Pikina', 'Noesis')
BG, PANEL, LINE = '#0d1117', '#161b22', '#30363d'
WHITE, MUTED, GOLD, CYAN = '#e6edf3', '#a8b3bf', '#e9b44c', '#70c9cb'
CSS = '''
text{font-family:Arial,Helvetica,sans-serif}.mono{font-family:Consolas,monospace;letter-spacing:2px}
.sweep{stroke-dasharray:70 1300;animation:sweep 14s linear infinite}
.breathe{animation:breathe 8s ease-in-out infinite}
.float{animation:float 10s ease-in-out infinite;transform-box:fill-box;transform-origin:center}
.scan{animation:scan 8s ease-in-out infinite}
.step1{animation:step1 12s ease-in-out infinite}.step2{animation:step2 12s ease-in-out infinite}.step3{animation:step3 12s ease-in-out infinite}
@keyframes sweep{to{stroke-dashoffset:-1370}}
@keyframes breathe{0%,100%{opacity:.35}50%{opacity:.8}}
@keyframes float{50%{transform:translateY(-5px)}}
@keyframes scan{0%,100%{transform:translateY(0);opacity:.2}50%{transform:translateY(70px);opacity:.8}}
@keyframes step1{0%,25%,100%{opacity:1}35%,85%{opacity:.35}}
@keyframes step2{0%,20%,70%,100%{opacity:.35}35%,55%{opacity:1}}
@keyframes step3{0%,50%,100%{opacity:.35}65%,90%{opacity:1}}
@media(prefers-reduced-motion:reduce){*{animation:none!important}}
'''

def text(x, y, value, size=20, color=WHITE, attrs=''):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" {attrs}>{escape(str(value))}</text>'

def svg(width, height, title, body, defs=''):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title">
<title id="title">{escape(title)}</title><style>{CSS}</style><defs>{defs}</defs>
<rect width="{width}" height="{height}" rx="16" fill="{BG}"/>{body}
<rect x="1" y="1" width="{width-2}" height="{height-2}" rx="15" fill="none" stroke="{LINE}"/>
</svg>\n'''

PROJECTS = [
    ('LexGuard', 'CONTRACT INTELLIGENCE', 'Catch what the model misses.', 'Statutory retrieval + deterministic risk checks.', GOLD, ['CLAUSE', 'RISK CHECK', 'EVIDENCE']),
    ('Pikina', 'LOCAL DESKTOP AGENT', 'Your machine. Your call.', 'Local inference + validated tools + consent.', CYAN, ['REQUEST', 'VALIDATE', 'APPROVE']),
    ('Noesis', 'MULTIMODAL SEARCH', 'Find the moment. Check the source.', 'Hybrid retrieval + reranking + source citations.', '#b6a7dc', ['QUESTION', 'RETRIEVE', 'SOURCE']),
]

from mission_art import hero, project, extra_assets

def decision(index, mobile=False):
    entries = [
        ('01 / DETERMINISTIC CHECKS', 'Why let code challenge a model?', 'LexGuard pairs model assessments with explicit checks.', 'A plausible answer still needs something you can verify.'),
        ('02 / HUMAN APPROVAL', 'Why pause before an action?', 'Pikina validates tool proposals and asks for high-risk consent.', 'Understanding a request is different from authorizing it.'),
        ('03 / SOURCE TRACEABILITY', 'Why make an answer traceable?', 'Noesis links retrieved evidence to pages or timestamps.', 'The reader should be able to inspect the source.')]
    label,title,a,b=entries[index]
    if mobile:
        body=text(28,36,'ENGINEERING DECISION',14,GOLD,'class="mono"')
        body+=text(28,68,label,14,GOLD,'class="mono"')
        y=113
        for line in textwrap.wrap(title,30):
            body+=text(28,y,line,28,WHITE,'font-weight="700"');y+=36
        y+=10
        for line in textwrap.wrap(a+' '+b,43):
            body+=text(28,y,line,22,MUTED);y+=31
        return svg(600,y+20,title+' '+a+' '+b,body)
    body=text(30,38,'ENGINEERING DECISION / '+label,13,GOLD,'class="mono"')
    body+=text(30,83,title,30,WHITE,'font-weight="700"')+text(30,122,a,19,MUTED)+text(30,155,b,19,MUTED)
    return svg(900,185,title+' '+a+' '+b,body)

def api(url):
    headers={'Accept':'application/vnd.github+json','User-Agent':'drop-zone-profile'}
    token=os.environ.get('GH_TOKEN') or os.environ.get('GITHUB_TOKEN')
    if token:headers['Authorization']='Bearer '+token
    with urlopen(Request(url,headers=headers),timeout=20) as response:return json.load(response)

def refresh(cache=CACHE, fetch=api):
    try:
        rows=[]
        for repo in REPOS:
            items=fetch(f'https://api.github.com/repos/{OWNER}/{repo}/commits?per_page=15')
            if not isinstance(items,list):raise ValueError('Unexpected commit response')
            for item in items:
                if len(item.get('parents',[]))>1:continue
                author=item['commit'].get('author') or {}
                if '[bot]' in author.get('name','').lower():continue
                sha=item['sha']
                if not re.fullmatch('[a-f0-9]{40}',sha):raise ValueError('Invalid commit SHA')
                rows.append({'repo':repo,'sha':sha,'title':item['commit']['message'].splitlines()[0],
                             'date':author['date'],'url':f'https://github.com/{OWNER}/{repo}/commit/{sha}'})
        if not rows:raise ValueError('No commit data')
        payload={'refreshed_at':datetime.now(timezone.utc).isoformat(),
                 'commits':sorted(rows,key=lambda c:c['date'],reverse=True)[:3]}
        temporary=cache.with_suffix('.tmp')
        temporary.write_text(json.dumps(payload,indent=2)+'\n')
        temporary.replace(cache)
        return True
    except Exception as error:
        print(f'::warning::Mission feed retained ({type(error).__name__}).')
        return False

def feed_block(payload):
    rows=['<!-- MISSION-FEED:START -->','', '| Repository | Recent change | Date (UTC) |','| :-- | :-- | :-- |']
    for c in payload['commits'][:3]:
        if c['repo'] not in REPOS or not re.fullmatch('[a-f0-9]{40}',c['sha']):raise ValueError('Invalid cached commit')
        title=escape(c['title']).replace('|','&#124;').replace('[','&#91;').replace(']','&#93;').replace('\n',' ')
        title=title.replace('`','&#96;').replace('*','&#42;').replace('_','&#95;')
        url=f'https://github.com/{OWNER}/{c["repo"]}/commit/{c["sha"]}'
        rows.append(f'| {c["repo"]} | [{title}]({url}) | {c["date"][:10]} |')
    stamp=datetime.fromisoformat(payload['refreshed_at'].replace('Z','+00:00')).astimezone(timezone.utc).strftime('%d %b %Y, %H:%M UTC')
    rows+=['',f'<sub>Recent non-merge changes from LexGuard, Pikina and Noesis. Refreshed {stamp}. Scheduled every six hours; the last successful snapshot stays visible if refresh fails.</sub>','', '<!-- MISSION-FEED:END -->']
    return '\n'.join(rows)

def replace_feed(readme, block):
    start,end='<!-- MISSION-FEED:START -->','<!-- MISSION-FEED:END -->'
    if readme.count(start)!=1 or readme.count(end)!=1:raise ValueError('Expected one mission feed marker pair')
    return readme.split(start)[0]+block+readme.split(end)[1]

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--refresh',action='store_true')
    args=parser.parse_args()
    OUT.mkdir(parents=True,exist_ok=True)
    # Refresh first: the hero's commit feed is drawn from the same snapshot as the README table.
    if args.refresh:refresh()
    for mobile in (False,True):
        suffix='-mobile' if mobile else ''
        for still in (False,True):
            (OUT/f'hero{suffix}{"-still" if still else ""}.svg').write_text(hero(mobile,still))
        for i,p in enumerate(PROJECTS):
            (OUT/f'{p[0].lower()}{suffix}.svg').write_text(project(i,mobile))
    extra_assets(json.loads((ROOT/'profile.json').read_text())['build_kit'])
    payload=json.loads(CACHE.read_text())
    # Rotate by the successful snapshot date, making offline rebuilds deterministic.
    day=datetime.fromisoformat(payload['refreshed_at'].replace('Z','+00:00')).date().toordinal()
    (OUT/'decision.svg').write_text(decision(day%3))
    (OUT/'decision-mobile.svg').write_text(decision(day%3,True))
    readme=ROOT/'README.md'
    readme.write_text(replace_feed(readme.read_text(),feed_block(payload)))
    print('Built mission hero, mobile variants, three project stories and commit feed.')

if __name__=='__main__':main()
