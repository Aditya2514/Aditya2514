"""Render the profile's static SVGs: the hero banner and the "how I build" board.

Run from the repo root:  python3 scripts/build_static.py
"""

from pathlib import Path
from xml.sax.saxutils import escape

from theme import AMBER, BORDER, FAINT, MONO, MUTED, PANEL, SANS, SURFACE, TEAL, TEXT, wrap

ASSETS = Path(__file__).resolve().parent.parent / "assets"

PERSON = "#c9d1d9"

PATTERN_ROWS = [
    {
        "name": "LexGuard",
        "stack": "Node · React · MongoDB Atlas",
        "cells": [
            "Risk analyst + adversarial judge rate every clause",
            "36 trap patterns + cross-clause contradiction rules",
            "Signer reviews ratings, cited statutes, rewrites",
        ],
    },
    {
        "name": "Resilion",
        "stack": "Python · NetworkX · Gemini",
        "cells": [
            "Risk Watcher agent turns news into disruption events",
            "Graph traversal traces which industries are hit",
            "Reroutes will need sign-off (approval console planned)",
        ],
    },
    {
        "name": "Pikina",
        "stack": "Python · Ollama · Electron",
        "cells": [
            "Local Ollama parses intent when regex routes miss",
            "Validation layer checks every model-proposed action",
            "Native consent popup before any level-4+ action",
        ],
    },
    {
        "name": "Noesis",
        "stack": "Python · Groq · ChromaDB",
        "cells": [
            "gpt-oss on Groq drafts the answer in one grounded pass",
            "Hybrid BM25 + dense retrieval with reranking",
            "Answers cite the timestamp, page or frame used",
        ],
    },
]


GREEN = "#3fb950"

# Typed under the name, one at a time. Each phrase is a list of (text, colour) runs.
HERO_PHRASES = [
    [("I build ", TEXT), ("LLM agents", TEAL), (" that are ", TEXT), ("safe to act on", AMBER)],
    [("checked by ", TEXT), ("deterministic code", AMBER)],
    [("grounded by ", TEXT), ("retrieval", TEAL)],
    [("approved by ", TEXT), ("a person", PERSON), (" before anything irreversible", TEXT)],
]
TYPE_FONT = 18
CHAR_W = TYPE_FONT * 0.6  # textLength pins every glyph to this advance, whatever mono font loads
TYPE_S, DELETE_S, GAP_S = 0.04, 0.015, 0.25
# Per-phrase hold once fully typed: the headline (shown at load) stays longest; longer phrases get more reading time.
HOLD_S = (2.2, 1.3, 1.2, 2.0)
BLINK_S = 0.5


def _typing_timeline():
    """Return (cycle length, per-phrase visible-char keyframes, caret x keyframes, caret opacity keyframes).

    The cycle opens on phrase 0 fully typed, so a frozen first frame still reads as a sentence,
    and closes by re-typing phrase 0 so the loop is seamless.
    """
    lens = [sum(len(t) for t, _ in ph) for ph in HERO_PHRASES]
    x0 = [450 - n * CHAR_W / 2 for n in lens]
    widths = [[(0.0, lens[0] if i == 0 else 0)] for i in range(len(lens))]
    caret_x = [(0.0, x0[0] + lens[0] * CHAR_W)]
    caret_on = [(0.0, 1)]
    t = 0.0

    def hold(i):
        nonlocal t
        steps = int(HOLD_S[i] / BLINK_S)
        for s in range(1, steps + 1):
            if s * BLINK_S < HOLD_S[i]:
                caret_on.append((t + s * BLINK_S, 0 if s % 2 else 1))
        t += HOLD_S[i]
        caret_on.append((t, 1))

    def step(i, k, dt):
        nonlocal t
        t += dt
        widths[i].append((t, k))
        caret_x.append((t, x0[i] + k * CHAR_W))

    order = list(range(len(lens)))
    for n, i in enumerate(order):
        hold(i)
        for k in range(lens[i] - 1, -1, -1):
            step(i, k, DELETE_S)
        nxt = order[(n + 1) % len(order)]
        t += GAP_S
        caret_x.append((t, x0[nxt]))
        for k in range(1, lens[nxt] + 1):
            step(nxt, k, TYPE_S)
    return t, lens, x0, widths, caret_x, caret_on


def _discrete(attr, frames, cycle, fmt="{:.1f}"):
    """One looping SMIL animation that steps through (time, value) keyframes."""
    times = ";".join(f"{tt / cycle:.5f}" for tt, _ in frames)
    values = ";".join(fmt.format(v) for _, v in frames)
    return f'<animate attributeName="{attr}" calcMode="discrete" dur="{cycle:.3f}s" repeatCount="indefinite" keyTimes="{times}" values="{values}"/>'


