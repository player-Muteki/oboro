#!/usr/bin/env node
// Keep the shipped manifest, npm metadata and optional bare release tag in sync.
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { pathToFileURL } from 'node:url';

export function validateVersions(manifest, pkg, lock, tag) {
  const version = manifest.version;
  assert.ok(typeof version === 'string' && version.trim() !== '', 'manifest.json: missing version');
  for (const [file, actual] of [
    ['package.json', pkg.version],
    ['package-lock.json', lock.version],
    ['package-lock.json packages[""]', lock.packages?.['']?.version],
  ]) {
    assert.equal(actual, version, `${file}: version must match manifest.json (${version})`);
  }
  if (tag !== undefined) {
    assert.equal(tag, version, `Release tag must exactly match manifest.json (${version}; no v prefix)`);
  }
  return version;
}

function main() {
  const args = process.argv.slice(2);
  assert.ok(args.length <= 1, 'Usage: node scripts/check-release.mjs [release-tag]');
  const root = new URL('../', import.meta.url);
  const read = name => JSON.parse(readFileSync(new URL(name, root), 'utf8'));
  const version = validateVersions(read('manifest.json'), read('package.json'), read('package-lock.json'), args[0]);
  assert.ok(readFileSync(new URL('theme.css', root), 'utf8').trim(), 'theme.css must not be empty');
  console.log(`Release metadata OK: ${version}${args.length ? ` (tag ${args[0]})` : ''}`);
}

if (process.argv[1] && pathToFileURL(process.argv[1]).href === import.meta.url) {
  try {
    main();
  } catch (error) {
    console.error(error.message);
    process.exitCode = 1;
  }
}
