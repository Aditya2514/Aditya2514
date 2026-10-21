"""Render the four flagship project cards: assets/card_{lexguard,pikina,resilion,noesis}.svg.

Run from the repo root:  python3 scripts/build_cards.py

One template, four cards. Each card is 440 wide (two sit side by side in the README, each ~410 px on GitHub):
kicker, name, one-line pitch, a micro-animation of the project's real mechanism, then stack chips and a status chip.

Every animated element's resting style is its final state, so a frozen first frame, a viewer with reduced motion,
or GitHub's mobile app still shows the finished run. Each loop starts on that final state, rewinds, and replays.
The example inputs (contract clauses, commands, the news event, the answer) are illustrative and labelled so;
the mechanisms, names and numbers are the projects' own.
"""

from pathlib import Path
from xml.sax.saxutils import escape

from theme import AMBER, BORDER, FAINT, MONO, MUTED, PANEL, SANS, SURFACE, TEAL, TEXT, wrap

ASSETS = Path(__file__).resolve().parent.parent / "assets"

RED = "#f85149"    # caught / flagged
GREEN = "#3fb950"  # verified ok

W, H = 440, 300
L, R = 24, 416                 # content edges
PANEL_Y, PANEL_H = 110, 136    # the micro-animation stage
CHIP_Y, CHIP_H = 262, 22
FADE = 0.3
MONO_W = 0.6                   # monospace glyph width, in em
POP = "transform-box:fill-box;transform-origin:center"


def text(x, y, body, size=13, color=TEXT, family=SANS, weight=None, anchor=None, spacing=None, cls=None, opacity=None):
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


def mono_w(label: str, size: float) -> float:
    return len(label) * size * MONO_W


def pill(x, y, label, color, size=11, h=18, filled=False, width=None, cls=None, opacity=None, text_color=None, dashed=False):
    """A mono label in a rounded outline; returns (svg, width)."""
    w = width or round(mono_w(label, size) + 14)
    fill = f'fill="{color}" fill-opacity="0.16"' if filled else f'fill="{SURFACE}"'
    dash = ' stroke-dasharray="3 3"' if dashed else ""
    group = f' class="{cls}"' if cls else ""
    op = f' opacity="{opacity}"' if opacity is not None else ""
    return (
        f'<g{group}{op}><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{h / 2}" {fill} stroke="{color}"{dash}/>'
        + text(round(x + w / 2, 1), round(y + h / 2 + size * 0.36, 1), escape(label), size, text_color or color, MONO,
               "700" if filled else None, "middle")
        + "</g>"
    ), w


