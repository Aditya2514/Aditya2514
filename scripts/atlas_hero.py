"""Atlas hero: the name over a generated contour map with a closing zone and project drop points."""
import math

from atlas_kit import (AMBER, BG, BG2, CYAN, INK, INK2, INK3, LINE, LINE2, NARROW, VIOLET, VOLT, WIDE,
                       brackets, chip, contour_paths, dot, label, mono_w, svg, t)

LOOP = 16  # seconds for one flight across the map

THESIS = [("01", "The model proposes.", VIOLET), ("02", "The system checks.", AMBER), ("03", "The person stays in control.", VOLT)]
CREDENTIALS = ["IIT MADRAS · DATA SCIENCE", "SCALER SCHOOL OF TECHNOLOGY", "CGPA 9.0"]

HERO_CSS = f"""
.ring{{transform-box:fill-box;transform-origin:center;animation:ring {LOOP}s ease-out infinite}}
@keyframes ring{{0%{{transform:scale(.4);opacity:0}}3%{{opacity:.95}}22%{{transform:scale(3.6);opacity:0}}100%{{transform:scale(3.6);opacity:0}}}}
.step{{animation:step 9s linear infinite}}
.s2{{animation-delay:3s}}.s3{{animation-delay:6s}}
@keyframes step{{0%,30%{{opacity:1}}36%,94%{{opacity:.5}}100%{{opacity:1}}}}
.rise{{animation:rise .9s cubic-bezier(.2,.7,.2,1) both}}
@keyframes rise{{from{{opacity:0;transform:translateY(14px)}}}}
.blink{{animation:blink 1.1s steps(2) infinite}}
@keyframes blink{{50%{{opacity:0}}}}
"""


