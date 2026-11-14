"""Atlas featured systems: three cards, each with a looping diagram of how the system checks a model.

The diagrams illustrate mechanisms described in each repository; they are not recordings of real runs.
"""
from atlas_kit import (AMBER, BG, BG2, BG3, CYAN, GREEN, INK, INK2, INK3, LINE, LINE2, NARROW, RED, VIOLET, VOLT, WIDE,
                       after, comet, dot, flow_chips, label, mono_w, rrect, svg, t, window, wrap)

LOOP = 12          # seconds per diagram loop
PW, PH = 420, 352  # diagram panel size

FEATURED = [
    dict(key="lexguard", repo="LexGuard", index="01", kind="CONTRACT INTELLIGENCE", color=AMBER,
         hook=["Spot the trap.", "Check the evidence."],
         text="Reviews contracts under Indian law. Deterministic trap checks can overrule the model's risk rating, and every statute it cites is verified.",
         stack=["Node.js", "React", "MongoDB", "Redis"]),
    dict(key="pikina", repo="Pikina", index="02", kind="LOCAL DESKTOP AGENT", color=CYAN,
         hook=["Your machine.", "Your call."],
         text="An offline-first assistant for Windows and Linux. Every tool the model proposes is validated, and high-risk actions wait for your consent. Pre-alpha.",
         stack=["Python", "Electron", "Ollama", "SQLite"]),
    dict(key="noesis", repo="Noesis", index="03", kind="MULTIMODAL SEARCH", color=VIOLET,
         hook=["Find the moment.", "Cite the source."],
         text="Searches video, audio, PDFs and images, then links each answer to a timestamp or page. Hybrid retrieval, reranking and an LLM audit. Built with Apurva Patil.",
         stack=["Python", "ChromaDB", "Whisper", "Streamlit"]),
]

CSS = f"""
.nudge{{animation:nudge 1.6s ease-in-out infinite}}
@keyframes nudge{{50%{{transform:translateX(5px)}}}}
.caret{{animation:caret 1s steps(2) infinite}}
@keyframes caret{{50%{{opacity:0}}}}
"""


def _typed(x, y, value, size, start, end, name):
    """Monospace text revealed left to right: a cover the colour of the field slides away, caret first."""
    w = mono_w(value, size) + 6
    a, b = 100 * start / LOOP, 100 * end / LOOP
    css = (f"@keyframes {name}{{0%,{a:.2f}%{{transform:translateX(0)}}{b:.2f}%,96%{{transform:translateX({w:.0f}px)}}100%{{transform:translateX(0)}}}}"
           f".{name}{{animation:{name} {LOOP}s steps({max(1, len(value)) * 3}) infinite}}")
    body = (f'<clipPath id="{name}-c"><rect x="{x - 2:g}" y="{y - size - 2:g}" width="{w + 6:.0f}" height="{size * 1.5 + 4:g}"/></clipPath>'
            + t(x, y, value, size, INK, 500, mono=True)
            + f'<g clip-path="url(#{name}-c)"><g class="{name} fx"><rect x="{x - 1:g}" y="{y - size:g}" width="{w + 4:.0f}" height="{size * 1.5:g}" fill="{BG}"/>'
            + f'<rect class="caret" x="{x:g}" y="{y - size + 2:g}" width="2" height="{size + 2:g}" fill="{INK2}"/></g></g>')
    return css, body


def _bars(x, y, widths, color=LINE2, h=5, gap=10, op=1.0):
    """Grey placeholder lines standing in for body text."""
    return "".join(f'<rect x="{x:g}" y="{y + k * gap:g}" width="{w:g}" height="{h}" rx="{h / 2:g}" fill="{color}" opacity="{op:g}"/>' for k, w in enumerate(widths))


def _verdict(x, y, w, kind, line, color, cls, mark=""):
    out = f'<g class="{cls}">' + rrect(x, y, w, 58, 10, BG, color, 'stroke-opacity=".55"')
    out += f'<rect x="{x}" y="{y + 12}" width="3" height="34" rx="1.5" fill="{color}"/>'
    out += label(x + 14, y + 23, kind, color, 10.5)
    out += t(x + 14, y + 43, line, 14, INK, 600)
    if mark:
        out += t(x + w - 14, y + 43, mark, 15, color, 700, "end")
    return out + "</g>"