class Card:
    """One card: collects body SVG plus one CSS @keyframes block per animated element, keyed by seconds into the loop."""

    def __init__(self, loop: float, reset=(0.7, 1.1)) -> None:
        self.loop, self.reset = loop, reset
        self.rules: list[str] = []
        self.body: list[str] = []

    def add(self, frames: list[tuple[float, str]]) -> str:
        name = f"k{len(self.rules)}"
        frames = sorted(frames, key=lambda f: f[0])
        steps = " ".join(f"{100 * min(t, self.loop) / self.loop:.2f}%{{{decl}}}" for t, decl in frames)
        self.rules.append(f"@keyframes {name}{{{steps}}} .{name}{{animation:{name} {self.loop}s linear infinite}}")
        return name

    def appear(self, at: float, final: float = 1.0) -> str:
        """Visible in the final state; hidden by the reset; fades in at `at`."""
        r0, r1 = self.reset
        return self.add([(0, f"opacity:{final}"), (r0, f"opacity:{final}"), (r1, "opacity:0"),
                         (at, "opacity:0"), (at + FADE, f"opacity:{final}"), (self.loop, f"opacity:{final}")])

    def vanish(self, at: float, start: float = 1.0) -> str:
        """Hidden in the final state; shown from the reset until it fades out at `at`."""
        r0, r1 = self.reset
        return self.add([(0, "opacity:0"), (r0, "opacity:0"), (r1, f"opacity:{start}"),
                         (at, f"opacity:{start}"), (at + FADE, "opacity:0"), (self.loop, "opacity:0")])

    def window(self, on: float, off: float, peak: float = 1.0) -> str:
        """Hidden in the final state; shown between `on` and `off`."""
        return self.add([(0, "opacity:0"), (on, "opacity:0"), (on + FADE, f"opacity:{peak}"),
                         (off, f"opacity:{peak}"), (off + FADE, "opacity:0"), (self.loop, "opacity:0")])

    def gap(self, on: float, off: float) -> str:
        """Visible in the final state; hidden by the reset and again between `on` and `off`."""
        r0, r1 = self.reset
        return self.add([(0, "opacity:1"), (r0, "opacity:1"), (r1, "opacity:0"), (r1 + 0.2, "opacity:1"),
                         (on, "opacity:1"), (on + FADE, "opacity:0"), (off, "opacity:0"), (off + FADE, "opacity:1"),
                         (self.loop, "opacity:1")])

    def travel(self, at: float, dur: float, dx: float, dy: float) -> str:
        """A token that is invisible at rest, then slides by (dx, dy) between `at` and `at + dur` and fades out."""
        tr0, tr1 = "transform:translate(0px,0px)", f"transform:translate({dx:.1f}px,{dy:.1f}px)"
        return self.add([(0, f"opacity:0;{tr0}"), (at - 0.01, f"opacity:0;{tr0}"),
                         (at, f"opacity:1;{tr0};animation-timing-function:ease-in-out"),
                         (at + dur, f"opacity:1;{tr1}"), (at + dur + 0.2, f"opacity:0;{tr1}"), (self.loop, f"opacity:0;{tr1}")])

    def along(self, d: str, at: float, dur: float, color: str, r: float = 3.2) -> str:
        """A dot that rides the path `d` between `at` and `at + dur` (SMIL motion, CSS opacity), invisible at rest."""
        k0, k1 = at / self.loop, (at + dur) / self.loop
        fade = self.add([(0, "opacity:0"), (at - 0.01, "opacity:0"), (at, "opacity:1"), (at + dur, "opacity:1"),
                         (at + dur + 0.2, "opacity:0"), (self.loop, "opacity:0")])
        return (f'<circle class="{fade}" cx="0" cy="0" r="{r}" fill="{color}" opacity="0">'
                f'<animateMotion dur="{self.loop}s" repeatCount="indefinite" path="{d}" calcMode="spline" '
                f'keyPoints="0;0;1;1" keyTimes="0;{k0:.4f};{k1:.4f};1" keySplines="0 0 1 1;0.45 0 0.55 1;0 0 1 1"/></circle>')

    def ping(self, at: float, scale: float = 1.9, dur: float = 0.9, peak: float = 0.8) -> str:
        """An outline that swells and fades once, starting at `at`."""
        return self.add([(0, "opacity:0;transform:scale(1)"), (at - 0.01, "opacity:0;transform:scale(1)"),
                         (at, f"opacity:{peak};transform:scale(1)"),
                         (at + dur, f"opacity:0;transform:scale({scale})"), (self.loop, f"opacity:0;transform:scale({scale})")])

    def typing(self, at: float, dur: float, width: float, chars: int) -> str:
        """A cover that hides typed text after the reset, then steps right one glyph at a time and disappears."""
        r0, r1 = self.reset
        tr0, tr1 = "transform:translateX(0px)", f"transform:translateX({width:.1f}px)"
        return self.add([(0, f"opacity:0;{tr0}"), (r0, f"opacity:0;{tr0}"), (r1, f"opacity:1;{tr0}"),
                         (at, f"opacity:1;{tr0};animation-timing-function:steps({chars},end)"),
                         (at + dur, f"opacity:1;{tr1}"), (at + dur + 0.25, f"opacity:1;{tr1}"),
                         (at + dur + 0.3, f"opacity:0;{tr1}"), (self.loop, f"opacity:0;{tr1}")])

    def css(self) -> str:
        return "\n".join(self.rules)


