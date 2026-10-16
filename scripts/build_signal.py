"""Render assets/signal.svg: 12 months of contributions, streaks, weekly rhythm and languages.

  python3 scripts/build_signal.py --github LOGIN               # GitHub API, needs GH_TOKEN (used in Actions)
  python3 scripts/build_signal.py --from-git DIR... --emails A,B  # offline preview from local clones

Never fails the build: if data can't be fetched, the existing SVG is left untouched.
"""

import argparse
import json
import os
import subprocess
import sys
import urllib.request
from collections import Counter
from datetime import date, timedelta
from pathlib import Path
from xml.sax.saxutils import escape

from theme import AMBER, BORDER, CATEGORICAL, FAINT, MONO, MUTED, OTHER, PANEL, SANS, SURFACE, TEAL, TEXT

OUT = Path(__file__).resolve().parent.parent / "assets" / "signal.svg"

QUERY = """
query($login: String!) {
  user(login: $login) {
    contributionsCollection {
      contributionCalendar { weeks { contributionDays { date contributionCount } } }
    }
    repositories(ownerAffiliations: OWNER, privacy: PUBLIC, isFork: false, first: 100) {
      totalCount
      nodes { isArchived languages(first: 20, orderBy: {field: SIZE, direction: DESC}) { edges { size node { name } } } }
    }
  }
}
"""

EXTENSIONS = {
    ".py": "Python", ".ipynb": "Jupyter Notebook", ".js": "JavaScript", ".jsx": "JavaScript", ".mjs": "JavaScript",
    ".cjs": "JavaScript", ".ts": "TypeScript", ".tsx": "TypeScript", ".cpp": "C++", ".hpp": "C++", ".h": "C++",
    ".html": "HTML", ".css": "CSS", ".java": "Java", ".kt": "Kotlin", ".swift": "Swift", ".sh": "Shell", ".rb": "Ruby",
}
SKIP_PARTS = ("node_modules/", "dist/", "build/", "vendor/", ".min.", "package-lock", "assets/")