def _lexguard():
    css, b = [], []
    b.append(label(20, 28, "CONTRACT / CLAUSE REVIEW", AMBER, 11) + label(PW - 20, 28, "ILLUSTRATIVE", INK3, 10, "end"))
    # The contract page with four clauses
    b.append(rrect(20, 44, 196, 288, 10, BG, LINE2))
    rows = [("A", 60, [150, 132, 96]), ("B", 124, [150, 142, 150, 78]), ("C", 198, [150, 118]), ("D", 252, [150, 140, 64])]
    for letter, y, widths in rows:
        if letter == "B":
            b.append(f'<rect class="lx-flag" x="26" y="{y - 8}" width="184" height="64" rx="7" fill="{AMBER}" fill-opacity=".09" stroke="{AMBER}"/>')
            b.append(f'<rect class="lx-crit" x="26" y="{y - 8}" width="184" height="64" rx="7" fill="{RED}" fill-opacity=".1" stroke="{RED}" stroke-width="1.5"/>')
        b.append(t(36, y + 9, letter, 12, INK3, 700, mono=True))
        b.append(_bars(54, y, widths, "#3a4656"))
    b.append(f'<g class="lx-scan fx"><rect x="22" y="46" width="192" height="26" fill="url(#lx-beam)"/><path d="M22 72H214" stroke="{AMBER}" stroke-width="1.5"/></g>')
    css.append(f"@keyframes lx-scan{{0%{{transform:translateY(0);opacity:0}}3%{{opacity:1}}23%{{transform:translateY(256px);opacity:1}}26%,100%{{transform:translateY(256px);opacity:0}}}}"
               f".lx-scan{{animation:lx-scan {LOOP}s linear infinite}}")
    css.append(window("lx-flag", LOOP, 1.6, 4.6))
    css.append(after("lx-crit", LOOP, 4.9))
    # Verdicts arrive in order: the model, the rule that overrules it, the statute, the rewrite
    x = 232
    b.append(f'<path d="M216 148H{x}" stroke="{LINE2}" stroke-dasharray="2 3"/>')
    b.append(_verdict(x, 44, 168, "MODEL RATES IT", "Risk: low", VIOLET, "lx-1"))
    b.append(f'<g class="lx-2">{t(x + 154, 87, "OVERRULED", 9.5, RED, 600, "end", True, 0.8)}</g>')
    b.append(_verdict(x, 112, 168, "TRAP CHECK", "Critical", RED, "lx-2", "↑"))
    b.append(_verdict(x, 180, 168, "STATUTE VERIFIED", "Contract Act s.74", GREEN, "lx-3", "✓"))
    b.append(_verdict(x, 248, 168, "FAIRER REWRITE", "Drafted", VOLT, "lx-4", "✓"))
    b.append(label(x, 326, "36 TRAP PATTERNS", INK3, 10))
    for k, start in enumerate((2.6, 4.9, 6.9, 8.7)):
        css.append(after(f"lx-{k + 1}", LOOP, start))
    defs = (f'<linearGradient id="lx-beam" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{AMBER}" stop-opacity="0"/>'
            f'<stop offset="1" stop-color="{AMBER}" stop-opacity=".22"/></linearGradient>')
    return "".join(css), defs, "".join(b)


