"""Render assets/rhythm.svg: a 24-hour clock of when the commits actually happen (IST).

  python3 scripts/build_rhythm.py --github LOGIN                 # GitHub REST API, needs GH_TOKEN (Actions)
  python3 scripts/build_rhythm.py --from-git DIR... --emails A,B  # offline preview from local clones

Never fails the build: if data can't be fetched, the existing SVG is left untouched.
"""

import math
import sys
from collections import Counter
from pathlib import Path
from xml.sax.saxutils import escape

from github_activity import IST, run_card
from theme import AMBER, BORDER, FAINT, MONO, MUTED, PANEL, SANS, SURFACE, TEAL, TEXT

OUT = Path(__file__).resolve().parent.parent / "assets" / "rhythm.svg"

W, H = 900, 380
CX, CY = 200, 218          # clock centre
R_IN, R_MAX = 36, 120      # bars run from R_IN out to at most R_MAX
SWEEP_S = 8.0              # one turn of the hand
BASE_OPACITY = 0.7
WEEKDAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
NIGHT = set(range(20, 24)) | set(range(0, 4))   # 20:00–04:00
EARLY = set(range(5, 10))                       # 05:00–10:00


def summarize(commits: list[dict]) -> dict:
    local = [c["authored_at"].astimezone(IST) for c in commits]
    hours = Counter(t.hour for t in local)
    days = Counter(t.weekday() for t in local)
    total = len(local)
    per_hour = [hours.get(h, 0) for h in range(24)]
    busiest_hour = max(range(24), key=lambda h: (per_hour[h], -h))
    # Busiest 3-hour block, wrapping round midnight
    block = max(range(24), key=lambda h: (sum(per_hour[(h + i) % 24] for i in range(3)), -h))
    block_n = sum(per_hour[(block + i) % 24] for i in range(3))
    night = sum(per_hour[h] for h in NIGHT)
    early = sum(per_hour[h] for h in EARLY)
    if night * 2 > total:
        chronotype = "Night owl"
    elif early * 2 > total:
        chronotype = "Early bird"
    else:
        chronotype = "Daytime builder"
    return {
        "total": total,
        "per_hour": per_hour,
        "busiest_hour": busiest_hour,
        "block": block,
        "block_share": block_n / total,
        "night_share": night / total,
        "per_day": [days.get(d, 0) for d in range(7)],
        "busiest_day": max(range(7), key=lambda d: (days.get(d, 0), -d)),
        "chronotype": chronotype,
    }


def hhmm(hour: int) -> str:
    return f"{hour % 24:02d}:00"


def polar(r: float, deg: float) -> tuple[float, float]:
    """Clock angle: 0° at the top (00:00), clockwise."""
    a = math.radians(deg - 90)
    return CX + r * math.cos(a), CY + r * math.sin(a)


def sector(r0: float, r1: float, a0: float, a1: float) -> str:
    """Annular sector between radii r0..r1 and clock angles a0..a1 (degrees, clockwise)."""
    large = 1 if (a1 - a0) % 360 > 180 else 0
    x0, y0 = polar(r1, a0)
    x1, y1 = polar(r1, a1)
    x2, y2 = polar(r0, a1)
    x3, y3 = polar(r0, a0)
    return (
        f"M{x0:.2f},{y0:.2f} A{r1},{r1} 0 {large} 1 {x1:.2f},{y1:.2f} "
        f"L{x2:.2f},{y2:.2f} A{r0},{r0} 0 {large} 0 {x3:.2f},{y3:.2f} Z"
    )


def text(x, y, s, size, fill, family=MONO, anchor="start", weight=None, spacing=None, extra=""):
    attrs = f'x="{x:.1f}" y="{y:.1f}" font-family="{family}" font-size="{size}" fill="{fill}"'
    if anchor != "start":
        attrs += f' text-anchor="{anchor}"'
    if weight:
        attrs += f' font-weight="{weight}"'
    if spacing:
        attrs += f' letter-spacing="{spacing}"'
    return f"<text {attrs}{extra}>{escape(s)}</text>"