def frame(card: Card, spec: dict) -> str:
    """Wrap the card body in the shared template: header, stage panel, chips, accessibility text."""
    accent = spec["accent"]
    head = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="100%" role="img" aria-labelledby="t d">',
        f'<title id="t">{escape(spec["title"])}</title>',
        f'<desc id="d">{escape(spec["desc"])}</desc>',
        "<defs>" + spec.get("defs", "") + "</defs>",
        "<style>",
        card.css(),
        "@keyframes breathe{0%,100%{opacity:1} 50%{opacity:0.3}} .breathe{animation:breathe 2.4s ease-in-out infinite}",
        "@media (prefers-reduced-motion: reduce) { * { animation: none !important; } }",
        "</style>",
        f'<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="16" fill="{SURFACE}" stroke="{BORDER}"/>',
        text(L, 34, escape(spec["kicker"]), 12, accent, MONO, spacing="2.5"),
        text(R, 34, "↗", 14, MUTED, SANS, anchor="end"),
        text(L, 60, escape(spec["name"]), 23, TEXT, SANS, "700"),
    ]
    lines = wrap(spec["pitch"], R - L, 14)
    assert len(lines) <= 2, spec["name"]
    for i, line in enumerate(lines):
        head.append(text(L, 82 + 18 * i, escape(line), 14, MUTED, SANS))

    # stage panel with its caption row
    head.append(f'<rect x="{L}" y="{PANEL_Y}" width="{R - L}" height="{PANEL_H}" rx="12" fill="{PANEL}" stroke="{BORDER}"/>')
    head.append(text(L + 12, PANEL_Y + 18, escape(spec["caption"]), 12, MUTED, MONO))
    note = spec.get("note", "illustrative run")
    assert mono_w(spec["caption"], 12) + mono_w(note, 12) + 40 <= R - L, f"{spec['name']}: caption row overflows"
    head.append(text(R - 12, PANEL_Y + 18, escape(note), 12, MUTED, MONO, anchor="end", opacity="0.8"))

    # bottom row: stack chips on the left, status chip on the right
    tail = []
    x = L
    for label in spec["stack"]:
        w = mono_w(label, 12) + 16
        tail.append(f'<rect x="{x:.1f}" y="{CHIP_Y}" width="{w:.1f}" height="{CHIP_H}" rx="{CHIP_H / 2}" fill="{PANEL}" stroke="{BORDER}"/>')
        tail.append(text(round(x + w / 2, 1), CHIP_Y + 15, escape(label), 12, TEXT, MONO, anchor="middle"))
        x += w + 6
    status, live = spec["status"]
    sw = mono_w(status, 12) + 28
    sx = R - sw
    assert sx >= x + 2, f"{spec['name']}: chips overflow ({x:.0f} > {sx:.0f})"
    tail.append(f'<rect x="{sx:.1f}" y="{CHIP_Y}" width="{sw:.1f}" height="{CHIP_H}" rx="{CHIP_H / 2}" fill="{accent}" fill-opacity="0.1" stroke="{accent}" stroke-opacity="0.7"/>')
    tail.append(f'<circle{" class=" + chr(34) + "breathe" + chr(34) if live else ""} cx="{sx + 12:.1f}" cy="{CHIP_Y + CHIP_H / 2}" r="3.5" fill="{accent}"/>')
    tail.append(text(round(sx + 20, 1), CHIP_Y + 15, escape(status), 12, accent, MONO))
    return "\n".join(head + card.body + tail + ["</svg>\n"])


