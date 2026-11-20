"""Scenes for the Aurora profile. Every function returns a standalone, animated SVG string.

World: a night sky over mountains. The year's contributions are the northern lights, every repo is a peak,
languages are rock strata, recent commits are a trail to the summit, and the contact card is a signal flare.
Palette: emerald, teal and ice for light; amber for the checks.
"""

from __future__ import annotations

import math
import random
from datetime import date, datetime
from xml.sax.saxutils import escape

NIGHT0, NIGHT1, NIGHT2 = "#02050b", "#061224", "#0a1b2e"
EMERALD, TEAL, ICE, AMBER, ROSE, STEEL = "#3df5a7", "#19d3c5", "#9eeaff", "#ffb547", "#ff7a90", "#7fa6c9"
TEXT, MUTED, FAINT = "#eafff8", "#93b7b2", "#47676b"
KIND = {"model": ICE, "rule": AMBER, "person": EMERALD, "io": STEEL}
CAT = {"ai": EMERALD, "agents": TEAL, "product": ICE, "systems": AMBER, "other": STEEL}
CAT_LABEL = {"ai": "AI SYSTEMS", "agents": "AGENTS", "product": "PRODUCTS", "systems": "SYSTEMS", "other": "OTHER"}
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, 'Liberation Mono', monospace"
SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Inter, Helvetica, Arial, sans-serif"

CSS = (
    ".tw{animation:tw 3.4s ease-in-out infinite}@keyframes tw{0%,100%{opacity:.2}50%{opacity:1}}"
    ".sway{transform-box:fill-box;transform-origin:50% 100%;animation:sway 13s ease-in-out infinite alternate}"
    "@keyframes sway{0%{transform:translateX(-22px) skewX(-4deg)}100%{transform:translateX(22px) skewX(4deg)}}"
    ".sway2{transform-box:fill-box;transform-origin:50% 100%;animation:sway 17s ease-in-out -6s infinite alternate-reverse}"
    ".sh{animation:sh 2.8s ease-in-out infinite}@keyframes sh{0%,100%{opacity:.35}50%{opacity:1}}"
    ".br{animation:br 5s ease-in-out infinite}@keyframes br{0%,100%{opacity:.6}50%{opacity:1}}"
    ".rise{transform-box:fill-box;transform-origin:50% 100%;animation:rise 1.2s cubic-bezier(.2,.8,.2,1) both}"
    # Entrances never hide content: the first frame is what thumbnails, link previews and a reader who
    # scrolls quickly see, so text, cards and charts start visible and only settle into place.
    "@keyframes rise{from{transform:scaleY(.35)}to{transform:scaleY(1)}}"
    ".up{animation:up .9s ease-out both}@keyframes up{from{transform:translateY(10px)}to{transform:none}}"
    ".fade{animation:fade 1s ease-out both}@keyframes fade{from{filter:brightness(1.7)}to{filter:none}}"
    ".slide{animation:slide 1s cubic-bezier(.2,.8,.2,1) both}@keyframes slide{from{transform:translateX(-14px)}to{transform:none}}"
    ".draw{stroke-dasharray:1;stroke-dashoffset:1;animation:draw 2.4s ease-out both}@keyframes draw{to{stroke-dashoffset:0}}"
    ".blink{animation:blink 1.6s steps(2,start) infinite}@keyframes blink{to{opacity:.2}}"
    ".surge{animation:surge 11s cubic-bezier(.45,0,.55,1) infinite}"
    "@keyframes surge{0%{transform:translateX(0)}70%,100%{transform:translateX(var(--run,1500px))}}"
    # "alive" layer for otherwise still corners: moving, fading and drawing only, never blur or masks
    ".flow{stroke-dasharray:7 93;animation:flow var(--d,7s) linear infinite}@keyframes flow{to{stroke-dashoffset:-100}}"
    ".scan{animation:scan var(--d,6s) ease-in-out infinite}"
    "@keyframes scan{0%{transform:translateY(0);opacity:0}12%,82%{opacity:1}100%{transform:translateY(var(--dy,100px));opacity:0}}"
    ".mistx{animation:mistx 24s ease-in-out infinite alternate}@keyframes mistx{from{transform:translateX(-90px)}to{transform:translateX(90px)}}"
    ".spin{transform-box:fill-box;transform-origin:center;animation:spin 9s linear infinite}@keyframes spin{to{transform:rotate(360deg)}}"
    ".ping{transform-box:fill-box;transform-origin:center;opacity:0;animation:ping var(--d,9s) ease-out infinite}"
    "@keyframes ping{0%{transform:scale(.6);opacity:.95}10%{transform:scale(2.6);opacity:0}100%{opacity:0}}"
    ".sheen{animation:sheen 8s ease-in-out infinite}@keyframes sheen{0%,60%{transform:translateX(0)}100%{transform:translateX(var(--run,800px))}}"
    ".meteor{animation:meteor 9s linear infinite}"
    "@keyframes meteor{0%,82%{opacity:0;transform:translate(0,0)}84%{opacity:1}96%{opacity:0;transform:translate(-260px,120px)}100%{opacity:0}}"
    "@media (prefers-reduced-motion: reduce){*{animation:none!important}.draw{stroke-dasharray:none}"
    ".flow,.scan,.mistx,.ping,.sheen,.fx-move{display:none}}"
)


# ------------------------------------------------------------------------------------------------ primitives

def svg(W: float, H: float, label: str, defs: str, body: str) -> str:
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" '
            f'aria-label="{escape(label, {chr(34): "&quot;"})}"><style>{CSS}</style><defs>{BASE_DEFS}{defs}</defs>{body}</svg>')


BASE_DEFS = (
    f'<linearGradient id="night" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{NIGHT0}"/>'
    f'<stop offset=".6" stop-color="{NIGHT1}"/><stop offset="1" stop-color="{NIGHT2}"/></linearGradient>'
    '<filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="5" result="b"/>'
    '<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>'
    '<filter id="soft" x="-20%" y="-50%" width="140%" height="200%"><feGaussianBlur stdDeviation="9"/></filter>'
    '<filter id="mist" x="-10%" y="-50%" width="120%" height="200%"><feGaussianBlur stdDeviation="2.2"/></filter>'
    f'<linearGradient id="title" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{ICE}"/>'
    f'<stop offset=".55" stop-color="{EMERALD}"/><stop offset="1" stop-color="{TEAL}"/></linearGradient>'
    f'<linearGradient id="warm" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{AMBER}"/>'
    f'<stop offset="1" stop-color="{ROSE}"/></linearGradient>'
    # A real curtain is coloured by height: red and magenta oxygen glow at the crown, the familiar green
    # through the body, a hot yellow-green lower edge, and a thin pink-violet nitrogen fringe below it.
    + "".join(
        f'<linearGradient id="ray-{k}" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0" stop-color="#ff5c8a" stop-opacity="0"/><stop offset=".14" stop-color="#ff4f86" stop-opacity=".2"/>'
        f'<stop offset=".34" stop-color="#c46bff" stop-opacity=".12"/><stop offset=".5" stop-color="{c}" stop-opacity=".24"/>'
        f'<stop offset=".8" stop-color="{c}" stop-opacity=".72"/><stop offset=".93" stop-color="#e4ffb8" stop-opacity="1"/>'
        f'<stop offset=".97" stop-color="#ff86d0" stop-opacity=".75"/><stop offset="1" stop-color="#b47cff" stop-opacity="0"/></linearGradient>'
        for k, c in (("em", "#45ff9b"), ("te", "#3ef0c4"), ("ic", "#8bffd8"), ("am", AMBER))
    )
    + '<linearGradient id="surge-band" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#000"/>'
      '<stop offset=".5" stop-color="#fff"/><stop offset="1" stop-color="#000"/></linearGradient>'
    + '<radialGradient id="star-halo"><stop offset="0" stop-color="#fff" stop-opacity=".55"/>'
      '<stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>'
    + "".join(
        f'<linearGradient id="cur-{k}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{c}" stop-opacity="0"/>'
        f'<stop offset=".3" stop-color="{c}" stop-opacity=".45"/><stop offset=".78" stop-color="{c}" stop-opacity=".9"/>'
        f'<stop offset="1" stop-color="#f2fffb" stop-opacity="1"/></linearGradient>'
        for k, c in (("em", EMERALD), ("te", TEAL), ("ic", ICE))
    )
)


def t(x, y, text, size=14, color=TEXT, family=SANS, weight=400, anchor="start", spacing=0, extra=""):
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-family="{family}" font-size="{size}" font-weight="{weight}" fill="{color}" '
            f'text-anchor="{anchor}" letter-spacing="{spacing}" {extra}>{escape(str(text))}</text>')


def wrap(text: str, limit: int) -> list[str]:
    lines, cur = [], ""
    for word in str(text).split():
        if cur and len(cur) + 1 + len(word) > limit:
            lines.append(cur)
            cur = word
        else:
            cur = f"{cur} {word}".strip()
    return lines + ([cur] if cur else [])


def ground(W, H, rx=16):
    return f'<rect width="{W}" height="{H}" rx="{rx}" fill="url(#night)"/>'


def frame(W, H, rx=16):
    return f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="{rx}" fill="none" stroke="{ICE}" stroke-opacity=".12"/>'


