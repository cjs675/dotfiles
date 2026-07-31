"""preview.py - render Prism Mono glyphs/text to PNG for inspection.

Usage:  .venv/bin/python tools/preview.py [size] [text]
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "source"))

from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.join(os.path.dirname(__file__), "..")
TTF = os.path.join(ROOT, "build", "PrismMono-Regular.ttf")


def render_glyphs(font_path, text, size=128, out="preview.png", pad=40):
    font = ImageFont.truetype(font_path, size)
    img = Image.new("RGB", (int(size * len(text)) + 2 * pad, int(size * 2.6)), "white")
    d = ImageDraw.Draw(img)
    d.text((pad, int(size * 1.4)), text, font=font, fill="black")
    img.save(out)
    print("wrote", out)


def main():
    args = sys.argv[1:]
    size = int(args[0]) if args else 128
    text = args[1] if len(args) > 1 else "o0@"
    out = os.path.join(ROOT, "build", f"preview_{size}_{''.join(c if c.isalnum() else '_' for c in text)}.png")
    render_glyphs(TTF, text, size, out)


if __name__ == "__main__":
    main()
