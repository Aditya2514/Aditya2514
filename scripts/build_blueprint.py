#!/usr/bin/env python3
"""Draw the profile as engineering blueprints and keep every code link pointing at real code.

  python3 scripts/build_blueprint.py                 # read the repos from GitHub (Actions; GH_TOKEN optional)
  python3 scripts/build_blueprint.py --local DIR     # read local clones in DIR/<repo> (offline preview)
  python3 scripts/build_blueprint.py --render-only   # redraw from data/evidence.json without reading repos

Each evidence link names a file and a snippet of code. On every run the snippet is looked up at the repo's current
default-branch commit, and the link points at that exact line, pinned to that commit. A snippet that can no longer
be found is left off the page and reported as a workflow warning. A repo that can't be reached keeps its last result.

README.md is generated from data/README.template.md: edit the template, not the README.
"""

from __future__ import annotations

import argparse
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
SPEC_FILE = ROOT / "data" / "blueprint.json"
KIT_FILE = ROOT / "profile.json"
STATE_FILE = ROOT / "data" / "evidence.json"
TEMPLATE = ROOT / "data" / "README.template.md"
README = ROOT / "README.md"
ART = ROOT / "assets" / "blueprint"
API = "https://api.github.com"

BG, PANEL = "#0a1424", "#0d1b31"
GRID_MINOR, GRID_MAJOR = "#0f1e36", "#14284a"
LINE, TEXT, MUTED, FAINT = "#8fb8ff", "#e6efff", "#8aa2c8", "#4a6290"
KIND = {"model": "#5cc8ff", "rule": "#ffb547", "person": "#8ef0b8", "io": "#8fb8ff"}
TAG = {"model": "◇ MODEL", "rule": "■ CHECK", "person": "● PERSON", "io": "▭ DATA"}
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, 'Liberation Mono', monospace"
SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif"


# ------------------------------------------------------------------------------------------------ evidence

def _get(url: str, raw: bool = False):
    headers = {"User-Agent": "blueprint-profile", "Accept": "application/vnd.github.raw" if raw else "application/vnd.github+json"}
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=30) as res:
        body = res.read()
    return body.decode("utf-8", "replace") if raw else json.loads(body)


class RemoteRepo:
    def __init__(self, owner: str, name: str):
        self.owner, self.name = owner, name
        branch = _get(f"{API}/repos/{owner}/{name}")["default_branch"]
        self.sha = _get(f"{API}/repos/{owner}/{name}/commits/{urllib.parse.quote(branch)}")["sha"]

    def read(self, path: str) -> str | None:
        try:
            return _get(f"{API}/repos/{self.owner}/{self.name}/contents/{urllib.parse.quote(path)}?ref={self.sha}", raw=True)
        except urllib.error.HTTPError as err:
            if err.code == 404:
                return None
            raise

    def recent(self, n: int = 2) -> list[dict]:
        rows = _get(f"{API}/repos/{self.owner}/{self.name}/commits?sha={self.sha}&per_page=10")
        return [{"sha": r["sha"], "date": r["commit"]["committer"]["date"][:10], "subject": r["commit"]["message"].splitlines()[0]}
                for r in rows if len(r.get("parents", [])) <= 1][:n]


class LocalRepo:
    def __init__(self, base: Path, name: str):
        self.dir = base / name
        self.sha = subprocess.run(["git", "-C", str(self.dir), "rev-parse", "HEAD"], capture_output=True, text=True, check=True).stdout.strip()

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


