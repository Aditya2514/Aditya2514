"""Atlas design kit: colours, type, SVG primitives and the contour-map generator.

Every Atlas image is a self-contained SVG that GitHub can show through <img>:
system fonts only, no scripts, no external files. Standard library only.
"""
from html import escape
import math
import random

# ---------------------------------------------------------------- tokens
BG, BG2, BG3 = "#07090d", "#0c1017", "#121821"
LINE, LINE2 = "#1c2530", "#2c3848"
INK, INK2, INK3 = "#f1f4f7", "#aeb8c4", "#7d8997"
VOLT, CYAN, AMBER, RED, VIOLET, GREEN = "#c8f542", "#5ed3e8", "#ffb648", "#ff6b63", "#a698ff", "#5ee6a0"

SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI','Helvetica Neue',Helvetica,Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,'Liberation Mono',monospace"

TILE, GAP = 432, 12            # every scene is built from 432-wide tiles
WIDE = GAP * 3 + TILE * 2      # 900: two tiles side by side (desktop)
NARROW = GAP * 2 + TILE        # 456: one tile (phones)

BASE_CSS = f"""
text{{font-family:{SANS}}}
.m{{font-family:{MONO}}}
.pulse{{animation:pulse 2.4s ease-in-out infinite}}
.comet{{animation:comet 9s linear infinite}}
.still{{display:none}}
@keyframes pulse{{50%{{opacity:.25}}}}
@keyframes comet{{to{{stroke-dashoffset:-1000}}}}
@media (prefers-reduced-motion:reduce){{*{{animation:none!important}}.fx{{display:none}}.still{{display:inline}}.bw{{opacity:.9}}}}
"""


# ---------------------------------------------------------------- text
def esc(value) -> str:
    return escape(str(value), quote=True)


def mono_w(value, size, spacing=0.0) -> float:
    """Width of monospace text; 0.61em is the widest of the fonts in MONO."""
    return len(str(value)) * (size * 0.61 + spacing)


_NARROW, _WIDE = set("iljtf.,:;'!|()[]/ "), set("mwMW@")


def sans_w(value, size, weight=400) -> float:
    """Estimated width of proportional text, deliberately a little generous."""
    total = 0.0
    for ch in str(value):
        if ch in _NARROW:
            total += 0.30
        elif ch in _WIDE:
            total += 0.86
        elif ch.isupper() or ch.isdigit():
            total += 0.67 if ch.isupper() else 0.57
        else:
            total += 0.55
    return total * size * (1.06 if weight >= 600 else 1.0)


def wrap(value, width, size, weight=400, max_lines=None) -> list[str]:
    """Greedy word wrap by estimated width; long words are split, overflow ends in an ellipsis."""
    words, lines, line = [], [], ""
    for word in str(value).split():
        while sans_w(word, size, weight) > width and len(word) > 4:
            cut = max(4, int(len(word) * width / sans_w(word, size, weight)) - 1)
            words.append(word[:cut])
            word = word[cut:]
        words.append(word)
    for word in words:
        trial = f"{line} {word}".strip()
        if line and sans_w(trial, size, weight) > width:
            lines.append(line)
            line = word
        else:
            line = trial
    if line:
        lines.append(line)
    if max_lines and len(lines) > max_lines:
        lines = lines[:max_lines]
        lines[-1] = lines[-1].rstrip(" .,;:") + "…"
    return lines or [""]


def clip_text(value, max_chars) -> str:
    value = " ".join(str(value).split())
    return value if len(value) <= max_chars else value[: max_chars - 1].rstrip() + "…"


def t(x, y, value, size=14, fill=INK, weight=400, anchor=None, mono=False, ls=None, cls="", op=None, extra="") -> str:
    attrs = [f'x="{x:g}" y="{y:g}" font-size="{size:g}" fill="{fill}"']
    if weight != 400:
        attrs.append(f'font-weight="{weight}"')
    if anchor:
        attrs.append(f'text-anchor="{anchor}"')
    if ls is not None:
        attrs.append(f'letter-spacing="{ls:g}"')
    if op is not None:
        attrs.append(f'opacity="{op:g}"')
    klass = " ".join(c for c in (("m" if mono else ""), cls) if c)
    if klass:
        attrs.append(f'class="{klass}"')
    if extra:
        attrs.append(extra)
    return f"<text {' '.join(attrs)}>{esc(value)}</text>"


