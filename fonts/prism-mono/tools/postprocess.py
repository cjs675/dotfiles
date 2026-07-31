"""postprocess.py - final metric fixes on the Nerd Font patched TTF.

The font-patcher normalizes OS/2 vertical metrics and forces every glyph to a
single advance width (--mono). Restore the designed multi-cell advances of the
ligature glyphs (so ->, =>, === compose without overlapping neighbours) and set
safe Windows metrics so tall glyphs (yMax 1119 / yMin -350) never clip.
"""

import os

from fontTools.ttLib import TTFont

ROOT = os.path.join(os.path.dirname(__file__), "..")
TTF = os.path.join(ROOT, "build", "PrismMonoNerdFontMono-Regular.ttf")

LIG_WIDTHS = {
    "arrowRight": 1200,
    "arrowLeft": 1200,
    "arrowDouble": 1200,
    "arrowDoubleRight": 1800,
    "lessEqual": 1200,
    "greaterEqual": 1200,
    "equalEqual": 1200,
    "equalEqualEqual": 1800,
    "notEqual": 1200,
    "notEqualEqual": 1800,
    "spaceship": 1800,
}


def main():
    f = TTFont(TTF)
    hmtx = f["hmtx"]
    for name, width in LIG_WIDTHS.items():
        if name in hmtx.metrics:
            hmtx[name] = (width, hmtx[name][1])
    os2 = f["OS/2"]
    os2.usWinAscent = 1119
    os2.usWinDescent = 350
    f.save(TTF)
    print("wrote", TTF)
    for name in LIG_WIDTHS:
        print(" ", name, hmtx[name][0])


if __name__ == "__main__":
    main()
