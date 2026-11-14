"""Atlas scenes below the hero: repository cards, build kit, GitHub signal, route and contact."""
from datetime import date
import random
import zlib

from atlas_hero import HERO_CSS, _map
from atlas_kit import (AMBER, BG, BG2, BG3, CYAN, GREEN, INK, INK2, INK3, LINE, LINE2, NARROW, VIOLET, VOLT, WIDE,
                       clip_text, comet, contour_paths, dot, esc, flow_chips, label, mono_w, rrect, sans_w, svg, t, wrap)

ACCENTS = [VOLT, CYAN, AMBER, VIOLET]
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

CSS = f"""
.ping{{transform-box:fill-box;transform-origin:center;animation:ping 3.2s ease-out infinite}}
@keyframes ping{{0%{{transform:scale(.5);opacity:.9}}70%,100%{{transform:scale(3.2);opacity:0}}}}
.nudge{{animation:nudge 1.6s ease-in-out infinite}}
@keyframes nudge{{50%{{transform:translateX(5px)}}}}
.bw{{opacity:.5;animation:bw 7s linear infinite}}
@keyframes bw{{0%,100%{{opacity:.5}}3%{{opacity:1}}16%{{opacity:.5}}}}
.head{{animation:head 7s linear infinite}}
@keyframes head{{0%{{transform:translateX(0);opacity:0}}2%{{opacity:.9}}57%{{transform:translateX(var(--run));opacity:.9}}60%,100%{{transform:translateX(var(--run));opacity:0}}}}
.kt{{opacity:.3;animation:kt 9s linear infinite}}
@keyframes kt{{0%,100%{{opacity:.3}}6%{{opacity:1}}22%{{opacity:.3}}}}
.stop{{opacity:.7;animation:stop 8s linear infinite}}
@keyframes stop{{0%,100%{{opacity:.7}}4%{{opacity:1}}30%{{opacity:.7}}}}
.walk{{animation:walk 8s linear infinite}}
@keyframes walk{{0%{{transform:translateY(0);opacity:0}}3%{{opacity:1}}82%{{transform:translateY(var(--run));opacity:1}}88%,100%{{transform:translateY(var(--run));opacity:0}}}}
"""


def _arrow(x, y, color):
    return (f'<path class="nudge" d="M{x:g} {y:g}h20m-6-5 6 5-6 5" fill="none" stroke="{color}" stroke-width="1.8" '
            f'stroke-linecap="round" stroke-linejoin="round"/>')


# ---------------------------------------------------------------- repository cards
def _corner_terrain(name, x, y, w, h, color):
    """A small contour patch unique to each repository name, with a marker on its summit."""
    seed = zlib.crc32(name.encode("utf-8"))
    rng = random.Random(seed)
    hills = [(rng.uniform(0.45, 0.72) * w, rng.uniform(0.42, 0.58) * h, rng.uniform(0.28, 0.4) * w, rng.uniform(0.32, 0.48) * h, 1.0),
             (rng.uniform(0.1, 0.9) * w, rng.uniform(0.1, 0.9) * h, rng.uniform(0.18, 0.3) * w, rng.uniform(0.22, 0.4) * h, 0.6)]
    out = [f'<g transform="translate({x:g} {y:g})">']
    for k, (_, data) in enumerate(contour_paths(w, h, seed, hills, [0.22, 0.42, 0.62, 0.82])):
        out.append(f'<path d="{data}" fill="none" stroke="{color}" stroke-width="1" opacity="{0.16 + 0.07 * k:.2f}"/>')
    px, py = round(hills[0][0]), round(hills[0][1])
    out.append(f'<circle class="ping fx" cx="{px}" cy="{py}" r="5" fill="none" stroke="{color}" stroke-width="1.4"/>')
    out.append(f'<path d="M{px} {py - 5}L{px + 5} {py}L{px} {py + 5}L{px - 5} {py}Z" fill="{BG}" stroke="{color}" stroke-width="1.4"/>')
    out.append("</g>")
    return "".join(out)


def _fade(x, w, h, ident="r-fade"):
    defs = (f'<linearGradient id="{ident}" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{BG}"/>'
            f'<stop offset="1" stop-color="{BG}" stop-opacity="0"/></linearGradient>'
            f'<linearGradient id="{ident}-v" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{BG}" stop-opacity="0"/>'
            f'<stop offset="1" stop-color="{BG}"/></linearGradient>')
    return defs, (f'<rect x="{x:g}" y="0" width="{w:g}" height="{h:g}" fill="url(#{ident})"/>'
                  f'<rect x="{x:g}" y="{h * 0.62:g}" width="600" height="{h * 0.38 + 1:g}" fill="url(#{ident}-v)"/>')


