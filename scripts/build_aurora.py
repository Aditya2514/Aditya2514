#!/usr/bin/env python3
"""Build the Aurora profile: fetch live data, draw every scene, and write README.md from its template.

  python3 scripts/build_aurora.py                  # Actions: GraphQL stats + repo reads over the GitHub API
  python3 scripts/build_aurora.py --local DIR      # read repo clones in DIR/<repo>; reuse the saved GitHub stats
  python3 scripts/build_aurora.py --render-only    # redraw from the saved data files only

Saved data: data/github.json (contribution calendar, repos, languages) and data/evidence.json (code links,
live metrics, recent commits). If a source can't be reached, the last saved value is used.
README.md is generated from data/README.template.md: edit the template, not the README.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from xml.sax.saxutils import escape

sys.path.insert(0, str(Path(__file__).resolve().parent))
import aurora_art as art  # noqa: E402
import aurora_data as data  # noqa: E402
import aurora_fx as fx  # noqa: E402
import github_activity as activity  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
SPEC = ROOT / "data" / "aurora.json"
GITHUB = ROOT / "data" / "github.json"
EVIDENCE = ROOT / "data" / "evidence.json"
KIT = ROOT / "profile.json"
TEMPLATE = ROOT / "data" / "README.template.md"
README = ROOT / "README.md"
OUT = ROOT / "assets" / "aurora"

DIVIDERS = ["", "", ""]

TAGLINES = [
    "I build AI that checks itself before you have to.",
    "Agents that ask before they act, and can undo what they did.",
    "Rules where mistakes are expensive. Models where they help.",
]

LOOP_RULES = [
    ("The model proposes", "LexGuard's agents draft the risk ratings; Pikina's local model drafts the tool call.", art.ICE),
    ("The system checks", "36 trap rules can overrule a rating. Every tool call is schema-checked first.", art.AMBER),
    ("The person decides", "Anything risky waits for consent, and a plan that fails rolls itself back.", art.EMERALD),
]


def load(path: Path) -> dict:
    return json.loads(path.read_text()) if path.exists() else {}


def code_links(spec: dict, ev: dict, card: dict) -> str:
    out = []
    for i, claim in enumerate(card["claims"], 1):
        hit = ev.get("links", {}).get(f"{card['repo']}#{i}")
        if hit:
            url = f"https://github.com/{spec['owner']}/{card['repo']}/blob/{hit['sha']}/{claim['path']}#L{hit['line']}"
            out.append(f"[`{claim['label']}`]({url})")
    return " · ".join(out)


def badge(name: str, logo: str, color: str) -> str:
    label = name.replace("-", "--").replace(" ", "%20").replace("+", "%2B")
    return f"![{name}](https://img.shields.io/badge/{label}-08141F?style=flat-square&logo={logo}&logoColor={color})"


def cards_html(spec: dict, ev: dict) -> str:
    rows, cells = [], []
    for card in spec["cards"]:
        links = code_links(spec, ev, card)
        sig = ev.get("signals", {}).get(card["repo"], {})
        chips = [f"`{sig['tests']} tests`" if sig.get("tests") else "", "`CI`" if sig.get("ci") else "",
                 "`Docker`" if sig.get("docker") else "", f"`{sig['adrs']} ADRs`" if sig.get("adrs") else ""]
        live = spec.get("live", {}).get(card["repo"])
        if live and ev.get("live", {}).get(card["repo"]):
            chips.append(f"**[● live ↗]({live})**")
        chips = " ".join(c for c in chips if c)
        cell = [f'<td width="50%" valign="top">', "", f"**{card['name']}**<br>", f"<sub>{escape(card['tag'])}</sub>", "",
                " ".join(badge(*b) for b in card["badges"]), "", card["lede"], ""] + ([chips, ""] if chips else []) + [
                "<details>", "<summary>Architecture notes</summary>", "<br>", "", card["notes"], "", "</details>", ""]
        if links:
            cell += [f"**In the code:** {links}", ""]
        cell += [f"[Source →](https://github.com/{spec['owner']}/{card['repo']})", "", "</td>"]
        cells.append("\n".join(cell))
    for i in range(0, len(cells), 2):
        rows.append("<tr>\n" + "\n".join(cells[i:i + 2]) + "\n</tr>")
    return "<table>\n" + "\n".join(rows) + "\n</table>"


def smaller_table(spec: dict, ev: dict) -> str:
    rows = ["| Project | What it does | Stack |", "| :-- | :-- | :-- |"]
    for s in spec.get("smaller", []):
        live = spec.get("live", {}).get(s["repo"])
        tag = f" · [live ↗]({live})" if live and ev.get("live", {}).get(s["repo"]) else ""
        rows.append(f"| [{s['name']}](https://github.com/{spec['owner']}/{s['repo']}){tag} | {escape(s['what'])} | {escape(s['stack'])} |")
    return "\n".join(rows)


def kit_badges(kit: list[dict]) -> str:
    logos = {"Python": ("python", "3776AB"), "JavaScript": ("javascript", "F7DF1E"), "TypeScript": ("typescript", "3178C6"),
             "C++": ("cplusplus", "00599C"), "Ollama": ("ollama", "FFFFFF"), "Gemini": ("googlegemini", "8E75B2"),
             "Groq": ("groq", "F55036"), "Hugging Face": ("huggingface", "FFD21E"), "ChromaDB": ("databricks", "FF6B6B"),
             "sentence-transformers": ("pytorch", "EE4C2C"), "Node.js": ("nodedotjs", "339933"), "Express": ("express", "FFFFFF"),
             "FastAPI": ("fastapi", "009688"), "Flask": ("flask", "FFFFFF"), "PostgreSQL": ("postgresql", "4169E1"),
             "MongoDB": ("mongodb", "47A248"), "Redis": ("redis", "DC382D"), "SQLite": ("sqlite", "74B9E8"),
             "React": ("react", "61DAFB"), "React Native": ("react", "61DAFB"), "Electron": ("electron", "47848F"),
             "Streamlit": ("streamlit", "FF4B4B"), "Git": ("git", "F05032"), "GitHub Actions": ("githubactions", "2088FF"),
             "Docker": ("docker", "2496ED"), "Vercel": ("vercel", "FFFFFF")}
    rows = ["| | |", "| :-- | :-- |"]
    for group in kit:
        rows.append(f"| <sub>**{escape(group['name'])}**</sub><br><sub>{escape(group['purpose'])}</sub> | "
                    + " ".join(badge(tool, *logos.get(tool, ("", "FFFFFF"))) for tool in group["tools"]) + " |")
    return "\n".join(rows)


def render(spec: dict, gh: dict, ev: dict) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    cats = spec["categories"]
    names = {c["repo"]: c["name"] for c in spec["cards"]}
    lat = "12.99° N  ·  80.23° E  ·  CHENNAI"
    (OUT / "hero.svg").write_text(fx.hero(lat, TAGLINES))
    if ev.get("rhythm"):
        (OUT / "rhythm.svg").write_text(fx.rhythm(ev["rhythm"], ev["generated_at"]))
    traps = ev.get("metrics", {}).get("LexGuard")
    rules = list(LOOP_RULES)
    if traps:
        rules[1] = (rules[1][0], f"{traps} trap rules can overrule a rating. Every tool call is schema-checked first.", rules[1][2])
    else:
        rules[1] = (rules[1][0], "Trap rules can overrule a rating. Every tool call is schema-checked first.", rules[1][2])
    (OUT / "basecamp.svg").write_text(art.basecamp(rules))
    (OUT / "expeditions.svg").write_text(art.expeditions(spec["flagships"], spec["systems"], ev.get("metrics", {}), cats, len(ev.get("links", {})), ev.get("live", {})))
    (OUT / "flare.svg").write_text(art.flare())
    for i, label in enumerate(DIVIDERS, 1):
        (OUT / f"divider-{i:02d}.svg").write_text(fx.divider(label, i))
    for key, label, sub, icon, color in [("linkedin", "LinkedIn", "aditya-singh-8286b137a", "linkedin", art.ICE),
                                         ("email", "Email", "adityasinghv05@gmail.com", "mail", art.AMBER),
                                         ("github", "GitHub", "@Aditya2514 · all repositories", "git", art.EMERALD)]:
        (OUT / f"channel-{key}.svg").write_text(art.channel(label, sub, icon, color))
    if ev.get("recent"):
        (OUT / "trail.svg").write_text(art.trail(ev["recent"], names, cats, ev["generated_at"]))
    display = {**{r["name"]: r["name"] for r in gh.get("repos", [])}, **names,
               **{s["repo"]: s["name"] for s in spec.get("smaller", [])}, "Simple-Sounboard": "Soundboard", "portfolio": "Portfolio"}
    if ev.get("signals"):
        (OUT / "instruments.svg").write_text(art.instruments(ev["signals"], ev.get("live", {}), gh.get("totals", {}).get("prs", 0),
                                                             spec.get("crew", []), display, ev["generated_at"]))
    if gh.get("repos"):
        (OUT / "ascent.svg").write_text(art.ascent(spec.get("journey", []), {r["name"]: r for r in gh["repos"]}, display, cats))
    if gh.get("days"):
        repos = [r for r in gh["repos"] if not r["archived"] or r["kb"] > 0]
        active, longest, current = data.streaks(gh["days"])
        (OUT / "sky.svg").write_text(art.sky(gh, data.weekly(gh["days"]), active, longest, current, len(repos)))
        (OUT / "terrain.svg").write_text(art.terrain(repos, cats, [c["repo"] for c in spec["cards"]], gh["fetched_at"]))
        (OUT / "bedrock.svg").write_text(art.bedrock(data.language_shares(repos), len(repos)))
    text = TEMPLATE.read_text()
    text = text.replace("{{cards}}", cards_html(spec, ev))
    text = text.replace("{{smaller}}", smaller_table(spec, ev))
    text = text.replace("{{kit}}", kit_badges(json.loads(KIT.read_text())["build_kit"]))
    stamp = datetime.fromisoformat(ev.get("generated_at", data.now_iso()).replace("Z", "+00:00")).strftime("%d %b %Y, %H:%M UTC")
    text = text.replace("{{generated}}", stamp)
    README.write_text("<!-- Generated from data/README.template.md by scripts/build_aurora.py. Edit the template, not this file. -->\n" + text)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--local", metavar="DIR", help="read repo clones in DIR/<repo>; reuse saved GitHub stats")
    parser.add_argument("--render-only", action="store_true", help="redraw from saved data only")
    args = parser.parse_args()
    spec = load(SPEC)
    gh, ev = load(GITHUB), load(EVIDENCE)
    if not args.render_only:
        if not args.local:
            try:
                gh = data.fetch_github(spec["owner"], spec.get("exclude", []))
                GITHUB.write_text(json.dumps(gh, indent=1) + "\n")
            except Exception as err:
                print(f"::warning::GitHub stats unavailable, keeping the last snapshot: {err}")
        opener = (lambda owner, name: data.LocalRepo(Path(args.local), name)) if args.local else data.RemoteRepo
        previous = ev
        ev = data.collect(spec, previous, opener)
        names_all = sorted({r["name"] for r in gh.get("repos", [])} | {c["repo"] for c in spec["cards"]})
        ev.update(data.collect_signals(names_all, previous, opener, spec["owner"], spec.get("live", {}), check_live=not args.local))
        try:  # when the commits land: GitHub API in Actions, local clones (emails from AURORA_EMAILS) in a preview
            if args.local:
                emails = {e.strip().lower() for e in os.environ.get("AURORA_EMAILS", "").split(",") if e.strip()}
                dirs = [str(Path(args.local) / n) for n in names_all if (Path(args.local) / n).is_dir()]
                commits = activity.from_git(dirs, emails) if emails else []
            else:
                commits = activity.from_github(spec["owner"])
            commits = [c for c in commits if c["repo"] not in spec.get("exclude", [])]
            if commits:
                ev["rhythm"] = data.rhythm(commits)
            elif previous.get("rhythm"):
                ev["rhythm"] = previous["rhythm"]
        except Exception as err:
            print(f"::warning::commit rhythm unavailable, keeping the last snapshot: {err}")
            if previous.get("rhythm"):
                ev["rhythm"] = previous["rhythm"]
        for item in spec["flagships"] + spec["systems"]:
            if item["metric"].get("tests") and ev["signals"].get(item["repo"], {}).get("tests"):
                ev["metrics"][item["repo"]] = str(ev["signals"][item["repo"]]["tests"])
        EVIDENCE.write_text(json.dumps(ev, indent=1) + "\n")
    render(spec, gh, ev)
    print(f"links {len(ev.get('links', {}))} · metrics {ev.get('metrics', {})} · stats {'yes' if gh.get('days') else 'no'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