def stars(W, top, bottom, n, seed, twinkle=.3):
    """Stars with real colour temperatures (blue-white, white, warm), most faint, a few bright with a halo."""
    rnd, out = random.Random(seed), []
    tints = ["#dff9ff", "#ffffff", "#ffffff", "#cfdcff", "#ffe8c2", "#ffd6b0"]
    for i in range(n):
        x, y = rnd.uniform(8, W - 8), top + (bottom - top) * rnd.random() ** 1.6  # denser near the top
        r = rnd.choice([.4, .5, .5, .6, .7, .8, 1, 1.2, 1.6])
        op = rnd.uniform(.25, .9)
        tint = rnd.choice(tints)
        cls = f' class="tw" style="animation-delay:{rnd.uniform(0, 3.4):.2f}s;animation-duration:{rnd.uniform(2.2, 5):.1f}s"' if rnd.random() < twinkle else ""
        if r >= 1.2:
            out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r * 4:.1f}" fill="url(#star-halo)" opacity="{op * .5:.2f}"/>')
        out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{tint}" opacity="{op:.2f}"{cls}/>')
    return "".join(out)


def meteor(x, y, delay=0):
    return (f'<g class="meteor" style="animation-delay:{delay}s"><line x1="{x}" y1="{y}" x2="{x + 70}" y2="{y - 32}" '
            f'stroke="url(#title)" stroke-width="1.4" stroke-linecap="round" opacity=".9"/>'
            f'<circle cx="{x}" cy="{y}" r="1.8" fill="#fff"/></g>')


def aurora(W, low, height, seed, color="em", step=6, opacity=1.0, cls="sway", amp=26, x0=-80, x1=None):
    """One aurora curtain, drawn the way a real one looks.

    Thin rays of uneven width and height hang from a wavy crown to a bright lower edge. The curtain folds:
    rays are pushed sideways by a slow wave, so they bunch (and glow brighter) where the sheet turns toward
    the viewer and thin out where it turns away. A bright surge travels along it every few seconds."""
    x1 = W + 80 if x1 is None else x1
    rnd = random.Random(seed)
    p = [rnd.uniform(0, 6.28) for _ in range(6)]
    f = [rnd.uniform(.004, .007), rnd.uniform(.011, .019), rnd.uniform(.002, .004), rnd.uniform(.008, .013)]
    fold = step * 2.6
    groups = [[] for _ in range(5)]
    edge = []
    u = x0
    while u <= x1:
        x = u + fold * math.sin(u * f[3] + p[3])
        bunch = 1 + fold * f[3] * math.cos(u * f[3] + p[3])  # >1 where rays spread out, <1 where they bunch
        lo = low + amp * math.sin(x * f[0] + p[0]) + amp * .45 * math.sin(x * f[1] + p[1])
        hi = lo - height * (.5 + .5 * (.5 + .5 * math.sin(x * f[2] + p[2]))) * rnd.uniform(.82, 1.12)
        w = rnd.uniform(.7, 1.5) * step * .8
        op = min(1, rnd.uniform(.3, .85) / max(bunch, .55))
        groups[rnd.randrange(5)].append(
            f'<rect x="{x:.1f}" y="{hi:.1f}" width="{w:.1f}" height="{lo - hi + 6:.1f}" fill="url(#ray-{color})" opacity="{op:.2f}"/>')
        edge.append(f"{x:.1f},{lo:.1f}")
        u += step * rnd.uniform(.85, 1.25)
    uid = f"au{seed}"
    rays = f'<g id="{uid}">' + "".join(f'<g class="sh" style="animation-delay:{i * .55:.2f}s;animation-duration:{2.2 + i * .45:.2f}s">{"".join(g)}</g>'
                                       for i, g in enumerate(groups)) + "</g>"
    c = {"em": EMERALD, "te": TEAL, "ic": ICE, "am": AMBER}[color]
    pts = " ".join(edge)
    line = (f'<polyline points="{pts}" fill="none" stroke="#e4ffb8" stroke-width="1.6" opacity=".6" filter="url(#mist)"/>'
            f'<polyline points="{pts}" fill="none" stroke="#ff86d0" stroke-width="2.4" opacity=".22" transform="translate(0 5)" filter="url(#mist)"/>')
    top, span = low - height - 2 * amp, height + 4 * amp
    run = (x1 - x0) + 520
    # Only the main, full-brightness curtain carries a surge: each one costs a mask on every frame, and the
    # faint curtains behind text-heavy panels gain little from it.
    surge = "" if opacity < .9 else (f'<mask id="sg{seed}" maskUnits="userSpaceOnUse" x="{x0}" y="{top:.0f}" width="{x1 - x0}" height="{span:.0f}">'
             f'<rect class="surge" style="--run:{run}px;animation-delay:{-rnd.uniform(0, 11):.1f}s;animation-duration:{rnd.uniform(9, 14):.1f}s" '
             f'x="{x0 - 480}" y="{top:.0f}" width="420" height="{span:.0f}" fill="url(#surge-band)"/></mask>'
             f'<use href="#{uid}" mask="url(#sg{seed})" opacity=".9"/>')
    return (f'<g class="{cls}" opacity="{opacity}"><use href="#{uid}" filter="url(#soft)" opacity=".8"/>'
            f'<g filter="url(#mist)">{rays}</g>{surge}{line}</g>')


def ridge(W, base, top_min, top_max, seed, rough=1.0, x0=-10, x1=None):
    """A mountain range: overlapping sharp peaks (each a cone with its own slope) plus fine rock texture.
    `rough` scales the texture. Returns (points, highest y)."""
    x1 = W + 10 if x1 is None else x1
    rnd = random.Random(seed)
    peaks, x = [], x0 - 40
    while x < x1 + 40:
        peaks.append((x, rnd.uniform(top_min, top_max), rnd.uniform(.45, 1.15), rnd.uniform(.45, 1.15)))
        x += rnd.uniform(70, 170)
    floor = top_max + (top_max - top_min) * .35
    noise = [0.0]
    for _ in range(int((x1 - x0) / 6) + 2):
        noise.append(max(-1, min(1, noise[-1] + rnd.uniform(-.55, .55))))
    line = []
    for i, xx in enumerate(range(int(x0), int(x1) + 1, 6)):
        y = floor
        for px, py, sl, sr in peaks:
            y = min(y, py + (sl if xx < px else sr) * abs(xx - px))
        line.append((xx, y + noise[i] * 3.2 * rough))
    return line, min(y for _, y in line)


def mountains(W, H, base_top, top_min, top_max, seed, fill, snow=True, uid="m", rough=1.0):
    line, peak = ridge(W, base_top, top_min, top_max, seed, rough)
    d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in line) + f" L{W + 10},{H + 2} L-10,{H + 2} Z"
    if snow:
        grad = (f'<linearGradient id="snow-{uid}" gradientUnits="userSpaceOnUse" x1="0" y1="{peak:.0f}" x2="0" y2="{peak + 52:.0f}">'
                f'<stop offset="0" stop-color="#e2fff4" stop-opacity=".92"/><stop offset=".3" stop-color="#a6dcd0" stop-opacity=".6"/>'
                f'<stop offset=".65" stop-color="#4f7f88" stop-opacity=".35"/><stop offset="1" stop-color="{fill}"/></linearGradient>')
        rim = " ".join(f"{x:.1f},{y:.1f}" for x, y in line)
        return (grad + f'<path d="{d}" fill="url(#snow-{uid})"/>'
                f'<polyline points="{rim}" fill="none" stroke="{EMERALD}" stroke-width="1.2" opacity=".28" filter="url(#mist)"/>')
    return f'<path d="{d}" fill="{fill}"/>'


def glass(x, y, w, h, rx=14, accent=None, op=.5):
    out = (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="#0b1b28" fill-opacity="{op}" '
           f'stroke="{ICE}" stroke-opacity=".14"/>')
    if accent:
        out += f'<rect x="{x + rx}" y="{y}" width="{w - 2 * rx}" height="1.6" fill="{accent}" opacity=".8"/>'
    return out


def border_run(x, y, w, h, r, color, delay=0.0, dur=7.0, width=1.6):
    """A short light that runs round a rounded rectangle's border."""
    d = (f"M{x + r},{y} H{x + w - r} A{r},{r} 0 0 1 {x + w},{y + r} V{y + h - r} A{r},{r} 0 0 1 {x + w - r},{y + h} "
         f"H{x + r} A{r},{r} 0 0 1 {x},{y + h - r} V{y + r} A{r},{r} 0 0 1 {x + r},{y} Z")
    return (f'<path class="flow" style="--d:{dur:.1f}s;animation-delay:{-delay:.2f}s" d="{d}" pathLength="100" fill="none" '
            f'stroke="{color}" stroke-width="{width}" stroke-linecap="round" opacity=".9"/>')


def drifting_mist(W, y, h, color=ICE, op=.07):
    """Low mist that drifts sideways: two soft ellipses, a gradient instead of a blur filter."""
    return (f'<radialGradient id="mistg"><stop offset="0" stop-color="{color}" stop-opacity="{op}"/><stop offset="1" stop-color="{color}" stop-opacity="0"/></radialGradient>'
            f'<g class="mistx"><ellipse cx="{W * .3:.0f}" cy="{y}" rx="{W * .38:.0f}" ry="{h / 2:.0f}" fill="url(#mistg)"/>'
            f'<ellipse cx="{W * .78:.0f}" cy="{y + h * .15:.0f}" rx="{W * .3:.0f}" ry="{h * .4:.0f}" fill="url(#mistg)"/></g>')


def pill(x, y, text, color, size=11, pad=12, h=26, fill_op=.55):
    w = len(text) * (size * .61 + 1.4) + pad * 2
    return (f'<rect x="{x:.1f}" y="{y}" width="{w:.1f}" height="{h}" rx="{h / 2}" fill="#06121c" fill-opacity="{fill_op}" stroke="{color}" stroke-opacity=".55"/>'
            + t(x + w / 2, y + h / 2 + size * .36, text, size, color, MONO, 500, "middle", 1.4)), w


def glyph(kind, cx, cy, s, color):
    """Small line icons drawn on a 24-unit grid around (cx, cy)."""
    k = s / 24
    P = lambda *pts: " ".join(f"{cx + (px - 12) * k:.1f},{cy + (py - 12) * k:.1f}" for px, py in pts)
    st = f'fill="none" stroke="{color}" stroke-width="{1.6 * max(k, .8):.2f}" stroke-linecap="round" stroke-linejoin="round"'
    if kind == "scales":
        return (f'<polyline points="{P((12, 4), (12, 20))}" {st}/><polyline points="{P((5, 7), (19, 7))}" {st}/>'
                f'<polyline points="{P((8, 20), (16, 20))}" {st}/><polyline points="{P((5, 7), (2.5, 13), (7.5, 13), (5, 7))}" {st}/>'
                f'<polyline points="{P((19, 7), (16.5, 13), (21.5, 13), (19, 7))}" {st}/>')
    if kind == "window":
        return (f'<rect x="{cx - 9 * k:.1f}" y="{cy - 8 * k:.1f}" width="{18 * k:.1f}" height="{14 * k:.1f}" rx="{2 * k:.1f}" {st}/>'
                f'<polyline points="{P((3, 8), (21, 8))}" {st}/><polyline points="{P((7, 12), (9.5, 14), (7, 16))}" {st}/>'
                f'<polyline points="{P((11.5, 16), (15, 16))}" {st}/><polyline points="{P((9, 22), (15, 22))}" {st}/>')
    if kind == "wave":
        return (f'<polyline points="{P((2, 12), (5, 12), (7, 7), (9, 17), (11, 4), (13, 20), (15, 9), (17, 14), (19, 12), (22, 12))}" {st}/>')
    if kind == "graph":
        return (f'<polyline points="{P((5, 6), (12, 12), (19, 7))}" {st}/><polyline points="{P((12, 12), (8, 19))}" {st}/>'
                f'<polyline points="{P((12, 12), (17, 18))}" {st}/>'
                + "".join(f'<circle cx="{cx + (px - 12) * k:.1f}" cy="{cy + (py - 12) * k:.1f}" r="{2.2 * k:.1f}" {st}/>'
                          for px, py in ((5, 6), (12, 12), (19, 7), (8, 19), (17, 18))))
    if kind == "ticket":
        return (f'<polyline points="{P((3, 7), (21, 7), (21, 10), (19.5, 12), (21, 14), (21, 17), (3, 17), (3, 14), (4.5, 12), (3, 10), (3, 7))}" {st}/>'
                f'<polyline points="{P((9, 10), (15, 10))}" {st}/><polyline points="{P((9, 14), (13, 14))}" {st}/>')
    if kind == "cart":
        return (f'<polyline points="{P((2, 4), (5, 4), (7.5, 15), (18, 15), (20.5, 7), (6, 7))}" {st}/>'
                f'<circle cx="{cx - 3 * k:.1f}" cy="{cy + 7 * k:.1f}" r="{1.6 * k:.1f}" {st}/><circle cx="{cx + 5 * k:.1f}" cy="{cy + 7 * k:.1f}" r="{1.6 * k:.1f}" {st}/>')
    if kind == "prompt":
        return f'<polyline points="{P((4, 7), (10, 12), (4, 17))}" {st}/><polyline points="{P((12, 18), (20, 18))}" {st}/>'
    if kind == "grid":
        return (f'<rect x="{cx - 9 * k:.1f}" y="{cy - 8 * k:.1f}" width="{18 * k:.1f}" height="{17 * k:.1f}" rx="{2 * k:.1f}" {st}/>'
                f'<polyline points="{P((3, 9), (21, 9))}" {st}/><polyline points="{P((8, 2), (8, 6))}" {st}/>'
                f'<polyline points="{P((16, 2), (16, 6))}" {st}/><polyline points="{P((8, 13), (10.5, 15.5), (16, 11))}" {st}/>')
    if kind == "loop":
        return (f'<path d="M{cx - 9 * k:.1f},{cy:.1f} a{6 * k:.1f},{6 * k:.1f} 0 1 1 {6 * k:.1f},{6 * k:.1f} M{cx + 9 * k:.1f},{cy:.1f} '
                f'a{6 * k:.1f},{6 * k:.1f} 0 1 1 {-6 * k:.1f},{-6 * k:.1f}" {st}/>'
                f'<polyline points="{P((5, 18), (9, 18), (9, 14))}" {st}/><polyline points="{P((19, 6), (15, 6), (15, 10))}" {st}/>')
    if kind == "shield":
        return (f'<polyline points="{P((12, 3), (20, 6), (19.5, 13), (12, 21), (4.5, 13), (4, 6), (12, 3))}" {st}/>'
                f'<polyline points="{P((8.5, 12), (11, 14.5), (15.5, 9.5))}" {st}/>')
    return ""


