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
    root.setAttribute('data-language', language);
    root.lang = language;
    const english = language === 'en';
    if (root.dataset.titleEn && root.dataset.titleTr) {
      document.title = english ? root.dataset.titleEn : root.dataset.titleTr;
    }
    const menuButton = document.querySelector('[data-nav-toggle]');
    if (menuButton) {
      const isOpen = menuButton.getAttribute('aria-expanded') === 'true';
      const labelLanguage = english ? 'En' : 'Tr';
      const labelAction = isOpen ? 'close' : 'open';
      const labelVal = menuButton.dataset[`${labelAction}Label${labelLanguage}`];
      if (labelVal) menuButton.setAttribute('aria-label', labelVal);
    }
    document.querySelectorAll('[data-set-language]').forEach(button => {
      const isActive = button.dataset.setLanguage === language;
      button.setAttribute('aria-pressed', String(isActive));
      if (isActive) {
        button.classList.add('is-active');
      } else {
        button.classList.remove('is-active');
      }
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
    document.querySelectorAll('[data-placeholder-tr][data-placeholder-en]').forEach(element => {
      element.setAttribute('placeholder', english ? element.dataset.placeholderEn : element.dataset.placeholderTr);
    });
    document.querySelectorAll('[data-status-key]').forEach(element => {
      element.textContent = statusCopy[element.dataset.statusKey]?.[language] || '';
    });
    document.dispatchEvent(new CustomEvent('nartech-language-change', { detail: { language } }));
    try { localStorage.setItem('nartech-language', language); } catch { /* Storage may be unavailable for file previews. */ }
  };

  const bindLanguageControls = () => {
    document.querySelectorAll('[data-set-language]').forEach(button => {
      button.addEventListener('click', event => {
        event.preventDefault();
        event.stopPropagation();
        setLanguage(button.dataset.setLanguage);
      });
    });
  };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
      bindLanguageControls();
      setLanguage(selectedLanguage());
    });
  } else {
    bindLanguageControls();
    setLanguage(selectedLanguage());
  }

  document.addEventListener('click', event => {
    const button = event.target.closest('[data-set-language]');
    if (button) {
      event.preventDefault();
      setLanguage(button.dataset.setLanguage);
    }
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
    let revealed = false;
    const revealProof = () => {
      if (revealed) return;
      revealed = true;
      proofStrip.classList.add('is-visible');
      if (reducedMotion) return;
      proofStrip.querySelectorAll('[data-count-up]').forEach(element => {
        const target = Number(element.dataset.countUp);
        const suffix = element.dataset.countSuffix || '';
        const duration = 1500;
        const startedAt = performance.now();
        element.classList.add('is-counting');
        const update = now => {
          const progress = Math.min((now - startedAt) / duration, 1);
          const easeOut = 1 - Math.pow(1 - progress, 3);
          const count = progress < 1 ? Math.min(target, Math.floor(target * easeOut) + 1) : target;
          element.textContent = `${count}${suffix}`;
          if (progress < 1) requestAnimationFrame(update);
          else {
            element.textContent = `${target}${suffix}`;
            element.classList.remove('is-counting');
          }
        };
        requestAnimationFrame(update);
      });
    };

    if (reducedMotion || !('IntersectionObserver' in window)) {
      revealProof();
    } else {
      const checkInView = () => {
        const rect = proofStrip.getBoundingClientRect();
        if (rect.top < window.innerHeight + 100 && rect.bottom > -50) {
          revealProof();
          return true;
        }
        return false;
      };

      if (!checkInView()) {
        setTimeout(checkInView, 80);
      }

      const proofObserver = new IntersectionObserver(entries => {
        if (entries.some(entry => entry.isIntersecting)) {
          revealProof();
          proofObserver.disconnect();
        }
      }, { threshold: 0, rootMargin: '120px 0px' });
      proofObserver.observe(proofStrip);
    }
  }

  const setupSupplyChain = () => {
    const supplyChainWrapper = document.querySelector('.supply-chain-wrapper');
    if (!supplyChainWrapper) return;

    const bannerText = document.getElementById('banner-text');
    const flowGroups = supplyChainWrapper.querySelectorAll('.flow-group');
    const nodeCards = supplyChainWrapper.querySelectorAll('.node-card');
    const hubCenter = supplyChainWrapper.querySelector('#hub-nartech');

    const nodeInfoMap = {
      consultancy: {
        tr: { title: 'Danışmanlık & Doğru Ürün Seçimi', desc: 'Müşteri operasyonel şartlarına en uygun, sertifikalı ve uzun ömürlü tank/terminal ekipmanlarının mühendislik analizi ile belirlenmesi.' },
        en: { title: 'Consultancy & Optimal Equipment Selection', desc: 'Identifying long-lasting, certified tank and terminal equipment tailored to client operational specifications.' }
      },
      engineering: {
        tr: { title: 'Mühendislik & Şartname Uyumu', desc: 'Projeye özel teknik şartnamelerin hazırlanması, proses/mekanik hesaplamalar ve uluslararası normlara tam uyumun sağlanması.' },
        en: { title: 'Engineering & Specification Compliance', desc: 'Preparing project-specific specifications, mechanical/process calculations, and ensuring total alignment with international standards.' }
      },
      procurement: {
        tr: { title: 'Doğrudan Üreticiden Tedarik', desc: 'Aracısız, doğrudan birinci el küresel üreticilerden en kaliteli tank ve terminal ekipmanlarının rekabetçi koşullarla temini.' },
        en: { title: 'Direct Procurement from Manufacturers', desc: 'Procuring premium certified equipment directly from world-class manufacturers under optimal and competitive conditions.' }
      },
      supervision: {
        tr: { title: 'Saha Süpervizörlüğü & Denetim', desc: 'Montaj, devreye alma ve saha kontrollerinde yerinde teknik gözetim, PVRV set point testleri ve IFR montaj süpervizörlüğü.' },
        en: { title: 'Field Supervision & Inspection', desc: 'On-site technical supervision, PVRV set point inspection, and IFR installation checks during mechanical assembly and commissioning.' }
      },
      hub: {
        tr: { title: 'NarTech Tank Terminal Solutions', desc: 'Depolama tankı ve terminal çözümlerinde doğru mühendislik, kaliteli ürün ve küresel standartları birleştiren güvenilir merkez.' },
        en: { title: 'NarTech Tank Terminal Solutions', desc: 'The trusted engineering hub uniting sound design, premier products, and international standards in storage tank and terminal solutions.' }
      },
      solutions: {
        tr: { title: 'Nihai Mühendislik Çözümleri', desc: 'Petrol & Gaz, Petrokimya, Rafineri, Kimya, Su ve Offshore depolama tesisleri için güvenilir, verimli ve sürdürülebilir anahtar teslim sonuçlar.' },
        en: { title: 'Final Engineering Solutions', desc: 'Reliable, efficient, and sustainable end-to-end engineering outcomes for Oil & Gas, Petrochemical, Refinery, Chemical, and Offshore storage facilities.' }
      }
    };

    const defaultBannerHTML = {
      tr: '<strong>Doğru Mühendislik &amp; Doğru Ürün:</strong> Müşteri gereksinimlerinden nihai çözüme kesintisiz, güvenilir ve sertifikalı süreç.',
      en: '<strong>The Right Engineering &amp; The Right Product:</strong> Seamless, certified, and reliable flow from technical requirements to final solutions.'
    };

    let activeNode = null;

    const renderBanner = () => {
      const lang = root.dataset.language === 'en' ? 'en' : 'tr';
      if (activeNode && nodeInfoMap[activeNode]) {
        const info = nodeInfoMap[activeNode][lang];
        bannerText.innerHTML = `<strong>${info.title}:</strong> ${info.desc}`;
      } else {
        bannerText.innerHTML = defaultBannerHTML[lang];
      }
    };

    const activateNode = nodeId => {
      activeNode = nodeId;
      flowGroups.forEach(flow => {
        if (flow.id === `flow-${nodeId}` || (nodeId === 'hub' && flow.id === 'flow-solutions')) {
          flow.classList.add('is-active');
          flow.classList.remove('is-dimmed');
        } else {
          flow.classList.remove('is-active');
          flow.classList.add('is-dimmed');
        }
      });
      nodeCards.forEach(card => card.classList.toggle('is-active', card.dataset.node === nodeId));
      if (hubCenter) hubCenter.classList.toggle('is-active', nodeId === 'hub');
      renderBanner();
    };

    const resetAll = () => {
      activeNode = null;
      flowGroups.forEach(flow => {
        flow.classList.remove('is-active', 'is-dimmed');
      });
      nodeCards.forEach(card => card.classList.remove('is-active'));
      if (hubCenter) hubCenter.classList.remove('is-active');
      renderBanner();
    };

    nodeCards.forEach(card => {
      const nodeId = card.dataset.node;
      card.addEventListener('mouseenter', () => activateNode(nodeId));
      card.addEventListener('mouseleave', resetAll);
      card.addEventListener('click', e => {
        e.stopPropagation();
        if (activeNode === nodeId) resetAll();
        else activateNode(nodeId);
      });
    });

    if (hubCenter) {
      hubCenter.addEventListener('mouseenter', () => activateNode('hub'));
      hubCenter.addEventListener('mouseleave', resetAll);
      hubCenter.addEventListener('click', e => {
        e.stopPropagation();
        if (activeNode === 'hub') resetAll();
        else activateNode('hub');
      });
    }

    document.addEventListener('click', e => {
      if (!e.target.closest('.supply-chain-wrapper')) resetAll();
    });

    document.addEventListener('nartech-language-change', renderBanner);
    renderBanner();
  };

  setupSupplyChain();
})();
