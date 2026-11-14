"""Atlas data: one JSON cache of live GitHub numbers.

refresh() asks GitHub for the contribution calendar and the commit history, and
replaces a section of the cache only when its request succeeds, so a failed or
rate-limited run leaves the last good snapshot (and its date) untouched.
"""
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / "data" / "atlas.json"
WEEKDAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
RECENT = 4


def signal_section(login: str) -> dict:
    """Contribution calendar, repository count and languages by bytes of code."""
    import build_signal
    data = build_signal.from_github(login)
    stats = build_signal.summarize(data)
    languages = data["languages"].most_common()
    total = sum(size for _, size in languages) or 1
    top = [[name, round(100 * size / total, 1)] for name, size in languages[:5]]
    rest = round(100 - sum(share for _, share in top), 1)
    if len(languages) > 5 and rest > 0:
        top.append(["Other", rest])
    return {"total": stats["total"], "active_months": stats["active_months"], "longest_streak": stats["longest_streak"],
            "peak_week": stats["peak_week"], "public_repos": data["public_repos"],
            "weeks": [[start, count] for start, count in zip(stats["week_starts"], stats["weekly"])], "languages": top}


def commit_sections(login: str) -> tuple[dict, list]:
    """Commit hours (IST) and the latest commits, excluding merges, bots and the profile repository."""
    import build_rhythm
    import github_activity
    commits = github_activity.from_github(login)
    if not commits:
        raise RuntimeError("no commits found in the last 12 months")
    summary = build_rhythm.summarize(commits)
    rhythm = {"total": summary["total"], "per_hour": summary["per_hour"], "block": summary["block"],
              "block_share": round(summary["block_share"], 4), "busiest_weekday": WEEKDAYS[summary["busiest_day"]],
              "chronotype": summary["chronotype"]}
    recent = [{"repo": c["repo"], "sha": c["sha"], "title": c["message_first_line"],
               "date": c["authored_at"].astimezone(timezone.utc).strftime("%Y-%m-%d")}
              for c in commits if c["repo"].lower() != login.lower()][:RECENT]
    return rhythm, recent


def load(cache: Path = CACHE) -> dict:
    return json.loads(cache.read_text(encoding="utf-8"))


def validate(data: dict) -> dict:
    """Fail loudly on a malformed cache rather than render a broken card."""
    signal, rhythm = data["signal"], data["rhythm"]
    for key in ("total", "active_months", "longest_streak", "peak_week", "public_repos"):
        if not isinstance(signal[key], int):
            raise ValueError(f"signal.{key} must be an integer")
    if not signal["weeks"] or any(not re.fullmatch(r"\d{4}-\d{2}-\d{2}", w[0]) or not isinstance(w[1], int) for w in signal["weeks"]):
        raise ValueError("signal.weeks must be [date, count] pairs")
    if len(rhythm["per_hour"]) != 24:
        raise ValueError("rhythm.per_hour must have 24 values")
    for commit in data.get("recent", []):
        if not re.fullmatch(r"[A-Za-z0-9_.-]+", commit["repo"]) or not re.fullmatch(r"[a-f0-9]{7,40}", commit["sha"]):
            raise ValueError("recent commit has an invalid repository or sha")
    return data


def refresh(login: str, cache: Path = CACHE, sources=None) -> bool:
    """Update whichever sections can be fetched. Returns True if the cache changed."""
    sources = sources or {"signal": lambda: signal_section(login), "commits": lambda: commit_sections(login)}
    data = load(cache)
    before = json.dumps(data, sort_keys=True)
    for name, fetch in sources.items():
        try:
            result = fetch()
        except Exception as error:  # keep the last good snapshot rather than fail the workflow
            print(f"::warning::Atlas {name} not refreshed ({type(error).__name__}); keeping the last snapshot.", file=sys.stderr)
            continue
        if name == "signal":
            data["signal"] = result
        else:
            data["rhythm"], data["recent"] = result
    try:
        validate(data)
    except (KeyError, TypeError, ValueError) as error:
        print(f"::warning::Atlas data rejected ({error}); keeping the last snapshot.", file=sys.stderr)
        return False
    if json.dumps(data, sort_keys=True) == before:
        return False
    data["refreshed_at"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    temporary = cache.with_suffix(".tmp")
    temporary.write_text(json.dumps(data, indent=1) + "\n", encoding="utf-8")
    temporary.replace(cache)
    return True
