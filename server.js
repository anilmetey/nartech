'use strict';

const fs = require('node:fs');
const path = require('node:path');
const http = require('node:http');
const nodemailer = require('nodemailer');

const ROOT = __dirname;
const MAX_BODY_BYTES = 16 * 1024;
const WINDOW_MS = 60 * 1000;
const RATE_LIMIT = 8;
const recentRequests = new Map();

function readLocalEnv() {
  const file = path.join(ROOT, '.env');
  if (!fs.existsSync(file)) return;
  for (const line of fs.readFileSync(file, 'utf8').split(/\r?\n/)) {
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith('#')) continue;
    const splitAt = trimmed.indexOf('=');
    if (splitAt < 1) continue;
    const key = trimmed.slice(0, splitAt).trim();
    let value = trimmed.slice(splitAt + 1).trim();
    if ((value.startsWith('"') && value.endsWith('"')) || (value.startsWith("'") && value.endsWith("'"))) {
      value = value.slice(1, -1);
    }
    if (/^[A-Z][A-Z0-9_]*$/.test(key) && process.env[key] === undefined) process.env[key] = value;
  }
}
readLocalEnv();
const PORT = Math.max(1, Math.min(65535, Number(process.env.PORT || 4318)));

function jsonResponse(res, status, data) {
  res.writeHead(status, {
    'Content-Type': 'application/json; charset=utf-8',
    'Cache-Control': 'no-store',
    'X-Content-Type-Options': 'nosniff',
  });
  res.end(JSON.stringify(data));
}

function readBody(req) {
  return new Promise((resolve, reject) => {
    let body = '';
    let size = 0;
    let tooLarge = false;
    req.setEncoding('utf8');
    req.on('data', chunk => {
      if (tooLarge) return;
      size += Buffer.byteLength(chunk);
      if (size > MAX_BODY_BYTES) {
        tooLarge = true;
        body = '';
        return;
      }
      body += chunk;
    });
    req.on('end', () => {
      if (tooLarge) {
        reject(Object.assign(new Error('BODY_TOO_LARGE'), { statusCode: 413 }));
        return;
      }
      try { resolve(JSON.parse(body || '{}')); }
      catch { reject(Object.assign(new Error('INVALID_JSON'), { statusCode: 400 })); }
    });
    req.on('error', reject);
  });
}

function isLimited(req) {
  const now = Date.now();
  const address = req.socket.remoteAddress || 'local';
  const prior = recentRequests.get(address) || [];
  const live = prior.filter(time => now - time < WINDOW_MS);
  live.push(now);
  recentRequests.set(address, live);
  return live.length > RATE_LIMIT;
}

function smtpSettings() {
  const host = process.env.SMTP_HOST?.trim();
  const port = Number(process.env.SMTP_PORT || 587);
  const user = process.env.SMTP_USER?.trim();
  const pass = process.env.SMTP_PASS;
  const from = process.env.SMTP_FROM?.trim() || user;
  if (!host || !Number.isInteger(port) || port < 1 || port > 65535 || !user || !pass || !from) return null;
  return { host, port, secure: String(process.env.SMTP_SECURE).toLowerCase() === 'true', auth: { user, pass }, from };
}

async function sendEmail(to, subject, text, html) {
  const settings = smtpSettings();
  if (!settings) return { ok: false, status: 503, message: 'E-posta gönderilemedi' };
  if (!isEmail(to)) return { ok: false, status: 503, message: 'E-posta gönderilemedi' };
  try {
    const transporter = nodemailer.createTransport({
      host: settings.host,
      port: settings.port,
      secure: settings.secure,
      auth: settings.auth,
      connectionTimeout: 8000,
      greetingTimeout: 8000,
      socketTimeout: 12000,
    });
    await transporter.sendMail({ from: settings.from, to, subject, text, html });
    transporter.close();
    return { ok: true };
  } catch (error) {
    console.error('E-posta gönderimi başarısız:', error.code || 'SMTP_ERROR');
    return { ok: false, status: 502, message: 'E-posta gönderilemedi' };
  }
}

function isEmail(value) {
  return typeof value === 'string' && value.length <= 254 && /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(value);
}

function calculateApi2000Venting(tankCapacityM3, maxFillRateM3h, maxEmptyRateM3h, productFlashPointAbove37C = true) {
  const outLiquid = maxFillRateM3h;
  const inLiquid = maxEmptyRateM3h;
  let thermalFactor;
  if (tankCapacityM3 <= 1000) thermalFactor = 0.5;
  else if (tankCapacityM3 <= 10000) thermalFactor = 0.3;
  else thermalFactor = 0.15;
  if (!productFlashPointAbove37C) thermalFactor *= 1.25;
  const thermalVenting = tankCapacityM3 * thermalFactor * 0.1;
  const totalOutM3h = outLiquid + thermalVenting;
  const totalInM3h = inLiquid + thermalVenting;
  const conversionFactor = 35.3147;
  return {
    tank_capacity_m3: tankCapacityM3,
    max_fill_rate_m3h: maxFillRateM3h,
    max_empty_rate_m3h: maxEmptyRateM3h,
    product_flash_point_above_37c: productFlashPointAbove37C,
    thermal_venting_m3h: thermalVenting,
    thermal_venting_scfh: thermalVenting * conversionFactor,
    outbreathing_m3h: totalOutM3h,
    outbreathing_scfh: totalOutM3h * conversionFactor,
    inbreathing_m3h: totalInM3h,
    inbreathing_scfh: totalInM3h * conversionFactor,
  };
}

