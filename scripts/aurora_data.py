"""Data for the Aurora profile: GitHub stats (GraphQL), code links, live metrics and recent commits.

Everything here degrades gracefully: when a source can't be reached, the last good value in data/*.json is kept.
"""

from __future__ import annotations

import fnmatch
import json
import os
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

API = "https://api.github.com"

QUERY = """
query($login: String!) {
  user(login: $login) {
    followers { totalCount }
    contributionsCollection {
      totalCommitContributions totalPullRequestContributions totalIssueContributions
      contributionCalendar { totalContributions weeks { contributionDays { date contributionCount } } }
    }
    repositories(ownerAffiliations: OWNER, privacy: PUBLIC, isFork: false, first: 100, orderBy: {field: CREATED_AT, direction: ASC}) {
      nodes {
        name createdAt pushedAt diskUsage stargazerCount isArchived
        primaryLanguage { name }
        languages(first: 12, orderBy: {field: SIZE, direction: DESC}) { edges { size node { name } } }
      }
    }
  }
}
"""


def _token() -> str | None:
    return os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")


def _request(url: str, data: bytes | None = None, accept: str = "application/vnd.github+json"):
    headers = {"User-Agent": "aurora-profile", "Accept": accept}
    if _token():
        headers["Authorization"] = f"Bearer {_token()}"
    if data is not None:
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, headers=headers, method="POST" if data else "GET")
    with urllib.request.urlopen(req, timeout=40) as res:
        return res.read()


def get_json(url: str):
    return json.loads(_request(url))


def get_raw(url: str) -> str:
    return _request(url, accept="application/vnd.github.raw").decode("utf-8", "replace")


# ------------------------------------------------------------------------------------------------ GitHub stats

def fetch_github(login: str, exclude: list[str]) -> dict:
    body = json.dumps({"query": QUERY, "variables": {"login": login}}).encode()
    payload = json.loads(_request(f"{API}/graphql", data=body))
    if payload.get("errors"):
        raise RuntimeError(payload["errors"])
    user = payload["data"]["user"]
    cc = user["contributionsCollection"]
    days = [{"date": d["date"], "count": d["contributionCount"]}
            for w in cc["contributionCalendar"]["weeks"] for d in w["contributionDays"]]
    repos = []
    for r in user["repositories"]["nodes"]:
        if r["name"] in exclude:
            continue
        repos.append({"name": r["name"], "created": r["createdAt"][:10], "pushed": (r["pushedAt"] or "")[:10],
                      "kb": r["diskUsage"] or 0, "stars": r["stargazerCount"], "archived": r["isArchived"],
                      "lang": (r["primaryLanguage"] or {}).get("name"),
                      "languages": [[e["node"]["name"], e["size"]] for e in r["languages"]["edges"]]})
    return {"fetched_at": now_iso(), "login": login, "followers": user["followers"]["totalCount"],
            "totals": {"contributions": cc["contributionCalendar"]["totalContributions"],
                       "commits": cc["totalCommitContributions"], "prs": cc["totalPullRequestContributions"],
                       "issues": cc["totalIssueContributions"]},
            "days": days, "repos": repos}


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def streaks(days: list[dict]) -> tuple[int, int, int]:
    """(active days, longest streak, current streak) over the calendar."""
    longest = run = 0
    for d in days:
        run = run + 1 if d["count"] > 0 else 0
        longest = max(longest, run)
    current = 0
    for d in reversed(days):
        if d["count"] > 0:
            current += 1
        elif current or d["date"] != days[-1]["date"]:
            break
    return sum(1 for d in days if d["count"] > 0), longest, current


def weekly(days: list[dict]) -> list[dict]:
    weeks, bucket = [], []
    for d in days:
        bucket.append(d)
        if date.fromisoformat(d["date"]).weekday() == 5:  # GitHub weeks run Sunday..Saturday
            weeks.append(bucket)
            bucket = []
    if bucket:
        weeks.append(bucket)
    return [{"start": w[0]["date"], "count": sum(x["count"] for x in w)} for w in weeks]


