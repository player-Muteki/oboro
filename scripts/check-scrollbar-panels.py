#!/usr/bin/env python3
"""Browser regression for panel scrollbars (agent-browser + Python Pillow).

Runs in an isolated browser session, without opening or changing an Obsidian vault.
Screenshots and reports are written to a temporary directory, not the repository.
"""
import json
import math
from pathlib import Path
import shutil
import subprocess
import tempfile

from PIL import Image, ImageChops


ROOT = Path(__file__).resolve().parents[1]
SESSION = 'oboro-panel-regression'
OUT = Path(tempfile.mkdtemp(prefix='oboro-panel-scrollbars-'))


def browser(*args):
    return subprocess.check_output(
        ['agent-browser', '--session', SESSION, *map(str, args)], text=True,
    ).strip()


def evaluate(code):
    return json.loads(browser('eval', code))


def screenshot(name):
    path = OUT / f'{name}.png'
    browser('screenshot', path)
    return Image.open(path).convert('RGB')


def mask(image, threshold=2):
    r, g, b = image.split()
    return ImageChops.lighter(ImageChops.lighter(r, g), b).point(
        lambda n: 255 if n > threshold else 0,
    )


def count(image):
    return image.width * image.height - image.histogram()[0]


# Explicit scrollports only; no wildcard leaf-content/view-content behavior.
SETUP = r"""
(async () => {
 document.body.className = 'styled-scrollbars theme-' + MODE +
   (PHONE ? ' is-mobile is-phone' : (TABLET ? ' is-mobile is-tablet' : ''));
 document.body.style.setProperty('--safe-area-inset-bottom', SAFE + 'px');
 document.body.style.setProperty('--keyboard-height', KEYBOARD + 'px');
 document.body.style.setProperty('--test-height', HEIGHT + 'px');
 document.getElementById('panels').style.gridTemplateColumns = 'repeat(' + COLS + ',260px)';
 if (PHONE || TABLET) document.getElementById('files').closest('.panel').classList.add('workspace-drawer-active-tab-content');
 if (PHONE) {
  for (const e of document.querySelectorAll('.modal.mod-settings')) e.classList.add('mod-sidebar-layout');
  for (const e of document.querySelectorAll('.vertical-tab-header')) {
   e.dataset.scroll = ''; e.id ||= 'phone-search-header';
  }
  // The children are auto-height on phones, and must not get size containment.
  for (const id of ['settings-list','settings-search']) document.getElementById(id).removeAttribute('data-scroll');
 }
 if (HORIZONTAL) for (const e of document.querySelectorAll('[data-scroll]')) {
  if (e.id === 'short' || e.matches('.vertical-tab-header')) continue;
  const wide = document.createElement('div');wide.className='wide';e.append(wide);
 }
 // Chromium caches native pseudo-element painting when a stylesheet is toggled.
 // Recreate only fixture scrollbars (never user views), preserving native offsets.
 window.repaintScrollbars = () => {
  for (const e of document.querySelectorAll('[data-scroll]')) {
   const css=e.style.cssText, top=e.scrollTop, left=e.scrollLeft;
   e.style.setProperty('overflow','hidden','important');void e.offsetHeight;
   e.style.cssText=css;e.scrollTop=top;e.scrollLeft=left;
  }
 };
 const probe = document.createElement('style');probe.id='probe';
 probe.textContent = '[data-scroll]::-webkit-scrollbar-thumb {outline:solid transparent;outline-width:round(nearest,calc(100cqh + var(--ob-scrollbar-block-inset)),1px)}';
 document.head.append(probe);
 const reference = document.createElement('style');reference.id='reference';
 reference.textContent = '[data-scroll]::-webkit-scrollbar-thumb:vertical,[data-scroll]::-webkit-scrollbar-thumb:vertical:hover,[data-scroll]::-webkit-scrollbar-thumb:vertical:active{background-image:none!important;background-color:transparent!important;}';
 document.head.append(reference);reference.disabled=true;
 const noContain = document.createElement('style');noContain.id='no-contain';
 noContain.textContent = '[data-scroll]{container-type:normal!important}';
 document.head.append(noContain);noContain.disabled=true;
 await new Promise(r=>setTimeout(r,100));
 return true;
})()
"""

