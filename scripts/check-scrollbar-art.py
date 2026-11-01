#!/usr/bin/env python3
"""Check paint-only highlighting and its phase-aligned SVG end fades.

Edit assets/scrollbar-art.svg, then run --write to regenerate all palettes/end images.
"""
import argparse
from pathlib import Path
import re
import sys
import urllib.parse
import xml.etree.ElementTree as ET

# Keep standalone checks from leaving bytecode artifacts in the repository.
sys.dont_write_bytecode = True

from scrollbar_art import render_art, replace_art


EDGE_PX = 18
PHASE_PAD_PX = 24


def svg_values(css: str, token: str) -> list[str]:
    pattern = rf'{re.escape(token)}: url\("data:image/svg\+xml,(.*?)"\);'
    return [urllib.parse.unquote(value) for value in re.findall(pattern, css)]


def edge_svg(art: str, side: str) -> str:
    # No outer viewBox: the image viewport follows background-size without stretching
    # the 18x192 pattern. Only the same artwork's alpha changes at the native ends.
    assert art.startswith("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 18 192'>"), 'Unexpected artwork root'
    art = art.replace(
        "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 18 192'>",
        "<svg width='18' height='192' viewBox='0 0 18 192'>",
        1,
    )
    if side == 'top':
        phase = f"style='transform:translateY(calc({PHASE_PAD_PX}px - 100vh))'"
        y = "y='0'"
        alpha = (0, .15625, .5, .84375, 1)
    else:
        phase = f"patternTransform='translate(0,{PHASE_PAD_PX})'"
        y = f"style='y:calc(100% - {EDGE_PX}px)'"
        alpha = (1, .84375, .5, .15625, 0)
    stops = ''.join(
        f"<stop offset='{i / 4:g}' stop-color='white' stop-opacity='{value:g}'/>"
        for i, value in enumerate(alpha)
    )
    return (
        "<svg xmlns='http://www.w3.org/2000/svg' width='18'><defs>"
        f"<pattern id='tile' width='18' height='192' patternUnits='userSpaceOnUse' {phase}>"
        f"{art}</pattern><linearGradient id='fade' x2='0' y2='1'>{stops}</linearGradient>"
        "<mask id='edge' maskContentUnits='objectBoundingBox'>"
        "<rect width='1' height='1' fill='url(#fade)'/></mask></defs>"
        f"<rect width='18' height='{EDGE_PX}' {y} fill='url(#tile)' mask='url(#edge)'/></svg>"
    )


def regenerate(css: str) -> str:
    # Generated helpers are kept next to each source palette, never edited by hand.
    css = re.sub(r'  --ob-scrollbar-active-(?:top|bottom)-image: url\(.*?\);\n', '', css)
    pattern = r'  --ob-scrollbar-active-art-image: url\("data:image/svg\+xml,(.*?)"\);'

    def replace(match: re.Match) -> str:
        art = urllib.parse.unquote(match.group(1))
        lines = [match.group(0)]
        for side in ('top', 'bottom'):
            encoded = urllib.parse.quote(edge_svg(art, side), safe="=':, ")
            lines.append(f'  --ob-scrollbar-active-{side}-image: url("data:image/svg+xml,{encoded}");')
        return '\n'.join(lines)

    return re.sub(pattern, replace, css)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write', action='store_true', help='regenerate all palettes and end images from the SVG master')
    args = parser.parse_args()
    path = Path(__file__).resolve().parents[1] / 'theme.css'
    css = path.read_text()
    if args.write:
        css = regenerate(replace_art(css))
        path.write_text(css)
    assert f'border: {EDGE_PX}px solid transparent;' in css, 'CSS edge width differs from generated images'
    assert css.count(f'18px calc({PHASE_PAD_PX}px +') == 2, 'CSS phase padding differs from generated images'
    originals = svg_values(css, '--ob-scrollbar-art-image')
    highlights = svg_values(css, '--ob-scrollbar-active-art-image')
    assert len(originals) == len(highlights) == 2, 'Both palettes need a matched SVG pair'
    for mode, original, highlight in zip(('light', 'dark'), originals, highlights):
        assert original == render_art(mode, False), f'{mode}: master changed; regenerate with --write'
        assert highlight == render_art(mode, True), f'{mode}: master changed; regenerate with --write'
        for svg in (original, highlight):
            root = ET.fromstring(svg)
            assert root.attrib['viewBox'] == '0 0 18 192', f'{mode}: unexpected tile dimensions'
        # The full-strength artwork preserves every path, transform and original opacity.
        without_colors = lambda svg: re.sub(r'#[0-9A-Fa-f]{6}', '#PAINT', svg)
        assert without_colors(original) == without_colors(highlight), f'{mode}: highlight changed original geometry/alpha'
        assert original != highlight, f'{mode}: missing highlight palette'
        print(f'{mode}: paint-only highlight; original geometry and alpha preserved')
    for side in ('top', 'bottom'):
        edges = svg_values(css, f'--ob-scrollbar-active-{side}-image')
        assert len(edges) == 2, f'{side}: both palettes need an end fade'
        for mode, art, edge in zip(('light', 'dark'), highlights, edges):
            ET.fromstring(edge)
            assert edge == edge_svg(art, side), f'{mode}/{side}: regenerate with --write'
        print(f'{side}: generated fade contains only the phase-aligned original artwork')
    assert '--ob-scrollbar-position-ink' not in css, 'Do not restore the rectangular color wash'
    assert '--ob-scrollbar-position-wash' not in css, 'Do not restore the rectangular color wash'


if __name__ == '__main__':
    main()
