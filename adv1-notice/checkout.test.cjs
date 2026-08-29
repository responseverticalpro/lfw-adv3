const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');

const AFFILIATE_CHECKOUT = 'https://horsejello.com/cc2/pay/checkout.php?package=6b19&hid=b2lkPW9mZl8wNzY2MTI5JmFpZD1hZmZfMDc5MTk4NiZ1aWQ9YmxfOTAwMDQxMw%3D%3D&affid=aff_0791986';

function checkoutUrl(source) {
  const match = source.match(/var CHECKOUT_URL = '([^']+)'/);
  assert.ok(match, 'CHECKOUT_URL must exist');
  return match[1];
}

function runWithParams(source, search) {
  const match = source.match(/function withParams\(u\)\{[\s\S]*?\n  \}/);
  assert.ok(match, 'withParams must exist');
  const context = { location: { search }, URLSearchParams };
  vm.runInNewContext(`${match[0]}; result = withParams(${JSON.stringify(AFFILIATE_CHECKOUT)});`, context);
  return context.result;
}

for (const file of ['index.html', 'build_quiz.py']) {
  const source = fs.readFileSync(file, 'utf8');

  test(`${file} sends checkout traffic through the affiliate URL`, () => {
    assert.equal(checkoutUrl(source), AFFILIATE_CHECKOUT);
  });

  test(`${file} preserves tracking params without allowing checkout identifiers to conflict`, () => {
    const result = runWithParams(source, '?utm_source=facebook&affid=aff_other&hid=wrong&package=other');
    assert.equal(result, `${AFFILIATE_CHECKOUT}&utm_source=facebook`);
  });
}
