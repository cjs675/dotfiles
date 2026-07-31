"""compare_weight.py - compare 14px ink/counter metrics vs IBM Plex Mono.

Usage:  .venv/bin/python tools/compare_weight.py
"""

import os

from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.join(os.path.dirname(__file__), "..")
PLEX = os.path.join(ROOT, "source", "IBMPlexMono-Regular.ttf")
PRISM = os.path.join(ROOT, "build", "PrismMono-Regular.ttf")


def glyph_stats(font, ch, size=14):
    img = Image.new("L", (size * 2, size * 4), 0)
    d = ImageDraw.Draw(img)
    d.text((size // 2, size), ch, font=font, fill=255)
    px = img.load()
    w, h = img.size
    xs = [x for y in range(h) for x in range(w) if px[x, y] > 127]
    if not xs:
        return None
    x0, x1 = min(xs), max(xs)
    ys = [y for y in range(h) for x in range(w) if px[x, y] > 127]
    y0, y1 = min(ys), max(ys)
    ink = len(xs)
    white = sum(1 for y in range(y0 + 1, y1) for x in range(x0 + 1, x1)
                if px[x, y] <= 127)
    return (ink, x1 - x0 + 1, y1 - y0 + 1, white)


def main():
    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789oae gBPRQ0689x%&$@#*/\\+=<>()[]{},.;:'\"`~!?_-^|".replace(" ", "")
    pr = ImageFont.truetype(PRISM, 14)
    pl = ImageFont.truetype(PLEX, 14)
    print(f"{'ch':>4} {'Plex ink':>9} {'Prism ink':>9} {'ratio':>6} {'Prism hole':>10}")
    for ch in chars:
        gp, gpl = glyph_stats(pr, ch), glyph_stats(pl, ch)
        if not gp or not gpl:
            continue
        inkp, wp, hp, holep = gp
        inkl, wl, hl, holel = gpl
        print(f"{ch:>4} {inkl:>9} {inkp:>9} {inkp / inkl:>6.2f} {holep:>10}")


if __name__ == "__main__":
    main()