def repo_card(row, index) -> str:
    """Desktop card for one repository: 440 wide, shown two to a row."""
    color = ACCENTS[index % len(ACCENTS)]
    w, h = 440, 228
    defs, fade = _fade(236, 90, 130)
    body = [_corner_terrain(row["repo"], 236, 0, 204, 130, color), fade]
    body.append(dot(27, 32, 3.5, color) + label(38, 36, f'{index + 1:02d} / {clip_text(row["category"], 34)}', color, 11.5))
    body.append(t(22, 80, wrap(row["title"], 330, 27, 800, 1)[0], 27, INK, 800, ls=-0.6))
    for k, line in enumerate(wrap(row["description"], 392, 14.5, max_lines=3)):
        body.append(t(24, 108 + k * 21, line, 14.5, INK2))
    chips, _ = flow_chips(24, 170, row["stack"], 392, INK2, 11, 23, 6, 1)
    body.append(chips)
    body.append(label(24, 215, "OPEN REPOSITORY", color, 10.5) + _arrow(150, 211, color))
    body.append(comet(0.75, 0.75, w - 1.5, h - 1.5, 17, color, 11, (index * 1.7) % 11))
    return svg(w, h, f'{row["title"]} — {row["description"]}', "Stack: " + ", ".join(row["stack"]), "".join(body), CSS, defs, glow=color)


def repo_mini(row, index) -> str:
    """Phone card for one repository: 220 wide, still shown two to a row."""
    color = ACCENTS[index % len(ACCENTS)]
    w, h = 220, 170
    defs, fade = _fade(96, 60, 84)
    body = [_corner_terrain(row["repo"], 96, 0, 124, 84, color), fade]
    body.append(label(16, 30, f"{index + 1:02d}", color, 12))
    for k, line in enumerate(wrap(row["title"], 186, 20, 800, 2)):
        body.append(t(15, 68 + k * 25, line, 20, INK, 800, ls=-0.4))
    chips, _ = flow_chips(16, 124, row["stack"], 150, INK2, 10.5, 22, 5, 1)
    body.append(chips)
    body.append(_arrow(182, 154, color))
    return svg(w, h, row["title"], row["description"], "".join(body), CSS, defs, radius=14, glow=color)


def browse_card(mini=False) -> str:
    row = {"repo": "all-repositories", "title": "All repositories", "category": "NEXT DROP",
           "description": "New ideas land here first. Browse everything on GitHub.", "stack": ["github.com/Aditya2514"]}
    return repo_mini(row, 1) if mini else repo_card(row, 1)


# ---------------------------------------------------------------- build kit
def kit(groups, mobile=False) -> str:
    w = NARROW if mobile else WIDE
    cols = 1 if mobile else 3
    pad, gap = (18, 10) if mobile else (24, 12)
    tw = (w - 2 * pad - (cols - 1) * gap) / cols
    tools = sum(len(g["tools"]) for g in groups)
    body = [dot(pad + 3, 34, 3.5, VOLT), label(pad + 14, 38, "BUILD KIT / TOOLS BY PURPOSE", VOLT, 12),
            label(w - pad, 38, f"{tools} TOOLS", INK3, 11, "end")]
    y = 58
    for start in range(0, len(groups), cols):
        row = groups[start:start + cols]
        drawn, row_h = [], 0
        for k, group in enumerate(row):
            x = pad + k * (tw + gap)
            chips, bottom = flow_chips(x + 16, y + 62, group["tools"], tw - 32, INK, 11.5, 24, 6, 4)
            row_h = max(row_h, bottom - y + 16)
            drawn.append((x, group, chips, start + k))
        for x, group, chips, n in drawn:
            color = ACCENTS[n % len(ACCENTS)]
            body.append(rrect(x, y, tw, row_h, 12, BG2, LINE))
            body.append(f'<path class="kt" d="M{x + 16:g} {y}h{tw - 32:g}" stroke="{color}" stroke-width="2" stroke-linecap="round" style="animation-delay:{n * 1.5 - 9:g}s"/>')
            body.append(label(x + 16, y + 27, clip_text(group["name"], 24), color, 11.5))
            body.append(t(x + 16, y + 48, clip_text(group["purpose"], 44), 13.5, INK2))
            body.append(chips)
        y += row_h + gap
    names = "; ".join(f'{g["name"].title()}: {", ".join(g["tools"])}' for g in groups)
    return svg(w, round(y + pad - gap), "Build kit — tools grouped by purpose", names, "".join(body), CSS)


