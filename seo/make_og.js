// Генератор og-картинок 1200×630 в стиле сайта (см. assets/og-vmix.png как эталон).
//   NODE_PATH=<...>/node_modules node seo/make_og.js <out.png> "<EYEBROW>" "<Headline>" "<Subtitle>" ["<footer>"]
// Рендерится в Chrome, чтобы шрифт и свечение совпадали с остальными картинками.
const puppeteer = require('puppeteer-core');
const CHROME = process.env.CHROME_PATH || '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const [out, eyebrow, headline, subtitle, footer] = process.argv.slice(2);
if (!out || !headline) { console.error('  нужны: out.png EYEBROW Headline Subtitle [footer]'); process.exit(1); }
const esc = s => String(s || '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
const html = `<!doctype html><meta charset="utf-8"><style>
*{margin:0;padding:0;box-sizing:border-box}
body{width:1200px;height:630px;background:#0b0b14;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif;position:relative;overflow:hidden}
.glow{position:absolute;top:-160px;right:-180px;width:820px;height:820px;border-radius:50%;
      background:radial-gradient(circle,rgba(40,120,252,.30),rgba(40,120,252,.10) 45%,transparent 70%)}
.wrap{position:relative;padding:64px 72px;height:100%;display:flex;flex-direction:column}
.mark{font-size:31px;font-weight:800;letter-spacing:-1px;color:#fff}
.mark span{color:#2878fc}
.eyebrow{margin-top:auto;color:#2878fc;font-size:19px;font-weight:800;letter-spacing:4px;text-transform:uppercase}
h1{color:#fff;font-size:74px;font-weight:800;letter-spacing:-2.6px;line-height:1.03;margin-top:16px;max-width:900px}
.sub{margin-top:auto;color:#c8ccd8;font-size:26px;line-height:1.35;max-width:940px}
.foot{margin-top:26px;color:#6a7086;font-size:20px}
</style><div class="glow"></div><div class="wrap">
<div class="mark">split<span>cam</span></div>
<div class="eyebrow">${esc(eyebrow)}</div>
<h1>${esc(headline)}</h1>
<div class="sub">${esc(subtitle)}</div>
<div class="foot">${esc(footer || 'splitcam.com  ·  free for Windows and macOS')}</div>
</div>`;
(async () => {
  const b = await puppeteer.launch({ executablePath: CHROME, headless: 'new', args: ['--no-sandbox'] });
  const p = await b.newPage();
  await p.setViewport({ width: 1200, height: 630, deviceScaleFactor: 1 });
  await p.setContent(html, { waitUntil: 'domcontentloaded' });
  await new Promise(r => setTimeout(r, 250));
  await p.screenshot({ path: out });
  await b.close();
  console.log('  записано: ' + out);
})();
