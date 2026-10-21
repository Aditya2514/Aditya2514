"""Render assets/stack.svg: which technologies each project really uses, derived from the repos themselves.

  python3 scripts/build_stack.py --clones DIR          # DIR holds the full-history clones (LexGuard, Pikina, ...)
  python3 scripts/build_stack.py --clones DIR --dump   # print raw dependencies / imports per project, no SVG

Nothing in the matrix is typed by hand. For every project the script reads the working copy under --work-root
(default: the folder holding this profile repo) and the full-history clone under --clones, and keeps only files
the candidate committed: each path is read as it stood in the candidate's latest commit touching it. Paths only
ever committed by someone else (an AI assistant, a teammate, a template bot) are ignored, and later edits by
others are not seen, so e.g. an assistant-added Linux backend or plugin system never counts as the candidate's.

The scan rules (dependency names, import names, code and path patterns) are RULES below. The derived matrix is
printed with the first file that justified each dot, then the SVG is written. If any project's sources are
missing the script exits without touching the SVG.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import tomllib
from pathlib import Path
from xml.sax.saxutils import escape

from theme import AMBER, BORDER, FAINT, MONO, MUTED, PANEL, SANS, SURFACE, TEAL, TEXT

OUT = Path(__file__).resolve().parent.parent / "assets" / "stack.svg"

# Commits by these e-mail addresses are the candidate's (local and GitHub no-reply identities).
CANDIDATE = re.compile(r"adityasinghv05@gmail\.com|aditya2514@users\.noreply\.github\.com", re.I)

# Column label, one-word role, working-copy dir under --work-root, full-history clone dir under --clones
PROJECTS = [
    ("LexGuard", "legal AI", "lexguard", "LexGuard"),
    ("Pikina", "desktop AI", "pikina", "Pikina"),
    ("Resilion", "supply chain", "resilion-", "Resilion-"),
    ("Noesis", "RAG", "noesis", "Noesis"),
    ("OpenEnv planner", "RL environment", "meta_openenv", "Meta_OpenEnv"),
    ("ShopKart", "e-commerce", None, "Shopkart"),
    ("BookFinder", "mobile", "vidya", "Vidya"),
    ("C++ shell", "POSIX shell", "codecrafters-shell-cpp", "codecrafters-shell-cpp"),
]

# Rule kinds:  npm / py      -> a dependency name in package.json / requirements*.txt or pyproject.toml
#              jsimp / pyimp -> a module imported (require / import / from) in a JS/TS or Python source file
#              code          -> a regex found in a source or CI file (not docs, reports or data)
#              path          -> a tracked file path
#              lines         -> at least N non-blank lines in files with these extensions
# A dot needs a USE rule (jsimp, pyimp, code, path or lines) to fire. A dependency that is only declared in a
# manifest (npm / py) is never enough on its own: e.g. Resilion pins fastapi for a later phase but imports it
# nowhere, so it gets no FastAPI dot. Manifest hits are printed alongside as supporting evidence.
RULES = [
    ("Languages", [
        ("Python", [("lines", r"py", 150)]),
        ("JavaScript", [("lines", r"js|jsx|mjs|cjs", 150)]),
        ("TypeScript", [("lines", r"ts|tsx", 150)]),
        ("C++", [("lines", r"cpp|cc|cxx|hpp", 150)]),
    ]),
    ("AI & LLM", [
        ("Gemini", [("npm", r"@google/(generative-ai|genai)"), ("jsimp", r"@google/(generative-ai|genai)"),
                    ("py", r"google-genai|google-generativeai"),
                    ("code", r"from google import genai|google\.generativeai|generativelanguage\.googleapis\.com")]),
        ("Groq", [("npm", r"groq-sdk"), ("jsimp", r"groq-sdk"), ("py", r"groq"), ("pyimp", r"groq"), ("code", r"api\.groq\.com")]),
        ("Ollama", [("npm", r"ollama"), ("jsimp", r"ollama"), ("pyimp", r"ollama"), ("code", r"(localhost|127\.0\.0\.1):11434")]),
        ("Hugging Face", [("npm", r"@xenova/transformers|@huggingface/.+"), ("jsimp", r"@xenova/transformers|@huggingface/.+"),
                          ("pyimp", r"transformers|huggingface_hub|datasets|setfit"),
                          ("code", r"(router|api-inference)\.huggingface\.co")]),
        ("sentence-transformers", [("py", r"sentence-transformers"), ("pyimp", r"sentence_transformers")]),
        ("ChromaDB", [("npm", r"chromadb"), ("jsimp", r"chromadb"), ("py", r"chromadb"), ("pyimp", r"chromadb")]),
        ("Whisper", [("pyimp", r"whisper|faster_whisper"), ("code", r"whisper-(large|medium|small|base|1)\b")]),
    ]),
    ("Backend & data", [
        ("Node.js · Express", [("npm", r"express"), ("jsimp", r"express")]),
        ("FastAPI", [("py", r"fastapi"), ("pyimp", r"fastapi")]),
        ("Flask", [("py", r"flask"), ("pyimp", r"flask")]),
        ("Pydantic", [("py", r"pydantic"), ("pyimp", r"pydantic")]),
        ("MongoDB", [("npm", r"mongoose|mongodb"), ("jsimp", r"mongoose|mongodb"), ("pyimp", r"pymongo|motor")]),
        ("Redis", [("npm", r"redis|ioredis"), ("jsimp", r"redis|ioredis"), ("pyimp", r"redis")]),
        ("NetworkX", [("py", r"networkx"), ("pyimp", r"networkx")]),
        ("Firebase", [("npm", r"firebase|@react-native-firebase/.+"), ("jsimp", r"firebase|@react-native-firebase/.+"),
                      ("pyimp", r"firebase_admin")]),
    ]),
    ("Frontend & mobile", [
        ("React", [("npm", r"react-dom"), ("jsimp", r"react-dom|react-router-dom")]),
        ("React Native", [("npm", r"react-native"), ("jsimp", r"react-native")]),
        ("Electron", [("npm", r"electron"), ("jsimp", r"electron")]),
        ("Streamlit", [("py", r"streamlit"), ("pyimp", r"streamlit")]),
    ]),
    ("Infra", [
        ("Docker", [("path", r"(^|/)Dockerfile[^/]*$|(^|/)docker-compose[^/]*\.ya?ml$")]),
        ("GitHub Actions", [("path", r"^\.github/workflows/[^/]+\.ya?ml$")]),
        ("Vercel", [("path", r"(^|/)vercel\.json$")]),
        ("Hugging Face Spaces", [("code", r"huggingface\.co/spaces|huggingface-spaces")]),
    ]),
]

SKIP = re.compile(
    r"(^|/)(node_modules|vendor|dist|build|\.venv|venv|__pycache__|Pods)/"
    r"|(package-lock\.json|yarn\.lock|pnpm-lock\.yaml|uv\.lock|Podfile\.lock|\.min\.js)$"
)
TEXT_EXT = re.compile(
    r"\.(py|js|jsx|mjs|cjs|ts|tsx|cpp|cc|cxx|hpp|h|json|toml|txt|cfg|ini|ya?ml|sh|bat|html|css|gradle|kt)$"
    r"|(^|/)(Dockerfile[^/]*|CMakeLists\.txt|Procfile|Gemfile)$"
)
CODE_EXT = re.compile(r"\.(py|js|jsx|mjs|cjs|ts|tsx|sh|ya?ml|toml)$|(^|/)Dockerfile[^/]*$")
TOOL_CONFIG = re.compile(r"(^|/)[^/]*\.config\.[cm]?[jt]s$|(^|/)\.[^/]+$")
MAX_BYTES = 1_500_000


# --------------------------------------------------------------------------- collection

def git(repo: Path, *args: str, data: bytes | None = None) -> bytes:
    return subprocess.run(["git", "-C", str(repo), *args], input=data, capture_output=True, check=True).stdout


def candidate_files(repo: Path) -> dict[str, str]:
    """{path: text} for every path the candidate committed, read at the candidate's latest commit touching it."""
    log = git(repo, "log", "--no-merges", "--no-renames", "--format=%x01%H%x00%ae", "--name-only")
    latest: dict[str, str] = {}
    for block in log.decode("utf-8", "replace").split("\x01")[1:]:
        head, *paths = block.strip("\n").split("\n")
        sha, email = head.split("\x00")
        if not CANDIDATE.search(email):
            continue
        for p in (p.strip() for p in paths):
            if p and p not in latest and not SKIP.search(p) and TEXT_EXT.search(p):
                latest[p] = sha
    if not latest:
        return {}
    out = git(repo, "cat-file", "--batch", data="".join(f"{sha}:{p}\n" for p, sha in latest.items()).encode())
    files, pos = {}, 0
    for p in latest:
        nl = out.index(b"\n", pos)
        header = out[pos:nl].split()
        pos = nl + 1
        if header[-1] == b"missing":  # the candidate's latest commit on this path deleted it
            continue
        size = int(header[2])
        if size <= MAX_BYTES:
            files[p] = out[pos:pos + size].decode("utf-8", "replace")
        pos += size + 1
    return files