def label(x, y, value, fill=INK3, size=11, anchor=None, cls="", op=None) -> str:
    """Small tracked monospace caption: the HUD voice of the system."""
    return t(x, y, value, size, fill, 500, anchor, True, 1.6, cls, op)


def chip(x, y, value, color=INK2, size=12, h=24, fill=BG3, stroke=LINE2, pad=10) -> tuple[str, float]:
    """Monospace pill. Returns (svg, width) so callers can flow chips."""
    w = round(mono_w(value, size) + pad * 2, 1)
    body = f'<rect x="{x:g}" y="{y:g}" width="{w:g}" height="{h}" rx="{h / 2:g}" fill="{fill}" stroke="{stroke}"/>'
    body += t(x + pad, y + h / 2 + size * 0.36, value, size, color, 500, mono=True)
    return body, w


def flow_chips(x, y, values, max_w, color=INK2, size=12, h=24, gap=6, max_rows=2) -> tuple[str, float]:
    """Lay chips out left to right, wrapping; returns (svg, bottom y)."""
    out, cx, cy, rows = [], x, y, 1
    for value in values:
        value = clip_text(value, 22)
        w = mono_w(value, size) + 20
        if cx + w > x + max_w and cx > x:
            rows += 1
            if rows > max_rows:
                break
            cx, cy = x, cy + h + gap
        body, w = chip(cx, cy, value, color, size, h)
        out.append(body)
        cx += w + gap
    return "".join(out), cy + h


# ---------------------------------------------------------------- shapes
def rrect(x, y, w, h, r=14, fill=BG2, stroke=LINE, extra="") -> str:
    return f'<rect x="{x:g}" y="{y:g}" width="{w:g}" height="{h:g}" rx="{r:g}" fill="{fill}" stroke="{stroke}" {extra}/>'


def dot(x, y, r=3.5, fill=VOLT, cls="pulse", extra="") -> str:
    klass = f' class="{cls}"' if cls else ""
    return f'<circle cx="{x:g}" cy="{y:g}" r="{r:g}" fill="{fill}"{klass} {extra}/>'


def brackets(x, y, w, h, size=10, stroke=LINE2, sw=1.5) -> str:
    """Four corner ticks, like a viewfinder."""
    s = size
    d = (f"M{x} {y + s}V{y}H{x + s}M{x + w - s} {y}H{x + w}V{y + s}"
         f"M{x + w} {y + h - s}V{y + h}H{x + w - s}M{x + s} {y + h}H{x}V{y + h - s}")
    return f'<path d="{d}" fill="none" stroke="{stroke}" stroke-width="{sw}"/>'


def comet(x, y, w, h, r=16, color=VOLT, seconds=9, delay=0) -> str:
    """A short bright dash that travels round a rounded rectangle's border."""
    per = 2 * (w + h - 4 * r) + 2 * math.pi * r
    return (f'<rect class="comet fx" x="{x:g}" y="{y:g}" width="{w:g}" height="{h:g}" rx="{r:g}" fill="none" '
            f'stroke="{color}" stroke-width="1.5" stroke-linecap="round" pathLength="1000" '
            f'stroke-dasharray="70 930" style="animation-duration:{seconds}s;animation-delay:-{delay}s"/>')


def arrow(x1, y1, x2, y2, color=LINE2, sw=1.5, head=5, dash=None, cls="") -> str:
    a = math.atan2(y2 - y1, x2 - x1)
    hx1 = x2 - head * math.cos(a - 0.5)
    hy1 = y2 - head * math.sin(a - 0.5)
    hx2 = x2 - head * math.cos(a + 0.5)
    hy2 = y2 - head * math.sin(a + 0.5)
    dashed = f' stroke-dasharray="{dash}"' if dash else ""
    klass = f' class="{cls}"' if cls else ""
    return (f'<path d="M{x1:g} {y1:g}L{x2:g} {y2:g}M{hx1:.1f} {hy1:.1f}L{x2:g} {y2:g}L{hx2:.1f} {hy2:.1f}" fill="none" '
            f'stroke="{color}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"{dashed}{klass}/>')


