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
    "@keyframes rise{from{transform:scaleY(0)}to{transform:scaleY(1)}}"
    ".up{animation:up .9s ease-out both}@keyframes up{from{opacity:0;transform:translateY(12px)}to{opacity:1;transform:none}}"
    ".fade{animation:fade 1s ease-out both}@keyframes fade{from{opacity:0}to{opacity:1}}"
    ".slide{animation:slide 1s cubic-bezier(.2,.8,.2,1) both}@keyframes slide{from{opacity:0;transform:translateX(-40px)}to{opacity:1;transform:none}}"
    ".draw{stroke-dasharray:1;stroke-dashoffset:1;animation:draw 2.4s ease-out both}@keyframes draw{to{stroke-dashoffset:0}}"
    ".blink{animation:blink 1.6s steps(2,start) infinite}@keyframes blink{to{opacity:.2}}"
    ".meteor{animation:meteor 9s linear infinite}"
    "@keyframes meteor{0%,82%{opacity:0;transform:translate(0,0)}84%{opacity:1}96%{opacity:0;transform:translate(-260px,120px)}100%{opacity:0}}"
    "@media (prefers-reduced-motion: reduce){*{animation:none!important}.draw{stroke-dasharray:none}}"
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
    + "".join(
        f'<linearGradient id="ray-{k}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{c}" stop-opacity="0"/>'
        f'<stop offset=".45" stop-color="{c}" stop-opacity=".16"/><stop offset=".82" stop-color="{c}" stop-opacity=".6"/>'
        f'<stop offset=".97" stop-color="{c}" stop-opacity="1"/><stop offset="1" stop-color="{c}" stop-opacity=".15"/></linearGradient>'
        for k, c in (("em", EMERALD), ("te", TEAL), ("ic", ICE), ("am", AMBER))
    )
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
    rnd, out = random.Random(seed), []
    for i in range(n):
        x, y = rnd.uniform(8, W - 8), top + (bottom - top) * rnd.random() ** 1.6  # denser near the top
        r = rnd.choice([.5, .6, .7, .8, 1, 1.2, 1.5])
        op = rnd.uniform(.25, .9)
        cls = f' class="tw" style="animation-delay:{rnd.uniform(0, 3.4):.2f}s"' if rnd.random() < twinkle else ""
        out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="#dff9ff" opacity="{op:.2f}"{cls}/>')
    return "".join(out)


def meteor(x, y, delay=0):
    return (f'<g class="meteor" style="animation-delay:{delay}s"><line x1="{x}" y1="{y}" x2="{x + 70}" y2="{y - 32}" '
            f'stroke="url(#title)" stroke-width="1.4" stroke-linecap="round" opacity=".9"/>'
            f'<circle cx="{x}" cy="{y}" r="1.8" fill="#fff"/></g>')


