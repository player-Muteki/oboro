import assert from 'node:assert/strict';
import { test } from 'node:test';
import { validateVersions } from './check-release.mjs';

const metadata = () => [
  { version: '0.3.1' },
  { version: '0.3.1' },
  { version: '0.3.1', packages: { '': { version: '0.3.1' } } },
];

test('matching versions, with and without a tag', () => {
  assert.equal(validateVersions(...metadata()), '0.3.1');
  assert.equal(validateVersions(...metadata(), '0.3.1'), '0.3.1');
});

for (const [name, mutate] of [
  ['npm version', ([, pkg]) => { pkg.version = '0.3.0'; }],
  ['lock version', ([,, lock]) => { lock.version = '0.3.0'; }],
  ['lock root version', ([,, lock]) => { lock.packages[''].version = '0.3.0'; }],
  ['missing lock root', ([,, lock]) => { delete lock.packages; }],
  ['missing manifest version', ([manifest]) => { delete manifest.version; }],
  ['empty manifest version', ([manifest]) => { manifest.version = ' '; }],
]) {
  test(`reject ${name}`, () => {
    const files = metadata();
    mutate(files);
    assert.throws(() => validateVersions(...files), /version/);
  });
}

for (const tag of ['0.3.0', 'v0.3.1', '']) {
  test(`reject mismatched tag ${JSON.stringify(tag)}`, () => {
    assert.throws(() => validateVersions(...metadata(), tag), /Release tag/);
  });
}
