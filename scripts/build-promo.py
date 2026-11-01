#!/usr/bin/env python3
"""Compose documentation artwork from real captures and the scrollbar SVG master.

Requires Pillow, Fontconfig, Inkscape. Never retouches the captured UI.
Run from any directory: python3 scripts/build-promo.py
"""
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile

from PIL import Image, ImageDraw, ImageFont

sys.dont_write_bytecode = True
from scrollbar_art import render_art

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'screenshots'
META = json.loads((OUT / 'capture.json').read_text())
INK = '#F7E6EF'
MUTED = '#C5A7B8'
ACCENT = '#E6B397'


def font(family, size):
    path = subprocess.check_output(
        ['fc-match', family, '-f', '%{file}'], text=True).strip()
    return ImageFont.truetype(path, size)


def text(canvas, xy, value, size=26, color=INK, family='Noto Sans'):
    ImageDraw.Draw(canvas).text(xy, value, fill=color, font=font(family, size))


def background(size):
    canvas = Image.new('RGB', size)
    draw = ImageDraw.Draw(canvas)
    top, bottom = (35, 24, 37), (50, 34, 49)
    for y in range(size[1]):
        t = y / (size[1] - 1)
        color = tuple(round(a + (b - a) * t) for a, b in zip(top, bottom))
        draw.line((0, y, size[0], y), fill=color)
    return canvas


def framed(canvas, source, xy, width, radius=16):
    image = source.resize((width, round(source.height * width / source.width)),
                          Image.Resampling.LANCZOS)
    mask = Image.new('L', image.size)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, image.width - 1, image.height - 1),
                                          radius=radius, fill=255)
    canvas.paste(image, xy, mask)
    x, y = xy
    ImageDraw.Draw(canvas).rounded_rectangle(
        (x, y, x + image.width - 1, y + image.height - 1),
        radius=radius, outline='#765566', width=1)


def crop(source, name, padding=8):
    rect = META['rects'][name]
    scale = META['viewport']['deviceScaleFactor']
    x, y, w, h = (rect[k] for k in ('x', 'y', 'width', 'height'))
    return source.crop(tuple(round(v * scale) for v in
                       (x - padding, y - padding, x + w + padding, y + h + padding)))


def promo(light, dark):
    canvas = background((2560, 1600))
    draw = ImageDraw.Draw(canvas)
    text(canvas, (96, 48), 'OBSIDIAN THEME  /  SAKURA PINK + NIGHT SAKURA', 23, MUTED)
    text(canvas, (89, 66), 'Oboro', 164, family='EB Garamond')
    text(canvas, (520, 137), '朧樱', 60, MUTED, 'Noto Serif CJK SC')
    text(canvas, (1320, 105), 'A softer frame for a clearer thought.', 48,
         family='EB Garamond:style=Italic')
    text(canvas, (1323, 172), 'Frosted glass. Quiet colour. A hand-drawn sakura branch.', 25, MUTED)
    text(canvas, (96, 262), 'SAKURA PINK  /  LIGHT', 23, '#F0C7D9')
    text(canvas, (1304, 262), 'NIGHT SAKURA  /  DARK', 23, ACCENT)
    framed(canvas, light, (96, 310), 1160)
    framed(canvas, dark, (1304, 310), 1160)
    details = [
        (96, 'GLASS TABLES', 'Defined edges. A transparent centre.', crop(light, 'table')),
        (896, 'TINTED CALLOUTS', 'A little colour, without the solid block.', crop(dark, 'callout')),
        (1696, 'CODE, BUT SOFTER', 'Macaron labels and a seven-segment light band.', crop(dark, 'code')),
    ]
    for x, title, subtitle, image in details:
        text(canvas, (x, 1060), title, 23, ACCENT)
        text(canvas, (x, 1102), subtitle, 23, MUTED)
        framed(canvas, image, (x, 1155), 768, 12)
    draw.line((96, 1497, 2464, 1497), fill='#634655')
    text(canvas, (96, 1520), f"OBORO {META['version']}  /  ACTUAL OBSIDIAN CAPTURES", 21, MUTED)
    text(canvas, (1410, 1520), 'Style Settings · custom wallpaper · reading view', 22, MUTED)
    canvas.save(OUT / 'promo.png', optimize=True)


def scrollbar_detail():
    canvas = background((2000, 1300))
    text(canvas, (80, 45), 'OBORO  /  SCROLLBAR ART STUDY', 22, MUTED)
    text(canvas, (75, 72), 'A branch, not a bar.', 104, family='EB Garamond')
    text(canvas, (82, 214), 'The painting stays still. Your place changes its colour.', 29, MUTED)
    for index, (mode, active) in enumerate(
            [('light', False), ('light', True), ('dark', False), ('dark', True)]):
        x = 80 + index * 470
        panel = '#FFF0F5' if mode == 'light' else '#3C2D3C'
        ink = '#7F405B' if mode == 'light' else '#EBC4D7'
        ImageDraw.Draw(canvas).rounded_rectangle((x, 302, x + 430, 1150),
                                                radius=18, fill=panel)
        text(canvas, (x + 30, 329), mode.upper(), 22, ink)
        text(canvas, (x + 30, 370), 'YOUR PLACE' if active else 'AT REST', 22, ink)
        with tempfile.TemporaryDirectory(prefix='oboro-art-export-') as folder:
            svg, png = Path(folder) / 'branch.svg', Path(folder) / 'branch.png'
            svg.write_text(render_art(mode, active))
            subprocess.run(['inkscape', str(svg), '--export-type=png',
                            f'--export-filename={png}', '--export-width=63',
                            '--export-height=672'], check=True, capture_output=True)
            art = Image.open(io.BytesIO(png.read_bytes())).convert('RGBA')
            canvas.paste(art, (x + 183, 445), art)
    text(canvas, (80, 1190), 'One original drawing · four palettes · identical geometry', 25, MUTED)
    text(canvas, (80, 1233), 'SVG artwork enlarged 3.5× for detail; not a screenshot or the actual scrollbar size.', 21, MUTED)
    canvas.save(OUT / 'scrollbar-detail.png', optimize=True)


if __name__ == '__main__':
    with Image.open(OUT / 'screenshot-light.png') as light, Image.open(OUT / 'screenshot-dark.png') as dark:
        expected = tuple(round(META['viewport'][k] * META['viewport']['deviceScaleFactor'])
                         for k in ('width', 'height'))
        assert light.size == dark.size == expected, 'Capture metadata and images must match'
        promo(light, dark)
    scrollbar_detail()
    print('Updated screenshots/promo.png and screenshots/scrollbar-detail.png')
