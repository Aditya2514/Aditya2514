"""Render assets/journey.svg: an animated month-by-month timeline, Aug 2025 to today.

Run from the repo root:  python3 scripts/build_journey.py

A progress line draws itself from left to right and each event lights up as the line reaches it, then the
finished timeline holds before the loop restarts. The loop starts on the finished state, so a frozen first
frame (thumbnails, GitHub mobile, prefers-reduced-motion) shows the whole timeline.

Repo dots sit on each repo's first commit (checked with `git log` in local clones); labels show only the month.
"""

from datetime import date
from pathlib import Path
from xml.sax.saxutils import escape

from theme import AMBER, BORDER, FAINT, MONO, MUTED, PANEL, SANS, SURFACE, TEAL, TEXT

OUT = Path(__file__).resolve().parent.parent / "assets" / "journey.svg"

W, H = 900, 322
AXIS_Y = 214
START, NOW = date(2025, 8, 1), date(2026, 10, 21)   # left end of the month axis, right end (today)
XA, XB = 150, 842                                    # axis pixels for START and NOW
START_MARK_X = 44                                    # "May 2025" marker, left of the axis (not to scale)

# Loop timing (seconds)
T = 12.0
DIM_FROM, DIM_TO = 1.2, 1.7      # finished state fades back to "not yet reached"
DRAW_FROM, DRAW_TO = 1.9, 5.9    # the progress line travels XA -> XB
POP = 0.35                       # how long a dot takes to pop in

UP_LANES = {1: 184, 2: 154, 3: 124, 4: 94}           # name baselines above the axis
DOWN_LANES = {1: AXIS_Y + 44, 2: AXIS_Y + 72}        # name baselines below the axis
SUB_DY = 13

# kind: start | flag (TEAL flagship) | amber (hackathon) | small
EVENTS = [
    dict(key="iit", at=None, kind="start", side="up", lane=3, anchor="start",
         name="IIT Madras · BS in Data Science", sub="May 2025 · co-enrolled at Scaler School of Technology"),
    dict(key="gh", at=date(2025, 8, 6), kind="small", side="down", lane=2, anchor="start",
         name="GitHub account", sub="Aug 2025"),
    dict(key="pf", at=date(2025, 10, 5), kind="small", side="down", lane=1, anchor="start",
         name="First public repo", sub="Oct 2025 · portfolio"),
    dict(key="nk", at=date(2026, 3, 18), kind="small", side="down", lane=1, anchor="start",
         name="Naukri · Fintrac", sub="Mar 2026", extra_dots=[date(2026, 3, 27)]),
    dict(key="oe", at=date(2026, 4, 3), kind="amber", side="up", lane=1, anchor="end",
         name="Meta PyTorch OpenEnv Hackathon", sub="Apr 2026 · planner RL environment · team of 2"),
    dict(key="bf", at=date(2026, 5, 11), kind="small", side="up", lane=2, anchor="end",
         name="BookFinder", sub="May 2026 · React Native + TS"),
    dict(key="lg", at=date(2026, 5, 17), until=date(2026, 8, 22), kind="flag", side="up", lane=4, anchor="start",
         name="LexGuard", sub="May – Aug 2026"),
    dict(key="sh", at=date(2026, 6, 15), kind="small", side="down", lane=1, anchor="start",
         name="POSIX shell in C++", sub="Jun 2026"),
    dict(key="pk", at=date(2026, 7, 5), kind="flag", side="up", lane=3, anchor="start",
         name="Pikina", sub="Jul 2026"),
    dict(key="rs", at=date(2026, 7, 20), kind="flag", side="up", lane=2, anchor="start",
         name="Resilion", sub="Jul 2026"),
    dict(key="no", at=date(2026, 8, 23), kind="flag", side="up", lane=1, anchor="start",
         name="Noesis", sub="Aug 2026 · team of 2"),
    dict(key="sk", at=date(2026, 9, 9), until=date(2026, 10, 15), kind="small", side="down", lane=2, anchor="end",
         name="ShopKart", sub="Sep – Oct 2026 · team of 2", leader_at="until"),
]

MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def x_of(d: date) -> float:
    return XA + (XB - XA) * (d - START).days / (NOW - START).days


