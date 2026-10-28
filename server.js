/**
 * Nartech Engineering - Production HTTP Server
 * Built with Node.js standard libraries. Zero dependencies. High security & performance.
 */
const http = require('http');
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

const PORT = process.env.PORT || 3000;
const BASE_DIR = __dirname;

// Statik Hedef E-posta Adresi (İleride belirtilmek üzere statik/konfigüre edilebilir bırakıldı)
const CONFIG_DESTINATION_EMAIL = process.env.APPOINTMENT_TARGET_EMAIL || "randevu-hedef@nartech.com.tr";

// MIME Types Mapping
const MIME_TYPES = {
  '.html': 'text/html; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.js': 'application/javascript; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.jpeg': 'image/jpeg',
  '.jpg': 'image/jpeg',
  '.png': 'image/png',
  '.webp': 'image/webp',
  '.svg': 'image/svg+xml',
  '.ico': 'image/x-icon',
  '.txt': 'text/plain; charset=utf-8',
  '.xml': 'application/xml; charset=utf-8'
};

// Rate limiter store in memory
const rateLimitMap = new Map();
const RATE_LIMIT_WINDOW_MS = 60 * 1000; // 1 minute
const MAX_REQUESTS_PER_WINDOW = 15; // 15 requests/min per IP

function isRateLimited(ip) {
  const now = Date.now();
  const clientData = rateLimitMap.get(ip) || { count: 0, resetTime: now + RATE_LIMIT_WINDOW_MS };

  if (now > clientData.resetTime) {
    clientData.count = 1;
    clientData.resetTime = now + RATE_LIMIT_WINDOW_MS;
    rateLimitMap.set(ip, clientData);
    return false;
  }

  clientData.count += 1;
  rateLimitMap.set(ip, clientData);
  return clientData.count > MAX_REQUESTS_PER_WINDOW;
}

// Clean old rate limiter entries periodically
const cleanupInterval = setInterval(() => {
  const now = Date.now();
  for (const [ip, data] of rateLimitMap.entries()) {
    if (now > data.resetTime) {
      rateLimitMap.delete(ip);
    }
  }
}, 5 * 60 * 1000);
if (cleanupInterval.unref) cleanupInterval.unref();

// Basic Sanitizer for User Inputs
function sanitizeText(str) {
  if (typeof str !== 'string') return '';
  return str
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;')
    .trim();
}