# ---------------------------------------------------------------- animation helpers
def window(name, total, start, end, fade=0.35, low=0.0, high=1.0) -> str:
    """Keyframes for 'on between start and end seconds of a total-second loop'."""
    def pct(sec):
        return f"{max(0.0, min(100.0, 100 * sec / total)):.2f}%"
    a, b, c, d = start - fade, start, end, end + fade
    frames = []
    if a > 0:
        frames.append(f"0%,{pct(a)}{{opacity:{low:g}}}")
    frames.append(f"{pct(b)},{pct(c)}{{opacity:{high:g}}}")
    if d < total:
        frames.append(f"{pct(d)},100%{{opacity:{low:g}}}")
    return f"@keyframes {name}{{{''.join(frames)}}}.{name}{{opacity:{low:g};animation:{name} {total:g}s linear infinite}}"


def after(name, total, start, fade=0.35, low=0.0, high=1.0, reset=0.6) -> str:
    """Keyframes for 'switch on at start and stay on until the loop restarts'."""
    return (window(name, total, start, total - reset, fade, low, high)
            + f"@media (prefers-reduced-motion:reduce){{.{name}{{opacity:{high:g}}}}}")


# ---------------------------------------------------------------- document
def svg(w, h, title, desc, body, css="", defs="", radius=18, glow=VOLT) -> str:
    """Wrap a scene in the shared card: dark surface, hairline border, soft corner light."""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="t d">
