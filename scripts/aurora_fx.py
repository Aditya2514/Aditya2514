"""Effects for the Aurora profile: Milky Way, a self-drawing constellation, falling snow, a rippling lake,
a campfire, count-up numbers, running-light borders and the living hero scene."""

from __future__ import annotations

import math
import random

from aurora_art import (AMBER, EMERALD, ICE, MONO, MUTED, ROSE, SANS, TEAL, TEXT, aurora, frame, ground, meteor,
                        mountains, pill, stars, svg, t)

FX_CSS = (
    "<style>"
    ".fallA{animation:fallA linear infinite}.fallB{animation:fallB linear infinite}.fallC{animation:fallC linear infinite}"
    "@keyframes fallA{from{transform:translate(0,-30px)}to{transform:translate(34px,600px)}}"
    "@keyframes fallB{from{transform:translate(0,-30px)}to{transform:translate(-26px,600px)}}"
    "@keyframes fallC{from{transform:translate(0,-30px)}to{transform:translate(10px,600px)}}"
    ".flick{transform-box:fill-box;transform-origin:50% 100%;animation:flick .9s ease-in-out infinite alternate}"
    "@keyframes flick{0%{transform:scale(1,1);opacity:.95}35%{transform:scale(.86,1.12);opacity:.8}70%{transform:scale(1.08,.9);opacity:1}100%{transform:scale(.94,1.06);opacity:.85}}"
    ".ember{animation:ember 2.6s ease-out infinite}"
    "@keyframes ember{0%{transform:translate(0,0);opacity:0}10%{opacity:1}100%{transform:translate(var(--dx,6px),-90px);opacity:0}}"
    ".warm{animation:warm 1.4s ease-in-out infinite alternate}@keyframes warm{from{opacity:.55}to{opacity:.95}}"
    ".drift{animation:drift 26s ease-in-out infinite alternate}@keyframes drift{from{transform:translateX(-8px)}to{transform:translateX(8px)}}"
    ".drift2{animation:drift 34s ease-in-out infinite alternate-reverse}"
    ".cyc{opacity:0;animation:cyc 10.5s ease-in-out infinite}"
    "@keyframes cyc{0%{opacity:0;transform:translateY(8px)}4%,29%{opacity:1;transform:none}33%,100%{opacity:0;transform:translateY(-6px)}}"
    ".glint{animation:glint 4s ease-in-out infinite}@keyframes glint{0%,100%{opacity:.05}50%{opacity:.4}}"
    ".mist{animation:mist 30s ease-in-out infinite alternate}@keyframes mist{from{transform:translateX(-60px)}to{transform:translateX(60px)}}"
    ".run{animation:run 5.5s linear infinite}@keyframes run{from{stroke-dashoffset:0}to{stroke-dashoffset:-100}}"
    ".breathe{transform-box:fill-box;transform-origin:50% 100%;animation:breathe 4.2s ease-in-out infinite alternate}"
    "@keyframes breathe{0%{transform:scaleY(.82)}55%{transform:scaleY(1.06)}100%{transform:scaleY(.94)}}"
    "@media (prefers-reduced-motion: reduce){.fallA,.fallB,.fallC,.ember{display:none}.cyc{animation:none}.cyc.first{opacity:1}}"
    "</style>"
)


# ------------------------------------------------------------------------------------------------ building blocks

def milky_way(W, H, seed=201, angle=-17, cy=150):
    rnd = random.Random(seed)
    dots = []
    for _ in range(420):
        x = rnd.uniform(-100, W + 100)
        off = rnd.gauss(0, 26)
        r = rnd.choice([.35, .45, .55, .7])
        dots.append(f'<circle cx="{x:.0f}" cy="{cy + off:.1f}" r="{r}" fill="#e8fbff" opacity="{max(.08, .7 - abs(off) / 60):.2f}"/>')
    return (f'<radialGradient id="mw" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="{ICE}" stop-opacity=".16"/>'
            f'<stop offset=".6" stop-color="{TEAL}" stop-opacity=".05"/><stop offset="1" stop-color="{ICE}" stop-opacity="0"/></radialGradient>'
            f'<g transform="rotate({angle} {W / 2} {cy})"><ellipse cx="{W / 2}" cy="{cy}" rx="{W * .75}" ry="70" fill="url(#mw)"/>'
            f'<ellipse cx="{W / 2 + 60}" cy="{cy + 6}" rx="{W * .5}" ry="9" fill="#02050b" opacity=".45" filter="url(#soft)"/>'
            + "".join(dots) + "</g>")


