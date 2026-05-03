"""Build assets/profile-header.png for GitHub profile README.

GitHub proxies README images through Camo; SVG in <img> often fails — PNG is reliable.

Run from repo root: python tools/generate_profile_header_png.py
"""

from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "profile-header.png"


def lerp_rgb(
    a: tuple[int, int, int],
    b: tuple[int, int, int],
    t: float,
) -> tuple[int, int, int]:
    return (int(a[0] + (b[0] - a[0]) * t), int(a[1] + (b[1] - a[1]) * t), int(a[2] + (b[2] - a[2]) * t))


def main() -> None:
    w, h = 1200, 300
    img = Image.new("RGB", (w, h))
    pix = img.load()

    c_top = (0x1A, 0x14, 0x12)
    c_mid = (0x0C, 0x0A, 0x09)
    c_bot = (0x12, 0x0E, 0x0C)

    for y in range(h):
        t = y / (h - 1) if h > 1 else 0
        row = lerp_rgb(lerp_rgb(c_top, c_mid, min(1, t * 1.35)), c_bot, max(0, (t - 0.35) / 0.65))
        for x in range(w):
            pix[x, y] = row

    draw = ImageDraw.Draw(img)

    # Very subtle grid (~4% lightness lift on intersections only)
    gcol = (0x21, 0x1E, 0x1D)
    for gx in range(0, w + 1, 40):
        draw.line([(gx, 0), (gx, h)], fill=gcol, width=1)
    for gy in range(0, h + 1, 40):
        draw.line([(0, gy), (w, gy)], fill=gcol, width=1)

    # Accent underline
    accent_a = (0xC9, 0x8C, 0x63)
    accent_b = (0x7C, 0x98, 0x85)
    y_line = h - 32
    for xi, x in enumerate(range(80, w - 80)):
        t = xi / max(w - 160 - 1, 1)
        c = lerp_rgb(accent_a, accent_b, 0.5 + 0.5 * math.sin(t * math.pi))
        draw.line([(x, y_line), (x + 1, y_line + 2)], fill=c)

    def try_font(paths: list[Path], size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
        for p in paths:
            if p.is_file():
                try:
                    return ImageFont.truetype(str(p), size=size)
                except OSError:
                    continue
        return ImageFont.load_default()

    win = Path("C:/Windows/Fonts")
    font_title = try_font([win / "segoeuib.ttf", win / "SegoeUI-Bold.ttf", win / "calibrib.ttf"], 54)
    font_caps = try_font([win / "consola.ttf", win / "cascadiamono.ttf"], 17)
    font_body = try_font([win / "segoeui.ttf", win / "Calibri.ttf"], 16)

    title = "Shahzaib Rehman"
    bbox = draw.textbbox((0, 0), title, font=font_title)
    tw = bbox[2] - bbox[0]
    draw.text((w // 2 - tw // 2, 92), title, fill=(0xF5, 0xF0, 0xE8), font=font_title)

    line2 = "SENIOR SOFTWARE ENGINEER · WEB · PAYMENTS · CLOUD · AI"
    bbox2 = draw.textbbox((0, 0), line2, font=font_caps)
    tw2 = bbox2[2] - bbox2[0]
    draw.text((w // 2 - tw2 // 2, 168), line2, fill=(0xC9, 0x8C, 0x63), font=font_caps)

    line3 = "Efficient systems, clear integrations, details that survive production."
    bbox3 = draw.textbbox((0, 0), line3, font=font_body)
    tw3 = bbox3[2] - bbox3[0]
    draw.text((w // 2 - tw3 // 2, 208), line3, fill=(0xA8, 0xA2, 0x9E), font=font_body)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    img.save(OUT, "PNG", optimize=True)
    print(f"Wrote {OUT}")

    # Footer bar (same PNG rationale as header)
    wf, hf = 1200, 72
    foot = Image.new("RGB", (wf, hf), (0x0C, 0x0A, 0x09))
    fdraw = ImageDraw.Draw(foot)
    for x in range(120, wf - 120):
        t = (x - 120) / max(wf - 240 - 1, 1)
        c = lerp_rgb(
            (0x7C, 0x98, 0x85),
            (0xC9, 0x8C, 0x63),
            0.35 + 0.65 * math.sin(t * math.pi),
        )
        fdraw.line([(x, 36), (x + 1, 37)], fill=c)
    foot_out = ROOT / "assets" / "profile-footer.png"
    foot.save(foot_out, "PNG", optimize=True)
    print(f"Wrote {foot_out}")


if __name__ == "__main__":
    main()