# ---------------------------------------------------------------- GitHub signal
def _signal_tile(x, y, w, signal):
    out = [label(x, y + 12, "12 MONTHS ON GITHUB", VOLT, 11)]
    total = f'{signal["total"]:,}'
    out.append(t(x - 2, y + 78, total, 60, INK, 800, ls=-2))
    out.append(t(x + sans_w(total, 60, 800) + 6, y + 78, "contributions", 16, INK2))
    weeks = signal["weeks"][-53:]
    top, base = y + 104, y + 196
    peak = max((c for _, c in weeks), default=0) or 1
    pitch = w / max(1, len(weeks))
    last_month = None
    for k, (start, count) in enumerate(weeks):
        bx = x + k * pitch
        height = max(2.0, (base - top) * count / peak) if count else 1.5
        fill = VOLT if count else LINE2
        out.append(f'<rect class="bw" x="{bx:.1f}" y="{base - height:.1f}" width="{max(2.0, pitch - 2.4):.1f}" height="{height:.1f}" rx="1.2" fill="{fill}" '
                   f'style="animation-delay:{k / len(weeks) * 4 - 7:.2f}s"><title>Week of {esc(start)}: {count} contributions</title></rect>')
        month = start[5:7]
        if month != last_month and k < len(weeks) - 2 and (last_month is not None or k == 0):
            out.append(label(bx, base + 16, MONTHS[int(month) - 1].upper(), INK3, 9))
        last_month = month
    out.append(f'<path class="head fx" style="--run:{w:g}px" d="M{x:g} {top - 6}V{base + 2}" stroke="{INK}" stroke-width="1"/>')
    stats = [(f'{signal["active_months"]}/12', "ACTIVE MONTHS"), (f'{signal["longest_streak"]} days', "LONGEST STREAK"),
             (str(signal["peak_week"]), "BUSIEST WEEK"), (str(signal["public_repos"]), "PUBLIC REPOS")]
    for k, (value, name) in enumerate(stats):
        sx = x + k * w / 4
        out.append(t(sx, y + 250, value, 19, INK, 700))
        out.append(t(sx, y + 268, name, 9, INK3, 500, mono=True, ls=0.5))
    return "".join(out)


