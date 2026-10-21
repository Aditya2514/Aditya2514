"""Render assets/terminal.svg: a terminal that types who I am, what I'm building and my latest real commits.

  python3 scripts/build_terminal.py --github LOGIN                 # GitHub REST API, needs GH_TOKEN (Actions)
  python3 scripts/build_terminal.py --from-git DIR... --emails A,B  # offline preview from local clones

The `git log` block is the four most recent commits from the data source, so the card stays live.
Never fails the build: if data can't be fetched, the existing SVG is left untouched.
"""

import sys
from pathlib import Path
from xml.sax.saxutils import escape

from github_activity import run_card
from theme import AMBER, BORDER, FAINT, MONO, MUTED, PANEL, SURFACE, TEAL, TEXT

OUT = Path(__file__).resolve().parent.parent / "assets" / "terminal.svg"
PERSON = "#c9d1d9"

W, H = 900, 340
X0, Y0, LINE_H = 32, 76, 22
FONT = 14
CHAR_W = FONT * 0.6          # textLength pins every glyph to this advance, whatever mono font loads
MAX_CHARS = int((W - 2 * X0) / CHAR_W)

WHOAMI = "Aditya Singh · BS Data Science @ IIT Madras (CGPA 9.0) · Scaler School of Technology"
NOW = "Building LLM agents that are safe to act on"
PROJECTS = ["LexGuard", "Pikina", "Noesis", "Resilion", "Meta_OpenEnv", "codecrafters-shell-cpp"]

# Timing (seconds)
TYPE_S = 0.075        # per typed character
THINK_S = 0.35        # after Enter, before output
OUT_STEP_S = 0.09     # between consecutive output lines
NEXT_PROMPT_S = 0.15  # output -> next prompt
IDLE_S = 0.8          # at a fresh prompt before typing
OPEN_HOLD_S = 1.2     # after the clear (whoami already shown) before typing starts
END_HOLD_S = 3.0      # everything visible, cursor blinking (this is the start of the cycle)
BLINK_S = 0.5


def commit_lines(commits: list[dict]) -> list[list[tuple[str, str]]]:
    latest = commits[:4]
    pad = max(len(c["repo"]) for c in latest)
    lines = []
    for c in latest:
        head = f"{c['sha'][:7]} {c['repo'].ljust(pad)}  "
        room = MAX_CHARS - len(head)
        msg = c["message_first_line"]
        if len(msg) > room:
            msg = msg[: room - 1].rstrip() + "…"
        lines.append([(c["sha"][:7] + " ", AMBER), (c["repo"].ljust(pad) + "  ", TEAL), (msg, PERSON)])
    return lines


def script(commits: list[dict]) -> list[tuple[str, list]]:
    """The session as (command, output lines); each output line is a list of (text, colour) runs."""
    return [
        ("whoami", [[(WHOAMI, PERSON)]]),
        ("cat now.txt", [[(NOW, AMBER)]]),
        ("git log --oneline -4", commit_lines(commits)),
        ("ls ~/projects", [[("  ".join(PROJECTS), TEAL)]]),
    ]


def build_lines(session):
    """Flatten into rows: (runs, kind, command index). The last row is the empty prompt."""
    rows = []
    for i, (cmd, outputs) in enumerate(session):
        rows.append(([("$ ", TEAL), (cmd, TEXT)], "cmd", i))
        rows += [(runs, "out", i) for runs in outputs]
    rows.append(([("$ ", TEAL)], "prompt", len(session)))
    return rows


def timeline(rows):
    """Keyframes for every row's visible character count and for the cursor (x chars, row, on/off).

    The cycle OPENS on the finished session (every line visible, cursor blinking at the last prompt), so
    a frozen first frame or thumbnail shows everything. After END_HOLD_S the screen "clears" back to
    `whoami` + its output, then types the remaining commands; when the last prompt appears the loop
    wraps straight into the finished state again, so the hold and the end look identical.
    """
    t = 0.0
    shown = {r: [] for r in range(len(rows))}
    cur_x, cur_row, cur_on = [], [], []
    full = {r: sum(len(s) for s, _ in runs) for r, (runs, _, _) in enumerate(rows)}
    last = len(rows) - 1

    first_cmd_rows = {r for r, (_, _, i) in enumerate(rows) if i == 0}
    second_prompt = next(r for r, (_, kind, i) in enumerate(rows) if kind == "cmd" and i == 1)

    def set_row(r, n):
        shown[r].append((t, n))

    def cursor(row, x):
        cur_row.append((t, row))
        cur_x.append((t, x))

    def idle(duration):
        nonlocal t
        steps = int(duration / BLINK_S)
        for s in range(1, steps + 1):
            cur_on.append((t + s * BLINK_S, 0 if s % 2 else 1))
        t += duration
        cur_on.append((t, 1))

    # Finished screen, held
    for r in range(len(rows)):
        set_row(r, full[r])
    cursor(last, 2)
    cur_on.append((0.0, 1))
    idle(END_HOLD_S)

    # "clear": back to whoami + output, cursor at the next prompt
    for r in range(len(rows)):
        set_row(r, full[r] if r in first_cmd_rows else (2 if r == second_prompt else 0))
    cursor(second_prompt, 2)
    idle(OPEN_HOLD_S)

    r = second_prompt
    while r < len(rows):
        runs, kind, _ = rows[r]
        if kind == "prompt":
            break
        # type the command after "$ "
        for k in range(3, full[r] + 1):
            t += TYPE_S
            set_row(r, k)
            cursor(r, k)
        t += THINK_S
        r += 1
        while r < len(rows) and rows[r][1] == "out":
            set_row(r, full[r])
            cursor(r + 1, 0)
            t += OUT_STEP_S
            r += 1
        t += NEXT_PROMPT_S - OUT_STEP_S
        set_row(r, 2)
        cursor(r, 2)
        if rows[r][1] != "prompt":
            idle(IDLE_S)
    idle(BLINK_S * 2)  # one blink at the final prompt, then wrap into the identical held state
    cycle = t
    # Close every track at the cycle end with its opening value so the loop restarts cleanly
    for r in shown:
        shown[r].append((cycle, shown[r][0][1]))
    cur_x.append((cycle, cur_x[0][1]))
    cur_row.append((cycle, cur_row[0][1]))
    cur_on.append((cycle, 1))
    return cycle, shown, cur_x, cur_row, cur_on


