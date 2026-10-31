#!/usr/bin/env python3
"""Build the extra BGMI-inspired vector animations. No external dependencies."""
from pathlib import Path
from html import escape
import math

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "dropzone"
A, T, FG, M = "#ffc247", "#54cbd5", "#edf2e9", "#9daab9"
CSS = """
.dz-run{animation:dz-run 12s linear infinite}
.dz-glow{animation:dz-glow 5s ease-in-out infinite}
.dz-float{animation:dz-float 7s ease-in-out infinite}
.dz-turn{animation:dz-turn 12s linear infinite;transform-origin:0 0}
.dz-eq{transform-box:fill-box;transform-origin:bottom;animation:dz-eq 2s ease-in-out infinite}
.dz-hop{animation:dz-hop 8s ease-in-out infinite;transform-box:fill-box;transform-origin:center}
.dz-spark{animation:dz-spark 9s linear infinite}
.dz-plane{animation:dz-plane 12s linear infinite}
.dz-drop{animation:dz-drop 8s ease-in-out infinite}
.dz-progress{stroke-dasharray:50 850;animation:dz-progress 7s linear infinite}
.dz-slot{animation:dz-slot 8s ease-in-out infinite}
@keyframes dz-run{to{stroke-dashoffset:-360}}
@keyframes dz-glow{50%{opacity:.55}}
@keyframes dz-float{50%{transform:translateY(-9px)}}
@keyframes dz-turn{to{transform:rotate(360deg)}}
@keyframes dz-eq{50%{transform:scaleY(.25);opacity:.4}}
@keyframes dz-hop{50%{transform:scale(1.07)}}
@keyframes dz-spark{0%{transform:translate(0,15px);opacity:0}20%{opacity:.55}80%{opacity:.25}100%{transform:translate(35px,-65px);opacity:0}}
@keyframes dz-plane{0%{transform:translate(9px,44px) rotate(39deg);opacity:0}8%{opacity:1}92%{opacity:1}100%{transform:translate(319px,299px) rotate(39deg);opacity:0}}
@keyframes dz-drop{0%,100%{transform:translateY(-12px)}50%{transform:translateY(10px)}}
@keyframes dz-progress{to{stroke-dashoffset:-900}}
@keyframes dz-slot{0%,18%,100%{stroke:#ffc247;fill:#253024}25%,92%{stroke:#293341;fill:#10141b}}
@media(prefers-reduced-motion:reduce){.dz-run,.dz-glow,.dz-float,.dz-turn,.dz-eq,.dz-hop,.dz-spark,.dz-plane,.dz-drop,.dz-progress,.dz-slot{animation:none!important}.dz-spark{opacity:.2}}
"""

def txt(x,y,text,size=16,color=FG,extra=""):
    return f'<text x="{x}" y="{y}" fill="{color}" font-size="{size}" {extra}>{escape(text)}</text>'

