#!/usr/bin/env python3
"""Cinematic framing for the existing SVG-based profile; standard library only."""
from pathlib import Path
from html import escape
import math
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"assets/cinema"
CSS="""
text{font-family:Arial,Helvetica,sans-serif}.mono{font-family:Consolas,monospace;letter-spacing:2px}
.film-dust{animation:film-dust 12s linear infinite}
.film-orbit{animation:film-orbit 24s linear infinite;transform-origin:0 0}
.film-haze{animation:film-haze 18s ease-in-out infinite alternate}
.film-light{animation:film-light 9s ease-in-out infinite}
.film-trace{stroke-dasharray:90 1110;animation:film-trace 14s linear infinite}
.film-credit{animation:film-credit 22s linear infinite}
.film-title{animation:film-title 12s ease-in-out infinite;transform-box:fill-box;transform-origin:left center}
@keyframes film-dust{0%{transform:translate(0,12px);opacity:0}20%,70%{opacity:.5}100%{transform:translate(35px,-55px);opacity:0}}
@keyframes film-orbit{to{transform:rotate(360deg)}}
@keyframes film-haze{to{transform:translateX(80px)}}
@keyframes film-light{50%{opacity:.35}}
@keyframes film-trace{to{stroke-dashoffset:-1200}}
@keyframes film-credit{to{transform:translateY(-240px)}}
@keyframes film-title{50%{transform:scale(1.015)}}
@media(prefers-reduced-motion:reduce){*{animation:none!important}}
"""
def t(x,y,s,size=16,c="#eaf0f7",a=""):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{c}" {a}>{escape(s)}</text>'
def frame(w,h,title,body,defs=""):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="film-title">
<title id="film-title">{escape(title)}</title><style>{CSS}</style>
<defs><radialGradient id="film-glow"><stop stop-color="#1d6570" stop-opacity=".38"/><stop offset="1" stop-color="#030509" stop-opacity="0"/></radialGradient>{defs}</defs>
<rect width="{w}" height="{h}" rx="12" fill="#030509"/><rect x="1" y="1" width="{w-2}" height="{h-2}" rx="11" fill="none" stroke="#28333f"/>
{body}</svg>'''
def dust(w,h):
    return "".join(f'<circle cx="{25+(i*173)%(w-55)}" cy="{55+(i*79)%(h-95)}" r="{.8+(i%3)*.6}" fill="#ffc247" opacity=".16" class="film-dust" style="animation-delay:-{i*.45}s"/>' for i in range(24))
def opening():
    b='<ellipse cx="908" cy="310" rx="425" ry="275" fill="url(#film-glow)"/>'
    b+='<g class="film-haze" opacity=".22"><path d="M500 380Q800 230 1199 325V384Q830 280 500 420Z" fill="#1e3d4a"/><path d="M430 420Q800 320 1199 410V450Q880 365 430 445Z" fill="#38616a"/></g>'
    b+=dust(1200,600)
    b+='<path d="M0 482H1200M100 550L700 360M370 550L760 360M650 550L820 360M930 550L880 360M1200 550L940 360" stroke="#192633" stroke-width="1"/>'
    b+='<rect x="0" y="0" width="1200" height="47" fill="#020305"/><rect x="0" y="551" width="1200" height="49" fill="#020305"/>'
    b+=t(36,29,"ADITYA2514 PRESENTS",12,"#94a7b9",'class="mono"')
    b+=t(1164,29,"AN ENGINEERING DOSSIER",12,"#94a7b9",'text-anchor="end" class="mono"')
    b+='<g class="film-title">'
    b+=t(47,186,"DROP",114,"#eef3f8",'font-weight="900" letter-spacing="-5"')
    b+=t(47,296,"ZONE.",114,"#ffc247",'font-weight="900" letter-spacing="-5"')+'</g>'
    b+=t(53,355,"THE ADITYA SINGH DOSSIER",24,"#dbe7f3",'font-weight="700" letter-spacing="3"')
    b+=t(53,393,"The drop is just the beginning.",22,"#96aabc")
    b+=t(53,473,"LLM SYSTEMS  /  AI AGENTS  /  FULL-STACK",15,"#54cbd5",'class="mono"')
    b+='<g transform="translate(945 286)">'
    b+='<circle r="142" fill="#080f17" fill-opacity=".7" stroke="#325361"/>'
    b+='<g class="film-orbit"><circle r="160" fill="none" stroke="#54cbd5" stroke-width="2" stroke-dasharray="200 45 28 45 200 45 28 415"/><path d="M0-173V-149M173 0H149M0 173V149M-173 0H-149" stroke="#ffc247" stroke-width="3"/></g>'
    b+='<path d="M-105-61L0-121 105-61V61L0 121-105 61Z" fill="none" stroke="#d8aa4c" stroke-opacity=".5"/>'
    b+=t(0,25,"AS",93,"#eaf0f7",'text-anchor="middle" font-weight="900" letter-spacing="-5"')
    b+=t(0,66,"OPERATOR / 2514",12,"#54cbd5",'text-anchor="middle" class="mono"')+'</g>'
    b+='<path d="M36 551H1164" stroke="#ffc247" stroke-width="2" class="film-trace"/>'
    b+=t(36,581,"READ THE PROBLEM. CHECK THE SYSTEM. SHIP THE FIX.",12,"#91a4b8",'class="mono"')
    b+=t(1164,581,"CHAPTER 00 / THE DROP",12,"#ffc247",'text-anchor="end" class="mono"')
    return frame(1200,600,"Drop Zone — The Aditya Singh Dossier. A cinematic engineering résumé.",b)
def mobile():
    b='<ellipse cx="470" cy="360" rx="300" ry="230" fill="url(#film-glow)"/>'+dust(600,650)
    b+=t(30,43,"ADITYA2514 PRESENTS",14,"#91a4b8",'class="mono"')
    b+=t(26,177,"DROP",111,"#edf2f7",'font-weight="900" letter-spacing="-5"')
    b+=t(26,284,"ZONE.",111,"#ffc247",'font-weight="900" letter-spacing="-5"')
    b+=t(32,341,"THE ADITYA SINGH",25,"#eaf0f7",'font-weight="700" letter-spacing="2"')
    b+=t(32,377,"DOSSIER",25,"#eaf0f7",'font-weight="700" letter-spacing="2"')
    b+=t(32,431,"The drop is just the beginning.",22,"#9eafbf")
    b+=t(32,493,"LLM systems / AI agents",21,"#54cbd5")
    b+=t(32,528,"Full-stack engineering",21,"#54cbd5")
    b+='<path d="M30 575H570" stroke="#ffc247" class="film-trace" stroke-width="2"/>'
    b+=t(32,612,"CHAPTER 00 / THE DROP",14,"#ffc247",'class="mono"')
    return frame(600,650,"Drop Zone — The Aditya Singh Dossier.",b)
CHAPTERS=[
("brief","01","THE OPERATOR","Meet the builder behind the systems."),
("loadout","02","THE SIGNATURE BUILDS","Four projects. Four engineering problems."),
("utilities","03","THE UTILITY BELT","Competitive energy. Practical engineering."),
("replay","04","THE MISSION REPLAY","Follow the checks behind a contract review."),
("projects","05","THE EXPANDING LOBBY","A growing collection of things worth building."),
("history","06","THE LONG GAME","Real contributions. Consistent progress."),
("kit","07","THE BUILD KIT","Choose the right tool for the next problem."),
("career","08","THE JOURNEY","Education, milestones and the work between."),
("contact","09","THE NEXT CHAPTER","A conversation can become the next build.")
]
def chapter(slug,number,title,subtitle):
    b=t(1160,151,number,161,"#14212d",'font-weight="900" text-anchor="end"')
    b+=t(34,40,"CHAPTER "+number,12,"#ffc247",'class="mono"')
    b+=t(32,92,title,34,"#edf3f9",'font-weight="800"')
    b+=t(34,131,subtitle,18,"#9aafc3")
    b+='<path d="M34 161H1166" stroke="#263443"/><path d="M34 161H1166" stroke="#ffc247" class="film-trace" stroke-width="2"/>'
    return frame(1200,184,title,b)
def credits():
    b='<ellipse cx="880" cy="250" rx="400" ry="240" fill="url(#film-glow)"/>'+dust(1200,420)
    b+=t(39,45,"END OF THIS REEL / START OF THE NEXT BUILD",13,"#54cbd5",'class="mono"')
    b+=t(36,139,"TO BE",66,"#edf2f7",'font-weight="900"')
    b+=t(36,209,"CONTINUED.",66,"#ffc247",'font-weight="900"')
    b+=t(41,265,"Bring a problem. Let's build the next chapter.",21,"#9eafc0")
    b+=t(41,326,"AI ENGINEERING  /  COLLABORATION  /  INTERNSHIPS",13,"#54cbd5",'class="mono"')
    defs='<clipPath id="credit-window"><rect x="770" y="75" width="395" height="240"/></clipPath>'
    b+='<g clip-path="url(#credit-window)"><g class="film-credit">'
    credits=[("THE BUILDER","Aditya Singh"),("THE FOCUS","LLM systems · agents · full-stack"),("THE NEXT CHAPTER","Built with you")]
    for repeat in range(2):
        for i,(label,value) in enumerate(credits):
            y=108+i*80+repeat*240
            b+=t(790,y,label,12,"#ffc247",'class="mono"')
            b+=t(790,y+28,value,19,"#d8e2ed")
    b+='</g></g>'
    b+='<path d="M40 370H1160" stroke="#293341"/><path d="M40 370H1160" stroke="#ffc247" class="film-trace" stroke-width="2"/>'
    b+=t(40,400,"GG. NOW GO INSPECT THE CODE.",12,"#91a4b8",'class="mono"')
    return frame(1200,420,"To be continued — build the next chapter with Aditya Singh.",b,defs)
def main():
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/"opening.svg").write_text(opening())
    (OUT/"opening-mobile.svg").write_text(mobile())
    (OUT/"credits.svg").write_text(credits())
    for args in CHAPTERS:(OUT/("chapter-"+args[0]+".svg")).write_text(chapter(*args))
    print("Built opening titles, nine chapter transitions and closing credits.")
if __name__=="__main__":main()