def fmt_day(iso: str) -> str:
    return datetime.fromisoformat(iso.replace("Z", "+00:00")).strftime("%d %b %H:%M UTC").upper()


def synced(W, y, iso):
    return (t(W - 52, y, f"SYNCED {fmt_day(iso)}", 11, MUTED, MONO, 400, "end", 2)
            + f'<circle class="blink" cx="{W - 38}" cy="{y - 4}" r="4" fill="{EMERALD}"/>')


# ------------------------------------------------------------------------------------------------ 1. hero

def hero(coords: str) -> str:
    W, H = 1000, 500
    body = [ground(W, H), stars(W, 0, 330, 190, 11, .35), meteor(860, 70, 2), meteor(560, 40, 6.5),
            aurora(W, 262, 190, 3, "te", opacity=.65, cls="sway2"),
            aurora(W, 228, 170, 7, "em"),
            aurora(W, 180, 120, 13, "ic", opacity=.45, cls="sway2", amp=18),
            mountains(W, H, 0, 268, 385, 21, "#0b1a2b", uid="a"),
            f'<rect x="0" y="330" width="{W}" height="90" fill="{TEAL}" opacity=".05" filter="url(#soft)"/>',
            mountains(W, H, 0, 330, 425, 34, "#071321", uid="b"),
            mountains(W, H, 0, 405, 462, 55, "#030a13", snow=False, rough=1.0)]
    body.append(f'<g class="up" style="animation-delay:.2s">{t(W / 2, 74, coords, 11.5, ICE, MONO, 500, "middle", 4, "opacity=\".75\"")}</g>')
    body.append(f'<g class="up" style="animation-delay:.4s" filter="url(#glow)">'
                f'{t(W / 2, 160, "ADITYA SINGH", 74, "url(#title)", SANS, 800, "middle", 10)}</g>')
    body.append(f'<g class="up" style="animation-delay:.7s">{t(W / 2, 203, "AI SYSTEMS  ·  AGENTS  ·  FULL-STACK", 15, TEXT, MONO, 500, "middle", 6)}</g>')
    body.append(f'<g class="up" style="animation-delay:.9s">'
                f'<line x1="{W / 2 - 150}" y1="226" x2="{W / 2 - 18}" y2="226" stroke="{ICE}" stroke-opacity=".35"/>'
                f'<line x1="{W / 2 + 18}" y1="226" x2="{W / 2 + 150}" y2="226" stroke="{ICE}" stroke-opacity=".35"/>'
                f'<rect x="{W / 2 - 5}" y="221" width="10" height="10" transform="rotate(45 {W / 2} 226)" fill="none" stroke="{EMERALD}"/>'
                f'{t(W / 2, 258, "IIT Madras  ·  Scaler School of Technology", 16.5, MUTED, SANS, 400, "middle")}</g>')
    chips = [("◇  THE MODEL PROPOSES", ICE), ("■  THE SYSTEM CHECKS", AMBER), ("●  THE PERSON DECIDES", EMERALD)]
    widths = [len(c) * (11 * .61 + 1.4) + 28 for c, _ in chips]
    x = (W - sum(widths) - 2 * 16) / 2
    for i, (label, color) in enumerate(chips):
        p, w = pill(x, 430, label, color, 11, 14, 30, .75)
        body.append(f'<g class="up" style="animation-delay:{1.3 + i * .25:.2f}s">{p}</g>')
        x += w + 16
    body.append(frame(W, H))
    return svg(W, H, "Aditya Singh. AI systems, agents and full-stack. IIT Madras and Scaler School of Technology. "
                     "The model proposes, the system checks, the person decides.", "", "".join(body))


# ------------------------------------------------------------------------------------------------ 2. sky (contributions)

def sky(gh: dict, weeks: list[dict], active: int, longest: int, current: int, n_repos: int) -> str:
    W, H = 1000, 590
    import aurora_fx as fx
    body = [fx.FX_CSS, ground(W, H), stars(W, 150, 470, 120, 5, .3), meteor(820, 190, 4)]
    body.append(t(52, 44, "SKY // THE LAST 12 MONTHS", 12, ICE, MONO, 500, "start", 3))
    body.append(synced(W, 44, gh["fetched_at"]))
    tiles = [("CONTRIBUTIONS", f'{gh["totals"]["contributions"]:,}', "last 12 months", EMERALD),
             ("COMMITS", f'{gh["totals"]["commits"]:,}', "authored", TEAL),
             ("ACTIVE DAYS", f"{active}", "of 365", ICE),
             ("LONGEST STREAK", f"{longest}", f"days · now {current}", AMBER),
             ("PUBLIC REPOS", f"{n_repos}", "original work", ROSE)]
    tw, gap = (W - 104 - 4 * 14) / 5, 14
    for i, (label, value, sub, color) in enumerate(tiles):
        x = 52 + i * (tw + gap)
        body.append(f'<g class="up" style="animation-delay:{.1 + i * .1:.2f}s">{glass(x, 64, tw, 92, 12, color)}'
                    f'{t(x + 16, 88, label, 10, MUTED, MONO, 500, "start", 2)}'
                    f'{t(x + 16, 124, value, 32, TEXT, SANS, 700)}'
                    f'{t(x + 16, 141, sub, 10.5, color, MONO)}</g>'
                    + border_run(x, 64, tw, 92, 12, color, delay=i * 1.6, dur=8))
    base, top = 440, 206
    peak = max((w["count"] for w in weeks), default=0) or 1
    n = len(weeks)
    x0, span = 60, W - 120
    step = span / max(n, 1)
    rays_glow, rays = [[] for _ in range(4)], [[] for _ in range(4)]
    for i, w in enumerate(weeks):
        x = x0 + i * step
        if w["count"] == 0:
            rays[i % 4].append(f'<circle cx="{x + step / 2:.1f}" cy="{base - 3}" r="1.3" fill="{TEAL}" opacity=".45"/>')
            continue
        h = 14 + (base - top - 14) * math.sqrt(w["count"] / peak)
        color = "ic" if w["count"] >= .7 * peak else "em" if w["count"] >= .25 * peak else "te"
        r = f'<rect x="{x + step * .06:.1f}" y="{base - h:.1f}" width="{step * .88:.1f}" height="{h:.1f}" rx="{step * .3:.1f}" fill="url(#cur-{color})"/>'
        core = (f'<rect x="{x + step * .44:.1f}" y="{base - h * .92:.1f}" width="{step * .12:.1f}" height="{h * .92:.1f}" '
                f'fill="#f2fffb" opacity=".55"/>')
        wrap_open = f'<g class="breathe" style="animation-delay:{-i * .29:.2f}s;animation-duration:{3.4 + (i % 5) * .7:.1f}s">'
        rays[i % 4].append(wrap_open + r + core + "</g>")
        rays_glow[i % 4].append(wrap_open + r + "</g>")
    layer = lambda groups: "".join(f'<g class="sh" style="animation-delay:{k * .7:.1f}s">{"".join(g)}</g>' for k, g in enumerate(groups))
    body.append(f'<g class="sway" style="animation-duration:20s"><g filter="url(#soft)">{layer(rays_glow)}</g>'
                f'<g filter="url(#soft)">{layer(rays_glow)}</g><g filter="url(#mist)">{layer(rays)}</g></g>')
    avg = sum(w["count"] for w in weeks) / max(n, 1)
    if avg > 0:
        ay = base - (14 + (base - top - 14) * math.sqrt(avg / peak))
        body.append(f'<line x1="{x0}" y1="{ay:.1f}" x2="{x0 + span}" y2="{ay:.1f}" stroke="{AMBER}" stroke-opacity=".55" stroke-dasharray="4 6"/>')
        body.append(t(x0, ay - 7, f"avg {avg:.0f} / week", 10.5, AMBER, MONO))
    if weeks and peak > 0:
        pi = max(range(n), key=lambda i: weeks[i]["count"])
        px = x0 + pi * step + step / 2
        py = base - (14 + (base - top - 14))
        label = f'PEAK {peak} · WEEK OF {date.fromisoformat(weeks[pi]["start"]).strftime("%d %b").upper()}'
        lx = min(max(px, 150), W - 150)
        body.append(f'<g class="fade" style="animation-delay:1.2s"><circle cx="{px:.1f}" cy="{py - 10:.1f}" r="4" fill="{ICE}" filter="url(#glow)"/>'
                    f'{t(lx, py - 22, label, 11, ICE, MONO, 600, "middle", 2)}</g>')
    body.append(mountains(W, H, 0, 448, 488, 77, "#071321", uid="s"))
    body.append(mountains(W, H, 0, 492, 512, 91, "#030a13", snow=False, rough=.8))
    seen, last_x = set(), -99
    for i, w in enumerate(weeks):
        d = date.fromisoformat(w["start"])
        key = (d.year, d.month)
        if key in seen or d.day > 7 and i or x0 + i * step - last_x < 52:
            continue
        seen.add(key)
        last_x = x0 + i * step
        label = d.strftime("%b").upper() + (f" '{d.strftime('%y')}" if d.month == 1 or i == 0 else "")
        body.append(t(x0 + i * step + 2, 538, label, 10.5, MUTED, MONO, 400, "start", 1.5))
    body.append(t(52, 570, "ONE CURTAIN = ONE WEEK  ·  HEIGHT = CONTRIBUTIONS (SQUARE-ROOT SCALE)", 10, FAINT, MONO, 400, "start", 2))
    body.append(t(W - 52, 570, "LIVE FROM THE GITHUB API", 10, FAINT, MONO, 400, "end", 2))
    body.append(frame(W, H))
    return svg(W, H, f'Contributions over the last 12 months drawn as northern lights: {gh["totals"]["contributions"]} contributions, '
                     f'{active} active days, longest streak {longest} days.', "", "".join(body))


