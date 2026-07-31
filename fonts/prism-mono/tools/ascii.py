"""ascii.py - render glyphs as ASCII art for design inspection.

Usage:  .venv/bin/python tools/ascii.py [size] [text]
"""

import os
import sys

from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.join(os.path.dirname(__file__), "..")
TTF = os.path.join(ROOT, "build", "PrismMono-Regular.ttf")

RAMP = " .:-=+*#%@"


def ink_bbox(img):
    px = img.load()
    w, h = img.size
    xs, ys = [], []
    for y in range(h):
        for x in range(w):
            if px[x, y] < 128:
                xs.append(x)
                ys.append(y)
    return (min(xs), min(ys), max(xs), max(ys)) if xs else (0, 0, 0, 0)


def ascii_render(font_path, text, size=96, pad=12):
    font = ImageFont.truetype(font_path, size)
    img = Image.new("L", (size * len(text) + 4 * pad, int(size * 2.6)), 255)
    d = ImageDraw.Draw(img)
    d.text((pad, int(size * 1.4)), text, font=font, fill=0)

    x0, y0, x1, y1 = ink_bbox(img)
    img = img.crop((max(0, x0 - pad), max(0, y0 - pad),
                    min(img.width, x1 + pad), min(img.height, y1 + pad)))

    cell_w = cell_h = 2 if size >= 96 else 1  # fine cells for small sizes
    if size < 48:
        cell_w = cell_h = 1
    cols = (img.width + cell_w - 1) // cell_w
    rows = (img.height + cell_h - 1) // cell_h
    small = img.resize((cols, rows), Image.LANCZOS)
    px = small.load()
    out = []
    for r in range(rows):
        line = ""
        for c in range(cols):
            v = px[c, r]
            line += RAMP[(255 - v) * (len(RAMP) - 1) // 255]
        out.append(line.rstrip())
    print("\n".join(out))


def main():
    args = sys.argv[1:]
    size = int(args[0]) if args else 96
    text = args[1] if len(args) > 1 else "o0@"
    ascii_render(TTF, text, size)


if __name__ == "__main__":
    main()
