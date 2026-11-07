"""Cinematic Drop Zone artwork. All SVG images are self-contained and script-free."""
import base64
from html import escape
from pathlib import Path
import textwrap

OUT=Path(__file__).resolve().parents[1]/'assets/mission'
BG='#0d1117'; PANEL='#161b22'; LINE='#30363d'; WHITE='#e6edf3'
MUTED='#a8b3bf'; GOLD='#e9b44c'; CYAN='#70c9cb'
CSS='''
text{font-family:Arial,Helvetica,sans-serif}.mono{font-family:Consolas,monospace;letter-spacing:2px}
.trace{stroke-dasharray:160 1240;animation:trace 9s linear infinite}
.pulse{animation:pulse 6s ease-in-out infinite}
.orbit{transform-origin:0 0;animation:orbit 28s linear infinite}
.scan{animation:scan 10s ease-in-out infinite}
.spark{animation:spark 9s ease-in-out infinite}
.s1{animation:s1 12s ease-in-out infinite}.s2{animation:s2 12s ease-in-out infinite}.s3{animation:s3 12s ease-in-out infinite}
@keyframes trace{to{stroke-dashoffset:-1400}}
@keyframes pulse{50%{opacity:.35}}
@keyframes orbit{to{transform:rotate(360deg)}}
@keyframes scan{0%,100%{transform:translateY(0);opacity:0}20%,70%{opacity:.45}80%{transform:translateY(260px);opacity:0}}
@keyframes spark{0%,100%{opacity:0;transform:translateY(10px)}40%{opacity:.6}90%{transform:translateY(-35px);opacity:0}}
@keyframes s1{0%,25%,100%{opacity:1}35%,85%{opacity:.35}}
@keyframes s2{0%,20%,70%,100%{opacity:.35}35%,55%{opacity:1}}
@keyframes s3{0%,50%,100%{opacity:.35}65%,90%{opacity:1}}
@media(prefers-reduced-motion:reduce){*{animation:none!important}.scan,.spark{display:none}}
'''

def t(x,y,s,size=20,color=WHITE,attr=''):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" {attr}>{escape(str(s))}</text>'

def embedded(name,x,y,w,h):
    data=base64.b64encode((OUT/name).read_bytes()).decode()
    return f'<image x="{x}" y="{y}" width="{w}" height="{h}" preserveAspectRatio="xMidYMid slice" xlink:href="data:image/jpeg;base64,{data}"/>'

def frame(w,h,title,body,still=False):
    css=CSS if not still else 'text{font-family:Arial,Helvetica,sans-serif}.mono{font-family:Consolas,monospace;letter-spacing:2px}.scan,.spark{display:none}'
    return f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title">
