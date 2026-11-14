#!/usr/bin/env python3
"""Build the Atlas profile: every image under assets/atlas and the two generated README blocks.

  python3 scripts/build_atlas.py             rebuild from cached data (offline, deterministic)
  python3 scripts/build_atlas.py --refresh   ask GitHub first (needs GH_TOKEN); failed requests keep the old data

Standard library only. Text that comes from GitHub (repository names, descriptions, commit
titles) is escaped before it reaches an SVG or the README.
"""
import argparse
from html import escape
import json
from pathlib import Path
import re
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import atlas_data  # noqa: E402
import build_catalog  # noqa: E402
from atlas_featured import FEATURED, featured  # noqa: E402
from atlas_hero import hero  # noqa: E402
from atlas_kit import CYAN, VIOLET, VOLT  # noqa: E402
import atlas_scenes as scenes  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "atlas"
LOBBY = ("<!-- PROJECT-LOBBY:START -->", "<!-- PROJECT-LOBBY:END -->")
FEED = ("<!-- MISSION-FEED:START -->", "<!-- MISSION-FEED:END -->")
BUTTONS = [("linkedin", "LINKEDIN", VOLT), ("email", "EMAIL", CYAN), ("repos", "ALL REPOSITORIES", VIOLET)]


def replace_block(readme: str, markers: tuple[str, str], block: str) -> str:
    start, end = markers
    if readme.count(start) != 1 or readme.count(end) != 1:
        raise ValueError(f"README must contain exactly one {start} … {end} pair")
    return readme.split(start)[0] + block + readme.split(end)[1]


def lobby_block(rows: list[dict], owner: str) -> str:
    """Two repository cards per row; phones get the compact card through <picture>."""
    items = []
    for row in rows:
        alt = escape(f'{row["title"]} — {row["description"]} Stack: {", ".join(row["stack"])}', quote=True)
        items.append(f'<a href="{row["url"]}"><picture><source media="(max-width: 600px)" srcset="assets/atlas/repo/{row["slug"]}-mini.svg" />'
                     f'<img src="assets/atlas/repo/{row["slug"]}.svg" width="49%" alt="{alt}" /></picture></a>')
    if len(items) % 2:
        items.append(f'<a href="https://github.com/{owner}?tab=repositories"><picture><source media="(max-width: 600px)" srcset="assets/atlas/repo/browse-mini.svg" />'
                     '<img src="assets/atlas/repo/browse.svg" width="49%" alt="Browse all repositories" /></picture></a>')
    groups = ['<p align="center">\n' + "\n".join(items[i:i + 2]) + "\n</p>" for i in range(0, len(items), 2)]
    return LOBBY[0] + "\n\n" + "\n\n".join(groups) + "\n\n" + LOBBY[1]


def _plain(value: str, limit: int = 96) -> str:
    """Commit titles are other people's text: neutralise HTML and Markdown before they enter the README."""
    value = " ".join(str(value).split())
    if len(value) > limit:
        value = value[: limit - 1].rstrip() + "…"
    value = escape(value)
    for char, entity in (("|", "&#124;"), ("[", "&#91;"), ("]", "&#93;"), ("`", "&#96;"), ("*", "&#42;"), ("_", "&#95;"), ("~", "&#126;")):
        value = value.replace(char, entity)
    return value


def feed_block(data: dict, owner: str) -> str:
    rows = [FEED[0], "", "| Repository | Latest change | Date |", "| :-- | :-- | :-- |"]
    for commit in data.get("recent", []):
        repo, sha = commit["repo"], commit["sha"]
        if not re.fullmatch(r"[A-Za-z0-9_.-]+", repo) or not re.fullmatch(r"[a-f0-9]{7,40}", sha):
            raise ValueError("Invalid cached commit")
        base = f"https://github.com/{owner}/{repo}"
        date = commit["date"] if re.fullmatch(r"\d{4}-\d{2}-\d{2}", commit["date"]) else ""
        rows.append(f'| [{repo}]({base}) | [{_plain(commit["title"])}]({base}/commit/{sha}) | {date} |')
    stamp = data.get("refreshed_at", "")[:10]
    rows += ["", f"<sub>My latest commits, excluding merges and bots. Snapshot {stamp}; refreshed every six hours.</sub>", "", FEED[1]]
    return "\n".join(rows)


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists() or path.read_text(encoding="utf-8") != content:
        path.write_text(content, encoding="utf-8")


def build(refresh: bool = False) -> int:
    config = json.loads((ROOT / "profile.json").read_text(encoding="utf-8"))
    owner = config["owner"]
    repo_cache = ROOT / "data" / "repos.json"
    if refresh:
        build_catalog.refresh_cache(config, repo_cache)
        atlas_data.refresh(owner)
    data = atlas_data.validate(atlas_data.load())
    repos = json.loads(repo_cache.read_text(encoding="utf-8"))
    if repos["owner"] != owner:
        raise ValueError("Cached repository owner differs from profile.json")
    # The grid shows every public repository except the three with their own cards above.
    rows = build_catalog.selected(dict(config, featured=[p["repo"] for p in FEATURED]), repos["repositories"])
    # README blocks first: if the markers are missing nothing is written at all.
    readme_path = ROOT / "README.md"
    readme = replace_block(readme_path.read_text(encoding="utf-8"), LOBBY, lobby_block(rows, owner))
    readme = replace_block(readme, FEED, feed_block(data, owner))

    for mobile in (False, True):
        suffix = "-mobile" if mobile else ""
        write(OUT / f"hero{suffix}.svg", hero(mobile))
        for index, project in enumerate(FEATURED):
            write(OUT / f'{project["key"]}{suffix}.svg', featured(index, mobile))
        write(OUT / f"kit{suffix}.svg", scenes.kit(config["build_kit"], mobile))
        write(OUT / f"pulse{suffix}.svg", scenes.pulse(data, mobile))
        write(OUT / f"route{suffix}.svg", scenes.route(mobile))
        write(OUT / f"contact{suffix}.svg", scenes.contact(mobile))
    for slug, text, color in BUTTONS:
        write(OUT / f"btn-{slug}.svg", scenes.button(text, color))
    keep = {"browse.svg", "browse-mini.svg"}
    for index, row in enumerate(rows):
        write(OUT / "repo" / f'{row["slug"]}.svg', scenes.repo_card(row, index))
        write(OUT / "repo" / f'{row["slug"]}-mini.svg', scenes.repo_mini(row, index))
        keep |= {f'{row["slug"]}.svg', f'{row["slug"]}-mini.svg'}
    write(OUT / "repo" / "browse.svg", scenes.browse_card())
    write(OUT / "repo" / "browse-mini.svg", scenes.browse_card(True))
    for stale in (OUT / "repo").glob("*.svg"):
        if stale.name not in keep:
            stale.unlink()
    write(readme_path, readme)
    print(f"Atlas built: {len(rows)} repository cards, snapshot {data.get('refreshed_at', '')[:10]}.")
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--refresh", action="store_true", help="fetch fresh data from GitHub before building")
    sys.exit(build(parser.parse_args().refresh))