def constellation(points, edges, delay, color=ICE, label=None, label_xy=None):
    out = []
    for k, (a, b) in enumerate(edges):
        (x1, y1), (x2, y2) = points[a], points[b]
        out.append(f'<path class="draw" pathLength="1" d="M{x1},{y1} L{x2},{y2}" stroke="{color}" stroke-opacity=".55" stroke-width="1" '
                   f'style="animation-delay:{delay + k * .35:.2f}s;animation-duration:.6s"/>')
    for k, (x, y) in enumerate(points):
        out.append(f'<circle class="tw" style="animation-delay:{k * .3:.1f}s" cx="{x}" cy="{y}" r="2.1" fill="#f4feff" filter="url(#glow)"/>')
    if label and label_xy:
        out.append(f'<g class="fade" style="animation-delay:{delay + len(edges) * .35:.1f}s">'
                   + t(label_xy[0], label_xy[1], label, 8.5, MUTED, MONO, 500, "middle", 2.4) + "</g>")
    return "".join(out)


def snow(W, H, n, seed):
    rnd = random.Random(seed)
    out = []
    for _ in range(n):
        x, y0 = rnd.uniform(0, W), rnd.uniform(-H, 0)
        r = rnd.choice([.7, .9, 1.1, 1.4, 1.8])
        cls = rnd.choice(["fallA", "fallB", "fallC"])
        out.append(f'<circle class="{cls}" style="animation-duration:{rnd.uniform(9, 19):.1f}s;animation-delay:{-rnd.uniform(0, 19):.1f}s" '
                   f'cx="{x:.0f}" cy="{rnd.uniform(-20, 0):.0f}" r="{r}" fill="#effcff" opacity="{rnd.uniform(.35, .85):.2f}"/>')
    return "".join(out)


def ripple_filter(uid="ripple"):
    return (f'<filter id="{uid}" x="-5%" y="-5%" width="110%" height="110%">'
            '<feTurbulence type="turbulence" baseFrequency="0.006 0.11" numOctaves="2" seed="4" result="n">'
            '<animate attributeName="baseFrequency" dur="11s" values="0.006 0.11;0.009 0.15;0.006 0.11" repeatCount="indefinite"/></feTurbulence>'
            '<feDisplacementMap in="SourceGraphic" in2="n" scale="12" xChannelSelector="R" yChannelSelector="G"/>'
            '<feGaussianBlur stdDeviation="1.1"/></filter>')


def lake(W, H, horizon, world_id, seed=7):
    rnd = random.Random(seed)
    glints = "".join(
        f'<line class="glint" style="animation-delay:{rnd.uniform(0, 4):.1f}s" x1="{x:.0f}" y1="{y:.0f}" x2="{x + rnd.uniform(30, 140):.0f}" y2="{y:.0f}" '
        f'stroke="{ICE}" stroke-width="1"/>'
        for x, y in ((rnd.uniform(0, W), rnd.uniform(horizon + 6, H - 6)) for _ in range(34)))
    return (f'<clipPath id="lakeclip"><rect x="0" y="{horizon}" width="{W}" height="{H - horizon}"/></clipPath>'
            f'<linearGradient id="lakefade" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#02050b" stop-opacity="0"/>'
            f'<stop offset="1" stop-color="#02050b" stop-opacity=".75"/></linearGradient>'
            f'<g clip-path="url(#lakeclip)"><rect x="0" y="{horizon}" width="{W}" height="{H - horizon}" fill="#030a14"/>'
            f'<use href="#{world_id}" transform="translate(0 {2 * horizon}) scale(1 -1)" opacity=".8" filter="url(#ripple)"/>'
            f'<rect x="0" y="{horizon}" width="{W}" height="{H - horizon}" fill="url(#lakefade)"/>{glints}</g>'
            f'<line x1="0" y1="{horizon}" x2="{W}" y2="{horizon}" stroke="{ICE}" stroke-opacity=".18"/>')