def _pikina():
    css, b = [], []
    b.append(label(20, 28, "DESKTOP / ACTION REVIEW", CYAN, 11) + label(PW - 20, 28, "ILLUSTRATIVE", INK3, 10, "end"))
    # What the person asked for
    b.append(rrect(20, 44, 380, 42, 10, BG, LINE2))
    b.append(t(34, 71, "›", 17, CYAN, 700, mono=True))
    c, body = _typed(52, 70, "delete the temp folder", 14, 0.4, 2.0, "pk-type")
    css.append(c)
    b.append(body)
    # Three gates light in turn
    gates = [("ROUTE", "regex → LLM", 2.3), ("VALIDATE", "tool + args", 4.4), ("CONSENT", "high risk: ask", 6.2)]
    for k, (name, sub, start) in enumerate(gates):
        gx = 20 + k * 130
        b.append(rrect(gx, 100, 120, 58, 10, BG, LINE2))
        b.append(f'<g class="pk-g{k}">' + rrect(gx, 100, 120, 58, 10, BG3, CYAN) + dot(gx + 104, 116, 3, CYAN, "") + "</g>")
        b.append(label(gx + 12, 122, name, INK, 11))
        b.append(t(gx + 12, 143, sub, 10.5, INK2, 400, mono=True))
        if k:
            b.append(f'<path d="M{gx - 9} 129h7" stroke="{INK3}" stroke-width="1.5"/>')
        css.append(after(f"pk-g{k}", LOOP, start))
    # The tool call the model proposes
    b.append(f'<g class="pk-call">' + rrect(20, 172, 380, 50, 10, BG, LINE2) + label(34, 190, "MODEL PROPOSES", VIOLET, 10)
             + t(34, 211, 'files.delete("~/tmp")', 14, INK, 500, mono=True) + "</g>")
    b.append(f'<g class="pk-risk"><rect x="304" y="184" width="84" height="26" rx="13" fill="{RED}" fill-opacity=".14" stroke="{RED}"/>'
             + t(346, 201.5, "HIGH RISK", 10.5, RED, 700, "middle", True, 0.8) + "</g>")
    css.append(after("pk-call", LOOP, 2.9))
    css.append(after("pk-risk", LOOP, 4.9))
    # The person decides
    b.append(f'<g class="pk-ask">' + rrect(20, 236, 380, 96, 12, BG3, CYAN, 'stroke-opacity=".6"')
             + t(36, 263, "Delete the folder ~/tmp?", 15, INK, 600)
             + t(36, 284, "Nothing runs until you approve.", 12.5, INK2)
             + rrect(210, 294, 84, 28, 8, BG, LINE2) + t(252, 313, "Deny", 13, INK2, 600, "middle")
             + rrect(304, 294, 84, 28, 8, BG, CYAN) + f'<rect class="pk-yes" x="304" y="294" width="84" height="28" rx="8" fill="{CYAN}"/>'
             + t(346, 313, "Approve", 13, INK, 700, "middle") + f'<g class="pk-yes">{t(346, 313, "Approve", 13, BG, 700, "middle")}</g>'
             + f'<g class="pk-done">{dot(40, 308, 3.5, GREEN, "")}{t(52, 312.5, "approved by you", 11.5, GREEN, 500, mono=True)}</g>'
             + "</g>")
    css.append(after("pk-ask", LOOP, 6.6))
    css.append(after("pk-yes", LOOP, 9.0, 0.12))
    css.append(after("pk-done", LOOP, 9.6))
    # Cursor travels to Approve and clicks
    b.append(f'<g class="pk-cur fx"><path d="M0 0L0 17L4.5 13L8 20.5L11 19L7.6 11.8L13.5 11.5Z" fill="{INK}" stroke="{BG}" stroke-width="1.2"/></g>')
    css.append(f"@keyframes pk-cur{{0%,56%{{transform:translate(250px,366px);opacity:0}}60%{{opacity:1}}73%,74.5%{{transform:translate(352px,306px)}}"
               f"75.2%{{transform:translate(352px,309px)}}76%,92%{{transform:translate(352px,306px);opacity:1}}96%,100%{{transform:translate(352px,306px);opacity:0}}}}"
               f".pk-cur{{animation:pk-cur {LOOP}s ease-in-out infinite}}")
    return "".join(css), "", "".join(b)


