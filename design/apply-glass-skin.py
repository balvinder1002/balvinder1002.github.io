"""Apply the Liquid glass skin to an archify diagram.

Usage (from the repo root):
    python design/apply-glass-skin.py <archify-output.html> how-its-tested.html

Archify has no theming hook, so this inserts design/diagram-glass.css as the last
<style> in <head>, where it overrides archify's colour variables. Run it again after
every archify rebuild. The skinned file no longer matches archify's provenance hash;
keep archify's own output (in .archify/) if you need `archify check` on it.
"""
import sys
from pathlib import Path

SKIN = Path(__file__).with_name("diagram-glass.css")
MARK = '<style id="glass-skin">'


def main(src: str, dst: str) -> None:
    html = Path(src).read_text(encoding="utf-8")
    if MARK in html:
        sys.exit(f"{src} already has the glass skin; pass archify's original output")
    if html.count("</head>") != 1:
        sys.exit("expected exactly one </head>")
    skin = SKIN.read_text(encoding="utf-8")
    html = html.replace("</head>", f"{MARK}\n{skin}\n</style>\n</head>")
    Path(dst).write_text(html, encoding="utf-8", newline="\n")
    print(f"skinned {src} -> {dst}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