def campfire(x, y, seed=11):
    """Tent, fire, embers and a figure watching the sky, standing on ground level y."""
    rnd = random.Random(seed)
    embers = "".join(
        f'<circle class="ember" style="animation-delay:{rnd.uniform(0, 2.6):.2f}s;--dx:{rnd.uniform(-14, 18):.0f}px" '
        f'cx="{x + rnd.uniform(-5, 5):.1f}" cy="{y - 10}" r="{rnd.uniform(.8, 1.6):.1f}" fill="{AMBER}"/>' for _ in range(14))
    tx = x - 78
    return (f'<radialGradient id="fireglow" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="{AMBER}" stop-opacity=".55"/>'
            f'<stop offset=".5" stop-color="{ROSE}" stop-opacity=".12"/><stop offset="1" stop-color="{AMBER}" stop-opacity="0"/></radialGradient>'
            f'<linearGradient id="flame" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#fff3c4"/>'
            f'<stop offset=".45" stop-color="{AMBER}"/><stop offset="1" stop-color="{ROSE}" stop-opacity="0"/></linearGradient>'
            f'<ellipse class="warm" cx="{x}" cy="{y - 8}" rx="130" ry="70" fill="url(#fireglow)"/>'
            # tent
            f'<polygon points="{tx - 34},{y} {tx},{y - 50} {tx + 34},{y}" fill="#0b1726" stroke="#1e3247"/>'
            f'<polygon class="warm" points="{tx - 9},{y} {tx},{y - 30} {tx + 9},{y}" fill="{AMBER}" opacity=".7"/>'
            f'<line x1="{tx}" y1="{y - 50}" x2="{tx}" y2="{y - 58}" stroke="#1e3247" stroke-width="1.5"/>'
            # logs + flames
            f'<line x1="{x - 13}" y1="{y - 1}" x2="{x + 13}" y2="{y - 6}" stroke="#3a2412" stroke-width="4" stroke-linecap="round"/>'
            f'<line x1="{x - 13}" y1="{y - 6}" x2="{x + 13}" y2="{y - 1}" stroke="#4a2e16" stroke-width="4" stroke-linecap="round"/>'
            f'<path class="flick" d="M{x - 9},{y - 4} Q{x - 10},{y - 18} {x - 2},{y - 30} Q{x},{y - 18} {x + 4},{y - 22} Q{x + 10},{y - 12} {x + 9},{y - 4} Z" fill="url(#flame)"/>'
            f'<path class="flick" style="animation-delay:-.4s;animation-duration:.7s" d="M{x - 5},{y - 4} Q{x - 4},{y - 14} {x + 1},{y - 20} Q{x + 6},{y - 12} {x + 5},{y - 4} Z" fill="#fff3c4" opacity=".9"/>'
            + embers +
            # figure, looking up at the sky
            f'<g fill="#050b14"><circle cx="{x + 46}" cy="{y - 44}" r="6.2"/>'
            f'<path d="M{x + 40},{y - 37} Q{x + 46},{y - 40} {x + 52},{y - 37} L{x + 54},{y - 14} L{x + 50},{y} L{x + 47},{y} L{x + 46},{y - 14} '
            f'L{x + 45},{y} L{x + 42},{y} L{x + 38},{y - 14} Z"/></g>'
            f'<path d="M{x + 40},{y - 36} Q{x + 34},{y - 30} {x + 37},{y - 22}" stroke="#050b14" stroke-width="3.4" fill="none" stroke-linecap="round"/>')


def running_border(x, y, w, h, r, color, delay=0.0, dur=5.5):
    d = (f"M{x + r},{y} H{x + w - r} A{r},{r} 0 0 1 {x + w},{y + r} V{y + h - r} A{r},{r} 0 0 1 {x + w - r},{y + h} "
         f"H{x + r} A{r},{r} 0 0 1 {x},{y + h - r} V{y + r} A{r},{r} 0 0 1 {x + r},{y} Z")
    return (f'<path class="run" style="animation-delay:{-delay:.2f}s;animation-duration:{dur}s" d="{d}" pathLength="100" fill="none" '
            f'stroke="{color}" stroke-width="2.2" stroke-dasharray="9 91" stroke-linecap="round" filter="url(#glow)"/>')


def countup(x, y, final: str, size, color, delay=0.3, frames=14, step=.07, anchor="start", extra=""):
    """A number that counts up to `final` (SMIL frame swap); non-numeric values are drawn as they are."""
    digits = final.replace(",", "")
    if not digits.isdigit():
        return t(x, y, final, size, color, SANS, 800, anchor, -1, extra)
    n = int(digits)
    out = []
    for k in range(frames):
        v = round(n * ((k + 1) / frames) ** 2.2)
        label = f"{v:,}" if "," in final else str(v)
        last = k == frames - 1
        out.append(f'<text x="{x}" y="{y}" font-family="{SANS}" font-size="{size}" font-weight="800" fill="{color}" text-anchor="{anchor}" '
                   f'letter-spacing="-1" opacity="0" {extra}>{label}'
                   f'<set attributeName="opacity" to="1" begin="{delay + k * step:.2f}s"' + ("" if last else f' dur="{step:.2f}s"') + "/></text>")
    return "".join(out)