def _map(w, h, ox, oy, hills, pois, zone, flight, seed=2514):
    """Contours, grid, zone and radar (base), then flight path and drop points (overlay). Returns (defs, base, overlay)."""
    levels = [0.16 + 0.105 * k for k in range(9)]
    paths = contour_paths(w, h, seed, hills, levels)
    body = [f'<g transform="translate({ox} {oy})">']
    # Grid squares with map references along the top edge.
    grid = "".join(f"M{x} 0V{h}" for x in range(0, w + 1, 72)) + "".join(f"M0 {y}H{w}" for y in range(0, h + 1, 72))
    body.append(f'<path d="{grid}" stroke="{LINE}" stroke-width="1" opacity=".55"/>')
    for k, (level, data) in enumerate(paths):
        coast = k == 0
        major = k % 3 == 0
        colour = CYAN if coast else "#8fa3b8"
        opacity = 0.6 if coast else (0.42 if major else 0.24)
        body.append(f'<path d="{data}" fill="none" stroke="{colour}" stroke-width="{1.4 if coast or major else 1}" opacity="{opacity}"/>')
    zx, zy, zr = zone
    # Radar sweep around the zone centre.
    r = zr * 1.9
    a = math.radians(42)
    body.append(f'<g transform="translate({zx} {zy})" class="fx"><path d="M0 0L0 {-r:g}A{r:g} {r:g} 0 0 0 {-r * math.sin(a):.1f} {-r * math.cos(a):.1f}Z" fill="url(#h-sweep)">'
                f'<animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="8s" repeatCount="indefinite"/></path></g>')
    # Safe zone (steady) and the zone that closes on it.
    body.append(f'<circle cx="{zx}" cy="{zy}" r="{zr}" fill="{VOLT}" fill-opacity=".025" stroke="{INK}" stroke-opacity=".55" stroke-width="1.2" stroke-dasharray="3 5"/>')
    body.append(f'<circle class="fx" cx="{zx}" cy="{zy}" r="{zr * 2}" fill="none" stroke="{CYAN}" stroke-width="2">'
                f'<animate attributeName="r" dur="{LOOP}s" repeatCount="indefinite" values="{zr * 2.1:g};{zr:g};{zr:g}" keyTimes="0;.78;1" calcMode="spline" keySplines=".45 0 .25 1;0 0 1 1"/>'
                f'<animate attributeName="opacity" dur="{LOOP}s" repeatCount="indefinite" values="0;.85;.85;0" keyTimes="0;.06;.86;1"/></circle>')
    body.append(f'<path d="M{zx - 7} {zy}H{zx + 7}M{zx} {zy - 7}V{zy + 7}" stroke="{INK3}" stroke-width="1"/>')
    body.append("</g>")
    base, body = "".join(body), [f'<g transform="translate({ox} {oy})">']
    # Flight path with an aircraft; each drop point pings as the aircraft passes it.
    (fx1, fy1), (fx2, fy2) = flight
    body.append(f'<path id="h-flight" d="M{fx1} {fy1}L{fx2} {fy2}" stroke="{VOLT}" stroke-width="1.2" stroke-dasharray="2 7" opacity=".5" fill="none"/>')
    plane = "M13 0L5-2-1-10-4-10-1.5-2-8-1.5-11-5-13-5-11.5 0-13 5-11 5-8 1.5-1.5 2-4 10-1 10 5 2Z"
    body.append(f'<g class="fx"><path d="{plane}" fill="{VOLT}"><animateMotion dur="{LOOP}s" repeatCount="indefinite" rotate="auto"><mpath href="#h-flight"/></animateMotion></path></g>')
    length = math.hypot(fx2 - fx1, fy2 - fy1)
    ux, uy = (fx2 - fx1) / length, (fy2 - fy1) / length
    for name, role, colour, px, py, side, live in pois:
        along = max(0.04, min(0.96, ((px - fx1) * ux + (py - fy1) * uy) / length))
        jx, jy = fx1 + ux * along * length, fy1 + uy * along * length
        delay = along * LOOP
        body.append(f'<path d="M{jx:.0f} {jy:.0f}L{px} {py}" stroke="{colour}" stroke-width="1" stroke-dasharray="1 5" opacity=".55"/>')
        end = min(0.99, along + 0.07)
        body.append(f'<circle class="fx" r="3" fill="{colour}" opacity="0"><animateMotion dur="{LOOP}s" repeatCount="indefinite" calcMode="linear" '
                    f'keyPoints="0;0;1;1" keyTimes="0;{along:.3f};{end:.3f};1" path="M{jx:.0f} {jy:.0f}L{px} {py}"/>'
                    f'<animate attributeName="opacity" dur="{LOOP}s" repeatCount="indefinite" values="0;0;1;1;0;0" keyTimes="0;{along:.3f};{along + 0.005:.3f};{end:.3f};{end + 0.005:.3f};1"/></circle>')
        body.append(f'<circle class="ring fx" cx="{px}" cy="{py}" r="7" fill="none" stroke="{colour}" stroke-width="1.5" style="animation-delay:{delay + 0.07 * LOOP - LOOP:.2f}s"/>')
        body.append(f'<path d="M{px} {py - 7}L{px + 7} {py}L{px} {py + 7}L{px - 7} {py}Z" fill="{BG}" stroke="{colour}" stroke-width="1.6"/>')
        body.append(dot(px, py, 2.6, colour, "pulse" if live else ""))
        tag_w = max(mono_w(role, 10.5, 0.6), len(name) * 9.4) + 20
        tx = px + 14 if side > 0 else px - 14 - tag_w
        body.append(f'<rect x="{tx:.0f}" y="{py - 21}" width="{tag_w:.0f}" height="42" rx="7" fill="{BG}" fill-opacity=".86" stroke="{colour}" stroke-opacity=".45"/>')
        body.append(t(tx + 10, py - 3, name, 14.5, INK, 700))
        body.append(t(tx + 10, py + 13, role, 10.5, colour, 500, mono=True, ls=0.6))
    body.append("</g>")
    defs = (f'<linearGradient id="h-sweep" gradientUnits="userSpaceOnUse" x1="{-r * 0.6:.0f}" y1="{-r * 0.7:.0f}" x2="0" y2="{-r * 0.7:.0f}">'
            f'<stop offset="0" stop-color="{VOLT}" stop-opacity="0"/><stop offset="1" stop-color="{VOLT}" stop-opacity=".16"/></linearGradient>')
    return defs, base, "".join(body)


def _fit(width):
    """Pin the wordmark to a fixed width so every system font fills the same space."""
    return f'textLength="{width}"'


def _thesis(x, y, gap, size):
    out = []
    for k, (num, line, colour) in enumerate(THESIS):
        yy = y + k * gap
        out.append(f'<g class="step s{k + 1}">')
        out.append(f'<rect x="{x}" y="{yy - size - 3}" width="34" height="{size + 9}" rx="6" fill="{colour}" fill-opacity=".13" stroke="{colour}" stroke-opacity=".5"/>')
        out.append(t(x + 17, yy + 0.5, num, size - 4, colour, 700, "middle", True))
        out.append(t(x + 46, yy + 1, line, size, INK, 600))
        out.append("</g>")
    return "".join(out)


def _chips(x, y, max_w):
    out, cx, cy = [], x, y
    for value in CREDENTIALS:
        w = mono_w(value, 11) + 20
        if cx + w > x + max_w and cx > x:
            cx, cy = x, cy + 31
        body, w = chip(cx, cy, value, INK2, 11, 25, BG2, LINE2)
        out.append(body)
        cx += w + 7
    return "".join(out), cy + 25