# ------------------------------------------------------------------------------------------------ 3. base camp

def basecamp(loop_rules: list[tuple[str, str, str]]) -> str:
    W, H = 1000, 500
    body = [ground(W, H), stars(W, 0, 220, 80, 17, .25), aurora(W, 160, 120, 29, "em", opacity=.35, cls="sway2", x0=520)]
    body.append(t(52, 58, "BASE CAMP // ADITYA SINGH", 12, ICE, MONO, 500, "start", 3))
    body.append(f'<g class="up" style="animation-delay:.2s">{t(52, 114, "What happens when", 40, TEXT, SANS, 700)}'
                f'{t(52, 162, "the model is wrong?", 40, "url(#title)", SANS, 800)}</g>')
    para = ("I study Data Science & Applications at IIT Madras, co-enrolled at Scaler School of Technology, and I build "
            "LLM systems, local desktop agents and full-stack products. Most of the work goes into the layer around the "
            "model: rules that can overrule it, retrieval that keeps it honest, consent before it acts, and a way to undo.")
    for i, line in enumerate(wrap(para, 60)):
        body.append(f'<g class="up" style="animation-delay:{.4 + i * .06:.2f}s">{t(52, 204 + i * 25, line, 15.5, MUTED)}</g>')
    quote_y = 204 + len(wrap(para, 60)) * 25 + 22
    body.append(f'<g class="up" style="animation-delay:.9s"><rect x="52" y="{quote_y - 16}" width="3" height="40" fill="{AMBER}"/>'
                f'{t(66, quote_y, "Read the situation. Coordinate the squad.", 14, TEXT, SANS, 600)}'
                f'{t(66, quote_y + 20, "Review the mistakes. Queue again.", 14, TEXT, SANS, 600)}</g>')
    x = 52
    chip_boxes = []
    for i, (label, color) in enumerate([("IIT MADRAS · CGPA 9.0", EMERALD), ("SCALER SOT", ICE), ("PARADOX DSA · RUNNER-UP", AMBER)]):
        p, w = pill(x, H - 62, label, color, 10.5, 12, 26)
        body.append(f'<g class="up" style="animation-delay:{1.1 + i * .15:.2f}s">{p}</g>')
        chip_boxes.append(f'<rect x="{x:.1f}" y="{H - 62}" width="{w:.1f}" height="26" rx="13"/>')
        x += w + 10
    body.append(f'<clipPath id="chipclip">{"".join(chip_boxes)}</clipPath><g clip-path="url(#chipclip)">'
                f'<g class="sheen" style="--run:{x - 52 + 120:.0f}px"><rect x="10" y="{H - 66}" width="34" height="34" fill="#ffffff" opacity=".22" '
                f'transform="skewX(-20)"/></g></g>')
    # the loop
    cx, cy, R = 772, 168, 88
    nodes = [("MODEL", "proposes", ICE, -90), ("SYSTEM", "checks", AMBER, 30), ("PERSON", "decides", EMERALD, 150)]
    pos = [(cx + R * math.cos(math.radians(a)), cy + R * math.sin(math.radians(a))) for *_, a in nodes]
    body.append(t(cx, 38, "THE LOOP", 11, MUTED, MONO, 500, "middle", 4))
    for i in range(3):
        (ax, ay), (bx, by) = pos[i], pos[(i + 1) % 3]
        mx, my = (ax + bx) / 2, (ay + by) / 2
        ox, oy = mx - cx, my - cy
        k = 1.55
        d = f"M{ax:.1f},{ay:.1f} Q{cx + ox * k:.1f},{cy + oy * k:.1f} {bx:.1f},{by:.1f}"
        body.append(f'<path id="loop{i}" d="{d}" fill="none" stroke="{nodes[i][2]}" stroke-opacity=".35" stroke-width="1.5" stroke-dasharray="3 5"/>')
        for j in range(3):
            body.append(f'<circle r="2.6" fill="{nodes[i][2]}" filter="url(#glow)"><animateMotion dur="3.6s" begin="{j * 1.2 + i * .4:.1f}s" '
                        f'repeatCount="indefinite" keyPoints="0.14;0.86" keyTimes="0;1" calcMode="linear"><mpath href="#loop{i}"/></animateMotion></circle>')
    for (label, sub, color, _), (x, y) in zip(nodes, pos):
        body.append(f'<g class="br"><circle cx="{x:.1f}" cy="{y:.1f}" r="40" fill="{color}" opacity=".10" filter="url(#soft)"/></g>'
                    f'<circle cx="{x:.1f}" cy="{y:.1f}" r="32" fill="#06121c" stroke="{color}" stroke-width="1.6"/>'
                    + t(x, y + 1, label, 11.5, color, MONO, 700, "middle", 2) + t(x, y + 16, sub, 10.5, MUTED, MONO, 400, "middle"))
    y = 290
    for i, (title, line1, color) in enumerate(loop_rules):
        body.append(f'<g class="up" style="animation-delay:{.8 + i * .2:.2f}s">'
                    f'{t(600, y, f"0{i + 1}", 12, color, MONO, 700)}{t(628, y, title, 15.5, TEXT, SANS, 700)}')
        for j, line in enumerate(wrap(line1, 50)):
            body.append(t(628, y + 21 + j * 18, line, 13, MUTED))
        body.append("</g>")
        y += 21 + len(wrap(line1, 50)) * 18 + 20
    body.append(frame(W, H))
    return svg(W, H, "Base camp: Aditya Singh builds the layer around the model. The loop: the model proposes, the system checks, the person decides.",
               "", "".join(body))


# ------------------------------------------------------------------------------------------------ 4. expeditions

def flow(x0, x1, y, steps, color, uid):
    out, n = [], len(steps)
    xs = [x0 + (x1 - x0) * i / (n - 1) for i in range(n)]
    out.append(f'<path id="{uid}" d="M{xs[0]:.1f},{y} L{xs[-1]:.1f},{y}" stroke="{ICE}" stroke-opacity=".25" stroke-width="1.4"/>')
    out.append(f'<circle r="3" fill="{color}" filter="url(#glow)"><animateMotion dur="3.4s" repeatCount="indefinite"><mpath href="#{uid}"/></animateMotion></circle>')
    for x, (kind, label) in zip(xs, steps):
        c = KIND[kind]
        shape = (f'<rect x="{x - 8:.1f}" y="{y - 8}" width="16" height="16" fill="#06121c" stroke="{c}" stroke-width="1.6"/>' if kind == "rule"
                 else f'<rect x="{x - 8:.1f}" y="{y - 8}" width="16" height="16" rx="3" transform="rotate(45 {x:.1f} {y})" fill="#06121c" stroke="{c}" stroke-width="1.6"/>' if kind == "model"
                 else f'<circle cx="{x:.1f}" cy="{y}" r="8.5" fill="#06121c" stroke="{c}" stroke-width="1.6"/>')
        out.append(shape + t(x, y + 26, label.upper(), 9, MUTED, MONO, 500, "middle", 1))
    return "".join(out)