def t_of(x: float) -> float:
    """Second (within the loop) at which the drawing line reaches pixel x."""
    return DRAW_FROM + (DRAW_TO - DRAW_FROM) * (x - XA) / (XB - XA)


def pct(t: float) -> str:
    return f"{100 * t / T:.2f}%"


def text(x, y, s, size, fill, family=MONO, anchor="start", weight=None, spacing=None, extra=""):
    attrs = f'x="{x:.1f}" y="{y:.1f}" font-family="{family}" font-size="{size}" fill="{fill}"'
    if anchor != "start":
        attrs += f' text-anchor="{anchor}"'
    if weight:
        attrs += f' font-weight="{weight}"'
    if spacing:
        attrs += f' letter-spacing="{spacing}"'
    return f"<text {attrs}{extra}>{escape(s)}</text>"


def est_width(s: str, size: float, family: str, bold=False) -> float:
    """Rough rendered width; used only to assert that labels in a lane don't collide."""
    em = 0.6 if family == MONO else (0.58 if bold else 0.54)
    return len(s) * size * em


# ---------------------------------------------------------------------------- animation (CSS keyframes)

keyframes: list[str] = []


def lit_keyframes(name: str, t_hit: float, lit: str, dim: str, overshoot: str | None = None) -> None:
    """Lit at t=0, dims with everything else, re-lights when the line reaches it, holds to the loop end."""
    steps = [(0, lit), (DIM_FROM, lit), (DIM_TO, dim), (t_hit, dim)]
    if overshoot:
        steps += [(t_hit + POP * 0.45, overshoot), (t_hit + POP, lit)]
    else:
        steps += [(t_hit + POP, lit)]
    steps.append((T, lit))
    body = " ".join(f"{pct(t)} {{ {css} }}" for t, css in steps)
    keyframes.append(f"@keyframes {name} {{ {body} }}")


def ripple_keyframes(name: str, t_hit: float) -> None:
    off = "opacity: 0; transform: scale(1)"
    body = (
        f"0% {{ {off} }} {pct(t_hit - 0.02)} {{ {off} }} {pct(t_hit)} {{ opacity: .8; transform: scale(1) }} "
        f"{pct(t_hit + 0.9)} {{ opacity: 0; transform: scale(3.2) }} 100% {{ {off} }}"
    )
    keyframes.append(f"@keyframes {name} {{ {body} }}")


def grow_keyframes(name: str, t0: float, t1: float) -> None:
    # Fades out with everything else (no reverse wipe), resets while invisible, then grows with the line
    body = (
        f"0% {{ transform: scaleX(1); opacity: 1 }} {pct(DIM_FROM)} {{ transform: scaleX(1); opacity: 1 }} "
        f"{pct(DIM_TO)} {{ transform: scaleX(1); opacity: 0 }} {pct(DIM_TO + 0.01)} {{ transform: scaleX(0); opacity: 0 }} "
        f"{pct(t0)} {{ transform: scaleX(0); opacity: 1 }} "
        f"{pct(t1)} {{ transform: scaleX(1); opacity: 1 }} 100% {{ transform: scaleX(1); opacity: 1 }}"
    )
    keyframes.append(f"@keyframes {name} {{ {body} }}")


def anim(name: str, timing="ease-out") -> str:
    return f' style="animation: {name} {T:g}s {timing} infinite"'


# ---------------------------------------------------------------------------- drawing