def hero() -> str:
    H = 330
    cycle, lens, x0, widths, caret_x, caret_on = _typing_timeline()
    type_y = 160

    # --- typing line: one <text> per phrase, each revealed by its own clip rect ---
    clips, typed = [], []
    for i, phrase in enumerate(HERO_PHRASES):
        w0 = widths[i][0][1] * CHAR_W
        clips.append(
            f'<clipPath id="type{i}"><rect x="{x0[i] - 2:.1f}" y="{type_y - 20}" width="{w0 + 2:.1f}" height="28">'
            + _discrete("width", [(tt, k * CHAR_W + 2 if k else 0) for tt, k in widths[i]], cycle)
            + "</rect></clipPath>"
        )
        runs = "".join(f'<tspan fill="{c}">{escape(txt)}</tspan>' for txt, c in phrase)
        typed.append(
            f'<text x="{x0[i]:.1f}" y="{type_y}" clip-path="url(#type{i})" font-family="{MONO}" font-size="{TYPE_FONT}" '
            f'textLength="{lens[i] * CHAR_W:.1f}" lengthAdjust="spacingAndGlyphs" fill="{TEXT}">{runs}</text>'
        )
    caret = (
        f'<rect x="{caret_x[0][1] + 2:.1f}" y="{type_y - 16}" width="2.5" height="21" rx="1" fill="{TEAL}">'
        + _discrete("x", [(tt, x + 2) for tt, x in caret_x], cycle)
        + _discrete("opacity", caret_on, cycle, "{:d}")
        + "</rect>"
    )

    # --- pipeline: MODEL -> VERIFY -> PERSON with a travelling pulse ---
    py, ph, pw = 196, 34, 132
    cy = py + ph / 2
    nodes = [
        (250, "MODEL", TEAL, "drafts the answer"),
        (450, "VERIFY", AMBER, "rules and tests check it"),
        (650, "PERSON", PERSON, "signs off on the action"),
    ]
    period, travel = 5.0, 4.2
    x_start, x_end = nodes[0][0] - pw / 2, nodes[-1][0] + pw / 2

    def at(cx):  # fraction of the pulse cycle when the pulse is at x = cx
        return (cx - x_start) / (x_end - x_start) * travel / period

    links = []
    for n, ((ax, _, ca, _), (bx, _, cb, _)) in enumerate(zip(nodes, nodes[1:])):
        x1, x2 = ax + pw / 2 + 4, bx - pw / 2 - 4
        links.append(
            f'<linearGradient id="link{n}" gradientUnits="userSpaceOnUse" x1="{x1}" y1="0" x2="{x2}" y2="0">'
            f'<stop offset="0" stop-color="{ca}"/><stop offset="1" stop-color="{cb}"/></linearGradient>'
        )
    link_svg = []
    for n, ((ax, *_), (bx, *_)) in enumerate(zip(nodes, nodes[1:])):
        x1, x2 = ax + pw / 2 + 4, bx - pw / 2 - 4
        d = f"M{x1},{cy} H{x2} M{x2 - 6},{cy - 5} L{x2},{cy} L{x2 - 6},{cy + 5}"
        # Faint rail is always there (first frame shows the whole pipeline); the coloured stroke draws in once.
        link_svg.append(f'<path d="{d}" fill="none" stroke="{FAINT}" stroke-width="1.5"/>')
        link_svg.append(
            f'<path d="{d}" fill="none" stroke="url(#link{n})" stroke-width="2" stroke-linecap="round" '
            f'pathLength="100" stroke-dasharray="100" stroke-dashoffset="100">'
            f'<animate attributeName="stroke-dashoffset" from="100" to="0" dur="0.9s" begin="{0.4 + n * 0.7:.1f}s" fill="freeze"/></path>'
        )

    node_svg = []
    for cx, label, color, caption in nodes:
        node_svg.append(
            f'<rect x="{cx - pw / 2}" y="{py}" width="{pw}" height="{ph}" rx="17" fill="{PANEL}" stroke="{color}" stroke-width="1.5"/>'
            f'<text x="{cx}" y="{py + 22}" text-anchor="middle" font-family="{MONO}" font-size="12" font-weight="700" letter-spacing="2" fill="{color}">{label}</text>'
            f'<text x="{cx}" y="{py + 58}" text-anchor="middle" font-family="{SANS}" font-size="12" fill="{MUTED}">{caption}</text>'
        )
        k = at(cx)
        # Each stage lights up as the pulse reaches it
        node_svg.append(
            f'<rect x="{cx - pw / 2}" y="{py}" width="{pw}" height="{ph}" rx="17" fill="{color}" opacity="0">'
            f'<animate attributeName="opacity" values="0;0;0.22;0;0" keyTimes="0;{k - 0.06:.3f};{k:.3f};{k + 0.12:.3f};1" '
            f'dur="{period}s" repeatCount="indefinite"/></rect>'
        )
    # Green tick on VERIFY once the pulse has passed through it
    kv = at(nodes[1][0])
    tick_x, tick_y = nodes[1][0] + pw / 2 - 8, py
    tick = (
        f'<g opacity="0"><circle cx="{tick_x}" cy="{tick_y}" r="8" fill="{GREEN}" stroke="{SURFACE}" stroke-width="2"/>'
        f'<path d="M{tick_x - 3.5},{tick_y} L{tick_x - 1},{tick_y + 2.6} L{tick_x + 3.6},{tick_y - 2.6}" fill="none" stroke="{SURFACE}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>'
        f'<animate attributeName="opacity" values="0;0;1;1;0;0" keyTimes="0;{kv:.3f};{kv + 0.04:.3f};{travel / period:.3f};{travel / period + 0.1:.3f};1" dur="{period}s" repeatCount="indefinite"/></g>'
    )
    k0, k1, k2, kend = at(nodes[0][0]), at(nodes[1][0]), at(nodes[2][0]), travel / period
    pulse_fill = (
        f'<animate attributeName="fill" values="{TEAL};{TEAL};{AMBER};{PERSON};{PERSON}" '
        f'keyTimes="0;{k0:.3f};{k1:.3f};{k2:.3f};1" dur="{period}s" repeatCount="indefinite"/>'
    )
    pulse = (
        f'<g opacity="0">'
        f'<animateMotion path="M{x_start},{cy} L{x_end},{cy}" dur="{period}s" repeatCount="indefinite" '
        f'keyPoints="0;1;1" keyTimes="0;{kend:.2f};1" calcMode="linear"/>'
        f'<animate attributeName="opacity" values="0;1;1;0;0" keyTimes="0;0.04;{kend - 0.04:.2f};{kend:.2f};1" dur="{period}s" repeatCount="indefinite"/>'
        f'<circle r="9" fill="{TEAL}" opacity="0.35" filter="url(#blur)">{pulse_fill}</circle>'
        f'<circle r="4" fill="{TEAL}">{pulse_fill}</circle></g>'
    )

    # --- facts row ---
    sep = f'<tspan fill="{FAINT}">  ·  </tspan>'
    facts = (
        f'<text x="450" y="{H - 30}" text-anchor="middle" font-family="{MONO}" font-size="12" fill="{MUTED}">'
        f'<tspan fill="{TEAL}">▸ </tspan><tspan fill="{TEXT}">IIT Madras</tspan>{sep}BS Data Science{sep}CGPA <tspan fill="{TEAL}" font-weight="700">9.0</tspan>'
        f'<tspan dx="22" fill="{AMBER}">▸ </tspan><tspan fill="{AMBER}" font-weight="700">Runner-up</tspan>, Paradox DSA Triathlon 2026</text>'
    )

    name_attrs = f'x="450" y="86" text-anchor="middle" font-family="{SANS}" font-size="50" font-weight="800" letter-spacing="7"'
    all_phrases = " / ".join("".join(t for t, _ in ph) for ph in HERO_PHRASES)
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 {H}" width="100%" role="img" aria-labelledby="t d">
<title id="t">Aditya Singh: LLM systems, AI agents, full-stack</title>
<desc id="d">Models propose. Code verifies. People decide. A typed line cycles through: {escape(all_phrases)}. Below it, a three-stage pipeline from model to verification to a person signing off. IIT Madras, BS Data Science, CGPA 9.0. Runner-up, Paradox DSA Triathlon 2026.</desc>
<defs>
  <linearGradient id="name" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{TEAL}"/><stop offset="0.55" stop-color="#a7f3d0"/><stop offset="1" stop-color="{AMBER}"/>
  </linearGradient>
  <linearGradient id="shine" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="170" y2="0">
    <stop offset="0" stop-color="#ffffff" stop-opacity="0"/><stop offset="0.5" stop-color="#ffffff" stop-opacity="0.8"/><stop offset="1" stop-color="#ffffff" stop-opacity="0"/>
    <animateTransform attributeName="gradientTransform" type="translate" values="-200 0;-200 0;900 0;900 0" keyTimes="0;0.12;0.42;1" dur="7s" repeatCount="indefinite"/>
  </linearGradient>
  <pattern id="dots" width="18" height="18" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r="1" fill="#1f2630"/></pattern>
  <radialGradient id="glow" cx="50%" cy="30%" r="55%"><stop offset="0" stop-color="{TEAL}" stop-opacity="0.10"/><stop offset="1" stop-color="{TEAL}" stop-opacity="0"/></radialGradient>
  <filter id="blur" x="-1" y="-1" width="3" height="3"><feGaussianBlur stdDeviation="3"/></filter>
  {"".join(links)}
  {"".join(clips)}