def collect(work_root: Path, clones: Path | None) -> dict[str, dict[str, str]]:
    projects = {}
    for name, _, work, clone in PROJECTS:
        files: dict[str, str] = {}
        sources = []
        for root, sub in ((clones, clone), (work_root, work)):
            if root is None or sub is None or not (root / sub / ".git").exists():
                continue
            sources.append(str(root / sub))
            for p, body in candidate_files(root / sub).items():
                if p not in files:
                    files[p] = body
                elif files[p] != body:  # same path, different candidate version in the other copy: keep both
                    files[f"{sub}::{p}"] = body
        if not sources:
            sys.exit(f"build_stack: no source found for {name}; leaving {OUT.name} untouched")
        print(f"{name}: {len(files)} candidate-authored files from {', '.join(sources)}", file=sys.stderr)
        projects[name] = files
    return projects


# --------------------------------------------------------------------------- per-file facts

def npm_deps(path: str, body: str) -> set[str]:
    if not path.endswith("package.json"):
        return set()
    try:
        data = json.loads(body)
    except ValueError:
        return set()
    deps = set()
    for key in ("dependencies", "devDependencies", "optionalDependencies"):
        deps |= {d.lower() for d in (data.get(key) or {})}
    return deps


DEP_NAME = re.compile(r"^\s*([A-Za-z0-9_.\-]+)")