def _discrete(attr, frames, cycle, fmt="{:.1f}"):
    """One looping SMIL animation that steps through (time, value) keyframes."""
    times = ";".join(f"{min(tt / cycle, 1):.5f}" for tt, _ in frames)
    values = ";".join(fmt.format(v) for _, v in frames)
    return (
        f'<animate attributeName="{attr}" calcMode="discrete" dur="{cycle:.3f}s" repeatCount="indefinite" '
        f'keyTimes="{times}" values="{values}"/>'
    )


def _dedupe(frames):
    """Drop keyframes that repeat the previous value (keeps the first and last)."""
    out = [frames[0]]
    for f in frames[1:-1]:
        if f[1] != out[-1][1]:
            out.append(f)
    out.append(frames[-1])
    return out


def render(commits: list[dict], source: str, today: str) -> str:
    session = script(commits)
    rows = build_lines(session)
    cycle, shown, cur_x, cur_row, cur_on = timeline(rows)

    def baseline(r):
        return Y0 + r * LINE_H

    clips, texts = [], []
    for r, (runs, _, _) in enumerate(rows):
        n = sum(len(s) for s, _ in runs)
        y = baseline(r)
        frames = _dedupe(shown[r])
        # Base attribute = fully typed, so a viewer without SMIL sees the finished screen
        clips.append(
            f'<clipPath id="row{r}"><rect x="{X0 - 1}" y="{y - 15}" width="{n * CHAR_W + 2:.1f}" height="{LINE_H}">'
            + _discrete("width", [(tt, k * CHAR_W + (1 if k else 0)) for tt, k in frames], cycle)
            + "</rect></clipPath>"
        )
        spans = "".join(f'<tspan fill="{c}">{escape(s)}</tspan>' for s, c in runs)
        weight = ' font-weight="700"' if runs[0][0] == "$ " else ""
        texts.append(
            f'<text x="{X0}" y="{y}" clip-path="url(#row{r})" xml:space="preserve" font-family="{MONO}" font-size="{FONT}"{weight} '
            f'textLength="{n * CHAR_W:.1f}" lengthAdjust="spacingAndGlyphs" fill="{TEXT}">{spans}</text>'
        )

    last = len(rows) - 1
    cursor = (
        f'<rect x="{X0 + 2 * CHAR_W:.1f}" y="{baseline(last) - 13}" width="{CHAR_W:.1f}" height="17" rx="1.5" fill="{TEAL}" opacity="0.9">'
        + _discrete("x", [(tt, X0 + k * CHAR_W) for tt, k in _dedupe(cur_x)], cycle)
        + _discrete("y", [(tt, baseline(r) - 13) for tt, r in _dedupe(cur_row)], cycle)
        + _discrete("opacity", _dedupe(cur_on), cycle, "{:d}")
        + "</rect>"
    )

    chrome = (
        f'<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="16" fill="{SURFACE}" stroke="{BORDER}"/>'
        f'<path d="M0.5,40 V16.5 A16,16 0 0 1 16.5,0.5 H{W - 16.5} A16,16 0 0 1 {W - 0.5},16.5 V40 Z" fill="{PANEL}"/>'
        f'<line x1="0.5" y1="40.5" x2="{W - 0.5}" y2="40.5" stroke="{BORDER}"/>'
        + "".join(f'<circle cx="{x}" cy="20.5" r="5.5" fill="{FAINT}"/>' for x in (26, 46, 66))
        + f'<text x="{W / 2}" y="25" text-anchor="middle" font-family="{MONO}" font-size="12" fill="{MUTED}">~/aditya — fish</text>'
        + f'<text x="{W - 24}" y="25" text-anchor="end" font-family="{MONO}" font-size="10.5" fill="{MUTED}">'
        f"git log: {escape(source)} · {today}</text>"
    )

    recent = "; ".join(f"{c['repo']}: {c['message_first_line']}" for c in commits[:4])
    desc = (
        f"A terminal session. whoami: {WHOAMI}. cat now.txt: {NOW}. "
        f"git log --oneline -4 lists the four most recent commits ({recent}). "
        f"ls ~/projects: {', '.join(PROJECTS)}."
    )
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="100%" role="img" aria-labelledby="t d">',
        '<title id="t">Terminal: who I am, what I am building, my latest commits</title>',
        f'<desc id="d">{escape(desc)}</desc>',
        "<defs>" + "".join(clips) + "</defs>",
        chrome,
        *texts,
        cursor,
        "</svg>",
    ]
    return "\n".join(parts) + "\n"


if __name__ == "__main__":
    sys.exit(run_card("terminal", OUT, render))