</defs>
<rect x="0.5" y="0.5" width="899" height="{H - 1}" rx="16" fill="{SURFACE}" stroke="{BORDER}"/>
<rect x="1" y="1" width="898" height="{H - 2}" rx="16" fill="url(#dots)"/>
<rect x="1" y="1" width="898" height="{H - 2}" rx="16" fill="url(#glow)"/>
<text {name_attrs} fill="url(#name)">ADITYA SINGH</text>
<text {name_attrs} fill="url(#shine)" aria-hidden="true">ADITYA SINGH</text>
<text x="450" y="118" text-anchor="middle" font-family="{MONO}" font-size="13" letter-spacing="3" fill="{MUTED}">LLM SYSTEMS  ·  AI AGENTS  ·  FULL-STACK</text>
{"".join(typed)}
{caret}
{"".join(link_svg)}
<!-- Drawn under the nodes so the pulse shows only on the connectors -->
{pulse}
{"".join(node_svg)}
{tick}
<line x1="300" y1="{H - 58}" x2="600" y2="{H - 58}" stroke="{BORDER}" stroke-width="1"/>
{facts}
</svg>
"""


def pattern() -> str:
    cols = [(230, 190, TEAL, "01  MODEL PROPOSES"), (452, 190, AMBER, "02  CODE VERIFIES"), (674, 190, PERSON, "03  A PERSON DECIDES")]
    top, row_h, gap = 122, 80, 10
    height = top + len(PATTERN_ROWS) * (row_h + gap) + 40
    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 {height}" width="100%" role="img" aria-labelledby="t d">',
        '<title id="t">How I build: one pattern across four AI projects</title>',
        '<desc id="d">'
        + escape(" ".join(f"{r['name']}: {' / '.join(r['cells'])}." for r in PATTERN_ROWS))
        + "</desc>",
        f'<rect x="0.5" y="0.5" width="899" height="{height - 1}" rx="16" fill="{SURFACE}" stroke="{BORDER}"/>',
        f'<text x="32" y="40" font-family="{MONO}" font-size="12" letter-spacing="3" fill="{AMBER}">HOW I BUILD</text>',
        f'<text x="32" y="68" font-family="{SANS}" font-size="20" font-weight="700" fill="{TEXT}">The model never gets the last word</text>',
    ]
    for x, _, color, label in cols:
        out.append(f'<text x="{x}" y="{top - 12}" font-family="{MONO}" font-size="11" font-weight="700" letter-spacing="2" fill="{color}">{label}</text>')
    for i, row in enumerate(PATTERN_ROWS):
        y = top + i * (row_h + gap)
        out.append(f'<rect x="20" y="{y}" width="860" height="{row_h}" rx="10" fill="{PANEL}" stroke="{BORDER}"/>')
        out.append(f'<text x="36" y="{y + 30}" font-family="{SANS}" font-size="16" font-weight="700" fill="{TEXT}">{row["name"]}</text>')
        out.append(f'<text x="36" y="{y + 50}" font-family="{MONO}" font-size="10.5" fill="{MUTED}">{escape(row["stack"])}</text>')
        for (x, width, color, _), cell in zip(cols, row["cells"]):
            lines = wrap(cell, width_px=width - 8, font_px=12.5)
            first = y + row_h / 2 - (len(lines) - 1) * 8 + 4
            tspans = "".join(f'<tspan x="{x}" y="{first + n * 16:.0f}">{escape(line)}</tspan>' for n, line in enumerate(lines))
            out.append(f'<text font-family="{SANS}" font-size="12.5" fill="{TEXT}">{tspans}</text>')
        for n, ax in enumerate((436, 658)):
            ay = y + row_h / 2
            begin = f"{i * 0.6 + n * 0.3:.1f}s"
            out.append(
                f'<path d="M{ax - 4},{ay - 5} L{ax + 2},{ay} L{ax - 4},{ay + 5}" fill="none" stroke="{cols[n + 1][2]}" stroke-width="1.8" opacity="0.35">'
                f'<animate attributeName="opacity" values="0.35;1;0.35" dur="2.4s" begin="{begin}" repeatCount="indefinite"/></path>'
            )
    out.append(
        f'<text x="32" y="{height - 16}" font-family="{SANS}" font-size="12" fill="{MUTED}">'
        "LLMs are the reasoning layer, not the foundation: deterministic code checks their output, and a person approves anything irreversible.</text>"
    )
    out.append("</svg>\n")
    return "\n".join(out)


if __name__ == "__main__":
    ASSETS.mkdir(exist_ok=True)
    (ASSETS / "hero.svg").write_text(hero(), encoding="utf-8")
    (ASSETS / "pattern.svg").write_text(pattern(), encoding="utf-8")
    print("wrote assets/hero.svg, assets/pattern.svg")
