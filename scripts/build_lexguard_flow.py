"""Render assets/lexguard_flow.svg: an illustrative contract moving through LexGuard's five pipeline stages.

Run from the repo root:  python3 scripts/build_lexguard_flow.py

The contract is illustrative; the stage names, trap types and verifier labels are LexGuard's own.
Every animated element's resting style is its final state, so a frozen first frame (or a viewer with
reduced motion) still shows the finished review. The loop starts on that final state, rewinds, and replays.
"""

from pathlib import Path
from xml.sax.saxutils import escape

from theme import AMBER, BORDER, FAINT, MONO, MUTED, PANEL, SANS, SURFACE, TEAL, TEXT, wrap

OUT = Path(__file__).resolve().parent.parent / "assets" / "lexguard_flow.svg"

RED = "#f85149"    # caught / flagged
GREEN = "#3fb950"  # verified ok

W = 900
LEFT, RIGHT = 32, 868
LOOP = 12.5                 # seconds
RESET = (0.8, 1.3)          # final state fades out here, then the run replays
FADE = 0.3

STAGES = [  # (label, caption, colour, start, end)
    ("Classifier", "tags clause types", TEAL, 1.5, 3.3),
    ("Risk analyst", "+ adversarial judge", TEAL, 3.3, 5.3),
    ("Safety net", "36 trap patterns", AMBER, 5.3, 7.6),
    ("Citation verifier", "checks statutes", AMBER, 7.6, 9.6),
    ("Fairer rewrite", "drafts fair wording", TEAL, 9.6, 11.0),
]

CLAUSES = [
    {
        "key": "A",
        "text": "Employee shall not join any competitor anywhere in India for 2 years after leaving.",
        "type": "non_compete",
        "first": ("HIGH", AMBER),
        "trap": "trap: post-employment non-compete",
    },
    {
        "key": "B",
        "text": "If Employee resigns within 24 months, Employee shall repay ₹3,00,000 in training costs.",
        "type": "compensation",
        "first": ("LOW", MUTED),
        "trap": "trap: punitive training bond",
        "rewrite": "Training costs repayable pro rata, only for resignation within 12 months, capped at actual cost.",
    },
    {"key": "C", "text": "Either party may terminate with 30 days' written notice.", "type": "termination", "first": ("LOW", MUTED)},
    {"key": "D", "text": "Invoices are payable within 45 days of receipt.", "type": "payment", "first": ("LOW", MUTED)},
]

CITATIONS = [  # (statute, subject, verdict, colour)
    ("Indian Contract Act, s.27", "restraint of trade", "strong", GREEN),
    ("Indian Contract Act, s.74", "penalty for breach", "strong", GREEN),
    ("Indian Contract Act, s.412", None, "hallucinated · not in corpus", RED),
]

# Card geometry
CARD_TOP = 140
HEAD_H = 28       # card header row
FIRST, STEP = 20, 17  # first baseline offset and line step inside a clause row
CARD_R = 600
TEXT_X, TEXT_W = 72, 330
TYPE_X, BADGE_X = 418, 516
PANEL_X = 616


class Timeline:
    """Collects one CSS @keyframes block per animated element, keyed by seconds into the loop."""

    def __init__(self) -> None:
        self.rules: list[str] = []

    def add(self, frames: list[tuple[float, str]]) -> str:
        name = f"k{len(self.rules)}"
        frames = sorted(frames, key=lambda f: f[0])
        steps = " ".join(f"{100 * t / LOOP:.2f}%{{{decl}}}" for t, decl in frames)
        self.rules.append(f"@keyframes {name}{{{steps}}} .{name}{{animation:{name} {LOOP}s linear infinite}}")
        return name

    def appear(self, at: float, final: float = 1.0) -> str:
        """Visible in the final state; hidden by the reset; fades in at `at`."""
        r0, r1 = RESET
        return self.add([(0, f"opacity:{final}"), (r0, f"opacity:{final}"), (r1, "opacity:0"),
                         (at, "opacity:0"), (at + FADE, f"opacity:{final}"), (LOOP, f"opacity:{final}")])

    def window(self, on: float, off: float, peak: float = 1.0) -> str:
        """Hidden in the final state; shown between `on` and `off`."""
        return self.add([(0, "opacity:0"), (on, "opacity:0"), (on + FADE, f"opacity:{peak}"),
                         (off, f"opacity:{peak}"), (off + FADE, "opacity:0"), (LOOP, "opacity:0")])

    def css(self) -> str:
        return "\n".join(self.rules)


