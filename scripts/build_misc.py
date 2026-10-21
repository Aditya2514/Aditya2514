"""Render two small animated cards: the status strip under the hero and the closing contact card.

Run from the repo root:  python3 scripts/build_misc.py

  assets/strip.svg    three tiles (flagship, studying, latest win) that fade up in turn, with a thin accent
                      sweeping under each kicker
  assets/contact.svg  a terminal that types `connect --with aditya` and prints how to reach me

Both open on their finished state, so a frozen first frame, reduced motion, or a viewer without animation still
shows every word. The links themselves stay clickable as badges under the card in the README.
"""

from pathlib import Path
from xml.sax.saxutils import escape

from theme import AMBER, BORDER, FAINT, MONO, MUTED, PANEL, SANS, SURFACE, TEAL, TEXT

ASSETS = Path(__file__).resolve().parent.parent / "assets"
PERSON = "#c9d1d9"
W = 900
REDUCED = "@media (prefers-reduced-motion: reduce){*{animation:none !important}}"


def _svg(h: int, title: str, desc: str, style: str, body: list[str], defs: str = "") -> str:
    return "\n".join([
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {h}" width="100%" role="img" aria-labelledby="t d">',
        f'<title id="t">{escape(title)}</title>',
        f'<desc id="d">{escape(desc)}</desc>',
        f"<style>{style}</style>" if style else "",
        f"<defs>{defs}</defs>" if defs else "",
        *body,
        "</svg>",
    ]) + "\n"


# --------------------------------------------------------------------------- strip

TILES = [
    ("FLAGSHIP // LEXGUARD", TEAL, "AI contract review for Indian law", "130+ commits · solo · May–Aug 2026"),
    ("STUDYING // IIT MADRAS", PERSON, "BS in Data Science & Applications", "CGPA 9.0 / 10 · 2025 – 2029"),
    ("LATEST // WIN", AMBER, "Paradox DSA Triathlon, IIT Madras", "Runner-up (2nd place) · 2026"),
]
STRIP_H = 112
KICK_Y, LINE_Y, TITLE_Y, META_Y = 36, 46, 71, 93
KICK_SIZE, KICK_SPACING = 12, 3
SWEEP_S = 7.0      # one accent sweep per tile per loop
SEG = 46           # length of the bright accent segment
# Tiles are not equal thirds: the titles are ~235, ~246 and ~250 px wide at 15 px, so the dividers sit where
# each title keeps >= 24 px of air, including the last one against the card edge.
TILE_X = (32, 316, 612)
DIVIDERS = (292, 588)


def kicker_width(label: str) -> float:
    return len(label) * (KICK_SIZE * 0.6 + KICK_SPACING) - KICK_SPACING


def strip() -> str:
    style = (
        ".tile{animation:up .8s cubic-bezier(.2,.7,.2,1) both}"
        "@keyframes up{from{opacity:.7;transform:translateY(6px)}to{opacity:1;transform:none}}"
        # The accent sweep is SMIL, which the CSS rule above cannot pause, so reduced motion hides it instead
        + "@media (prefers-reduced-motion: reduce){.sw{display:none}}"
        + REDUCED
    )
    defs, body = [], [f'<rect x="0.5" y="0.5" width="899" height="{STRIP_H - 1}" rx="16" fill="{SURFACE}" stroke="{BORDER}"/>']
    for x in DIVIDERS:
        body.append(f'<line x1="{x:.1f}" y1="20" x2="{x:.1f}" y2="{STRIP_H - 20}" stroke="{BORDER}"/>')

    for i, (kick, color, title, meta) in enumerate(TILES):
        x0 = TILE_X[i]
        kw = kicker_width(kick)
        # Accent: a faint rule under the kicker, and a bright segment that sweeps along it (clipped to the rule)
        defs.append(
            f'<clipPath id="rule{i}"><rect x="{x0:.1f}" y="{LINE_Y - 1.5}" width="{kw:.1f}" height="3"/></clipPath>'
            f'<linearGradient id="seg{i}" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{color}" stop-opacity="0"/>'
            f'<stop offset="0.6" stop-color="{color}"/><stop offset="1" stop-color="{color}" stop-opacity="0"/></linearGradient>'
        )
        begin = 0.9 + i * 0.6
        frac = 1.6 / SWEEP_S   # the sweep itself takes 1.6 s, then the segment rests off the end
        sweep = (
            f'<rect class="sw" x="{x0 - SEG:.1f}" y="{LINE_Y - 1}" width="{SEG}" height="2" fill="url(#seg{i})" clip-path="url(#rule{i})">'
            f'<animate attributeName="x" values="{x0 - SEG:.1f};{x0 + kw:.1f};{x0 + kw:.1f}" keyTimes="0;{frac:.3f};1" '
            f'calcMode="spline" keySplines="0.45 0 0.25 1;0 0 1 1" dur="{SWEEP_S}s" begin="{begin:.1f}s" repeatCount="indefinite"/></rect>'
        )
        body.append(
            f'<g class="tile" style="animation-delay:{0.1 + i * 0.18:.2f}s">'
            f'<text x="{x0:.1f}" y="{KICK_Y}" font-family="{MONO}" font-size="{KICK_SIZE}" letter-spacing="{KICK_SPACING}" fill="{color}">{escape(kick)}</text>'
            f'<line x1="{x0:.1f}" y1="{LINE_Y}" x2="{x0 + kw:.1f}" y2="{LINE_Y}" stroke="{color}" stroke-opacity="0.28" stroke-width="1"/>'
            + sweep
            + f'<text x="{x0:.1f}" y="{TITLE_Y}" font-family="{SANS}" font-size="15" font-weight="700" fill="{TEXT}">{escape(title)}</text>'
            f'<text x="{x0:.1f}" y="{META_Y}" font-family="{SANS}" font-size="13" fill="{MUTED}">{escape(meta)}</text>'
            "</g>"
        )
    # Spoken form of each kicker ("FLAGSHIP // LEXGUARD" -> "Flagship: LexGuard"); str.title() would mangle the names
    spoken = ("Flagship: LexGuard", "Studying: IIT Madras", "Latest win")
    desc = " ".join(f"{k} — {t}; {m}." for k, (_, _, t, m) in zip(spoken, TILES))
    return _svg(STRIP_H, "Now: flagship project, studies, latest win", desc, style, body, "".join(defs))