def py_deps(path: str, body: str) -> set[str]:
    lines: list[str] = []
    if re.search(r"(^|/)requirements[^/]*\.txt$", path):
        lines = [l for l in body.splitlines() if l.strip() and not l.lstrip().startswith(("#", "-"))]
    elif path.endswith("pyproject.toml"):
        try:
            proj = tomllib.loads(body).get("project", {})
        except tomllib.TOMLDecodeError:
            return set()
        lines = list(proj.get("dependencies", []))
        for extra in proj.get("optional-dependencies", {}).values():
            lines += extra
    deps = set()
    for line in lines:
        m = DEP_NAME.match(line)
        if m:
            deps.add(m.group(1).lower().replace("_", "-"))
    return deps


PY_IMPORT = re.compile(r"^\s*(?:from\s+([A-Za-z_]\w*)[\w.]*\s+import\b|import\s+([A-Za-z_]\w*))", re.M)
JS_IMPORT = re.compile(r"""(?:require\(\s*|\bfrom\s+|^\s*import\s+)['"]([^'"./$][^'"]*)['"]""", re.M)


def py_imports(path: str, body: str) -> set[str]:
    return {(a or b).lower() for a, b in PY_IMPORT.findall(body)} if path.endswith(".py") else set()


def js_imports(path: str, body: str) -> set[str]:
    if not re.search(r"\.(js|jsx|mjs|cjs|ts|tsx)$", path):
        return set()
    mods = set()
    for m in JS_IMPORT.findall(body):
        parts = m.split("/")
        mods.add("/".join(parts[:2]) if m.startswith("@") else parts[0])
    return mods


def ext_of(path: str) -> str:
    name = path.rsplit("/", 1)[-1]
    return name.rsplit(".", 1)[-1].lower() if "." in name else ""