<title id="t">{esc(title)}</title><desc id="d">{esc(desc)}</desc>
<style>{BASE_CSS}{css}</style>
<defs>
<radialGradient id="k-glow" cx="0" cy="0" r="1"><stop offset="0" stop-color="{glow}" stop-opacity=".10"/><stop offset="1" stop-color="{glow}" stop-opacity="0"/></radialGradient>
<linearGradient id="k-edge" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".09"/><stop offset=".25" stop-color="#fff" stop-opacity="0"/></linearGradient>
<clipPath id="k-card"><rect width="{w}" height="{h}" rx="{radius}"/></clipPath>
{defs}</defs>
<g clip-path="url(#k-card)"><rect width="{w}" height="{h}" fill="{BG}"/><rect width="{w * 0.7:g}" height="{h}" fill="url(#k-glow)"/>
{body}</g>
<rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="{radius - .5}" fill="none" stroke="{LINE}"/>
<rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="{radius - .5}" fill="none" stroke="url(#k-edge)"/>
</svg>
'''


def header(w, index, name, status="", color=VOLT, y=30, pad=24) -> str:
    """Top strip of a scene: numbered label on the left, live status on the right."""
    out = dot(pad + 3, y - 4, 3.5, color)
    out += label(pad + 14, y, f"{index} / {name}", color, 12)
    if status:
        out += label(w - pad, y, status, INK3, 11, "end")
    return out


# ---------------------------------------------------------------- contour map
def terrain(w, h, seed, hills, step=10) -> list[list[float]]:
    """A smooth height field: a few Gaussian hills plus gentle ripples. Deterministic."""
    rng = random.Random(seed)
    waves = [(rng.uniform(0.006, 0.016), rng.uniform(0.006, 0.016), rng.uniform(0, 6.28), rng.uniform(0.03, 0.07)) for _ in range(5)]
    cols, rows = w // step + 2, h // step + 2
    field = []
    for j in range(rows):
        row = []
        for i in range(cols):
            x, y = i * step, j * step
            value = sum(a * math.exp(-(((x - cx) / sx) ** 2 + ((y - cy) / sy) ** 2)) for cx, cy, sx, sy, a in hills)
            value += sum(a * math.sin(x * fx + y * fy + p) for fx, fy, p, a in waves)
            row.append(value)
        field.append(row)
    return field


def contours(field, step, level) -> list[list[tuple[float, float]]]:
    """Marching squares for one level, stitched into polylines."""
    segments = []
    rows, cols = len(field), len(field[0])

    def lerp(ax, ay, av, bx, by, bv):
        k = (level - av) / (bv - av) if bv != av else 0.5
        return (round((ax + (bx - ax) * k) * step, 1), round((ay + (by - ay) * k) * step, 1))

    for j in range(rows - 1):
        for i in range(cols - 1):
            a, b, c, d = field[j][i], field[j][i + 1], field[j + 1][i + 1], field[j + 1][i]
            code = (a > level) << 3 | (b > level) << 2 | (c > level) << 1 | (d > level)
            if code in (0, 15):
                continue
            top = lambda: lerp(i, j, a, i + 1, j, b)
            right = lambda: lerp(i + 1, j, b, i + 1, j + 1, c)
            bottom = lambda: lerp(i, j + 1, d, i + 1, j + 1, c)
            left = lambda: lerp(i, j, a, i, j + 1, d)
            table = {1: [(left, bottom)], 2: [(bottom, right)], 3: [(left, right)], 4: [(top, right)],
                     5: [(top, left), (bottom, right)], 6: [(top, bottom)], 7: [(top, left)], 8: [(top, left)],
                     9: [(top, bottom)], 10: [(top, right), (left, bottom)], 11: [(top, right)], 12: [(left, right)],
                     13: [(bottom, right)], 14: [(left, bottom)]}
            for p, q in table[code]:
                segments.append((p(), q()))
    # Stitch segments that share endpoints into long lines.
    ends: dict = {}
    for index, (p, q) in enumerate(segments):
        ends.setdefault(p, []).append(index)
        ends.setdefault(q, []).append(index)
    used, lines = set(), []
    for start in range(len(segments)):
        if start in used:
            continue
        used.add(start)
        line = list(segments[start])
        for head in (False, True):
            while True:
                tip = line[0] if head else line[-1]
                nxt = next((k for k in ends.get(tip, []) if k not in used), None)
                if nxt is None:
                    break
                used.add(nxt)
                p, q = segments[nxt]
                other = q if p == tip else p
                if head:
                    line.insert(0, other)
                else:
                    line.append(other)
        if len(line) >= 4:
            lines.append(line)
    return lines


def smooth_path(points) -> str:
    """Quadratic curves through segment midpoints: cheap, round, compact."""
    if len(points) < 3:
        return ""
    closed = points[0] == points[-1]
    pts = points[:-1] if closed else points
    mid = lambda p, q: ((p[0] + q[0]) / 2, (p[1] + q[1]) / 2)
    if closed:
        start = mid(pts[-1], pts[0])
        out = [f"M{start[0]:.0f} {start[1]:.0f}"]
        for k, p in enumerate(pts):
            m = mid(p, pts[(k + 1) % len(pts)])
            out.append(f"Q{p[0]:.0f} {p[1]:.0f} {m[0]:.0f} {m[1]:.0f}")
        return "".join(out) + "Z"
    out = [f"M{pts[0][0]:.0f} {pts[0][1]:.0f}"]
    for k in range(1, len(pts) - 1):
        m = mid(pts[k], pts[k + 1])
        out.append(f"Q{pts[k][0]:.0f} {pts[k][1]:.0f} {m[0]:.0f} {m[1]:.0f}")
    out.append(f"L{pts[-1][0]:.0f} {pts[-1][1]:.0f}")
    return "".join(out)


def contour_paths(w, h, seed, hills, levels, step=10) -> list[tuple[float, str]]:
    """[(level, path data)] for the whole map; each level is one path string."""
    field = terrain(w, h, seed, hills, step)
    out = []
    for level in levels:
        data = "".join(smooth_path(line) for line in contours(field, step, level))
        if data:
            out.append((level, data))
    return out
