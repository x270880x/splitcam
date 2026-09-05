// Мобильная проверка страниц splitcam.com (правило CLAUDE.md: после ЛЮБОЙ правки вёрстки или текста).
//   NODE_PATH=<...>/node_modules node seo/mobile_check.js products ru/products ...
// Проверяет на 390px и 1440px: нет горизонтальной прокрутки страницы (scrollWidth == innerWidth)
// и ни один элемент не вылезает за экран НЕ будучи обрезан предком (overflow-x: auto/scroll/hidden/clip —
// таблицы и декоративные подсветки законно шире экрана внутри своего контейнера).
// RTL-локали (ar/he/fa) проверяются по левому краю. Скриншоты 390px кладутся в seo/screenshots/.
// 🔴 Браузеру задаётся en-US: иначе скрипт автоопределения языка уводит АНГЛИЙСКУЮ страницу на /ru/,
// под file:// это несуществующий путь, и проверка молча меряет страницу ошибки Chrome (найдено 2026-09-05).
// Поэтому каждая проверка требует доказательства загрузки: ровно один <h1>, непустой <title>, есть <footer>.
const puppeteer = require('puppeteer-core');
const { pathToFileURL } = require('url');
const CHROME = process.env.CHROME_PATH || '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const CLIP = new Set(['auto', 'scroll', 'hidden', 'clip']);
(async () => {
  const browser = await puppeteer.launch({ executablePath: CHROME, headless: 'new', args: ['--no-sandbox', '--lang=en-US'] });
  let bad = 0, n = 0;
  for (const spec of process.argv.slice(2)) {
    for (const [w, h, tag] of [[390, 844, 'mobile'], [1440, 900, 'desktop']]) {
      const page = await browser.newPage();
      await page.emulateTimezone('America/New_York').catch(() => {});
      await page.setExtraHTTPHeaders({ 'Accept-Language': 'en-US,en;q=0.9' });
      await page.evaluateOnNewDocument(() => {
        Object.defineProperty(navigator, 'language', { get: () => 'en-US' });
        Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] });
      });
      await page.setRequestInterception(true);
      page.on('request', r => (r.url().startsWith('file://') ? r.continue() : r.abort()));   // без сети: GA и шрифты не ждём
      await page.setViewport({ width: w, height: h, deviceScaleFactor: 1 });
      try {
        await page.goto(pathToFileURL(process.cwd() + (spec === '.' ? '' : '/' + spec) + '/index.html').href, { waitUntil: 'domcontentloaded', timeout: 20000 });
      } catch (e) {
        console.log(`  🔴  ${tag.padEnd(7)} ${spec.padEnd(28)} НЕ ОТКРЫЛАСЬ: ${String(e).split('\n')[0].slice(0, 90)}`);
        bad++; n++; await page.close(); continue;
      }
      await new Promise(r => setTimeout(r, 400));
      const r = await page.evaluate((CLIPARR) => {
        const CLIP = new Set(CLIPARR);
        const rtl = getComputedStyle(document.body).direction === 'rtl';
        const over = [];
        for (const e of document.querySelectorAll('body *')) {
          const b = e.getBoundingClientRect();
          if (b.width <= 0 || b.height <= 0) continue;
          if (!(rtl ? b.left < -1 : b.right > window.innerWidth + 1)) continue;
          let a = e.parentElement, clipped = false;
          while (a && a !== document.body) {
            if (CLIP.has(getComputedStyle(a).overflowX)) { clipped = true; break; }
            a = a.parentElement;
          }
          if (!clipped) over.push(e.tagName + '.' + (e.className || '').toString().split(' ')[0] + '@' + Math.round(rtl ? b.left : b.right));
        }
        return { scrollW: document.documentElement.scrollWidth, innerW: window.innerWidth, over: over.slice(0, 4), rtl,
                 loaded: document.querySelectorAll('h1').length === 1 && document.title.length > 10 && document.querySelectorAll('footer').length > 0 };
      }, [...CLIP]);
      const ok = r.loaded && r.scrollW <= r.innerW + 1 && r.over.length === 0;
      n++; if (!ok) bad++;
      console.log(`  ${ok ? 'OK ' : '🔴 '} ${tag.padEnd(7)} ${spec.padEnd(28)} scrollW=${r.scrollW}/${r.innerW}${r.rtl ? ' rtl' : ''}${r.loaded ? '' : '  🔴 СТРАНИЦА НЕ ЗАГРУЗИЛАСЬ'}${r.over.length ? '  вылезает: ' + r.over.join(', ') : ''}`);
      if (tag === 'mobile') await page.screenshot({ path: 'seo/screenshots/' + (spec === '.' ? 'home' : spec.replace(/\//g, '_')) + '_390.png' });
      await page.close();
    }
  }
  await browser.close();
  console.log(`  проверок ${n}, с проблемой ${bad}`);
  process.exit(bad ? 1 : 0);
})();