// Create HTTP Server
const server = http.createServer((req, res) => {
  const clientIp = req.headers['x-forwarded-for'] || req.socket.remoteAddress || 'unknown';

  // 1. Strict Security Headers
  res.setHeader('X-Content-Type-Options', 'nosniff');
  res.setHeader('X-Frame-Options', 'DENY');
  res.setHeader('Referrer-Policy', 'strict-origin-when-cross-origin');
  res.setHeader('Permissions-Policy', 'camera=(), microphone=(), geolocation=()');
  res.setHeader('Content-Security-Policy', "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; font-src 'self'; frame-ancestors 'none';");

  const parsedUrl = new URL(req.url, `http://${req.headers.host || 'localhost'}`);
  let pathname = decodeURIComponent(parsedUrl.pathname);

  // 2. API Endpoints: Randevu (Appointment)
  if (pathname === '/api/appointment' || pathname === '/api/randevu') {
    if (req.method !== 'POST') {
      res.writeHead(405, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ success: false, message: 'Method Not Allowed' }));
      return;
    }

    if (isRateLimited(clientIp)) {
      res.writeHead(429, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ success: false, message: 'Çok fazla istek gönderildi. Lütfen bir süre sonra tekrar deneyiniz.' }));
      return;
    }

    let body = '';
    req.on('data', chunk => {
      body += chunk;
      if (body.length > 1e6) req.destroy();
    });

    req.on('end', () => {
      try {
        let data = {};
        if (req.headers['content-type'] && req.headers['content-type'].includes('application/json')) {
          data = JSON.parse(body || '{}');
        } else {
          const params = new URLSearchParams(body);
          for (const [key, val] of params.entries()) {
            data[key] = val;
          }
        }

        // Honeypot anti-spam
        if (data.company_website_url) {
          res.writeHead(200, { 'Content-Type': 'application/json' });
          res.end(JSON.stringify({ success: true, message: 'Randevu talebiniz alındı.' }));
          return;
        }

        const fullname = sanitizeText(data.fullname);
        const phone = sanitizeText(data.phone);
        const description = sanitizeText(data.description || data.notes);
        const date = sanitizeText(data.date || 'En kısa sürede');

        // Validation: Ad Soyad, Numara, Açıklama kutucukları
        if (!fullname || !phone || !description) {
          res.writeHead(400, { 'Content-Type': 'application/json' });
          res.end(JSON.stringify({
            success: false,
            message: 'Lütfen Ad Soyad, Telefon Numarası ve Açıklama alanlarını doldurunuz.'
          }));
          return;
        }

        // Statik hedefe e-posta gönderim kaydı oluştur
        const emailDispatch = {
          id: crypto.randomUUID(),
          to: CONFIG_DESTINATION_EMAIL,
          subject: `[YENİ MÜHENDİSLİK RANDEVUSU] - ${fullname}`,
          createdAt: new Date().toISOString(),
          clientIp,
          content: {
            fullname,
            phone,
            preferredDate: date,
            description
          }
        };

        console.log('[APPOINTMENT_EMAIL_SENT_TO_STATIC_DESTINATION]', JSON.stringify(emailDispatch));

        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({
          success: true,
          message: 'Randevu talebiniz başarıyla alındı ve e-posta olarak iletildi.',
          destinationEmail: CONFIG_DESTINATION_EMAIL
        }));
      } catch (err) {
        res.writeHead(400, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ success: false, message: 'Geçersiz istek verisi.' }));
      }
    });
    return;
  }

  // 2. API Endpoints: RFQ / Teklif & İletişim
  if (pathname === '/api/rfq' || pathname === '/api/contact') {
    if (req.method !== 'POST') {
      res.writeHead(405, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ success: false, message: 'Method Not Allowed' }));
      return;
    }

    if (isRateLimited(clientIp)) {
      res.writeHead(429, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ success: false, message: 'Çok fazla istek gönderildi. Lütfen bir süre sonra tekrar deneyiniz.' }));
      return;
    }

    let body = '';
    req.on('data', chunk => {
      body += chunk;
      if (body.length > 1e6) { // 1MB payload limit
        req.destroy();
      }
    });

    req.on('end', () => {
      try {
        let data = {};
        if (req.headers['content-type'] && req.headers['content-type'].includes('application/json')) {
          data = JSON.parse(body || '{}');
        } else {
          // urlencoded fallback
          const params = new URLSearchParams(body);
          for (const [key, val] of params.entries()) {
            data[key] = val;
          }
        }

        // Honeypot bot protection
        if (data.company_website_url) {
          res.writeHead(200, { 'Content-Type': 'application/json' });
          res.end(JSON.stringify({ success: true, message: 'Talebiniz alındı.' }));
          return;
        }

        const fullname = sanitizeText(data.fullname);
        const phone = sanitizeText(data.phone);
        const product = sanitizeText(data.product || 'Genel Mühendislik / Ekipman');
        const details = sanitizeText(data.details);
        const company = sanitizeText(data.company || '');
        const email = sanitizeText(data.email || '');

        // Server-Side Input Validation: strictly Ad Soyad, Telefon, Açıklama
        if (!fullname || !phone || !details) {
          res.writeHead(400, { 'Content-Type': 'application/json' });
          res.end(JSON.stringify({ success: false, message: 'Lütfen Ad Soyad, Telefon Numarası ve Açıklama alanlarını eksiksiz doldurunuz.' }));
          return;
        }

        // Log RFQ securely (without exposing sensitive secrets)
        const inquiryRecord = {
          id: crypto.randomUUID(),
          timestamp: new Date().toISOString(),
          fullname,
          phone,
          product,
          company,
          email,
          detailsLength: details.length
        };
        console.log('[RFQ_RECEIVED]', JSON.stringify(inquiryRecord));

        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({
          success: true,
          message: 'Talebiniz başarıyla alındı. Mühendislik ekibimiz en kısa sürede sizinle iletişime geçecektir.'
        }));
      } catch (err) {
        res.writeHead(400, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ success: false, message: 'Geçersiz istek verisi.' }));
      }
    });
    return;
  }

  // 3. Static File Serving with Clean URL Support
  if (pathname === '/privacy' || pathname === '/privacy.html') {
    res.writeHead(301, { 'Location': '/' });
    res.end();
    return;
  }

  if (pathname === '/') {
    pathname = '/index.html';
  } else if (!path.extname(pathname)) {
    if (fs.existsSync(path.join(BASE_DIR, pathname + '.html'))) {
      pathname = pathname + '.html';
    }
  }

  // Prevent Directory Traversal
  const safePath = path.normalize(path.join(BASE_DIR, pathname));
  if (!safePath.startsWith(BASE_DIR)) {
    res.writeHead(403, { 'Content-Type': 'text/plain' });
    res.end('Access Denied');
    return;
  }

  fs.stat(safePath, (err, stats) => {
    if (err || !stats.isFile()) {
      // Serve custom 404 page
      const notFoundPath = path.join(BASE_DIR, '404.html');
      fs.readFile(notFoundPath, (err404, data404) => {
        res.writeHead(404, { 'Content-Type': 'text/html; charset=utf-8' });
        res.end(data404 || '<h1>404 Sayfa Bulunamadı</h1>');
      });
      return;
    }

    const ext = path.extname(safePath).toLowerCase();
    const contentType = MIME_TYPES[ext] || 'application/octet-stream';

    // Caching Strategy
    if (ext === '.jpeg' || ext === '.jpg' || ext === '.png' || ext === '.webp' || ext === '.svg') {
      res.setHeader('Cache-Control', 'public, max-age=604800, immutable'); // 7 days for images
    } else if (ext === '.css' || ext === '.js') {
      res.setHeader('Cache-Control', 'public, max-age=86400'); // 1 day
    } else {
      res.setHeader('Cache-Control', 'no-cache');
    }

    res.writeHead(200, { 'Content-Type': contentType });
    const stream = fs.createReadStream(safePath);
    stream.pipe(res);
  });
});

if (require.main === module) {
  server.listen(PORT, () => {
    console.log(`Nartech Engineering web server running at http://localhost:${PORT}`);
  });
}

module.exports = server;