def _noesis():
    css, b = [], []
    b.append(label(20, 28, "LIBRARY / CITED SEARCH", VIOLET, 11) + label(PW - 20, 28, "ILLUSTRATIVE", INK3, 10, "end"))
    b.append(rrect(20, 44, 380, 42, 10, BG, LINE2))
    b.append(f'<circle cx="38" cy="64" r="5.5" fill="none" stroke="{VIOLET}" stroke-width="1.8"/><path d="M42 68.5l4.5 4.5" stroke="{VIOLET}" stroke-width="1.8" stroke-linecap="round"/>')
    c, body = _typed(56, 70, "where is backprop derived?", 14, 0.4, 2.1, "no-type")
    css.append(c)
    b.append(body)
    # Four kinds of source, scanned left to right
    kinds = ["VIDEO", "AUDIO", "PDF", "IMAGE"]
    for k, name in enumerate(kinds):
        sx = 20 + k * 97
        hit = name in ("VIDEO", "PDF")
        b.append(rrect(sx, 100, 89, 84, 10, BG, LINE2))
        if hit:
            b.append(f'<g class="no-hit">' + rrect(sx, 100, 89, 84, 10, BG3, VIOLET) + "</g>")
        b.append(label(sx + 10, 119, name, INK2, 10))
        ix, iy = sx + 10, 130
        if name == "VIDEO":
            b.append(f'<rect x="{ix}" y="{iy}" width="69" height="34" rx="4" fill="none" stroke="{INK3}"/><path d="M{ix + 29} {iy + 10}v14l12-7z" fill="{INK3}"/>'
                     f'<path d="M{ix} {iy + 44}h69" stroke="{LINE2}" stroke-width="3" stroke-linecap="round"/>'
                     f'<circle class="no-hit" cx="{ix + 44}" cy="{iy + 44}" r="4" fill="{VIOLET}"/>')
        elif name == "AUDIO":
            heights = [8, 18, 28, 14, 34, 22, 10, 26, 16, 30, 12, 20]
            b.append("".join(f'<rect x="{ix + j * 6}" y="{iy + 22 - hh / 2:g}" width="3" height="{hh}" rx="1.5" fill="{INK3}"/>' for j, hh in enumerate(heights)))
        elif name == "PDF":
            b.append(f'<path d="M{ix + 12} {iy}h30l12 12v32h-42z" fill="none" stroke="{INK3}"/>' + _bars(ix + 19, iy + 16, [28, 28, 18], INK3, 3, 8))
            b.append(f'<rect class="no-hit" x="{ix + 17}" y="{iy + 22}" width="32" height="7" rx="2" fill="{VIOLET}" fill-opacity=".5"/>')
        else:
            b.append(f'<rect x="{ix}" y="{iy}" width="69" height="44" rx="4" fill="none" stroke="{INK3}"/><path d="M{ix + 6} {iy + 38}l16-18 12 12 9-8 20 14z" fill="{INK3}" opacity=".6"/>'
                     f'<circle cx="{ix + 53}" cy="{iy + 12}" r="5" fill="{INK3}" opacity=".6"/>')
    b.append(f'<g class="no-scan fx"><rect x="20" y="100" width="30" height="84" fill="url(#no-beam)"/><path d="M50 100V184" stroke="{VIOLET}" stroke-width="1.5"/></g>')
    css.append(f"@keyframes no-scan{{0%,17%{{transform:translateX(0);opacity:0}}19%{{opacity:1}}36%{{transform:translateX(350px);opacity:1}}39%,100%{{transform:translateX(350px);opacity:0}}}}"
               f".no-scan{{animation:no-scan {LOOP}s linear infinite}}")
    css.append(after("no-hit", LOOP, 4.5))
    # Retrieval: two retrievers, then a reranker
    steps = [("BM25", 20, 76), ("DENSE", 116, 84), ("RERANK", 228, 92), ("AUDIT", 344, 56)]
    for k, (name, sx, sw) in enumerate(steps):
        b.append(rrect(sx, 198, sw, 30, 15, BG, LINE2))
        b.append(f'<g class="no-s{k}">' + rrect(sx, 198, sw, 30, 15, BG3, VIOLET) + "</g>")
        b.append(label(sx + sw / 2, 217.5, name, INK, 10.5, "middle"))
    b.append(t(106, 218, "+", 14, INK3, 600, "middle", True))
    b.append(f'<path d="M206 213h16m-5-4 5 4-5 4M326 213h12m-5-4 5 4-5 4" fill="none" stroke="{INK3}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>')
    for k, start in enumerate((5.0, 5.0, 6.0, 9.4)):
        css.append(after(f"no-s{k}", LOOP, start))
    # The answer, with the places it came from
    b.append(f'<g class="no-ans">' + rrect(20, 242, 380, 90, 12, BG3, VIOLET, 'stroke-opacity=".6"') + label(36, 262, "ANSWER", VIOLET, 10)
             + _bars(36, 272, [330, 248], "#4a5567", 5, 11) + "</g>")
    b.append(f'<g class="no-c1"><rect x="36" y="298" width="162" height="24" rx="12" fill="{BG}" stroke="{VIOLET}"/><path d="M48 304v12l9-6z" fill="{VIOLET}"/>'
             + t(63, 314.5, "lecture 07 · 12:41", 11, INK, 500, mono=True) + "</g>")
    b.append(f'<g class="no-c2"><rect x="206" y="298" width="142" height="24" rx="12" fill="{BG}" stroke="{VIOLET}"/><path d="M217 304h8l3 3v9h-11z" fill="none" stroke="{VIOLET}" stroke-width="1.3"/>'
             + t(234, 314.5, "notes.pdf · p.7", 11, INK, 500, mono=True) + "</g>")
    b.append(f'<g class="no-s3">{t(384, 315, "✓", 15, GREEN, 700, "end")}</g>')
    css.append(after("no-ans", LOOP, 6.8))
    css.append(after("no-c1", LOOP, 7.7))
    css.append(after("no-c2", LOOP, 8.4))
    defs = (f'<linearGradient id="no-beam" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{VIOLET}" stop-opacity="0"/>'
            f'<stop offset="1" stop-color="{VIOLET}" stop-opacity=".2"/></linearGradient>')
    return "".join(css), defs, "".join(b)