# ------------------------------------------------------------------------------------------------ the living hero

def hero(coords: str, taglines: list[str]) -> str:
    W, H, horizon = 1000, 600, 452
    a_pts = [(48, 98), (68, 34), (88, 98), (57, 70), (79, 70)]
    s_pts = [(152, 42), (130, 33), (113, 45), (121, 64), (146, 74), (153, 91), (136, 101), (115, 95)]
    world = ("<g id='world'>"
             + aurora(W, 300, 210, 3, "te", opacity=.65, cls="sway2")
             + aurora(W, 262, 190, 7, "em")
             + aurora(W, 214, 130, 13, "ic", opacity=.45, cls="sway2", amp=18)
             + f'<g class="drift2">{mountains(W, horizon, 0, 300, 400, 21, "#0b1a2b", uid="a")}</g>'
             + f'<g class="drift">{mountains(W, horizon, 0, 368, 430, 34, "#071321", uid="b")}</g>'
             + "</g>")
    body = [ground(W, H, 18), milky_way(W, H), stars(W, 0, 380, 210, 11, .4),
            constellation(a_pts, [(0, 1), (1, 2), (3, 4)], 1.2, ICE) + constellation(s_pts, [(i, i + 1) for i in range(7)], 2.4, EMERALD,
                                                                                   "THE A.S. CONSTELLATION", (100, 124)),
            meteor(700, 60, 2), meteor(420, 34, 6.5), meteor(980, 120, 11), world,
            f'<rect x="0" y="{horizon - 40}" width="{W}" height="60" fill="{TEAL}" opacity=".06" filter="url(#soft)"/>',
            lake(W, H, horizon, "world")]
    # foreground ledge with the campfire
    g = horizon + 40
    top = [(-10, g - 12), (40, g - 26), (78, g - 18), (120, g - 4), (180, g + 2), (300, g + 2), (336, g + 12), (372, g + 34), (402, g + 62), (430, H + 5)]
    d = "M-10," + str(H + 5) + " L" + " L".join(f"{x},{y}" for x, y in top) + " Z"
    body.append(f'<linearGradient id="rock" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#c9e6f2" stop-opacity=".55"/>'
                f'<stop offset=".06" stop-color="#1b2c3d"/><stop offset=".35" stop-color="#08121d"/><stop offset="1" stop-color="#03070d"/></linearGradient>')
    body.append(f'<path d="{d}" fill="url(#rock)"/>')
    body.append(f'<polyline points="{" ".join(f"{x},{y}" for x, y in top[:-1])}" fill="none" stroke="#e6fbff" stroke-opacity=".55" stroke-width="1.4"/>')
    body.append(f'<g transform="translate(240 {g + 2}) scale(1.35) translate(-240 {-(g + 2)})">{campfire(240, g + 2)}</g>')
    body.append(snow(W, H, 70, 99))
    # title
    body.append(f'<g class="up" style="animation-delay:.2s">{t(W / 2, 64, coords, 11.5, ICE, MONO, 500, "middle", 4, "opacity=\".75\"")}</g>')
    body.append(f'<linearGradient id="shine" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="260" y2="0">'
                f'<stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".95"/>'
                f'<stop offset="1" stop-color="#fff" stop-opacity="0"/>'
                f'<animateTransform attributeName="gradientTransform" type="translate" from="-300 0" to="1300 0" dur="5s" begin="1.6s" repeatCount="indefinite"/>'
                f'</linearGradient>'
                f'<clipPath id="reveal"><rect x="0" y="80" width="0" height="110">'
                f'<animate attributeName="width" from="0" to="{W}" dur="1.8s" begin=".3s" fill="freeze" calcMode="spline" keySplines=".2 .8 .2 1" keyTimes="0;1"/></rect></clipPath>')
    name = lambda fill, extra="": t(W / 2, 156, "ADITYA SINGH", 78, fill, SANS, 800, "middle", 11, extra)
    body.append(f'<g clip-path="url(#reveal)"><g filter="url(#glow)">{name("url(#title)")}</g>{name("url(#shine)", "opacity=\".7\"")}</g>')
    body.append(f'<g class="up" style="animation-delay:1.4s">{t(W / 2, 200, "AI SYSTEMS  ·  AGENTS  ·  FULL-STACK", 15, TEXT, MONO, 500, "middle", 6)}</g>')
    for i, line in enumerate(taglines[:3]):
        body.append(f'<g class="cyc{" first" if i == 0 else ""}" style="animation-delay:{2 + i * 3.5:.1f}s">'
                    + t(W / 2, 238, line, 18, EMERALD, SANS, 500, "middle") + "</g>")
    body.append(f'<g class="up" style="animation-delay:1.8s">{t(W / 2, 268, "IIT Madras  ·  Scaler School of Technology", 15, MUTED, SANS, 400, "middle")}</g>')
    chips = [("◇  THE MODEL PROPOSES", ICE), ("■  THE SYSTEM CHECKS", AMBER), ("●  THE PERSON DECIDES", EMERALD)]
    widths = [len(c) * (10.5 * .61 + 1.4) + 24 for c, _ in chips]
    x = W - 36 - sum(widths) - 2 * 10
    for i, (label, color) in enumerate(chips):
        p, w = pill(x, H - 58, label, color, 10.5, 12, 28, .8)
        body.append(f'<g class="up" style="animation-delay:{2.2 + i * .25:.2f}s">{p}</g>')
        x += w + 10
    body.append(frame(W, H, 18))
    return svg(W, H, "Aditya Singh. AI systems, agents and full-stack. IIT Madras and Scaler School of Technology. A night scene: the "
                     "northern lights and the Milky Way over mountains and a frozen lake, the initials A.S. drawn as a constellation, "
                     "and a lone figure by a campfire watching the sky.", ripple_filter(), FX_CSS + "".join(body))


