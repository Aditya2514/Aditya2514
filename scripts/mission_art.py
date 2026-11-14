"""Cinematic Drop Zone artwork. All SVG images are self-contained and script-free.

Each scene is a painted JPEG with motion layered on top of it. Effects are drawn in the
painting's own coordinates, so they stay locked to the art on desktop and phone crops.
Everything that moves carries class "fx" and is hidden under prefers-reduced-motion.
"""
import base64
from html import escape
import json
import math
from pathlib import Path
import textwrap

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assets/mission'
BG='#0d1117'; PANEL='#161b22'; LINE='#30363d'; WHITE='#e6edf3'
MUTED='#a8b3bf'; GOLD='#e9b44c'; CYAN='#70c9cb'; LAV='#b6a7dc'; RED='#f0655a'; GREEN='#6fd69b'
FONT='text{font-family:Arial,Helvetica,sans-serif}.mono{font-family:Consolas,Menlo,monospace;letter-spacing:2px}.tag{font-family:Consolas,Menlo,monospace;letter-spacing:1px}'
CSS=FONT+'''
.trace{stroke-dasharray:160 1240;animation:trace 9s linear infinite}
.pulse{animation:pulse 3.2s ease-in-out infinite}
.blink{animation:blink 1.1s steps(2) infinite}
.spin{transform-box:fill-box;transform-origin:center;animation:spin 40s linear infinite}
.kb{animation:kb 26s ease-in-out infinite alternate}
.spark{animation:spark 7s ease-out infinite}
.ring{transform-box:fill-box;transform-origin:center;animation:ring 3.6s ease-out infinite}
.glint{animation:glint 7s ease-in-out infinite}
.shine{animation:shine 6s ease-in-out infinite}
.ga{animation:ga 7s steps(1) infinite}.gb{animation:gb 7s steps(1) infinite}
.sweepy{animation:sweepy 4.5s ease-in-out infinite}
.draw{stroke-dasharray:400;animation:draw 5s ease-in-out infinite}
.march{stroke-dasharray:6 8;animation:march 1.2s linear infinite}
.compass{animation:compass 50s linear infinite}
.kf{animation:kf 10s ease-out infinite backwards}
.st{animation:st 9s linear infinite backwards}
.fill{transform-box:fill-box;transform-origin:left;animation:fill 9s linear infinite backwards}
.pop{animation:pop var(--loop,8s) linear infinite backwards}
.chev{animation:chev 1.8s linear infinite backwards}
.drift{animation:drift 16s ease-in-out infinite alternate}
.eq{animation:eq 12s linear infinite backwards}
.drop{animation:drop 16s linear infinite}
.fly{animation:fly 16s linear infinite}
.smoke{animation:smoke 5s ease-out infinite}
@keyframes trace{to{stroke-dashoffset:-1400}}
@keyframes pulse{50%{opacity:.3}}
@keyframes blink{50%{opacity:0}}
@keyframes spin{to{transform:rotate(360deg)}}
@keyframes kb{from{transform:scale(1)}to{transform:scale(1.05)}}
@keyframes spark{0%{opacity:0;transform:translate(0,14px)}25%{opacity:.85}100%{opacity:0;transform:translate(var(--sx,12px),-70px)}}
@keyframes ring{0%{transform:scale(.15);opacity:.95}100%{transform:scale(1);opacity:0}}
@keyframes glint{0%,70%{transform:translateX(0);opacity:0}73%{opacity:.55}86%{transform:translateX(var(--dx,160px));opacity:.55}89%,100%{transform:translateX(var(--dx,160px));opacity:0}}
@keyframes shine{0%,35%{transform:translateX(0)}75%,100%{transform:translateX(var(--dx,700px))}}
@keyframes ga{0%,90%,96%,100%{opacity:0;transform:translate(0,0)}91%{opacity:.85;transform:translate(-7px,2px)}93%{opacity:.6;transform:translate(5px,-2px)}95%{opacity:.75;transform:translate(-3px,0)}}
@keyframes gb{0%,90%,96%,100%{opacity:0;transform:translate(0,0)}91%{opacity:.7;transform:translate(7px,-2px)}93%{opacity:.8;transform:translate(-5px,2px)}95%{opacity:.5;transform:translate(3px,0)}}
@keyframes sweepy{0%{transform:translateY(0);opacity:0}12%{opacity:.9}88%{opacity:.9}100%{transform:translateY(var(--dy,130px));opacity:0}}
@keyframes draw{0%{stroke-dashoffset:400;opacity:0}15%{opacity:1}60%,80%{stroke-dashoffset:0;opacity:1}100%{stroke-dashoffset:0;opacity:0}}
@keyframes march{to{stroke-dashoffset:-14}}
@keyframes compass{to{transform:translateX(-720px)}}
@keyframes kf{0%{opacity:0;transform:translateX(26px)}4%,60%{opacity:1;transform:translateX(0)}68%,100%{opacity:0;transform:translateX(0)}}
@keyframes st{0%,31%{opacity:1}36%,100%{opacity:.42}}
@keyframes fill{0%{transform:scaleX(0);opacity:1}31%{transform:scaleX(1);opacity:1}35%,100%{transform:scaleX(1);opacity:0}}
@keyframes pop{0%{opacity:0;transform:translateY(6px)}5%,82%{opacity:1;transform:translateY(0)}90%,100%{opacity:0;transform:translateY(0)}}
@keyframes chev{0%,100%{opacity:.15}30%{opacity:1}60%{opacity:.15}}
@keyframes drift{from{transform:translateX(0)}to{transform:translateX(-26px)}}
@keyframes eq{0%{opacity:0}1%,15%{opacity:1}18%,100%{opacity:0}}
@keyframes drop{0%{transform:translate(0,0);opacity:0}6%{opacity:1}70%{transform:translate(10px,104px);opacity:1}76%,100%{transform:translate(10px,104px);opacity:0}}
@keyframes fly{0%,8%{transform:translateX(0);opacity:0}10%{opacity:.9}40%{transform:translateX(-150px);opacity:.9}42%,100%{transform:translateX(-150px);opacity:0}}
@keyframes smoke{0%{transform:translate(0,0) scale(.5);opacity:0}20%{opacity:.75}100%{transform:translate(9px,-30px) scale(1.7);opacity:0}}
@media(prefers-reduced-motion:reduce){*{animation:none!important}.fx{display:none}}
'''
STILL_CSS=FONT+'.fx{display:none}'

