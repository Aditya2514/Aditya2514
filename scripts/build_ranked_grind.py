#!/usr/bin/env python3
"""Turn the current signal.svg's real weekly totals into an esports activity map.

Consumes the existing data generator's dated bar titles. No invented dates or
counts; no extra API call. Only active weeks are shown, in chronological order.
"""
from pathlib import Path
from xml.etree import ElementTree as ET
import math
import re
from build_catalog import svg,txt,GOLD,CYAN

ROOT=Path(__file__).resolve().parents[1]
NS="{http://www.w3.org/2000/svg}"
def read_weeks(source):
    tree=ET.fromstring(source)
    weeks=[]
    for el in tree.iter(NS+"title"):
        m=re.fullmatch(r"Week of (\d{4}-\d{2}-\d{2}): (\d+) contributions",el.text or "")
        if m:weeks.append((m[1],int(m[2])))
    if len({d for d,c in weeks})!=len(weeks):raise ValueError("Duplicate weekly totals")
    weeks=sorted((d,c) for d,c in weeks if c>0)
    texts=[el.text or "" for el in tree.iter(NS+"text")]
    stamp=next((re.search(r"updated (\d{4}-\d{2}-\d{2})",s).group(1) for s in texts if re.search(r"updated (\d{4}-\d{2}-\d{2})",s)),"not recorded")
    return weeks,stamp
def render(weeks,stamp):
    count=len(weeks)
    cols=9
    rows=max(1,math.ceil(count/cols))
    cell=58;gap=8;left=35;top=126
    map_h=rows*(cell+gap)-gap
    height=max(440,top+map_h+75)
    total=sum(c for d,c in weeks);peak=max((c for d,c in weeks),default=0)
    body=txt(32,39,"RANKED GRIND / CONTRIBUTION BATTLEGROUND",15,GOLD,'class="mono"')
    body+=txt(32,82,"Drop. Commit. Repeat.",32,"#edf2f7",'font-weight="900"')
    body+=txt(1165,37,"SNAPSHOT / "+stamp,12,"#91a2b6",'text-anchor="end" class="mono"')
    body+=f'<rect x="22" y="112" width="612" height="{map_h+31}" rx="9" fill="#090f18" stroke="#354353"/>'
    centers=[]
    for i,(day,value) in enumerate(weeks):
        x=left+(i%cols)*(cell+gap);y=top+(i//cols)*(cell+gap)
        shade=["#142830","#1d414b","#286570","#448e94"][min(3,int(value/peak*3))] if peak else "#142830"
        body+=f'<g><title>Week of {day}: {value} contributions</title><rect x="{x}" y="{y}" width="{cell}" height="{cell}" rx="5" fill="{shade}" stroke="#3b6674"/>'
        body+=txt(x+cell/2,y+36,str(value),20,"#e6f5f7",'text-anchor="middle" font-weight="700"')+'</g>'
        centers.append((x+cell/2,y+cell/2))
    if centers:
        # Patrol four actual active-week locations; it never changes their values.
        indices=sorted({0,len(centers)//3,2*len(centers)//3,len(centers)-1})
        coordinates=[centers[i] for i in indices]
        coordinates.append(coordinates[0])
        n=len(coordinates)-1
        keyframes="".join(f'{100*i/n:.2f}%{{transform:translate({x}px,{y}px)}}' for i,(x,y) in enumerate(coordinates))
        body+=f'<style>.grind-scope{{animation:grind-patrol 18s ease-in-out infinite}}@keyframes grind-patrol{{{keyframes}}}@media(prefers-reduced-motion:reduce){{.grind-scope{{animation:none!important}}}}</style>'
        x,y=coordinates[0]
        body+=f'<g class="grind-scope" transform="translate({x} {y})" fill="none" stroke="{GOLD}" stroke-width="2"><circle r="26"/><circle r="19" stroke-opacity=".4"/><path d="M-37 0H-15M15 0H37M0-37V-15M0 15V37"/></g>'
    else:
        body+=txt(60,168,"No active weeks in this snapshot.",20,"#9daab9")
    body+=txt(34,top+map_h+35,"ONE TILE = ONE ACTIVE WEEK  /  OLDER → NEWER",12,"#90a2b8",'class="mono"')
    for i,(label,value) in enumerate([("CONTRIBUTIONS",total),("ACTIVE WEEKS",count),("PEAK WEEK",peak)]):
        x=670+i*170
        body+=f'<rect x="{x}" y="113" width="154" height="113" rx="7" fill="#0e151f" stroke="#354353"/>'
        body+=txt(x+17,163,str(value),35,GOLD if i==0 else CYAN,'font-weight="800"')
        body+=txt(x+17,198,label,11,"#9daab9",'class="mono"')
    body+=txt(674,275,"PLAY THE LONG GAME.",25,"#edf2f7",'font-weight="800"')
    body+=txt(674,310,"Real GitHub activity. A tactical replay.",17,"#a7b5c7")
    body+=txt(674,339,"The scope moves. Your numbers stay honest.",16,"#a7b5c7")
    body+=f'<path d="M674 375H1164" stroke="#334353"/><path d="M674 375H1164" stroke="{GOLD}" stroke-width="2" class="cat-trace"/>'
    body+=txt(674,405,"SCOUT  /  LOCK  /  COMMIT  /  REPEAT",12,CYAN,'class="mono"')
    return svg(1200,height,"Ranked Grind — actual active-week contribution totals from "+stamp,body)
def main():
    source=(ROOT/"assets/signal.svg").read_text()
    weeks,stamp=read_weeks(source)
    output=ROOT/"assets/catalog/ranked-grind.svg"
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(render(weeks,stamp))
    print(f"Ranked Grind: {len(weeks)} active weeks, {sum(c for d,c in weeks)} contributions; source {stamp}.")
if __name__=="__main__":main()