def axis() -> tuple[list[str], list[str]]:
    """Returns (axis line + ticks, month labels); labels are painted later, over the leaders."""
    out, labels = [], []
    # Lead-in from the May 2025 start marker: dashed and broken, because it is not to scale
    out.append(f'<line x1="{START_MARK_X}" y1="{AXIS_Y}" x2="{XA}" y2="{AXIS_Y}" stroke="{FAINT}" stroke-width="2" stroke-dasharray="3 5"/>')
    bx = (START_MARK_X + XA) / 2 + 6
    for dx in (-3, 3):
        out.append(f'<line x1="{bx + dx - 3:.1f}" y1="{AXIS_Y + 7}" x2="{bx + dx + 3:.1f}" y2="{AXIS_Y - 7}" stroke="{MUTED}" stroke-width="1.5"/>')
    # Base axis
    out.append(f'<line x1="{XA}" y1="{AXIS_Y}" x2="{XB}" y2="{AXIS_Y}" stroke="{BORDER}" stroke-width="3" stroke-linecap="round"/>')
    # Month ticks at the 1st of each month, labels centred in the month; the year replaces "Aug"/"Jan"
    y, m = START.year, START.month
    while date(y, m, 1) <= NOW:
        x0 = x_of(date(y, m, 1))
        ny, nm = (y + (m == 12), m % 12 + 1)
        x1 = min(x_of(date(ny, nm, 1)), XB)
        major = m in (1, 8) and (y, m) != (2026, 8)
        out.append(f'<line x1="{x0:.1f}" y1="{AXIS_Y - (6 if major else 4)}" x2="{x0:.1f}" y2="{AXIS_Y + (6 if major else 4)}" stroke="{MUTED if major else FAINT}" stroke-width="1"/>')
        label = str(y) if major else MONTHS[m - 1]
        labels.append(text((x0 + x1) / 2, AXIS_Y + 20, label, 10.5, TEXT if major else MUTED, anchor="middle",
                        weight="700" if major else None,
                        extra=f' stroke="{SURFACE}" stroke-width="5" paint-order="stroke"'))
        y, m = ny, nm
    return out, labels


def progress() -> list[str]:
    length = XB - XA
    body = (
        f"0% {{ stroke-dashoffset: 0; opacity: 1 }} {pct(DIM_FROM)} {{ stroke-dashoffset: 0; opacity: 1 }} "
        f"{pct(DIM_TO)} {{ stroke-dashoffset: 0; opacity: 0 }} {pct(DIM_TO + 0.01)} {{ stroke-dashoffset: {length}; opacity: 0 }} "
        f"{pct(DRAW_FROM)} {{ stroke-dashoffset: {length}; opacity: 1 }} {pct(DRAW_TO)} {{ stroke-dashoffset: 0; opacity: 1 }} "
        f"100% {{ stroke-dashoffset: 0; opacity: 1 }}"
    )
    keyframes.append(f"@keyframes draw {{ {body} }}")
    head = (
        f"0% {{ transform: translateX(0) }} {pct(DIM_TO)} {{ transform: translateX(0) }} "
        f"{pct(DIM_TO + 0.01)} {{ transform: translateX({-length}px) }} {pct(DRAW_FROM)} {{ transform: translateX({-length}px) }} "
        f"{pct(DRAW_TO)} {{ transform: translateX(0) }} 100% {{ transform: translateX(0) }}"
    )
    keyframes.append(f"@keyframes head {{ {head} }}")
    return [
        f'<line x1="{XA}" y1="{AXIS_Y}" x2="{XB}" y2="{AXIS_Y}" stroke="{TEAL}" stroke-width="3" stroke-linecap="round" '
        f'stroke-dasharray="{length} {length}" opacity="0.85"{anim("draw", "linear")}/>',
    ]


def head() -> list[str]:
    """The moving tip of the progress line; at rest it marks the build date and breathes slowly."""
    return [
        f'<g{anim("head", "linear")}>'
        f'<circle class="breathe" cx="{XB}" cy="{AXIS_Y}" r="6" fill="none" stroke="{TEAL}" stroke-width="1.5"/>'
        f'<circle cx="{XB}" cy="{AXIS_Y}" r="4" fill="{TEXT}"/></g>',
        text(XB + 11, AXIS_Y + 3.5, f"{NOW:%b} {NOW.day}", 10, MUTED),
    ]


