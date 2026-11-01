"""Render the single hand-drawn scrollbar master into four paint-only palettes.

The master is valid SVG in the light selected palette, so it can also be opened
in an image editor. Run check-scrollbar-art.py --write after editing the master.
"""
from pathlib import Path
import re
import urllib.parse
import xml.etree.ElementTree as ET

SOURCE = Path(__file__).resolve().parent / 'assets' / 'scrollbar-art.svg'
# bark body/ridge/midtone, petal throat/wash/rim/outline/vein,
# pollen filament/head, foliage, bark edge/glint. Keep alpha in the master only.
MASTER_COLORS = (
    '#91344F', '#CE8192', '#AB4C68', '#B83264', '#E78CA9', '#FFD6DD',
    '#B84A75', '#9D2D58', '#A77A38', '#F6CF83', '#7C8060', '#68263F', '#EDAFB4',
)
PALETTES = {
    ('light', False): (
        '#A59CAA', '#D7CEDD', '#BDB1C5', '#B4A7BD', '#DDD5E5', '#F4F0F7',
        '#B7A8BF', '#A295AE', '#B6ADA0', '#EDE4D2', '#ADB0A8', '#928A9C', '#E4DEE8',
    ),
    ('light', True): MASTER_COLORS,
    ('dark', False): (
        '#705A6E', '#A48798', '#887085', '#845571', '#AA829C', '#C4ACB8',
        '#986C89', '#774C6C', '#A2835F', '#C0A27B', '#7C806D', '#584557', '#B49BA5',
    ),
    ('dark', True): (
        '#F0BB78', '#FFE6A0', '#FFD28A', '#EE7898', '#FFB3BB', '#FFF3DE',
        '#FF98B0', '#E7839E', '#F9D17C', '#FFF0B2', '#D7CD8E', '#E1A467', '#FFE9BB',
    ),
}


def render_art(mode: str, active: bool) -> str:
    source = SOURCE.read_text()
    ET.fromstring(source)
    colors = dict(zip(MASTER_COLORS, PALETTES[mode, active], strict=True))
    assert set(re.findall(r'#[0-9A-Fa-f]{6}', source)) == set(colors), 'Unknown/missing master pigments'
    source = re.sub(r'<!--[\s\S]*?-->', '', source)
    source = re.sub(r'>\s+<', '><', source).strip()
    return re.sub(r'#[0-9A-Fa-f]{6}', lambda match: colors[match[0]], source)


def replace_art(css: str) -> str:
    for active in (False, True):
        token = '--ob-scrollbar-active-art-image' if active else '--ob-scrollbar-art-image'
        modes = iter(('light', 'dark'))

        def replace(match):
            art = render_art(next(modes), active)
            encoded = urllib.parse.quote(art, safe="=':, ")
            return f'{token}: url("data:image/svg+xml,{encoded}");'

        css, count = re.subn(re.escape(token) + r': url\("data:image/svg\+xml,.*?"\);', replace, css)
        assert count == 2, f'{token}: expected exactly two palettes'
    return css