# --------------------------------------------------------------------------- contact

CONTACT_H = 212
X0, FONT = 32, 15
CHAR_W = FONT * 0.6   # textLength pins every glyph to this advance, whatever mono font loads
COMMAND = "connect --with aditya"
# (y, runs) — runs are (text, colour); the prompt row is first, the pitch line last
ROWS = [
    (78, [("$ ", TEAL), (COMMAND, TEXT)]),
    (106, [("→ ", FAINT), ("linkedin.com/in/aditya-singh-8286b137a", TEAL)]),
    (130, [("→ ", FAINT), ("adityasinghv05@gmail.com", TEAL)]),
    (154, [("→ ", FAINT), ("github.com/Aditya2514", TEAL)]),
    (186, [("Open to ", TEXT), ("AI engineering internships", AMBER), (" with teams building ", TEXT), ("agents", TEAL), (".", TEXT)]),
]
TYPE_S, PITCH_S = 0.075, 0.028   # per character: the command, then the pitch line
HOLD_S, CLEAR_S, THINK_S, OUT_S, BLINK_S = 4.0, 0.6, 0.35, 0.18, 0.5


def _discrete(attr, frames, cycle, fmt="{:.1f}"):
    times = ";".join(f"{min(t / cycle, 1):.5f}" for t, _ in frames)
    values = ";".join(fmt.format(v) for _, v in frames)
    return (
        f'<animate attributeName="{attr}" calcMode="discrete" dur="{cycle:.3f}s" repeatCount="indefinite" '
        f'keyTimes="{times}" values="{values}"/>'
    )


