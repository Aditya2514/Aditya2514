#!/usr/bin/env python3
"""Original game-inspired scope and utility animations; no external assets."""
from pathlib import Path
from html import escape
import math
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"assets"/"actions"
GOLD="#ffc247"
CYAN="#54cbd5"
WHITE="#edf2f7"
MUTED="#9daab9"
CSS="""
text{font-family:Arial,Helvetica,sans-serif}.mono{font-family:Consolas,monospace;letter-spacing:2px}
.a-scope{animation:a-scope 10s ease-in-out infinite;transform-origin:0 0}
.a-target{animation:a-target 10s ease-in-out infinite}
.a-cross{animation:a-cross 10s ease-in-out infinite}
.a-hit{opacity:0;animation:a-hit 10s ease-in-out infinite}
.a-confirm{opacity:0;animation:a-confirm 10s ease-in-out infinite}
.a-trace{stroke-dasharray:38 600;animation:a-trace 8s linear infinite}
.a-glow{animation:a-glow 5s ease-in-out infinite}
.a-smoke{animation:a-smoke 7s ease-out infinite;transform-box:fill-box;transform-origin:center}
.a-frag{animation:a-frag 8s ease-in-out infinite}
.a-burst{opacity:0;animation:a-burst 8s ease-out infinite;transform-origin:100px 143px}
.a-flame{animation:a-flame 3s ease-in-out infinite;transform-box:fill-box;transform-origin:bottom}
.a-can{animation:a-can 4s ease-in-out infinite}
.a-energy{animation:a-energy 4s ease-in-out infinite;transform-box:fill-box;transform-origin:bottom}
.a-feed{animation:a-feed 12s linear infinite}
@keyframes a-scope{0%,10%{transform:scale(.82) rotate(-5deg);opacity:.6}30%,68%{transform:scale(1) rotate(0);opacity:1}80%,100%{transform:scale(.82) rotate(-5deg);opacity:.6}}
@keyframes a-target{0%,12%{transform:translate(48px,-28px)}32%,70%{transform:translate(0,0)}85%,100%{transform:translate(48px,-28px)}}
@keyframes a-cross{0%,20%{stroke:#54cbd5}35%,70%{stroke:#ffc247}80%,100%{stroke:#54cbd5}}
@keyframes a-hit{0%,43%,78%,100%{opacity:0}49%,63%{opacity:1}}
@keyframes a-confirm{0%,45%,82%,100%{opacity:0;transform:translateY(8px)}51%,74%{opacity:1;transform:translateY(0)}}
@keyframes a-trace{to{stroke-dashoffset:-638}}
@keyframes a-glow{50%{opacity:.5}}
@keyframes a-smoke{0%{transform:translate(0,15px) scale(.55);opacity:0}20%{opacity:.4}70%{opacity:.22}100%{transform:translate(25px,-55px) scale(1.45);opacity:0}}
@keyframes a-frag{0%,12%{transform:translate(-30px,35px) rotate(-20deg)}40%,60%{transform:translate(25px,-25px) rotate(80deg)}75%,100%{transform:translate(-30px,35px) rotate(-20deg)}}
@keyframes a-burst{0%,40%,85%,100%{opacity:0;transform:scale(.4)}50%{opacity:.8;transform:scale(.9)}75%{opacity:0;transform:scale(1.5)}}
@keyframes a-flame{50%{transform:scaleX(.8) scaleY(1.15);opacity:.75}}
@keyframes a-can{50%{transform:translateY(-9px)}}
@keyframes a-energy{0%,100%{transform:scaleY(.25)}50%{transform:scaleY(1)}}
@keyframes a-feed{0%,100%{transform:translateX(0)}50%{transform:translateX(-12px)}}
@media(prefers-reduced-motion:reduce){*{animation:none!important}.a-hit,.a-confirm{opacity:1}.a-smoke{opacity:.2}}
"""
def text(x,y,s,size=16,fill=WHITE,attrs=""):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" {attrs}>{escape(s)}</text>'
def svg(w,h,title,body):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="a-title">
<title id="a-title">{escape(title)}</title><style>{CSS}</style>
<defs><pattern id="a-grid" width="36" height="36" patternUnits="userSpaceOnUse"><path d="M36 0H0V36" fill="none" stroke="#202736" stroke-width=".5"/></pattern><radialGradient id="a-glass"><stop stop-color="#182c35"/><stop offset="1" stop-color="#080c12"/></radialGradient><clipPath id="a-clip"><rect x="1" y="1" width="{w-2}" height="{h-2}" rx="12"/></clipPath></defs>
<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="12" fill="#06080d" stroke="#293341"/>
<g clip-path="url(#a-clip)"><rect width="{w}" height="{h}" fill="url(#a-grid)"/>{body}</g>
<path d="M16 1H{w-16}" fill="none" stroke="{GOLD}" stroke-width="2" class="a-trace"/>
</svg>'''
def scope():
    body=text(42,45,"SCOPE IN / DEBUG MODE",15,CYAN,'class="mono"')
    body+=text(40,132,"PATT SE",70,WHITE,'font-weight="900"')
    body+=text(40,210,"HEADSHOT!",70,GOLD,'font-weight="900"')
    body+=text(44,254,"AIM AT THE BUG. SHIP THE FIX.",21,MUTED,'font-weight="700"')
    body+=f'<g class="a-confirm"><rect x="44" y="284" width="393" height="46" rx="4" fill="#222014" stroke="{GOLD}"/>'
    body+=text(62,314,"BUG ELIMINATED / NEXT COMMIT",17,GOLD,'class="mono"')+'</g>'
    # A symbolic bug target inside the scope, never a person.
    body+='<g transform="translate(940 204)"><g class="a-scope">'
    body+=f'<circle r="164" fill="#0a1018" stroke="#303c4b" stroke-width="15"/><circle r="150" fill="url(#a-glass)" stroke="{CYAN}" stroke-opacity=".6"/>'
    body+=''.join(f'<path d="M{142*math.cos(i*math.pi/12):.2f} {142*math.sin(i*math.pi/12):.2f}L{(129 if i%3==0 else 136)*math.cos(i*math.pi/12):.2f} {(129 if i%3==0 else 136)*math.sin(i*math.pi/12):.2f}" stroke="#627b8c"/>' for i in range(24))
    body+='<g class="a-target">'
    body+=f'<rect x="-34" y="-39" width="68" height="78" rx="15" fill="#301d24" stroke="#ee7180" stroke-width="2"/><path d="M0-35V35M-34-20L-51-35M-34 0H-56M-34 20L-51 35M34-20L51-35M34 0H56M34 20L51 35" fill="none" stroke="#ee7180" stroke-width="3"/>'
    body+=text(0,7,"BUG",15,WHITE,'text-anchor="middle" font-weight="700"')+'</g>'
    body+=f'<g fill="none" stroke="{CYAN}" stroke-width="1.5" class="a-cross"><path d="M-147 0H-47M47 0H147M0-147V-47M0 47V147"/><circle r="45"/><path d="M-10 0H10M0-10V10"/><path d="M-25 75H25M-17 96H17M-9 116H9"/></g>'
    body+='<g stroke="#ffc247" stroke-width="5" class="a-hit"><path d="M-47-47L-28-28M47-47L28-28M-47 47L-28 28M47 47L28 28"/></g>'
    body+='</g>'+text(0,194,"4x / BUG HUNT",13,CYAN,'class="mono" text-anchor="middle"')+'</g>'
    for i,(a,b) in enumerate([("01","SCOUT"),("02","SCOPE"),("03","LOCK"),("04","DEBUG")]):
        x=44+i*163
        body+=f'<path d="M{x} 372h135" stroke="#303c4b" stroke-width="3"/><path d="M{x} 372h135" stroke="{GOLD}" stroke-width="3" class="a-trace" style="animation-delay:-{i*2}s"/>'
        body+=text(x,400,a+" / "+b,13,MUTED,'class="mono"')
    return svg(1200,430,"Patt se headshot! A scope tracks a symbolic software bug, locks on and confirms the hit.",body)
def utility(kind):
    specs={
      "smoke":("01 / SMOKE","SMOKE DAAL.","NOISE HATA.","Retrieve the signal. Cite the source.",CYAN),
      "frag":("02 / FRAG","FRAG OUT.","BUG OUT.","Find the edge case. Test the fix.",GOLD),
      "molotov":("03 / MOLOTOV","DEBT JALAO.","CLEAN BUILD.","Refactor the mess. Keep the logic.","#ff9360"),
      "boost":("04 / ENERGY","BOOST ON.","BUILD ON.","Next idea. Next commit. Repeat.","#a9a2ff")}
    tag,a,b,sub,c=specs[kind]
    body=text(24,34,tag,12,c,'class="mono"')
    body+='<path d="M186 58V226" stroke="#293341"/>'
    body+=text(210,103,a,29,WHITE,'font-weight="900"')+text(210,143,b,29,c,'font-weight="900"')
    body+=text(210,186,sub,15,MUTED)
    body+=f'<path d="M210 219H572" stroke="{c}" stroke-width="2" class="a-trace"/>'
    if kind=="smoke":
        for i,(x,y) in enumerate([(76,121),(113,105),(81,83),(130,77)]):
            body+=f'<ellipse cx="{x}" cy="{y}" rx="26" ry="24" fill="#a7bdc5" opacity=".14" class="a-smoke" style="animation-delay:-{i*1.6}s"/>'
        body+=f'<g transform="translate(83 150) rotate(-12)"><rect x="0" y="0" width="38" height="67" rx="7" fill="#273a3b" stroke="{CYAN}" stroke-width="2"/><rect x="0" y="23" width="38" height="21" fill="#a18443"/><rect x="7" y="-9" width="24" height="11" rx="3" fill="#a5b5b7"/><path d="M24-10Q47-24 42-5" fill="none" stroke="#a5b5b7" stroke-width="3"/></g>'
    elif kind=="frag":
        body+=f'<path d="M40 202Q70 69 147 112" fill="none" stroke="#536b7c" stroke-dasharray="4 7"/>'
        body+='<g transform="translate(86 153)"><g class="a-frag">'
        body+=f'<rect x="-11" y="-38" width="22" height="14" fill="#b5bca3"/><ellipse rx="25" ry="34" fill="#46583b" stroke="#94a477" stroke-width="2"/><path d="M-21-17H21M-25 0H25M-21 17H21M-9-30V30M9-30V30" stroke="#182516" stroke-width="3"/><path d="M8-39Q35-55 29-30" fill="none" stroke="#c0c7a8" stroke-width="3"/></g></g>'
        body+=f'<g class="a-burst" fill="none" stroke="{GOLD}" stroke-width="2"><circle cx="100" cy="143" r="38"/><path d="M100 84V100M100 186V202M41 143H58M142 143H160M58 101L70 113M130 173L143 186M58 186L70 174M130 113L143 100"/></g>'
    elif kind=="molotov":
        body+='<g transform="translate(92 146) rotate(14)">'
        body+=f'<path d="M-10-42H10V-16L23 0V62Q0 71-23 62V0L-10-16Z" fill="#314133" stroke="#8b9d7c" stroke-width="2"/><rect x="-18" y="16" width="36" height="25" fill="#8a7145"/><path d="M-10-42Q8-66 23-54" fill="none" stroke="#bfb6a3" stroke-width="6"/>'
        body+=f'<path d="M13-51Q-8-70 15-98Q9-78 27-86Q45-62 13-51Z" fill="#f4a33c" class="a-flame"/><path d="M15-56Q7-70 21-79Q31-65 15-56Z" fill="#ffe59a" class="a-flame"/></g>'
    else:
        body+='<g transform="translate(77 91)"><g class="a-can">'
        body+=f'<rect width="58" height="118" rx="12" fill="#202e58" stroke="#a9a2ff" stroke-width="2"/><ellipse cx="29" cy="8" rx="27" ry="7" fill="#aeb7cc"/><ellipse cx="29" cy="5" rx="8" ry="3" fill="#293341"/><path d="M32 30L13 65H29L22 91 46 52H30Z" fill="#d4cfff"/>'
        body+='</g></g>'
        body+=f'<rect x="149" y="95" width="8" height="112" rx="4" fill="#2b2444"/><rect x="149" y="95" width="8" height="112" rx="4" fill="#a9a2ff" class="a-energy"/>'
    return svg(600,260,tag+" — "+a+" "+b+" "+sub,body)
def feed():
    body=text(25,34,"DEV FEED / ILLUSTRATIVE",12,CYAN,'class="mono"')
    rows=[("ADITYA2514","scoped","BUG","PATT SE HEADSHOT!",GOLD),("NOESIS","cleared","NOISE","SMOKE SUCCESS",CYAN),("YOU + ME","queued","NEXT BUILD","SQUAD READY","#a9a2ff")]
    for i,(who,verb,target,result,c) in enumerate(rows):
        y=66+i*48
        body+=f'<g class="a-feed" style="animation-delay:-{i*3}s"><rect x="22" y="{y-23}" width="1156" height="39" rx="5" fill="#10141b" stroke="#293341"/>'
        body+=text(42,y,who,16,c,'font-weight="700"')+text(238,y,verb,15,MUTED)
        body+=f'<path d="M342 {y-6}h42m-7-5 7 5-7 5" fill="none" stroke="{c}"/>'
        body+=text(414,y,target,16,WHITE,'font-weight="700"')+text(1152,y,result,15,c,'text-anchor="end" class="mono"')+'</g>'
    return svg(1200,203,"Illustrative developer feed: bugs scoped, noise cleared, squad ready.",body)
def main():
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/"scope.svg").write_text(scope())
    (OUT/"dev-feed.svg").write_text(feed())
    for name in ["smoke","frag","molotov","boost"]:(OUT/(name+".svg")).write_text(utility(name))
    print("Built scope, developer feed and four utility animations.")
if __name__=="__main__":main()
