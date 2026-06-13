// Headless-Chrome CDP overflow probe. Measures scrollWidth vs innerWidth with
// real mobile emulation, per-locale Accept-Language (so the auto-redirect stays put).
import { spawn } from 'node:child_process';
import http from 'node:http';

const CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const PORT = 9333;
const BASE = 'http://localhost:8799/';
const MOBILE_UA = 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1';

// [path, lang, viewport] — viewport 'm' = 390 mobile, 'd' = 1440 desktop
const PAGES = [
  ['', 'en', 'm'], ['bg/', 'bg', 'm'],
  ['ar/', 'ar', 'm'], ['ar/products/', 'ar', 'm'], ['ar/for/churches/', 'ar', 'm'], ['ar/', 'ar', 'd'],
  ['th/for/churches/', 'th', 'm'], ['hu/changelog/', 'hu', 'm'],
  ['ko/products/', 'ko', 'm'], ['pl/privacy-policy/', 'pl', 'm'],
];

const sleep = ms => new Promise(r => setTimeout(r, ms));
const getJSON = url => new Promise((res, rej) => http.get(url, r => { let d = ''; r.on('data', c => d += c); r.on('end', () => res(JSON.parse(d))); }).on('error', rej));

const chrome = spawn(CHROME, ['--headless=new', '--disable-gpu', `--remote-debugging-port=${PORT}`,
  '--user-data-dir=/tmp/cdpqa_splitcam', '--no-first-run', '--no-default-browser-check', 'about:blank']);

let ws;
try {
  // wait for devtools endpoint
  let tabs;
  for (let i = 0; i < 40; i++) { try { tabs = await getJSON(`http://localhost:${PORT}/json`); if (tabs.length) break; } catch {} await sleep(250); }
  const page = tabs.find(t => t.type === 'page');
  ws = new WebSocket(page.webSocketDebuggerUrl);
  await new Promise((r, j) => { ws.onopen = r; ws.onerror = j; });

  let id = 0; const pend = new Map(); const waiters = [];
  ws.onmessage = e => {
    const m = JSON.parse(e.data);
    if (m.id && pend.has(m.id)) { pend.get(m.id)(m.result); pend.delete(m.id); }
    if (m.method) waiters.forEach(w => w(m));
  };
  const cmd = (method, params = {}) => new Promise(r => { const i = ++id; pend.set(i, r); ws.send(JSON.stringify({ id: i, method, params })); });
  const onceEvent = name => new Promise(r => { const w = m => { if (m.method === name) { const k = waiters.indexOf(w); if (k >= 0) waiters.splice(k, 1); r(m.params); } }; waiters.push(w); });

  await cmd('Page.enable'); await cmd('Runtime.enable');

  const rows = [];
  for (const [path, lang, vp] of PAGES) {
    const W = vp === 'd' ? 1440 : 390, H = vp === 'd' ? 900 : 844;
    await cmd('Emulation.setDeviceMetricsOverride', { width: W, height: H, deviceScaleFactor: vp === 'd' ? 1 : 2, mobile: vp !== 'd' });
    await cmd('Emulation.setUserAgentOverride', { userAgent: vp === 'd' ? '' : MOBILE_UA, acceptLanguage: lang });
    const loaded = onceEvent('Page.loadEventFired');
    await cmd('Page.navigate', { url: BASE + path });
    await Promise.race([loaded, sleep(8000)]);
    await sleep(900); // let redirect/layout settle
    const { result } = await cmd('Runtime.evaluate', {
      returnByValue: true,
      expression: `(()=>{var d=document.documentElement;return{loc:location.pathname,iw:innerWidth,sw:d.scrollWidth,bw:document.body?document.body.scrollWidth:0,over:Math.max(d.scrollWidth,document.body?document.body.scrollWidth:0)-innerWidth};})()`
    });
    const r = result.value;
    rows.push({ want: '/' + path, ...r, vp });
  }

  console.log('VP  ' + 'requested'.padEnd(24) + 'landed'.padEnd(24) + 'iw   sw   over');
  for (const r of rows) {
    const flag = r.over > 0 ? `  ⟵ OVERFLOW +${r.over}px` : '';
    console.log(`${r.vp}   ${r.want.padEnd(24)}${String(r.loc).padEnd(24)}${String(r.iw).padEnd(5)}${String(r.sw).padEnd(5)}${r.over}${flag}`);
  }
} finally {
  if (ws) try { ws.close(); } catch {}
  chrome.kill('SIGKILL');
}