def language_shares(repos: list[dict], skip=("Jupyter Notebook",)) -> list[tuple[str, float]]:
    totals: dict[str, int] = {}
    for r in repos:
        for name, size in r["languages"]:
            if name not in skip:
                totals[name] = totals.get(name, 0) + size
    whole = sum(totals.values()) or 1
    ranked = sorted(totals.items(), key=lambda kv: kv[1], reverse=True)
    top = [(n, s / whole) for n, s in ranked[:6]]
    rest = sum(s for _, s in ranked[6:]) / whole
    return top + ([("Other", rest)] if rest > 0.001 else [])


# ------------------------------------------------------------------------------------------------ repos

class RemoteRepo:
    def __init__(self, owner: str, name: str):
        self.owner, self.name = owner, name
        branch = get_json(f"{API}/repos/{owner}/{name}")["default_branch"]
        self.sha = get_json(f"{API}/repos/{owner}/{name}/commits/{urllib.parse.quote(branch)}")["sha"]
        self._tree = None

    def read(self, path: str) -> str | None:
        try:
            return get_raw(f"{API}/repos/{self.owner}/{self.name}/contents/{urllib.parse.quote(path)}?ref={self.sha}")
        except urllib.error.HTTPError as err:
            if err.code == 404:
                return None
            raise

    def files(self) -> list[str]:
        if self._tree is None:
            tree = get_json(f"{API}/repos/{self.owner}/{self.name}/git/trees/{self.sha}?recursive=1")
            self._tree = [t["path"] for t in tree["tree"] if t["type"] == "blob"]
        return self._tree

    def recent(self, n: int = 3) -> list[dict]:
        rows = get_json(f"{API}/repos/{self.owner}/{self.name}/commits?sha={self.sha}&per_page=12")
        return [{"sha": r["sha"], "date": r["commit"]["committer"]["date"][:10], "subject": r["commit"]["message"].splitlines()[0]}
                for r in rows if len(r.get("parents", [])) <= 1][:n]


class LocalRepo:
    def __init__(self, base: Path, name: str):
        self.dir = base / name
        self.sha = self._git("rev-parse", "HEAD").strip()

    def _git(self, *args) -> str:
        return subprocess.run(["git", "-C", str(self.dir), *args], capture_output=True, text=True, check=True).stdout

    def read(self, path: str) -> str | None:
        f = self.dir / path
        return f.read_text(errors="replace") if f.is_file() else None

    def files(self) -> list[str]:
        return self._git("ls-files").splitlines()

    def recent(self, n: int = 3) -> list[dict]:
        out = self._git("log", f"-{n}", "--no-merges", "--format=%H%x09%cs%x09%s", self.sha)
        return [dict(zip(("sha", "date", "subject"), line.split("\t", 2))) for line in out.splitlines() if line]


def find_line(text: str | None, needle: str) -> int | None:
    if text is None:
        return None
    for number, line in enumerate(text.splitlines(), 1):
        if needle in line:
            return number
    return None


def measure(repo, metric: dict) -> str | None:
    if "value" in metric:
        return metric["value"]
    if metric.get("tests"):
        return None  # filled in from the account-wide signals
    if "count" in metric:
        text = repo.read(metric["count"]["path"])
        return str(text.count(metric["count"]["needle"])) if text else None
    if "files" in metric:
        pattern = metric["files"]["glob"]
        files = [p for p in repo.files() if "node_modules/" not in p]
        if pattern.startswith("**/"):  # any directory: match the file name only
            hits = [p for p in files if fnmatch.fnmatch(p.rsplit("/", 1)[-1], pattern[3:])]
        else:
            hits = [p for p in files if fnmatch.fnmatch(p, pattern)]
        return str(len(hits)) if hits else None
    return None


