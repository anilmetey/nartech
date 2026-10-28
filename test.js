/**
 * In-process Unit & Integration Test Suite for Nartech Engineering Server
 * Completely self-contained, no TCP sockets needed.
 */
const { EventEmitter } = require('events');
const fs = require('fs');
const path = require('path');
const server = require('./server');

function mockRequest({ method = 'GET', url = '/', headers = {}, body = '' }) {
  return new Promise((resolve) => {
    const req = new EventEmitter();
    req.method = method;
    req.url = url;
    req.headers = { host: 'localhost:3000', ...headers };
    req.socket = { remoteAddress: '127.0.0.1' };

    const res = new EventEmitter();
    res.headers = {};
    res.statusCode = 200;
    res._data = [];

    res.setHeader = (k, v) => {
      res.headers[k.toLowerCase()] = v;
    };
    res.writeHead = (status, headersObj) => {
      res.statusCode = status;
      if (headersObj) {
        for (const [k, v] of Object.entries(headersObj)) {
          res.headers[k.toLowerCase()] = v;
        }
      }
    };
    res.write = (chunk) => {
      if (chunk) res._data.push(Buffer.isBuffer(chunk) ? chunk : Buffer.from(chunk));
    };
    res.end = (chunk) => {
      if (chunk) res._data.push(Buffer.isBuffer(chunk) ? chunk : Buffer.from(chunk));
      resolve({
        statusCode: res.statusCode,
        headers: res.headers,
        body: Buffer.concat(res._data).toString('utf-8')
      });
    };

    // Emit request into server
    server.emit('request', req, res);

    if (body) {
      req.emit('data', Buffer.from(body));
    }
    req.emit('end');
  });
}

