"""Shared commit fetching for the live cards (build_rhythm.py, build_terminal.py).

Two sources, same output: a list of the candidate's own commits from the last 365 days,
newest first, as dicts {repo, sha, message_first_line, authored_at (aware datetime)}.

  --github LOGIN                 GitHub REST API, token from GH_TOKEN or GITHUB_TOKEN (used in Actions)
  --from-git DIR... --emails A,B  local clones, matched on author email (offline preview)

Commits authored by Claude (noreply@anthropic.com) or by any [bot] account are not the candidate's
work and are always dropped. Merge commits are dropped too: merging someone else's (or Claude's)
pull request is not authoring it.
"""

import argparse
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

API = "https://api.github.com"
WINDOW_DAYS = 365
IST = timezone(timedelta(hours=5, minutes=30), "IST")  # India has no DST, so a fixed offset is exact

SOURCE_API = "GitHub API"
SOURCE_GIT = "local git history"


def is_excluded(name: str, email: str) -> bool:
    """Authors whose commits are never counted as the candidate's."""
    name, email = (name or "").strip(), (email or "").strip().lower()
    return (
        name.lower() == "claude"
        or email == "noreply@anthropic.com"
        or "[bot]" in name.lower()
        or "[bot]" in email
    )


def _parse_time(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


# ---------------------------------------------------------------- GitHub REST

def _get(url: str, token: str):
    request = urllib.request.Request(
        url,
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "profile-readme-cards",
        },
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        link = response.headers.get("Link", "")
        return json.load(response), link


def _paginate(url: str, token: str):
    """Yield items from every page, following Link: rel="next".

    GitHub's next link may use the numeric /repositories/{id}/ form; we keep our own owner/repo
    URL and only take the page number from it, which works everywhere."""
    while url:
        page, link = _get(url, token)
        yield from page
        match = re.search(r'<([^>]+)>;\s*rel="next"', link or "")
        if not match:
            return
        next_page = urllib.parse.parse_qs(urllib.parse.urlsplit(match.group(1)).query).get("page")
        if not next_page:
            url = match.group(1)
            continue
        parts = urllib.parse.urlsplit(url)
        query = dict(urllib.parse.parse_qsl(parts.query))
        query["page"] = next_page[0]
        url = urllib.parse.urlunsplit(parts._replace(query=urllib.parse.urlencode(query)))


def _is_noreply_of(email: str, login: str) -> bool:
    email = (email or "").lower()
    return email == f"{login.lower()}@users.noreply.github.com" or email.endswith(f"+{login.lower()}@users.noreply.github.com")


def from_github(login: str) -> list[dict]:
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if not token:
        raise RuntimeError("GH_TOKEN / GITHUB_TOKEN is not set")
    since = (datetime.now(timezone.utc) - timedelta(days=WINDOW_DAYS)).strftime("%Y-%m-%dT%H:%M:%SZ")
    owner = urllib.parse.quote(login)
    commits = []
    for repo in _paginate(f"{API}/users/{owner}/repos?type=owner&per_page=100", token):
        if repo.get("fork"):
            continue
        name = repo["name"]
        # No author= filter: GitHub's filter silently misses some commits (seen on fresh repos), so we
        # list the window and match on the linked account or the account's noreply address ourselves.
        query = urllib.parse.urlencode({"since": since, "per_page": 100})
        url = f"{API}/repos/{owner}/{urllib.parse.quote(name)}/commits?{query}"
        try:
            items = list(_paginate(url, token))
        except urllib.error.HTTPError as error:
            if error.code == 409:  # empty repository
                continue
            raise
        for item in items:
            author = item["commit"]["author"] or {}
            linked = ((item.get("author") or {}).get("login") or "").lower()
            if linked != login.lower() and not _is_noreply_of(author.get("email", ""), login):
                continue
            if is_excluded(author.get("name", ""), author.get("email", "")) or len(item.get("parents") or []) > 1:
                continue
            message = item["commit"].get("message") or ""
            commits.append({
                "repo": name,
                "sha": item["sha"],
                "message_first_line": message.splitlines()[0].strip() if message else "",
                "authored_at": _parse_time(author["date"]),
            })
    return _finish(commits)


# ---------------------------------------------------------------- local clones

def from_git(dirs: list[str], emails: set[str]) -> list[dict]:
    since = datetime.now(timezone.utc) - timedelta(days=WINDOW_DAYS)
    commits = []
    sep = "\x1f"
    for directory in dirs:
        log = subprocess.run(
            ["git", "-C", directory, "log", "--all", "--no-merges", f"--since={since.isoformat()}",
             f"--format=%H{sep}%an{sep}%ae{sep}%aI{sep}%s"],
            capture_output=True, text=True, check=True,
        ).stdout
        repo = Path(directory).resolve().name
        for line in log.splitlines():
            parts = line.split(sep)
            if len(parts) != 5:
                continue
            sha, name, email, when, subject = parts
            if email.lower() not in emails or is_excluded(name, email):
                continue
            commits.append({
                "repo": repo,
                "sha": sha,
                "message_first_line": subject.strip(),
                "authored_at": _parse_time(when),
            })
    return _finish(commits)


def _finish(commits: list[dict]) -> list[dict]:
    """Deduplicate by sha, keep the 365-day window, newest first."""
    cutoff = datetime.now(timezone.utc) - timedelta(days=WINDOW_DAYS)
    unique = {c["sha"]: c for c in commits if c["authored_at"] >= cutoff}
    return sorted(unique.values(), key=lambda c: c["authored_at"], reverse=True)


# ---------------------------------------------------------------- CLI shared by the card builders

def add_source_args(parser: argparse.ArgumentParser) -> None:
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--github", metavar="LOGIN")
    source.add_argument("--from-git", nargs="+", metavar="DIR")
    parser.add_argument("--emails", default="", help="comma-separated author emails for --from-git")


def load(args: argparse.Namespace) -> tuple[list[dict], str]:
    """Return (commits, source label) for the parsed CLI arguments."""
    if args.github:
        return from_github(args.github), SOURCE_API
    emails = {e.strip().lower() for e in args.emails.split(",") if e.strip()}
    if not emails:
        raise RuntimeError("--from-git needs --emails")
    return from_git(args.from_git, emails), SOURCE_GIT


def run_card(name: str, out: Path, render) -> int:
    """CLI entry for a card: fetch, render, write. Never fails the workflow; on any error the
    existing SVG is left untouched and a ::warning:: is printed."""
    parser = argparse.ArgumentParser(description=f"Render {out.name}")
    add_source_args(parser)
    args = parser.parse_args()
    try:
        commits, source = load(args)
        if not commits:
            raise RuntimeError("no commits found in the last 12 months")
        svg = render(commits, source, datetime.now(IST).date().isoformat())
        out.write_text(svg, encoding="utf-8")
    except Exception as error:  # keep the last good SVG rather than failing the workflow
        print(f"::warning::{name} not refreshed: {error}", file=sys.stderr)
        return 0
    print(f"wrote {out} ({len(commits)} commits, {source})")
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Print the commits the cards would use")
    add_source_args(parser)
    try:
        found, label = load(parser.parse_args())
    except Exception as error:
        print(f"::warning::activity not fetched: {error}", file=sys.stderr)
        sys.exit(0)
    print(f"{len(found)} commits from {label}")
    for c in found:
        print(c["authored_at"].astimezone(IST).isoformat(), c["repo"], c["sha"][:7], c["message_first_line"][:70])