class Project:
    def __init__(self, files: dict[str, str]) -> None:
        self.files = {}
        for key, body in files.items():
            self.files[key] = (key.split("::")[-1], body)

    def match(self, kind: str, pattern: str, minimum: int = 0) -> str | None:
        """Return evidence (a file path, or a line count) when the rule fires, else None."""
        rx = re.compile(pattern if kind in ("code", "path") else rf"(?:{pattern})", re.I)
        if kind == "lines":
            total, where = 0, None
            for path, body in self.files.values():
                if rx.fullmatch(ext_of(path)) and not TOOL_CONFIG.search(path):
                    n = sum(1 for line in body.splitlines() if line.strip())
                    total += n
                    where = where or path
            return f"{total} lines, e.g. {where}" if total >= minimum else None
        for path, body in sorted(self.files.values()):
            if kind == "path" and rx.search(path):
                return path
            if kind == "code" and CODE_EXT.search(path) and rx.search(body):
                return path
            names = {"npm": npm_deps, "py": py_deps, "pyimp": py_imports, "jsimp": js_imports}.get(kind)
            if names and any(rx.fullmatch(n) for n in names(path, body)):
                return path
        return None


MANIFEST = ("npm", "py")


def derive(projects: dict[str, dict[str, str]]) -> list[tuple[str, list[tuple[str, list[str | None]]]]]:
    scanned = {name: Project(files) for name, files in projects.items()}
    matrix = []
    for group, rows in RULES:
        out_rows = []
        for label, rules in rows:
            cells = []
            for name, *_ in PROJECTS:
                used = declared = None
                for rule in rules:
                    hit = scanned[name].match(*rule)
                    if not hit:
                        continue
                    if rule[0] in MANIFEST:
                        declared = declared or f"{rule[0]}: {hit}"
                    else:
                        used = used or f"{rule[0]}: {hit}"
                # Declared-but-never-used dependencies do not earn a dot
                cells.append(f"{used}" + (f"  (declared in {declared.split(': ', 1)[1]})" if declared else "") if used else None)
                if declared and not used:
                    print(f"  skipped {label} for {name}: {declared} but never used in code", file=sys.stderr)
            out_rows.append((label, cells))
        matrix.append((group, out_rows))
    return matrix


def print_matrix(matrix) -> None:
    names = [p[0] for p in PROJECTS]
    short = [n[:9] for n in names]
    print(" " * 24 + " ".join(f"{s:>9}" for s in short))
    for group, rows in matrix:
        print(f"-- {group}")
        for label, cells in rows:
            print(f"{label:<24}" + " ".join(f"{'●' if c else '·':>9}" for c in cells))
    print("\nEvidence (first file that fired each rule):")
    for group, rows in matrix:
        for label, cells in rows:
            for name, ev in zip(names, cells):
                if ev:
                    print(f"  {label:<22} {name:<16} {ev}")


def dump(projects: dict[str, dict[str, str]]) -> None:
    for name, files in projects.items():
        npm, py, pyimp, jsimp = set(), set(), set(), set()
        for key, body in files.items():
            npm |= npm_deps(key, body)
            py |= py_deps(key, body)
            pyimp |= py_imports(key, body)
            jsimp |= js_imports(key, body)
        print(f"\n## {name}")
        for tag, vals in (("npm", npm), ("py", py), ("pyimp", pyimp), ("jsimp", jsimp)):
            print(f"  {tag:<6}:", " ".join(sorted(vals)))


# --------------------------------------------------------------------------- SVG

W = 900
L, R = 32, 868
COL_L = 222                      # first project column's left edge
CW = (R - COL_L) / len(PROJECTS)  # column width
HEAD_Y = 88                      # top of the column header block
GRID_Y = 140                     # first group header
GROUP_H, ROW_H = 25, 18
SWEEP_S, SWEEP_STEP, SWEEP_START = 8.0, 0.8, 1.6


def col_x(i: int) -> float:
    return COL_L + CW * (i + 0.5)


