(() => {
  const root = document.documentElement;
  const statusCopy = {
    sent: { tr: 'Gönderildi', en: 'Sent' },
    failed: { tr: 'Gönderilemedi', en: 'Could not send' },
  };
  const setStatus = (element, key) => {
    element.dataset.statusKey = key;
    element.textContent = statusCopy[key][root.dataset.language] || '';
  };

  const selectedLanguage = () => {
    try { return localStorage.getItem('nartech-language') || 'tr'; }
    catch { return 'tr'; }
  };
  const setLanguage = language => {
    language = language === 'en' ? 'en' : 'tr';
    root.dataset.language = language;
    root.lang = language;
    const english = language === 'en';
    document.title = english ? root.dataset.titleEn : root.dataset.titleTr;
    const menuButton = document.querySelector('[data-nav-toggle]');
    if (menuButton) {
      const isOpen = menuButton.getAttribute('aria-expanded') === 'true';
      const labelLanguage = english ? 'En' : 'Tr';
      const labelAction = isOpen ? 'close' : 'open';
      menuButton.setAttribute('aria-label', menuButton.dataset[`${labelAction}Label${labelLanguage}`]);
    }
    document.querySelectorAll('[data-set-language]').forEach(button => {
      button.setAttribute('aria-pressed', String(button.dataset.setLanguage === language));
    });
    document.querySelectorAll('[data-aria-tr][data-aria-en]').forEach(element => {
      element.setAttribute('aria-label', english ? element.dataset.ariaEn : element.dataset.ariaTr);
    });
    document.querySelectorAll('[data-alt-tr][data-alt-en]').forEach(element => {
      element.setAttribute('alt', english ? element.dataset.altEn : element.dataset.altTr);
    });
    document.querySelectorAll('[data-i18n-tr][data-i18n-en]').forEach(element => {
      element.textContent = english ? element.dataset.i18nEn : element.dataset.i18nTr;
    });
    document.querySelectorAll('[data-status-key]').forEach(element => {
      element.textContent = statusCopy[element.dataset.statusKey]?.[language] || '';
    });
    document.dispatchEvent(new CustomEvent('nartech-language-change', { detail: { language } }));
    try { localStorage.setItem('nartech-language', language); } catch { /* Storage may be unavailable for file previews. */ }
  };
  setLanguage(selectedLanguage());
  document.addEventListener('click', event => {
    const button = event.target.closest('[data-set-language]');
    if (button) setLanguage(button.dataset.setLanguage);
  });

  const navToggle = document.querySelector('[data-nav-toggle]');
  const siteNav = document.querySelector('#site-nav');
  const navBackdrop = document.querySelector('[data-nav-close]');
  if (navToggle && siteNav && navBackdrop) {
    const mobileNav = window.matchMedia('(max-width: 1100px)');
    const menuLabel = opened => {
      const language = root.dataset.language === 'en' ? 'En' : 'Tr';
      navToggle.setAttribute('aria-label', navToggle.dataset[`${opened ? 'close' : 'open'}Label${language}`]);
    };
    const closeMenu = returnFocus => {
      root.removeAttribute('data-nav-open');
      document.body.classList.remove('nav-is-open');
      navToggle.setAttribute('aria-expanded', 'false');
      menuLabel(false);
      if (returnFocus) navToggle.focus();
    };
    const openMenu = () => {
      if (!mobileNav.matches) return;
      root.setAttribute('data-nav-open', 'true');
      document.body.classList.add('nav-is-open');
      navToggle.setAttribute('aria-expanded', 'true');
      menuLabel(true);
      siteNav.querySelector('a')?.focus();
    };
    navToggle.addEventListener('click', () => {
      if (root.dataset.navOpen === 'true') closeMenu(true);
      else openMenu();
    });
    navBackdrop.addEventListener('click', () => closeMenu(true));
    siteNav.querySelectorAll('a').forEach(link => link.addEventListener('click', () => closeMenu(false)));
    document.addEventListener('keydown', event => {
      if (event.key === 'Escape' && root.dataset.navOpen === 'true') closeMenu(true);
    });
    mobileNav.addEventListener('change', event => {
      if (!event.matches) closeMenu(false);
    });
  }

  document.querySelectorAll('.catalog-index a[href^="#"]').forEach(link => {
    link.addEventListener('click', () => {
      const target = document.getElementById(link.hash.slice(1));
      if (target?.tagName === 'DETAILS') target.open = true;
    });
  });

  const homeProductExplorer = document.querySelector('[data-home-product-explorer]');
  if (homeProductExplorer) {
    const categoryButtons = [...homeProductExplorer.querySelectorAll('[data-home-category]')];
    const productPanels = [...homeProductExplorer.querySelectorAll('[data-home-product-panel]')];
    categoryButtons.forEach(button => {
      button.addEventListener('click', () => {
        const selectedCategory = button.dataset.homeCategory;
        if (!productPanels.some(panel => panel.dataset.homeProductPanel === selectedCategory)) return;
        categoryButtons.forEach(item => item.setAttribute('aria-pressed', String(item === button)));
        productPanels.forEach(panel => {
          panel.hidden = panel.dataset.homeProductPanel !== selectedCategory;
        });
      });
    });
  }

  const calculatorEmailForm = document.querySelector('#calc-email-form');
  if (calculatorEmailForm) {
    const stepEmail = document.querySelector('#calc-step-email');
    const stepInputs = document.querySelector('#calc-step-inputs');
    const stepResults = document.querySelector('#calc-step-results');
    const resultContent = document.querySelector('#calc-results');
    const status = document.querySelector('#calc-status');
    let recipientEmail = '';
    let calculation = null;

    const showStep = number => {
      stepEmail.hidden = number !== 1;
      stepInputs.hidden = number !== 2;
      stepResults.hidden = number !== 3;
      document.querySelectorAll('[data-step-indicator]').forEach(indicator => {
        if (Number(indicator.dataset.stepIndicator) === number) indicator.setAttribute('aria-current', 'step');
        else indicator.removeAttribute('aria-current');
      });
    };
    const format = value => new Intl.NumberFormat(root.dataset.language === 'en' ? 'en-US' : 'tr-TR', {
      minimumFractionDigits: 2,
      maximumFractionDigits: 2,
    }).format(Number(value));
    const createResult = (label, value) => {
      const row = document.createElement('div');
      row.className = 'calc-result-row';
      const name = document.createElement('dt');
      name.textContent = label;
      const result = document.createElement('dd');
      result.textContent = value;
      row.append(name, result);
      return row;
    };

    const renderResults = () => {
      if (!calculation) return;
      const labels = root.dataset.language === 'en' ? {
        capacity: 'Tank Capacity',
        fill: 'Max Fill Rate',
        empty: 'Max Empty Rate',
        thermal: 'Thermal Venting Contribution',
        out: 'Total Outbreathing (Pressure Valve Capacity)',
        in: 'Total Inbreathing (Vacuum Valve Capacity)',
      } : {
        capacity: 'Tank Kapasitesi',
        fill: 'Maksimum Dolum Debisi',
        empty: 'Maksimum Boşaltım Debisi',
        thermal: 'Termal Nefesleme Katkısı',
        out: 'Toplam Dış Nefesleme (Basınç Ventili Kapasitesi)',
        in: 'Toplam İç Nefesleme (Vakum Ventili Kapasitesi)',
      };
      resultContent.replaceChildren(
        createResult(labels.capacity, `${format(calculation.tank_capacity_m3)} m³`),
        createResult(labels.fill, `${format(calculation.max_fill_rate_m3h)} m³/h`),
        createResult(labels.empty, `${format(calculation.max_empty_rate_m3h)} m³/h`),
        createResult(labels.thermal, `${format(calculation.thermal_venting_m3h)} m³/h | ${format(calculation.thermal_venting_scfh)} SCFH`),
        createResult(labels.out, `${format(calculation.outbreathing_m3h)} m³/h | ${format(calculation.outbreathing_scfh)} SCFH`),
        createResult(labels.in, `${format(calculation.inbreathing_m3h)} m³/h | ${format(calculation.inbreathing_scfh)} SCFH`),
      );
    };

    calculatorEmailForm.addEventListener('submit', event => {
      event.preventDefault();
      const field = calculatorEmailForm.elements.email;
      if (!field.reportValidity()) return;
      recipientEmail = field.value.trim();
      showStep(2);
      document.querySelector('#tank-capacity').focus();
    });

    document.querySelector('#calc-input-form').addEventListener('submit', event => {
      event.preventDefault();
      const form = event.currentTarget;
      if (!form.reportValidity()) return;
      const capacity = Number(form.elements.tank_capacity_m3.value);
      const fillRate = Number(form.elements.max_fill_rate_m3h.value);
      const emptyRate = Number(form.elements.max_empty_rate_m3h.value);
      if (![capacity, fillRate, emptyRate].every(Number.isFinite) || capacity <= 0 || fillRate < 0 || emptyRate < 0) return;

      let thermalFactor = capacity <= 1000 ? 0.5 : capacity <= 10000 ? 0.3 : 0.15;
      const flashPointAbove37C = form.elements.product_flash_point_above_37c.value === 'true';
      if (!flashPointAbove37C) thermalFactor *= 1.25;
      const thermalVenting = capacity * thermalFactor * 0.1;
      const totalOutbreathing = fillRate + thermalVenting;
      const totalInbreathing = emptyRate + thermalVenting;
      const conversionFactor = 35.3147;
      calculation = {
        tank_capacity_m3: capacity,
        max_fill_rate_m3h: fillRate,
        max_empty_rate_m3h: emptyRate,
        product_flash_point_above_37c: flashPointAbove37C,
        thermal_venting_m3h: thermalVenting,
        thermal_venting_scfh: thermalVenting * conversionFactor,
        outbreathing_m3h: totalOutbreathing,
        outbreathing_scfh: totalOutbreathing * conversionFactor,
        inbreathing_m3h: totalInbreathing,
        inbreathing_scfh: totalInbreathing * conversionFactor,
      };
      renderResults();
      status.removeAttribute('data-status-key');
      status.textContent = '';
      showStep(3);
      document.querySelector('#calc-send').focus();
    });

    document.querySelector('#calc-back').addEventListener('click', () => {
      status.removeAttribute('data-status-key');
      status.textContent = '';
      showStep(2);
    });

    document.addEventListener('nartech-language-change', renderResults);

    document.querySelector('#calc-send').addEventListener('click', async event => {
      if (!calculation || !recipientEmail) return;
      const button = event.currentTarget;
      button.disabled = true;
      status.removeAttribute('data-status-key');
      status.textContent = '';
      try {
        const response = await fetch('/api/api2000-report', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ recipientEmail, calculation, language: root.dataset.language }),
        });
        if (!response.ok) throw new Error('send-failed');
        setStatus(status, 'sent');
      } catch {
        setStatus(status, 'failed');
      } finally {
        button.disabled = false;
      }
    });
  }

  const contactForm = document.querySelector('#contact-form');
  if (contactForm) {
    const params = new URLSearchParams(location.search);
    contactForm.elements.product.value = params.get('product') || '';
    const status = document.querySelector('#contact-status');
    contactForm.addEventListener('submit', async event => {
      event.preventDefault();
      if (!contactForm.reportValidity()) return;
      const button = contactForm.querySelector('button[type="submit"]');
      button.disabled = true;
      status.removeAttribute('data-status-key');
      status.textContent = '';
      const form = new FormData(contactForm);
      try {
        const response = await fetch('/api/contact', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ name: form.get('name'), phone: form.get('phone'), description: form.get('description'), product: form.get('product'), language: root.dataset.language }),
        });
        if (!response.ok) throw new Error('send-failed');
        setStatus(status, 'sent');
        contactForm.reset();
        contactForm.elements.product.value = params.get('product') || '';
      } catch {
        setStatus(status, 'failed');
      } finally {
        button.disabled = false;
      }
    });
  }

  const proofStrip = document.querySelector('.home-proof-strip');
  if (proofStrip) {
    const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    const revealProof = () => {
      proofStrip.classList.add('is-visible');
      if (reducedMotion) return;
      proofStrip.querySelectorAll('[data-count-up]').forEach(element => {
        const target = Number(element.dataset.countUp);
        const suffix = element.dataset.countSuffix || '';
        const duration = 900;
        const startedAt = performance.now();
        const update = now => {
          const progress = Math.min((now - startedAt) / duration, 1);
          const eased = 1 - Math.pow(1 - progress, 3);
          element.textContent = `${Math.round(target * eased)}${suffix}`;
          if (progress < 1) requestAnimationFrame(update);
        };
        requestAnimationFrame(update);
      });
    };

    if (reducedMotion || !('IntersectionObserver' in window)) {
      proofStrip.classList.add('is-visible');
    } else {
      const proofObserver = new IntersectionObserver(entries => {
        if (entries.some(entry => entry.isIntersecting)) {
          revealProof();
          proofObserver.disconnect();
        }
      }, { threshold: 0.2 });
      proofObserver.observe(proofStrip);
    }
  }

  const homeFlow = document.querySelector('[data-home-flow]');
  if (homeFlow) {
    const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    const showFlow = () => homeFlow.classList.add('is-visible');

    if (reducedMotion || !('IntersectionObserver' in window)) {
      showFlow();
    } else {
      homeFlow.classList.add('motion-ready');
      const flowObserver = new IntersectionObserver(entries => {
        if (entries.some(entry => entry.isIntersecting)) {
          showFlow();
          flowObserver.disconnect();
        }
      }, { threshold: 0.12 });
      flowObserver.observe(homeFlow);
    }
  }
})();