def expeditions(flagships: list[dict], systems: list[dict], metrics: dict, cats: dict, n_links: int, live: dict | None = None) -> str:
    import aurora_fx as fx
    live = live or {}
    W = 1000
    rows = (len(flagships) + 2) // 3
    cw, ch, gap, y0 = 290, 372, 23, 146
    H = y0 + rows * (ch + 22) + 212
    body = [fx.FX_CSS, ground(W, H), stars(W, 0, 140, 70, 41, .25), aurora(W, 120, 110, 47, "te", opacity=.3, cls="sway2")]
    body.append(t(52, 52, "EXPEDITIONS // FLAGSHIP SYSTEMS", 12, ICE, MONO, 500, "start", 3))
    body.append(t(52, 92, "Where the model meets a rule.", 30, TEXT, SANS, 700))
    body.append(t(52, 118, f"{len(flagships)} flagships and {len(systems)} more climbs, each with a number read live from its own repository.", 14, MUTED))
    for i, (v, l, c) in enumerate([(str(len(flagships)), "FLAGSHIPS", EMERALD), (str(len(flagships) + len(systems)), "SYSTEMS", ICE), (str(n_links), "CODE LINKS", AMBER)]):
        x = W - 52 - (2 - i) * 104
        body.append(t(x, 92, v, 32, c, SANS, 700, "end") + t(x, 112, l, 9.5, MUTED, MONO, 500, "end", 2))
    for i, f in enumerate(flagships):
        x = 52 + (i % 3) * (cw + gap)
        y0 = 146 + (i // 3) * (ch + 22)
        color = CAT.get(cats.get(f["repo"], "other"))
        g = [f'<g class="up" style="animation-delay:{.2 + i * .18:.2f}s">',
             f'<rect x="{x}" y="{y0}" width="{cw}" height="{ch}" rx="18" fill="{color}" opacity=".06" filter="url(#soft)"/>',
             glass(x, y0, cw, ch, 18, color, .7),
             fx.running_border(x, y0, cw, ch, 18, color, delay=i * 1.3, dur=6 + (i % 3)),
             f'<circle cx="{x + 42}" cy="{y0 + 48}" r="24" fill="none" stroke="{color}" stroke-width="1.5">'
             f'<animate attributeName="r" values="24;36" dur="2.8s" begin="{i * .5:.1f}s" repeatCount="indefinite"/>'
             f'<animate attributeName="opacity" values=".7;0" dur="2.8s" begin="{i * .5:.1f}s" repeatCount="indefinite"/></circle>',
             f'<circle cx="{x + 42}" cy="{y0 + 48}" r="24" fill="{color}" opacity=".12"/>',
             f'<circle cx="{x + 42}" cy="{y0 + 48}" r="24" fill="none" stroke="{color}" stroke-opacity=".6"/>',
             glyph(f["glyph"], x + 42, y0 + 48, 26, color),
             t(x + 78, y0 + 46, f["name"], 23, TEXT, SANS, 700), t(x + 78, y0 + 65, f["tag"], 9.5, color, MONO, 500, "start", 1.5)]
        for j, line in enumerate(wrap(f["pitch"], 38)[:3]):
            g.append(t(x + 22, y0 + 108 + j * 20, line, 14, MUTED))
        value = metrics.get(f["repo"], "·")
        g.append(fx.countup(x + 22, y0 + 210, value, 48, "url(#title)", delay=.6 + i * .15, extra='filter="url(#glow)"'))
        if live.get(f["repo"]):
            g.append(f'<rect x="{x + cw - 86}" y="{y0 + 180}" width="64" height="22" rx="11" fill="{EMERALD}" fill-opacity=".12" stroke="{EMERALD}" stroke-opacity=".6"/>'
                     f'<circle class="blink" cx="{x + cw - 71}" cy="{y0 + 191}" r="3.5" fill="{EMERALD}"/>'
                     + t(x + cw - 46, y0 + 195, "LIVE", 10, EMERALD, MONO, 700, "middle", 1.5))
        for j, line in enumerate(wrap(f["metric"]["label"], 36)[:2]):
            g.append(t(x + 22, y0 + 234 + j * 16, line.upper(), 10, MUTED, MONO, 500, "start", 1.2))
        g.append(f'<line x1="{x + 22}" y1="{y0 + 262}" x2="{x + cw - 22}" y2="{y0 + 262}" stroke="{ICE}" stroke-opacity=".1"/>')
        g.append(flow(x + 34, x + cw - 34, y0 + 294, f["flow"], color, f"fl{i}"))
        g.append(t(x + 22, y0 + ch - 20, f["stack"], 10.5, FAINT, MONO))
        g.append("</g>")
        body.append("".join(g))
    n_sys = max(len(systems), 1)
    sw, sgap, sy = (W - 104 - (n_sys - 1) * 14) / n_sys, 14, 146 + rows * (ch + 22) + 14
    body.append(t(52, sy - 8, "ALSO CLIMBED", 10.5, MUTED, MONO, 500, "start", 3))
    for i, s in enumerate(systems):
        x = 52 + i * (sw + sgap)
        color = CAT.get(cats.get(s["repo"], "other"))
        value = metrics.get(s["repo"], "·")
        size = 26 if len(value) <= 6 else 19
        body.append(f'<g class="up" style="animation-delay:{.8 + i * .1:.2f}s">{glass(x, sy + 6, sw, 140, 14, color, .65)}'
                    f'{fx.running_border(x, sy + 6, sw, 140, 14, color, delay=2 + i * 1.1, dur=7)}'
                    f'{glyph(s["glyph"], x + 26, sy + 34, 20, color)}{t(x + 46, sy + 39, s["name"], 15, TEXT, SANS, 700)}'
                    f'{t(x + 16, sy + 64, s["tag"], 8.5, color, MONO, 500, "start", 1.2)}'
                    f'{fx.countup(x + 16, sy + 102, value, size, TEXT, delay=1 + i * .12)}'
                    + "".join(t(x + 16, sy + 122 + j * 13, line.upper(), 8.8, MUTED, MONO, 500, "start", .8)
                              for j, line in enumerate(wrap(s["metric"]["label"], int(sw / 6.6))[:2])) + "</g>")
    legend = [("◇ MODEL", ICE), ("■ CHECK", AMBER), ("● PERSON", EMERALD), ("● DATA", STEEL)]
    x = 52
    for label, c in legend:
        body.append(t(x, H - 18, label, 10, c, MONO, 500, "start", 1.5))
        x += len(label) * 7 + 24
    body.append(t(W - 52, H - 18, "NUMBERS ARE RE-READ FROM EACH REPO ON EVERY REFRESH", 10, FAINT, MONO, 400, "end", 1.5))
    body.append(frame(W, H))
    return svg(W, H, "Flagship systems: " + "; ".join(f'{f["name"]}: {f["pitch"]}' for f in flagships), "", "".join(body))


# ------------------------------------------------------------------------------------------------ 5. terrain

def terrain(repos: list[dict], cats: dict, flags: list[str], fetched: str) -> str:
    W, H = 1000, 500
    body = [ground(W, H), stars(W, 0, 260, 110, 61, .3), aurora(W, 170, 130, 67, "em", opacity=.4)]
    total_mb = sum(r["kb"] for r in repos) / 1024
    since = min((r["created"] for r in repos), default=fetched[:10])
    body.append(t(52, 48, "TERRAIN // EVERY PUBLIC REPO IS A PEAK", 12, ICE, MONO, 500, "start", 3))
    body.append(t(W - 52, 48, f"{len(repos)} PEAKS · {total_mb:.1f} MB OF CODE · SINCE {date.fromisoformat(since).strftime('%b %Y').upper()}",
                  11, MUTED, MONO, 400, "end", 2))
    base = 408
    if not repos:
        return svg(W, H, "Terrain", "", "".join(body) + frame(W, H))
    d0 = date.fromisoformat(since).toordinal() - 20
    d1 = date.fromisoformat(fetched[:10]).toordinal() + 12
    X = lambda iso: 70 + (date.fromisoformat(iso).toordinal() - d0) / (d1 - d0) * (W - 140)
    maxkb = max(r["kb"] for r in repos) or 1
    order = sorted(range(len(repos)), key=lambda i: repos[i]["created"])
    rank = {i: k for k, i in enumerate(order)}
    grads = "".join(
        f'<linearGradient id="peak-{k}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#effcff" stop-opacity=".95"/>'
        f'<stop offset=".09" stop-color="{c}" stop-opacity=".85"/><stop offset=".4" stop-color="{c}" stop-opacity=".32"/>'
        f'<stop offset="1" stop-color="{NIGHT1}" stop-opacity=".96"/></linearGradient>' for k, c in CAT.items())
    shapes = []
    for i in sorted(range(len(repos)), key=lambda i: -repos[i]["kb"]):
        r = repos[i]
        x = X(r["created"])
        h = 46 + 226 * math.log1p(r["kb"]) / math.log1p(maxkb)
        w = 24 + h * .36
        rnd = random.Random(r["name"])
        j = lambda a: a * rnd.uniform(.85, 1.15)
        pts = [(x - w, base), (x - w * .58, base - j(h * .42)), (x - w * .3, base - j(h * .7)), (x - w * .12, base - h * .9),
               (x, base - h), (x + w * .18, base - j(h * .8)), (x + w * .4, base - j(h * .55)), (x + w * .7, base - j(h * .25)), (x + w, base)]
        cat = cats.get(r["name"], "other")
        d = "M" + " L".join(f"{px:.1f},{py:.1f}" for px, py in pts) + " Z"
        shapes.append((rank[i], f'<g class="rise" style="animation-delay:{.15 + rank[i] * .09:.2f}s"><path d="{d}" fill="url(#peak-{cat})"/>'
                                f'<polyline points="{" ".join(f"{px:.1f},{py:.1f}" for px, py in pts[1:-1])}" fill="none" stroke="{CAT[cat]}" '
                                f'stroke-opacity=".75" stroke-width="1.2"/></g>', r, x, base - h))
    body += [s[1] for s in shapes]
    body.append(f'<rect x="0" y="{base - 10}" width="{W}" height="60" fill="{NIGHT2}" opacity=".7" filter="url(#soft)"/>')
    import aurora_fx as fx
    body.insert(0, fx.FX_CSS)
    for k, (my, op, dur) in enumerate([(base - 40, .16, 30), (base - 90, .1, 38), (base - 18, .22, 26)]):
        body.append(f'<ellipse class="mist" style="animation-duration:{dur}s;animation-delay:{-k * 7}s" cx="{W / 2}" cy="{my}" rx="{W * .7}" ry="14" '
                    f'fill="#cfeff6" opacity="{op}" filter="url(#soft)"/>')
    body.append(f'<line x1="60" y1="{base + 6}" x2="{W - 60}" y2="{base + 6}" stroke="{ICE}" stroke-opacity=".25"/>')
    # quarter ticks
    q = date.fromordinal(d0).replace(day=1)
    while q.toordinal() < d1:
        if q.month in (1, 4, 7, 10) and q.toordinal() > d0:
            x = 70 + (q.toordinal() - d0) / (d1 - d0) * (W - 140)
            body.append(f'<line x1="{x:.1f}" y1="{base + 2}" x2="{x:.1f}" y2="{base + 10}" stroke="{ICE}" stroke-opacity=".4"/>'
                        + t(x, base + 26, f"Q{(q.month - 1) // 3 + 1} '{q.strftime('%y')}", 10.5, MUTED, MONO, 400, "middle", 1.5))
        q = date(q.year + (q.month // 12), q.month % 12 + 1, 1)
    flagged = [s for s in shapes if s[2]["name"] in flags]
    flagged.sort(key=lambda s: s[3])
    placed = []  # label boxes already drawn, so the next one climbs higher instead of overlapping
    names_ = {"codecrafters-shell-cpp": "C++ Shell", "Meta_OpenEnv": "Meta OpenEnv", "Shopkart": "ShopKart"}
    for k, (_, _, r, x, top) in enumerate(flagged):
        lw_ = len(names_.get(r["name"], r["name"])) * 7.4 + 18
        pole = 26
        while True:
            box = (x - lw_ / 2 - 4, top - pole - 24, x + lw_ / 2 + 4, top - pole)
            if box[1] < 64 or not any(box[0] < b[2] and b[0] < box[2] and box[1] < b[3] and b[1] < box[3] for b in placed):
                break
            pole += 12
        if box[1] < 64:  # out of sky: tuck the label beside the peak instead
            pole = max(18, top - 90)
            box = (x - lw_ / 2 - 4, top - pole - 24, x + lw_ / 2 + 4, top - pole)
        placed.append(box)
        cat = CAT[cats.get(r["name"], "other")]
        name = {"codecrafters-shell-cpp": "C++ Shell", "Meta_OpenEnv": "Meta OpenEnv", "Shopkart": "ShopKart"}.get(r["name"], r["name"])
        lw = len(name) * 7.4 + 18
        body.append(f'<g class="fade" style="animation-delay:{1.6 + k * .12:.2f}s">'
                    f'<line x1="{x:.1f}" y1="{top:.1f}" x2="{x:.1f}" y2="{top - pole:.1f}" stroke="{TEXT}" stroke-opacity=".7"/>'
                    f'<path fill="{cat}" opacity=".9" d="M{x:.1f},{top - pole + 2:.1f} q8,-3 16,1 v9 q-8,-4 -16,-1 z">'
                    f'<animate attributeName="d" dur="{1.6 + k * .2:.1f}s" repeatCount="indefinite" values="'
                    f'M{x:.1f},{top - pole + 2:.1f} q8,-3 16,1 v9 q-8,-4 -16,-1 z;M{x:.1f},{top - pole + 2:.1f} q8,3 16,-1 v9 q-8,4 -16,1 z;'
                    f'M{x:.1f},{top - pole + 2:.1f} q8,-3 16,1 v9 q-8,-4 -16,-1 z"/></path>'
                    f'<rect x="{x - lw / 2:.1f}" y="{top - pole - 22:.1f}" width="{lw:.1f}" height="20" rx="10" fill="#06121c" stroke="{cat}"/>'
                    + t(x, top - pole - 8, name, 11.5, TEXT, SANS, 600, "middle") + "</g>")
    x = 52
    for k, label in CAT_LABEL.items():
        if not any(cats.get(r["name"], "other") == k for r in repos):
            continue
        body.append(f'<circle cx="{x + 5}" cy="{H - 26}" r="4.5" fill="{CAT[k]}"/>' + t(x + 16, H - 22, label, 10, MUTED, MONO, 500, "start", 1.5))
        x += len(label) * 7.2 + 40
    body.append(t(W - 52, H - 22, "HEIGHT = CODE SIZE · POSITION = WHEN IT BEGAN", 10, FAINT, MONO, 400, "end", 1.5))
    body.append(frame(W, H))
    return svg(W, H, f"Terrain: {len(repos)} public repositories drawn as mountain peaks, height by code size, placed by start date.",
               grads, "".join(body))


# ------------------------------------------------------------------------------------------------ 6. bedrock

def bedrock(shares: list[tuple[str, float]], n_repos: int) -> str:
    W, H = 1000, 430
    colors = [ICE, EMERALD, TEAL, AMBER, STEEL, ROSE, "#5b7290"]
    body = [ground(W, H), stars(W, 0, 90, 60, 71, .3), aurora(W, 96, 70, 73, "em", opacity=.35, amp=10)]
    body.append(t(52, 44, "BEDROCK // WHAT EVERYTHING IS BUILT ON", 12, ICE, MONO, 500, "start", 3))
    body.append(t(W - 52, 44, f"BY BYTES OF CODE · {n_repos} REPOS", 11, MUTED, MONO, 400, "end", 2))
    surface, depth = 128, 250
    # surface with snow and pines
    line, _ = ridge(W, surface, surface - 14, surface + 2, 79, .8)
    d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in line)
    rnd = random.Random(83)
    pines = []
    for _ in range(26):
        x = rnd.uniform(20, W - 20)
        y = min(py for px, py in line if abs(px - x) < 14) + 2
        s = rnd.uniform(.6, 1.2)
        pines.append(f'<polygon points="{x:.1f},{y - 26 * s:.1f} {x - 7 * s:.1f},{y - 8 * s:.1f} {x - 3 * s:.1f},{y - 9 * s:.1f} {x - 9 * s:.1f},{y:.1f} {x + 9 * s:.1f},{y:.1f} {x + 3 * s:.1f},{y - 9 * s:.1f} {x + 7 * s:.1f},{y - 8 * s:.1f}" fill="#04101b"/>')
    body.append("".join(pines))
    body.append(f'<path d="{d}" fill="none" stroke="#e6fbff" stroke-opacity=".75" stroke-width="2.4"/>')
    small = sum(s for n, s in shares if s < .015 or n == "Other")
    shares = [(n, s) for n, s in shares if s >= .015 and n != "Other"] + ([("Other", small)] if small else [])
    floor = 26
    spare = depth - floor * len(shares)
    thick = [floor + spare * s for _, s in shares]
    y = surface + 4
    prev = [(x, py + 4) for x, py in line]
    for i, ((name, share), h) in enumerate(zip(shares, thick)):
        c = colors[i % len(colors)]
        ph = random.Random(i * 13).uniform(0, 6.28)
        bottom = [(x, y + h + 5 * math.sin(x * .012 + ph) + 3 * math.sin(x * .031 + ph * 2)) for x in range(-10, W + 20, 20)]
        if i == len(shares) - 1:
            bottom = [(x, H - 18) for x, _ in bottom]
        top_pts = " L".join(f"{x:.1f},{py:.1f}" for x, py in prev)
        bot_pts = " L".join(f"{x:.1f},{py:.1f}" for x, py in reversed(bottom))
        pid = f"tex{i}"
        dots = (f'<pattern id="{pid}" width="{9 + i * 3}" height="{7 + i * 2}" patternUnits="userSpaceOnUse">'
                f'<circle cx="2" cy="2" r="{.8 + (i % 3) * .3:.1f}" fill="{c}" opacity=".35"/></pattern>')
        body.append(f'<defs>{dots}</defs><g class="slide" style="animation-delay:{.2 + i * .14:.2f}s">'
                    f'<path d="M{top_pts} L{bot_pts} Z" fill="{c}" fill-opacity=".14"/>'
                    f'<path d="M{top_pts} L{bot_pts} Z" fill="url(#{pid})"/>'
                    f'<polyline points="{" ".join(f"{x:.1f},{py:.1f}" for x, py in prev)}" fill="none" stroke="{c}" stroke-opacity=".65" stroke-width="1.4"/>'
                    f'<polyline class="flow" style="--d:{9 + i * 1.3:.1f}s;animation-delay:{-i * 2.1:.1f}s" pathLength="100" '
                    f'points="{" ".join(f"{x:.1f},{py:.1f}" for x, py in prev)}" fill="none" stroke="{c}" stroke-width="2.2" stroke-linecap="round"/>')
        mid = y + h / 2 + 5
        size = 17 if h >= 34 else 13
        body.append(t(70, mid, name, size, TEXT, SANS, 700) + t(70 + len(name) * size * .58 + 14, mid, f"{share * 100:.1f}%", size - 3, c, MONO, 600))
        body.append("</g>")
        prev = bottom
        y += h
    # drill core
    cx, cw = W - 120, 34
    body.append(t(cx + cw / 2, surface - 26, "CORE", 9.5, MUTED, MONO, 500, "middle", 2))
    cy = surface
    for i, ((_, share), h) in enumerate(zip(shares, thick)):
        hh = (H - 18 - surface) * h / sum(thick)
        body.append(f'<rect class="fade" style="animation-delay:{.4 + i * .14:.2f}s" x="{cx}" y="{cy:.1f}" width="{cw}" height="{hh:.1f}" '
                    f'fill="{colors[i % len(colors)]}" fill-opacity=".55" stroke="{NIGHT0}"/>')
        cy += hh
    body.append(f'<rect x="{cx}" y="{surface}" width="{cw}" height="{H - 18 - surface}" rx="4" fill="none" stroke="{ICE}" stroke-opacity=".4"/>')
    body.append(f'<g class="scan" style="--dy:{H - 26 - surface}px;--d:5s"><rect x="{cx - 6}" y="{surface}" width="{cw + 12}" height="3" rx="1.5" fill="#f2fffb" opacity=".85"/>'
                f'<rect x="{cx}" y="{surface - 10}" width="{cw}" height="10" fill="{ICE}" opacity=".18"/></g>')
    body.append(frame(W, H))
    return svg(W, H, "Bedrock: languages by bytes of code. " + ", ".join(f"{n} {s * 100:.1f}%" for n, s in shares), "", "".join(body))


# ------------------------------------------------------------------------------------------------ 7. trail

def catmull(points, samples=18):
    out = []
    pts = [points[0]] + points + [points[-1]]
    for i in range(1, len(pts) - 2):
        p0, p1, p2, p3 = pts[i - 1], pts[i], pts[i + 1], pts[i + 2]
        for s in range(samples):
            u = s / samples
            u2, u3 = u * u, u * u * u
            out.append(tuple(.5 * ((2 * p1[k]) + (-p0[k] + p2[k]) * u + (2 * p0[k] - 5 * p1[k] + 4 * p2[k] - p3[k]) * u2
                                   + (-p0[k] + 3 * p1[k] - 3 * p2[k] + p3[k]) * u3) for k in range(2)))
    return out + [points[-1]]


def trail(commits: list[dict], names: dict, cats: dict, fetched: str) -> str:
    W, H = 1000, 560
    body = [ground(W, H), stars(W, 0, 260, 120, 97, .3), aurora(W, 200, 150, 101, "em", opacity=.55), aurora(W, 150, 90, 103, "ic", opacity=.3, cls="sway2")]
    body.append(t(52, 48, "TRAIL LOG // LATEST ASCENTS", 12, ICE, MONO, 500, "start", 3))
    body.append(synced(W, 48, fetched))
    peak = (800, 112)
    mtn = [(140, H), (330, 420), (420, 380), (520, 300), (600, 250), (690, 170), (760, 140), peak, (850, 140), (900, 190), (960, 230), (1010, 260), (1010, H)]
    body.append(f'<linearGradient id="mt" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e6fbff" stop-opacity=".9"/>'
                f'<stop offset=".09" stop-color="#9cc6d8" stop-opacity=".5"/><stop offset=".22" stop-color="#0c1d2f"/><stop offset="1" stop-color="#050e19"/></linearGradient>')
    body.append(f'<polygon points="{" ".join(f"{x},{y}" for x, y in mtn)}" fill="url(#mt)"/>')
    body.append(mountains(W, H, 0, 470, 520, 107, "#030a13", snow=False, rough=.8))
    way = [(110, 506), (470, 470), (330, 420), (600, 365), (470, 300), (680, 245), (600, 190), peak]
    path = catmull(way)
    d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in path)
    body.append(f'<path id="trail" d="{d}" fill="none" stroke="{AMBER}" stroke-opacity=".25" stroke-width="5" stroke-linecap="round"/>')
    body.append(f'<path class="draw" pathLength="1" d="{d}" fill="none" stroke="{AMBER}" stroke-width="1.6" stroke-dasharray="1" stroke-linecap="round"/>')
    body.append(f'<g><circle r="22" fill="{AMBER}" opacity=".16" filter="url(#soft)"/><circle r="4.5" fill="#fff1c9" filter="url(#glow)"/>'
                f'<animateMotion dur="11s" repeatCount="indefinite"><mpath href="#trail"/></animateMotion></g>')
    lengths = [0.0]
    for (ax, ay), (bx, by) in zip(path, path[1:]):
        lengths.append(lengths[-1] + math.hypot(bx - ax, by - ay))
    total = lengths[-1]
    picks = list(reversed(commits[:8]))
    n = len(picks)
    y_lo, y_hi = path[0][1] - 8, peak[1]
    for i, c in enumerate(picks):
        target_y = y_lo - (y_lo - y_hi) * i / max(n - 1, 1)
        k = next((j for j, (_, py) in enumerate(path) if py <= target_y), len(path) - 1)
        x, y = path[k]
        color = CAT[cats.get(c["repo"], "other")]
        cw = 318
        right = x < 430
        cx = x + 30 if right else 36
        if not right and cx + cw > x - 24:
            cx = x - 30 - cw
        cx = min(max(cx, 24), W - 24 - cw)
        cy = y - 22
        subject = c["subject"] if len(c["subject"]) <= 44 else c["subject"][:43] + "…"
        frac = lengths[k] / total
        k1, k2 = max(frac - .001, .0005), min(frac + .07, .999)
        body.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="6" fill="none" stroke="{AMBER}" stroke-width="2" opacity="0">'
                    f'<animate attributeName="r" dur="11s" repeatCount="indefinite" values="6;6;22;22" keyTimes="0;{k1:.4f};{k2:.4f};1"/>'
                    f'<animate attributeName="opacity" dur="11s" repeatCount="indefinite" values="0;0;.9;0;0" keyTimes="0;{k1:.4f};{(k1 + .002):.4f};{k2:.4f};1"/></circle>')
        body.append(f'<g class="up" style="animation-delay:{.5 + i * .22:.2f}s">'
                    f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{cx + (0 if right else cw):.1f}" y2="{y:.1f}" stroke="{color}" stroke-opacity=".5"/>'
                    f'<circle cx="{x:.1f}" cy="{y:.1f}" r="6" fill="#06121c" stroke="{color}" stroke-width="2"/>'
                    f'<circle cx="{x:.1f}" cy="{y:.1f}" r="2.4" fill="{color}"/>'
                    + glass(cx, cy, cw, 44, 10, None, .82)
                    + t(cx + 12, cy + 17, f'{c["date"]}  ·  {names.get(c["repo"], c["repo"]).upper()}', 10, color, MONO, 600, "start", 1)
                    + t(cx + 12, cy + 35, subject, 13, TEXT) + "</g>")
    if n:
        body.append(f'<g class="fade" style="animation-delay:2.4s"><line x1="{peak[0]}" y1="{peak[1]}" x2="{peak[0]}" y2="{peak[1] - 44}" stroke="{TEXT}"/>'
                    f'<polygon points="{peak[0]},{peak[1] - 44} {peak[0] + 26},{peak[1] - 37} {peak[0]},{peak[1] - 30}" fill="{EMERALD}"/>'
                    + t(peak[0] + 32, peak[1] - 33, "NOW", 11, EMERALD, MONO, 700, "start", 2) + "</g>")
    body.append(drifting_mist(W, H - 70, 120, ICE, .09))
    body.append(t(52, H - 20, "EACH WAYPOINT = ONE COMMIT · NEWEST AT THE SUMMIT", 10, FAINT, MONO, 400, "start", 1.5))
    body.append(frame(W, H))
    return svg(W, H, "Trail log: latest commits as waypoints up a mountain. " + "; ".join(f'{c["date"]} {c["repo"]}: {c["subject"]}' for c in commits[:8]),
               "", "".join(body))