# ------------------------------------------------------------------------------------------------
# N.01 LexGuard: a scan passes three clauses, a trap pattern overrules the LLM's LOW, a citation is caught
# ------------------------------------------------------------------------------------------------
def lexguard() -> str:
    c = Card(loop=9.0)
    b = c.body
    rows = [  # (clause, flipped?)
        ("Payment due within 45 days", False),
        ("Repay ₹3,00,000 if you resign", True),
        ("30 days' notice to terminate", False),
    ]
    base0, step = 152, 24
    badge_x, badge_w = 330, 76
    scan_start, scan_end = 1.4, 3.4
    scan_top, scan_bot = base0 - 18, base0 + 2 * step + 8
    flip_at = None
    for i, (clause, flips) in enumerate(rows):
        y = base0 + i * step
        if i:
            b.append(f'<line x1="{L + 10}" y1="{y - 17}" x2="{R - 10}" y2="{y - 17}" stroke="{BORDER}" stroke-dasharray="2 4"/>')
        mid = y - 5
        reach = scan_start + (scan_end - scan_start) * (mid - scan_top) / (scan_bot - scan_top)
        if flips:
            flip_at = reach
            b.append(f'<rect class="{c.add([(0, "opacity:0.1"), (c.reset[0], "opacity:0.1"), (c.reset[1], "opacity:0"), (reach - 0.05, "opacity:0"), (reach + 0.2, "opacity:0.28"), (reach + 1.0, "opacity:0.1"), (c.loop, "opacity:0.1")])}" '
                     f'x="{L + 6}" y="{y - 16}" width="{R - L - 12}" height="22" rx="5" fill="{RED}" opacity="0.1"/>')
        b.append(text(L + 12, y, f"{i + 1:02d}", 11, FAINT, MONO))
        b.append(text(L + 36, y, escape(clause), 13.5, TEXT, SANS))
        low, _ = pill(badge_x, y - 13, "LOW", MUTED, size=12, width=badge_w, cls=c.vanish(reach) if flips else None)
        if flips:
            b.append(low.replace("<g class=", '<g opacity="0" class=', 1))  # the LLM's LOW, gone once the trap fires
            crit, _ = pill(badge_x, y - 13, "CRITICAL", RED, size=12, filled=True, width=badge_w, cls=c.appear(reach))
            b.append(crit)
            trap, _ = pill(badge_x - 50, y - 13, "trap", AMBER, size=12, width=44, cls=c.appear(reach + 0.35))
            b.append(trap)
        else:
            b.append(low)

    # the scan bar: an amber line with a soft trailing wash
    span = scan_bot - scan_top
    scan = c.add([(0, "opacity:0;transform:translateY(0px)"), (scan_start - 0.01, "opacity:0;transform:translateY(0px)"),
                  (scan_start, "opacity:1;transform:translateY(0px)"), (scan_end, f"opacity:1;transform:translateY({span}px)"),
                  (scan_end + 0.3, f"opacity:0;transform:translateY({span}px)"), (c.loop, f"opacity:0;transform:translateY({span}px)")])
    b.append(f'<g class="{scan}" opacity="0"><rect x="{L + 6}" y="{scan_top - 14}" width="{R - L - 12}" height="14" fill="url(#scan)"/>'
             f'<line x1="{L + 6}" y1="{scan_top}" x2="{R - 6}" y2="{scan_top}" stroke="{AMBER}" stroke-width="1.5"/></g>')

    # citation verifier strip
    cy = base0 + 3 * step - 10
    b.append(f'<line x1="{L + 10}" y1="{cy - 7}" x2="{R - 10}" y2="{cy - 7}" stroke="{BORDER}"/>')
    b.append(text(L + 12, cy + 13, "Contract Act", 12, MUTED, MONO))
    ok, w1 = pill(L + 104, cy, "s.27 · strong", GREEN, size=12, h=19, cls=c.appear(scan_end + 0.3))
    bad, w2 = pill(L + 104 + w1 + 8, cy, "s.412 · hallucinated", RED, size=12, h=19, filled=True, cls=c.appear(scan_end + 0.9))
    b += [ok, bad]
    assert L + 104 + w1 + 8 + w2 <= R - 8, "LexGuard verifier strip overflows"

    defs = (f'<linearGradient id="scan" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{AMBER}" stop-opacity="0"/>'
            f'<stop offset="1" stop-color="{AMBER}" stop-opacity="0.25"/></linearGradient>')
    return frame(c, {
        "accent": AMBER, "kicker": "N.01 · LEGAL AI", "name": "LexGuard",
        "pitch": "AI contract review for Indian law. 36 trap patterns can overrule the LLM's risk rating.",
        "caption": "safety net · 36 trap patterns", "defs": defs,
        "stack": ["Node.js", "Redis", "MongoDB"], "status": ("solo · May–Aug 2026", False),
        "title": "LexGuard: AI contract review for Indian law",
        "desc": ("Project card for LexGuard, a solo project from May to August 2026. Illustrative run: a scan passes three "
                 "contract clauses; the LLM rated 'Repay 3,00,000 rupees if you resign' LOW, and one of 36 trap patterns "
                 "forces it to CRITICAL. The citation verifier marks Indian Contract Act section 27 strong and section 412 "
                 "hallucinated. Stack: Node.js, Redis job queue, MongoDB Atlas Vector Search."),
    })