def event(e: dict, i: int) -> tuple[list[str], list[str]]:
    """Returns (behind, front): leaders/labels behind the axis, dots in front of it."""
    behind, front = [], []
    big = e["kind"] in ("flag", "amber", "start")
    color = {"flag": TEAL, "amber": AMBER, "start": TEAL, "small": MUTED}[e["kind"]]
    x = START_MARK_X if e["at"] is None else x_of(e["at"])
    t_hit = DIM_TO + 0.05 if e["at"] is None else t_of(x)
    lx = x_of(e["until"]) if e.get("leader_at") == "until" else x

    # Duration bar (active commit span)
    if e.get("until"):
        x1 = x_of(e["until"])
        h = 9 if big else 7
        grow_keyframes(f"g{i}", t_hit, t_of(x1))
        front.append(f'<rect x="{x:.1f}" y="{AXIS_Y - h / 2}" width="{x1 - x:.1f}" height="{h}" rx="{h / 2}" fill="{color}" opacity="0.18"/>')
        front.append(f'<rect class="bar" x="{x:.1f}" y="{AXIS_Y - h / 2}" width="{x1 - x:.1f}" height="{h}" rx="{h / 2}" '
                     f'fill="{color}" fill-opacity="{0.9 if big else 0.75}"{anim(f"g{i}", "linear")}/>')

    # Leader + label
    up = e["side"] == "up"
    base = (UP_LANES if up else DOWN_LANES)[e["lane"]]
    top_y = base - 11
    if up:
        y0, y1 = AXIS_Y - (8 if big else 5), top_y
    else:
        y0, y1 = AXIS_Y + (8 if big else 5), base + SUB_DY + 3
    t_lab = t_hit if lx == x else t_of(lx)
    lit_keyframes(f"l{i}", t_lab, "opacity: 1", "opacity: .28")
    anchor = e["anchor"]
    tx = lx + 6 if anchor == "start" else lx - 6
    name_size, name_fill = (13, TEXT) if big else (12, MUTED)
    if e["kind"] == "amber":
        name_fill = AMBER
    behind.append(
        f'<g{anim(f"l{i}")}>'
        f'<line x1="{lx:.1f}" y1="{y0}" x2="{lx:.1f}" y2="{y1}" stroke="{color if big else FAINT}" stroke-width="1" '
        f'opacity="{0.6 if big else 1}"/>'
        + text(tx, base, e["name"], name_size, name_fill, family=SANS, anchor=anchor, weight="700" if big else "600")
        + text(tx, base + SUB_DY, e["sub"], 10.5, MUTED, anchor=anchor)
        + "</g>"
    )
    if lx != x:   # leader hangs off the end of a bar; mark that end
        front.append(f'<circle cx="{lx:.1f}" cy="{AXIS_Y}" r="2" fill="{TEXT}" opacity=".6"/>')

    # Dots
    r = 6.5 if big else 4
    if big:
        ripple_keyframes(f"r{i}", t_hit)
        front.append(f'<circle class="pop" cx="{x:.1f}" cy="{AXIS_Y}" r="{r}" fill="none" stroke="{color}" stroke-width="1.5" '
                     f'opacity="0"{anim(f"r{i}")}/>')
    lit_keyframes(f"d{i}", t_hit, "opacity: 1; transform: scale(1)", "opacity: .35; transform: scale(.55)",
                  overshoot="opacity: 1; transform: scale(1.6)")
    fill = SURFACE if e["kind"] == "start" else color
    front.append(f'<circle class="pop" cx="{x:.1f}" cy="{AXIS_Y}" r="{r}" fill="{fill}" stroke="{color if e["kind"] == "start" else SURFACE}" '
                 f'stroke-width="2"{anim(f"d{i}")}/>')
    for j, d in enumerate(e.get("extra_dots", [])):
        xe = x_of(d)
        lit_keyframes(f"d{i}x{j}", t_of(xe), "opacity: 1; transform: scale(1)", "opacity: .35; transform: scale(.55)",
                      overshoot="opacity: 1; transform: scale(1.6)")
        front.append(f'<circle class="pop" cx="{xe:.1f}" cy="{AXIS_Y}" r="{r}" fill="{color}" stroke="{SURFACE}" '
                     f'stroke-width="2"{anim(f"d{i}x{j}")}/>')
    return behind, front


def check_layout() -> None:
    """Fail loudly if two labels in a lane overlap, or a leader runs through another lane's label."""
    boxes = []
    for e in EVENTS:
        x = START_MARK_X if e["at"] is None else x_of(e["at"])
        lx = x_of(e["until"]) if e.get("leader_at") == "until" else x
        big = e["kind"] != "small"
        w = max(est_width(e["name"], 13 if big else 12, SANS, True), est_width(e["sub"], 10.5, MONO))
        x0, x1 = (lx + 6, lx + 6 + w) if e["anchor"] == "start" else (lx - 6 - w, lx - 6)
        assert 16 <= x0 and x1 <= W - 16, f"{e['key']} label leaves the card: {x0:.0f}..{x1:.0f}"
        boxes.append((e, lx, x0, x1))
    for a, la, a0, a1 in boxes:
        for b, lb, b0, b1 in boxes:
            if a is b or a["side"] != b["side"]:
                continue
            if a["lane"] == b["lane"] and a0 < b1 + 6 and b0 < a1 + 6 and a["key"] < b["key"]:
                raise AssertionError(f"labels {a['key']} and {b['key']} overlap")
            if b["lane"] < a["lane"] and b0 - 4 <= la <= b1 + 4:
                raise AssertionError(f"leader of {a['key']} crosses label {b['key']}")