# ------------------------------------------------------------------------------------------------ 8. flare

def flare() -> str:
    W, H = 1000, 470
    horizon = 352
    sky_art = (aurora(W, 250, 180, 111, "em") + aurora(W, 205, 130, 113, "ic", opacity=.45, cls="sway2")
               + aurora(W, 280, 150, 117, "te", opacity=.6, cls="sway2"))
    body = [ground(W, H), stars(W, 0, horizon - 40, 170, 109, .35), meteor(700, 60, 3), f'<g id="skyart">{sky_art}</g>']
    body.append(f'<use href="#skyart" transform="translate(0 {2 * horizon}) scale(1 -1)" opacity=".28" filter="url(#mist)"/>')
    body.append(mountains(W, horizon + 1, 0, 300, 345, 121, "#071321", uid="f"))
    body.append(f'<rect x="0" y="{horizon}" width="{W}" height="{H - horizon}" fill="{NIGHT0}" opacity=".55"/>')
    rnd = random.Random(127)
    for _ in range(26):
        y = rnd.uniform(horizon + 8, H - 10)
        x = rnd.uniform(0, W - 200)
        body.append(f'<line x1="{x:.0f}" y1="{y:.0f}" x2="{x + rnd.uniform(60, 220):.0f}" y2="{y:.0f}" stroke="{ICE}" stroke-opacity="{rnd.uniform(.05, .18):.2f}"/>')
    fx, fy0, fy1 = 800, 300, 96
    sparks = "".join(
        f'<line x1="{fx}" y1="{fy1}" x2="{fx + 46 * math.cos(a):.1f}" y2="{fy1 + 46 * math.sin(a):.1f}" stroke="{AMBER}" stroke-width="1.6" stroke-linecap="round"/>'
        for a in [i * math.pi / 7 for i in range(14)])
    body.append(
        '<style>.fl{animation:fl 6s ease-out infinite}@keyframes fl{0%{stroke-dashoffset:1;opacity:1}30%{stroke-dashoffset:0;opacity:1}55%,100%{stroke-dashoffset:0;opacity:0}}'
        '.bu{transform-box:fill-box;transform-origin:center;animation:bu 6s ease-out infinite}'
        '@keyframes bu{0%,28%{opacity:0;transform:scale(.2)}34%{opacity:1}70%,100%{opacity:0;transform:scale(1.6)}}'
        '@media (prefers-reduced-motion: reduce){.fl{stroke-dasharray:none;opacity:1}.bu{opacity:1}}</style>'
        f'<line class="fl" x1="{fx}" y1="{fy0}" x2="{fx}" y2="{fy1}" pathLength="1" stroke-dasharray="1" stroke="url(#warm)" stroke-width="2.4" stroke-linecap="round" filter="url(#glow)"/>'
        f'<g class="bu" filter="url(#glow)"><circle cx="{fx}" cy="{fy1}" r="10" fill="{AMBER}"/>{sparks}</g>'
        f'<circle cx="{fx}" cy="{fy0}" r="3" fill="{AMBER}" class="br"/>')
    for (bx, by, c, d0) in [(640, 120, EMERALD, 2.0), (900, 150, ICE, 3.4), (720, 70, ROSE, 4.6)]:
        sp = "".join(f'<line x1="{bx}" y1="{by}" x2="{bx + 34 * math.cos(a):.1f}" y2="{by + 34 * math.sin(a):.1f}" stroke="{c}" stroke-width="1.4" stroke-linecap="round"/>'
                     f'<circle cx="{bx + 40 * math.cos(a):.1f}" cy="{by + 40 * math.sin(a):.1f}" r="1.6" fill="{c}"/>'
                     for a in [j * math.pi / 8 for j in range(16)])
        body.append(f'<g class="bu" style="animation-delay:{d0}s" filter="url(#glow)">{sp}</g>')
    for j in range(3):
        body.append(f'<ellipse cx="{fx}" cy="{horizon + 14}" rx="10" ry="2.5" fill="none" stroke="{AMBER}" stroke-opacity=".6">'
                    f'<animate attributeName="rx" values="10;120" dur="6s" begin="{j * 2}s" repeatCount="indefinite"/>'
                    f'<animate attributeName="ry" values="2.5;14" dur="6s" begin="{j * 2}s" repeatCount="indefinite"/>'
                    f'<animate attributeName="opacity" values=".8;0" dur="6s" begin="{j * 2}s" repeatCount="indefinite"/></ellipse>')
    # keep the headline readable over the brightest part of the sky
    body.append(f'<radialGradient id="scrim" cx=".3" cy=".42" r=".55"><stop offset="0" stop-color="{NIGHT0}" stop-opacity=".78"/>'
                f'<stop offset=".7" stop-color="{NIGHT0}" stop-opacity=".35"/><stop offset="1" stop-color="{NIGHT0}" stop-opacity="0"/></radialGradient>'
                f'<ellipse cx="300" cy="175" rx="420" ry="150" fill="url(#scrim)"/>')
    body.append(f'<g class="up" style="animation-delay:.2s">{t(64, 100, "SEND A SIGNAL", 13, AMBER, MONO, 600, "start", 6)}</g>')
    body.append(f'<g class="up" style="animation-delay:.4s" filter="url(#glow)">{t(60, 160, "Let’s build something", 50, TEXT, SANS, 800, "start", -1)}'
                f'{t(60, 216, "worth finding.", 50, "url(#title)", SANS, 800, "start", -1)}</g>')
    body.append(f'<g class="up" style="animation-delay:.7s">{t(64, 254, "AI engineering internships  ·  agent systems  ·  hackathon teams", 16, MUTED)}</g>')
    body.append(t(64, H - 24, "END OF TRANSMISSION · REDRAWN EVERY SIX HOURS FROM LIVE DATA", 10, FAINT, MONO, 400, "start", 2))
    body.append(frame(W, H))
    return svg(W, H, "Send a signal: let's build something worth finding. AI engineering internships, agent systems, hackathon teams.", "", "".join(body))