DIAGRAMS = {"lexguard": _lexguard, "pikina": _pikina, "noesis": _noesis}


def _copy(p, x, y, width, name_size):
    """Index, name, hook, description, stack and call to action. Returns (svg, bottom y)."""
    color = p["color"]
    out = [dot(x + 3, y - 4, 3.5, color), label(x + 14, y, f'{p["index"]} / {p["kind"]}', color, 12)]
    y += name_size + 14
    out.append(t(x - 2, y, p["repo"], name_size, INK, 800, ls=-1.5))
    y += 40
    out.append(t(x, y, p["hook"][0], 22, INK, 600))
    out.append(t(x, y + 29, p["hook"][1], 22, color, 600))
    y += 64
    for line in wrap(p["text"], width, 15):
        out.append(t(x, y, line, 15, INK2))
        y += 22
    y += 8
    chips, bottom = flow_chips(x, y, p["stack"], width, INK2, 11.5, 24)
    out.append(chips)
    return "".join(out), bottom


def _cta(x, y, color):
    return (label(x, y, "OPEN REPOSITORY", color, 12)
            + f'<path class="nudge" d="M{x + 142} {y - 4}h20m-6-5 6 5-6 5" fill="none" stroke="{color}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>')


def featured(index, mobile=False) -> str:
    p = FEATURED[index]
    css, defs, diagram = DIAGRAMS[p["key"]]()
    title = f'{p["repo"]} — {p["hook"][0]} {p["hook"][1]}'
    desc = f'{p["text"]} Stack: {", ".join(p["stack"])}. The animated diagram is illustrative.'
    if mobile:
        copy, bottom = _copy(p, 24, 40, NARROW - 48, 50)
        py = bottom + 50
        h = py + PH + 18
        body = copy + _cta(24, bottom + 30, p["color"])
        body += rrect(18, py, PW, PH, 14, BG2, LINE) + f'<g transform="translate(18 {py})">{diagram}</g>'
        body += comet(18, py, PW, PH, 14, p["color"], 10, index * 3)
        return svg(NARROW, h, title, desc, body, CSS + css, defs, glow=p["color"])
    h = 400
    copy, bottom = _copy(p, 28, 44, 384, 58)
    body = copy + _cta(28, h - 32, p["color"])
    px, py = WIDE - PW - 24, 24
    body += rrect(px, py, PW, PH, 14, BG2, LINE) + f'<g transform="translate({px} {py})">{diagram}</g>'
    body += comet(px, py, PW, PH, 14, p["color"], 10, index * 3)
    return svg(WIDE, h, title, desc, body, CSS + css, defs, glow=p["color"])


if __name__ == "__main__":
    import sys
    sys.stdout.write(featured(int(sys.argv[1]), "--mobile" in sys.argv))