def t(x,y,s,size=20,color=WHITE,attr=''):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" {attr}>{escape(str(s))}</text>'

def embedded(name,x,y,w,h):
    data=base64.b64encode((OUT/name).read_bytes()).decode()
    return f'<image x="{x}" y="{y}" width="{w}" height="{h}" preserveAspectRatio="xMidYMid slice" xlink:href="data:image/jpeg;base64,{data}"/>'

def frame(w,h,title,body,still=False,defs=''):
    css=STILL_CSS if still else CSS
    return f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title">
<title id="title">{escape(title)}</title><style>{css}</style><defs>
<clipPath id="bounds"><rect width="{w}" height="{h}" rx="14"/></clipPath>
<linearGradient id="fade" x1="0" y1="0" x2="0" y2="1"><stop stop-color="{BG}" stop-opacity="0"/><stop offset="1" stop-color="{BG}"/></linearGradient>
<linearGradient id="shade"><stop stop-color="{BG}" stop-opacity=".8"/><stop offset=".55" stop-color="{BG}" stop-opacity=".2"/><stop offset="1" stop-color="{BG}" stop-opacity="0"/></linearGradient>
<linearGradient id="band" x1="0" y1="0" x2="1" y2="0"><stop stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".85"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
{defs}</defs><rect width="{w}" height="{h}" rx="14" fill="{BG}"/>
<g clip-path="url(#bounds)">{body}</g><rect x="1" y="1" width="{w-2}" height="{h-2}" rx="13" fill="none" stroke="{LINE}"/></svg>\n'''

# ---------------------------------------------------------------- effect primitives
def glow(ident,color):
    return f'<radialGradient id="{ident}"><stop stop-color="{color}" stop-opacity=".55"/><stop offset="1" stop-color="{color}" stop-opacity="0"/></radialGradient>'

def embers(x0,y0,w,h,color,count=16,seed=3):
    """Small lights that rise and fade; positions are fixed so builds stay deterministic."""
    out=[]
    for i in range(count):
        x=x0+(i*73+seed*29)%w; y=y0+(i*41+seed*17)%h
        out.append(f'<circle cx="{x}" cy="{y}" r="{1+(i%3)*.6:.1f}" fill="{color}" class="spark fx" style="--sx:{-18+(i*13)%40}px;animation-delay:-{i*.47:.2f}s;animation-duration:{5+i%4}s"/>')
    return ''.join(out)

def rings(cx,cy,r,color,count=3,dur=3.6,sw=1.5,squash=1):
    out=f'<g class="fx" transform="translate({cx} {cy}) scale(1 {squash})">'
    for i in range(count):
        out+=f'<circle r="{r}" fill="none" stroke="{color}" stroke-width="{sw}" class="ring" style="animation-duration:{dur}s;animation-delay:-{i*dur/count:.2f}s"/>'
    return out+'</g>'

def glint(ident,points,x,y,w,h,dx,delay=0,dur=7):
    """A soft band of light that crosses a shape now and then (visor, shield, glass)."""
    return (f'<clipPath id="{ident}"><polygon points="{points}"/></clipPath><g clip-path="url(#{ident})" class="fx">'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="url(#band)" transform="skewX(-18)" class="glint" style="--dx:{dx}px;animation-delay:-{delay}s;animation-duration:{dur}s"/></g>')

def tag(x,y,label,color,delay,loop=8,anchor='start',size=11):
    """A small HUD callout that pops in at its moment in the loop."""
    w=len(label)*size*.66+16
    x0=x if anchor=='start' else x-w
    return (f'<g class="pop fx" style="--loop:{loop}s;animation-delay:{delay}s"><rect x="{x0:.0f}" y="{y-15}" width="{w:.0f}" height="21" rx="3" fill="{BG}" fill-opacity=".86" stroke="{color}"/>'
            +t(f'{x0+8:.0f}',y,label,size,color,'class="tag" font-weight="700"')+'</g>')

def shimmer(ident,text_svg,x,y,w,h,dx,delay=0):
    """Light passing across lettering: the text is the clip, a bright band slides behind it."""
    return (f'<clipPath id="{ident}">{text_svg}</clipPath><g clip-path="url(#{ident})" class="fx">'
            f'<rect x="{x-w}" y="{y}" width="{w}" height="{h}" fill="url(#band)" transform="skewX(-20)" class="shine" style="--dx:{dx}px;animation-delay:-{delay}s"/></g>')

def glitch(text_fn):
    """Two tinted ghosts of the lettering that jump for an instant every few seconds."""
    return f'<g class="ga fx">{text_fn("#59e3ff")}</g><g class="gb fx">{text_fn("#ff5a6e")}</g>'

def steps_row(x,y,w,h,labels,color,gap,num_size=15,label_size=14,mono=True):
    """Three boxes that light in turn while a bar fills along the active one."""
    out=''
    for i,label in enumerate(labels):
        bx=x+i*(w+gap)
        out+=f'<g class="st" style="animation-delay:{i*3}s"><rect x="{bx}" y="{y}" width="{w}" height="{h}" rx="7" fill="{BG}" fill-opacity=".9" stroke="{LINE}"/>'
        if mono:
            out+=t(bx+18,y+h/2+5,f'0{i+1}',num_size,color,'class="mono"')+t(bx+58,y+h/2+5,label,label_size,WHITE,'class="mono"')
        else:
            out+=t(bx+18,y+29,f'0{i+1}',13,color,'class="mono"')+t(bx+18,y+66,label,23)
        out+='</g>'
        out+=f'<rect class="fill fx" x="{bx+1}" y="{y+h-4}" width="{w-2}" height="3" rx="1.5" fill="{color}" style="animation-delay:{i*3}s"/>'
    return out

# ---------------------------------------------------------------- HUD pieces
def compass(x,y,w):
    """The heading tape from the top of the game screen, sliding slowly."""
    marks=['N','15','30','NE','60','75','E','105','120','SE','150','165','S','195','210','SW','240','255','W','285','300','NW','330','345']
    strip=''
    for k in range(len(marks)*2+8):
        label=marks[k%len(marks)]; px=k*30
        major=not label.isdigit()
        strip+=f'<path d="M{px} 18v{9 if major else 5}" stroke="{WHITE if major else MUTED}" stroke-width="{1.6 if major else 1}"/>'
        strip+=t(px,12,label,11 if major else 9,GOLD if label=='N' else (WHITE if major else MUTED),'text-anchor="middle" class="tag" font-weight="700"')
    return (f'<clipPath id="cmp"><rect x="{x}" y="{y}" width="{w}" height="30"/></clipPath>'
            f'<g opacity=".85"><rect x="{x}" y="{y}" width="{w}" height="30" fill="{BG}" fill-opacity=".45"/>'
            f'<g clip-path="url(#cmp)"><g transform="translate({x} {y})"><g class="compass">{strip}</g></g></g>'
            f'<path d="M{x+w/2-5} {y-4}h10l-5 7z" fill="{GOLD}"/><path d="M{x} {y+30}h{w}" stroke="{LINE}"/></g>')

def killfeed(x,y,commits,owner='Aditya2514'):
    """Recent real commits, shown the way the game announces eliminations."""
    out=''
    for i,c in enumerate(commits[:3]):
        title=' '.join(str(c.get('title','')).split())
        if len(title)>24:title=title[:23].rstrip()+'…'
        repo=str(c.get('repo',''))[:14]
        ry=y+i*28
        out+=(f'<g class="kf fx" style="animation-delay:{i*1.3}s"><rect x="{x}" y="{ry}" width="348" height="23" rx="4" fill="{BG}" fill-opacity=".8" stroke="{LINE}"/>'
              +t(x+9,ry+16,owner[:10],11,GOLD,'class="tag" font-weight="700"')
              +f'<path d="M{x+92} {ry+11.5}h6m7 0h6" stroke="{MUTED}" stroke-width="1.4"/><circle cx="{x+101.5}" cy="{ry+11.5}" r="3.2" fill="none" stroke="{WHITE}" stroke-width="1.4"/>'
              +t(x+118,ry+16,repo,11,CYAN,'class="tag" font-weight="700"')
              +t(x+118+len(repo)*7.7+8,ry+16,title,10,MUTED,'class="tag"')+'</g>')
    return out

def minimap(cx,cy,r):
    """Round minimap: wobbly contour lines, a sweep, the closing zone and three marked drops."""
    lines=''
    for k in range(5):
        base=r*(.28+.2*k); pts=[]
        for a in range(0,360,12):
            rad=math.radians(a)
            rr=base*(1+.11*math.sin(3*rad+k)+.07*math.sin(5*rad+2*k))
            pts.append(f'{rr*math.cos(rad)+k*3-6:.1f},{rr*math.sin(rad)+k*2-4:.1f}')
        lines+=f'<polygon points="{" ".join(pts)}" fill="none" stroke="{CYAN}" stroke-opacity="{.5-.07*k:.2f}"/>'
    blips=''
    for (bx,by,color,delay) in ((-24,-18,GOLD,0),(26,-6,CYAN,1.2),(-6,27,LAV,2.4)):
        blips+=f'<circle cx="{bx}" cy="{by}" r="11" fill="none" stroke="{color}" class="ring fx" style="animation-delay:-{delay}s"/><circle cx="{bx}" cy="{by}" r="3.2" fill="{color}"/>'
    sweep=(f'<g class="fx"><path d="M0 0L0 {-r}A{r} {r} 0 0 1 {r*.64:.1f} {-r*.77:.1f}Z" fill="{GOLD}" fill-opacity=".16">'
           f'<animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="6s" repeatCount="indefinite"/></path></g>')
    zone=(f'<circle r="{r*.5:.0f}" fill="none" stroke="{WHITE}" stroke-opacity=".8" stroke-dasharray="3 4"/>'
          f'<circle class="fx" r="{r}" fill="none" stroke="#5aa9ff" stroke-width="2"><animate attributeName="r" values="{r*1.3:.0f};{r*.5:.0f};{r*.5:.0f}" keyTimes="0;.8;1" dur="12s" repeatCount="indefinite"/>'
          f'<animate attributeName="opacity" values="0;.9;.9;0" keyTimes="0;.08;.88;1" dur="12s" repeatCount="indefinite"/></circle>')
    return (f'<clipPath id="mm"><circle r="{r}"/></clipPath><g transform="translate({cx} {cy})"><circle r="{r}" fill="{BG}" fill-opacity=".88"/>'
            f'<g clip-path="url(#mm)"><path d="M{-r} 0H{r}M0 {-r}V{r}" stroke="{LINE}"/>{lines}{sweep}{zone}{blips}'
            f'<path d="M0-7L5 6 0 3-5 6Z" fill="{WHITE}"/></g><circle r="{r}" fill="none" stroke="{GOLD}" stroke-width="2"/>'
            f'<circle r="{r+6}" fill="none" stroke="{GOLD}" stroke-opacity=".5" stroke-dasharray="60 30 10 40" class="spin fx"/>'
            +t(0,-r-12,'N',11,GOLD,'text-anchor="middle" class="tag" font-weight="700"')+'</g>')

# ---------------------------------------------------------------- motion painted onto each artwork
def operator_fx():
    """Hero painting (1320x440): hologram, visor, airdrop beyond the hangar door, embers."""
    b=f'<ellipse cx="850" cy="300" rx="150" ry="100" fill="url(#g-cyan)" class="pulse fx" opacity=".5"/>'
    b+=rings(893,262,58,CYAN,3,3.2,1.6,.82)
    b+=f'<circle cx="899" cy="267" r="3.5" fill="#dffcff" class="pulse fx"/>'
    # scanline and a redrawn ridge on the holographic panel
    b+=(f'<clipPath id="holo"><polygon points="745,243 888,228 945,365 800,360"/></clipPath><g clip-path="url(#holo)" class="fx">'
        f'<g class="sweepy" style="--dy:140px"><rect x="740" y="210" width="210" height="16" fill="{CYAN}" fill-opacity=".16"/><path d="M740 226H950" stroke="#dffcff" stroke-width="1.6"/></g>'
        f'<path d="M790 338L812 304 830 320 852 296 876 318 902 306 930 330" fill="none" stroke="#dffcff" stroke-width="2" class="draw"/></g>')
    b+=glint('visor','1004,106 1096,90 1102,140 1010,152',930,80,46,90,210,0,7)
    # beyond the door: a plane passes, an airdrop comes down, signal smoke rises
    b+=(f'<clipPath id="sky"><polygon points="902,76 1003,76 1003,130 1012,205 902,205"/></clipPath><g clip-path="url(#sky)" class="fx">'
        f'<g class="fly"><path d="M1016 96l8-2h6l5-7h3l-3 7h5l3-3h2l-1.5 5 1.5 5h-2l-3-3h-5l3 7h-3l-5-7h-6z" fill="#1b2330"/></g>'
        f'<g class="drop"><path d="M934 84a11 9 0 0 1 22 0z" fill="{RED}"/><path d="M934 84l8 13M956 84l-8 13M945 84v13" stroke="#e8d9c0" stroke-width=".8"/><rect x="940" y="97" width="10" height="8" fill="#3d5a80" stroke="#e8d9c0" stroke-width=".7"/></g>'
        +''.join(f'<circle cx="957" cy="196" r="4" fill="{RED}" class="smoke" style="animation-delay:-{i*1.25}s"/>' for i in range(4))
        +f'</g><circle cx="981" cy="152" r="1.8" fill="{RED}" class="blink fx"/>')
    b+=embers(610,90,560,300,GOLD,18,3)
    return b

def lexguard_fx(tags=True):
    """LexGuard painting (1200x600): shield, laser sweep down the page, findings, vault dial."""
    b=f'<ellipse cx="712" cy="165" rx="140" ry="170" fill="url(#g-gold)" class="pulse fx" opacity=".55"/>'
    b+=glint('shield','605,72 712,15 822,76 800,215 712,300 625,215',560,0,60,320,330,2,6)
    b+=f'<circle cx="1025" cy="172" r="96" fill="none" stroke="{GOLD}" stroke-opacity=".4" stroke-width="2" stroke-dasharray="26 14 4 14" class="spin fx"/>'
    loop=8
    sweep=f'dur="{loop}s" repeatCount="indefinite" keyTimes="0;.5;.9;1"'
    b+=(f'<g class="fx"><path d="M720 300L1150 295" stroke="#ffd98a" stroke-width="9" stroke-opacity=".22" stroke-linecap="round"><animate attributeName="d" values="M722 300L1150 295;M668 410L1176 416;M722 300L1150 295;M722 300L1150 295" {sweep}/></path>'
        f'<path d="M720 300L1150 295" stroke="#fff1c9" stroke-width="2.2" stroke-linecap="round"><animate attributeName="d" values="M722 300L1150 295;M668 410L1176 416;M722 300L1150 295;M722 300L1150 295" {sweep}/></path>'
        f'<line x1="1074" y1="262" x2="1030" y2="298" stroke="#ffd98a" stroke-width="2" stroke-opacity=".8"><animate attributeName="x2" values="1030;1058;1030;1030" {sweep}/><animate attributeName="y2" values="298;414;298;298" {sweep}/></line></g>')
    b+=rings(965,408,30,GREEN,2,4,1.6,.5)
    if tags:
        b+=tag(760,338,'! NON-COMPETE',RED,1.0,loop)+tag(880,368,'! TRAINING BOND',RED,2.1,loop)+tag(716,400,'! PENALTY',GOLD,3.2,loop)
        b+=tag(1012,402,'S.74 VERIFIED',GREEN,4.6,loop)
    b+=embers(590,60,300,280,GOLD,12,5)
    return b

def pikina_fx(tags=True):
    """Pikina painting (1200x600): orbiting ring, core, energy pulses and a consent hologram."""
    b=f'<ellipse cx="825" cy="170" rx="120" ry="80" fill="url(#g-cyan)" class="pulse fx" opacity=".5"/>'
    orbit='M640 150a185 75 0 1 0 370 0a185 75 0 1 0-370 0'
    for i in range(3):
        b+=(f'<g class="fx"><circle r="9" fill="{CYAN}" fill-opacity=".3"/><circle r="3.6" fill="#e6feff"/>'
            f'<animateMotion dur="6s" begin="-{i*2}s" repeatCount="indefinite" path="{orbit}"/></g>')
    b+=f'<rect x="800" y="143" width="44" height="44" fill="none" stroke="#dffcff" stroke-opacity=".75" stroke-width="1.4" class="spin fx" style="animation-duration:9s"/>'
    b+=f'<path d="M825 266V196" stroke="#dffcff" stroke-width="2.4" stroke-opacity=".8" class="march fx"/>'
    b+=rings(825,278,190,CYAN,3,4.2,1.6,.28)
    for (x,y,w,h,delay) in ((660,400,46,4,0),(871,368,4,52,.8),(1000,318,30,3,1.6),(1098,262,70,3,.4)):
        b+=f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="1.5" fill="#bffbff" class="pulse fx" style="animation-delay:-{delay}s"/>'
    b+=f'<ellipse cx="1092" cy="128" rx="60" ry="26" fill="#ffe9b0" fill-opacity=".14" class="pulse fx" style="animation-duration:5s"/>'
    if tags:
        loop=10; x,y=452,104
        b+=(f'<g class="pop fx" style="--loop:{loop}s;animation-delay:.4s"><rect x="{x}" y="{y}" width="176" height="132" rx="6" fill="{BG}" fill-opacity=".72" stroke="{CYAN}" stroke-opacity=".7"/>'
            +t(x+12,y+22,'CONSENT CHECK',10,CYAN,'class="tag" font-weight="700"')+f'<path d="M{x+12} {y+30}h152" stroke="{CYAN}" stroke-opacity=".35"/></g>')
        rows=[('> delete ~/tmp',WHITE,1.2),('tool  files.delete  OK',GREEN,2.6),('risk  HIGH  ->  ask',RED,4.0)]
        for i,(line,color,delay) in enumerate(rows):
            b+=f'<g class="pop fx" style="--loop:{loop}s;animation-delay:{delay}s">'+t(x+12,y+52+i*21,line,11,color,'class="tag"')+'</g>'
        b+=(f'<g class="pop fx" style="--loop:{loop}s;animation-delay:5.6s"><rect x="{x+12}" y="{y+100}" width="96" height="22" rx="4" fill="{CYAN}"/>'
            +t(x+60,y+115,'APPROVED',11,BG,'class="tag" text-anchor="middle" font-weight="700"')+'</g>')
        b+=f'<path d="M{x+176} {y+60}L640 150" stroke="{CYAN}" stroke-opacity=".5" stroke-dasharray="3 5" class="fx"/>'
    b+=embers(600,80,460,260,CYAN,12,7)
    return b

def noesis_fx(tags=True):
    """Noesis painting (1200x600): each pane is scanned, evidence flows to the crystal, sources are cited."""
    b=f'<ellipse cx="790" cy="340" rx="90" ry="70" fill="url(#g-lav)" class="pulse fx" opacity=".6"/>'
    panes=[((640,62),(1065,8),(590,150),(1010,130)),((650,160),(1068,135),(592,210),(1010,190)),((650,215),(1080,200),(592,275),(1020,280))]
    loop=9
    for i,(ta,tb,ba,bb) in enumerate(panes):
        a=i*1.3/loop; z=a+2.4/loop
        kt=f'keyTimes="0;{a:.3f};{z:.3f};1" dur="{loop}s" repeatCount="indefinite"'
        hold=lambda p,q:f'{p};{p};{q};{q}'
        b+=(f'<line class="fx" stroke="#f1eaff" stroke-width="2.2" x1="{ta[0]}" y1="{ta[1]}" x2="{ba[0]}" y2="{ba[1]}">'
            f'<animate attributeName="x1" values="{hold(ta[0],tb[0])}" {kt}/><animate attributeName="y1" values="{hold(ta[1],tb[1])}" {kt}/>'
            f'<animate attributeName="x2" values="{hold(ba[0],bb[0])}" {kt}/><animate attributeName="y2" values="{hold(ba[1],bb[1])}" {kt}/>'
            f'<animate attributeName="opacity" values="0;0;1;1;0;0" keyTimes="0;{a:.3f};{a+.01:.3f};{z:.3f};{z+.01:.3f};1" dur="{loop}s" repeatCount="indefinite"/></line>')
    for i,path in enumerate(('M575 160C520 250 640 330 782 345','M1012 132C1090 240 900 320 800 345','M592 276C600 320 700 340 785 348')):
        b+=(f'<path d="{path}" fill="none" stroke="{LAV}" stroke-opacity=".35" class="march fx"/>'
            f'<g class="fx"><circle r="7" fill="{LAV}" fill-opacity=".35"/><circle r="3" fill="#f6f0ff"/><animateMotion dur="3s" begin="-{i}s" repeatCount="indefinite" path="{path}"/></g>')
    b+=rings(790,338,46,LAV,3,3,1.5)
    b+=f'<ellipse cx="800" cy="482" rx="230" ry="50" fill="none" stroke="{LAV}" stroke-opacity=".4" stroke-dasharray="40 24 6 24" class="march fx" style="animation-duration:3s"/>'
    if tags:
        b+=tag(1076,104,'VIDEO 12:41',LAV,2.6,loop)+tag(1080,160,'AUDIO 03:15',LAV,3.9,loop)+tag(1092,246,'PDF P.7',LAV,5.2,loop)
        b+=tag(836,388,'ANSWER + 3 SOURCES',GREEN,6.3,loop)
    b+=embers(560,40,560,340,LAV,14,9)
    return b

ART_DEFS=glow('g-cyan',CYAN)+glow('g-gold','#ffb638')+glow('g-lav','#b79cff')

def art(name,x,y,w,h,fx,src_w,origin):
    """A painting plus its motion layer, sharing one slow push-in."""
    k=w/src_w
    return (f'<g class="kb" style="transform-origin:{origin}">{embedded(name,x,y,w,h)}'
            f'<g transform="translate({x} {y}) scale({k:.4f})">{fx}</g></g>')

# ---------------------------------------------------------------- scenes
def load_commits():
    try:return json.loads((ROOT/'data/mission-activity.json').read_text()).get('commits',[])
    except (OSError,ValueError):return []

def hero(mobile=False,still=False,commits=None):
    commits=load_commits() if commits is None else commits
    w,h=(600,880) if mobile else (1200,690)
    if mobile:
        name=lambda c:t(28,457,'ADITYA',78,c,'font-weight="900" letter-spacing="-3"')
        last=lambda c:t(28,535,'SINGH.',78,c,'font-weight="900" letter-spacing="-3"')
        b=art('operator.jpg',-615,0,1350,450,operator_fx(),1320,'330px 230px')
        b+='<rect y="230" width="600" height="250" fill="url(#fade)"/>'
        b+=t(30,43,'DROP ZONE / ADITYA2514',15,GOLD,'class="mono"')
        b+=glitch(lambda c:name(c)+last(c))+name(WHITE)+last(GOLD)
        b+=shimmer('sh1',name('#000')+last('#000'),28,385,150,170,820,1)
        b+=t(32,584,'Build. Inspect. Level up.',29)
        b+=t(32,627,'LLM SYSTEMS / AGENTS / FULL-STACK',14,CYAN,'class="mono"')
        b+=t(32,669,'IIT Madras · Scaler School of Technology',20,MUTED)
        y=715
        for i,s in enumerate(['READ THE PROBLEM','CHECK THE SYSTEM','SHIP THE FIX']):
            b+=f'<g class="st" style="animation-delay:{i*3}s">'+t(32,y+i*49,f'0{i+1}',17,GOLD,'class="mono"')+t(80,y+i*49,s,17,WHITE,'class="mono"')+'</g>'
            b+=f'<rect class="fill fx" x="32" y="{y+i*49+10}" width="300" height="3" rx="1.5" fill="{GOLD}" style="animation-delay:{i*3}s"/>'
        b+=minimap(516,676,52)
    else:
        name=lambda c:t(40,178,'ADITYA',96,c,'font-weight="900" letter-spacing="-4"')
        last=lambda c:t(40,274,'SINGH.',96,c,'font-weight="900" letter-spacing="-4"')
        b=art('operator.jpg',0,0,1320,440,operator_fx(),1320,'900px 250px')
        b+='<rect width="1200" height="440" fill="url(#shade)"/><rect y="310" width="1200" height="170" fill="url(#fade)"/>'
        b+=t(44,54,'DROP ZONE / THE ADITYA SINGH DOSSIER',15,GOLD,'class="mono"')
        b+=compass(486,30,288)+killfeed(486,84,commits)
        b+=glitch(lambda c:name(c)+last(c))+name(WHITE)+last(GOLD)
        b+=shimmer('sh1',name('#000')+last('#000'),40,90,170,200,900,1)
        b+=t(46,331,'Build. Inspect. Level up.',32)
        b+=t(46,383,'LLM SYSTEMS / AGENTS / FULL-STACK',15,CYAN,'class="mono"')
        b+=t(46,441,'IIT Madras · Scaler School of Technology',20,MUTED)
        b+=t(46,516,'A model can propose anything.',30,WHITE,'font-weight="700"')
        b+=t(46,557,'I build the systems that check what happens next.',25,MUTED)
        b+=steps_row(44,600,358,56,['READ THE PROBLEM','CHECK THE SYSTEM','SHIP THE FIX'],GOLD,26)
        b+=minimap(1092,512,62)+t(1012,572,'3 DROPS MARKED',10,MUTED,'class="tag" text-anchor="end"')
    b+=f'<path d="M28 {h-2}H{w-28}" stroke="{GOLD}" stroke-width="3" class="trace"/>'
    return frame(w,h,'Aditya Singh. Build. Inspect. Level up. LLM systems, agents and full-stack. IIT Madras and Scaler.',b,still,ART_DEFS)

PROJECTS=[
('LexGuard','CONTRACT INTELLIGENCE','Spot the trap.','Check the evidence.',GOLD,['Read the clause','Check the risk','Trace the statute'],lexguard_fx),
('Pikina','LOCAL DESKTOP AGENT','Your machine.','Your call.',CYAN,['Understand intent','Validate the tool','Ask for consent'],pikina_fx),
('Noesis','MULTIMODAL SEARCH','Find the moment.','Check the source.',LAV,['Search mixed media','Rerank evidence','Cite the source'],noesis_fx)]

def project(index,mobile=False):
    name,category,line1,line2,color,steps,fx=PROJECTS[index]
    w,h=(600,800) if mobile else (1200,590)
    if mobile:
        title=lambda c:t(28,432,name,61,c,'font-weight="900" letter-spacing="-2"')
        b=art(name.lower()+'-art.jpg',-280,0,880,440,fx(False),1200,'330px 200px')
        b+='<rect y="225" width="600" height="220" fill="url(#fade)"/>'
        b+=t(28,42,f'0{index+1} / {category}',13,color,'class="mono"')
        b+=glitch(title)+title(WHITE)+shimmer('sh1',title('#000'),28,378,130,70,760,index)
        b+=t(30,481,line1,30)+t(30,519,line2,30,color)
        for i,label in enumerate(steps):
            y=577+i*57
            b+=f'<g class="st" style="animation-delay:{i*3}s"><rect x="30" y="{y-27}" width="36" height="36" rx="5" fill="{PANEL}" stroke="{color}"/>'
            b+=t(48,y-3,str(i+1),18,color,'text-anchor="middle"')+t(84,y,label,23)+'</g>'
            b+=f'<rect class="fill fx" x="84" y="{y+9}" width="260" height="3" rx="1.5" fill="{color}" style="animation-delay:{i*3}s"/>'
        b+=t(30,749,'ILLUSTRATIVE SYSTEM STORY',11,MUTED,'class="mono"')
        b+=t(30,781,'EXPLORE THE REPOSITORY →',15,color,'class="mono"')
    else:
        title=lambda c:t(40,160,name,75,c,'font-weight="900" letter-spacing="-3"')
        b=art(name.lower()+'-art.jpg',0,0,1200,600,fx(True),1200,'820px 260px')
        b+='<rect width="1200" height="600" fill="url(#shade)"/><rect y="300" width="1200" height="290" fill="url(#fade)"/>'
        b+=t(42,51,f'MISSION 0{index+1} / {category}',15,color,'class="mono"')
        b+=f'<circle cx="1022" cy="46" r="4.5" fill="{RED}" class="blink fx"/>'+t(1156,51,'ILLUSTRATIVE REPLAY',12,MUTED,'class="mono" text-anchor="end"')
        b+=glitch(title)+title(WHITE)+shimmer('sh1',title('#000'),40,96,150,80,820,index)
        b+=t(44,220,line1,35)+t(44,265,line2,35,color)
        b+=t(44,333,'ILLUSTRATIVE SYSTEM STORY',12,MUTED,'class="mono"')
        b+=steps_row(42,422,358,91,steps,color,20,mono=False)
        b+=t(44,557,'MODEL PROPOSES / SYSTEM CHECKS / YOU DECIDE',12,MUTED,'class="mono"')
        b+=t(1156,557,'INSPECT THE CODE →',14,color,'class="mono" text-anchor="end"')
    b+=f'<path d="M28 2H{w-28}" stroke="{color}" stroke-width="3" class="trace"/>'
    return frame(w,h,f'{name}: {line1} {line2} '+'. '.join(steps)+'. Illustrative animation.',b,False,ART_DEFS)

def chapter(number,title,subtitle,mobile=False):
    w,h=(600,170) if mobile else (1200,145)
    size=34 if mobile else 43
    head=lambda c:t(28,86,title,size,c,'font-weight="800" letter-spacing="-1"')
    ghost=lambda c,o:t(w-25,h-15,number,142 if mobile else 154,c,f'font-weight="900" text-anchor="end" opacity="{o}"')
    # speed lines drifting behind the number, then the number itself with a glitch
    b='<g class="drift fx">'+''.join(f'<path d="M{w-360+i*46} {h+10}l70-{h+20}" stroke="{GOLD}" stroke-opacity="{.05+.02*(i%3):.2f}" stroke-width="{6+4*(i%2)}"/>' for i in range(9))+'</g>'
    b+=ghost(GOLD,.1)+f'<g class="ga fx">{ghost("#59e3ff",.35)}</g><g class="gb fx">{ghost("#ff5a6e",.3)}</g>'
    b+=t(30,37,'CHAPTER '+number,13,GOLD,'class="mono"')
    b+=''.join(f'<path class="chev fx" d="M{150+i*13} 27l6 6-6 6" fill="none" stroke="{GOLD}" stroke-width="2" style="animation-delay:{i*.25}s"/>' for i in range(4))
    b+=head(WHITE)+shimmer('sh1',head('#000'),28,50,120,46,w,int(number))
    for i,line in enumerate(textwrap.wrap(subtitle,43 if mobile else 90)):
        b+=t(30,120+i*25,line,18,MUTED)
    b+=f'<path d="M1 15V{h-15}" stroke="{GOLD}" stroke-width="3"/><path d="M1 15V{h-15}" stroke="#fff7dc" stroke-width="3" stroke-dasharray="26 200" class="march fx" style="animation-duration:2.6s"/>'
    b+=f'<path d="M28 {h-2}H{w-28}" stroke="{GOLD}" stroke-width="2" class="trace"/>'
    return frame(w,h,title+'. '+subtitle,b)

def arsenal(groups,mobile=False):
    w=600 if mobile else 1200
    slots=['PRIMARY','SECONDARY','SIDEARM','THROWABLES','ATTACHMENTS','BACKPACK']
    b='';y=0
    for i,g in enumerate(groups):
        x=0 if mobile else (i%2)*600
        if not mobile:y=(i//2)*206
        tools=' / '.join(g['tools'])
        rows=textwrap.wrap(tools,43)
        height=max(184,110+len(rows)*28)
        b+=f'<rect x="{x+12}" y="{y+12}" width="576" height="{height}" rx="10" fill="{PANEL}" stroke="{LINE}"/>'
        # the loadout cursor visits each slot in turn
        b+=(f'<g class="eq fx" style="animation-delay:{i*2}s"><rect x="{x+12}" y="{y+12}" width="576" height="{height}" rx="10" fill="{GOLD}" fill-opacity=".05" stroke="{GOLD}" stroke-width="2"/>'
            f'<rect x="{x+468}" y="{y+28}" width="100" height="24" rx="4" fill="{GOLD}"/>'+t(x+518,y+45,'EQUIPPED',11,BG,'class="tag" text-anchor="middle" font-weight="700"')+'</g>')
        b+=t(x+36,y+48,f'0{i+1} / '+g['name'],15,GOLD,'class="mono"')
        b+=t(x+36,y+84,g['purpose'],22)
        for j,line in enumerate(rows):b+=t(x+36,y+124+j*28,line,19,CYAN)
        b+=t(x+568,y+height-6,slots[i%len(slots)]+' SLOT',10,MUTED,'class="tag" text-anchor="end"')
        b+=f'<path d="M{x+30} {y+12}H{x+570}" stroke="{CYAN}" stroke-width="2" class="trace" style="animation-delay:-{i*1.4}s"/>'
        if mobile:y+=height+24
    h=y if mobile else y+206
    return frame(w,h,'Build kit: tools grouped by purpose.',b)

def outro(mobile=False):
    w,h=(600,410) if mobile else (1200,330)
    line1=lambda c:t(28,128,'BUILD SOMETHING',42 if mobile else 66,c,'font-weight="900" letter-spacing="-2"')
    line2=lambda c:t(28,190 if mobile else 207,'WORTH FINDING.',42 if mobile else 66,c,'font-weight="900" letter-spacing="-2"')
    ox=-550 if mobile else 0
    b=art('operator.jpg',ox,0,1200,400,operator_fx(),1320,'800px 200px')
    b+=f'<rect width="{w}" height="{h}" fill="{BG}" opacity=".7"/>'
    # the final circle closes on the invitation
    cx,cy,r=(530,340,90) if mobile else (790,168,150)
    b+=(f'<g class="fx"><circle cx="{cx}" cy="{cy}" r="{r*.42:.0f}" fill="none" stroke="{WHITE}" stroke-opacity=".7" stroke-dasharray="3 5"/>'
        f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#5aa9ff" stroke-width="2.5"><animate attributeName="r" values="{r*1.15:.0f};{r*.42:.0f};{r*.42:.0f}" keyTimes="0;.8;1" dur="10s" repeatCount="indefinite"/>'
        f'<animate attributeName="opacity" values="0;.9;.9;0" keyTimes="0;.08;.9;1" dur="10s" repeatCount="indefinite"/></circle></g>')
    b+=t(cx,cy+r*.42+22,'FINAL CIRCLE',11,MUTED,'class="tag" text-anchor="middle"')
    b+=t(32,49,'NEXT MISSION / SQUAD UP',15,GOLD,'class="mono"')
    b+=glitch(lambda c:line1(c)+line2(c))+line1(WHITE)+line2(GOLD)
    b+=shimmer('sh1',line1('#000')+line2('#000'),28,70,160,150,w+200,2)
    b+=t(32,251 if mobile else 265,'AI engineering / agents / hackathons',20,CYAN)
    b+=t(32,298 if mobile else 307,'Bring the problem. Let’s build the next chapter.',19,MUTED)
    if mobile:b+=t(32,372,'GG. NOW GO INSPECT THE CODE.',15,GOLD,'class="mono"')
    b+=f'<path d="M28 {h-2}H{w-28}" stroke="{GOLD}" class="trace" stroke-width="3"/>'
    return frame(w,h,'Squad up. Build something worth finding. AI engineering, agents and hackathons.',b,False,ART_DEFS)

def results(mobile=False):
    """The post-match screen, used for the record: placement, then the stats that go with it."""
    w,h=(600,474) if mobile else (1200,300)
    size=128 if mobile else 150
    rank=lambda c:t(30 if mobile else 36,166 if mobile else 196,'#2',size,c,'font-weight="900" letter-spacing="-6"')
    b=embers(30,60,w-60,h-90,GOLD,22,11)
    b+=rings(126 if mobile else 140,118 if mobile else 142,118,GOLD,3,4.5,1.4)
    b+=t(32 if mobile else 40,46,'MATCH RESULT / PARADOX DSA TRIATHLON',13 if mobile else 14,GOLD,'class="mono"')
    b+=glitch(rank)+rank(GOLD)+shimmer('sh1',rank('#000'),30,50,110,160,520,0)
    tiles=[('CGPA','9.0 / 10','IIT Madras · BS, Data Science & Applications'),('CO-ENROLLED','2025–2029','Scaler School of Technology'),('HACKATHON','Meta PyTorch OpenEnv','Team submission · 2026')]
    if mobile:
        head=lambda c:t(236,112,'RUNNER-UP',42,c,'font-weight="900" letter-spacing="-1"')
        b+=head(WHITE)+shimmer('sh2',head('#000'),236,76,110,46,560,2)
        b+=t(238,146,'IIT Madras · 2026',19,MUTED)+t(238,182,'So close to the chicken dinner.',16,CYAN)+t(238,205,'Queued again.',16,CYAN)
        tx,ty,tw,th,gap=30,244,540,64,10
    else:
        head=lambda c:t(268,138,'RUNNER-UP',68,c,'font-weight="900" letter-spacing="-2"')
        b+=head(WHITE)+shimmer('sh2',head('#000'),268,78,150,70,700,2)
        b+=t(272,182,'IIT Madras · 2026',22,MUTED)+t(272,226,'So close to the chicken dinner. Queued again.',20,CYAN)
        tx,ty,tw,th,gap=776,28,384,76,8
    for i,(label,value,sub) in enumerate(tiles):
        y=ty+i*(th+gap)
        b+=f'<g class="st" style="animation-delay:{i*3}s"><rect x="{tx}" y="{y}" width="{tw}" height="{th}" rx="8" fill="{PANEL}" stroke="{LINE}"/>'
        b+=t(tx+16,y+22,label,11,GOLD,'class="tag" font-weight="700"')+t(tx+16,y+th-28 if mobile else y+48,value,19,WHITE,'font-weight="700"')
        b+=t(tx+16,y+th-9,sub,12.5,MUTED)+'</g>'
        b+=f'<rect class="fill fx" x="{tx+1}" y="{y+th-3}" width="{tw-2}" height="3" rx="1.5" fill="{GOLD}" style="animation-delay:{i*3}s"/>'
    b+=f'<path d="M28 {h-2}H{w-28}" stroke="{GOLD}" stroke-width="3" class="trace"/>'
    return frame(w,h,'Match result: runner-up, number two, at the Paradox DSA Triathlon, IIT Madras, 2026. CGPA 9.0 of 10 at IIT Madras. Co-enrolled at Scaler School of Technology. Meta PyTorch OpenEnv Hackathon team submission.',b)

def extra_assets(groups):
    chapters=[('01','THE OPERATOR','A competitive mindset. An inspectable engineering process.'),('02','FEATURED MISSIONS','Three systems. Three distinct stories. Explore the code.'),('03','THE PROJECT LOBBY','More builds, experiments and systems in progress.'),('04','THE BUILD KIT','Choose the tool for the job. Make the system work.'),('05','MATCH HISTORY','Real contributions. Recent changes. Lessons from the replay.'),('06','CAREER CAMPAIGN','The education and milestones behind the builds.')]
    for mobile in (False,True):
        suffix='-mobile' if mobile else ''
        for number,title,subtitle in chapters:
            (OUT/f'chapter-{number}{suffix}.svg').write_text(chapter(number,title,subtitle,mobile))
        (OUT/f'arsenal{suffix}.svg').write_text(arsenal(groups,mobile))
        (OUT/f'outro{suffix}.svg').write_text(outro(mobile))
        (OUT/f'results{suffix}.svg').write_text(results(mobile))