# ------------------------------------------------------------------------------------------------ rhythm: a day of light

DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]


def rhythm(r: dict, fetched: str) -> str:
    from aurora_art import CSS as _css, FAINT, STEEL, glass, synced, wrap  # noqa: F401
    W, H = 1000, 800
    x0, x1, horizon, ray_max = 92, 880, 432, 168
    col = (x1 - x0) / 24
    hx = lambda h: x0 + (h + .5) * col
    cycle = 24.0
    body = [ground(W, H, 18), stars(W, 0, 300, 120, 301, .35)]
    body.append(t(52, 46, "RHYTHM // WHEN THE CODE SHIPS", 12, ICE, MONO, 500, "start", 3))
    from aurora_art import synced as _sync
    body.append(_sync(W, 46, fetched))
    body.append(t(52, 82, f"CHRONOTYPE · DERIVED FROM {r['commits']} COMMITS, NOT SELF-DECLARED", 10, MUTED, MONO, 500, "start", 2))
    body.append(f'<g class="up" style="animation-delay:.2s" filter="url(#glow)">{t(50, 140, r["chronotype"], 54, "url(#title)", SANS, 800, "start", -1)}</g>')
    body.append(f'<g class="up" style="animation-delay:.4s">{t(52, 172, r["line"], 16, TEXT)}</g>')
    f0, f1, fn = r["focus"]
    tiles = [(f"{r['night']:.0%}", "AFTER DARK", "22:00 to 05:00 IST", ICE),
             (f"{f0:02d}–{f1:02d}", "FOCUS WINDOW", f"{fn} commits", EMERALD),
             (f"{r['weekend']:.0%}", "WEEKENDS", "Sat + Sun share", AMBER),
             (str(r["active_days"]), "ACTIVE DAYS", f"since {r['since']}", TEAL)]
    for i, (v, label, sub, c) in enumerate(tiles):
        x, y = 560 + (i % 2) * 200, 66 + (i // 2) * 64
        body.append(f'<g class="up" style="animation-delay:{.3 + i * .1:.2f}s">'
                    f'<rect x="{x}" y="{y}" width="188" height="54" rx="10" fill="#0b1b28" fill-opacity=".6" stroke="{ICE}" stroke-opacity=".12"/>'
                    f'<rect x="{x}" y="{y + 12}" width="2" height="30" fill="{c}"/>'
                    + t(x + 14, y + 20, label, 9, MUTED, MONO, 600, "start", 1.6) + t(x + 14, y + 44, v, 22, TEXT, SANS, 800)
                    + t(x + 180, y + 44, sub, 9.5, c, MONO, 400, "end") + "</g>")
    # the sky of one day: night at the edges, dawn, noon, dusk
    body.append(f'<linearGradient id="dayband" x1="0" y1="0" x2="1" y2="0">'
                f'<stop offset="0" stop-color="#0a1430"/><stop offset=".22" stop-color="#1b1f3e"/><stop offset=".27" stop-color="#5a3448"/>'
                f'<stop offset=".33" stop-color="#1f4a5c"/><stop offset=".5" stop-color="#1b5a66"/><stop offset=".7" stop-color="#1f4a5c"/>'
                f'<stop offset=".76" stop-color="#5a3040"/><stop offset=".82" stop-color="#1b1f3e"/><stop offset="1" stop-color="#0a1430"/></linearGradient>'
                f'<linearGradient id="dayfade" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#02050b" stop-opacity=".95"/>'
                f'<stop offset="1" stop-color="#02050b" stop-opacity=".1"/></linearGradient>'
                f'<clipPath id="above"><rect x="{x0 - 30}" y="200" width="{x1 - x0 + 60}" height="{horizon - 200}"/></clipPath>')
    body.append(f'<rect x="{x0 - 30}" y="200" width="{x1 - x0 + 60}" height="{horizon - 200}" rx="12" fill="url(#dayband)" opacity=".75"/>'
                f'<rect x="{x0 - 30}" y="200" width="{x1 - x0 + 60}" height="{horizon - 200}" rx="12" fill="url(#dayfade)"/>')
    peak = max(r["hours"]) or 1
    rays = []
    for h, c in enumerate(r["hours"]):
        x = hx(h)
        day = 6 <= h < 18
        color = "em" if day else "ic"
        f = (h + .5) / 24
        k1, k2, k3 = max(f - .03, .001), f, min(f + .07, .999)
        lit = (f'<animate attributeName="opacity" dur="{cycle}s" repeatCount="indefinite" '
               f'values=".55;.55;1;.55;.55" keyTimes="0;{k1:.3f};{k2:.3f};{k3:.3f};1"/>')
        if c == 0:
            rays.append(f'<circle cx="{x:.1f}" cy="{horizon - 4}" r="1.6" fill="{TEAL}" opacity=".5"/>')
            continue
        hgt = 10 + ray_max * math.sqrt(c / peak)
        rays.append(f'<g opacity=".55">{lit}<g class="breathe" style="animation-delay:{-h * .37:.2f}s">'
                    f'<rect x="{x - col * .36:.1f}" y="{horizon - hgt:.1f}" width="{col * .72:.1f}" height="{hgt:.1f}" rx="{col * .3:.1f}" fill="url(#cur-{color})" filter="url(#soft)"/>'
                    f'<rect x="{x - col * .2:.1f}" y="{horizon - hgt:.1f}" width="{col * .4:.1f}" height="{hgt:.1f}" rx="{col * .2:.1f}" fill="url(#cur-{color})"/>'
                    f'<rect x="{x - 1:.1f}" y="{horizon - hgt * .9:.1f}" width="2" height="{hgt * .9:.1f}" fill="#f4fffb" opacity=".7"/></g></g>')
        if c == peak:
            rays.append(f'<g class="fade" style="animation-delay:1.5s">{t(x, horizon - hgt - 12, f"PEAK {h:02d}:00 · {c}", 10, ICE, MONO, 700, "middle", 1.5)}</g>')
    body.append("".join(rays))
    # sun and moon on their arcs; the sun rises at 06:00 and sets at 18:00
    def arc(phase):
        pts = []
        for i in range(97):
            u = i / 96
            y = horizon - 34 - 150 * math.cos(2 * math.pi * (u - phase))
            pts.append(f"{x0 + u * (x1 - x0):.1f},{y:.1f}")
        return "M" + " L".join(pts)
    body.append(f'<path id="sunpath" d="{arc(.5)}" fill="none"/><path id="moonpath" d="{arc(0)}" fill="none"/>')
    body.append(f'<path d="{arc(.5)}" fill="none" stroke="{AMBER}" stroke-opacity=".12" stroke-dasharray="2 6" clip-path="url(#above)"/>')
    body.append(f'<radialGradient id="sunglow"><stop offset="0" stop-color="#fff4c9"/><stop offset=".3" stop-color="{AMBER}" stop-opacity=".9"/>'
                f'<stop offset="1" stop-color="{AMBER}" stop-opacity="0"/></radialGradient>'
                f'<g clip-path="url(#above)"><g><circle r="38" fill="url(#sunglow)" opacity=".55"/><circle r="11" fill="#fff4c9"/>'
                f'<animateMotion dur="{cycle}s" repeatCount="indefinite"><mpath href="#sunpath"/></animateMotion></g>'
                f'<g><circle r="26" fill="{ICE}" opacity=".18" filter="url(#soft)"/><circle r="10" fill="#eaf8ff"/><circle cx="4" cy="-3" r="9" fill="#0a1430"/>'
                f'<animateMotion dur="{cycle}s" repeatCount="indefinite"><mpath href="#moonpath"/></animateMotion></g></g>')
    body.append(mountains(W, horizon + 4, 0, horizon - 22, horizon - 2, 307, "#040c17", snow=False))
    body.append(f'<line x1="{x0 - 30}" y1="{horizon}" x2="{x1 + 30}" y2="{horizon}" stroke="{ICE}" stroke-opacity=".25"/>')
    for h in range(0, 24, 3):
        body.append(t(hx(h) - col / 2, horizon + 20, f"{h:02d}", 10.5, MUTED if h % 6 else TEXT, MONO, 600, "middle", 1))
    body.append(t(hx(6) - col / 2, horizon + 34, "DAWN", 8.5, AMBER, MONO, 600, "middle", 1.5) + t(hx(18) - col / 2, horizon + 34, "DUSK", 8.5, ROSE, MONO, 600, "middle", 1.5))
    # seven nights of aurora: weekday x hour
    gy = 498
    body.append(t(52, gy - 14, "SEVEN NIGHTS · WEEKDAY × HOUR · BRIGHTNESS = COMMITS", 10, MUTED, MONO, 500, "start", 2))
    gmax = max(max(row) for row in r["grid"]) or 1
    scan = (f'<rect x="{x0}" y="{gy - 4}" width="{col:.1f}" height="{7 * 22 + 4}" rx="4" fill="{ICE}" opacity=".07">'
            f'<animate attributeName="x" dur="{cycle}s" repeatCount="indefinite" from="{x0}" to="{x1 - col:.1f}"/></rect>')
    body.append(scan)
    bd, bh, _ = r["busiest"]
    for d in range(7):
        y = gy + d * 22
        total = sum(r["grid"][d])
        body.append(t(x0 - 14, y + 12, DAYS[d], 11, TEXT if d == bd else MUTED, MONO, 600 if d == bd else 400, "end"))
        cells = []
        for h in range(24):
            c = r["grid"][d][h]
            if not c:
                cells.append(f'<circle cx="{hx(h):.1f}" cy="{y + 8}" r="1" fill="{ICE}" opacity=".18"/>')
                continue
            a = .18 + .82 * math.sqrt(c / gmax)
            colr = EMERALD if 6 <= h < 18 else ICE
            cells.append(f'<rect x="{hx(h) - col * .46:.1f}" y="{y}" width="{col * .92:.1f}" height="16" rx="8" fill="{colr}" opacity="{a * .45:.2f}" filter="url(#mist)"/>'
                         f'<rect x="{hx(h) - col * .3:.1f}" y="{y + 5}" width="{col * .6:.1f}" height="6" rx="3" fill="{colr}" opacity="{a:.2f}"/>')
        body.append(f'<g class="slide" style="animation-delay:{.4 + d * .1:.2f}s">{"".join(cells)}</g>')
        bar = 56 * total / max(sum(row) for row in r["grid"])
        body.append(f'<rect x="{x1 + 16}" y="{y + 5}" width="56" height="6" rx="3" fill="{ICE}" opacity=".08"/>'
                    f'<rect x="{x1 + 16}" y="{y + 5}" width="{bar:.1f}" height="6" rx="3" fill="{EMERALD if d == bd else TEAL}" opacity=".8"/>'
                    + t(W - 26, y + 12, str(total), 10.5, TEXT if d == bd else MUTED, MONO, 600, "end"))
    bx, by = hx(bh), gy + bd * 22 + 8
    body.append(f'<circle cx="{bx:.1f}" cy="{by}" r="9" fill="none" stroke="{TEXT}" stroke-width="1.5"><animate attributeName="r" values="7;12;7" dur="2.4s" repeatCount="indefinite"/>'
                f'<animate attributeName="opacity" values="1;.3;1" dur="2.4s" repeatCount="indefinite"/></circle>')
    # the deepest session
    dy = gy + 7 * 22 + 34
    dp = r["deep"]
    hh, mm = divmod(dp["minutes"], 60)
    body.append(t(52, dy, "DEEPEST SESSION · NO GAP OVER 90 MIN", 10, MUTED, MONO, 500, "start", 2))
    body.append(f'<g class="up" style="animation-delay:.6s">{t(52, dy + 40, f"{hh}h {mm:02d}m", 36, TEXT, SANS, 800)}'
                + t(212, dy + 40, f'{dp["commits"]} commits · {dp["repo"]}', 16, EMERALD, SANS, 600)
                + t(52, dy + 62, f'{dp["start"]} → {dp["end"]} IST', 11, MUTED, MONO) + "</g>")
    sx0, sx1, sy = 520, 948, dy + 30
    span = max(dp["offsets"][-1], 1)
    body.append(f'<line x1="{sx0}" y1="{sy}" x2="{sx1}" y2="{sy}" stroke="{ICE}" stroke-opacity=".15" stroke-width="6" stroke-linecap="round"/>')
    ticks = "".join(f'<line x1="{sx0 + (sx1 - sx0) * o / span:.1f}" y1="{sy - 9}" x2="{sx0 + (sx1 - sx0) * o / span:.1f}" y2="{sy + 9}" '
                    f'stroke="{EMERALD}" stroke-width="1.4" opacity=".85"/>' for o in dp["offsets"])
    body.append(f'<clipPath id="sweep"><rect x="{sx0 - 2}" y="{sy - 12}" width="0" height="24">'
                f'<animate attributeName="width" from="0" to="{sx1 - sx0 + 4}" dur="3s" begin=".8s" fill="freeze"/></rect></clipPath>'
                f'<g clip-path="url(#sweep)">{ticks}</g>')
    body.append(t(sx0, sy + 26, dp["start"][-5:], 9.5, MUTED, MONO) + t(sx1, sy + 26, dp["end"], 9.5, MUTED, MONO, 400, "end"))
    lt = r["latest"]
    subj = lt["subject"] if len(lt["subject"]) < 64 else lt["subject"][:63] + "…"
    body.append(f'<circle class="blink" cx="58" cy="{H - 26}" r="4" fill="{EMERALD}"/>'
                + t(70, H - 22, f'LATEST  {lt["repo"]}  ·  {subj}  ·  {lt["when"]}', 10, MUTED, MONO, 400, "start", .6))
    body.append(t(W - 52, H - 22, f'BUSIEST  {DAYS[bd].upper()} {bh:02d}:00 · {r["busiest"][2]} COMMITS', 10, TEXT, MONO, 600, "end", 1))
    body.append(frame(W, H, 18))
    return svg(W, H, f'Rhythm: {r["chronotype"]}. {r["line"]} Busiest hour {bh:02d}:00 on {DAYS[bd]}. '
                     f'Deepest session {hh}h {mm}m, {dp["commits"]} commits on {dp["repo"]}.', "", FX_CSS + "".join(body))


def divider(label: str = "", seed: int = 1) -> str:
    W, H = 1000, 46
    rnd = random.Random(seed)
    pts = []
    for i in range(0, W + 1, 10):
        pts.append(f"{i},{H / 2 + 5 * math.sin(i * .018 + seed) + 2 * math.sin(i * .051 + seed * 2):.1f}")
    d = "M" + " L".join(pts)
    sparks = "".join(f'<circle class="tw" style="animation-delay:{rnd.uniform(0, 3):.1f}s" cx="{rnd.uniform(20, W - 20):.0f}" '
                     f'cy="{rnd.uniform(6, H - 6):.0f}" r="{rnd.choice([.6, .9, 1.2])}" fill="#e8fbff"/>' for _ in range(26))
    body = (f'<linearGradient id="thread" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{TEAL}" stop-opacity="0"/>'
            f'<stop offset=".3" stop-color="{EMERALD}"/><stop offset=".7" stop-color="{ICE}"/><stop offset="1" stop-color="{TEAL}" stop-opacity="0"/></linearGradient>'
            + sparks
            + f'<path id="thr" d="{d}" fill="none" stroke="url(#thread)" stroke-width="5" opacity=".25" filter="url(#soft)"/>'
            + f'<path d="{d}" fill="none" stroke="url(#thread)" stroke-width="1.2"/>'
            + f'<g><circle r="9" fill="{EMERALD}" opacity=".25" filter="url(#soft)"/><circle r="2.4" fill="#f4fffb"/>'
            + f'<animateMotion dur="7s" repeatCount="indefinite"><mpath href="#thr"/></animateMotion></g>')
    if label:
        w = len(label) * 8.2 + 40
        body += (f'<rect x="{W / 2 - w / 2}" y="{H / 2 - 12}" width="{w}" height="24" rx="12" fill="#06121c" stroke="{ICE}" stroke-opacity=".25"/>'
                 + t(W / 2, H / 2 + 4, label, 10.5, ICE, MONO, 600, "middle", 3))
    return svg(W, H, label or "divider", "", body)