def hero(mobile=False) -> str:
    title = "Aditya Singh — AI systems, agents and full-stack"
    desc = ("Aditya Singh, studying Data Science at IIT Madras and at Scaler School of Technology, CGPA 9.0. "
            "The model proposes. The system checks. The person stays in control. "
            "An animated contour map marks four projects: LexGuard, Pikina, Noesis and Resilion.")
    if mobile:
        w, h, top = NARROW, 800, 466
        hills = [(240, 170, 150, 105, 1.0), (110, 100, 90, 70, 0.55), (350, 100, 80, 70, 0.5), (120, 262, 100, 60, 0.5), (360, 262, 80, 60, 0.45)]
        pois = [("LexGuard", "CONTRACT CHECKS", AMBER, 92, 92, 1, True), ("Pikina", "LOCAL AGENT", CYAN, 350, 138, -1, True),
                ("Noesis", "CITED SEARCH", VIOLET, 104, 226, 1, True), ("Resilion", "IN PROGRESS", INK3, 366, 268, -1, False)]
        defs, base, overlay = _map(w, h - top, 0, top, hills, pois, (228, 170, 112), ((0, 34), (456, 214)))
        body = [base, f'<rect width="{w}" height="{top + 60}" fill="url(#h-fade)"/>', overlay]
        body.append(dot(27, 26, 3.5, VOLT) + label(38, 30, "DROP ZONE / PROFILE", VOLT, 12))
        body.append(label(w - 24, 30, "GRID 25-14", INK3, 11, "end"))
        body.append(f'<g class="rise">{t(20, 128, "ADITYA", 92, INK, 800, extra=_fit(330))}</g>')
        body.append(f'<g class="rise" style="animation-delay:.12s">{t(20, 214, "SINGH", 92, VOLT, 800, extra=_fit(282))}</g>')
        body.append(t(24, 254, "AI systems  ·  agents  ·  full-stack", 21, INK2, 500))
        body.append(_thesis(24, 304, 37, 19))
        chips, bottom = _chips(24, 400, w - 48)
        body.append(chips)
        body.append(brackets(12, 12, w - 24, h - 24, 12, LINE2))
        defs += (f'<linearGradient id="h-fade" x1="0" y1="0" x2="0" y2="1"><stop offset=".86" stop-color="{BG}"/><stop offset="1" stop-color="{BG}" stop-opacity="0"/></linearGradient>')
        return svg(w, h, title, desc, "".join(body), HERO_CSS, defs)

    w, h = WIDE, 520
    hills = [(650, 262, 190, 150, 1.0), (800, 150, 110, 90, 0.6), (520, 150, 100, 80, 0.5), (560, 400, 120, 70, 0.5),
             (830, 400, 100, 80, 0.5), (130, 250, 200, 220, -0.5)]
    pois = [("LexGuard", "CONTRACT CHECKS", AMBER, 566, 152, -1, True), ("Pikina", "LOCAL AGENT", CYAN, 772, 214, 1, True),
            ("Noesis", "CITED SEARCH", VIOLET, 612, 356, -1, True), ("Resilion", "IN PROGRESS", INK3, 800, 410, -1, False)]
    defs, base, overlay = _map(w, h, 0, 0, hills, pois, (672, 268, 172), ((420, 72), (900, 300)))
    body = [base, f'<rect width="{w}" height="{h}" fill="url(#h-fade)"/>', overlay]
    # Top strip
    body.append(dot(27, 26, 3.5, VOLT) + label(38, 30, "DROP ZONE / PROFILE", VOLT, 12))
    body.append(label(w - 24, 30, "GRID 25-14  ·  SECTOR AI", INK3, 11, "end"))
    # Name
    body.append(f'<g class="rise">{t(20, 164, "ADITYA", 100, INK, 800, extra=_fit(358))}</g>')
    body.append(f'<g class="rise" style="animation-delay:.12s">{t(20, 256, "SINGH", 100, VOLT, 800, extra=_fit(306))}</g>')
    body.append(t(24, 298, "AI systems  ·  agents  ·  full-stack", 22, INK2, 500))
    body.append(_thesis(24, 350, 36, 18))
    chips, _ = _chips(24, h - 49, 640)
    body.append(chips)
    # Map furniture: compass and scale bar
    body.append(f'<g transform="translate({w - 44} 78)"><circle r="15" fill="{BG}" fill-opacity=".7" stroke="{LINE2}"/><path d="M0-10L4 3 0 0-4 3Z" fill="{VOLT}"/>{t(0, 30, "N", 10, INK3, 600, "middle", True)}</g>')
    body.append(f'<rect x="{w - 156}" y="{h - 56}" width="112" height="32" rx="6" fill="{BG}" fill-opacity=".8"/>'
                f'<path d="M{w - 150} {h - 30}v-6h100v6" fill="none" stroke="{INK3}" stroke-width="1.2"/>' + label(w - 100, h - 42, "500 M", INK3, 10, "middle"))
    body.append(brackets(12, 12, w - 24, h - 24, 12, LINE2))
    defs += (f'<linearGradient id="h-fade" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{BG}"/><stop offset=".36" stop-color="{BG}" stop-opacity=".93"/>'
             f'<stop offset=".6" stop-color="{BG}" stop-opacity="0"/></linearGradient>')
    return svg(w, h, title, desc, "".join(body), HERO_CSS, defs)


if __name__ == "__main__":
    import sys
    sys.stdout.write(hero("--mobile" in sys.argv))