def aurora(W, low, height, seed, color="em", step=6, opacity=1.0, cls="sway", amp=26, x0=-80, x1=None):
    """One aurora curtain: hundreds of thin rays hanging from a wavy top to a bright, wavy lower edge."""
    x1 = W + 80 if x1 is None else x1
    rnd = random.Random(seed)
    p = [rnd.uniform(0, 6.28) for _ in range(5)]
    f = [rnd.uniform(.004, .007), rnd.uniform(.011, .019), rnd.uniform(.002, .004)]
    groups = [[] for _ in range(5)]
    edge = []
    x = x0
    while x <= x1:
        lo = low + amp * math.sin(x * f[0] + p[0]) + amp * .45 * math.sin(x * f[1] + p[1])
        hi = lo - height * (.55 + .45 * (.5 + .5 * math.sin(x * f[2] + p[2])))
        groups[rnd.randrange(5)].append(
            f'<rect x="{x:.1f}" y="{hi:.1f}" width="{step + 1.2:.1f}" height="{lo - hi:.1f}" fill="url(#ray-{color})" opacity="{rnd.uniform(.35, 1):.2f}"/>')
        edge.append(f"{x:.1f},{lo:.1f}")
        x += step
    uid = f"au{seed}"
    rays = f'<g id="{uid}">' + "".join(f'<g class="sh" style="animation-delay:{i * .55:.2f}s">{"".join(g)}</g>' for i, g in enumerate(groups)) + "</g>"
    c = {"em": EMERALD, "te": TEAL, "ic": ICE, "am": AMBER}[color]
    line = f'<polyline points="{" ".join(edge)}" fill="none" stroke="{c}" stroke-width="2" opacity=".55" filter="url(#mist)"/>'
    return (f'<g class="{cls}" opacity="{opacity}"><use href="#{uid}" filter="url(#soft)" opacity=".75"/>'
            f'<g filter="url(#mist)">{rays}</g>{line}</g>')


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
        grad = (f'<linearGradient id="snow-{uid}" gradientUnits="userSpaceOnUse" x1="0" y1="{peak:.0f}" x2="0" y2="{peak + 46:.0f}">'
                f'<stop offset="0" stop-color="#e6fbff" stop-opacity=".9"/><stop offset=".35" stop-color="#9cc6d8" stop-opacity=".55"/>'
                f'<stop offset="1" stop-color="{fill}"/></linearGradient>')
        return grad + f'<path d="{d}" fill="url(#snow-{uid})"/>'
    return f'<path d="{d}" fill="{fill}"/>'


def glass(x, y, w, h, rx=14, accent=None, op=.5):
    out = (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="#0b1b28" fill-opacity="{op}" '
           f'stroke="{ICE}" stroke-opacity=".14"/>')
    if accent:
        out += f'<rect x="{x + rx}" y="{y}" width="{w - 2 * rx}" height="1.6" fill="{accent}" opacity=".8"/>'
    return out


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
    body = [ground(W, H), stars(W, 150, 470, 120, 5, .3)]
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
                    f'{t(x + 16, 141, sub, 10.5, color, MONO)}</g>')
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
        rays[i % 4].append(r + core)
        rays_glow[i % 4].append(r)
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
    for i, (label, color) in enumerate([("IIT MADRAS · CGPA 9.0", EMERALD), ("SCALER SOT", ICE), ("PARADOX DSA · RUNNER-UP", AMBER)]):
        p, w = pill(x, H - 62, label, color, 10.5, 12, 26)
        body.append(f'<g class="up" style="animation-delay:{1.1 + i * .15:.2f}s">{p}</g>')
        x += w + 10
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