def text(x, y, body, size=12, color=TEXT, family=SANS, weight=None, anchor=None, spacing=None, cls=None, opacity=None):
    attrs = [f'x="{x}"', f'y="{y}"', f'font-family="{family}"', f'font-size="{size}"', f'fill="{color}"']
    if weight:
        attrs.append(f'font-weight="{weight}"')
    if anchor:
        attrs.append(f'text-anchor="{anchor}"')
    if spacing:
        attrs.append(f'letter-spacing="{spacing}"')
    if cls:
        attrs.append(f'class="{cls}"')
    if opacity is not None:
        attrs.append(f'opacity="{opacity}"')
    return f'<text {" ".join(attrs)}>{body}</text>'


def pill(x, y, label, color, cls=None, filled=False, width=None, opacity=None):
    """A small mono label in a rounded outline; returns (svg, width)."""
    w = width or round(len(label) * 6.4 + 16)
    fill = color if filled else "none"
    fill_op = ' fill-opacity="0.16"' if filled else ""
    group = f' class="{cls}"' if cls else ""
    op = f' opacity="{opacity}"' if opacity is not None else ""
    return (
        f'<g{group}{op}><rect x="{x}" y="{y}" width="{w}" height="18" rx="9" fill="{fill}"{fill_op} stroke="{color}" stroke-width="1"/>'
        + text(x + w / 2, y + 12.5, escape(label), 10.5, color, MONO, "700" if filled else None, "middle")
        + "</g>"
    ), w