function finiteNumber(value) { return typeof value === 'number' && Number.isFinite(value); }
function escapeHtml(value) {
  return String(value).replace(/[&<>"']/g, character => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[character]);
}
function fixed(value) { return value.toFixed(2); }

const DISCLAIMER = 'Yasal Uyarı ve Sorumluluk Reddi: Bu raporda sunulan tüm hesaplamalar, veriler ve sonuçlar yalnızca bilgi amaçlıdır ve hiçbir şekilde mühendislik veya ticari açıdan bağlayıcılığı yoktur. Kesin ekipman seçimi, boyutlandırma ve projelendirme aşamalarında saha koşulları, meteorolojik veriler, boru hattı dinamikleri ve yerel/uluslararası standartlar göz önünde bulundurularak doğrulama yapılması gerekmektedir.';

function reportText(calc) {
  return [
    'API 2000 7th Edition Venting Sizing Program', '',
    `Tank Capacity: ${fixed(calc.tank_capacity_m3)} m³`,
    `Max Fill Rate: ${fixed(calc.max_fill_rate_m3h)} m³/h`,
    `Max Empty Rate: ${fixed(calc.max_empty_rate_m3h)} m³/h`, '',
    '=== TOTAL SIZING RESULTS ===',
    `Thermal Venting Contribution: ${fixed(calc.thermal_venting_m3h)} m³/h (${fixed(calc.thermal_venting_scfh)} SCFH)`,
    `Total Outbreathing (Pressure Valve Capacity): ${fixed(calc.outbreathing_m3h)} m³/h | ${fixed(calc.outbreathing_scfh)} SCFH`,
    `Total Inbreathing (Vacuum Valve Capacity):   ${fixed(calc.inbreathing_m3h)} m³/h | ${fixed(calc.inbreathing_scfh)} SCFH`, '',
    DISCLAIMER,
  ].join('\n');
}

function reportHtml(calc) {
  const safeDisclaimer = escapeHtml(DISCLAIMER);
  const rows = [
    ['Tank Capacity', `${fixed(calc.tank_capacity_m3)} m³`],
    ['Max Fill Rate', `${fixed(calc.max_fill_rate_m3h)} m³/h`],
    ['Max Empty Rate', `${fixed(calc.max_empty_rate_m3h)} m³/h`],
    ['Thermal Venting Contribution', `${fixed(calc.thermal_venting_m3h)} m³/h (${fixed(calc.thermal_venting_scfh)} SCFH)`],
    ['Total Outbreathing (Pressure Valve Capacity)', `${fixed(calc.outbreathing_m3h)} m³/h | ${fixed(calc.outbreathing_scfh)} SCFH`],
    ['Total Inbreathing (Vacuum Valve Capacity)', `${fixed(calc.inbreathing_m3h)} m³/h | ${fixed(calc.inbreathing_scfh)} SCFH`],
  ];
  return `<h2>API 2000 7th Edition Venting Sizing Program</h2><table>${rows.map(([label, value]) => `<tr><th align="left">${escapeHtml(label)}</th><td>${escapeHtml(value)}</td></tr>`).join('')}</table><p>${safeDisclaimer}</p>`;
}

async function apiRequest(req, res, pathname) {
  if (req.method !== 'POST') return jsonResponse(res, 405, { message: 'Gönderilemedi' });
  if (isLimited(req)) return jsonResponse(res, 429, { message: 'Gönderilemedi' });
  let payload;
  try { payload = await readBody(req); }
  catch (error) { return jsonResponse(res, error.statusCode || 400, { message: 'Gönderilemedi' }); }

  if (pathname === '/api/api2000-report') {
    const { recipientEmail, calculation } = payload || {};
    if (!isEmail(recipientEmail) || !calculation || typeof calculation !== 'object') return jsonResponse(res, 400, { message: 'Gönderilemedi' });
    const capacity = calculation.tank_capacity_m3;
    const fillRate = calculation.max_fill_rate_m3h;
    const emptyRate = calculation.max_empty_rate_m3h;
    const flashPoint = calculation.product_flash_point_above_37c;
    if (!finiteNumber(capacity) || capacity <= 0 || !finiteNumber(fillRate) || fillRate < 0 || !finiteNumber(emptyRate) || emptyRate < 0 || typeof flashPoint !== 'boolean') {
      return jsonResponse(res, 400, { message: 'Gönderilemedi' });
    }
    const result = calculateApi2000Venting(capacity, fillRate, emptyRate, flashPoint);
    const delivery = await sendEmail(recipientEmail.trim(), 'API 2000 7th Edition Venting Sizing Program', reportText(result), reportHtml(result));
    return delivery.ok ? jsonResponse(res, 200, { message: 'Gönderildi' }) : jsonResponse(res, delivery.status, { message: delivery.message });
  }

  if (pathname === '/api/contact') {
    const { name, phone, description } = payload || {};
    if (typeof name !== 'string' || !name.trim() || name.length > 150 || typeof phone !== 'string' || !phone.trim() || phone.length > 80 || typeof description !== 'string' || !description.trim() || description.length > 5000) {
      return jsonResponse(res, 400, { message: 'Gönderilemedi' });
    }
    const destination = process.env.CONTACT_EMAIL?.trim();
    if (!isEmail(destination)) return jsonResponse(res, 503, { message: 'E-posta gönderilemedi' });
    const product = typeof payload.product === 'string' && /^[a-z0-9-]{1,100}$/.test(payload.product) ? payload.product : '';
    const lines = [`Ad Soyad: ${name.trim()}`, `Telefon No: ${phone.trim()}`, `Açıklama: ${description.trim()}`];
    if (product) lines.push(`Ürün: ${product}`);
    const content = lines.join('\n');
    const safeContent = content.split('\n').map(escapeHtml).join('<br>');
    const delivery = await sendEmail(destination, 'NarTech', content, `<p>${safeContent}</p>`);
    return delivery.ok ? jsonResponse(res, 200, { message: 'Gönderildi' }) : jsonResponse(res, delivery.status, { message: delivery.message });
  }
  return jsonResponse(res, 404, { message: 'Gönderilemedi' });
}

const TYPES = {
  '.html':'text/html; charset=utf-8', '.css':'text/css; charset=utf-8', '.js':'text/javascript; charset=utf-8',
  '.json':'application/json; charset=utf-8', '.xml':'application/xml; charset=utf-8', '.txt':'text/plain; charset=utf-8',
  '.svg':'image/svg+xml', '.png':'image/png', '.jpg':'image/jpeg', '.jpeg':'image/jpeg', '.webp':'image/webp', '.ico':'image/x-icon',
};
const PUBLIC_ROOT_FILES = new Set(['index.html','about.html','products.html','services.html','contact.html','calculator.html','faq.html','robots.txt','sitemap.xml']);
const PUBLIC_DIRECTORIES = new Set(['assets','categories','products']);

const server = http.createServer(async (req, res) => {
  res.setHeader('X-Content-Type-Options', 'nosniff');
  res.setHeader('Referrer-Policy', 'no-referrer');
  res.setHeader('Content-Security-Policy', "default-src 'self'; img-src 'self' data:; style-src 'self'; script-src 'self'; connect-src 'self'; form-action 'self'; base-uri 'self'; object-src 'none'; frame-ancestors 'none'");
  let pathname;
  try { pathname = decodeURIComponent(new URL(req.url, 'http://localhost').pathname); }
  catch { res.writeHead(400).end(''); return; }
  if (pathname.startsWith('/api/')) return apiRequest(req, res, pathname);
  if (req.method !== 'GET' && req.method !== 'HEAD') { res.writeHead(405).end(''); return; }

  const relative = pathname === '/' ? 'index.html' : pathname.replace(/^\/+/, '');
  const firstSegment = relative.split('/')[0];
  if (relative.split('/').some(segment => segment.startsWith('.')) ||
      (relative.includes('/') && !PUBLIC_DIRECTORIES.has(firstSegment)) ||
      (!relative.includes('/') && !PUBLIC_ROOT_FILES.has(firstSegment))) {
    res.writeHead(404, { 'Content-Type': 'text/plain; charset=utf-8', 'Cache-Control': 'no-store' }).end('Not found');
    return;
  }
  let filePath = path.resolve(ROOT, relative);
  if (!filePath.startsWith(ROOT + path.sep) && filePath !== ROOT) { res.writeHead(403).end(''); return; }
  try {
    if (!path.extname(filePath)) filePath += '.html';
    const info = await fs.promises.stat(filePath);
    if (info.isDirectory()) filePath = path.join(filePath, 'index.html');
    const data = await fs.promises.readFile(filePath);
    res.writeHead(200, { 'Content-Type': TYPES[path.extname(filePath).toLowerCase()] || 'application/octet-stream', 'Cache-Control': 'no-cache' });
    if (req.method === 'HEAD') res.end(); else res.end(data);
  } catch {
    res.writeHead(404, { 'Content-Type': 'text/plain; charset=utf-8', 'Cache-Control': 'no-store' });
    res.end();
  }
});

server.listen(PORT, process.env.HOST || '127.0.0.1', () => console.log(`NarTech web server: http://localhost:${PORT}`));
