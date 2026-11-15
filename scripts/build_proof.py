#!/usr/bin/env python3
"""Proof of Work: check every claim on the profile against the line of code behind it, then draw the page.

  python3 scripts/build_proof.py                 # read the repos from GitHub (Actions; GH_TOKEN optional)
  python3 scripts/build_proof.py --local DIR     # read local clones in DIR/<repo> (offline preview)
  python3 scripts/build_proof.py --render-only   # redraw from data/proof.json without checking

A claim is VERIFIED when its file, at the repository's current default-branch commit, still contains its
needle; the link then points at that exact line, pinned to that commit. It is STALE when the file is gone
or the needle no longer appears. If a repository can't be reached at all, the last result is carried over
and marked as such, so a network blip never rewrites history in either direction.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent.parent
CLAIMS = ROOT / "data" / "claims.json"
STATE = ROOT / "data" / "proof.json"
ART = ROOT / "assets" / "proof"
README = ROOT / "README.md"
START, END = "<!-- LEDGER:START -->", "<!-- LEDGER:END -->"
API = "https://api.github.com"

# Paper and ink. The paper objects (receipt, tags) look the same in both themes; only the desk changes.
PAPER, PAPER_EDGE, INK, INK_SOFT, INK_FAINT = "#f8f5ec", "#ddd5c2", "#1f1d1a", "#5d574c", "#9a927f"
RED, GREEN, AMBER = "#c8372d", "#2f6b3f", "#a86a12"
DESK = {
    "dark": {"bg": "#12141a", "line": "#22262f", "text": "#f1ede4", "muted": "#a3a7ae", "slot": "#050608"},
    "light": {"bg": "#ece7dc", "line": "#ddd6c7", "text": "#1b1a17", "muted": "#5f5a50", "slot": "#2a2824"},
}
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, 'Liberation Mono', monospace"
SERIF = "Georgia, 'Times New Roman', Times, serif"
SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif"


# ----------------------------------------------------------------------------------------------- checking

def _get(url: str, raw: bool = False):
    headers = {"User-Agent": "proof-of-work-profile", "Accept": "application/vnd.github.raw" if raw else "application/vnd.github+json"}
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=30) as res:
        body = res.read()
    return body.decode("utf-8", "replace") if raw else json.loads(body)


class RemoteRepo:
    """Default-branch head of a GitHub repository; files are read at that exact commit."""

    def __init__(self, owner: str, name: str):
        self.owner, self.name = owner, name
        meta = _get(f"{API}/repos/{owner}/{name}")
        self.branch = meta["default_branch"]
        self.sha = _get(f"{API}/repos/{owner}/{name}/commits/{urllib.parse.quote(self.branch)}")["sha"]

    def read(self, path: str) -> str | None:
        try:
            return _get(f"{API}/repos/{self.owner}/{self.name}/contents/{urllib.parse.quote(path)}?ref={self.sha}", raw=True)
        except urllib.error.HTTPError as err:
            if err.code == 404:
                return None
            raise

    def recent(self, n: int = 2) -> list[dict]:
        rows = _get(f"{API}/repos/{self.owner}/{self.name}/commits?sha={self.sha}&per_page=10")
        return [{"sha": r["sha"], "date": r["commit"]["committer"]["date"][:10],
                 "subject": r["commit"]["message"].splitlines()[0]} for r in rows if len(r.get("parents", [])) <= 1][:n]


class LocalRepo:
    """A local clone, for previews without network access."""

    def __init__(self, base: Path, name: str):
        self.dir = base / name
        git = lambda *a: subprocess.run(["git", "-C", str(self.dir), *a], capture_output=True, text=True, check=True).stdout.strip()
        self.sha = git("rev-parse", "HEAD")
        self.branch = git("branch", "--show-current") or "HEAD"

    def read(self, path: str) -> str | None:
        file = self.dir / path
        return file.read_text(errors="replace") if file.is_file() else None

    def recent(self, n: int = 2) -> list[dict]:
        out = subprocess.run(["git", "-C", str(self.dir), "log", f"-{n}", "--no-merges", "--format=%H%x09%cs%x09%s", self.sha],
                             capture_output=True, text=True, check=True).stdout
        return [dict(zip(("sha", "date", "subject"), line.split("\t", 2))) for line in out.splitlines() if line]


def find_line(text: str | None, needle: str) -> int | None:
    if text is None:
        return None
    for number, line in enumerate(text.splitlines(), 1):
        if needle in line:
            return number
    return None


def check(spec: dict, previous: dict, open_repo) -> dict:
    owner = spec["owner"]
    old = {c["id"]: c for c in previous.get("claims", [])}
    claims, repos, recent = [], {}, []
    old_recent = [r for r in previous.get("recent", [])]
    for ex in spec["exhibits"]:
        try:
            repo = open_repo(owner, ex["repo"])
            repos[ex["repo"]] = {"sha": repo.sha, "branch": repo.branch}
        except Exception as err:  # unreachable: carry the last known result forward
            print(f"warn: {ex['repo']}: {err}", file=sys.stderr)
            repo = None
            if ex["repo"] in previous.get("repos", {}):
                repos[ex["repo"]] = previous["repos"][ex["repo"]]
        try:
            if repo is None:
                raise RuntimeError("unreachable")
            recent += [{**c, "repo": ex["repo"]} for c in repo.recent()]
        except Exception as err:
            print(f"warn: {ex['repo']} history: {err}", file=sys.stderr)
            recent += [r for r in old_recent if r.get("repo") == ex["repo"]]
        for i, claim in enumerate(ex["claims"], 1):
            cid = f"{ex['id']}{i}"
            if repo is None:
                prior = old.get(cid)
                claims.append({**prior, "carried": True} if prior else {"id": cid, "status": "unchecked", "line": None, "sha": None})
                continue
            try:
                text = repo.read(claim["path"])
            except Exception as err:
                print(f"warn: {ex['repo']}/{claim['path']}: {err}", file=sys.stderr)
                prior = old.get(cid)
                claims.append({**prior, "carried": True} if prior else {"id": cid, "status": "unchecked", "line": None, "sha": None})
                continue
            line = find_line(text, claim["needle"])
            claims.append({"id": cid, "status": "verified" if line else "stale", "line": line, "sha": repo.sha})
    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    recent.sort(key=lambda r: (r["date"], r["repo"]), reverse=True)
    return {"audited_at": now, "repos": repos, "claims": claims, "recent": recent}


# ----------------------------------------------------------------------------------------------- helpers

def counts(state: dict) -> dict:
    statuses = [c["status"] for c in state["claims"]]
    return {"total": len(statuses), "verified": statuses.count("verified"), "stale": statuses.count("stale"),
            "unchecked": statuses.count("unchecked")}


def stamp_date(iso: str) -> str:
    return datetime.fromisoformat(iso.replace("Z", "+00:00")).strftime("%d %b %Y").upper()


def stamp_time(iso: str) -> str:
    return datetime.fromisoformat(iso.replace("Z", "+00:00")).strftime("%d %b %Y %H:%MZ").upper()


def barcode(seed: str, x: float, y: float, width: float, height: float, color: str) -> str:
    """Decorative bars derived from a hash, so each commit prints a different code."""
    digest = hashlib.sha256(seed.encode()).digest()
    widths = [1 + b % 3 for b in digest] * 3
    bars, cursor, out = [], 0.0, []
    for i, w in enumerate(widths):
        if cursor + w > width:
            break
        if i % 2 == 0:
            bars.append((cursor, w))
        cursor += w + (1 + digest[i % len(digest)] % 2)
    for bx, bw in bars:
        out.append(f'<rect x="{x + bx:.1f}" y="{y}" width="{bw}" height="{height}" fill="{color}"/>')
    return "".join(out)


def wrap(text: str, limit: int) -> list[str]:
    lines, current = [], ""
    for word in text.split():
        if current and len(current) + 1 + len(word) > limit:
            lines.append(current)
            current = word
        else:
            current = f"{current} {word}".strip()
    return lines + ([current] if current else [])


def zigzag(x: float, y: float, width: float, tooth: float = 8) -> str:
    """Torn bottom edge, drawn right to left so it closes a path that went down the right side."""
    points, n = [], int(width // tooth)
    for i in range(n, -1, -1):
        px = x + width * i / n
        points.append(f"{px:.1f},{y + (tooth * 0.6 if i % 2 else 0):.1f}")
    return " L".join(points)


# ----------------------------------------------------------------------------------------------- receipt hero

def receipt_lines(spec: dict, state: dict) -> list[tuple[str, str]]:
    c = counts(state)
    width = 32
    row = lambda left, right: left + right.rjust(width - len(left))
    rule = "-" * width
    lines = [
        ("title", "PROOF OF WORK"),
        ("center", "ADITYA SINGH"),
        ("center", "IIT MADRAS · SCALER SOT"),
        ("plain", rule),
        ("plain", row("CLAIMS ON THIS PAGE", str(c["total"]))),
        ("plain", row("CHECKED AGAINST SOURCE", str(c["total"] - c["unchecked"]))),
        ("ok", row("VERIFIED", str(c["verified"]))),
        ("bad" if c["stale"] else "plain", row("STALE", str(c["stale"]))),
        ("plain", row("REPOSITORIES READ", str(len(spec["exhibits"])))),
        ("plain", rule),
        ("plain", row("LAST AUDIT", stamp_time(state["audited_at"]))),
        ("plain", row("NEXT AUDIT", "IN < 6 HOURS")),
        ("plain", rule),
        ("center", "THE MODEL PROPOSES."),
        ("center", "THE SYSTEM CHECKS."),
        ("center", "THE PERSON STAYS IN CONTROL."),
    ]
    return lines


def receipt(spec: dict, state: dict, x: float, top: float, width: float = 300) -> tuple[str, float]:
    """The receipt as it sits fully printed; returns (svg, height)."""
    lh, pad = 19, 22
    lines = receipt_lines(spec, state)
    body_h = pad + len(lines) * lh + 14 + 34 + 26
    out = [f'<path d="M{x},{top} L{x + width},{top} L{x + width},{top + body_h} L{zigzag(x, top + body_h, width)} Z" '
           f'fill="{PAPER}" stroke="{PAPER_EDGE}" stroke-width="1"/>']
    y = top + pad + 8
    for kind, text in lines:
        color = {"ok": GREEN, "bad": RED}.get(kind, INK)
        if kind == "title":
            out.append(f'<text x="{x + width / 2}" y="{y + 2}" text-anchor="middle" font-family="{MONO}" font-size="17" '
                       f'font-weight="700" letter-spacing="3" fill="{INK}">{escape(text)}</text>')
        elif kind == "center":
            out.append(f'<text x="{x + width / 2}" y="{y}" text-anchor="middle" font-family="{MONO}" font-size="12.5" '
                       f'fill="{INK_SOFT}">{escape(text)}</text>')
        else:
            out.append(f'<text x="{x + 20}" y="{y}" font-family="{MONO}" font-size="12.5" fill="{color}" '
                       f'xml:space="preserve">{escape(text)}</text>')
        y += lh
    seed = "".join(sorted(r["sha"] for r in state["repos"].values() if r.get("sha")))
    out.append(barcode(seed, x + 34, y + 2, width - 68, 34, INK))
    out.append(f'<text x="{x + width / 2}" y="{y + 52}" text-anchor="middle" font-family="{MONO}" font-size="10" '
               f'letter-spacing="1.5" fill="{INK_FAINT}">KEEP THIS RECEIPT · DIFF IT LATER</text>')
    return "".join(out), body_h + 6


def stamp(cx: float, cy: float, state: dict, scale: float = 1.0) -> str:
    c = counts(state)
    label = "VERIFIED" if c["verified"] == c["total"] else "PARTIAL"
    ink = RED if label == "VERIFIED" else AMBER
    w, h = 292 * scale, 100 * scale
    return (
        f'<g transform="translate({cx} {cy}) rotate(-8)"><g class="stamp" filter="url(#worn)" opacity="0.9">'
        f'<rect x="{-w / 2}" y="{-h / 2}" width="{w}" height="{h}" rx="{8 * scale}" fill="none" stroke="{ink}" stroke-width="{4 * scale}"/>'
        f'<rect x="{-w / 2 + 7 * scale}" y="{-h / 2 + 7 * scale}" width="{w - 14 * scale}" height="{h - 14 * scale}" rx="{4 * scale}" '
        f'fill="none" stroke="{ink}" stroke-width="{1.5 * scale}"/>'
        f'<text x="0" y="{6 * scale}" text-anchor="middle" font-family="{MONO}" font-size="{38 * scale}" font-weight="800" '
        f'letter-spacing="{5 * scale}" fill="{ink}">{label}</text>'
        f'<text x="0" y="{31 * scale}" text-anchor="middle" font-family="{MONO}" font-size="{11.5 * scale}" font-weight="700" '
        f'letter-spacing="{1 * scale}" fill="{ink}">{c["verified"]} OF {c["total"]} CLAIMS · {stamp_date(state["audited_at"])}</text>'
        f'</g></g>'
    )


def defs(feed_px: float) -> str:
    return (
        '<defs><filter id="worn" x="-10%" y="-20%" width="120%" height="140%">'
        '<feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" seed="7" result="n"/>'
        '<feDisplacementMap in="SourceGraphic" in2="n" scale="2.2" result="d"/>'
        '<feColorMatrix in="n" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 -1.2 1.42" result="holes"/>'
        '<feComposite in="d" in2="holes" operator="in"/></filter>'
        '<filter id="shadow" x="-10%" y="-10%" width="130%" height="130%"><feDropShadow dx="0" dy="6" stdDeviation="7" '
        'flood-color="#000" flood-opacity="0.28"/></filter></defs>'
        '<style>'
        f'.feed{{animation:feed 2.6s steps(18,end) .35s both}}'
        f'@keyframes feed{{from{{transform:translateY(-{feed_px:.0f}px)}}to{{transform:translateY(0)}}}}'
        '.stamp{transform-box:fill-box;transform-origin:center;animation:thump .32s cubic-bezier(.2,1.5,.45,1) 3.2s both}'
        '@keyframes thump{0%{opacity:0;transform:scale(1.9)}100%{opacity:1;transform:scale(1)}}'
        '.led{animation:led .5s steps(2,start) 6 .35s both}'
        '@keyframes led{to{opacity:.25}}'
        '@media (prefers-reduced-motion: reduce){.feed,.stamp,.led{animation:none}}'
        '</style>'
    )


def printer(x: float, y: float, width: float, theme: dict) -> str:
    return (f'<rect x="{x - 18}" y="{y - 14}" width="{width + 36}" height="26" rx="13" fill="{theme["slot"]}"/>'
            f'<rect x="{x - 6}" y="{y - 2}" width="{width + 12}" height="4" rx="2" fill="#000" opacity="0.6"/>'
            f'<circle class="led" cx="{x + width + 4}" cy="{y - 1}" r="3.2" fill="#3ddc84"/>')


def hero(spec: dict, state: dict, mode: str, mobile: bool) -> str:
    t = DESK[mode]
    rw = 300
    if mobile:
        W = 600
        rx, slot_y = (W - rw) / 2, 40
    else:
        W = 1000
        rx, slot_y = 64, 40
    paper, ph = receipt(spec, state, rx, slot_y, rw)
    receipt_bottom = slot_y + ph
    parts = []
    if mobile:
        ty = receipt_bottom + 56
        text = [
            f'<text x="40" y="{ty}" font-family="{MONO}" font-size="13" letter-spacing="3" fill="{RED}">A PROFILE YOU CAN AUDIT</text>',
            f'<text x="40" y="{ty + 48}" font-family="{SERIF}" font-size="40" fill="{t["text"]}">Don’t take my word</text>',
            f'<text x="40" y="{ty + 94}" font-family="{SERIF}" font-size="40" font-style="italic" fill="{t["text"]}">for it.</text>',
        ]
        for i, line in enumerate(wrap("Every claim below links to the exact line of code behind it. "
                                      "A bot re-reads those lines every six hours and stamps what still holds.", 56)):
            text.append(f'<text x="40" y="{ty + 136 + i * 24}" font-family="{SANS}" font-size="17" fill="{t["muted"]}">{escape(line)}</text>')
        H = ty + 136 + 3 * 24 + 110
        parts += text
        parts.append(stamp(W - 190, H - 66, state, 0.9))
    else:
        tx = 440
        parts += [
            f'<text x="{tx}" y="104" font-family="{MONO}" font-size="13" letter-spacing="3" fill="{RED}">A PROFILE YOU CAN AUDIT</text>',
            f'<text x="{tx}" y="166" font-family="{SERIF}" font-size="54" fill="{t["text"]}">Don’t take my word</text>',
            f'<text x="{tx}" y="228" font-family="{SERIF}" font-size="54" font-style="italic" fill="{t["text"]}">for it.</text>',
        ]
        for i, line in enumerate(wrap("Every claim below links to the exact line of code behind it. "
                                      "A bot re-reads those lines every six hours and stamps what still holds.", 58)):
            parts.append(f'<text x="{tx}" y="{276 + i * 26}" font-family="{SANS}" font-size="18" fill="{t["muted"]}">{escape(line)}</text>')
        H = max(receipt_bottom + 34, 470)
        parts.append(stamp(tx + 200, H - 74, state))
    grid = "".join(f'<line x1="0" y1="{y}" x2="{W}" y2="{y}" stroke="{t["line"]}" stroke-width="1"/>' for y in range(24, int(H), 24))
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H:.0f}" width="{W}" height="{H:.0f}" role="img" '
        f'aria-label="Proof of Work receipt for Aditya Singh">'
        + defs(ph + 10)
        + f'<rect width="{W}" height="{H:.0f}" rx="14" fill="{t["bg"]}"/>{grid}'
        + f'<clipPath id="below"><rect x="0" y="{slot_y}" width="{W}" height="{H}"/></clipPath>'
        + f'<g clip-path="url(#below)"><g class="feed"><g filter="url(#shadow)">{paper}</g></g></g>'
        + printer(rx, slot_y, rw, t)
        + "".join(parts)
        + "</svg>"
    )


# ----------------------------------------------------------------------------------------------- exhibit tags

def tag(ex: dict, state: dict) -> str:
    W, H = 480, 236
    x0, y0, w, h = 34, 16, 432, 204
    mine = [c for c in state["claims"] if c["id"].startswith(ex["id"]) and c["id"][len(ex["id"]):].isdigit()]
    ok = sum(c["status"] == "verified" for c in mine)
    status_color = GREEN if ok == len(mine) else RED
    sha = (state["repos"].get(ex["repo"]) or {}).get("sha") or "0" * 40
    cut = 26
    shape = (f'M{x0 + cut},{y0} L{x0 + w},{y0} L{x0 + w},{y0 + h} L{x0 + cut},{y0 + h} '
             f'L{x0},{y0 + h - cut} L{x0},{y0 + cut} Z')
    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" '
        f'aria-label="Exhibit {ex["id"]}: {escape(ex["name"])}">',
        '<defs><filter id="s" x="-10%" y="-10%" width="125%" height="135%"><feDropShadow dx="0" dy="4" stdDeviation="5" '
        'flood-color="#000" flood-opacity="0.25"/></filter></defs>',
        f'<path d="M{x0 + 22},{y0 + h / 2} C {x0 - 4},{y0 + h / 2 - 30} 6,{y0 + 30} 2,{y0 + 6}" fill="none" stroke="#b9a989" stroke-width="2"/>',
        f'<path d="{shape}" fill="{PAPER}" stroke="{PAPER_EDGE}" filter="url(#s)"/>',
        f'<circle cx="{x0 + 22}" cy="{y0 + h / 2}" r="8" fill="none" stroke="{PAPER_EDGE}" stroke-width="3"/>',
        f'<circle cx="{x0 + 22}" cy="{y0 + h / 2}" r="5" fill="#cfc6b1"/>',
        f'<line x1="{x0 + 48}" y1="{y0 + 12}" x2="{x0 + 48}" y2="{y0 + h - 12}" stroke="{PAPER_EDGE}" stroke-dasharray="3 4"/>',
        f'<text x="{x0 + 66}" y="{y0 + 32}" font-family="{MONO}" font-size="12" font-weight="700" letter-spacing="2.5" fill="{RED}">EXHIBIT {ex["id"]}</text>',
        f'<text x="{x0 + 66}" y="{y0 + 70}" font-family="{SERIF}" font-size="31" fill="{INK}">{escape(ex["name"])}</text>',
    ]
    for i, line in enumerate(wrap(ex["pitch"], 44)[:3]):
        out.append(f'<text x="{x0 + 66}" y="{y0 + 98 + i * 19}" font-family="{SANS}" font-size="14" fill="{INK_SOFT}">{escape(line)}</text>')
    out += [
        f'<text x="{x0 + 66}" y="{y0 + h - 44}" font-family="{MONO}" font-size="10.5" fill="{INK_FAINT}">{escape(ex["stack"])}</text>',
        f'<line x1="{x0 + 66}" y1="{y0 + h - 32}" x2="{x0 + w - 18}" y2="{y0 + h - 32}" stroke="{PAPER_EDGE}"/>',
        f'<text x="{x0 + 66}" y="{y0 + h - 13}" font-family="{MONO}" font-size="11.5" font-weight="700" letter-spacing="1" '
        f'fill="{status_color}">{ok}/{len(mine)} CLAIMS VERIFIED</text>',
        f'<text x="{x0 + w - 18}" y="{y0 + h - 13}" text-anchor="end" font-family="{MONO}" font-size="11" fill="{INK_FAINT}">@{sha[:7]}</text>',
        barcode(sha, x0 + w - 104, y0 + 18, 86, 26, INK),
        "</svg>",
    ]
    return "".join(out)


# ----------------------------------------------------------------------------------------------- README ledger

# ----------------------------------------------------------------------------------------------- how-it-works

def pipeline(spec: dict, state: dict, mode: str, mobile: bool) -> str:
    t = DESK[mode]
    total = counts(state)["total"]
    steps = [
        ("01", "Claim", f"{total} claims, each naming a file and the exact code it rests on."),
        ("02", "Read", "Each repo at its latest commit, through the GitHub API."),
        ("03", "Match", "Find the code. Found means a line number; gone means stale."),
        ("04", "Stamp", "VERIFIED or STALE, with a link pinned to that commit."),
        ("05", "Redraw", "Receipt, tags and this page, every six hours."),
    ]
    css = ('<style>.flow{stroke-dasharray:5 6;animation:flow 1.2s linear infinite}'
           '@keyframes flow{to{stroke-dashoffset:-22}}@media (prefers-reduced-motion: reduce){.flow{animation:none}}</style>')
    out = []
    if mobile:
        W, cw, ch, gap, x = 600, 520, 92, 34, 40
        H = 40 + len(steps) * ch + (len(steps) - 1) * gap + 40
        for i, (num, title, body) in enumerate(steps):
            y = 40 + i * (ch + gap)
            out.append(f'<rect x="{x}" y="{y}" width="{cw}" height="{ch}" rx="6" fill="{PAPER}" stroke="{PAPER_EDGE}"/>')
            out.append(f'<text x="{x + 22}" y="{y + 36}" font-family="{MONO}" font-size="15" font-weight="700" fill="{RED}">{num}</text>')
            out.append(f'<text x="{x + 66}" y="{y + 38}" font-family="{SERIF}" font-size="26" fill="{INK}">{title}</text>')
            for j, line in enumerate(wrap(body, 52)[:2]):
                out.append(f'<text x="{x + 66}" y="{y + 62 + j * 19}" font-family="{SANS}" font-size="15" fill="{INK_SOFT}">{escape(line)}</text>')
            if i < len(steps) - 1:
                out.append(f'<line class="flow" x1="{W / 2}" y1="{y + ch + 4}" x2="{W / 2}" y2="{y + ch + gap - 6}" stroke="{RED}" stroke-width="2.5"/>')
                out.append(f'<path d="M{W / 2 - 6},{y + ch + gap - 11} L{W / 2},{y + ch + gap - 3} L{W / 2 + 6},{y + ch + gap - 11}" fill="none" stroke="{RED}" stroke-width="2.5"/>')
    else:
        W, H, cw, ch, y = 1000, 214, 168, 150, 32
        gap = (W - 48 - len(steps) * cw) / (len(steps) - 1)
        for i, (num, title, body) in enumerate(steps):
            x = 24 + i * (cw + gap)
            out.append(f'<rect x="{x}" y="{y}" width="{cw}" height="{ch}" rx="6" fill="{PAPER}" stroke="{PAPER_EDGE}"/>')
            out.append(f'<text x="{x + 16}" y="{y + 28}" font-family="{MONO}" font-size="13" font-weight="700" letter-spacing="1" fill="{RED}">{num}</text>')
            out.append(f'<text x="{x + 16}" y="{y + 62}" font-family="{SERIF}" font-size="25" fill="{INK}">{title}</text>')
            for j, line in enumerate(wrap(body, 22)[:4]):
                out.append(f'<text x="{x + 16}" y="{y + 88 + j * 17}" font-family="{SANS}" font-size="13" fill="{INK_SOFT}">{escape(line)}</text>')
            if i < len(steps) - 1:
                ax, bx, my = x + cw + 5, x + cw + gap - 5, y + ch / 2
                out.append(f'<line class="flow" x1="{ax}" y1="{my}" x2="{bx - 3}" y2="{my}" stroke="{RED}" stroke-width="2.5"/>')
                out.append(f'<path d="M{bx - 9},{my - 6} L{bx - 1},{my} L{bx - 9},{my + 6}" fill="none" stroke="{RED}" stroke-width="2.5"/>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" '
            f'aria-label="How the audit works: claim, read, match, stamp, redraw">{css}'
            f'<rect width="{W}" height="{H}" rx="14" fill="{t["bg"]}"/>' + "".join(out) + "</svg>")


def md_cell(text: str) -> str:
    return escape(text).replace("|", "&#124;").replace("\n", " ")


def claim_url(owner: str, ex: dict, claim: dict, result: dict) -> str | None:
    if result.get("status") != "verified":
        return None
    return f"https://github.com/{owner}/{ex['repo']}/blob/{result['sha']}/{claim['path']}#L{result['line']}"


def ledger(spec: dict, state: dict) -> str:
    owner = spec["owner"]
    by_id = {c["id"]: c for c in state["claims"]}
    index = {f"{ex['id']}{i}": (ex, claim) for ex in spec["exhibits"] for i, claim in enumerate(ex["claims"], 1)}
    names = {ex["repo"]: ex["name"] for ex in spec["exhibits"]}
    c = counts(state)

    def ref(cid: str) -> str:
        ex, claim = index[cid]
        url = claim_url(owner, ex, claim, by_id.get(cid, {}))
        return f"[`{cid}`]({url})" if url else f"`{cid}` (stale)"

    def repo_link(repo: str) -> str:
        return f"[{names.get(repo, repo)}](https://github.com/{owner}/{repo})"

    out = [START, "", "## Exhibits", "",
           f"{len(spec['exhibits'])} projects, {c['total']} claims. Each tag opens the repository; each claim ID opens the line.", ""]
    cards = [
        f'<a href="https://github.com/{owner}/{ex["repo"]}"><img src="assets/proof/exhibit-{ex["id"].lower()}.svg" width="49%" '
        f'alt="Exhibit {ex["id"]}: {md_cell(ex["name"])}. {md_cell(ex["pitch"])}" /></a>'
        for ex in spec["exhibits"]
    ]
    for i in range(0, len(cards), 2):
        out += ['<p align="center">', *cards[i:i + 2], "</p>", ""]

    # Case files: the story of each exhibit, collapsed so the page stays scannable.
    out += ["## Case files", "", "Open any file for the problem, the approach, what was hard and what is unfinished.", ""]
    for ex in spec["exhibits"]:
        ids = [f"{ex['id']}{i}" for i in range(1, len(ex["claims"]) + 1)]
        ok = sum(by_id.get(i, {}).get("status") == "verified" for i in ids)
        out += ["<details>", f"<summary><b>Exhibit {ex['id']} · {escape(ex['name'])}</b> &nbsp;·&nbsp; {escape(ex['pitch'])} "
                f"&nbsp;<code>{ok}/{len(ids)} verified</code></summary>", "",
                f"**The problem.** {ex['problem']}", "", f"**The approach.** {ex['approach']}", ""]
        if ex.get("hard"):
            out += ["**What was hard.**", ""] + [f"- {h}" for h in ex["hard"]] + [""]
        out += ["**Claims.**", ""]
        for cid in ids:
            out.append(f"- {ref(cid)} {index[cid][1]['text']}")
        out += ["", f"**Not done yet.** {ex['limits']}", "",
                f"<sub>{escape(ex['stack'])} · [Open the repository →](https://github.com/{owner}/{ex['repo']})</sub>", "",
                "</details>", ""]

    # The ledger: every claim in one table.
    out += ["## The ledger", "", "| # | Claim | Evidence | Status |", "| :-- | :-- | :-- | :-- |"]
    for cid, (ex, claim) in index.items():
        result = by_id.get(cid, {"status": "unchecked"})
        name = claim["path"].rsplit("/", 1)[-1]
        url = claim_url(owner, ex, claim, result)
        if url:
            evidence, status = f"[`{name}:{result['line']}`]({url})", "**VERIFIED**"
        elif result["status"] == "stale":
            evidence = f"`{name}` at [`{result['sha'][:7]}`](https://github.com/{owner}/{ex['repo']}/tree/{result['sha']})"
            status = "**STALE**: the code moved or changed"
        else:
            evidence, status = f"`{name}`", "not checked yet"
        if result.get("carried"):
            status += " <sub>(last known; repo unreachable at audit)</sub>"
        out.append(f"| {cid} | {md_cell(claim['text'])} | {evidence} | {status} |")
    out += ["", f"<sub>Audited {stamp_time(state['audited_at'])} · {c['verified']} of {c['total']} claims verified · "
            "each link is pinned to the commit that was read.</sub>", ""]

    # Principles, each backed by claims above.
    out += ["## Principles, with receipts", "", "Opinions are cheap, so each one links to the code where I acted on it.", ""]
    for n, p in enumerate(spec.get("principles", []), 1):
        out += [f"**{n}. {p['title']}** {p['body']} &nbsp;→ {' · '.join(ref(cid) for cid in p['claims'])}", ""]

    # Latest receipts: recent commits across the exhibits.
    if state.get("recent"):
        out += ["## Latest receipts", "", "The most recent changes across the exhibits, read during the last audit.", "",
                "| Date | Project | Change |", "| :-- | :-- | :-- |"]
        for r in state["recent"][:10]:
            subject = md_cell(r["subject"][:96] + ("…" if len(r["subject"]) > 96 else ""))
            out.append(f"| {r['date'].replace('-', '\u2011')} | {repo_link(r['repo'])} | [{subject}](https://github.com/{owner}/{r['repo']}/commit/{r['sha']}) |")
        out.append("")

    # Honesty section, generated from the same file so it can't drift from the case files.
    out += ["## What isn't done yet", "", "A profile that lists only wins is hiding something. Here is what is unfinished or easy to overstate:", ""]
    out += [f"- **{escape(ex['name'])}:** {ex['limits']}" for ex in spec["exhibits"]] + [""]

    if spec.get("toolbox"):
        out += ["## Toolbox, with receipts", "", "Only tools I have shipped something with, and where.", "",
                "| Tool | Used in |", "| :-- | :-- |"]
        out += [f"| {md_cell(t['tool'])} | {' · '.join(repo_link(r) for r in t['where'])} |" for t in spec["toolbox"]]
        out.append("")
    out.append(END)
    return "\n".join(out)


def replace_block(readme: str, block: str) -> str:
    if readme.count(START) != 1 or readme.count(END) != 1:
        raise ValueError("README must contain exactly one ledger marker pair")
    return readme.split(START)[0] + block + readme.split(END)[1]


# ----------------------------------------------------------------------------------------------- main

def render(spec: dict, state: dict) -> None:
    ART.mkdir(parents=True, exist_ok=True)
    for mode in ("dark", "light"):
        (ART / f"receipt-{mode}.svg").write_text(hero(spec, state, mode, mobile=False))
        (ART / f"receipt-{mode}-mobile.svg").write_text(hero(spec, state, mode, mobile=True))
        (ART / f"pipeline-{mode}.svg").write_text(pipeline(spec, state, mode, mobile=False))
        (ART / f"pipeline-{mode}-mobile.svg").write_text(pipeline(spec, state, mode, mobile=True))
    for ex in spec["exhibits"]:
        (ART / f"exhibit-{ex['id'].lower()}.svg").write_text(tag(ex, state))
    README.write_text(replace_block(README.read_text(), ledger(spec, state)))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--local", metavar="DIR", help="read local clones in DIR/<repo> instead of GitHub")
    parser.add_argument("--render-only", action="store_true", help="redraw from data/proof.json without checking")
    args = parser.parse_args()
    spec = json.loads(CLAIMS.read_text())
    previous = json.loads(STATE.read_text()) if STATE.exists() else {}
    if args.render_only:
        state = previous
    else:
        opener = (lambda owner, name: LocalRepo(Path(args.local), name)) if args.local else RemoteRepo
        state = check(spec, previous, opener)
        STATE.write_text(json.dumps(state, indent=2) + "\n")
    render(spec, state)
    c = counts(state)
    print(f"{c['verified']}/{c['total']} verified, {c['stale']} stale, {c['unchecked']} unchecked")
    return 0


if __name__ == "__main__":
    sys.exit(main())