def _rhythm_tile(x, y, w, rhythm, languages):
    block = rhythm["block"]
    out = [label(x, y + 12, "WHEN COMMITS LAND / IST", CYAN, 11)]
    out.append(t(x, y + 50, rhythm["chronotype"], 26, INK, 700, ls=-0.4))
    share = round(100 * rhythm["block_share"])
    out.append(t(x, y + 74, f'Busiest {block:02d}:00–{(block + 3) % 24:02d}:00 · {share}% of {rhythm["total"]} commits', 13, INK2))
    top, base = y + 104, y + 174
    hours = rhythm["per_hour"]
    peak = max(hours) or 1
    pitch = w / 24
    for hour, count in enumerate(hours):
        bx = x + hour * pitch
        height = max(2.0, (base - top) * count / peak)
        hot = (hour - block) % 24 < 3
        out.append(f'<rect class="bw" x="{bx:.1f}" y="{base - height:.1f}" width="{pitch - 4:.1f}" height="{height:.1f}" rx="2" fill="{CYAN if hot else "#55657a"}" '
                   f'style="animation-delay:{hour / 24 * 4 - 7:.2f}s"><title>{hour:02d}:00: {count} commits</title></rect>')
        if hour % 6 == 0:
            out.append(label(bx, base + 16, f"{hour:02d}", INK3, 9))
    out.append(f'<path class="head fx" style="--run:{w:g}px" d="M{x:g} {top - 6}V{base + 2}" stroke="{INK}" stroke-width="1"/>')
    # Languages by bytes of code
    out.append(label(x, y + 218, "LANGUAGES BY CODE SIZE", INK3, 9.5))
    palette = [VOLT, CYAN, VIOLET, AMBER, GREEN, INK3]
    total = sum(share for _, share in languages) or 1
    lx = x
    for k, (name, share) in enumerate(languages[:6]):
        seg = w * share / total
        out.append(f'<rect x="{lx:.1f}" y="{y + 228}" width="{max(1.0, seg - 2):.1f}" height="8" rx="3" fill="{palette[k]}"><title>{esc(name)}: {share}%</title></rect>')
        lx += seg
    for k, (name, share) in enumerate(languages[:6]):
        cx, cy = x + (k % 3) * w / 3, y + 256 + (k // 3) * 19
        out.append(dot(cx + 4, cy - 4, 3.5, palette[k], ""))
        out.append(t(cx + 14, cy, f"{clip_text(name, 11)} {share:.0f}%", 12, INK2))
    return "".join(out)


def pulse(data, mobile=False) -> str:
    signal, rhythm = data["signal"], data["rhythm"]
    w = NARROW if mobile else WIDE
    pad, tile_h = (18, 304) if mobile else (24, 304)
    tw = w - 2 * pad if mobile else (w - 2 * pad - 12) / 2
    stamp = data.get("refreshed_at", "")[:10]
    body = [dot(pad + 3, 34, 3.5, VOLT), label(pad + 14, 38, "SIGNAL / FROM GITHUB DATA", VOLT, 12),
            label(w - pad, 38, f"SNAPSHOT {stamp}", INK3, 11, "end")]
    y = 58
    body.append(rrect(pad, y, tw, tile_h, 12, BG2, LINE) + _signal_tile(pad + 18, y + 18, tw - 36, signal))
    if mobile:
        y += tile_h + 10
        x2 = pad
    else:
        x2 = pad + tw + 12
    body.append(rrect(x2, y, tw, tile_h, 12, BG2, LINE) + _rhythm_tile(x2 + 18, y + 18, tw - 36, rhythm, signal["languages"]))
    desc = (f'{signal["total"]} contributions in the last 12 months, active in {signal["active_months"]} of 12 months, longest streak '
            f'{signal["longest_streak"]} days, busiest week {signal["peak_week"]}, {signal["public_repos"]} public repositories. '
            f'{rhythm["chronotype"]}: busiest three hours start at {rhythm["block"]:02d}:00 IST. Languages: '
            + ", ".join(f"{n} {s:.0f}%" for n, s in signal["languages"]) + ".")
    return svg(w, y + tile_h + pad, "GitHub signal — contributions, commit hours and languages", desc, "".join(body), CSS)


# ---------------------------------------------------------------- route
RECORD = [("IIT Madras", "BS, Data Science & Applications · 2025–2029", "CGPA 9.0", VOLT),
          ("Scaler School of Technology", "Co-enrolled · 2025–2029", "", CYAN),
          ("Paradox DSA Triathlon", "IIT Madras · 2026", "RUNNER-UP", AMBER),
          ("Meta PyTorch OpenEnv Hackathon", "Team submission · 2026", "HACKATHON", VIOLET)]

STOPS = [("OCT 2025", "First public repository", INK3), ("APR 2026", "OpenEnv hackathon environment", VIOLET),
         ("MAY 2026", "LexGuard", AMBER), ("JUN 2026", "POSIX shell in C++", INK3), ("JUL 2026", "Pikina · Resilion", CYAN),
         ("AUG 2026", "Noesis", VIOLET), ("OCT 2026", "HostelDesk 1.0 · ShopKart", VOLT)]


def route(mobile=False) -> str:
    w = NARROW if mobile else WIDE
    pad = 18 if mobile else 24
    tw = w - 2 * pad if mobile else (w - 2 * pad - 12) / 2
    body = [dot(pad + 3, 34, 3.5, VOLT), label(pad + 14, 38, "ROUTE / RECORD SO FAR", VOLT, 12),
            label(w - pad, 38, "2025 → 2026", INK3, 11, "end")]
    y = 58
    # Record: education and results
    rec_h = 30 + len(RECORD) * 62
    route_h = 46 + len(STOPS) * 34
    tile_h = rec_h if mobile else max(rec_h, route_h)
    body.append(rrect(pad, y, tw, tile_h, 12, BG2, LINE))
    for k, (name, sub, tag, color) in enumerate(RECORD):
        ry = y + (tile_h - (len(RECORD) - 1) * 62 - 40) / 2 + k * 62
        body.append(f'<rect x="{pad + 18}" y="{ry}" width="3" height="40" rx="1.5" fill="{color}"/>')
        body.append(t(pad + 34, ry + 16, name, 15.5, INK, 700))
        body.append(t(pad + 34, ry + 36, sub, 12.5, INK2))
        if tag:
            body.append(label(pad + tw - 18, ry + 16, tag, color, 10.5, "end"))
    # Route: what shipped, in order
    if mobile:
        x2, y2, tile2 = pad, y + tile_h + 10, route_h
    else:
        x2, y2, tile2 = pad + tw + 12, y, tile_h
    body.append(rrect(x2, y2, tw, tile2, 12, BG2, LINE))
    lx, first = x2 + 108, y2 + 34
    run = (len(STOPS) - 1) * 34
    body.append(f'<path d="M{lx:g} {first}v{run}" stroke="{LINE2}" stroke-width="2" stroke-linecap="round"/>')
    body.append(f'<circle class="walk fx" style="--run:{run}px" cx="{lx:g}" cy="{first}" r="5" fill="{BG}" stroke="{VOLT}" stroke-width="2"/>')
    for k, (when, name, color) in enumerate(STOPS):
        sy = first + k * 34
        delay = k / (len(STOPS) - 1) * 6.3 - 8
        body.append(f'<g class="stop" style="animation-delay:{delay:.2f}s">' + label(x2 + 18, sy + 4, when, INK2, 10.5)
                    + f'<circle cx="{lx:g}" cy="{sy}" r="4.5" fill="{color}" stroke="{BG2}" stroke-width="2"/>'
                    + t(lx + 18, sy + 5, name, 14.5, INK, 600) + "</g>")
    desc = ("Education: " + "; ".join(f"{n} ({s}{', ' + g if g else ''})" for n, s, g, _ in RECORD) + ". Route: "
            + "; ".join(f"{d.title()} {n}" for d, n, _ in STOPS) + ".")
    return svg(w, y2 + tile2 + pad, "Route so far — education, results and what shipped", desc, "".join(body), CSS)


# ---------------------------------------------------------------- contact
def contact(mobile=False) -> str:
    title = "Bring the problem. I'll bring the checks."
    desc = "Open to AI engineering internships, agent systems and hackathon teams. Links to LinkedIn, email and repositories follow."
    if mobile:
        w, h, top = NARROW, 400, 214
        hills = [(250, 100, 150, 80, 1.0), (90, 70, 90, 60, 0.5), (380, 140, 80, 60, 0.5)]
        defs, base, overlay = _map(w, h - top, 0, top, hills, [("Your project", "NEXT DROP", VOLT, 250, 96, -1, True)], (250, 96, 70), ((0, 20), (456, 150)), seed=77)
        body = [base, f'<rect width="{w}" height="{top + 40}" fill="url(#c-fade)"/>', overlay]
        body += [dot(21, 34, 3.5, VOLT), label(32, 38, "NEXT DROP / OPEN COMMS", VOLT, 12)]
        body += [t(17, 92, "Bring the problem.", 37, INK, 800, ls=-1), t(17, 136, "I'll bring the checks.", 37, VOLT, 800, ls=-1)]
        for k, line in enumerate(wrap("Open to AI engineering internships, agent systems and hackathon teams.", w - 40, 15.5)):
            body.append(t(18, 168 + k * 22, line, 15.5, INK2))
        defs += (f'<linearGradient id="c-fade" x1="0" y1="0" x2="0" y2="1"><stop offset=".84" stop-color="{BG}"/><stop offset="1" stop-color="{BG}" stop-opacity="0"/></linearGradient>')
        return svg(w, h, title, desc, "".join(body), HERO_CSS + CSS, defs)
    w, h = WIDE, 240
    hills = [(700, 120, 170, 100, 1.0), (850, 60, 90, 70, 0.5), (560, 190, 90, 60, 0.45), (200, 120, 240, 160, -0.5)]
    defs, base, overlay = _map(w, h, 0, 0, hills, [("Your project", "NEXT DROP", VOLT, 716, 122, -1, True)], (716, 122, 84), ((470, 30), (900, 190)), seed=77)
    body = [base, f'<rect width="{w}" height="{h}" fill="url(#c-fade)"/>', overlay]
    body += [dot(27, 34, 3.5, VOLT), label(38, 38, "NEXT DROP / OPEN COMMS", VOLT, 12)]
    body += [t(22, 104, "Bring the problem.", 44, INK, 800, ls=-1.2), t(22, 154, "I'll bring the checks.", 44, VOLT, 800, ls=-1.2)]
    body.append(t(24, 196, "Open to AI engineering internships, agent systems and hackathon teams.", 15.5, INK2))
    defs += (f'<linearGradient id="c-fade" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{BG}"/><stop offset=".5" stop-color="{BG}" stop-opacity=".92"/>'
             f'<stop offset=".68" stop-color="{BG}" stop-opacity="0"/></linearGradient>')
    return svg(w, h, title, desc, "".join(body), HERO_CSS + CSS, defs)


def button(text, color) -> str:
    w, h = round(max(200, 42 + mono_w(text, 13, 1.4) + 54)), 52
    body = dot(26, 26, 3.5, color) + t(42, 31, text, 13, INK, 600, mono=True, ls=1.4)
    body += f'<path d="M{w - 34} 32l10-10m-7 0h7v7" fill="none" stroke="{color}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>'
    body += comet(0.75, 0.75, w - 1.5, h - 1.5, 13, color, 6)
    return svg(w, h, text.title(), f"Link: {text.title()}", body, CSS, radius=14, glow=color)