def collect(spec: dict, previous: dict, open_repo) -> dict:
    """Code links, live metrics and recent commits for every repo the page mentions."""
    owner = spec["owner"]
    repos_needed: dict[str, dict] = {}
    for card in spec["cards"]:
        repos_needed.setdefault(card["repo"], {})["claims"] = card["claims"]
    for item in spec["flagships"] + spec["systems"]:
        repos_needed.setdefault(item["repo"], {})["metric"] = item["metric"]
    old = {"links": previous.get("links", {}), "metrics": previous.get("metrics", {}), "repos": previous.get("repos", {})}
    links, metrics, shas, recent = {}, {}, {}, []
    for name, need in repos_needed.items():
        try:
            repo = open_repo(owner, name)
            shas[name] = repo.sha
        except Exception as err:
            print(f"warn: {name}: {err}", file=sys.stderr)
            repo = None
            if name in old["repos"]:
                shas[name] = old["repos"][name]
        for i, claim in enumerate(need.get("claims", []), 1):
            cid = f"{name}#{i}"
            try:
                if repo is None:
                    raise RuntimeError("unreachable")
                line = find_line(repo.read(claim["path"]), claim["needle"])
            except Exception as err:
                print(f"warn: {cid}: {err}", file=sys.stderr)
                if cid in old["links"]:
                    links[cid] = old["links"][cid]
                continue
            if line:
                links[cid] = {"sha": repo.sha, "line": line}
            else:
                print(f"::warning::{cid} ({claim['path']}) no longer contains its snippet; the link is hidden until data/aurora.json is updated")
        if "metric" in need:
            try:
                if repo is None:
                    raise RuntimeError("unreachable")
                value = measure(repo, need["metric"])
            except Exception as err:
                print(f"warn: metric {name}: {err}", file=sys.stderr)
                value = old["metrics"].get(name)
            if value is not None:
                metrics[name] = value
        try:
            if repo is None:
                raise RuntimeError("unreachable")
            recent += [{**c, "repo": name} for c in repo.recent()]
        except Exception:
            recent += [r for r in previous.get("recent", []) if r.get("repo") == name]
    recent.sort(key=lambda r: (r["date"], r["sha"]), reverse=True)
    return {"generated_at": now_iso(), "repos": shas, "links": links, "metrics": metrics, "recent": recent}


# ------------------------------------------------------------------------------------------------ account-wide signals

import re  # noqa: E402

TEST_FILE = re.compile(r"(^|/)(tests?|__tests__)/.*\.(py|js|ts|tsx)$|\.(test|spec)\.(js|ts|tsx)$|(^|/)test_[^/]*\.py$", re.I)
TEST_CASE = re.compile(r"^\s*(async\s+def\s+test_|def\s+test_|it\(|test\(|it\.each|test\.each|TEST\()", re.M)


def repo_signals(repo) -> dict:
    files = [p for p in repo.files() if "node_modules/" not in p and "/vendor/" not in p]
    test_files = [p for p in files if TEST_FILE.search(p)]
    cases = 0
    for p in test_files:
        text = repo.read(p) or ""
        cases += len(TEST_CASE.findall(text))
    readme = next((p for p in files if p.lower() == "readme.md"), None)
    readme_kb = len((repo.read(readme) or "").encode()) // 1024 if readme else 0
    return {
        "tests": cases, "test_files": len(test_files),
        "ci": len([p for p in files if p.startswith(".github/workflows/") and p.endswith((".yml", ".yaml"))]),
        "docker": any(re.search(r"(^|/)(Dockerfile|docker-compose[^/]*\.ya?ml)$", p) for p in files),
        "license": any(re.match(r"^licen[cs]e", p, re.I) for p in files),
        "adrs": len([p for p in files if re.search(r"(^|/)adr/\d+.*\.md$", p, re.I)]),
        "docs": len([p for p in files if p.startswith("docs/") and p.endswith(".md")]),
        "readme_kb": readme_kb,
    }


def health(url: str) -> bool:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "aurora-profile-healthcheck"})
        with urllib.request.urlopen(req, timeout=20) as res:
            return res.status < 400
    except Exception:
        return False