def contact() -> str:
    lens = [sum(len(s) for s, _ in runs) for _, runs in ROWS]
    last = len(ROWS) - 1
    shown = {r: [(0.0, lens[r])] for r in range(len(ROWS))}
    cur = [(0.0, (last, lens[last]))]  # (row, column) of the cursor
    blink = [(0.0, 1)]
    t = 0.0

    def idle(duration):
        nonlocal t
        steps = int(duration / BLINK_S)
        for s in range(1, steps + 1):
            if s * BLINK_S < duration:
                blink.append((t + s * BLINK_S, 0 if s % 2 else 1))
        t += duration
        blink.append((t, 1))

    idle(HOLD_S)                               # finished card, cursor blinking after the pitch
    for r in range(len(ROWS)):                 # clear: only the "$ " prompt is left
        shown[r].append((t, 2 if r == 0 else 0))
    cur.append((t, (0, 2)))
    idle(CLEAR_S)
    for k in range(3, lens[0] + 1):            # type the command
        t += TYPE_S
        shown[0].append((t, k))
        cur.append((t, (0, k)))
    t += THINK_S
    for r in range(1, last):                   # print the three links
        shown[r].append((t, lens[r]))
        cur.append((t, (r + 1, 0)))
        t += OUT_S
    for k in range(1, lens[last] + 1):         # the pitch line types out
        t += PITCH_S
        shown[last].append((t, k))
        cur.append((t, (last, k)))
    idle(BLINK_S * 4)
    cycle = t
    for r in shown:
        shown[r].append((cycle, shown[r][0][1]))
    cur.append((cycle, cur[0][1]))
    blink.append((cycle, 1))

    clips, texts, still = [], [], []
    for r, (y, runs) in enumerate(ROWS):
        n = lens[r]
        clips.append(
            f'<clipPath id="row{r}"><rect x="{X0 - 1}" y="{y - 17}" width="{n * CHAR_W + 2:.1f}" height="24">'
            + _discrete("width", [(tt, k * CHAR_W + (1 if k else 0)) for tt, k in shown[r]], cycle)
            + "</rect></clipPath>"
        )
        spans = "".join(f'<tspan fill="{c}">{escape(s)}</tspan>' for s, c in runs)
        weight = ' font-weight="700"' if r == 0 else ""
        common = (
            f'xml:space="preserve" font-family="{MONO}" font-size="{FONT}"{weight} '
            f'textLength="{n * CHAR_W:.1f}" lengthAdjust="spacingAndGlyphs" fill="{TEXT}">{spans}</text>'
        )
        texts.append(f'<text x="{X0}" y="{y}" clip-path="url(#row{r})" ' + common)
        still.append(f'<text x="{X0}" y="{y}" ' + common)
    ys = [y for y, _ in ROWS]
    cursor = (
        f'<rect x="{X0 + lens[last] * CHAR_W + 2:.1f}" y="{ys[last] - 14}" width="{CHAR_W:.1f}" height="18" rx="1.5" fill="{TEAL}" opacity="0.9">'
        + _discrete("x", [(tt, X0 + c * CHAR_W + (2 if c else 0)) for tt, (_, c) in cur], cycle)
        + _discrete("y", [(tt, ys[r] - 14) for tt, (r, _) in cur], cycle)
        + _discrete("opacity", blink, cycle, "{:d}")
        + "</rect>"
    )
    # Typing is SMIL, which prefers-reduced-motion CSS cannot pause: reduced motion swaps in the finished screen
    style = ".still{display:none}@media (prefers-reduced-motion: reduce){.live{display:none}.still{display:inline}}" + REDUCED
    still.append(
        f'<rect x="{X0 + lens[last] * CHAR_W + 2:.1f}" y="{ys[last] - 14}" width="{CHAR_W:.1f}" height="18" rx="1.5" fill="{TEAL}" opacity="0.9"/>'
    )
    chrome = [
        f'<rect x="0.5" y="0.5" width="{W - 1}" height="{CONTACT_H - 1}" rx="16" fill="{SURFACE}" stroke="{BORDER}"/>',
        f'<path d="M0.5,40 V16.5 A16,16 0 0 1 16.5,0.5 H{W - 16.5} A16,16 0 0 1 {W - 0.5},16.5 V40 Z" fill="{PANEL}"/>',
        f'<line x1="0.5" y1="40.5" x2="{W - 0.5}" y2="40.5" stroke="{BORDER}"/>',
        "".join(f'<circle cx="{x}" cy="20.5" r="5.5" fill="{FAINT}"/>' for x in (26, 46, 66)),
        f'<text x="{W / 2}" y="25" text-anchor="middle" font-family="{MONO}" font-size="12" fill="{MUTED}">~/aditya — connect</text>',
        f'<text x="{W - 24}" y="25" text-anchor="end" font-family="{MONO}" font-size="11" fill="{MUTED}">clickable links below ↓</text>',
    ]
    desc = (
        f"A terminal types: {COMMAND}. It prints linkedin.com/in/aditya-singh-8286b137a, adityasinghv05@gmail.com and "
        "github.com/Aditya2514, then: Open to AI engineering internships with teams building agents."
    )
    body = chrome + ["<defs>" + "".join(clips) + "</defs>", '<g class="live">', *texts, cursor, "</g>",
                     '<g class="still">', *still, "</g>"]
    return _svg(CONTACT_H, "Contact: connect with Aditya", desc, style, body)


if __name__ == "__main__":
    for name, fn in (("strip", strip), ("contact", contact)):
        out = ASSETS / f"{name}.svg"
        out.write_text(fn())
        print(f"wrote {out} ({out.stat().st_size / 1024:.1f} KB)")