def svg(w,h,title,body):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="dz-title">
<title id="dz-title">{escape(title)}</title>
<style>text{{font-family:Arial,Helvetica,sans-serif}}.mono{{font-family:Consolas,monospace;letter-spacing:2px}}{CSS}</style>
<defs><pattern id="dz-grid" width="32" height="32" patternUnits="userSpaceOnUse"><path d="M32 0H0V32" fill="none" stroke="#202736" stroke-width=".5"/></pattern><clipPath id="dz-clip"><rect width="{w}" height="{h}" rx="12"/></clipPath></defs>
<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="12" fill="#06080d" stroke="#293341"/>
<g clip-path="url(#dz-clip)"><rect width="{w}" height="{h}" fill="url(#dz-grid)"/>{body}</g></svg>
'''

def sparks(w,h,n=18):
    return "".join(f'<circle cx="{35+(i*137)%(w-65)}" cy="{60+(i*71)%(h-80)}" r="{1+i%3*.5}" fill="{A if i%3 else T}" opacity=".15" class="dz-spark" style="animation-delay:-{i*.7}s;animation-duration:{8+i%5}s"/>' for i in range(n))

def hero(mobile=False):
    path=ROOT/"scripts"/"templates"/("hero-mobile.svg" if mobile else "hero.svg")
    source=path.read_text().replace("<style>","<style>"+CSS,1)
    source=source.replace('font-weight="900" letter-spacing="-5"','font-weight="900" letter-spacing="-5" class="dz-glow"')
    source=source.replace('font-weight="900" letter-spacing="-4"','font-weight="900" letter-spacing="-4" class="dz-glow"')
    # Background particles stay behind the text.
    at=source.index('<path d="M0 0H')
    source=source[:at]+sparks(600 if mobile else 1200,560 if mobile else 540)+source[at:]
    if mobile:
        decoration='<g transform="translate(529 489)"><g class="dz-turn"><circle r="33" fill="none" stroke="#54cbd5" stroke-dasharray="32 24" opacity=".6"/></g></g>'
        return source.replace("</svg>",decoration+"</svg>")
    radar='''<g transform="translate(184 174)"><g class="dz-turn"><path d="M0 0L0-137A137 137 0 0 1 97-97Z" fill="#54cbd5" opacity=".08"/><path d="M0 0V-137" stroke="#54cbd5" opacity=".55"/></g></g>'''
    plane=f'<g class="dz-plane" transform="translate(9 44) rotate(39)"><path d="M24 0L-12-5-5 0-12 5Z M-1 0L-8-17-12-17-7 0-12 17-8 17Z" fill="{FG}" stroke="#06080d" stroke-width="1"/></g>'
    pings="".join(f'<g transform="translate({x} {y})"><circle r="4" fill="{T}"/><circle r="12" fill="none" stroke="{T}" class="dz-hop dz-glow" style="animation-delay:-{i}s"/></g>' for i,(x,y) in enumerate([(115,106),(265,212),(116,252)]))
    # Place the sweep before the drop marker; place plane above the terrain.
    source=source.replace('<g transform="translate(190 177)">',radar+pings+'<g transform="translate(190 177)">')
    source=source.replace('</g></svg>',plane+'</g></svg>')
    return source

def divider(label,number):
    w,h=1200,74
    body=f'<path d="M20 37H1180" stroke="#2b443a"/><path d="M20 37H1180" stroke="{A}" stroke-width="2" stroke-dasharray="28 240" class="dz-run"/><path d="M24 18L43 37 24 56 5 37Z" fill="#06080d" stroke="{A}" class="dz-glow"/>'
    body+=f'<rect x="61" y="17" width="540" height="40" fill="#06080d"/>'
    body+=txt(75,44,f"{number} / {label}",17,A,'class="mono"')
    body+=f'<g transform="translate(1150 37)"><g class="dz-turn"><path d="M-13-13h9m8 0h9v9m0 8v9h-9m-8 0h-9v-9m0-8v-9" fill="none" stroke="{T}"/></g></g>'
    return svg(w,h,label,body)

def lobby():
    body=sparks(1200,132,12)
    labels=[("DROP","Read the problem"),("LOOT","Find the evidence"),("BUILD","Test the system"),("REPEAT","Learn from the run")]
    for i,(head,sub) in enumerate(labels):
        x=20+i*296
        body+=f'<rect x="{x}" y="19" width="273" height="94" rx="7" fill="#10141b" stroke="#293341" class="dz-slot" style="animation-delay:-{8-i*2}s"/>'
        body+=txt(x+20,53,head,24,A,'font-weight="800"')+txt(x+20,84,sub,16,M)
    return svg(1200,132,"Drop. Loot. Build. Repeat. A builder's loop.",body)

def armory():
    body=txt(32,43,"LOADOUT / ALWAYS EVOLVING",15,A,'class="mono"')
    slots=[("PY","PYTHON","Agents + retrieval"),("JS","JAVASCRIPT","Web + desktop"),("TS","TYPESCRIPT","Apps + APIs"),("C++","C++","Systems + shells")]
    for i,(code,name,detail) in enumerate(slots):
        x=24+i*294
        body+=f'<rect x="{x}" y="64" width="272" height="172" rx="8" fill="#10141b" stroke="#293341" class="dz-slot" style="animation-delay:-{i*2}s"/>'
        body+=txt(x+18,133,code,47,T,'font-weight="900" class="dz-glow"')
        body+=txt(x+18,175,name,16,FG,'class="mono"')+txt(x+18,205,detail,16,M)
        body+="".join(f'<rect x="{x+201+j*10}" y="{100-j*6}" width="5" height="{15+j*6}" fill="{A}" class="dz-eq" style="animation-delay:-{j*.3+i}s"/>' for j in range(4))
    return svg(1200,260,"Python, JavaScript, TypeScript and C++ — developer loadout.",body)

def victory():
    body=sparks(1200,260,25)
    body+=txt(40,45,"NEXT MATCH / YOUR NEXT IDEA",16,T,'class="mono"')
    body+=txt(38,105,"WINNER WINNER.",48,A,'font-weight="900" class="dz-glow"')
    body+=txt(38,158,"CLEANER CODE.",48,FG,'font-weight="900"')
    body+=txt(41,211,"Good comms. Better builds. Let's squad up.",21,M)
    # Supply crate suspended below a parachute; slowly descends and rises.
    body+='<g transform="translate(1040 95)"><g class="dz-drop">'
    body+=f'<path d="M-70 0Q0-95 70 0Q35-20 0 0Q-35-20-70 0Z" fill="#223d35" stroke="{T}" stroke-width="2"/><path d="M-70 0L-25 70M70 0L25 70M0 0V70" fill="none" stroke="#8faea5"/>'
    body+=f'<rect x="-30" y="70" width="60" height="45" rx="4" fill="#77581d" stroke="{A}" stroke-width="2"/><path d="M-30 83H30M-13 70V115M13 70V115" stroke="{A}"/></g></g>'
    return svg(1200,260,"Winner winner. Cleaner code. Good comms, better builds.",body)

def button(label,color):
    return svg(350,78,label,f'<rect x="3" y="3" width="344" height="72" rx="10" fill="none" stroke="{color}" stroke-width="2" stroke-dasharray="35 400" class="dz-run"/><circle cx="29" cy="39" r="5" fill="{color}" class="dz-glow"/>'+txt(53,47,label,19,FG,'font-weight="700"')+f'<path d="M302 39H325M318 32L325 39 318 46" fill="none" stroke="{color}" stroke-width="2"/>')

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    files={"hero.svg":hero(),"hero-mobile.svg":hero(True),"lobby.svg":lobby(),"victory.svg":victory()}
    for num,label,slug in [("01","PLAYER BRIEF","brief"),("02","FEATURED LOADOUT","loadout"),("03","MISSION REPLAY","replay"),("04","PROJECT LOBBY","projects"),("05","MATCH HISTORY","history"),("06","BUILD KIT","kit"),("07","CAREER CAMPAIGN","career"),("08","SQUAD UP","contact")]:
        files["divider-"+slug+".svg"]=divider(label,num)
    for label,name,color in [("LINKEDIN","linkedin",T),("EMAIL","email",A),("EXPLORE REPOS","repos","#a8b9ff")]:
        files["button-"+name+".svg"]=button(label,color)
    for name,content in files.items():
        (OUT/name).write_text(content)
    print(f"Built {len(files)} Drop Zone graphics.")

if __name__=="__main__":
    main()
