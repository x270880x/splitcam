// Correct mobile screenshots via CDP device emulation (real 390 layout viewport).
import { spawn } from 'node:child_process';
import http from 'node:http';
import { writeFileSync } from 'node:fs';

const CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const PORT = 9334, BASE = 'http://localhost:8799/';
const UA = 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1';
const SHOTS = [['ar/', 'ar', 'qa2-ar-home-m'], ['ar/products/', 'ar', 'qa2-ar-products-m'], ['ko/products/', 'ko', 'qa2-ko-products-m'], ['th/for/churches/', 'th', 'qa2-th-churches-m']];
const sleep = ms => new Promise(r => setTimeout(r, ms));
const getJSON = u => new Promise((res, rej) => http.get(u, r => { let d = ''; r.on('data', c => d += c); r.on('end', () => res(JSON.parse(d))); }).on('error', rej));

const chrome = spawn(CHROME, ['--headless=new', '--disable-gpu', `--remote-debugging-port=${PORT}`, '--user-data-dir=/tmp/cdpqa_shots', '--no-first-run', 'about:blank']);
let ws;
try {
  let tabs; for (let i = 0; i < 40; i++) { try { tabs = await getJSON(`http://localhost:${PORT}/json`); if (tabs.length) break; } catch {} await sleep(250); }
  ws = new WebSocket(tabs.find(t => t.type === 'page').webSocketDebuggerUrl);
  await new Promise((r, j) => { ws.onopen = r; ws.onerror = j; });
  let id = 0; const pend = new Map(); const waiters = [];
  ws.onmessage = e => { const m = JSON.parse(e.data); if (m.id && pend.has(m.id)) { pend.get(m.id)(m.result); pend.delete(m.id); } if (m.method) waiters.forEach(w => w(m)); };
  const cmd = (method, params = {}) => new Promise(r => { const i = ++id; pend.set(i, r); ws.send(JSON.stringify({ id: i, method, params })); });
  const onceEvent = n => new Promise(r => { const w = m => { if (m.method === n) { waiters.splice(waiters.indexOf(w), 1); r(); } }; waiters.push(w); });
  await cmd('Page.enable');
  for (const [path, lang, name] of SHOTS) {
    await cmd('Emulation.setDeviceMetricsOverride', { width: 390, height: 844, deviceScaleFactor: 2, mobile: true });
    await cmd('Emulation.setUserAgentOverride', { userAgent: UA, acceptLanguage: lang });
    const loaded = onceEvent('Page.loadEventFired');
    await cmd('Page.navigate', { url: BASE + path });
    await Promise.race([loaded, sleep(8000)]); await sleep(1100);
    const { data } = await cmd('Page.captureScreenshot', { format: 'png', captureBeyondViewport: true, clip: { x: 0, y: 0, width: 390, height: 1500, scale: 1 } });
    writeFileSync(`seo/screenshots/${name}.png`, Buffer.from(data, 'base64'));
    console.log('shot', name);
  }
} finally { if (ws) try { ws.close(); } catch {} chrome.kill('SIGKILL'); }
