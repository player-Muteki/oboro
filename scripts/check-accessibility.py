#!/usr/bin/env python3
"""Chromium accessibility regressions (agent-browser + Pillow), no vault changes.

Force high contrast via Chromium's launch flag and assert the media query is active;
use browser media emulation for reduced motion. These are not real OS/device tests.
"""
import json
from pathlib import Path
import subprocess
import tempfile

from PIL import Image, ImageChops

ROOT = Path(__file__).resolve().parents[1]
OUT = Path(tempfile.mkdtemp(prefix='oboro-accessibility-'))


def main():
    failures = []
    checks = 0

    def check(condition, message):
        nonlocal checks
        checks += 1
        if not condition:
            failures.append(message)

    for forced in (False, True):
        session = 'oboro-a11y-forced' if forced else 'oboro-a11y-normal'

        def browser(*args):
            return subprocess.check_output(
                ['agent-browser', '--session', session, *map(str, args)], text=True,
            ).strip()

        def evaluate(js):
            return json.loads(browser('eval', js))

        try:
            flags = '--no-sandbox' + (',--force-high-contrast' if forced else '')
            browser('--args', flags, 'open', (ROOT / 'scripts/fixtures/accessibility.html').as_uri())
            check(evaluate("matchMedia('(forced-colors: active)').matches") == forced,
                  f'{session}: forced-colors emulation')
            for mode in ('light', 'dark'):
                evaluate(f"document.body.className = 'theme-{mode} styled-scrollbars'")
                for target in ('reading', 'legacy', 'editing'):
                    style = evaluate(f"""(() => {{
                        const s = getComputedStyle(document.getElementById('{target}'));
                        return {{fill:s.webkitTextFillColor, color:s.color, bg:s.backgroundImage}};
                    }})()""")
                    if forced:
                        check(style['fill'] == style['color'] and style['bg'] == 'none',
                              f'{mode}/{target}: high-contrast solid text: {style}')
                        # Check actual painted glyphs, not merely computed styles.
                        rect = evaluate(f"""(() => {{const r = document.getElementById('{target}').getBoundingClientRect();
                            return [Math.floor(r.x), Math.floor(r.y), Math.ceil(r.right), Math.ceil(r.bottom)];}})()""")
                        before = OUT / f'{mode}-{target}-visible.png'
                        hidden = OUT / f'{mode}-{target}-hidden.png'
                        browser('screenshot', before)
                        evaluate(f"document.getElementById('{target}').style.visibility='hidden'")
                        browser('screenshot', hidden)
                        evaluate(f"document.getElementById('{target}').style.visibility=''")
                        with Image.open(before) as a, Image.open(hidden) as b:
                            diff = ImageChops.difference(a.convert('RGB').crop(rect), b.convert('RGB').crop(rect))
                            check(diff.getbbox() is not None, f'{mode}/{target}: glyphs actually painted')
                    else:
                        check(style['fill'] == 'rgba(0, 0, 0, 0)' and 'linear-gradient' in style['bg'],
                              f'{mode}/{target}: default gradient preserved')
                for target in ('math', 'code', 'edit-math', 'edit-code'):
                    fill = evaluate(f"getComputedStyle(document.getElementById('{target}')).webkitTextFillColor")
                    check(fill not in ('transparent', 'rgba(0, 0, 0, 0)'), f'{mode}/{target}: visible nested text')
            if not forced:
                check(evaluate("getComputedStyle(document.querySelector('.hover-popover')).animationName") == 'ob-fade-scale',
                      'default preview animation preserved')
            browser('set', 'media', 'light', 'reduced-motion')
            check(evaluate("matchMedia('(prefers-reduced-motion: reduce)').matches"), 'reduced-motion emulation')
            for selector in ('.hover-popover', '.modal', '.menu', '.suggestion-container', '.notice', '#codeblock', '#edit-codeblock'):
                pseudo = ", '::before'" if 'codeblock' in selector else ''
                name = evaluate(f"getComputedStyle(document.querySelector('{selector}'){pseudo}).animationName")
                check(name == 'none', f'{session}/{selector}: reduced-motion animation = {name}')
            if not forced:
                # The scrollbar timeline is functional state, not decorative motion.
                progress = evaluate("""(async () => {
                    const e = document.getElementById('files');
                    const read = () => parseFloat(getComputedStyle(e).getPropertyValue('--ob-scrollbar-progress'));
                    e.scrollTop = 0;
                    await new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r)));
                    const start = read();
                    e.scrollTop = e.scrollHeight;
                    await new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r)));
                    return {start, end:read(), animation:getComputedStyle(e).animationName};
                })()""")
                check(progress['animation'] == 'ob-scrollbar-progress' and
                      abs(progress['start']) < .01 and abs(progress['end'] - 1) < .01,
                      f'reduced-motion scrollbar stays synchronized: {progress}')
        finally:
            browser('close')
    print(f'{checks} checks; artifacts: {OUT}')
    if failures:
        raise SystemExit('\n'.join(failures))
    print('Accessibility regression passed')


if __name__ == '__main__':
    main()
