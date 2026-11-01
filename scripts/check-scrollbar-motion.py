#!/usr/bin/env python3
"""Verify stationary panel artwork during uninterrupted native scrolling.

Uses an isolated agent-browser fixture, not the user's Obsidian instance.
White/red paint probes preserve production SVG geometry, alpha and end fades.
"""
import importlib.util
import json
import math
import re
import sys
import urllib.parse
from pathlib import Path

from PIL import ImageChops

ROOT = Path(__file__).resolve().parents[1]
# Loading standalone check helpers must not leave cache files in the repository.
sys.dont_write_bytecode = True


def load_module(name, filename):
    spec = importlib.util.spec_from_file_location(name, ROOT / 'scripts' / filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


panels = load_module('scrollbar_panels', 'check-scrollbar-panels.py')
art = load_module('scrollbar_art', 'check-scrollbar-art.py')
panels.SESSION = 'oboro-scrollbar-motion'


def main():
    panels.browser('--args', '--no-sandbox', 'open', (ROOT / 'scripts/fixtures/scrollbar-panels.html').as_uri())
    cases = [
        dict(mode='light', phone=False, tablet=False, width=1440, cols=4, height=494, horizontal=True, safe=0, keyboard=0),
        dict(mode='dark', phone=False, tablet=False, width=1440, cols=4, height=494, horizontal=True, safe=0, keyboard=0),
        dict(mode='light', phone=False, tablet=True, width=834, cols=2, height=270, horizontal=True, safe=34, keyboard=0),
        dict(mode='dark', phone=True, tablet=False, width=390, cols=1, height=270, horizontal=False, safe=34, keyboard=160),
    ]
    source = art.svg_values((ROOT / 'theme.css').read_text(), '--ob-scrollbar-art-image')[0]
    white = re.sub(r'#[0-9A-Fa-f]{6}', '#FFFFFF', source)
    red = re.sub(r'#[0-9A-Fa-f]{6}', '#FF0000', source)
    images = {'--ob-scrollbar-art-image': white, '--ob-scrollbar-active-art-image': red,
              '--ob-scrollbar-active-top-image': art.edge_svg(red, 'top'),
              '--ob-scrollbar-active-bottom-image': art.edge_svg(red, 'bottom')}
    images = {k: 'url("data:image/svg+xml,' + urllib.parse.quote(v, safe="=':, ") + '")'
              for k, v in images.items()}
    count = 0
    for index, case in enumerate(cases):
        panels.browser('set', 'viewport', case['width'], math.ceil(18/case['cols'])*(case['height']+16)+100)
        panels.browser('open', (ROOT / 'scripts/fixtures/scrollbar-panels.html').as_uri())
        setup = panels.SETUP
        for name, value in sorted(case.items(), key=lambda item: -len(item[0])):
            setup = setup.replace(name.upper(), json.dumps(value))
        panels.evaluate(setup)
        panels.evaluate('''(async()=>{
          for(const [k,v] of Object.entries(VALUES))document.body.style.setProperty(k,v);
          const s=document.createElement('style');s.id='motion-check';
          s.textContent='.panel,[data-scroll]{background:#000!important;border-radius:0!important;box-shadow:none!important;backdrop-filter:none!important}';
          document.head.append(s);document.getElementById('reference').disabled=false;
          repaintScrollbars();await new Promise(r=>setTimeout(r,100));return true})()'''.replace('VALUES', json.dumps(images)))
        geometry = panels.evaluate(panels.GEOMETRY)
        reference = panels.screenshot(f'{index}-motion-original')
        panels.evaluate("(async()=>{const s=document.createElement('style');s.id='motion-blank';s.textContent='[data-scroll]::-webkit-scrollbar-track:vertical{background-image:none!important}';document.head.append(s);repaintScrollbars();await new Promise(r=>setTimeout(r,100));return true})()")
        blank = panels.screenshot(f'{index}-motion-blank')
        panels.evaluate("(async()=>{document.getElementById('motion-blank').remove();document.getElementById('reference').disabled=true;repaintScrollbars();await new Promise(r=>setTimeout(r,100));return true})()")
        # No stylesheet changes, overflow toggles, or recreated scrollbars in this loop.
        for fraction in (0, .137, .5, .837, 1, .4, .1, 0):
            panels.evaluate('''(async()=>{for(const e of document.querySelectorAll('[data-scroll]'))e.scrollTop=(e.scrollHeight-e.clientHeight)*F;await new Promise(r=>setTimeout(r,100));return true})()'''.replace('*F', '*' + str(fraction)))
            current = panels.screenshot(f'{index}-motion-{fraction}')
            for g in geometry:
                if g['total'] <= g['h']:
                    continue
                rect = tuple(round(n) for n in (g['x'], g['y'], g['x']+18, g['y']+g['h']))
                silhouette = panels.mask(ImageChops.difference(reference.crop(rect), blank.crop(rect)), 0)
                changes = panels.mask(ImageChops.difference(current.crop(rect), reference.crop(rect)))
                outside = panels.count(ImageChops.subtract(changes, silhouette))
                assert outside == 0, (case, fraction, g['id'], outside, 'highlight art moved outside stationary original')
                count += 1
        print(f"{case['mode']} {case['width']}px: continuous forward/reverse scrolling preserves original artwork silhouette", flush=True)
    print(f'{count} stationary-art checks passed; screenshots: {panels.OUT}', flush=True)


if __name__ == '__main__':
    try:
        main()
    finally:
        panels.browser('close')