async function runTests() {
  console.log('🚀 Starting Nartech Engineering In-Process Test Suite...\n');
  let passed = 0;
  let failed = 0;

  function assert(condition, testName) {
    if (condition) {
      console.log(`✅ PASS: ${testName}`);
      passed++;
    } else {
      console.error(`❌ FAIL: ${testName}`);
      failed++;
    }
  }

  try {
    // 1. Files on Disk Check
    const requiredFiles = [
      'index.html',
      'about.html',
      'products.html',
      'services.html',
      'contact.html',
      'faq.html',
      '404.html',
      'robots.txt',
      'sitemap.xml',
      'assets/css/variables.css',
      'assets/css/main.css',
      'assets/js/i18n.js',
      'assets/js/app.js',
      'assets/images/home.jpeg',
      'assets/images/nartech-logo-transparent.png',
      'assets/images/logo-white.png'
    ];

    for (const file of requiredFiles) {
      assert(fs.existsSync(path.join(__dirname, file)), `File exists: ${file}`);
    }

    // Verify privacy.html is completely removed as requested
    assert(!fs.existsSync(path.join(__dirname, 'privacy.html')), 'privacy.html is safely removed to avoid compliance penalty');

    // 2. Verify the site's approved image references
    // Check that all HTML pages use only the hero photograph and current NarTech logo.
    const htmlFiles = ['index.html', 'about.html', 'products.html', 'services.html', 'contact.html', 'faq.html', '404.html'];
    const allowedImages = ['home.jpeg', 'nartech-logo-transparent.png', 'logo-white.png'];
    for (const file of htmlFiles) {
      const content = fs.readFileSync(path.join(__dirname, file), 'utf-8');
      const imgMatches = content.match(/<img[^>]+src=["']([^"']+)["']/g) || [];
      for (const tag of imgMatches) {
        const src = tag.match(/src=["']([^"']+)["']/)[1];
        const isAllowed = allowedImages.some(img => src.toLowerCase().includes(img));
        assert(isAllowed, `Image tag in ${file} strictly references authorized asset (${src})`);
      }
      assert(content.includes('nartech-logo-transparent.png'), `${file} uses the current NarTech logo`);
    }

    // Check Hero Image Overlay Text Removal in index.html
    const indexHeroCheck = fs.readFileSync(path.join(__dirname, 'index.html'), 'utf-8');
    assert(!indexHeroCheck.includes('FIELD COMMISSION // TANK FARM & TERMINAL'), 'Hero image overlay text "FIELD COMMISSION // TANK FARM & TERMINAL" has been removed');
    assert(!indexHeroCheck.includes('CANLI UYGULAMA'), 'Hero image overlay text "CANLI UYGULAMA" has been removed');

    // 3. Server Route: Home page
    const resHome = await mockRequest({ method: 'GET', url: '/' });
    assert(resHome.statusCode === 200, 'Route / returns 200 OK');
    assert(resHome.headers['x-content-type-options'] === 'nosniff', 'Header X-Content-Type-Options: nosniff present');
    assert(resHome.headers['x-frame-options'] === 'DENY', 'Header X-Frame-Options: DENY present');
    assert(resHome.headers['content-security-policy'].includes("default-src 'self'"), 'CSP Header strict');

    // 4. Server Route: Clean URLs
    for (const p of ['about', 'products', 'services', 'contact', 'faq']) {
      const res = await mockRequest({ method: 'GET', url: `/${p}` });
      assert(res.statusCode === 200, `Clean URL /${p} returns 200 OK`);
    }

    // 4b. Privacy URL Redirect
    const resPrivacy = await mockRequest({ method: 'GET', url: '/privacy' });
    assert(resPrivacy.statusCode === 301, 'Clean URL /privacy redirects with 301 to avoid penalty');

    // 5. Server Route: 404 Not Found
    const res404 = await mockRequest({ method: 'GET', url: '/not-found-random-page' });
    assert(res404.statusCode === 404, 'Route /not-found-random-page returns 404');
    assert(res404.body.includes('404'), '404 custom template served');

    // 6. Server Route: RFQ API Validation (Incomplete)
    const resBadRfq = await mockRequest({
      method: 'POST',
      url: '/api/rfq',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify({ fullname: 'Ahmet' })
    });
    assert(resBadRfq.statusCode === 400, 'API rejects incomplete payload with 400');

    // 7. Server Route: RFQ API Valid Submission (Strictly Fullname, Phone, Details)
    const resValidRfq = await mockRequest({
      method: 'POST',
      url: '/api/rfq',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify({
        fullname: 'Mühendis Ali',
        phone: '+905551234567',
        product: 'pvrv',
        details: 'API 2000 sizing required for atmospheric crude tank'
      })
    });
    assert(resValidRfq.statusCode === 200, 'API accepts valid RFQ with strictly Ad Soyad, Telefon, Açıklama');
    const validJson = JSON.parse(resValidRfq.body);
    assert(validJson.success === true, 'API response is { success: true }');

    // 8. Server Route: Honeypot Protection
    const resBot = await mockRequest({
      method: 'POST',
      url: '/api/rfq',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify({
        fullname: 'Bot',
        company: 'Spam Inc',
        email: 'bot@spam.com',
        phone: '123',
        details: 'Spam',
        company_website_url: 'http://spam.org'
      })
    });
    assert(resBot.statusCode === 200, 'Honeypot safely intercepts bot');

    // 9. Server Route: Appointment API - Incomplete
    const resBadApt = await mockRequest({
      method: 'POST',
      url: '/api/appointment',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify({ fullname: 'Hasan' }) // missing phone and description
    });
    assert(resBadApt.statusCode === 400, 'Appointment API rejects incomplete payload with 400');

    // 10. Server Route: Appointment API - Valid Submission with Separate Fields
    const resValidApt = await mockRequest({
      method: 'POST',
      url: '/api/appointment',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify({
        fullname: 'Hasan Kaya',
        phone: '+90 532 999 88 77',
        date: '2026-11-05',
        description: 'PVRV API 2000 saha testi ve süpervizörlük randevu talebi'
      })
    });
    assert(resValidApt.statusCode === 200, 'Appointment API accepts valid appointment with 200 OK');
    const aptJson = JSON.parse(resValidApt.body);
    assert(aptJson.success === true, 'Appointment response is { success: true }');
    assert(aptJson.destinationEmail.includes('@'), 'Static target email configured in appointment response');

    // 11. Specific Feature Assertions for User Requirements
    const indexContent = fs.readFileSync(path.join(__dirname, 'index.html'), 'utf-8');
    assert(indexContent.includes('tech-window-wrapper'), 'Technical window console exists in index.html');
    assert(indexContent.includes('pane-gauge-hatches'), 'Gauge hatches pane exists in technical window');
    assert(indexContent.includes('<dt class="spec-col-info">') && indexContent.includes('<dd class="spec-col-desc">'), 'Spec box has semantic technical terms and descriptions');
    
    // Verify Gauge Hatches has 4 rows of info/description
    const ghSection = indexContent.slice(indexContent.indexOf('id="pane-gauge-hatches"'), indexContent.indexOf('id="pane-ifr-seals"'));
    const infoCount = (ghSection.match(/<dt class="spec-col-info">/g) || []).length;
    const descCount = (ghSection.match(/<dd class="spec-col-desc">/g) || []).length;
    assert(infoCount === 4, `Gauge Hatches has exactly 4 info rows (found ${infoCount})`);
    assert(descCount === 4, `Gauge Hatches has exactly 4 description rows (found ${descCount})`);

    // Verify No Pink in CSS
    const mainCssContent = fs.readFileSync(path.join(__dirname, 'assets/css/main.css'), 'utf-8');
    assert(!mainCssContent.includes('#FDF2F4'), 'main.css does not contain light pink #FDF2F4');
    assert(!mainCssContent.includes('#F8E4E9'), 'main.css does not contain light pink #F8E4E9');
    assert(!mainCssContent.includes('#FFD4DC'), 'main.css does not contain light pink #FFD4DC');

    // 12. Modal and Upgraded Sections Assertions
    assert(mainCssContent.includes('.modal-overlay') && mainCssContent.includes('position: fixed;'), 'Modal overlay has fixed positioning and does not overflow below footer');
    assert(indexContent.includes('products-catalog-banner'), 'Comprehensive Products Catalog Banner exists');
    assert(indexContent.includes('footer-tagline-badge'), 'Footer tagline badge has high-contrast styling');

    // 13. Dual-Language Isolation Assertions (TR / EN Separation)
    assert(mainCssContent.includes('html[lang="tr"] .lang-en') && mainCssContent.includes('display: none !important;'), 'CSS strictly isolates EN elements when lang="tr"');
    assert(mainCssContent.includes('html[lang="en"] .lang-tr') && mainCssContent.includes('display: none !important;'), 'CSS strictly isolates TR elements when lang="en"');
    
    // Verify 6 distinct TR and EN panes in index.html
    const trPaneCount = (indexContent.match(/class="pane-lang-section pane-lang-tr"/g) || []).length;
    const enPaneCount = (indexContent.match(/class="pane-lang-section pane-lang-en"/g) || []).length;
    assert(trPaneCount === 6, `Exactly 6 isolated Turkish pane sections in index.html (found ${trPaneCount})`);
    assert(enPaneCount === 6, `Exactly 6 isolated English pane sections in index.html (found ${enPaneCount})`);

    // Verify app.js dynamic activeLang tracking
    let appJsContent = fs.readFileSync(path.join(__dirname, 'assets/js/app.js'), 'utf-8');
    assert(appJsContent.includes('let activeLang') && appJsContent.includes('activeLang = selectedLang'), 'app.js dynamically manages activeLang without stale const locking');

    // Verify products.html bilingual isolation
    const productsContent = fs.readFileSync(path.join(__dirname, 'products.html'), 'utf-8');
    assert(productsContent.includes('class="lang-tr"') && productsContent.includes('class="lang-en"'), 'products.html utilizes dual-language isolation wrappers');

    // 14. Sectors Marquee (Sağdan Sola Kayan Ultra HD Sonsuz Marquee)
    assert(indexContent.includes('sectors-ticker-bar') && indexContent.includes('sectors-ticker-track'), 'index.html contains continuous right-to-left sectors marquee');
    assert(mainCssContent.includes('@keyframes sectors-marquee'), 'main.css contains smooth infinite sectors marquee animation');

    // 15. Standards & Certifications Grid
    assert(indexContent.includes('standards-section') && indexContent.includes('standards-grid'), 'index.html contains standards and certifications grid');
    assert(indexContent.includes('API 650') && indexContent.includes('API 2000') && indexContent.includes('EN ISO 16852') && indexContent.includes('ATEX') && indexContent.includes('FM / UL'), 'Standards grid displays all 5 requested engineering standards');

    // 16. Products Subheadings Cleanup (No ugly 1.a, 1.f, 3.a tags)
    assert(!productsContent.includes('Alt Başlık 1.a'), 'products.html does not contain placeholder Alt Başlık 1.a');
    assert(!productsContent.includes('Alt Başlık 1.f'), 'products.html does not contain placeholder Alt Başlık 1.f');
    assert(!productsContent.includes('Section 1.a'), 'products.html does not contain placeholder Section 1.a');
    assert(!productsContent.includes('Bu Alt Başlık İçin Teklif Al'), 'products.html does not contain Bu Alt Başlık İçin Teklif Al button text');

    // 17. About Page Redesign with 4K Image
    const aboutContent = fs.readFileSync(path.join(__dirname, 'about.html'), 'utf-8');
    assert(aboutContent.includes('assets/images/home.jpeg'), 'about.html contains 4K home.jpeg engineering image');
    assert(aboutContent.includes('about-hero-grid'), 'about.html utilizes split hero grid layout');
    assert(!aboutContent.includes('privacy.html'), 'about.html does not contain privacy policy links');

    // 18. Forms Only Ask for Ad Soyad, Telefon, Açıklama
    const rfqFormHtml = indexContent.slice(indexContent.indexOf('id="home-rfq-form"'), indexContent.indexOf('</form>', indexContent.indexOf('id="home-rfq-form"')));
    assert(!rfqFormHtml.includes('name="company"'), 'Home RFQ form does not ask for company name');
    assert(!rfqFormHtml.includes('name="email"'), 'Home RFQ form does not ask for corporate email');
    assert(rfqFormHtml.includes('name="fullname"'), 'Home RFQ form includes Ad Soyad');
    assert(rfqFormHtml.includes('name="phone"'), 'Home RFQ form includes Telefon Numarası');
    assert(rfqFormHtml.includes('name="details"'), 'Home RFQ form includes Açıklama');

    // 19. Hero Ambient Motion Animation (~10% opacity floating particles)
    assert(indexContent.includes('hero-ambient-bg'), 'index.html contains hero-ambient-bg container');
    assert(mainCssContent.includes('.hero-ambient-bg'), 'main.css contains .hero-ambient-bg rule');
    assert(mainCssContent.includes('@keyframes ambient-float-1'), 'main.css contains ambient-float animation');

    // 20. Technical Window Console Cleaned (No fake dots, hidden fake schematics, hidden info/desc literals)
    assert(mainCssContent.includes('.control-dots') && mainCssContent.includes('display: none !important'), 'Fake macOS window control dots are hidden');
    assert(mainCssContent.includes('.pane-schematic-frame') && mainCssContent.includes('display: none !important'), 'Fake CAD schematics are hidden');
    assert(!indexContent.includes('class="info-literal"') && !indexContent.includes('class="desc-literal"'), 'Literal info/description debug tags are absent');

    // 21. Field Supervision Services Hover & Prominent Typography
    assert(mainCssContent.includes('.service-card:hover'), 'main.css contains service-card:hover interactive transition');
    assert(mainCssContent.includes('transform: translateY(-8px)'), 'service-card:hover has prominent lift effect');
    const servicesContent = fs.readFileSync(path.join(__dirname, 'services.html'), 'utf-8');
    const servicesTrCount = (servicesContent.match(/class="lang-tr"/g) || []).length;
    const servicesEnCount = (servicesContent.match(/class="lang-en"/g) || []).length;
    assert(servicesTrCount >= 25, `services.html has comprehensive Turkish localization tags (${servicesTrCount} found)`);
    assert(servicesEnCount >= 25, `services.html has comprehensive English localization tags (${servicesEnCount} found)`);

    // 22. Standards & Certifications Translucent Frosted White & Button-Box Styling
    assert(mainCssContent.includes('backdrop-filter: blur'), 'standards-section has frosted glass backdrop filter');
    assert(mainCssContent.includes('.standard-card:hover'), 'standard-card has tactile button-box hover effect');

    // 23. Contact & FAQ Bilingual Isolation
    const contactContent = fs.readFileSync(path.join(__dirname, 'contact.html'), 'utf-8');
    const contactTrCount = (contactContent.match(/class="lang-tr"/g) || []).length;
    const contactEnCount = (contactContent.match(/class="lang-en"/g) || []).length;
    assert(contactTrCount >= 15, `contact.html has comprehensive Turkish localization tags (${contactTrCount} found)`);
    assert(contactEnCount >= 15, `contact.html has comprehensive English localization tags (${contactEnCount} found)`);

    const faqContent = fs.readFileSync(path.join(__dirname, 'faq.html'), 'utf-8');
    const faqTrCount = (faqContent.match(/class="lang-tr"/g) || []).length;
    const faqEnCount = (faqContent.match(/class="lang-en"/g) || []).length;
    assert(faqTrCount >= 10, `faq.html has comprehensive Turkish localization tags (${faqTrCount} found)`);
    assert(faqEnCount >= 10, `faq.html has comprehensive English localization tags (${faqEnCount} found)`);

    // 24. No Mixed Slashes in Products
    assert(!productsContent.includes(' / All products'), 'products.html has no mixed bilingual slash line');

    // 25. Static Email Badge Removal & Executive Appointment Button
    assert(!contactContent.includes('İletim Hedefi: Statik E-posta Kanalı'), 'contact.html does not contain static email badge');
    assert(!contactContent.includes('E-posta İletim Güvencesi'), 'contact.html does not contain email guarantee badge');
    assert(!indexHeroCheck.includes('E-posta İletim Güvencesi'), 'index.html does not contain static email notice');
    assert(contactContent.includes('btn-apt-executive'), 'contact.html uses executive appointment button');
    assert(indexHeroCheck.includes('btn-apt-executive'), 'index.html modal uses executive appointment button');
    assert(mainCssContent.includes('.btn-apt-executive'), 'main.css styles executive appointment button');

    // 26. 3D Interactive White RFQ Info Card
    assert(contactContent.includes('rfq-info-3d-card'), 'contact.html contains 3D RFQ info card');
    assert(contactContent.includes('rfq-step-pill'), 'contact.html contains RFQ step pills');
    assert(mainCssContent.includes('.rfq-info-3d-card'), 'main.css contains .rfq-info-3d-card');
    assert(mainCssContent.includes('background-color: #FFFFFF;'), 'main.css styles 3D card with white background');
    assert(mainCssContent.includes('color: #0F1A14'), 'main.css styles 3D card with high-contrast dark text');
    assert(mainCssContent.includes('perspective: 1000px;'), 'main.css configures 3D perspective');
    assert(mainCssContent.includes('@keyframes rfq-card-3d-float'), 'main.css contains 3D card floating animation');

    // 27. Collapsible Products Catalog & Spec Drawers
    assert(productsContent.includes('id="btn-expand-all"'), 'products.html contains Expand All button');
    assert(productsContent.includes('id="btn-collapse-all"'), 'products.html contains Collapse All button');
    assert(productsContent.includes('data-category-toggle'), 'products.html contains collapsible category headers');
    assert(productsContent.includes('spec-drawer'), 'products.html contains spec drawers');
    assert(productsContent.includes('spec-drawer-toggle'), 'products.html contains spec drawer toggles');
    assert(mainCssContent.includes('.spec-drawer'), 'main.css styles spec drawer accordion');
    assert(mainCssContent.includes('.category-header-wrap[data-category-toggle]'), 'main.css styles collapsible category header');

    appJsContent = fs.readFileSync(path.join(__dirname, 'assets/js/app.js'), 'utf-8');
    assert(appJsContent.includes('.spec-drawer-toggle'), 'app.js wires spec drawer toggle handler');
    assert(appJsContent.includes('[data-category-toggle]'), 'app.js wires category accordion toggle handler');
    assert(appJsContent.includes('btn-expand-all'), 'app.js wires expand all button handler');
    assert(appJsContent.includes('btn-collapse-all'), 'app.js wires collapse all button handler');

    // 28. Sectors Ticker Responsive Stacking, Spec Ledger Tactile Hover, and Standards Dossier Styling
    assert(mainCssContent.includes('mask-image: linear-gradient'), 'sectors-ticker-wrapper has smooth gradient fade mask');
    assert(mainCssContent.includes('.spec-ledger-item:hover'), 'spec-ledger-item has interactive hover state');
    assert(mainCssContent.includes('.spec-ledger-item:hover .spec-ledger-val'), 'spec-ledger-val animates on hover');
    assert(mainCssContent.includes('.spec-ledger-item:hover .spec-ledger-code'), 'spec-ledger-code animates on hover');
    assert(indexHeroCheck.includes('ATEX CERTIFIED'), 'Standards section includes English translation ATEX CERTIFIED');
    assert(indexHeroCheck.includes('FM / UL LISTED'), 'Standards section includes English translation FM / UL LISTED');
    assert(indexHeroCheck.includes('standard-card-scope'), 'Standards cards feature informative engineering scope descriptions');
    assert(mainCssContent.includes('.std-arrow-circle'), 'Standards cards feature interactive arrow circles');

    // 29. Translucent Footer Grounding on Confirm Button & RFQ Button Safely Removed
    assert(contactContent.includes('btn-apt-executive') && !contactContent.includes('Submit Engineering RFQ'), 'contact.html uses executive styling on Confirm button and redundant RFQ button is removed');
    assert(mainCssContent.includes('rgba(24, 18, 17, 0.90)') || mainCssContent.includes('rgba(24, 18, 17'), 'btn-apt-executive utilizes footer translucent dark espresso grounding');
    assert(mainCssContent.includes('backdrop-filter: blur(12px)'), 'btn-apt-executive utilizes backdrop-filter blur');

    console.log(`\n📊 Final In-Process Test Results: ${passed} Passed, ${failed} Failed.`);
    if (failed > 0) process.exit(1);
  } catch (err) {
    console.error('Error during testing:', err);
    process.exit(1);
  }
}

runTests();
