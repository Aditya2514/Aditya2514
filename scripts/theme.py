"""Shared colours, fonts and text helpers for every generated SVG."""

SURFACE = "#0d1117"
PANEL = "#161b22"
BORDER = "#30363d"
TEXT = "#e6edf3"
MUTED = "#8b949e"
FAINT = "#484f58"
TEAL = "#2dd4bf"
AMBER = "#f5a524"

# Fixed category order for languages, validated for the dark surface (CVD-safe adjacent pairs).
CATEGORICAL = ["#3987e5", "#d95926", "#199e70", "#c98500", "#d55181"]
OTHER = "#6e7681"

SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"


def wrap(text: str, width_px: float, font_px: float) -> list[str]:
    """Greedy word wrap using an average glyph width; SVG has no text layout of its own."""
    max_chars = max(1, int(width_px / (font_px * 0.53)))
    lines, line = [], ""
    for word in text.split():
        candidate = f"{line} {word}".strip()
        if len(candidate) > max_chars and line:
            lines.append(line)
            line = word
        else:
            line = candidate
    if line:
        lines.append(line)
    return lines