def render() -> str:
    tl = Timeline()
    body: list[str] = []

    # ---- stage rail -------------------------------------------------------------------------
    rail_y, rail_h, gap = 80, 42, 19
    pill_w = (RIGHT - LEFT - gap * (len(STAGES) - 1)) / len(STAGES)
    for i, (label, caption, color, start, end) in enumerate(STAGES):
        x = LEFT + i * (pill_w + gap)
        body.append(f'<rect x="{x:.1f}" y="{rail_y}" width="{pill_w:.1f}" height="{rail_h}" rx="10" fill="{PANEL}" stroke="{BORDER}"/>')
        # Active glow while the stage runs, lit outline once it has run
        body.append(f'<rect class="{tl.window(start, end - FADE, 0.16)}" x="{x:.1f}" y="{rail_y}" width="{pill_w:.1f}" height="{rail_h}" rx="10" fill="{color}" opacity="0"/>')
        body.append(f'<rect class="{tl.appear(start, 0.85)}" x="{x:.1f}" y="{rail_y}" width="{pill_w:.1f}" height="{rail_h}" rx="10" fill="none" stroke="{color}" stroke-width="1.5" opacity="0.85"/>')
        body.append(text(f"{x + 14:.1f}", rail_y + 18, f'<tspan fill="{color}" font-family="{MONO}" font-weight="700">{i + 1}</tspan>  {escape(label)}', 13, TEXT, SANS, "700"))
        body.append(text(f"{x + 14:.1f}", rail_y + 33, escape(caption), 10.5, MUTED, MONO))
        if i < len(STAGES) - 1:
            cx = x + pill_w + gap / 2
            cy = rail_y + rail_h / 2
            body.append(f'<path d="M{cx - 3:.1f},{cy - 5} L{cx + 3:.1f},{cy} L{cx - 3:.1f},{cy + 5}" fill="none" stroke="{FAINT}" stroke-width="1.6"/>')

    # Progress line under the rail: draws across each pill while its stage runs
    track_y = rail_y + rail_h + 7
    length = RIGHT - LEFT
    body.append(f'<line x1="{LEFT}" y1="{track_y}" x2="{RIGHT}" y2="{track_y}" stroke="{BORDER}" stroke-width="2" stroke-linecap="round"/>')
    frames = [(0, "stroke-dashoffset:0;opacity:1"), (RESET[0], "stroke-dashoffset:0;opacity:1"),
              (RESET[1], f"stroke-dashoffset:0;opacity:0"), (RESET[1] + 0.05, f"stroke-dashoffset:{length};opacity:0"),
              (STAGES[0][3] - 0.05, f"stroke-dashoffset:{length};opacity:1")]
    for i, (*_, start, end) in enumerate(STAGES):
        x0 = i * (pill_w + gap)
        x1 = x0 + pill_w if i < len(STAGES) - 1 else length
        frames += [(start, f"stroke-dashoffset:{length - x0:.1f};opacity:1"), (end - 0.05, f"stroke-dashoffset:{length - x1:.1f};opacity:1")]
    frames.append((LOOP, "stroke-dashoffset:0;opacity:1"))
    body.append(f'<line class="{tl.add(frames)}" x1="{LEFT}" y1="{track_y}" x2="{RIGHT}" y2="{track_y}" stroke="url(#rail)" '
                f'stroke-width="2" stroke-linecap="round" stroke-dasharray="{length} {length}" stroke-dashoffset="0"/>')

    # ---- contract card ----------------------------------------------------------------------
    s1, s2, s3, s4, s5 = (s[3] for s in STAGES)
    flips = {"A": s3 + 0.45, "B": s3 + 1.05}
    y = CARD_TOP + HEAD_H + 2
    rows = []
    for clause in CLAUSES:
        g = {"top": y, "lines": wrap(clause["text"], TEXT_W, 13)}
        g["first"] = y + FIRST
        end = g["first"] + (len(g["lines"]) - 1) * STEP
        if "trap" in clause:
            g["note"] = end = end + 15
        bottom = end + 12
        if "rewrite" in clause:
            g["rew"] = wrap(clause["rewrite"], CARD_R - TEXT_X - 40, 12.5)
            g["box"] = end + 10
            g["box_h"] = 22 + len(g["rew"]) * 16
            bottom = g["box"] + g["box_h"] + 10
        g["height"] = bottom - y
        rows.append((clause, g))
        y = bottom
    card_bottom = y + 4

    body.append(f'<rect x="{LEFT}" y="{CARD_TOP}" width="{CARD_R - LEFT}" height="{card_bottom - CARD_TOP}" rx="12" fill="{PANEL}" stroke="{BORDER}"/>')
    hy = CARD_TOP + 19
    body.append(text(LEFT + 16, hy, "CONTRACT · 4 CLAUSES", 10.5, MUTED, MONO, spacing="1.5"))
    body.append(text(TYPE_X, hy, "TYPE", 10.5, MUTED, MONO, spacing="1.5"))
    body.append(text(BADGE_X, hy, "RISK", 10.5, MUTED, MONO, spacing="1.5"))
    body.append(f'<line x1="{LEFT + 1}" y1="{CARD_TOP + HEAD_H}" x2="{CARD_R - 1}" y2="{CARD_TOP + HEAD_H}" stroke="{BORDER}"/>')

    scan_from, scan_to = CARD_TOP + HEAD_H + 2, card_bottom - 4
    for n, (clause, g) in enumerate(rows):
        key, top, height, lines = clause["key"], g["top"], g["height"], g["lines"]
        if n:
            body.append(f'<line x1="{LEFT + 16}" y1="{top}" x2="{CARD_R - 16}" y2="{top}" stroke="{BORDER}" stroke-dasharray="2 4"/>')
        if "trap" in clause:
            flip = flips[key]
            # Red wash: one 0.8 s pulse when the trap pattern fires (well under 3 Hz), then a faint resting tint
            body.append(f'<rect class="{tl.add([(0, "opacity:0.07"), (RESET[0], "opacity:0.07"), (RESET[1], "opacity:0"), (flip - 0.1, "opacity:0"), (flip + 0.2, "opacity:0.24"), (flip + 0.9, "opacity:0.07"), (LOOP, "opacity:0.07")])}" '
                        f'x="{LEFT + 1}" y="{top + 1}" width="{CARD_R - LEFT - 2}" height="{height - 2}" fill="{RED}" opacity="0.07"/>')
            body.append(f'<rect class="{tl.appear(flip)}" x="{LEFT + 1}" y="{top + 6}" width="3" height="{height - 12}" rx="1.5" fill="{RED}"/>')
        first_y = g["first"]
        body.append(text(LEFT + 18, first_y, key, 13, MUTED, MONO, "700"))
        tspans = "".join(f'<tspan x="{TEXT_X}" y="{first_y + i * STEP}">{escape(line)}</tspan>' for i, line in enumerate(lines))
        if "rewrite" in clause:
            # The original wording dims once the rewrite lands
            dim = tl.add([(0, "opacity:0.55"), (RESET[0], "opacity:0.55"), (RESET[1], "opacity:1"), (s5 + 0.2, "opacity:1"), (s5 + 0.5, "opacity:0.55"), (LOOP, "opacity:0.55")])
            body.append(f'<text class="{dim}" font-family="{SANS}" font-size="13" fill="{TEXT}" opacity="0.55">{tspans}</text>')
        else:
            body.append(f'<text font-family="{SANS}" font-size="13" fill="{TEXT}">{tspans}</text>')

        # 1 classifier: type tag
        svg, _ = pill(TYPE_X, first_y - 13, clause["type"], TEAL, tl.appear(s1 + 0.3 + 0.3 * n), width=88)
        body.append(svg)
        # 2 risk analyst: first badge (replaced by CRITICAL for trapped clauses)
        label, color = clause["first"]
        appear = s2 + 0.3 + 0.3 * n
        if "trap" in clause:
            svg, _ = pill(BADGE_X, first_y - 13, label, color, tl.window(appear, flips[key] - FADE), filled=True, width=66, opacity=0)
            body.append(svg)
            # 3 safety net: badge flips to CRITICAL with the trap that fired
            svg, _ = pill(BADGE_X, first_y - 13, "CRITICAL", RED, tl.appear(flips[key]), filled=True, width=66)
            body.append(svg)
            # Keep the overruled LLM rating visible under the new badge
            body.append(text(BADGE_X + 33, first_y + STEP, f"LLM: {label}", 10, MUTED, MONO, anchor="middle", cls=tl.appear(flips[key] + 0.15)))
            body.append(text(TEXT_X, g["note"], escape(clause["trap"]), 11, RED, MONO, cls=tl.appear(flips[key] + 0.15)))
        else:
            svg, _ = pill(BADGE_X, first_y - 13, label, color, tl.appear(appear), filled=True, width=66)
            body.append(svg)

        if "rewrite" in clause:
            # 5 fairer rewrite
            box_y, box_h = g["box"], g["box_h"]
            rew = "".join(f'<tspan x="{TEXT_X + 12}" y="{box_y + 33 + i * 16}">{escape(line)}</tspan>' for i, line in enumerate(g["rew"]))
            body.append(
                f'<g class="{tl.window(RESET[1], s5 + 0.3)}" opacity="0"><rect x="{TEXT_X}" y="{box_y}" width="{CARD_R - TEXT_X - 16}" height="{box_h}" rx="8" fill="none" stroke="{FAINT}" stroke-dasharray="3 4"/>'
                + text(TEXT_X + 12, box_y + 15, "REWRITE · STAGE 5", 10, FAINT, MONO, spacing="1.5") + "</g>"
            )
            body.append(
                f'<g class="{tl.appear(s5 + 0.3)}"><rect x="{TEXT_X}" y="{box_y}" width="{CARD_R - TEXT_X - 16}" height="{box_h}" rx="8" fill="{TEAL}" fill-opacity="0.08" stroke="{TEAL}" stroke-opacity="0.6"/>'
                + text(TEXT_X + 12, box_y + 15, "↳ FAIRER REWRITE", 10, TEAL, MONO, "700", spacing="1.5")
                + f'<text font-family="{SANS}" font-size="12.5" fill="{TEXT}">{rew}</text></g>'
            )

    # Safety-net scan line sweeping down the clauses
    scan = tl.add([(0, f"opacity:0;transform:translateY(0px)"), (s3 + 0.1, "opacity:0;transform:translateY(0px)"),
                   (s3 + 0.25, "opacity:1;transform:translateY(0px)"),
                   (s3 + 1.9, f"opacity:1;transform:translateY({scan_to - scan_from}px)"),
                   (s3 + 2.1, f"opacity:0;transform:translateY({scan_to - scan_from}px)"), (LOOP, "opacity:0;transform:translateY(0px)")])
    body.append(f'<g class="{scan}" opacity="0"><rect x="{LEFT + 1}" y="{scan_from - 18}" width="{CARD_R - LEFT - 2}" height="18" fill="url(#scan)"/>'
                f'<line x1="{LEFT + 1}" y1="{scan_from}" x2="{CARD_R - 1}" y2="{scan_from}" stroke="{AMBER}" stroke-width="1.5"/></g>')

    # ---- citations panel --------------------------------------------------------------------
    body.append(f'<rect x="{PANEL_X}" y="{CARD_TOP}" width="{RIGHT - PANEL_X}" height="{card_bottom - CARD_TOP}" rx="12" fill="{PANEL}" stroke="{BORDER}"/>')
    body.append(text(PANEL_X + 16, hy, "STATUTES CITED", 10.5, MUTED, MONO, spacing="1.5"))
    body.append(f'<line x1="{PANEL_X + 1}" y1="{CARD_TOP + HEAD_H}" x2="{RIGHT - 1}" y2="{CARD_TOP + HEAD_H}" stroke="{BORDER}"/>')
    body.append(text((PANEL_X + RIGHT) / 2, CARD_TOP + 150, "verifier runs at stage 4", 11, FAINT, MONO, anchor="middle", cls=tl.window(RESET[1], s4 + 0.1), opacity=0))
    cy = CARD_TOP + HEAD_H + 24
    for i, (statute, subject, verdict, color) in enumerate(CITATIONS):
        at = s4 + 0.2 + 0.6 * i
        inner = text(PANEL_X + 16, cy, escape(statute), 13, TEXT, SANS, "600")
        vy = cy + 10
        if subject:
            inner += text(PANEL_X + 16, cy + 18, escape(subject), 11, MUTED, MONO)
            vy = cy + 28
        body.append(f'<g class="{tl.appear(at)}">{inner}</g>')
        svg, _ = pill(PANEL_X + 16, vy, verdict, color, tl.appear(at + 0.3), filled=True)
        body.append(svg)
        cy = vy + 46
    ly = card_bottom - 48
    body.append(f'<line x1="{PANEL_X + 16}" y1="{ly - 16}" x2="{RIGHT - 16}" y2="{ly - 16}" stroke="{BORDER}" stroke-dasharray="2 4"/>')
    body.append(text(PANEL_X + 16, ly, "VERIFIER LABELS", 10, MUTED, MONO, spacing="1.5"))
    body.append(text(PANEL_X + 16, ly + 18,
                     f'<tspan fill="{GREEN}">strong</tspan> · weak ·',
                     10.5, MUTED, MONO))
    body.append(text(PANEL_X + 16, ly + 34, f'<tspan fill="{RED}">hallucinated</tspan> · unverifiable', 10.5, MUTED, MONO))

    # ---- footer: real benchmark + infra facts, then the honesty note ------------------------
    fy = card_bottom + 26
    H = fy + 40
    body.append(text(LEFT, fy, "BENCHMARK", 10.5, AMBER, MONO, spacing="1.5"))
    body.append(text(LEFT + 92, fy, "28/30 clause types · 21/30 risk tiers · 0 risky under-rated (May 2026 runs)", 12.5, TEXT, SANS))
    body.append(text(RIGHT, fy, "pipeline runs on a Redis job queue", 10.5, MUTED, MONO, anchor="end"))
    body.append(text(LEFT, fy + 22, "illustrative run · real pipeline stages, trap types and verifier labels from github.com/Aditya2514/LexGuard",
                     10.5, MUTED, MONO))

    desc = (
        "Illustrative run of LexGuard's pipeline on a four-clause contract. Stages: classifier, risk analyst plus adversarial judge, "
        "safety net with 36 trap patterns, citation verifier, fairer rewrite. The classifier tags clauses as non_compete, compensation, "
        "termination and payment. The risk analyst rates the non-compete HIGH and a training-bond clause LOW; the safety net overrules both "
        "to CRITICAL (post-employment non-compete, punitive training bond). The citation verifier marks Indian Contract Act s.27 and s.74 "
        "strong and s.412 hallucinated, not in corpus. The training bond gets a fairer rewrite: costs repayable pro rata, only within "
        "12 months, capped at actual cost. Benchmark: 28 of 30 clause types, 21 of 30 risk tiers, 0 risky clauses under-rated."
    )
    head = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="100%" role="img" aria-labelledby="t d">',
        '<title id="t">Watch LexGuard work: a contract through the pipeline</title>',
        f'<desc id="d">{escape(desc)}</desc>',
        "<defs>",
        f'<linearGradient id="rail" x1="{LEFT}" y1="0" x2="{RIGHT}" y2="0" gradientUnits="userSpaceOnUse">'
        f'<stop offset="0" stop-color="{TEAL}"/><stop offset="0.38" stop-color="{TEAL}"/><stop offset="0.42" stop-color="{AMBER}"/>'
        f'<stop offset="0.78" stop-color="{AMBER}"/><stop offset="0.82" stop-color="{TEAL}"/><stop offset="1" stop-color="{TEAL}"/></linearGradient>',
        f'<linearGradient id="scan" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{AMBER}" stop-opacity="0"/>'
        f'<stop offset="1" stop-color="{AMBER}" stop-opacity="0.22"/></linearGradient>',
        "</defs>",
        "<style>",
        tl.css(),
        "@media (prefers-reduced-motion: reduce) { * { animation: none !important; } }",
        "</style>",
        f'<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="16" fill="{SURFACE}" stroke="{BORDER}"/>',
        text(LEFT, 40, "WATCH IT WORK", 12, AMBER, MONO, spacing="3"),
        text(LEFT, 66, "LexGuard: a contract through the pipeline", 20, TEXT, SANS, "700"),
    ]
    return "\n".join(head + body + ["</svg>\n"])


if __name__ == "__main__":
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(render(), encoding="utf-8")
    print("wrote assets/lexguard_flow.svg")
