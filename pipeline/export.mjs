// Step 1 – export the finished building (phase 7) from Lukáš Eršil's narodni-divadlo-3d as a flat triangle soup.
// The app is run headless in Chromium (WebGL 2 fallback); every visible mesh is baked to world space and streamed
// to out/tris.bin, with per-mesh metadata (material key, colour, registry flags) in out/meta.json.
// Env: ND_REPO (path to the cloned model repo, default vendor/narodni-divadlo-3d), ND_CHROMIUM (browser binary).
import { chromium } from 'playwright';
import fs from 'node:fs';
import path from 'node:path';
import { spawn } from 'node:child_process';

const REPO = path.resolve(process.env.ND_REPO || 'vendor/narodni-divadlo-3d');
const THREE_DIR = path.resolve('node_modules/three');
const OUT = path.resolve('out');
fs.mkdirSync(OUT, { recursive: true });

const PORT = 5199;
const server = spawn('python3', [path.join(REPO, 'serve.py'), String(PORT)], { stdio: 'ignore' });
await new Promise((r) => setTimeout(r, 1200));

const browser = await chromium.launch({
  ...(process.env.ND_CHROMIUM ? { executablePath: process.env.ND_CHROMIUM } : {}),
  args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'],
});
const page = await browser.newPage({ viewport: { width: 1280, height: 800 } });
page.on('console', (m) => { const t = m.text(); if (!t.includes('GPU stall')) console.log('[page]', t.slice(0, 300)); });
page.on('pageerror', (e) => console.log('[pageerror]', e.message));

// CDN → local node_modules; fonts → abort
await page.route(/cdn\.jsdelivr\.net\/npm\/three@0\.186\.1\/(.*)/, async (route, req) => {
  const rel = req.url().match(/three@0\.186\.1\/([^?]*)/)[1];
  const f = path.join(THREE_DIR, rel);
  if (!fs.existsSync(f)) return route.fulfill({ status: 404, body: 'nf' });
  route.fulfill({ status: 200, contentType: 'application/javascript', body: fs.readFileSync(f) });
});
await page.route(/fonts\.(googleapis|gstatic)\.com/, (route) => route.abort());
// patch main.js to expose the scene
await page.route(/\/src\/main\.js/, (route) => {
  let src = fs.readFileSync(path.join(REPO, 'src/main.js'), 'utf8');
  src = src.replace('R.update(state.T, true);', 'R.update(state.T, true); window.__ND = { scene, R, THREE, root, state, M };');
  route.fulfill({ status: 200, contentType: 'application/javascript', body: src });
});

const chunks = [];
const meta = [];
let offset = 0;
await page.exposeFunction('__emit', (m, b64) => {
  const buf = Buffer.from(b64, 'base64');
  m.start = offset; m.floats = buf.length / 4; offset += buf.length / 4;
  meta.push(m); chunks.push(buf);
});

await page.goto(`http://localhost:${PORT}/`);
await page.waitForFunction(() => window.__ND, null, { timeout: 180000 });
console.log('scene ready');
await page.waitForSelector('#loading', { state: 'detached', timeout: 600000 });
await page.waitForTimeout(2000);
console.log('warm-up done');

const stats = await page.evaluate(async () => {
  const { scene, R, THREE, M } = window.__ND;
  const matKey = new Map(); for (const [k, v] of Object.entries(M)) if (v && v.isMaterial) matKey.set(v, k);
  const regOf = new Map(); for (const it of R.items) regOf.set(it.obj, it);
  R.update(7, true);
  scene.updateMatrixWorld(true);
  const v = new THREE.Vector3();
  const m4 = new THREE.Matrix4();
  let nMesh = 0, nTri = 0;
  const skip = new Set(['sky']);
  const objs = [];
  scene.traverse((o) => { if (o.isMesh || o.isLine || o.isLineSegments || o.isPoints) objs.push(o); });
  for (const o of objs) {
    if (!o.visible) continue;
    let vis = true; for (let p = o.parent; p; p = p.parent) if (!p.visible) { vis = false; break; }
    if (!vis) continue;
    const g = o.geometry;
    if (!g || !g.attributes.position) continue;
    if (g.boundingSphere === null) g.computeBoundingSphere();
    if (g.boundingSphere.radius > 2000) continue; // sky
    const pos = g.attributes.position;
    const idx = g.index ? g.index.array : null;
    const n = idx ? idx.length : pos.count;
    const names = []; for (let p = o; p; p = p.parent) if (p.name) names.push(p.name);
    const mat = Array.isArray(o.material) ? o.material[0] : o.material;
    const type = o.isPoints ? 'points' : (o.isLineSegments ? 'linesegs' : (o.isLine ? 'line' : 'mesh'));
    const mats = (o.isInstancedMesh) ? Array.from({ length: o.count }, (_, i) => { o.getMatrixAt(i, m4); return m4.clone().premultiply(o.matrixWorld); }) : [o.matrixWorld];
    const out = new Float32Array(n * 3 * mats.length);
    let k = 0;
    for (const M of mats) {
      // skip collapsed instances
      const sc = new THREE.Vector3().setFromMatrixColumn(M, 0).length();
      if (sc < 1e-3) continue;
      for (let i = 0; i < n; i++) {
        const j = idx ? idx[i] : i;
        v.fromBufferAttribute(pos, j).applyMatrix4(M);
        out[k++] = v.x; out[k++] = v.y; out[k++] = v.z;
      }
    }
    const data = out.subarray(0, k);
    if (k === 0) continue;
    nMesh++; nTri += type === 'mesh' ? k / 9 : 0;
    const bytes = new Uint8Array(data.buffer, data.byteOffset, data.byteLength);
    let s = ''; const CH = 0x8000;
    for (let i = 0; i < bytes.length; i += CH) s += String.fromCharCode.apply(null, bytes.subarray(i, i + CH));
    await window.__emit({
      name: o.name || '', path: names.reverse().join('/'), type,
      mat: mat ? (mat.name || mat.constructor.name) : '', color: mat && mat.color ? mat.color.getHexString() : '',
      emissive: mat && mat.emissive ? mat.emissive.getHexString() : '', transparent: !!(mat && mat.transparent), opacity: mat ? mat.opacity : 1,
      instances: mats.length, matKey: matKey.get(mat) || '', reg: (() => { for (let p = o; p; p = p.parent) { const it = regOf.get(p); if (it) return { stage: it.stage, modern: it.modern, layer: it.layer, remove: it.remove, until: it.until, xray: it.xray }; } return null; })(),
    }, btoa(s));
  }
  // registry info: name → stage/modern/layer
  const reg = R.items.map((it) => ({ name: it.obj.name, stage: it.stage, modern: it.modern, layer: it.layer, remove: it.remove, until: it.until, xray: it.xray }));
  return { nMesh, nTri, reg };
});
console.log('meshes', stats.nMesh, 'triangles', stats.nTri);
fs.writeFileSync(path.join(OUT, 'tris.bin'), Buffer.concat(chunks));
fs.writeFileSync(path.join(OUT, 'meta.json'), JSON.stringify({ items: meta, registry: stats.reg }));
await browser.close();
server.kill();
console.log('done', offset * 4 / 1e6, 'MB');