GEOMETRY = r"""
[...document.querySelectorAll('[data-scroll]')].map(e=>{
 const r=e.getBoundingClientRect(), c=getComputedStyle(e), s=getComputedStyle(e,'::-webkit-scrollbar-thumb');
 return {id:e.id,x:r.right-18,y:r.top,outerH:r.height,outerW:r.width,h:e.clientHeight,
   total:e.scrollHeight,top:e.scrollTop,w:e.clientWidth,scrollW:e.scrollWidth,
   container:c.containerType,padding:parseFloat(c.paddingTop)+parseFloat(c.paddingBottom),
   probe:parseFloat(s.outlineWidth),progress:parseFloat(c.getPropertyValue('--ob-scrollbar-progress'))||0};
})
"""


def main():
    assert shutil.which('agent-browser'), 'Install agent-browser before running this check'
    browser('--args', '--no-sandbox', 'open', (ROOT / 'scripts/fixtures/scrollbar-panels.html').as_uri())
    reports = []
    cases = [
        # Both palettes, fractional viewport heights, horizontal overflow and mobile safe area/keyboard.
        dict(mode='light', phone=False, tablet=False, width=1440, cols=4, height=370.375, horizontal=False, safe=0, keyboard=0),
        dict(mode='dark', phone=False, tablet=False, width=1440, cols=4, height=493.7375, horizontal=True, safe=0, keyboard=0),
        dict(mode='light', phone=False, tablet=True, width=834, cols=2, height=270.375, horizontal=True, safe=34, keyboard=0),
        dict(mode='dark', phone=True, tablet=False, width=390, cols=1, height=270.375, horizontal=False, safe=34, keyboard=160),
    ]
    for index, case in enumerate(cases):
        browser('set', 'viewport', case['width'], math.ceil(18/case['cols'])*(math.ceil(case['height'])+16)+100)
        browser('open', (ROOT / 'scripts/fixtures/scrollbar-panels.html').as_uri())
        setup = SETUP
        for name, value in sorted(case.items(), key=lambda item: -len(item[0])):
            setup = setup.replace(name.upper(), json.dumps(value))
        evaluate(setup)
        actual = evaluate(GEOMETRY)
        evaluate("document.getElementById('no-contain').disabled=false")
        baseline = evaluate(GEOMETRY)
        evaluate("document.getElementById('no-contain').disabled=true")
        assert len(actual) == len(baseline)
        for a, b in zip(actual, baseline):
            for key in ('outerH', 'outerW', 'h', 'total'):
                assert a[key] == b[key], (case, a['id'], key, a[key], b[key], 'containment changed native layout')
            # Both wrapper and self size containers include the horizontal gutter; subtract it once.
            is_note = a['id'].startswith('docked-')
            gutter = round(a['outerH']) - a['h']
            assert a['probe'] - gutter == a['h'], (case, a, 'viewport compensation mismatch')
            if not is_note:
                assert a['container'] == 'size scroll-state', (case, a, 'missing self size/scroll-state')
            assert a['outerW'] - a['w'] == (0 if a['id'] == 'short' else 18), (case, a, 'native vertical width changed')
        unaffected = evaluate("['embedded-query','code-scroll','embedded-backlinks'].map(id=>{let e=document.getElementById(id);return {id,container:getComputedStyle(e).containerType,w:e.offsetWidth-e.clientWidth}})")
        for e in unaffected:
            assert e['container'] == 'normal', (case, e, 'embedded content was size-contained')
            assert e['w'] in (0,12), (case, e, 'embedded scrollbar was restyled')
        if case['phone']:
            for value in evaluate("['settings-list','settings-search'].map(id=>getComputedStyle(document.getElementById(id)).containerType)"):
                assert value == 'normal', ('phone settings child collapsed', value)
        # Each panel has its own progress, even when all panels are visible simultaneously.
        reference_at_start = None
        for fraction in (0, .137, .5, .837, 1):
            geometry = evaluate('''(async()=>{for(const e of document.querySelectorAll('[data-scroll]'))e.scrollTop=(e.scrollHeight-e.clientHeight)*F;await new Promise(r=>setTimeout(r,100));return G})()'''.replace('*F', '*'+str(fraction)).replace('return G', 'return ('+GEOMETRY+')'))
            new = screenshot(f'{index}-{fraction}-active')
            evaluate("(async()=>{document.getElementById('reference').disabled=false;repaintScrollbars();await new Promise(r=>setTimeout(r,100));return true})()")
            reference = screenshot(f'{index}-{fraction}-track')
            evaluate("(async()=>{document.getElementById('reference').disabled=true;repaintScrollbars();await new Promise(r=>setTimeout(r,100));return true})()")
            if fraction == 0:
                reference_at_start = reference
            for g in geometry:
                rect = tuple(round(n) for n in (g['x'], g['y'], g['x']+18, g['y']+g['h']))
                # Native track must stay stationary while content and thumb move.
                assert ImageChops.difference(reference_at_start.crop(rect), reference.crop(rect)).getbbox() is None, (case, fraction, g['id'], 'track moved')
                changes = mask(ImageChops.difference(new.crop(rect), reference.crop(rect)))
                if g['total'] <= g['h']:
                    assert changes.getbbox() is None, (case, g, 'short content got a fake thumb')
                    continue
                assert abs(g['progress'] - g['top']/(g['total']-g['h'])) < .00001, (case, g, 'shared progress leaked')
                thumb_height = max(64, math.floor(g['h']*g['h']/g['total']))
                thumb_top = math.floor(g['progress']*(g['h']-thumb_height))
                bounds = changes.getbbox()
                assert bounds is not None and count(changes) > 12, (case, fraction, g, 'missing visible art highlight')
                assert bounds[1] >= thumb_top-1 and bounds[3] <= thumb_top+thumb_height+1, (case, fraction, g, bounds, thumb_top, thumb_height, 'highlight outside native thumb')
                # No opaque strip: the selected area must still contain transparent gaps.
                area=changes.crop((0,thumb_top,18,min(g['h'],thumb_top+thumb_height)))
                assert count(area) < area.width*area.height*.75, (case, fraction, g['id'], 'rectangular wash')
                reports.append(dict(case=index,fraction=fraction,id=g['id'],pixels=count(changes)))
        # Verify progress isolation by scrolling just one panel after resetting the others.
        isolated = evaluate("(async()=>{for(const e of document.querySelectorAll('[data-scroll]'))e.scrollTop=0;let f=document.getElementById('files');f.scrollTop=(f.scrollHeight-f.clientHeight)*.73;await new Promise(r=>setTimeout(r,100));return [...document.querySelectorAll('[data-scroll]')].map(e=>({id:e.id,p:parseFloat(getComputedStyle(e).getPropertyValue('--ob-scrollbar-progress'))||0}))})()")
        assert .72 < isolated[0]['p'] < .74
        assert all(e['p'] == 0 for e in isolated[1:]), ('panels inherited each other progress', isolated)
        # Exercise the real native thumb and keyboard in this isolated fixture.
        drag = evaluate("(async()=>{const e=document.getElementById('files');e.scrollTop=(e.scrollHeight-e.clientHeight)/2;await new Promise(r=>setTimeout(r,100));const b=e.getBoundingClientRect(),h=Math.max(64,Math.floor(e.clientHeight*e.clientHeight/e.scrollHeight));return {x:Math.round(b.right-9),y:Math.round(b.top+(e.clientHeight-h)*e.scrollTop/(e.scrollHeight-e.clientHeight)+h/2),top:e.scrollTop}})()")
        browser('mouse','move',drag['x'],drag['y'])
        browser('mouse','down')
        try:
            browser('mouse','move',drag['x'],drag['y']+30)
        finally:
            browser('mouse','up')
        assert evaluate("document.getElementById('files').scrollTop") > drag['top'], (case, 'native drag failed')
        evaluate("(()=>{const e=document.getElementById('files');e.tabIndex=0;e.focus();e.scrollTop=0;return true})()")
        browser('press','PageDown')
        browser('wait','--fn',"document.getElementById('files').scrollTop > 0")
        print(f"case {index}: {case['mode']}, {case['width']}px, phone={case['phone']}; native layout/phase/progress/drag/keyboard passed")
    (OUT / 'report.json').write_text(json.dumps(reports,indent=2))
    print(f'{len(reports)} highlighted thumbs verified; screenshots/report: {OUT}')


if __name__ == '__main__':
    try:
        main()
    finally:
        browser('close')