def collect(spec: dict, previous: dict, open_repo) -> dict:
    old_links = previous.get("links", {})
    links, repos, recent = {}, {}, []
    for repo_name, claims in spec["projects"].items():
        try:
            repo = open_repo(spec["owner"], repo_name)
            repos[repo_name] = repo.sha
        except Exception as err:
            print(f"warn: {repo_name}: {err}", file=sys.stderr)
            repo = None
            if repo_name in previous.get("repos", {}):
                repos[repo_name] = previous["repos"][repo_name]
        for i, claim in enumerate(claims, 1):
            cid = f"{repo_name}#{i}"
            try:
                if repo is None:
                    raise RuntimeError("repo unreachable")
                line = find_line(repo.read(claim["path"]), claim["needle"])
            except Exception as err:
                print(f"warn: {cid}: {err}", file=sys.stderr)
                if cid in old_links:
                    links[cid] = old_links[cid]
                continue
            if line:
                links[cid] = {"sha": repo.sha, "line": line}
            else:
                print(f"::warning::{cid} ({claim['path']}) no longer contains its snippet; its link is hidden until data/blueprint.json is updated")
        try:
            if repo is None:
                raise RuntimeError("repo unreachable")
            recent += [{**c, "repo": repo_name} for c in repo.recent()]
        except Exception:
            recent += [r for r in previous.get("recent", []) if r.get("repo") == repo_name]
    recent.sort(key=lambda r: (r["date"], r["repo"]), reverse=True)
    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    return {"generated_at": now, "repos": repos, "links": links, "recent": recent}


# ------------------------------------------------------------------------------------------------ drawing kit

def wrap(text: str, limit: int) -> list[str]:
    lines, current = [], ""
    for word in text.split():
        if current and len(current) + 1 + len(word) > limit:
            lines.append(current)
            current = word
        else:
            current = f"{current} {word}".strip()
    return lines + ([current] if current else [])


def style() -> str:
    return (
        "<style>"
        ".draw{stroke-dasharray:1;stroke-dashoffset:1;animation:draw .7s ease-out both}"
        "@keyframes draw{to{stroke-dashoffset:0}}"
        ".pop{opacity:0;animation:pop .45s ease-out both}"
        "@keyframes pop{from{opacity:0;transform:translateY(4px)}to{opacity:1;transform:none}}"
        "@media (prefers-reduced-motion: reduce){.draw{stroke-dasharray:none;stroke-dashoffset:0;animation:none}"
        ".pop{opacity:1;animation:none}.pulse{display:none}}"
        "</style>"
    )


def paper(W: float, H: float) -> str:
    """Blueprint sheet: ground, grid, double frame and edge ticks."""
    out = [f'<rect width="{W}" height="{H}" rx="12" fill="{BG}"/>']
    for x in range(20, int(W), 20):
        out.append(f'<line x1="{x}" y1="14" x2="{x}" y2="{H - 14}" stroke="{GRID_MAJOR if x % 100 == 0 else GRID_MINOR}" stroke-width="1"/>')
    for y in range(20, int(H), 20):
        out.append(f'<line x1="14" y1="{y}" x2="{W - 14}" y2="{y}" stroke="{GRID_MAJOR if y % 100 == 0 else GRID_MINOR}" stroke-width="1"/>')
    out.append(f'<rect x="10" y="10" width="{W - 20}" height="{H - 20}" fill="none" stroke="{FAINT}" stroke-width="1"/>')
    out.append(f'<rect x="16" y="16" width="{W - 32}" height="{H - 32}" fill="none" stroke="{LINE}" stroke-width="1.4" opacity="0.7"/>')
    for i, x in enumerate(range(100, int(W) - 50, 100), 1):
        out.append(f'<line x1="{x}" y1="10" x2="{x}" y2="16" stroke="{LINE}"/>')
        out.append(f'<text x="{x - 50}" y="15" text-anchor="middle" font-family="{MONO}" font-size="6" fill="{FAINT}">{i}</text>')
    return "".join(out)


def title_block(x: float, y: float, w: float, rows: list[tuple[str, str]]) -> str:
    h = 22 * len(rows)
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{BG}" stroke="{LINE}" stroke-width="1.2"/>']
    for i, (label, value) in enumerate(rows):
        ry = y + i * 22
        if i:
            out.append(f'<line x1="{x}" y1="{ry}" x2="{x + w}" y2="{ry}" stroke="{FAINT}"/>')
        out.append(f'<line x1="{x + 78}" y1="{ry}" x2="{x + 78}" y2="{ry + 22}" stroke="{FAINT}"/>')
        out.append(f'<text x="{x + 8}" y="{ry + 15}" font-family="{MONO}" font-size="9.5" letter-spacing="1" fill="{MUTED}">{label}</text>')
        out.append(f'<text x="{x + 88}" y="{ry + 15}" font-family="{MONO}" font-size="11" fill="{TEXT}">{escape(value)}</text>')
    return "".join(out)