def collect_signals(names: list[str], previous: dict, open_repo, owner: str, live: dict, check_live: bool) -> dict:
    out = {}
    for name in names:
        try:
            out[name] = repo_signals(open_repo(owner, name))
        except Exception as err:
            print(f"warn: signals {name}: {err}", file=sys.stderr)
            if name in previous.get("signals", {}):
                out[name] = previous["signals"][name]
    status = {}
    for name, url in live.items():
        status[name] = health(url) if check_live else previous.get("live", {}).get(name)
    return {"signals": out, "live": status}


# ------------------------------------------------------------------------------------------------ rhythm

def rhythm(commits: list[dict]) -> dict:
    """When the commits land, in IST: per hour, per weekday x hour, chronotype and the longest session."""
    from datetime import timedelta as _td, timezone as _tz
    ist = _tz(_td(hours=5, minutes=30))
    times = sorted(c["authored_at"].astimezone(ist) for c in commits)
    n = len(times)
    if not n:
        return {}
    hours = [0] * 24
    grid = [[0] * 24 for _ in range(7)]
    for t in times:
        hours[t.hour] += 1
        grid[t.weekday()][t.hour] += 1
    share = lambda hs: sum(hours[h] for h in hs) / n
    night = share([22, 23, 0, 1, 2, 3, 4])
    bands = [("Night Owl", night, "22:00 and 05:00"), ("Early Riser", share(range(5, 11)), "05:00 and 11:00"),
             ("Afternoon Climber", share(range(11, 17)), "11:00 and 17:00"), ("Evening Climber", share(range(17, 22)), "17:00 and 22:00")]
    kind, frac, span = max(bands, key=lambda b: b[1])
    line = f"{frac:.0%} of my commits land between {span} IST."
    best = max(range(24), key=lambda h: hours[h] + hours[(h + 1) % 24] + hours[(h + 2) % 24])
    focus = hours[best] + hours[(best + 1) % 24] + hours[(best + 2) % 24]
    weekend = sum(1 for t in times if t.weekday() >= 5) / n
    # longest session: commits no more than 90 minutes apart
    sessions, cur = [], [times[0]]
    for a, b in zip(times, times[1:]):
        if (b - a).total_seconds() <= 90 * 60:
            cur.append(b)
        else:
            sessions.append(cur)
            cur = [b]
    sessions.append(cur)
    deep = max(sessions, key=lambda s: (s[-1] - s[0], len(s)))
    deep_repos = [c["repo"] for c in commits if deep[0] <= c["authored_at"].astimezone(ist) <= deep[-1]]
    top_repo = max(set(deep_repos), key=deep_repos.count) if deep_repos else ""
    bd, bh = max(((d, h) for d in range(7) for h in range(24)), key=lambda dh: grid[dh[0]][dh[1]])
    latest = max(commits, key=lambda c: c["authored_at"])
    return {
        "commits": n, "repos": len({c["repo"] for c in commits}), "active_days": len({t.date() for t in times}),
        "since": times[0].strftime("%b %Y"), "hours": hours, "grid": grid,
        "chronotype": kind, "line": line, "night": round(night, 3), "weekend": round(weekend, 3),
        "focus": [best, (best + 3) % 24, focus], "peak_hour": max(range(24), key=lambda h: hours[h]),
        "deep": {"minutes": int((deep[-1] - deep[0]).total_seconds() // 60), "commits": len(deep), "repo": top_repo,
                 "start": deep[0].strftime("%a %d %b %Y · %H:%M"), "end": deep[-1].strftime("%H:%M"),
                 "offsets": [int((t - deep[0]).total_seconds() // 60) for t in deep]},
        "busiest": [bd, bh, grid[bd][bh]],
        "latest": {"repo": latest["repo"], "subject": latest["message_first_line"],
                   "when": latest["authored_at"].astimezone(ist).strftime("%d %b %H:%M IST")},
    }
