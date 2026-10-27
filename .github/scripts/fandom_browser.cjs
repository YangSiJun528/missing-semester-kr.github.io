const { chromium } = require(process.env.PLAYWRIGHT_MODULE);
const fs = require('node:fs/promises');
const path = require('node:path');

const urls = [
  'https://vim.fandom.com/wiki/Search_and_replace',
  'https://vim.fandom.com/wiki/Map_caps_lock_to_escape_in_macOS',
  'https://vim.fandom.com/wiki/Using_undo_branches#Persistent_undo',
  'https://vim.fandom.com/wiki/Vim_Tips_Wiki',
  'https://vim.fandom.com/wiki/Vim_key_bindings_for_web_browsers',
];
const mode = process.env.BROWSER_MODE || 'headless';
const output = path.resolve('diagnostics', mode);

(async () => {
  await fs.mkdir(output, { recursive: true });
  const browser = await chromium.launch({ headless: mode === 'headless' });
  const context = await browser.newContext();
  const results = [];
  try {
    for (const [index, url] of urls.entries()) {
      const page = await context.newPage();
      const navigations = [];
      const pending = [];
      const errors = [];
      const started = Date.now();
      page.on('response', response => {
        if (response.request().isNavigationRequest() && response.frame() === page.mainFrame()) {
          pending.push((async () => {
            const headers = await response.allHeaders();
            if (headers['set-cookie']) headers['set-cookie'] = '[redacted]';
            navigations.push({ url: response.url(), status: response.status(), headers, elapsed_ms: Date.now() - started });
          })());
        }
      });
      try {
        await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 30000 });
        await page.waitForFunction(() => document.querySelector('.mw-parser-output') && !/just a moment/i.test(document.title), null, { timeout: 25000 });
      } catch (error) {
        errors.push(String(error));
      }
      await Promise.allSettled(pending);
      const content = await page.evaluate(() => {
        const article = document.querySelector('.mw-parser-output');
        const hash = decodeURIComponent(location.hash.slice(1));
        return {
          title: document.title,
          h1: document.querySelector('h1')?.textContent?.trim() || '',
          article_characters: article?.textContent?.length || 0,
          anchor_exists: !hash || Boolean(document.getElementById(hash) || document.getElementsByName(hash).length),
          body_excerpt: document.body?.innerText?.slice(0, 300) || '',
        };
      }).catch(error => {
        errors.push(String(error));
        return { title: '', h1: '', article_characters: 0, anchor_exists: false, body_excerpt: '' };
      });
      const expected = decodeURIComponent(new URL(url).pathname.split('/').pop()).replaceAll('_', ' ').toLowerCase();
      const last = navigations.at(-1);
      const passed = last?.status >= 200 && last.status < 300 && content.article_characters > 500 && content.h1.toLowerCase().includes(expected) && content.anchor_exists;
      const result = { mode, browser_version: browser.version(), url, final_url: page.url(), elapsed_ms: Date.now() - started, passed, navigations, errors, ...content };
      results.push(result);
      await page.screenshot({ path: path.join(output, `${index}.png`) }).catch(error => errors.push(String(error)));
      await fs.writeFile(path.join(output, `${index}.json`), JSON.stringify(result, null, 2) + '\n');
      console.log(JSON.stringify(result));
      await page.close();
    }
  } finally {
    await browser.close();
    await fs.writeFile(path.join(output, 'results.json'), JSON.stringify(results, null, 2) + '\n');
  }
  process.exitCode = results.length === urls.length && results.every(row => row.passed) ? 0 : 1;
})().catch(error => { console.error(error); process.exitCode = 1; });
