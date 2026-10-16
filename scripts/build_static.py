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
            "38 trap patterns + cross-clause contradiction rules",
            "Signer reviews ratings, cited statutes, rewrites",
        ],
    },
    {
        "name": "Resilion",
        "stack": "FastAPI · NetworkX · Gemini",
        "cells": [
            "Risk Watcher agent turns news into disruption events",
            "Graph traversal proves the downstream impact",
            "No rerouting order runs without approval",
        ],
    },
    {
        "name": "Pikina",
        "stack": "Python · Ollama · Electron",
        "cells": [
            "Local Ollama parses intent when regex routes miss",
            "Validation layer + DAG checks gate every task",
            "Consent popup for risky OS actions; rollback on failure",
        ],
    },
    {
        "name": "Noesis",
        "stack": "Python · Groq · ChromaDB",
        "cells": [
            "Llama 3.3 drafts the answer in one grounded pass",
            "Hybrid BM25 + dense retrieval with reranking",
            "Answers cite the timestamp, page or frame used",
        ],
    },
]


def hero() -> str:
    nodes = [
        (270, "MODEL", TEAL, "drafts the answer"),
        (450, "VERIFY", AMBER, "rules and tests check it"),
        (630, "PERSON", PERSON, "signs off on the action"),
    ]
    node_svg = []
    for i, (cx, label, color, caption) in enumerate(nodes):
        node_svg.append(
            f'<rect x="{cx - 62}" y="206" width="124" height="34" rx="17" fill="{PANEL}" stroke="{color}" stroke-width="1.5"/>'
            f'<text x="{cx}" y="228" text-anchor="middle" font-family="{MONO}" font-size="12" font-weight="700" letter-spacing="2" fill="{color}">{label}</text>'
            f'<text x="{cx}" y="266" text-anchor="middle" font-family="{SANS}" font-size="12" fill="{MUTED}">{caption}</text>'
        )
        # Each stage lights up as the pulse reaches it
        node_svg.append(
            f'<rect x="{cx - 62}" y="206" width="124" height="34" rx="17" fill="{color}" opacity="0">'
            f'<animate attributeName="opacity" values="0;0.18;0" keyTimes="0;0.5;1" dur="1.2s" begin="{i * 1.4}s;pulse.end+{i * 1.4}s"/></rect>'
        )
    links = "".join(
        f'<line x1="{x1}" y1="223" x2="{x2}" y2="223" stroke="{FAINT}" stroke-width="1.5"/>'
        f'<path d="M{x2 - 6},218 L{x2},223 L{x2 - 6},228" fill="none" stroke="{FAINT}" stroke-width="1.5"/>'
        for x1, x2 in ((338, 382), (518, 562))
    )
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 300" width="100%" role="img" aria-labelledby="t d">
<title id="t">Aditya Singh: LLM systems, AI agents, full-stack</title>
<desc id="d">Models propose. Code verifies. People decide. A three-stage pipeline from model to verification to a person signing off.</desc>
<defs>
  <linearGradient id="name" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{TEAL}"/><stop offset="0.55" stop-color="#a7f3d0"/><stop offset="1" stop-color="{AMBER}"/>
  </linearGradient>
  <pattern id="dots" width="18" height="18" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r="1" fill="#1f2630"/></pattern>
  <radialGradient id="glow" cx="50%" cy="30%" r="55%"><stop offset="0" stop-color="{TEAL}" stop-opacity="0.10"/><stop offset="1" stop-color="{TEAL}" stop-opacity="0"/></radialGradient>
</defs>
<rect x="0.5" y="0.5" width="899" height="299" rx="16" fill="{SURFACE}" stroke="{BORDER}"/>
<rect x="1" y="1" width="898" height="298" rx="16" fill="url(#dots)"/>
<rect x="1" y="1" width="898" height="298" rx="16" fill="url(#glow)"/>
<text x="450" y="88" text-anchor="middle" font-family="{SANS}" font-size="50" font-weight="800" letter-spacing="7" fill="url(#name)">ADITYA SINGH</text>
<text x="450" y="122" text-anchor="middle" font-family="{MONO}" font-size="13" letter-spacing="3" fill="{MUTED}">LLM SYSTEMS  ·  AI AGENTS  ·  FULL-STACK</text>
<text x="450" y="166" text-anchor="middle" font-family="{SANS}" font-size="20" fill="{TEXT}">Models <tspan fill="{TEAL}" font-weight="700">propose</tspan>. Code <tspan fill="{AMBER}" font-weight="700">verifies</tspan>. People <tspan fill="{PERSON}" font-weight="700">decide</tspan>.</text>
{links}
<!-- Drawn under the nodes so the pulse shows only on the connectors -->
<circle r="4" fill="{TEXT}">
  <animateMotion id="pulse" path="M208,223 L692,223" dur="4.2s" begin="0s;pulse.end+0.8s" keyPoints="0;1" keyTimes="0;1" calcMode="linear"/>
  <animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.1;0.9;1" dur="4.2s" begin="0s;pulse.end+0.8s"/>
</circle>
{''.join(node_svg)}
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
