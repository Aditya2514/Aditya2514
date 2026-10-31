#!/usr/bin/env python3
"""Generate a growing project lobby and a project-independent build kit.

profile.json contains optional overrides, order, featured/excluded names and tools.
--discover refreshes the public-repository cache atomically; failed fetches keep it.
No third-party dependencies. New eligible repositories need no custom artwork.
"""
from pathlib import Path
from html import escape
from urllib.request import Request, urlopen
from urllib.parse import quote
import argparse
import json
import os
import re
import sys
import textwrap

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"assets"/"catalog"
START="<!-- PROJECT-LOBBY:START -->"
END="<!-- PROJECT-LOBBY:END -->"
GOLD="#ffc247"
CYAN="#54cbd5"
CSS="""
text{font-family:Arial,Helvetica,sans-serif}.mono{font-family:Consolas,monospace;letter-spacing:1.5px}
.cat-trace{stroke-dasharray:55 760;animation:cat-trace 12s linear infinite}
.cat-pulse{animation:cat-pulse 4s ease-in-out infinite}
.cat-sweep{transform-origin:0 0;animation:cat-sweep 12s linear infinite}
.cat-meter{transform-box:fill-box;transform-origin:bottom;animation:cat-meter 2.5s ease-in-out infinite}
@keyframes cat-trace{to{stroke-dashoffset:-815}}
@keyframes cat-pulse{50%{opacity:.4}}
@keyframes cat-sweep{to{transform:rotate(360deg)}}
@keyframes cat-meter{50%{transform:scaleY(.35);opacity:.45}}
@media(prefers-reduced-motion:reduce){*{animation:none!important}}
"""
def txt(x,y,s,size=16,color="#edf2f7",attrs=""):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" {attrs}>{escape(str(s))}</text>'
def svg(w,h,title,body):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="cat-title">
<title id="cat-title">{escape(title)}</title><style>{CSS}</style>
<defs><pattern id="cat-grid" width="32" height="32" patternUnits="userSpaceOnUse"><path d="M32 0H0V32" fill="none" stroke="#26303d" stroke-width=".45"/></pattern></defs>
<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="12" fill="#070a10" stroke="#293341"/>
<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="12" fill="url(#cat-grid)"/>
{body}</svg>'''
def lines(value,width,max_lines=None):
    result=textwrap.wrap(str(value),width=width,break_long_words=True,break_on_hyphens=False) or [""]
    if max_lines and len(result)>max_lines:
        result=result[:max_lines]
        result[-1]=result[-1].rstrip(" .")+"…"
    return result
def selected(config,repos):
    excluded={s.casefold() for s in config.get("featured",[])+config.get("exclude",[])+[config["owner"]]}
    overrides={k.casefold():v for k,v in config.get("overrides",{}).items()}
    rows=[]
    for repo in repos:
        name=repo.get("name","")
        if not re.fullmatch(r"[A-Za-z0-9_.-]+",name) or name.casefold() in excluded:
            continue
        if repo.get("fork") or repo.get("archived") or repo.get("private"):
            continue
        extra=overrides.get(name.casefold(),{})
        rows.append({
            "repo":name, "slug":name.lower(),
            "title":extra.get("title",name),
            "description":extra.get("description") or repo.get("description") or "Explore the source, documentation and latest changes.",
            "category":extra.get("category","OPEN-SOURCE PROJECT"),
            "stack":extra.get("stack") or ([repo["language"]] if repo.get("language") else ["Explore source"]),
            "url":f'https://github.com/{quote(config["owner"],safe="")}/{quote(name,safe="")}'
        })
    order={name.casefold():i for i,name in enumerate(config.get("order",[]))}
    return sorted(rows,key=lambda r:(order.get(r["repo"].casefold(),len(order)),r["repo"].casefold()))
def fetch_repositories(owner,fetch=None):
    if not re.fullmatch(r"[A-Za-z0-9-]+",owner):
        raise ValueError("Invalid GitHub owner")
    def api(url):
        headers={"Accept":"application/vnd.github+json","User-Agent":"profile-lobby"}
        token=os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
        if token:headers["Authorization"]="Bearer "+token
        with urlopen(Request(url,headers=headers),timeout=30) as response:
            return json.load(response)
    fetch=fetch or api
    repos=[]
    for page in range(1,101):
        result=fetch(f"https://api.github.com/users/{owner}/repos?type=owner&sort=full_name&per_page=100&page={page}")
        if not isinstance(result,list):raise ValueError("Unexpected repository response")
        for repo in result:
            if not isinstance(repo,dict) or not repo.get("name"):
                raise ValueError("Invalid repository entry")
            if repo.get("private"):continue
            repos.append({k:repo.get(k) for k in ["name","description","language","html_url","fork","archived","private","pushed_at"]})
        if len(result)<100:return repos
    raise ValueError("Repository pagination exceeded limit; retaining the existing cache")
def refresh_cache(config,cache,fetch=None):
    try:
        repos=fetch_repositories(config["owner"],fetch)
        payload=json.dumps({"owner":config["owner"],"repositories":repos},indent=2,sort_keys=True)+"\n"
        temporary=cache.with_suffix(".tmp")
        temporary.write_text(payload)
        temporary.replace(cache)
        return True
    except Exception as error:
        print(f"::warning::Repository discovery unavailable ({type(error).__name__}); keeping cached catalog.",file=sys.stderr)
        return False
def project_card(row,index):
    color=[GOLD,CYAN,"#aa9ff5","#ee946d"][index%4]
    body=f'<path d="M1 1H599V123H447L421 146H1Z" fill="{color}" opacity=".045"/><path d="M436 1H599V164Z" fill="{color}" opacity=".075"/>'
    body+=txt(562,223,f"{index+1:02d}",82,color,'text-anchor="end" font-weight="900" opacity=".07"')
    body+=f'<path d="M18 1H582" stroke="{color}" stroke-width="3" class="cat-trace"/>'
    body+=txt(26,35,f'{index+1:02d} / '+row["category"],12,color,'class="mono"')
    for i,line in enumerate(lines(row["title"],22,2)):
        body+=txt(25,91+i*36,line,34,"#edf2f7",'font-weight="800"')
    body+=f'<g transform="translate(534 86)"><circle r="34" fill="#0d151f" stroke="#334456"/><g class="cat-sweep"><path d="M0 0V-29A29 29 0 0 1 25-14Z" fill="{color}" opacity=".12"/></g><path d="M-15-8L-24 0-15 8M15-8L24 0 15 8M5-16L-5 16" fill="none" stroke="{color}" stroke-width="2"/></g>'
    for i,line in enumerate(lines(row["description"],59,3)):
        body+=txt(26,159+i*23,line,17,"#acb8c7")
    x,y=26,239
    stack=list(row["stack"])
    if len(stack)>6:stack=stack[:5]+[f"+{len(stack)-5} tools"]
    for tag in stack:
        label=str(tag)
        if len(label)>25:label=label[:24]+"…"
        w=24+len(label)*7.7
        if x+w>574:x,y=26,y+31
        body+=f'<rect x="{x}" y="{y}" width="{w:.1f}" height="24" rx="5" fill="#101722" stroke="#334050"/>'
        body+=txt(x+12,y+17,label,13,"#c4cdd9")
        x+=w+8
    h=max(356,y+82)
    body+=f'<path d="M26 {h-52}H574" stroke="#293341"/>'
    body+=f'<rect x="1" y="{h-51}" width="598" height="50" rx="10" fill="{color}" opacity=".035"/>'
    body+=txt(26,h-24,"OPEN REPOSITORY",13,color,'class="mono"')
    body+=f'<path d="M540 {h-30}H572m-8-6 8 6-8 6" fill="none" stroke="{color}" stroke-width="2"/>'
    return svg(600,h,row["title"]+" — "+row["description"],body)
def browse_card(owner):
    return svg(600,356,"Explore all repositories",f'<path d="M18 1H582" stroke="{CYAN}" stroke-width="3" class="cat-trace"/>'+txt(26,35,"NEXT DROP / ALWAYS BUILDING",12,CYAN,'class="mono"')+txt(26,104,"THE LOBBY",42,"#edf2f7",'font-weight="900"')+txt(26,155,"KEEPS GROWING.",36,GOLD,'font-weight="900"')+txt(26,216,"New ideas. New repositories. Same curiosity.",17,"#acb8c7")+txt(26,271,"Browse the next build.",20,"#edf2f7")+txt(26,332,"EXPLORE ALL REPOS  →",14,CYAN,'class="mono"'))
def chips(tools,x,y,width):
    out=[];start=x
    for tool in tools:
        tool=str(tool)
        # Long labels wrap inside their own card rather than extending its width.
        for part in lines(tool,42):
            w=min(width,24+len(part)*7.6)
            if x+w>start+width:x=start;y+=34
            out.append(f'<rect x="{x}" y="{y}" width="{w:.1f}" height="26" rx="5" fill="#121b28" stroke="#344252"/>')
            out.append(txt(x+12,y+18,part,13,"#cbd5e3"))
            x+=w+8
    return "".join(out),y+26
def build_kit(groups):
    body=txt(30,40,"BUILD KIT / CHOOSE THE TOOL FOR THE JOB",15,GOLD,'class="mono"')
    body+=txt(30,77,"Tools I reach for",32,"#edf2f7",'font-weight="800"')
    y=106
    for offset in range(0,len(groups),2):
        blocks=[];row_h=0
        for j,group in enumerate(groups[offset:offset+2]):
            x=24+j*582
            tags,bottom=chips(group["tools"],x+22,y+92,516)
            h=max(156,bottom-y+21);row_h=max(row_h,h)
            block=txt(x+22,y+30,group["name"],15,CYAN,'class="mono" font-weight="700"')
            block+=txt(x+22,y+61,group["purpose"],17,"#aab8c8")+tags
            block+=f'<circle cx="{x+532}" cy="{y+25}" r="4" fill="{GOLD}" class="cat-pulse"/>'
            blocks.append((x,block))
        for x,block in blocks:
            body+=f'<rect x="{x}" y="{y}" width="558" height="{row_h}" rx="8" fill="#0a1018" stroke="#293341"/><path d="M{x+12} {y}H{x+546}" stroke="{CYAN}" class="cat-trace" style="animation-delay:-{offset+j}s"/>'+block
        y+=row_h+16
    body+=txt(30,y+17,"PICK THE RIGHT TOOL. BUILD THE RIGHT THING.",15,"#8394a9")
    return svg(1200,y+42,"Build Kit — tools grouped by purpose, independent of project count.",body)
def lobby_block(rows,owner):
    items=[]
    for row in rows:
        alt=escape(row["title"]+" — "+row["description"]+" Stack: "+", ".join(row["stack"]),quote=True)
        items.append(f'<a href="{row["url"]}"><img src="assets/catalog/{row["slug"]}.svg" width="49%" alt="{alt}" /></a>')
    if len(items)%2:
        items.append(f'<a href="https://github.com/{owner}?tab=repositories"><img src="assets/catalog/browse.svg" width="49%" alt="Explore all repositories" /></a>')
    groups=['<p align="center">\n'+"\n".join(items[i:i+2])+'\n</p>' for i in range(0,len(items),2)]
    return START+"\n\n"+"\n\n".join(groups)+"\n\n"+END
def replace_block(readme,block):
    if readme.count(START)!=1 or readme.count(END)!=1:
        raise ValueError("README must contain exactly one project-lobby marker pair")
    return readme.split(START)[0]+block+readme.split(END)[1]
def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--discover",action="store_true")
    args=parser.parse_args()
    config=json.loads((ROOT/"profile.json").read_text())
    cache=ROOT/"data"/"repos.json"
    if args.discover:refresh_cache(config,cache)
    data=json.loads(cache.read_text())
    if data["owner"]!=config["owner"]:raise ValueError("Cached repository owner differs from config")
    rows=selected(config,data["repositories"])
    new_readme=replace_block((ROOT/"README.md").read_text(),lobby_block(rows,config["owner"]))
    OUT.mkdir(parents=True,exist_ok=True)
    keep={"browse.svg","build-kit.svg","ranked-grind.svg"}
    for index,row in enumerate(rows):
        filename=row["slug"]+".svg";keep.add(filename)
        (OUT/filename).write_text(project_card(row,index))
    (OUT/"browse.svg").write_text(browse_card(config["owner"]))
    (OUT/"build-kit.svg").write_text(build_kit(config["build_kit"]))
    for file in OUT.glob("*.svg"):
        if file.name not in keep:file.unlink()
    (ROOT/"README.md").write_text(new_readme)
    print(f"Generated {len(rows)} reusable project cards and a project-independent Build Kit.")
if __name__=="__main__":main()