def channel(label: str, sub: str, icon: str, color: str) -> str:
    W, H = 320, 72
    icons = {
        "linkedin": f'<rect x="20" y="22" width="28" height="28" rx="6" fill="none" stroke="{color}" stroke-width="1.8"/>'
                    + t(34, 42, "in", 15, color, SANS, 800, "middle"),
        "mail": f'<rect x="19" y="24" width="30" height="22" rx="3" fill="none" stroke="{color}" stroke-width="1.8"/>'
                f'<polyline points="19,26 34,38 49,26" fill="none" stroke="{color}" stroke-width="1.8"/>',
        "git": f'<circle cx="26" cy="26" r="4" fill="none" stroke="{color}" stroke-width="1.8"/><circle cx="26" cy="47" r="4" fill="none" stroke="{color}" stroke-width="1.8"/>'
               f'<circle cx="43" cy="31" r="4" fill="none" stroke="{color}" stroke-width="1.8"/>'
               f'<path d="M26 30 V43 M43 35 Q43 41 30 45" fill="none" stroke="{color}" stroke-width="1.8"/>',
    }
    body = (f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="36" fill="#06121c" stroke="{color}" stroke-opacity=".55"/>'
            f'<rect class="br" x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="36" fill="{color}" opacity=".06"/>'
            + icons[icon] + t(66, 33, label, 16, TEXT, SANS, 700) + t(66, 52, sub, 11, MUTED, MONO)
            + f'<polyline points="{W - 40},28 {W - 30},36 {W - 40},44" fill="none" stroke="{color}" stroke-width="2"/>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{escape(label)}"><style>{CSS}</style>{body}</svg>'


# ------------------------------------------------------------------------------------------------ 9. ascent (the journey)

def ascent(journey: list[dict], repos: dict, names: dict, cats: dict) -> str:
    W, H = 1000, 560
    stops = [j for j in journey if j["repo"] in repos]
    n = len(stops)
    body = [ground(W, H), stars(W, 0, 470, 210, 131, .4), aurora(W, 150, 120, 137, "ic", opacity=.35, cls="sway2"),
            mountains(W, H, 0, 486, 530, 139, "#040c17", snow=False)]
    first, last = (repos[stops[0]["repo"]]["created"], repos[stops[-1]["repo"]]["created"]) if stops else ("", "")
    months = 0
    if stops:
        a, b = date.fromisoformat(first), date.fromisoformat(last)
        months = (b.year - a.year) * 12 + b.month - a.month
    body.append(t(52, 48, f"ASCENT // {months} MONTHS · {n} REPOS", 12, ICE, MONO, 500, "start", 3))
    body.append(t(52, 92, "From a static page to systems", 30, TEXT, SANS, 700))
    body.append(t(52, 128, "that check themselves.", 30, "url(#title)", SANS, 800))
    if not n:
        return svg(W, H, "Ascent", "", "".join(body) + frame(W, H))
    x0, x1, ylo, yhi = 78, W - 70, 448, 182
    pts = [(x0 + (x1 - x0) * i / max(n - 1, 1), ylo - (ylo - yhi) * (i / max(n - 1, 1)) ** .85) for i in range(n)]
    d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    body.append(f'<path d="{d}" fill="none" stroke="{ICE}" stroke-opacity=".18" stroke-width="6" filter="url(#soft)"/>')
    body.append(f'<path class="draw" pathLength="1" d="{d}" fill="none" stroke="url(#title)" stroke-width="1.6" style="animation-duration:4s"/>')
    climb = 10.0  # seconds per climb; the light rests at the top for the last fifth
    seg = [math.dist(pts[i], pts[i + 1]) for i in range(n - 1)]
    total = sum(seg) or 1
    reach = [0.0]
    for L in seg:
        reach.append(reach[-1] + L / total)
    times = [.8 * i / max(n - 1, 1) for i in range(n)]
    maxkb = max(repos[s["repo"]]["kb"] for s in stops) or 1
    for i, (s, (x, y)) in enumerate(zip(stops, pts)):
        r = repos[s["repo"]]
        c = CAT[cats.get(s["repo"], "other")]
        size = 3 + 6 * math.log1p(r["kb"]) / math.log1p(maxkb)
        delay = .3 + i * 3.6 / n
        above = i % 2 == 0
        lift = 34 if (i // 2) % 2 else 0
        ny = y - 30 - lift if above else y + 30 + lift
        when = date.fromisoformat(r["created"]).strftime("%b '%y").upper()
        body.append(f'<g class="fade" style="animation-delay:{delay:.2f}s">'
                    f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{size * 2.6:.1f}" fill="{c}" opacity=".18" filter="url(#soft)"/>'
                    f'<circle class="tw" style="animation-delay:{i * .4:.1f}s" cx="{x:.1f}" cy="{y:.1f}" r="{size:.1f}" fill="#f2fffb"/>'
                    f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{size + 3:.1f}" fill="none" stroke="{c}" stroke-opacity=".7"/>')
        if lift:
            y2 = ny + 6 if above else ny - 16
            body.append(f'<line x1="{x:.1f}" y1="{y - size - 4 if above else y + size + 4:.1f}" x2="{x:.1f}" y2="{y2:.1f}" stroke="{c}" stroke-opacity=".35"/>')
        name_y, note_y = (ny - 14, ny) if above else (ny, ny + 14)
        x = min(max(x, 70), W - 76)
        body.append(t(x, name_y - 13, when, 8.5, c, MONO, 600, "middle", 1.2) if above else "")
        body.append(t(x, name_y, names.get(s["repo"], s["label"]), 12.5, TEXT, SANS, 700, "middle"))
        body.append(t(x, note_y, s["note"], 9.5, MUTED, MONO, 400, "middle"))
        body.append(t(x, note_y + 13, when, 8.5, c, MONO, 600, "middle", 1.2) if not above else "")
        body.append("</g>")
    if n > 1:
        for i, (x, y) in enumerate(pts):
            c = CAT[cats.get(stops[i]["repo"], "other")]
            body.append(f'<circle class="ping" style="--d:{climb}s;animation-delay:{times[i] * climb:.2f}s" cx="{x:.1f}" cy="{y:.1f}" r="9" '
                        f'fill="none" stroke="{c}" stroke-width="1.6"/>')
        kt = ";".join(f"{v:.4f}" for v in times + [1])
        kp = ";".join(f"{v:.4f}" for v in reach + [1])
        body.append(f'<g class="fx-move"><circle r="11" fill="{ICE}" opacity=".22"/><circle r="4.2" fill="#ffffff"/>'
                    f'<animateMotion dur="{climb}s" repeatCount="indefinite" path="{d}" calcMode="linear" keyTimes="0;{kt[kt.index(";") + 1:]}" keyPoints="0;{kp[kp.index(";") + 1:]}"/>'
                    f'<animate attributeName="opacity" dur="{climb}s" repeatCount="indefinite" values="0;1;1;0;0" keyTimes="0;.03;.8;.9;1"/></g>')
    body.append(drifting_mist(W, H - 64, 110, ICE, .08))
    body.append(t(52, H - 24, "ONE STAR = ONE REPO, IN THE ORDER IT BEGAN · BRIGHTNESS = SIZE OF THE CODE", 10, FAINT, MONO, 400, "start", 1.5))
    body.append(frame(W, H))
    return svg(W, H, f"Ascent: {n} repositories over {months} months, from a static portfolio to " + ", ".join(s["label"] for s in stops[-4:]),
               "", "".join(body))


# ------------------------------------------------------------------------------------------------ 10. instruments

def gauge(cx, cy, value, label, color, delay):
    r = 50
    return (f'<g class="up" style="animation-delay:{delay:.2f}s">'
            f'<circle cx="{cx}" cy="{cy}" r="{r + 14}" fill="{color}" opacity=".07" filter="url(#soft)"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#06121c" stroke="{color}" stroke-opacity=".18" stroke-width="7"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{color}" stroke-width="7" stroke-linecap="round" pathLength="100" '
            f'stroke-dasharray="22 78" filter="url(#glow)"><animateTransform attributeName="transform" type="rotate" '
            f'from="0 {cx} {cy}" to="360 {cx} {cy}" dur="{6 + delay * 4:.1f}s" repeatCount="indefinite"/></circle>'
            + __import__("aurora_fx").countup(cx, cy + 9, value, 26 if len(value) < 4 else 21, TEXT, delay=delay + .3, anchor="middle")
            + t(cx, cy + r + 30, label, 9.5, MUTED, MONO, 600, "middle", 1.6) + "</g>")


def instruments(signals: dict, live: dict, prs: int, crew: list[dict], names: dict, fetched: str) -> str:
    W = 1000
    tests = sum(s["tests"] for s in signals.values())
    tfiles = sum(s["test_files"] for s in signals.values())
    ci = sum(s["ci"] for s in signals.values())
    docker = sum(1 for s in signals.values() if s["docker"])
    docs = sum(s["docs"] + s["adrs"] for s in signals.values())
    live_n = sum(1 for v in live.values() if v)
    board = sorted(((n, s) for n, s in signals.items()
                    if s["tests"] or s["ci"] or s["docker"] or s["adrs"] or s["license"] or live.get(n)),
                   key=lambda kv: (-kv[1]["tests"], kv[0]))
    rows = (len(board) + 1) // 2
    H = 330 + rows * 44 + 120
    body = [ground(W, H), stars(W, 0, 140, 70, 151, .3), aurora(W, 130, 110, 157, "te", opacity=.3, cls="sway2")]
    body.append(t(52, 48, "INSTRUMENTS // ENGINEERING ACROSS EVERY REPO", 12, ICE, MONO, 500, "start", 3))
    body.append(synced(W, 48, fetched))
    head = f"{tests:,} test cases. {ci} CI workflows." + (f" {live_n} live apps." if live_n else "")
    body.append(t(52, 92, head, 28, TEXT, SANS, 700))
    gauges = [(f"{tests:,}", "TEST CASES", EMERALD), (str(tfiles), "TEST FILES", TEAL), (str(ci), "CI WORKFLOWS", ICE),
              (str(docker), "DOCKERISED REPOS", STEEL), (str(docs), "DESIGN DOCS & ADRS", AMBER), (str(prs), "PULL REQUESTS", ROSE)]
    gx = (W - 104) / len(gauges)
    for i, (v, l, c) in enumerate(gauges):
        body.append(gauge(52 + gx * (i + .5), 182, v, l, c, .1 + i * .12))
    y = 300
    body.append(t(52, y - 8, "SIGNAL BOARD", 10.5, MUTED, MONO, 500, "start", 3))
    colw = (W - 104 - 20) / 2
    for k, (name, s) in enumerate(board):
        x = 52 + (k % 2) * (colw + 20)
        yy = y + (k // 2) * 44
        chips = []
        if s["tests"]:
            chips.append((f"{s['tests']} TESTS", EMERALD))
        if s["ci"]:
            chips.append(("CI", TEAL))
        if s["docker"]:
            chips.append(("DOCKER", ICE))
        if s["adrs"]:
            chips.append((f"{s['adrs']} ADRS", AMBER))
        elif s["docs"] >= 3:
            chips.append((f"{s['docs']} DOCS", AMBER))
        if s["license"]:
            chips.append(("LICENSED", STEEL))
        if live.get(name):
            chips.append(("● LIVE", EMERALD))
        g = [f'<g class="slide" style="animation-delay:{.5 + k * .06:.2f}s">', glass(x, yy, colw, 36, 10, None, .55),
             t(x + 14, yy + 23, names.get(name, name), 14, TEXT, SANS, 700)]
        cx = x + 132
        for label, c in chips:
            w = len(label) * 6.6 + 16
            if cx + w > x + colw - 8:
                break
            g.append(f'<rect x="{cx:.1f}" y="{yy + 9}" width="{w:.1f}" height="18" rx="9" fill="{c}" fill-opacity=".1" stroke="{c}" stroke-opacity=".55"/>'
                     + t(cx + w / 2, yy + 22, label, 9.5, c, MONO, 600, "middle", .8))
            cx += w + 6
        g.append("</g>")
        body.append("".join(g))
    if rows:
        body.append(f'<linearGradient id="sweep" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{TEAL}" stop-opacity="0"/>'
                    f'<stop offset=".5" stop-color="{TEAL}" stop-opacity=".16"/><stop offset="1" stop-color="{TEAL}" stop-opacity="0"/></linearGradient>'
                    f'<g class="scan" style="--dy:{(rows - 1) * 44}px;--d:{2.2 + rows * .8:.1f}s"><rect x="52" y="{y}" width="{W - 104}" height="36" rx="10" fill="url(#sweep)"/>'
                    f'<rect x="52" y="{y + 35}" width="{W - 104}" height="1.2" fill="{TEAL}" opacity=".55"/></g>')
    cy = y + rows * 44 + 34
    body.append(t(52, cy, "ROPE TEAM // BUILT WITH", 10.5, MUTED, MONO, 500, "start", 3))
    x = 52
    for m in crew:
        label = f'{m["name"]}  ·  ' + (f'{len(m["repos"])} repos' if len(m["repos"]) > 1 else names.get(m["repos"][0], m["repos"][0]))
        initials = "".join(w[0] for w in m["name"].split()[:2]).upper()
        w = len(label) * 7.4 + 58
        body.append(f'<g class="up" style="animation-delay:1.2s">{glass(x, cy + 14, w, 40, 20, None, .7)}'
                    f'<circle cx="{x + 21}" cy="{cy + 34}" r="13" fill="{TEAL}" fill-opacity=".15" stroke="{TEAL}"/>'
                    f'<circle class="spin" cx="{x + 21}" cy="{cy + 34}" r="17" fill="none" stroke="{TEAL}" stroke-opacity=".6" stroke-dasharray="10 7 2 7"/>'
                    + t(x + 21, cy + 38, initials, 10, TEAL, MONO, 700, "middle") + t(x + 42, cy + 39, label, 12.5, TEXT, SANS, 600) + "</g>")
        x += w + 12
    body.append(t(W - 52, H - 20, "COUNTED FROM EVERY PUBLIC REPO ON EACH REFRESH", 10, FAINT, MONO, 400, "end", 1.5))
    body.append(frame(W, H))
    return svg(W, H, f"Instruments: {tests} test cases in {tfiles} test files, {ci} CI workflows, {docker} dockerised repos, "
                     f"{docs} design documents, {prs} pull requests across every public repository.", "", "".join(body))