def clock(s: dict) -> list[str]:
    out = []
    peak = max(s["per_hour"]) or 1
    r_ring = R_MAX + 4

    # Night window 20:00–04:00, shaded so the side-panel share has a visible referent
    out.append(f'<path d="{sector(R_IN - 2, r_ring, 300, 420)}" fill="{FAINT}" opacity="0.18"/>')
    nx, ny = polar(R_MAX - 22, 330)
    out.append(text(nx, ny + 3, "night", 10, MUTED, anchor="middle", spacing="1"))

    # Guide rings
    for r, op in ((R_IN, 1), ((R_IN + R_MAX) / 2, 0.5), (r_ring, 1)):
        out.append(f'<circle cx="{CX}" cy="{CY}" r="{r}" fill="none" stroke="{BORDER}" stroke-width="1" opacity="{op}"/>')

    # Hour ticks: small at every hour boundary, long + labelled at 00/06/12/18
    for h in range(24):
        major = h % 6 == 0
        x0, y0 = polar(r_ring, h * 15)
        x1, y1 = polar(r_ring + (7 if major else 3), h * 15)
        out.append(
            f'<line x1="{x0:.2f}" y1="{y0:.2f}" x2="{x1:.2f}" y2="{y1:.2f}" stroke="{MUTED if major else FAINT}" stroke-width="{1.5 if major else 1}"/>'
        )
        if major:
            tx, ty = polar(r_ring + 18, h * 15)
            out.append(text(tx, ty + 4, f"{h:02d}", 11, MUTED, anchor="middle"))

    # Bars: length = commits in that hour; each flashes as the hand passes its centre
    for h, n in enumerate(s["per_hour"]):
        mid = (h + 0.5) * 15
        if n == 0:
            x, y = polar(R_IN + 4, mid)
            out.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="1.6" fill="{FAINT}"/>')
            continue
        length = 5 + (R_MAX - R_IN - 5) * n / peak
        color = AMBER if h == s["busiest_hour"] else TEAL
        t_pass = (h + 0.5) / 24 * SWEEP_S
        begin = f"{t_pass - SWEEP_S:.3f}s"   # negative begin: already in phase at t=0
        anim = (
            f'<animate attributeName="opacity" values="1;{BASE_OPACITY};{BASE_OPACITY}" keyTimes="0;0.14;1" '
            f'dur="{SWEEP_S}s" begin="{begin}" repeatCount="indefinite"/>'
            f'<animate attributeName="fill" values="{TEXT};{color};{color}" keyTimes="0;0.08;1" '
            f'dur="{SWEEP_S}s" begin="{begin}" repeatCount="indefinite"/>'
        )
        out.append(
            f'<path d="{sector(R_IN + 2, R_IN + 2 + length, h * 15 + 2, h * 15 + 13)}" fill="{color}" opacity="{BASE_OPACITY}">'
            f"<title>{hhmm(h)}–{hhmm(h + 1)}: {n} commits</title>{anim}</path>"
        )

    # Sweeping hand with a fading wake (drawn at 00:00, rotated by SMIL)
    wake = "".join(
        f'<path d="{sector(R_IN, r_ring, -w1, -w0)}" fill="{TEAL}" opacity="{op}"/>'
        for w0, w1, op in ((0, 8, 0.16), (8, 16, 0.09), (16, 26, 0.04))
    )
    hx, hy = polar(r_ring + 2, 0)
    out.append(
        f'<g>{wake}'
        f'<line x1="{CX}" y1="{CY - 30}" x2="{hx:.2f}" y2="{hy:.2f}" stroke="{TEXT}" stroke-width="2" stroke-linecap="round"/>'
        f'<circle cx="{hx:.2f}" cy="{hy:.2f}" r="3.5" fill="{TEXT}"/>'
        f'<animateTransform attributeName="transform" type="rotate" from="0 {CX} {CY}" to="360 {CX} {CY}" '
        f'dur="{SWEEP_S}s" repeatCount="indefinite"/></g>'
    )

    # Hub
    out.append(f'<circle cx="{CX}" cy="{CY}" r="30" fill="{PANEL}" stroke="{BORDER}"/>')
    out.append(text(CX, CY - 2, "IST", 12, TEXT, anchor="middle", weight="700", spacing="1.5"))
    out.append(text(CX, CY + 12, "24 h", 10, MUTED, anchor="middle"))
    return out


def tile(x, y, w, h, value, label, value_fill, delay, extra="", value_size=22):
    return (
        f'<g class="tile" style="animation-delay:{delay:.2f}s">'
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{PANEL}" stroke="{BORDER}"/>'
        + text(x + 16, y + 32, value, value_size, value_fill, family=SANS, weight="700")
        + text(x + 16, y + 51, label, 10, MUTED, spacing="1.5")
        + extra
        + "</g>"
    )