# ------------------------------------------------------------------------------------------------
# N.02 Pikina: a known command routes through Tier 1 regex; a miss goes to local llama3, checked by the AVL
# ------------------------------------------------------------------------------------------------
def pikina() -> str:
    # Only mechanisms from Pikina's own history: Tier 1 regex routes, the Tier 2 Ollama router, the Action
    # Validation Layer (registered tool, claimed level must equal the registry level) and the consent rule.
    c = Card(loop=9.5)
    b = c.body
    box_x, box_w, box_h = L + 8, R - L - 16, 26
    glyph = mono_w("x", 13)
    cmds = [  # (command, box top, type start)
        ("add todo call mom", PANEL_Y + 28, 1.4),
        ("remind me to pay rent", PANEL_Y + 60, 3.4),
    ]
    done = {}
    for n, (cmd, top, start) in enumerate(cmds):
        grp = c.appear(3.2) if n else None
        b.append(f'<g{" class=" + chr(34) + grp + chr(34) if grp else ""}>')
        b.append(f'<rect x="{box_x}" y="{top}" width="{box_w}" height="{box_h}" rx="7" fill="{SURFACE}" stroke="{BORDER}"/>')
        tx, ty = box_x + 26, top + 17.5
        b.append(text(box_x + 10, ty, "›", 14, TEAL, MONO, "700"))
        b.append(text(tx, ty, escape(cmd), 13, TEXT, MONO))
        dur = 0.055 * len(cmd) + 0.3
        tw = glyph * len(cmd) + 2
        cover = c.typing(start, dur, tw, len(cmd))
        b.append(f'<g class="{cover}" opacity="0"><rect x="{tx - 1}" y="{top + 4}" width="{tw + 2}" height="{box_h - 8}" fill="{SURFACE}"/>'
                 f'<rect x="{tx - 1}" y="{top + 6}" width="2" height="{box_h - 12}" fill="{TEAL}"/></g>')
        b.append("</g>")
        done[n] = start + dur + 0.35

    # row 1: a Tier 1 regex route, no model call
    chip_w = round(mono_w("Tier 1 · regex ✓", 11.5) + 14)
    cx = box_x + box_w - chip_w - 4
    chip, _ = pill(cx, cmds[0][1] + 4, "Tier 1 · regex ✓", TEAL, size=11.5, width=chip_w, filled=True, cls=c.appear(done[0]))
    b.append(chip)

    # row 2: no regex matches, so the local model gets it
    miss_at = done[1]
    t2_at = miss_at + 0.9
    miss, _ = pill(cx, cmds[1][1] + 4, "no regex match", MUTED, size=11.5, width=chip_w, cls=c.window(miss_at, t2_at - 0.1))
    b.append(miss.replace("<g class=", '<g opacity="0" class=', 1))
    t2, _ = pill(cx, cmds[1][1] + 4, "Tier 2 · llama3", TEAL, size=11.5, width=chip_w, cls=c.appear(t2_at))
    b.append(t2)

    # what llama3 proposes, what the AVL checks, then it runs (level 0: no consent dialog needed)
    py, ph = PANEL_Y + 94, 19
    x = box_x
    steps = [("todo.add · level 0", TEAL, False, t2_at + 0.6),
             ("AVL ✓ tool · level", AMBER, True, t2_at + 1.3),
             ("runs", MUTED, False, t2_at + 1.9)]
    for n, (label, color, filled, at) in enumerate(steps):
        if n:
            b.append(f'<path class="{c.appear(at - 0.15)}" d="M{x + 3},{py + ph / 2} h9 m-4,-3.5 l4,3.5 l-4,3.5" fill="none" stroke="{MUTED}" stroke-width="1.2"/>')
            x += 18
        w = round(mono_w(label, 11.5) + 14)
        if filled:
            b.append(f'<rect class="{c.ping(at, 1.25, 0.8)}" style="{POP}" x="{x}" y="{py}" width="{w}" height="{ph}" rx="{ph / 2}" '
                     f'fill="none" stroke="{color}" stroke-width="2" opacity="0"/>')
        p, _ = pill(x, py, label, color, size=11.5, h=ph, width=w, filled=filled, cls=c.appear(at),
                    text_color=TEXT if color == MUTED else None)
        b.append(p)
        x += w
    assert x <= box_x + box_w, f"Pikina pipeline overflows ({x} > {box_x + box_w})"

    # the consent rule, always visible
    b.append(text(box_x + 2, PANEL_Y + 129, f'asks first: <tspan fill="{AMBER}">level 4+ or irreversible</tspan>', 12, MUTED, MONO))

    return frame(c, {
        "accent": TEAL, "kicker": "N.02 · LOCAL AGENT", "name": "Pikina",
        "pitch": "Offline-first personal operating layer for Windows and Linux.",
        "caption": "regex → llama3 → AVL → consent",
        "stack": ["Python", "Ollama", "Electron"], "status": ("pre-alpha · Jul 2026", True),
        "title": "Pikina: offline-first personal operating layer",
        "desc": ("Project card for Pikina, pre-alpha, started July 2026. Illustrative run in the quick panel: 'add todo call mom' "
                 "matches a Tier 1 regex route, with no model call. 'remind me to pay rent' matches no regex, so it goes to a "
                 "local llama3 model through Ollama, which must return a registered tool or no_match; it proposes todo.add at "
                 "level 0, the Action Validation Layer checks that the tool is registered and the claimed level matches the "
                 "registry, and it runs. Actions at level 4 or above, or with irreversible side effects, ask for native consent first. "
                 "Stack: Python, Ollama, Electron."),
    })