def legend(x: float, y: float, vertical: bool = False) -> str:
    items = [("model", "MODEL PROPOSES"), ("rule", "SYSTEM CHECKS"), ("person", "PERSON DECIDES")]
    out = []
    for i, (kind, label) in enumerate(items):
        ix, iy = (x, y + i * 20) if vertical else (x + i * 158, y)
        out.append(f'<text x="{ix}" y="{iy}" font-family="{MONO}" font-size="11" letter-spacing="1" fill="{KIND[kind]}">'
                   f'{TAG[kind].split()[0]} {label}</text>')
    return "".join(out)


def node(n: dict, delay: float, big: bool = False) -> str:
    kind, color = n["kind"], KIND[n["kind"]]
    x, y, w, h = n["x"], n["y"], n["w"], n["h"]
    rx = {"model": 12, "person": h / 2 if not big else 16, "rule": 0, "io": 4}[kind]
    fs_title, fs_sub, fs_tag = (18, 13, 10.5) if big else (14.5, 11, 9)
    out = [f'<g class="pop" style="animation-delay:{delay:.2f}s">',
           f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{PANEL}" stroke="{color}" stroke-width="1.6"/>']
    if kind == "rule":
        out.append(f'<rect x="{x + 3}" y="{y + 3}" width="{w - 6}" height="{h - 6}" fill="none" stroke="{color}" stroke-width="0.7" opacity="0.6"/>')
    cx = x + w / 2
    out.append(f'<text x="{cx}" y="{y + (17 if not big else 21)}" text-anchor="middle" font-family="{MONO}" font-size="{fs_tag}" '
               f'letter-spacing="1.2" fill="{color}">{TAG[kind]}</text>')
    out.append(f'<text x="{cx}" y="{y + h / 2 + (5 if not big else 6)}" text-anchor="middle" font-family="{SANS}" font-size="{fs_title}" '
               f'font-weight="600" fill="{TEXT}">{escape(n["title"])}</text>')
    out.append(f'<text x="{cx}" y="{y + h - (11 if not big else 13)}" text-anchor="middle" font-family="{MONO}" font-size="{fs_sub}" '
               f'fill="{MUTED}">{escape(n["sub"])}</text>')
    out.append("</g>")
    return "".join(out)


def edge(i: int, points: list[tuple[float, float]], delay: float, label: str | None = None, uid: str = "e") -> tuple[str, str]:
    d = "M" + " L".join(f"{px:.1f},{py:.1f}" for px, py in points)
    (ax, ay), (bx, by) = points[-2], points[-1]
    if abs(bx - ax) >= abs(by - ay):
        s = 1 if bx > ax else -1
        head = f"M{bx - 8 * s},{by - 5} L{bx},{by} L{bx - 8 * s},{by + 5}"
    else:
        s = 1 if by > ay else -1
        head = f"M{bx - 5},{by - 8 * s} L{bx},{by} L{bx + 5},{by - 8 * s}"
    pid = f"{uid}{i}"
    out = [f'<path id="{pid}" class="draw" pathLength="1" d="{d}" fill="none" stroke="{LINE}" stroke-width="1.5" '
           f'style="animation-delay:{delay:.2f}s"/>',
           f'<path class="pop" d="{head}" fill="none" stroke="{LINE}" stroke-width="1.5" style="animation-delay:{delay + 0.55:.2f}s"/>']
    tag = ""
    if label:
        segs = list(zip(points, points[1:]))
        (p1x, p1y), (p2x, p2y) = max(segs, key=lambda sg: abs(sg[1][0] - sg[0][0]) + abs(sg[1][1] - sg[0][1]))
        mx, my = (p1x + p2x) / 2, (p1y + p2y) / 2
        tw = 8 + len(label) * 6.4
        tag = (f'<g class="pop" style="animation-delay:{delay + 0.4:.2f}s"><rect x="{mx - tw / 2}" y="{my - 9}" '
               f'width="{tw}" height="16" rx="3" fill="{BG}" stroke="{FAINT}" stroke-width="0.8"/>'
               f'<text x="{mx}" y="{my + 3}" text-anchor="middle" font-family="{MONO}" font-size="10.5" fill="{MUTED}">{escape(label)}</text></g>')
    begin = delay + 0.8
    out.append(f'<circle class="pulse" r="2.6" fill="{TEXT}" opacity="0"><set attributeName="opacity" to="0.9" begin="{begin:.2f}s"/>'
               f'<animateMotion dur="1.8s" begin="{begin:.2f}s" repeatCount="indefinite"><mpath href="#{pid}"/></animateMotion></circle>')
    return "".join(out), tag


def svg(W: float, H: float, label: str, body: str) -> str:
    return (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 {W} {H:.0f}" '
            f'width="{W}" height="{H:.0f}" role="img" aria-label="{escape(label)}">{style()}{paper(W, H)}{body}</svg>')


# ------------------------------------------------------------------------------------------------ sheets

def sheet_edges(sheet: dict) -> list[list]:
    if "edges" in sheet:
        return sheet["edges"]
    edges = []
    for i in range(len(sheet["stages"]) - 1):
        edges.append([i, i + 1])
    return edges


def layout_desktop(sheet: dict):
    W, per_row = 1000, sheet.get("per_row", 5)
    colw = (W - 80) / per_row
    nw, nh, vgap = colw - (76 if per_row <= 4 else 42), 70, 14
    stages = sheet["stages"]
    rows = [stages[i:i + per_row] for i in range(0, len(stages), per_row)]
    y, placed = 132.0, []
    for r, row in enumerate(rows):
        band = max(len(st) * nh + (len(st) - 1) * vgap for st in row)
        top_pad = 34 if any(len(e) > 3 and e[3] == "over" for e in sheet_edges(sheet)) else 0
        y += top_pad
        for c, st in enumerate(row):
            sh = len(st) * nh + (len(st) - 1) * vgap
            for k, (kind, title, sub) in enumerate(st):
                placed.append({"stage": r * per_row + c, "row": r, "col": c, "kind": kind, "title": title, "sub": sub,
                               "x": 40 + c * colw + (colw - nw) / 2, "y": y + (band - sh) / 2 + k * (nh + vgap), "w": nw, "h": nh})
        y += band + 64
    return W, y - 64 + 26, placed


def layout_mobile(sheet: dict):
    W, nh, rgap = 600, 80, 50
    y, placed = 150.0, []
    for s, st in enumerate(sheet["stages"]):
        k = len(st)
        gap = 14
        nw = min(300, (W - 100 - (k - 1) * gap) / k)
        total = k * nw + (k - 1) * gap
        for j, (kind, title, sub) in enumerate(st):
            placed.append({"stage": s, "row": s, "col": 0, "kind": kind, "title": title, "sub": sub,
                           "x": (W - total) / 2 + j * (nw + gap), "y": y, "w": nw, "h": nh})
        y += nh + rgap
    return W, y - rgap + 30, placed


def route(a: dict, b: dict, mode: str, mobile: bool, W: float) -> list[tuple[float, float]]:
    if mobile:
        if mode == "over":
            rx = W - 40
            return [(a["x"] + a["w"], a["y"] + a["h"] / 2), (rx, a["y"] + a["h"] / 2), (rx, b["y"] + b["h"] / 2), (b["x"] + b["w"], b["y"] + b["h"] / 2)]
        sx, sy, ex, ey = a["x"] + a["w"] / 2, a["y"] + a["h"], b["x"] + b["w"] / 2, b["y"]
        if abs(sx - ex) < 1:
            return [(sx, sy), (ex, ey)]
        my = (sy + ey) / 2
        return [(sx, sy), (sx, my), (ex, my), (ex, ey)]
    if mode == "over":
        top = min(a["y"], b["y"]) - 22
        return [(a["x"] + a["w"] / 2, a["y"]), (a["x"] + a["w"] / 2, top), (b["x"] + b["w"] / 2, top), (b["x"] + b["w"] / 2, b["y"])]
    sx, sy = a["x"] + a["w"], a["y"] + a["h"] / 2
    ex, ey = b["x"], b["y"] + b["h"] / 2
    if b["row"] == a["row"]:
        if abs(sy - ey) < 1:
            return [(sx, sy), (ex, ey)]
        mx = (sx + ex) / 2
        return [(sx, sy), (mx, sy), (mx, ey), (ex, ey)]
    gap_y = a["band_bottom"] + 32
    return [(sx, sy), (sx + 14, sy), (sx + 14, gap_y), (ex - 14, gap_y), (ex - 14, ey), (ex, ey)]


def draw_sheet(sheet: dict, state: dict, names: dict, mobile: bool) -> str:
    W, h_draw, placed = (layout_mobile if mobile else layout_desktop)(sheet)
    by_stage: dict[int, list] = {}
    for n in placed:
        by_stage.setdefault(n["stage"], []).append(n)
    if not mobile:  # bottom of each row band, for wrap-around edges
        for n in placed:
            n["band_bottom"] = max(m["y"] + m["h"] for m in placed if m["row"] == n["row"])
    step = 0.32
    body, tags, n_edges = [], [], 0
    for i, e in enumerate(sheet_edges(sheet)):
        a_stage, b_stage = e[0], e[1]
        label = e[2] if len(e) > 2 else None
        mode = e[3] if len(e) > 3 else "next"
        for a in by_stage[a_stage]:
            for b in by_stage[b_stage]:
                pts = route(a, b, mode, mobile, W)
                first = a is by_stage[a_stage][0] and b is by_stage[b_stage][0]
                line, tag = edge(n_edges, pts, 0.3 + a_stage * step + 0.2, label if first else None)
                n_edges += 1
                body.append(line)
                tags.append(tag)
    for n in placed:
        body.append(node(n, 0.3 + n["stage"] * step, big=mobile))
    body += tags
    name = names.get(sheet["repo"], sheet["repo"])
    sha = (state["repos"].get(sheet["repo"]) or "0" * 7)[:7]
    header = [
        f'<text x="40" y="{50 if not mobile else 52}" font-family="{MONO}" font-size="{12 if not mobile else 14}" letter-spacing="2" fill="{KIND["model"]}">'
        f'SHEET {sheet["sheet"]} · {escape(name.upper())}</text>',
        f'<text x="40" y="{84 if not mobile else 92}" font-family="{SANS}" font-size="{24 if not mobile else 28}" font-weight="600" fill="{TEXT}">{escape(sheet["title"])}</text>',
    ]
    if mobile:
        header.append(f'<line x1="40" y1="114" x2="{W - 40}" y2="114" stroke="{FAINT}"/>')
        H = h_draw + 150
        foot = legend(40, h_draw + 18, vertical=True) + title_block(W - 300, h_draw + 2, 260,
                                                                   [("DRAWN", "A. SINGH"), ("REPO", sheet["repo"]), ("REV", "@" + sha)])
    else:
        header.append(f'<text x="{W - 40}" y="50" text-anchor="end" font-family="{MONO}" font-size="11" fill="{MUTED}">DWG AS-{sheet["sheet"]} · SCALE NTS</text>')
        header.append(f'<line x1="40" y1="104" x2="{W - 40}" y2="104" stroke="{FAINT}"/>')
        H = h_draw + 92
        foot = legend(40, H - 44) + title_block(W - 300, H - 98, 260, [("DRAWN", "A. SINGH"), ("REPO", sheet["repo"]), ("REV", "@" + sha)])
    return svg(W, H, f"Blueprint of {name}: {sheet['title']}", "".join(header) + "".join(body) + foot)


# ------------------------------------------------------------------------------------------------ hero

def draw_hero(mobile: bool) -> str:
    if mobile:
        W, H = 600, 880
        tx, ty = 44, 70
        cx, cy, r = 300, 545, 140
    else:
        W, H = 1000, 460
        tx, ty = 52, 92
        cx, cy, r = 760, 222, 132
    body = [
        f'<text x="{tx}" y="{ty}" font-family="{MONO}" font-size="13" letter-spacing="2.5" fill="{KIND["model"]}">SHEET 00 · OPERATOR</text>',
        f'<text class="pop" x="{tx - 3}" y="{ty + 70}" font-family="{SANS}" font-size="{60 if not mobile else 64}" font-weight="700" '
        f'letter-spacing="-1" fill="{TEXT}" style="animation-delay:.1s">Aditya Singh</text>',
        f'<text class="pop" x="{tx}" y="{ty + 110}" font-family="{SANS}" font-size="22" fill="{MUTED}" style="animation-delay:.3s">'
        f'AI systems · Agents · Full-stack</text>',
        f'<text class="pop" x="{tx}" y="{ty + 142}" font-family="{MONO}" font-size="13.5" letter-spacing="1" fill="{LINE}" style="animation-delay:.45s">'
        f'IIT MADRAS · SCALER SCHOOL OF TECHNOLOGY</text>',
    ]
    lines = ["The model proposes.", "The system checks.", "The person stays in control."]
    for i, line in enumerate(lines):
        color = [KIND["model"], KIND["rule"], KIND["person"]][i]
        body.append(f'<text class="pop" x="{tx}" y="{ty + 196 + i * 30}" font-family="{SANS}" font-size="20" fill="{TEXT}" '
                    f'style="animation-delay:{1.4 + i * 0.5:.1f}s"><tspan fill="{color}">{"◇■●"[i]}</tspan>  {line}</text>')
    nw, nh = 150, 70
    spots = [(cx - nw / 2, cy - r), (cx + r * 0.87 - nw / 2, cy + r * 0.5 - nh / 2), (cx - r * 0.87 - nw / 2, cy + r * 0.5 - nh / 2)]
    nodes = [{"kind": "model", "title": "Model", "sub": "proposes"}, {"kind": "rule", "title": "System", "sub": "checks"},
             {"kind": "person", "title": "Person", "sub": "decides"}]
    for n, (x, y) in zip(nodes, spots):
        n.update(x=x, y=y, w=nw, h=nh)
    m, s, p = nodes
    paths = [
        [(m["x"] + nw, m["y"] + nh / 2), (s["x"] + nw / 2, m["y"] + nh / 2), (s["x"] + nw / 2, s["y"])],
        [(s["x"], s["y"] + nh / 2), (p["x"] + nw, p["y"] + nh / 2)],
        [(p["x"] + nw / 2, p["y"]), (p["x"] + nw / 2, m["y"] + nh / 2), (m["x"], m["y"] + nh / 2)],
    ]
    tags = []
    for i, (pts, label) in enumerate(zip(paths, ["proposal", "verified", "approve / undo"])):
        line, tag = edge(i, pts, 1.2 + i * 0.5, label, uid="h")
        body.append(line)
        tags.append(tag)
    for i, n in enumerate(nodes):
        body.append(node(n, 0.9 + i * 0.5, big=True))
    body += tags
    if mobile:
        body.append(title_block(44, H - 112, W - 88, [("DRAWN", "A. SINGH"), ("SHEETS", "00 TO 04"), ("STATUS", "ACTIVELY BUILDING")]))
    else:
        body.append(title_block(W - 312, H - 92, 272, [("DRAWN", "A. SINGH"), ("SHEETS", "00 TO 04"), ("STATUS", "ACTIVELY BUILDING")]))
    return svg(W, H, "Aditya Singh: AI systems, agents and full-stack. The model proposes, the system checks, the person stays in control.",
               "".join(body))


# ------------------------------------------------------------------------------------------------ parts list

def draw_kit(kit: list[dict], mobile: bool) -> str:
    rows = []
    if mobile:
        W = 600
        y = 120
        for i, group in enumerate(kit, 1):
            rows.append(f'<g class="pop" style="animation-delay:{0.15 * i:.2f}s">'
                        f'<text x="44" y="{y}" font-family="{MONO}" font-size="13" letter-spacing="1.5" fill="{KIND["model"]}">{i:02d}  {escape(group["name"])}</text>'
                        f'<text x="{W - 44}" y="{y}" text-anchor="end" font-family="{SANS}" font-size="13" fill="{MUTED}">{escape(group["purpose"])}</text>')
            for j, line in enumerate(wrap(" · ".join(group["tools"]), 40)):
                rows.append(f'<text x="44" y="{y + 28 + j * 24}" font-family="{SANS}" font-size="19" fill="{TEXT}">{escape(line)}</text>')
            lines = len(wrap(" · ".join(group["tools"]), 40))
            rows.append(f'<line x1="44" y1="{y + 22 + lines * 24}" x2="{W - 44}" y2="{y + 22 + lines * 24}" stroke="{FAINT}"/></g>')
            y += 44 + lines * 24 + 18
        H = y + 10
    else:
        W = 1000
        cols = [(44, "ITEM"), (100, "ASSEMBLY"), (290, "PARTS"), (760, "FUNCTION")]
        rows.append(f'<rect x="40" y="96" width="{W - 80}" height="30" fill="{PANEL}" stroke="{LINE}" stroke-width="1"/>')
        rows += [f'<text x="{x + 8}" y="116" font-family="{MONO}" font-size="11" letter-spacing="1.5" fill="{MUTED}">{h}</text>' for x, h in cols]
        y = 126
        for i, group in enumerate(kit, 1):
            parts = wrap(" · ".join(group["tools"]), 52)
            purpose = wrap(group["purpose"], 24)
            rh = 24 + 22 * max(len(parts), len(purpose))
            cell = [f'<g class="pop" style="animation-delay:{0.15 * i:.2f}s">',
                    f'<rect x="40" y="{y}" width="{W - 80}" height="{rh}" fill="none" stroke="{FAINT}"/>',
                    f'<text x="52" y="{y + 28}" font-family="{MONO}" font-size="13" fill="{KIND["model"]}">{i:02d}</text>',
                    f'<text x="108" y="{y + 28}" font-family="{MONO}" font-size="13" letter-spacing="1.2" fill="{TEXT}">{escape(group["name"])}</text>']
            cell += [f'<text x="298" y="{y + 28 + j * 22}" font-family="{SANS}" font-size="15.5" fill="{TEXT}">{escape(t)}</text>' for j, t in enumerate(parts)]
            cell += [f'<text x="768" y="{y + 28 + j * 22}" font-family="{SANS}" font-size="13.5" fill="{MUTED}">{escape(t)}</text>' for j, t in enumerate(purpose)]
            rows.append("".join(cell) + "</g>")
            y += rh
        for x, _ in cols[1:]:
            rows.append(f'<line x1="{x}" y1="96" x2="{x}" y2="{y}" stroke="{FAINT}"/>')
        H = y + 44
    header = (f'<text x="44" y="{52 if not mobile else 56}" font-family="{MONO}" font-size="{12 if not mobile else 14}" letter-spacing="2" fill="{KIND["model"]}">SHEET 04 · PARTS LIST</text>'
              f'<text x="44" y="{80 if not mobile else 88}" font-family="{SANS}" font-size="{22 if not mobile else 26}" font-weight="600" fill="{TEXT}">What I build with</text>')
    return svg(W, H, "Parts list: " + "; ".join(f"{g['name']}: {', '.join(g['tools'])}" for g in kit), header + "".join(rows))


# ------------------------------------------------------------------------------------------------ README

def link_for(spec: dict, state: dict, repo: str, i: int) -> str | None:
    hit = state["links"].get(f"{repo}#{i}")
    if not hit:
        return None
    claim = spec["projects"][repo][i - 1]
    name = claim["path"].rsplit("/", 1)[-1]
    return f"[`{name}:{hit['line']}`](https://github.com/{spec['owner']}/{repo}/blob/{hit['sha']}/{claim['path']}#L{hit['line']})"


def md_cell(text: str) -> str:
    return escape(text).replace("|", "&#124;").replace("\n", " ")


def render_readme(spec: dict, state: dict) -> str:
    names, owner = spec["names"], spec["owner"]
    text = TEMPLATE.read_text()
    for repo, claims in spec["projects"].items():
        links = [l for l in (link_for(spec, state, repo, i) for i in range(1, len(claims) + 1)) if l]
        text = text.replace("{{code:" + repo + "}}", " · ".join(links) if links else "")
    rows = ["| System | Design decision | In the code |", "| :-- | :-- | :-- |"]
    for d in spec["decisions"]:
        links = [l for l in (link_for(spec, state, d["repo"], i) for i in d["claims"]) if l]
        rows.append(f"| [{names[d['repo']]}](https://github.com/{owner}/{d['repo']}) | {md_cell(d['text'])} | {'<br>'.join(links) or '·'} |")
    text = text.replace("{{decisions}}", "\n".join(rows))
    log = ["| Date | Project | Change |", "| :-- | :-- | :-- |"]
    for r in state.get("recent", [])[:10]:
        subject = md_cell(r["subject"][:96] + ("…" if len(r["subject"]) > 96 else ""))
        log.append(f"| {r['date'].replace('-', chr(0x2011))} | [{names.get(r['repo'], r['repo'])}](https://github.com/{owner}/{r['repo']}) | "
                   f"[{subject}](https://github.com/{owner}/{r['repo']}/commit/{r['sha']}) |")
    text = text.replace("{{buildlog}}", "\n".join(log))
    stamp = datetime.fromisoformat(state["generated_at"].replace("Z", "+00:00")).strftime("%d %b %Y, %H:%M UTC")
    text = text.replace("{{generated}}", stamp)
    head = "<!-- Generated from data/README.template.md by scripts/build_blueprint.py. Edit the template, not this file. -->\n"
    return head + text


def render(spec: dict, state: dict) -> None:
    ART.mkdir(parents=True, exist_ok=True)
    kit = json.loads(KIT_FILE.read_text())["build_kit"]
    (ART / "hero.svg").write_text(draw_hero(False))
    (ART / "hero-mobile.svg").write_text(draw_hero(True))
    for sheet in spec["sheets"]:
        key = sheet["repo"].lower()
        (ART / f"{key}.svg").write_text(draw_sheet(sheet, state, spec["names"], False))
        (ART / f"{key}-mobile.svg").write_text(draw_sheet(sheet, state, spec["names"], True))
    (ART / "parts.svg").write_text(draw_kit(kit, False))
    (ART / "parts-mobile.svg").write_text(draw_kit(kit, True))
    README.write_text(render_readme(spec, state))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--local", metavar="DIR", help="read local clones in DIR/<repo> instead of GitHub")
    parser.add_argument("--render-only", action="store_true", help="redraw from data/evidence.json without reading repos")
    args = parser.parse_args()
    spec = json.loads(SPEC_FILE.read_text())
    previous = json.loads(STATE_FILE.read_text()) if STATE_FILE.exists() else {}
    if args.render_only:
        state = previous
    else:
        opener = (lambda owner, name: LocalRepo(Path(args.local), name)) if args.local else RemoteRepo
        state = collect(spec, previous, opener)
        STATE_FILE.write_text(json.dumps(state, indent=2) + "\n")
    render(spec, state)
    total = sum(len(c) for c in spec["projects"].values())
    print(f"{len(state['links'])}/{total} code links resolved")
    return 0


if __name__ == "__main__":
    sys.exit(main())