def panel(s: dict) -> list[str]:
    x0, w = 400, 468
    out = [
        text(x0, 104, "CHRONOTYPE · DERIVED FROM COMMIT TIMES", 10, MUTED, spacing="1.5"),
        f'<g class="tile" style="animation-delay:0s">'
        + text(x0, 140, s["chronotype"], 30, TEXT, family=SANS, weight="700")
        + "</g>",
        text(
            x0, 166,
            f"busiest 3-hour block {hhmm(s['block'])}–{hhmm(s['block'] + 3)} IST · "
            f"{round(s['block_share'] * 100)}% of commits",
            13, MUTED, family=SANS,
        ),
    ]
    tw, th, gap = (w - 10) / 2, 64, 10
    ya, yb = 186, 186 + th + gap

    # Mini weekday bars inside the weekday tile, busiest day highlighted (letters >= 10px to stay legible)
    days, top = s["per_day"], max(s["per_day"]) or 1
    pitch, bar_w, bar_max = 12, 8, 28
    bx0, base = x0 + tw + gap + tw - 16 - (6 * pitch + bar_w), yb + 44
    mini = "".join(
        f'<rect x="{bx0 + d * pitch:.1f}" y="{base - max(2, bar_max * n / top):.1f}" width="{bar_w}" height="{max(2, bar_max * n / top):.1f}" rx="1.5" '
        f'fill="{AMBER if d == s["busiest_day"] else FAINT}"/>'
        for d, n in enumerate(days)
    ) + "".join(
        text(bx0 + d * pitch + bar_w / 2, base + 12, "MTWTFSS"[d], 10, AMBER if d == s["busiest_day"] else MUTED, anchor="middle")
        for d in range(7)
    )
    # Meter for the night share, to the right of the value
    meter_x = x0 + tw + gap + 96
    meter_w = tw - 96 - 16
    meter = (
        f'<rect x="{meter_x:.1f}" y="{ya + 22}" width="{meter_w:.1f}" height="8" rx="4" fill="{BORDER}"/>'
        f'<rect x="{meter_x:.1f}" y="{ya + 22}" width="{max(8, meter_w * s["night_share"]):.1f}" height="8" rx="4" fill="{MUTED}"/>'
    )
    out += [
        tile(x0, ya, tw, th, f"{s['total']:,}", "COMMITS ANALYSED", TEXT, 0.05),
        tile(x0 + tw + gap, ya, tw, th, f"{round(s['night_share'] * 100)}%", "BETWEEN 20:00 AND 04:00", TEXT, 0.10, meter),
        tile(x0, yb, tw, th, f"{hhmm(s['busiest_hour'])}–{hhmm(s['busiest_hour'] + 1)}", "BUSIEST HOUR", AMBER, 0.15),
        tile(x0 + tw + gap, yb, tw, th, WEEKDAYS[s["busiest_day"]], "BUSIEST WEEKDAY", TEXT, 0.20, mini,
             value_size=22 if len(WEEKDAYS[s["busiest_day"]]) <= 8 else 18),
    ]
    return out


STYLE = """<style>
  .tile { animation: fade-up .6s ease-out both; }
  @keyframes fade-up { from { opacity: .6; transform: translateY(4px); } to { opacity: 1; transform: none; } }
  @media (prefers-reduced-motion: reduce) { * { animation: none !important; } }
</style>"""


def render(commits: list[dict], source: str, today: str) -> str:
    s = summarize(commits)
    desc = (
        f"A 24-hour clock in India Standard Time with one bar per hour, sized by how many of {s['total']} commits "
        f"from the last 12 months were made in that hour; a hand sweeps round and lights each bar. "
        f"Busiest hour {hhmm(s['busiest_hour'])} to {hhmm(s['busiest_hour'] + 1)}, "
        f"{round(s['night_share'] * 100)}% of commits between 20:00 and 04:00, busiest weekday {WEEKDAYS[s['busiest_day']]}. "
        f"Chronotype: {s['chronotype'].lower()}. Source: {source}."
    )
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="100%" role="img" aria-labelledby="t d">',
        '<title id="t">Build rhythm: when I actually commit</title>',
        f'<desc id="d">{escape(desc)}</desc>',
        STYLE,
        f'<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="16" fill="{SURFACE}" stroke="{BORDER}"/>',
        text(32, 40, "BUILD RHYTHM", 12, TEAL, spacing="3"),
        text(32, 66, "When I actually commit", 20, TEXT, family=SANS, weight="700"),
        text(868, 40, "bar length = commits in that hour (IST)", 10.5, MUTED, anchor="end"),
        *clock(s),
        *panel(s),
        text(868, 362, f"updated {today} · source: {source} · last 12 months", 10.5, MUTED, anchor="end"),
        "</svg>",
    ]
    return "\n".join(parts) + "\n"


if __name__ == "__main__":
    sys.exit(run_card("rhythm", OUT, render))