# ------------------------------------------------------------------------------------------------
# N.03 Resilion: a news event lands on a corridor and a 2-hop traversal lights refineries, then industries
# ------------------------------------------------------------------------------------------------
def resilion() -> str:
    c = Card(loop=10.0)
    b = c.body
    ph = 20
    corr_x, corr_w = L + 10, 66
    ref_x, ref_w = L + 104, 72
    ind_x, ind_w = L + 212, 78
    app_x, app_w = L + 312, 72
    event = {"x": L + 8, "y": PANEL_Y + 30, "w": 86}
    corridors = {"Hormuz": PANEL_Y + 74, "Red Sea": PANEL_Y + 106}
    refineries = {"Jamnagar": PANEL_Y + 40, "Panipat": PANEL_Y + 74, "Mumbai": PANEL_Y + 106}
    industries = {"power": PANEL_Y + 32, "petrochem": PANEL_Y + 56, "transport": PANEL_Y + 80, "LPG": PANEL_Y + 104}
    supplies = [("Hormuz", "Jamnagar"), ("Hormuz", "Panipat"), ("Hormuz", "Mumbai"), ("Red Sea", "Jamnagar"), ("Red Sea", "Mumbai")]
    serves = [("Jamnagar", k) for k in industries] + [("Panipat", k) for k in ("petrochem", "transport", "LPG")] \
        + [("Mumbai", k) for k in ("power", "transport", "LPG")]

    hit0, hop1, hop2 = 1.5, 2.6, 3.9
    leg = 0.9

    def curve(x1, y1, x2, y2):
        return f'M{x1},{y1} C{(x1 + x2) / 2},{y1} {(x1 + x2) / 2},{y2} {x2},{y2}'

    def edge(x1, y1, x2, y2, lit_at=None, dashed=False):
        d = curve(x1, y1, x2, y2)
        dash = ' stroke-dasharray="3 3"' if dashed else ""
        b.append(f'<path d="{d}" fill="none" stroke="{FAINT}" stroke-width="1"{dash}/>')
        if lit_at is not None:
            b.append(f'<path class="{c.appear(lit_at, 0.75)}" d="{d}" fill="none" stroke="{AMBER}" stroke-width="1.4" opacity="0.75"/>')

    # edges first so the pills sit on top
    for a, z in supplies:
        lit = hop1 + leg if a == "Hormuz" else None
        edge(corr_x + corr_w, corridors[a] + ph / 2, ref_x, refineries[z] + ph / 2, lit)
    for a, z in serves:
        edge(ref_x + ref_w, refineries[a] + ph / 2, ind_x, industries[z] + ph / 2, hop2 + leg)
    for z in industries:
        edge(ind_x + ind_w, industries[z] + ph / 2, app_x, PANEL_Y + 76, dashed=True)
    ex_mid = corr_x + corr_w / 2
    b.append(f'<line x1="{ex_mid}" y1="{event["y"] + ph}" x2="{ex_mid}" y2="{corridors["Hormuz"]}" stroke="{RED}" stroke-width="1.4" opacity="0.8"/>')

    # tokens travelling the hops
    def token(x1, y1, x2, y2, at, color):
        b.append(c.along(curve(x1, y1, x2, y2), at, leg, color))

    token(ex_mid, event["y"] + ph, ex_mid, corridors["Hormuz"], hit0 + 0.3, RED)
    for z in ("Jamnagar", "Panipat", "Mumbai"):
        token(corr_x + corr_w, corridors["Hormuz"] + ph / 2, ref_x, refineries[z] + ph / 2, hop1, AMBER)
    for a, z in serves:
        token(ref_x + ref_w, refineries[a] + ph / 2, ind_x, industries[z] + ph / 2, hop2, AMBER)

    # nodes
    ping = c.ping(hit0, 1.35, 1.0)
    b.append(f'<rect class="{ping}" style="{POP}" x="{event["x"]}" y="{event["y"]}" width="{event["w"]}" height="{ph}" rx="{ph / 2}" '
             f'fill="none" stroke="{RED}" stroke-width="2" opacity="0"/>')
    ev, _ = pill(event["x"], event["y"], "news event", RED, size=12, h=ph, filled=True, width=event["w"])
    b.append(ev)

    def node(x, y, w, label, lit_at=None, faint=False):
        color = FAINT if faint else MUTED
        p, _ = pill(x, y, label, color, size=12, h=ph, width=w, text_color=MUTED if faint else TEXT)
        b.append(p)
        if lit_at is not None:
            lit, _ = pill(x, y, label, AMBER, size=12, h=ph, width=w, filled=True, cls=c.appear(lit_at))
            b.append(lit)

    for k, y in corridors.items():
        if k == "Hormuz":
            p, _ = pill(corr_x, y, k, RED, size=12, h=ph, width=corr_w, cls=c.appear(hit0 + 0.3 + leg))
            b.append(pill(corr_x, y, k, MUTED, size=12, h=ph, width=corr_w, text_color=TEXT)[0])
            b.append(p)
        else:
            node(corr_x, y, corr_w, k, faint=True)
    for k, y in refineries.items():
        node(ref_x, y, ref_w, k, hop1 + leg)
    for k, y in industries.items():
        node(ind_x, y, ind_w, k, hop2 + leg)

    # planned: human approval console (not built yet), drawn dashed and faint
    ay, ah = PANEL_Y + 58, 36
    b.append(f'<rect x="{app_x}" y="{ay}" width="{app_w}" height="{ah}" rx="9" fill="{SURFACE}" stroke="{MUTED}" stroke-dasharray="3 3"/>')
    b.append(text(app_x + app_w / 2, ay + 15, "planned", 11.5, MUTED, MONO, anchor="middle"))
    b.append(text(app_x + app_w / 2, ay + 29, "approval", 12, TEXT, MONO, anchor="middle", opacity="0.75"))

    return frame(c, {
        "accent": AMBER, "kicker": "N.03 · SUPPLY-CHAIN AI", "name": "Resilion",
        "pitch": "Supply-chain risk intelligence for India's crude-oil imports.",
        "caption": "Risk Watcher → 2-hop traversal", "note": "illustrative event",
        "stack": ["Python", "NetworkX", "Gemini", "React"], "status": ("in progress", True),
        "title": "Resilion: supply-chain risk intelligence for India's crude-oil imports",
        "desc": ("Project card for Resilion, in progress. A Gemini Risk Watcher agent turns news (GDELT headlines, Guardian "
                 "articles) into structured disruption events. In this illustrative event, a news event lands on the Strait of "
                 "Hormuz corridor in the NetworkX supply graph (seeded with 13 nodes and 19 edges); a 2-hop traversal lights the "
                 "refineries it supplies (Jamnagar, Panipat, Mumbai) and then the industries they serve (power, petrochemicals, "
                 "transport fuel, LPG). The Red Sea corridor is untouched. A human approval console is planned, drawn dashed. "
                 "Stack: Python, NetworkX, Gemini, React."),
    })