def badge(x_right: float, y: float, parts: list[tuple[str, str]]) -> tuple[str, float]:
    """A pill right-aligned at x_right; parts are (text, colour) runs in MONO 11."""
    size, pad = 11, 12
    full = "".join(p for p, _ in parts)
    w = est_width(full, size, MONO) + 2 * pad
    x = x_right - w
    spans = "".join(f'<tspan fill="{c}">{escape(p)}</tspan>' for p, c in parts)
    return (
        f'<g><rect x="{x:.1f}" y="{y}" width="{w:.1f}" height="24" rx="12" fill="{PANEL}" stroke="{BORDER}"/>'
        f'<text x="{x + pad:.1f}" y="{y + 16}" font-family="{MONO}" font-size="{size}" fill="{TEXT}">{spans}</text></g>',
        x,
    )


STYLE_STATIC = """
  .pop { transform-box: fill-box; transform-origin: center; }
  .bar { transform-box: fill-box; transform-origin: 0 50%; }
  .breathe { transform-box: fill-box; transform-origin: center; animation: breathe 3s ease-in-out infinite; }
  @keyframes breathe { 0%, 100% { opacity: .9; transform: scale(1); } 50% { opacity: .2; transform: scale(1.8); } }
  @media (prefers-reduced-motion: reduce) { * { animation: none !important; } }"""


def render() -> str:
    check_layout()
    keyframes.clear()
    behind, front = [], []
    for i, e in enumerate(EVENTS):
        b, f = event(e, i)
        behind += b
        front += f
    line = progress()
    axis_lines, month_labels = axis()
    tip = head()

    b1, bx = badge(W - 32, 28, [("2026 · ", MUTED), ("Runner-up", AMBER), (" · Paradox DSA Triathlon, IIT Madras", TEXT)])
    b2, _ = badge(bx - 8, 28, [("CGPA ", MUTED), ("9.0", TEAL), (" / 10", MUTED)])

    desc = (
        "A timeline from August 2025 to October 2026. A line draws itself left to right and each milestone lights up "
        "as it is reached. Start: May 2025, BS in Data Science and Applications at IIT Madras, co-enrolled at Scaler "
        "School of Technology. August 2025: GitHub account created. October 2025: first public repo (portfolio). "
        "March 2026: Naukri and Fintrac. April 2026: Meta PyTorch OpenEnv Hackathon, a planner RL environment built by a "
        "team of 2. May 2026: BookFinder (React Native and TypeScript); LexGuard starts and runs to August 2026. "
        "June 2026: a POSIX shell in C++. July 2026: Pikina, then Resilion. August 2026: Noesis (team of 2). "
        "September to October 2026: ShopKart (team of 2). Also: runner-up at the Paradox DSA Triathlon, IIT Madras, "
        "2026; CGPA 9.0 out of 10."
    )
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="100%" role="img" aria-labelledby="t d">',
        '<title id="t">Journey: fourteen months of building, Aug 2025 to Oct 2026</title>',
        f'<desc id="d">{escape(desc)}</desc>',
        "<style>" + STYLE_STATIC + "\n  " + "\n  ".join(keyframes) + "\n</style>",
        f'<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="16" fill="{SURFACE}" stroke="{BORDER}"/>',
        text(32, 40, "JOURNEY", 12, TEAL, spacing="3"),
        text(32, 66, "Fourteen months of building", 20, TEXT, family=SANS, weight="700"),
        b2,
        b1,
        *axis_lines,
        *behind,
        *month_labels,
        *line,
        *front,
        *tip,
        text(32, 90, "dot = when it started · bar = span of commits · labels give the month", 10.5, MUTED),
        "</svg>",
    ]
    return "\n".join(parts) + "\n"


if __name__ == "__main__":
    OUT.write_text(render(), encoding="utf-8")
    print(f"wrote {OUT} ({OUT.stat().st_size / 1024:.1f} KB)")
