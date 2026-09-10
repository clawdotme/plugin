#!/usr/bin/env node
/** Export file editions from the same built HTML. No separate content source. */
const fs = require('node:fs');
const path = require('node:path');
const {pathToFileURL} = require('node:url');
const {chromium} = require(process.env.PLAYWRIGHT_MODULE || '@playwright/test');
const output = path.resolve(process.argv[2] || '/tmp/claw-me-review-ten');
const {slugs} = JSON.parse(fs.readFileSync(path.join(__dirname, 'review-set.json'), 'utf8'));
(async () => {
  const browser = await chromium.launch();
  try {
    for (const slug of slugs) {
      const page = await browser.newPage({viewport: {width: 1440, height: 1000}});
      await page.goto(pathToFileURL(path.join(output, `${slug}.html`)).href);
      await page.evaluate(() => document.fonts.ready);
      await page.evaluate(() => document.querySelectorAll('details').forEach(detail => { detail.open = true; }));
      await page.pdf({path: path.join(output, `${slug}.pdf`), format: 'A4', landscape: slug === 'project-progress-report', printBackground: true, tagged: true, margin: {top: '14mm', bottom: '14mm', left: '14mm', right: '14mm'}});
      await page.close();
      console.log(`Exported ${slug}.pdf`);
    }
  } finally { await browser.close(); }
})().catch(error => { console.error(error); process.exitCode = 1; });