# ------------------------------------------------------------------------------------------------
# N.04 Noesis: video, audio and PDF chunks flow into a hybrid index; an answer arrives with checked citations
# ------------------------------------------------------------------------------------------------
def noesis() -> str:
    c = Card(loop=9.0)
    b = c.body
    src_x, src_w, src_h = L + 8, 68, 26
    srcs = [("video", PANEL_Y + 30), ("audio", PANEL_Y + 64), ("pdf", PANEL_Y + 98)]
    idx_x, idx_y, idx_w, idx_h = L + 92, PANEL_Y + 28, 62, 98
    ans_x, ans_y = L + 168, PANEL_Y + 28
    ans_w, ans_h = R - 8 - ans_x, 98

    # source tiles with small drawn icons
    for name, y in srcs:
        b.append(f'<rect x="{src_x}" y="{y}" width="{src_w}" height="{src_h}" rx="7" fill="{SURFACE}" stroke="{BORDER}"/>')
        ix, iy = src_x + 9, y + 7
        if name == "video":
            b.append(f'<rect x="{ix}" y="{iy}" width="16" height="12" rx="2" fill="none" stroke="{TEAL}"/>'
                     f'<path d="M{ix + 6},{iy + 3} L{ix + 11},{iy + 6} L{ix + 6},{iy + 9} Z" fill="{TEAL}"/>')
        elif name == "audio":
            for k, hgt in enumerate([4, 9, 12, 7, 10, 5]):
                b.append(f'<rect x="{ix + k * 3}" y="{iy + 6 - hgt / 2}" width="1.8" height="{hgt}" rx="0.9" fill="{TEAL}"/>')
        else:
            b.append(f'<path d="M{ix + 2},{iy - 1} h8 l4,4 v10 h-12 Z" fill="none" stroke="{TEAL}"/>'
                     f'<path d="M{ix + 5},{iy + 6} h6 M{ix + 5},{iy + 9} h6" stroke="{TEAL}"/>')
        b.append(text(src_x + 31, y + 17, name, 11.5, TEXT, MONO))

    # dashed feeds from each source into the index
    for n, (name, y) in enumerate(srcs):
        b.append(f'<path d="M{src_x + src_w + 2},{y + src_h / 2} L{idx_x - 2},{idx_y + 33 + n * 14}" stroke="{FAINT}" stroke-dasharray="2 3"/>')

    # the index: lit while chunks arrive, then hybrid retrieval steps light up in order
    ingest0, ingest1 = 1.3, 3.5
    b.append(f'<rect x="{idx_x}" y="{idx_y}" width="{idx_w}" height="{idx_h}" rx="8" fill="{SURFACE}" stroke="{BORDER}"/>')
    b.append(f'<rect class="{c.window(ingest0, ingest1, 0.9)}" x="{idx_x}" y="{idx_y}" width="{idx_w}" height="{idx_h}" rx="8" '
             f'fill="none" stroke="{TEAL}" opacity="0"/>')
    b.append(text(idx_x + idx_w / 2, idx_y + 17, "index", 12.5, TEXT, SANS, "700", "middle"))

    # chunks flowing from each source into the index, two per source, staggered
    for n, (name, y) in enumerate(srcs):
        first = ingest0 + n * 0.4
        b.append(f'<rect class="{c.window(first, first + 1.3, 0.9)}" x="{src_x}" y="{y}" width="{src_w}" height="{src_h}" rx="7" '
                 f'fill="none" stroke="{TEAL}" opacity="0"/>')
        for k in range(2):
            at = first + k * 0.6
            x1, y1 = src_x + src_w + 1, y + src_h / 2 - 3.5
            x2, y2 = idx_x + idx_w / 2 - 6, idx_y + 19.5  # between the 'index' label and the BM25 line
            b.append(f'<rect class="{c.travel(at, 0.8, x2 - x1, y2 - y1)}" x="{x1}" y="{y1}" width="12" height="7" rx="1.5" '
                     f'fill="{TEAL}" fill-opacity="0.45" stroke="{TEAL}" opacity="0"/>')
    steps = ["BM25", "+ dense", "RRF", "rerank"]
    q0 = 3.6
    for n, s in enumerate(steps):
        y = idx_y + 36 + n * 17
        b.append(text(idx_x + 8, y, escape(s), 12, FAINT, MONO))
        b.append(text(idx_x + 8, y, escape(s), 12, TEAL, MONO, cls=c.appear(q0 + n * 0.3)))
    b.append(f'<path d="M{idx_x + idx_w + 2},{ans_y + ans_h / 2} h{ans_x - idx_x - idx_w - 8}" stroke="{TEAL}" stroke-width="1.4" '
             f'class="{c.appear(q0 + 1.2, 0.8)}" opacity="0.8"/>')
    b.append(f'<path d="M{ans_x - 7},{ans_y + ans_h / 2 - 4} l5,4 l-5,4" fill="none" stroke="{TEAL}" stroke-width="1.4" '
             f'class="{c.appear(q0 + 1.2, 0.8)}" opacity="0.8"/>')

    # the answer bubble with citation chips, the audit and the confidence gate
    a0 = q0 + 1.4
    g = c.appear(a0)
    b.append(f'<g class="{g}"><rect x="{ans_x}" y="{ans_y}" width="{ans_w}" height="{ans_h}" rx="10" fill="{SURFACE}" stroke="{TEAL}" stroke-opacity="0.8"/>'
             + text(ans_x + 10, ans_y + 16, "answer · Groq gpt-oss-20b", 11.5, TEAL, MONO)
             + f'<rect x="{ans_x + 10}" y="{ans_y + 24}" width="{ans_w - 30}" height="5" rx="2.5" fill="{FAINT}"/>'
             + f'<rect x="{ans_x + 10}" y="{ans_y + 34}" width="{ans_w - 70}" height="5" rx="2.5" fill="{FAINT}"/></g>')
    cy1, cy2 = ans_y + 48, ans_y + 72
    c1, w1 = pill(ans_x + 10, cy1, "[video 00:14:20]", AMBER, size=11, h=19, cls=c.appear(a0 + 0.5))
    c2, _ = pill(ans_x + 10 + w1 + 6, cy1, "[pdf p.4]", AMBER, size=11, h=19, cls=c.appear(a0 + 0.8))
    c3, w3 = pill(ans_x + 10, cy2, "LLM audit ✓", GREEN, size=11, h=19, filled=True, cls=c.appear(a0 + 1.4))
    c4, _ = pill(ans_x + 10 + w3 + 6, cy2, "gate 0.65", MUTED, size=11, h=19, cls=c.appear(a0 + 1.7), text_color=TEXT)
    b += [c1, c2, c3, c4]

    return frame(c, {
        "accent": TEAL, "kicker": "N.04 · MULTIMODAL RAG", "name": "Noesis",
        "pitch": "Multimodal RAG with per-claim citations across video, audio and PDFs.",
        "caption": "ingest → hybrid retrieval → cite",
        "stack": ["Python", "Groq", "ChromaDB", "Streamlit"], "status": ("team of 2", False),
        "title": "Noesis: multimodal RAG with per-claim citations",
        "desc": ("Project card for Noesis, built by a team of 2 in August 2026. Video, audio and PDF sources send chunks into an "
                 "index (Whisper with word-level timestamps, keyframes de-duplicated by perceptual hash, PyMuPDF plus RapidOCR plus "
                 "a Gemini vision model). Retrieval runs BM25 plus dense bge-small, fused with RRF and reranked by a cross-encoder. "
                 "In this illustrative run, a Groq gpt-oss-20b answer arrives with citation chips [video 00:14:20] and [pdf p.4], "
                 "checked by an LLM audit; a 0.65 confidence gate falls back to extractive answers. Stack: Python, Groq, ChromaDB, "
                 "Streamlit."),
    })


CARDS = {"lexguard": lexguard, "pikina": pikina, "resilion": resilion, "noesis": noesis}

if __name__ == "__main__":
    ASSETS.mkdir(exist_ok=True)
    for key, build in CARDS.items():
        out = ASSETS / f"card_{key}.svg"
        out.write_text(build(), encoding="utf-8")
        print(f"wrote assets/card_{key}.svg ({out.stat().st_size // 1024} KB)")