<title id="title">{escape(title)}</title><style>{css}</style><defs>
<clipPath id="bounds"><rect width="{w}" height="{h}" rx="14"/></clipPath>
<linearGradient id="fade" x1="0" y1="0" x2="0" y2="1"><stop stop-color="{BG}" stop-opacity="0"/><stop offset="1" stop-color="{BG}"/></linearGradient>
<linearGradient id="shade"><stop stop-color="{BG}" stop-opacity=".8"/><stop offset=".55" stop-color="{BG}" stop-opacity=".2"/><stop offset="1" stop-color="{BG}" stop-opacity="0"/></linearGradient>
</defs><rect width="{w}" height="{h}" rx="14" fill="{BG}"/>
<g clip-path="url(#bounds)">{body}</g><rect x="1" y="1" width="{w-2}" height="{h-2}" rx="13" fill="none" stroke="{LINE}"/></svg>\n'''

def sparks(w,h):
    return ''.join(f'<circle cx="{int(w*.46)+(i*73)%int(w*.49)}" cy="{80+(i*41)%int(h*.6)}" r="{1+i%2}" fill="{GOLD}" class="spark" style="animation-delay:-{i*.7}s"/>' for i in range(14))

def hero(mobile=False,still=False):
    w,h=(600,880) if mobile else (1200,690)
    if mobile:
        b=embedded('operator.jpg',-615,0,1350,450)
        b+='<rect y="230" width="600" height="250" fill="url(#fade)"/>'
        b+=t(30,43,'DROP ZONE / ADITYA2514',15,GOLD,'class="mono"')
        b+=t(28,457,'ADITYA',78,WHITE,'font-weight="900" letter-spacing="-3"')
        b+=t(28,535,'SINGH.',78,GOLD,'font-weight="900" letter-spacing="-3"')
        b+=t(32,584,'Build. Inspect. Level up.',29)
        b+=t(32,627,'LLM SYSTEMS / AGENTS / FULL-STACK',14,CYAN,'class="mono"')
        b+=t(32,669,'IIT Madras · Scaler School of Technology',20,MUTED)
        y=715
        for i,s in enumerate(['READ THE PROBLEM','CHECK THE SYSTEM','SHIP THE FIX']):
            b+=t(32,y+i*49,f'0{i+1}',17,GOLD,'class="mono"')+t(80,y+i*49,s,17,WHITE,'class="mono"')
    else:
        b=embedded('operator.jpg',0,0,1320,440)
        b+='<rect width="1200" height="440" fill="url(#shade)"/><rect y="310" width="1200" height="170" fill="url(#fade)"/>'
        b+=t(44,54,'DROP ZONE / THE ADITYA SINGH DOSSIER',15,GOLD,'class="mono"')
        b+=t(40,178,'ADITYA',96,WHITE,'font-weight="900" letter-spacing="-4"')
        b+=t(40,274,'SINGH.',96,GOLD,'font-weight="900" letter-spacing="-4"')
        b+=t(46,331,'Build. Inspect. Level up.',32)
        b+=t(46,383,'LLM SYSTEMS / AGENTS / FULL-STACK',15,CYAN,'class="mono"')
        b+=t(46,441,'IIT Madras · Scaler School of Technology',20,MUTED)
        b+=t(46,516,'A model can propose anything.',30,WHITE,'font-weight="700"')
        b+=t(46,557,'I build the systems that check what happens next.',25,MUTED)
        for i,s in enumerate(['READ THE PROBLEM','CHECK THE SYSTEM','SHIP THE FIX']):
            x=44+i*384
            b+=f'<rect x="{x}" y="600" width="358" height="56" rx="6" fill="{PANEL}" stroke="{LINE}"/>'
            b+=t(x+18,635,f'0{i+1}',15,GOLD,'class="mono"')+t(x+58,635,s,14,WHITE,'class="mono"')
        b+='<g transform="translate(1025 485)" opacity=".45"><circle r="55" fill="none" stroke="#70c9cb"/><g class="orbit"><circle r="67" fill="none" stroke="#e9b44c" stroke-dasharray="80 40 15 60"/></g><path d="M-30 0H30M0-30V30" stroke="#70c9cb"/></g>'
    b+=sparks(w,h)+f'<path d="M28 {h-2}H{w-28}" stroke="{GOLD}" stroke-width="3" class="trace"/>'
    return frame(w,h,'Aditya Singh. Build. Inspect. Level up. LLM systems, agents and full-stack. IIT Madras and Scaler.',b,still)

PROJECTS=[
('LexGuard','CONTRACT INTELLIGENCE','Spot the trap.','Check the evidence.',GOLD,['Read the clause','Check the risk','Trace the statute']),
('Pikina','LOCAL DESKTOP AGENT','Your machine.','Your call.',CYAN,['Understand intent','Validate the tool','Ask for consent']),
('Noesis','MULTIMODAL SEARCH','Find the moment.','Check the source.','#b6a7dc',['Search mixed media','Rerank evidence','Cite the source'])]

def project(index,mobile=False):
    name,category,line1,line2,color,steps=PROJECTS[index]
    w,h=(600,800) if mobile else (1200,590)
    if mobile:
        b=embedded(name.lower()+'-art.jpg',-280,0,880,440)
        b+='<rect y="225" width="600" height="220" fill="url(#fade)"/>'
        b+=t(28,42,f'0{index+1} / {category}',13,color,'class="mono"')
        b+=t(28,432,name,61,WHITE,'font-weight="900" letter-spacing="-2"')
        b+=t(30,481,line1,30)+t(30,519,line2,30,color)
        for i,label in enumerate(steps):
            y=577+i*57
            b+=f'<g class="s{i+1}"><rect x="30" y="{y-27}" width="36" height="36" rx="5" fill="{PANEL}" stroke="{color}"/>'
            b+=t(48,y-3,str(i+1),18,color,'text-anchor="middle"')+t(84,y,label,23)+'</g>'
        b+=t(30,749,'ILLUSTRATIVE SYSTEM STORY',11,MUTED,'class="mono"')
        b+=t(30,781,'EXPLORE THE REPOSITORY →',15,color,'class="mono"')
    else:
        b=embedded(name.lower()+'-art.jpg',0,0,1200,600)
        b+='<rect width="1200" height="600" fill="url(#shade)"/><rect y="300" width="1200" height="290" fill="url(#fade)"/>'
        b+=t(42,51,f'MISSION 0{index+1} / {category}',15,color,'class="mono"')
        b+=t(40,160,name,75,WHITE,'font-weight="900" letter-spacing="-3"')
        b+=t(44,220,line1,35)+t(44,265,line2,35,color)
        b+=t(44,333,'ILLUSTRATIVE SYSTEM STORY',12,MUTED,'class="mono"')
        b+=f'<path d="M700 100H1140" stroke="{color}" class="scan"/>'
        for i,label in enumerate(steps):
            x=42+i*378
            b+=f'<g class="s{i+1}"><rect x="{x}" y="422" width="358" height="91" rx="8" fill="{BG}" fill-opacity=".9" stroke="{LINE}"/>'
            b+=t(x+18,451,f'0{i+1}',13,color,'class="mono"')+t(x+18,488,label,23)+'</g>'
        b+=t(44,557,'MODEL PROPOSES / SYSTEM CHECKS / YOU DECIDE',12,MUTED,'class="mono"')
        b+=t(1156,557,'INSPECT THE CODE →',14,color,'class="mono" text-anchor="end"')
    b+=f'<path d="M28 2H{w-28}" stroke="{color}" stroke-width="3" class="trace"/>'
    return frame(w,h,f'{name}: {line1} {line2} '+'. '.join(steps)+'. Illustrative animation.',b)

def chapter(number,title,subtitle,mobile=False):
    w,h=(600,170) if mobile else (1200,145)
    b=t(w-25,h-15,number,142 if mobile else 154,GOLD,'font-weight="900" text-anchor="end" opacity=".08"')
    b+=t(30,37,'CHAPTER '+number,13,GOLD,'class="mono"')
    b+=t(28,86,title,34 if mobile else 43,WHITE,'font-weight="800" letter-spacing="-1"')
    for i,line in enumerate(textwrap.wrap(subtitle,43 if mobile else 90)):
        b+=t(30,120+i*25,line,18,MUTED)
    b+=f'<path d="M1 15V{h-15}" stroke="{GOLD}" stroke-width="3"/>'
    return frame(w,h,title+'. '+subtitle,b)

def arsenal(groups,mobile=False):
    w=600 if mobile else 1200
    b='';y=0
    for i,g in enumerate(groups):
        x=0 if mobile else (i%2)*600
        if not mobile:y=(i//2)*206
        tools=' / '.join(g['tools'])
        rows=textwrap.wrap(tools,43)
        height=max(184,110+len(rows)*28)
        b+=f'<rect x="{x+12}" y="{y+12}" width="576" height="{height}" rx="10" fill="{PANEL}" stroke="{LINE}"/>'
        b+=t(x+36,y+48,f'0{i+1} / '+g['name'],15,GOLD,'class="mono"')
        b+=t(x+36,y+84,g['purpose'],22)
        for j,line in enumerate(rows):b+=t(x+36,y+124+j*28,line,19,CYAN)
        if mobile:y+=height+24
    h=y if mobile else y+206
    return frame(w,h,'Build kit: tools grouped by purpose.',b)

def outro(mobile=False):
    w,h=(600,410) if mobile else (1200,330)
    b=embedded('operator.jpg',-550 if mobile else 0,0,1200,400)
    b+=f'<rect width="{w}" height="{h}" fill="{BG}" opacity=".76"/>'
    b+=t(32,49,'NEXT MISSION / SQUAD UP',15,GOLD,'class="mono"')
    b+=t(28,128,'BUILD SOMETHING',42 if mobile else 66,WHITE,'font-weight="900" letter-spacing="-2"')
    b+=t(28,190 if mobile else 207,'WORTH FINDING.',42 if mobile else 66,GOLD,'font-weight="900" letter-spacing="-2"')
    b+=t(32,251 if mobile else 265,'AI engineering / agents / hackathons',20,CYAN)
    b+=t(32,298 if mobile else 307,'Bring the problem. Let’s build the next chapter.',19,MUTED)
    if mobile:b+=t(32,372,'GG. NOW GO INSPECT THE CODE.',15,GOLD,'class="mono"')
    b+=f'<path d="M28 {h-2}H{w-28}" stroke="{GOLD}" class="trace" stroke-width="3"/>'
    return frame(w,h,'Squad up. Build something worth finding. AI engineering, agents and hackathons.',b)

def extra_assets(groups):
    chapters=[('01','THE OPERATOR','A competitive mindset. An inspectable engineering process.'),('02','FEATURED MISSIONS','Three systems. Three distinct stories. Explore the code.'),('03','THE PROJECT LOBBY','More builds, experiments and systems in progress.'),('04','THE BUILD KIT','Choose the tool for the job. Make the system work.'),('05','MATCH HISTORY','Real contributions. Recent changes. Lessons from the replay.'),('06','CAREER CAMPAIGN','The education and milestones behind the builds.')]
    for mobile in (False,True):
        suffix='-mobile' if mobile else ''
        for number,title,subtitle in chapters:
            (OUT/f'chapter-{number}{suffix}.svg').write_text(chapter(number,title,subtitle,mobile))
        (OUT/f'arsenal{suffix}.svg').write_text(arsenal(groups,mobile))
        (OUT/f'outro{suffix}.svg').write_text(outro(mobile))