def expeditions(flagships: list[dict], systems: list[dict], metrics: dict, cats: dict, n_links: int) -> str:
    W, H = 1000, 760
    body = [ground(W, H), stars(W, 0, 140, 70, 41, .25), aurora(W, 120, 110, 47, "te", opacity=.3, cls="sway2")]
    body.append(t(52, 52, "EXPEDITIONS // FLAGSHIP SYSTEMS", 12, ICE, MONO, 500, "start", 3))
    body.append(t(52, 92, "Where the model meets a rule.", 30, TEXT, SANS, 700))
    body.append(t(52, 118, "Three flagships and five more climbs, each with a number read live from its own repository.", 14, MUTED))
    for i, (v, l, c) in enumerate([("3", "FLAGSHIPS", EMERALD), (str(len(flagships) + len(systems)), "SYSTEMS", ICE), (str(n_links), "CODE LINKS", AMBER)]):
        x = W - 52 - (2 - i) * 104
        body.append(t(x, 92, v, 32, c, SANS, 700, "end") + t(x, 112, l, 9.5, MUTED, MONO, 500, "end", 2))
    cw, ch, gap, y0 = 290, 400, 23, 146
    for i, f in enumerate(flagships):
        x = 52 + i * (cw + gap)
        color = CAT.get(cats.get(f["repo"], "other"))
        g = [f'<g class="up" style="animation-delay:{.2 + i * .18:.2f}s">',
             f'<rect x="{x}" y="{y0}" width="{cw}" height="{ch}" rx="18" fill="{color}" opacity=".06" filter="url(#soft)"/>',
             glass(x, y0, cw, ch, 18, color, .7),
             f'<circle cx="{x + 42}" cy="{y0 + 48}" r="24" fill="{color}" opacity=".12"/>',
             f'<circle cx="{x + 42}" cy="{y0 + 48}" r="24" fill="none" stroke="{color}" stroke-opacity=".6"/>',
             glyph(f["glyph"], x + 42, y0 + 48, 26, color),
             t(x + 78, y0 + 46, f["name"], 23, TEXT, SANS, 700), t(x + 78, y0 + 65, f["tag"], 9.5, color, MONO, 500, "start", 1.5)]
        for j, line in enumerate(wrap(f["pitch"], 38)[:3]):
            g.append(t(x + 22, y0 + 108 + j * 20, line, 14, MUTED))
        value = metrics.get(f["repo"], "·")
        g.append(t(x + 22, y0 + 218, value, 48, "url(#title)", SANS, 800, "start", -1, 'filter="url(#glow)"'))
        for j, line in enumerate(wrap(f["metric"]["label"], 36)[:2]):
            g.append(t(x + 22, y0 + 242 + j * 16, line.upper(), 10, MUTED, MONO, 500, "start", 1.2))
        g.append(f'<line x1="{x + 22}" y1="{y0 + 278}" x2="{x + cw - 22}" y2="{y0 + 278}" stroke="{ICE}" stroke-opacity=".1"/>')
        g.append(flow(x + 34, x + cw - 34, y0 + 312, f["flow"], color, f"fl{i}"))
        g.append(t(x + 22, y0 + ch - 20, f["stack"], 10.5, FAINT, MONO))
        g.append("</g>")
        body.append("".join(g))
    sw, sgap, sy = (W - 104 - 4 * 14) / 5, 14, y0 + ch + 30
    body.append(t(52, sy - 8, "ALSO CLIMBED", 10.5, MUTED, MONO, 500, "start", 3))
    for i, s in enumerate(systems):
        x = 52 + i * (sw + sgap)
        color = CAT.get(cats.get(s["repo"], "other"))
        value = metrics.get(s["repo"], "·")
        size = 26 if len(value) <= 6 else 19
        body.append(f'<g class="up" style="animation-delay:{.8 + i * .1:.2f}s">{glass(x, sy + 6, sw, 140, 14, color, .65)}'
                    f'{glyph(s["glyph"], x + 26, sy + 34, 20, color)}{t(x + 46, sy + 39, s["name"], 15, TEXT, SANS, 700)}'
                    f'{t(x + 16, sy + 64, s["tag"], 8.5, color, MONO, 500, "start", 1.2)}'
                    f'{t(x + 16, sy + 102, value, size, TEXT, SANS, 800)}'
                    + "".join(t(x + 16, sy + 122 + j * 13, line.upper(), 8.8, MUTED, MONO, 500, "start", .8)
                              for j, line in enumerate(wrap(s["metric"]["label"], 27)[:2])) + "</g>")
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
    for k, (_, _, r, x, top) in enumerate(flagged):
        pole = min(26 + (k % 3) * 26, top - 92)
        cat = CAT[cats.get(r["name"], "other")]
        name = {"codecrafters-shell-cpp": "C++ Shell", "Meta_OpenEnv": "Meta OpenEnv", "Shopkart": "ShopKart"}.get(r["name"], r["name"])
        lw = len(name) * 7.4 + 18
        body.append(f'<g class="fade" style="animation-delay:{1.6 + k * .12:.2f}s">'
                    f'<line x1="{x:.1f}" y1="{top:.1f}" x2="{x:.1f}" y2="{top - pole:.1f}" stroke="{TEXT}" stroke-opacity=".7"/>'
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
                    f'<polyline points="{" ".join(f"{x:.1f},{py:.1f}" for x, py in prev)}" fill="none" stroke="{c}" stroke-opacity=".65" stroke-width="1.4"/>')
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
    body.append(f'<circle r="4.5" fill="{AMBER}" filter="url(#glow)"><animateMotion dur="11s" repeatCount="indefinite"><mpath href="#trail"/></animateMotion></circle>')
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