def render(matrix) -> str:
    n_rows = sum(len(rows) for _, rows in matrix)
    grid_end = GRID_Y + GROUP_H * len(matrix) + ROW_H * n_rows
    counts = [sum(1 for _, rows in matrix for _, cells in rows if cells[i]) for i in range(len(PROJECTS))]
    H = int(grid_end + 74)

    css = [
        f".d{{transform-box:fill-box;transform-origin:center;animation:pop .55s cubic-bezier(.3,1.7,.5,1) both}}",
        "@keyframes pop{from{transform:scale(.55);opacity:.8}to{transform:scale(1);opacity:1}}",
        # One column window inside an 8 s loop: fade in, hold, fade out, rest. Each column is delayed a step.
        f".band,.ring{{opacity:0;animation:win {SWEEP_S}s ease-in-out infinite}}",
        "@keyframes win{0%{opacity:0}4%{opacity:1}11%{opacity:1}16%{opacity:0}100%{opacity:0}}",
        f".hn{{animation:hn {SWEEP_S}s ease-in-out infinite}}",
        f"@keyframes hn{{0%{{fill:{TEXT}}}4%{{fill:{AMBER}}}11%{{fill:{AMBER}}}16%{{fill:{TEXT}}}100%{{fill:{TEXT}}}}}",
        f".hc{{animation:hc {SWEEP_S}s ease-in-out infinite}}",
        f"@keyframes hc{{0%{{fill:{MUTED}}}4%{{fill:{TEAL}}}11%{{fill:{TEAL}}}16%{{fill:{MUTED}}}100%{{fill:{MUTED}}}}}",
        "@media (prefers-reduced-motion: reduce){*{animation:none !important}.band,.ring{opacity:0}}",
    ]

    def sweep_delay(i: int) -> str:
        return f"animation-delay:{SWEEP_START + i * SWEEP_STEP:.2f}s"

    body = [f'<rect x="0.5" y="0.5" width="899" height="{H - 1}" rx="16" fill="{SURFACE}" stroke="{BORDER}"/>']
    body.append(f'<text x="{L}" y="40" font-family="{MONO}" font-size="12" letter-spacing="3" fill="{AMBER}">STACK // BY PROJECT</text>')
    body.append(f'<text x="{L}" y="66" font-family="{SANS}" font-size="20" font-weight="700" fill="{TEXT}">What each project is actually built with</text>')
    # Legend, top right
    body.append(
        f'<circle cx="{R - 196}" cy="36" r="5" fill="{TEAL}"/>'
        f'<text x="{R - 186}" y="40" font-family="{SANS}" font-size="12" fill="{MUTED}">used in my code</text>'
        f'<circle cx="{R - 84}" cy="36" r="1.8" fill="{FAINT}"/>'
        f'<text x="{R - 76}" y="40" font-family="{SANS}" font-size="12" fill="{MUTED}">not used</text>'
    )

    # Column sweep bands (behind everything else in the grid)
    for i in range(len(PROJECTS)):
        x = COL_L + CW * i + 3
        body.append(
            f'<rect class="band" style="{sweep_delay(i)}" x="{x:.1f}" y="{HEAD_Y}" width="{CW - 6:.1f}" '
            f'height="{grid_end + 34 - HEAD_Y}" rx="10" fill="{TEAL}" fill-opacity="0.07" stroke="{TEAL}" stroke-opacity="0.35"/>'
        )

    # Column headers
    for i, (name, role, *_) in enumerate(PROJECTS):
        cx = col_x(i)
        # "OpenEnv planner" is too wide for one column: the second word moves to the role line
        first, second = name.split(" ", 1) if name == "OpenEnv planner" else (name, None)
        label = escape(first)
        body.append(
            f'<text class="hn" style="{sweep_delay(i)}" x="{cx:.1f}" y="{HEAD_Y + 22}" text-anchor="middle" font-family="{SANS}" '
            f'font-size="13" font-weight="700" fill="{TEXT}">{label}</text>'
        )
        sub = f"{second} · RL" if second else role
        body.append(
            f'<text x="{cx:.1f}" y="{HEAD_Y + 39}" text-anchor="middle" font-family="{SANS}" font-size="11" fill="{MUTED}">{escape(sub)}</text>'
        )

    # Groups and rows
    y = GRID_Y
    r_index = 0
    for group, rows in matrix:
        body.append(
            f'<text x="{L}" y="{y + 17}" font-family="{MONO}" font-size="11" font-weight="700" letter-spacing="2" fill="{AMBER}">{escape(group.upper())}</text>'
            f'<line x1="{L + 12 + len(group) * 8.6:.0f}" y1="{y + 13}" x2="{R}" y2="{y + 13}" stroke="{BORDER}" stroke-width="1"/>'
        )
        y += GROUP_H
        for k, (label, cells) in enumerate(rows):
            cy = y + ROW_H / 2
            if k % 2 == 0:
                body.append(f'<rect x="{L - 8}" y="{y}" width="{R - L + 16}" height="{ROW_H}" rx="5" fill="{PANEL}" fill-opacity="0.55"/>')
            body.append(f'<text x="{L}" y="{cy + 4.5:.1f}" font-family="{SANS}" font-size="13" fill="{TEXT}">{escape(label)}</text>')
            for i, ev in enumerate(cells):
                cx = col_x(i)
                if ev:
                    delay = 0.15 + i * 0.09 + r_index * 0.012
                    body.append(
                        f'<circle class="ring" style="{sweep_delay(i)}" cx="{cx:.1f}" cy="{cy:.1f}" r="8.5" fill="none" stroke="{TEAL}" stroke-opacity="0.55" stroke-width="1.5"/>'
                        f'<circle class="d" style="animation-delay:{delay:.2f}s" cx="{cx:.1f}" cy="{cy:.1f}" r="5.2" fill="{TEAL}"/>'
                    )
                else:
                    body.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="1.6" fill="{FAINT}"/>')
            y += ROW_H
            r_index += 1

    # Per-project totals
    ty = grid_end + 22
    body.append(f'<line x1="{L}" y1="{grid_end + 6}" x2="{R}" y2="{grid_end + 6}" stroke="{BORDER}" stroke-width="1"/>')
    body.append(f'<text x="{L}" y="{ty}" font-family="{SANS}" font-size="12" fill="{MUTED}">technologies per project</text>')
    for i, n in enumerate(counts):
        body.append(
            f'<text class="hc" style="{sweep_delay(i)}" x="{col_x(i):.1f}" y="{ty}" text-anchor="middle" font-family="{MONO}" '
            f'font-size="13" font-weight="700" fill="{MUTED}">{n}</text>'
        )
    body.append(
        f'<text x="{L}" y="{H - 18}" font-family="{MONO}" font-size="11" fill="{MUTED}">'
        f"derived from each repo's manifests and imports · only files I committed · scripts/build_stack.py</text>"
    )

    used = []
    for group, rows in matrix:
        for label, cells in rows:
            who = [PROJECTS[i][0] for i, c in enumerate(cells) if c]
            if who:
                used.append(f"{label}: {', '.join(who)}")
    desc = (
        "Technology by project matrix, derived from each repository's manifests and imports, counting only files "
        "the author committed. " + "; ".join(used) + "."
    )
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="100%" role="img" aria-labelledby="t d">\n'
        f'<title id="t">Stack by project: what each project is actually built with</title>\n'
        f'<desc id="d">{escape(desc)}</desc>\n'
        f"<style>{''.join(css)}</style>\n" + "\n".join(body) + "\n</svg>\n"
    )


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--work-root", type=Path, default=Path(__file__).resolve().parents[2],
                    help="where the working copies live (default: the folder holding this repo)")
    ap.add_argument("--clones", type=Path, default=None, help="where the full-history clones live")
    ap.add_argument("--dump", action="store_true", help="print raw dependencies and imports, write nothing")
    args = ap.parse_args()
    projects = collect(args.work_root, args.clones)
    if args.dump:
        dump(projects)
        return
    matrix = derive(projects)
    print_matrix(matrix)
    OUT.write_text(render(matrix))
    print(f"\nwrote {OUT} ({OUT.stat().st_size / 1024:.1f} KB)", file=sys.stderr)


if __name__ == "__main__":
    main()