def from_github(login: str) -> dict:
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if not token:
        raise RuntimeError("GH_TOKEN is not set")
    request = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": {"login": login}}).encode(),
        headers={"Authorization": f"bearer {token}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        payload = json.load(response)
    if payload.get("errors"):
        raise RuntimeError(payload["errors"][0].get("message", "GraphQL error"))
    user = payload["data"]["user"]
    weeks = [
        [(d["date"], d["contributionCount"]) for d in w["contributionDays"]]
        for w in user["contributionsCollection"]["contributionCalendar"]["weeks"]
    ]
    languages = Counter()
    for repo in user["repositories"]["nodes"]:
        if repo["isArchived"]:
            continue
        for edge in repo["languages"]["edges"]:
            languages[edge["node"]["name"]] += edge["size"]
    return {
        "weeks": weeks,
        "public_repos": user["repositories"]["totalCount"],
        "languages": languages,
        "source": "GitHub contribution calendar",
    }


def from_git(dirs: list[str], emails: set[str]) -> dict:
    today = date.today()
    start = today - timedelta(days=364)
    start -= timedelta(days=(start.weekday() + 1) % 7)  # calendar weeks start on Sunday, like GitHub's
    per_day, languages = Counter(), Counter()
    for repo in dirs:
        log = subprocess.run(
            ["git", "-C", repo, "log", "--all", f"--since={start.isoformat()}", "--format=%ae %ad", "--date=short"],
            capture_output=True, text=True, check=True,
        ).stdout
        for line in log.splitlines():
            email, day = line.rsplit(" ", 1)
            if email.lower() in emails:
                per_day[day] += 1
        tree = subprocess.run(["git", "-C", repo, "ls-tree", "-r", "-l", "HEAD"], capture_output=True, text=True, check=True).stdout
        for line in tree.splitlines():
            meta, path = line.split("\t", 1)
            size = meta.split()[3]
            language = EXTENSIONS.get(Path(path).suffix.lower())
            if language and size.isdigit() and not any(part in path for part in SKIP_PARTS):
                languages[language] += int(size)
    days = [start + timedelta(days=i) for i in range((today - start).days + 1)]
    weeks = [[(d.isoformat(), per_day[d.isoformat()]) for d in days[i:i + 7]] for i in range(0, len(days), 7)]
    return {"weeks": weeks, "public_repos": len(dirs), "languages": languages, "source": "commit history of public repos"}


def summarize(data: dict) -> dict:
    days = [count for week in data["weeks"] for _, count in week]
    longest = run = 0
    for count in days:
        run = run + 1 if count else 0
        longest = max(longest, run)
    weekly = [sum(c for _, c in week) for week in data["weeks"]]
    return {
        "total": sum(days),
        "active_months": len({d[:7] for week in data["weeks"] for d, c in week if c}),
        "longest_streak": longest,
        "weekly": weekly,
        "week_starts": [week[0][0] for week in data["weeks"]],
        "peak_week": max(weekly) if weekly else 0,
    }


def bar_path(x: float, base: float, width: float, height: float, r: float = 2.0) -> str:
    """A bar anchored to the baseline with only its data end rounded."""
    r = min(r, width / 2, height)
    top = base - height
    return (
        f"M{x:.1f},{base:.1f} V{top + r:.1f} Q{x:.1f},{top:.1f} {x + r:.1f},{top:.1f} "
        f"H{x + width - r:.1f} Q{x + width:.1f},{top:.1f} {x + width:.1f},{top + r:.1f} V{base:.1f} Z"
    )


def render(data: dict, stats: dict, updated: str) -> str:
    width, left, right = 900, 32, 868
    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} 350" width="100%" role="img" aria-labelledby="t d">',
        '<title id="t">Live GitHub signal for the last 12 months</title>',
        f'<desc id="d">{stats["total"]} contributions, active in {stats["active_months"]} of the last 12 months, longest streak {stats["longest_streak"]} days, '
        f'busiest week {stats["peak_week"]}, {data["public_repos"]} public repositories. Weekly contribution bars and languages by bytes of code.</desc>',
        f'<rect x="0.5" y="0.5" width="{width - 1}" height="349" rx="16" fill="{SURFACE}" stroke="{BORDER}"/>',
        f'<text x="{left}" y="40" font-family="{MONO}" font-size="12" letter-spacing="3" fill="{TEAL}">LIVE SIGNAL</text>',
        f'<text x="{left}" y="66" font-family="{SANS}" font-size="20" font-weight="700" fill="{TEXT}">Last 12 months on GitHub</text>',
        f'<text x="{right}" y="40" text-anchor="end" font-family="{MONO}" font-size="10.5" fill="{MUTED}">updated {updated} · {escape(data["source"])}</text>',
    ]

    tiles = [
        (stats["total"], "CONTRIBUTIONS"),
        (f'{stats["active_months"]} / 12', "ACTIVE MONTHS"),
        (stats["longest_streak"], "LONGEST STREAK"),
        (stats["peak_week"], "BUSIEST WEEK"),
        (data["public_repos"], "PUBLIC REPOS"),
    ]
    tile_w, tile_gap = 160, 9
    for i, (value, label) in enumerate(tiles):
        x = left + i * (tile_w + tile_gap)
        out.append(f'<rect x="{x}" y="86" width="{tile_w}" height="64" rx="10" fill="{PANEL}" stroke="{BORDER}"/>')
        shown = f"{value:,}" if isinstance(value, int) else value
        out.append(f'<text x="{x + 16}" y="120" font-family="{SANS}" font-size="26" font-weight="700" fill="{TEXT}">{shown}</text>')
        out.append(f'<text x="{x + 16}" y="140" font-family="{MONO}" font-size="10" letter-spacing="1.5" fill="{MUTED}">{label}</text>')

    # Weekly rhythm: one series, so no legend; the peak and the average are labelled directly.
    weekly, base, plot_h = stats["weekly"], 258, 76
    slot = (right - left) / max(1, len(weekly))
    peak = max(weekly) if weekly else 0
    scale = plot_h / peak if peak else 0
    peak_index = weekly.index(peak) if peak else -1
    out.append(f'<line x1="{left}" y1="{base}" x2="{right}" y2="{base}" stroke="{BORDER}"/>')
    for i, count in enumerate(weekly):
        if not count:
            continue
        x = left + i * slot + 1
        color = AMBER if i == peak_index else TEAL
        out.append(
            f'<path d="{bar_path(x, base, slot - 2, max(2, count * scale))}" fill="{color}">'
            f'<title>Week of {stats["week_starts"][i]}: {count} contributions</title></path>'
        )
    if peak:
        px = left + peak_index * slot + slot / 2
        anchor = "end" if px > right - 60 else "start" if px < left + 60 else "middle"
        out.append(f'<text x="{px:.1f}" y="{base - peak * scale - 6:.1f}" text-anchor="{anchor}" font-family="{MONO}" font-size="10.5" fill="{TEXT}">peak {peak}</text>')
        average = sum(weekly) / len(weekly)
        ay = base - average * scale
        out.append(f'<line x1="{left}" y1="{ay:.1f}" x2="{right}" y2="{ay:.1f}" stroke="{FAINT}" stroke-dasharray="3 4"/>')
        out.append(f'<text x="{right}" y="{ay - 5:.1f}" text-anchor="end" font-family="{MONO}" font-size="10.5" fill="{MUTED}">avg {average:.1f} / week</text>')
    last_month = None
    for i, start in enumerate(stats["week_starts"]):
        month = start[:7]
        if month != last_month and i > 0:
            label = date.fromisoformat(start).strftime("%b")
            out.append(f'<text x="{left + i * slot:.1f}" y="{base + 15}" font-family="{MONO}" font-size="10" fill="{MUTED}">{label}</text>')
        last_month = month

    # Languages by bytes: fixed category order, 2px surface gaps, labels carry the identity.
    languages = data["languages"].most_common()
    total_bytes = sum(size for _, size in languages)
    if total_bytes:
        top = languages[:5]
        rest = total_bytes - sum(size for _, size in top)
        segments = [(name, size, CATEGORICAL[i]) for i, (name, size) in enumerate(top)]
        if rest / total_bytes >= 0.005:
            segments.append(("Other", rest, OTHER))
        x, y = left, 292
        for name, size, color in segments:
            w = (right - left) * size / total_bytes
            if w > 2:
                out.append(f'<rect x="{x:.1f}" y="{y}" width="{w - 2:.1f}" height="10" rx="2" fill="{color}"><title>{escape(name)}: {100 * size / total_bytes:.1f}%</title></rect>')
            x += w
        lx = left
        for name, size, color in segments:
            label = f"{name} {100 * size / total_bytes:.0f}%"
            out.append(f'<circle cx="{lx + 4}" cy="322" r="4" fill="{color}"/>')
            out.append(f'<text x="{lx + 13}" y="326" font-family="{SANS}" font-size="12" fill="{TEXT}">{escape(label)}</text>')
            lx += 28 + len(label) * 7
    out.append("</svg>\n")
    return "\n".join(out)


def main() -> int:
    parser = argparse.ArgumentParser()
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--github", metavar="LOGIN")
    source.add_argument("--from-git", nargs="+", metavar="DIR")
    parser.add_argument("--emails", default="", help="comma-separated author emails for --from-git")
    args = parser.parse_args()
    try:
        if args.github:
            data = from_github(args.github)
        else:
            data = from_git(args.from_git, {e.strip().lower() for e in args.emails.split(",") if e.strip()})
    except Exception as error:  # keep the last good SVG rather than failing the workflow
        print(f"::warning::signal not refreshed: {error}", file=sys.stderr)
        return 0
    OUT.write_text(render(data, summarize(data), date.today().isoformat()), encoding="utf-8")
    print(f"wrote {OUT.relative_to(Path.cwd()) if OUT.is_relative_to(Path.cwd()) else OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
