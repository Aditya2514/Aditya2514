#!/usr/bin/env python3
"""Frame the original profile animations without replacing their internals.

Run after the existing data generators. Standard library only; no API requests.
The original assets/ SVGs remain the source of truth.
"""
from pathlib import Path
from html import escape
import re

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "arena"
PANELS = {
    "hero": ("01 / OPERATOR ID", "TYPING PROFILE"),
    "strip": ("PLAYER RECORD", "ACADEMICS + PROJECTS"),
    "terminal": ("02 / COMMAND CONSOLE", "GITHUB ACTIVITY"),
    "pattern": ("03 / THE PLAYBOOK", "MODEL / CODE / PERSON"),
    "card_lexguard": ("PRIMARY / LEXGUARD", "DEMO LOOP"),
    "card_pikina": ("CONTROL / PIKINA", "DEMO LOOP"),
    "card_noesis": ("RECON / NOESIS", "DEMO LOOP"),
    "card_resilion": ("STRATEGY / RESILION", "DEMO LOOP"),
    "lexguard_flow": ("04 / MISSION REPLAY", "ILLUSTRATIVE CONTRACT"),
    "signal": ("05 / MATCH HISTORY", "GITHUB DATA"),
    "rhythm": ("BUILD RHYTHM", "COMMIT TIMES / IST"),
    "journey": ("07 / CAREER CAMPAIGN", "MILESTONES"),
    "contact": ("08 / OPEN COMMS", "LET'S BUILD"),
}

def frame(name, label, status):
    source = (ROOT / "assets" / (name + ".svg")).read_text()
    # Only the display palette changes; source files and animation timings remain intact.
    for old, new in {"#0d1117":"#080a0f", "#161b22":"#10141b", "#30363d":"#293341", "#2dd4bf":"#54cbd5", "#1f2630":"#18202b"}.items():
        source = source.replace(old, new)
    match = re.search(r'viewBox="([^"]+)"', source)
    if not match:
        raise ValueError("Missing viewBox: " + name)
    _, _, sw, sh = map(float, match.group(1).split())
    w, h = int(sw + 24), int(sh + 70)
    small = sw < 600
    # Keep animation elements, IDs, clipping and timing; only colors are remapped.
    nested = re.sub(r'<svg\b[^>]*>',
        f'<svg xmlns="http://www.w3.org/2000/svg" x="12" y="48" width="{sw:g}" height="{sh:g}" viewBox="0 0 {sw:g} {sh:g}" role="img" aria-labelledby="t d">',
        source, count=1)
    right = "" if small else f'<text class="arena-label" x="{w-40}" y="28" text-anchor="end" fill="#8faea5">{escape(status)}</text>'
    bars = "".join(f'<rect x="{w-103+i*8}" y="{h-13-(i%3)*2}" width="4" height="{4+(i%3)*2}" fill="#54cbd5" class="arena-eq" style="animation-delay:-{i*.23}s"/>' for i in range(9))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-labelledby="arena-title">
<title id="arena-title">{escape(label)} — original animated profile panel</title>
<style>
.arena-label{{font:11px Consolas,monospace;letter-spacing:1.5px}}
.arena-border{{animation:arena-run 18s linear infinite}}
.arena-dot{{animation:arena-ping 3s ease-in-out infinite}}
.arena-eq{{transform-box:fill-box;transform-origin:bottom;animation:arena-eq 2.4s ease-in-out infinite}}
@keyframes arena-run{{to{{stroke-dashoffset:-2400}}}}
@keyframes arena-ping{{50%{{opacity:.35}}}}
@keyframes arena-eq{{50%{{transform:scaleY(.35);opacity:.4}}}}
@media(prefers-reduced-motion:reduce){{.arena-border,.arena-dot,.arena-eq{{animation:none!important}}}}
</style>
<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="12" fill="#06080d" stroke="#293341"/>
<rect x="1.5" y="1.5" width="{w-3}" height="{h-3}" rx="12" fill="none" stroke="#ffc247" stroke-width="2" stroke-dasharray="70 1130" class="arena-border"/>
<path d="M16 38H{w-16}" stroke="#293341"/>
<text class="arena-label" x="18" y="27" fill="#ffc247">{escape(label)}</text>
{right}<circle cx="{w-22}" cy="24" r="4" fill="#54cbd5" class="arena-dot"/>
{nested}
<path d="M20 {h-12}h30m6 0h10" stroke="#ffc247" stroke-width="2"/>
{bars}</svg>
'''

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for name, (label, status) in PANELS.items():
        (OUT / (name + ".svg")).write_text(frame(name, label, status))
    print(f"Rebuilt {len(PANELS)} arena panels from the original assets.")

if __name__ == "__main__":
    main()
