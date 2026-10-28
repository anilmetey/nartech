/**
 * Nartech Engineering Main Application Logic
 * Accessible, fast, responsive interaction handler.
 */
try {
  sessionStorage.setItem('nartech-home-splash-seen', 'true');
} catch (err) {}

document.addEventListener('DOMContentLoaded', () => {
  // 1. Language Handling
  let activeLang = 'tr';
  try {
    activeLang = localStorage.getItem('nartech_lang') || 'tr';
  } catch (err) {}
  applyLanguage(activeLang);

  document.querySelectorAll('.lang-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      const selectedLang = btn.getAttribute('data-lang');
      if (selectedLang && selectedLang !== activeLang) {
        activeLang = selectedLang;
        try {
          localStorage.setItem('nartech_lang', activeLang);
        } catch (err) {}
        applyLanguage(activeLang);
      }
    });
  });

  // Delegated click listener for 100% reliable language toggling on all mobile and desktop devices
  document.addEventListener('click', (e) => {
    const langBtn = e.target.closest('.lang-btn');
    if (langBtn) {
      e.preventDefault();
      const selectedLang = langBtn.getAttribute('data-lang');
      if (selectedLang && selectedLang !== activeLang) {
        activeLang = selectedLang;
        try {
          localStorage.setItem('nartech_lang', activeLang);
        } catch (_) {}
        applyLanguage(activeLang);
      }
    }
  });

  function applyLanguage(lang) {
    if (!translations || !translations[lang]) return;
    activeLang = lang;
    const dict = translations[lang];

    document.documentElement.lang = lang;
    document.documentElement.setAttribute('data-active-lang', lang);

    // Update active state on buttons
    document.querySelectorAll('.lang-btn').forEach(btn => {
      if (btn.getAttribute('data-lang') === lang) {
        btn.classList.add('active');
        btn.setAttribute('aria-pressed', 'true');
      } else {
        btn.classList.remove('active');
        btn.setAttribute('aria-pressed', 'false');
      }
    });

    // Update text for all elements with data-i18n
    document.querySelectorAll('[data-i18n]').forEach(el => {
      const key = el.getAttribute('data-i18n');
      if (dict[key]) {
        el.textContent = dict[key];
      }
    });

    // Update placeholders
    document.querySelectorAll('[data-i18n-ph]').forEach(el => {
      const key = el.getAttribute('data-i18n-ph');
      if (dict[key]) {
        el.setAttribute('placeholder', dict[key]);
      }
    });

    // Explicitly toggle any data-lang-block elements
    document.querySelectorAll('[data-lang-block]').forEach(el => {
      if (el.getAttribute('data-lang-block') === lang) {
        el.style.display = '';
      } else {
        el.style.display = 'none';
      }
    });
  }

  // 2. Sticky Header Elevation on Scroll
  const header = document.querySelector('.site-header');
  if (header) {
    const updateHeaderScroll = () => {
      if (window.scrollY > 10) {
        header.classList.add('scrolled');
      } else {
        header.classList.remove('scrolled');
      }
    };
    window.addEventListener('scroll', updateHeaderScroll, { passive: true });
    updateHeaderScroll();
  }

  // 3. Mobile Navigation Drawer (Bulletproof click & touch for all mobile browsers)
  const mobileToggles = document.querySelectorAll('.mobile-nav-toggle');
  const drawerCloseBtns = document.querySelectorAll('.drawer-close-btn');
  const drawerOverlays = document.querySelectorAll('.mobile-drawer-overlay');

  function openDrawer(e) {
    if (e && typeof e.preventDefault === 'function') e.preventDefault();
    document.body.classList.add('drawer-open');
    document.documentElement.classList.add('drawer-open');
    mobileToggles.forEach(btn => btn.setAttribute('aria-expanded', 'true'));
    const firstClose = document.querySelector('.drawer-close-btn');
    if (firstClose) firstClose.focus({ preventScroll: true });
  }

  function closeDrawer(e) {
    // Do NOT preventDefault here: drawer links must still navigate when the drawer closes.
    document.body.classList.remove('drawer-open');
    document.documentElement.classList.remove('drawer-open');
    mobileToggles.forEach(btn => btn.setAttribute('aria-expanded', 'false'));
    const isLinkClick = e && e.target && e.target.closest && e.target.closest('.mobile-drawer a, .mobile-drawer [data-open-modal]');
    const firstToggle = document.querySelector('.mobile-nav-toggle');
    if (firstToggle && !isLinkClick) firstToggle.focus({ preventScroll: true });
  }

  let lastDrawerToggleTick = 0;
  function toggleDrawer(e) {
    if (e) {
      if (typeof e.preventDefault === 'function') e.preventDefault();
      if (typeof e.stopPropagation === 'function') e.stopPropagation();
    }
    const now = Date.now();
    if (now - lastDrawerToggleTick < 280) {
      return;
    }
    lastDrawerToggleTick = now;

    if (document.body.classList.contains('drawer-open')) {
      closeDrawer(e);
    } else {
      openDrawer(e);
    }
  }

  mobileToggles.forEach(btn => {
    btn.addEventListener('click', (e) => {
      toggleDrawer(e);
    });
  });

  drawerCloseBtns.forEach(btn => {
    btn.addEventListener('click', (e) => {
      if (e) {
        if (typeof e.preventDefault === 'function') e.preventDefault();
        if (typeof e.stopPropagation === 'function') e.stopPropagation();
      }
      closeDrawer(e);
    });
  });

  drawerOverlays.forEach(overlay => {
    overlay.addEventListener('click', (e) => {
      if (e) {
        if (typeof e.preventDefault === 'function') e.preventDefault();
        if (typeof e.stopPropagation === 'function') e.stopPropagation();
      }
      closeDrawer(e);
    });
  });

  document.addEventListener('click', (e) => {
    const toggle = e.target.closest('.mobile-nav-toggle');
    if (toggle) {
      toggleDrawer(e);
      return;
    }

    const closeBtn = e.target.closest('.drawer-close-btn');
    if (closeBtn) {
      if (typeof e.preventDefault === 'function') e.preventDefault();
      if (typeof e.stopPropagation === 'function') e.stopPropagation();
      closeDrawer(e);
      return;
    }

    const overlay = e.target.closest('.mobile-drawer-overlay');
    if (overlay) {
      if (typeof e.preventDefault === 'function') e.preventDefault();
      if (typeof e.stopPropagation === 'function') e.stopPropagation();
      closeDrawer(e);
      return;
    }

    const drawerLink = e.target.closest('.mobile-drawer a, .mobile-drawer [data-open-modal]');
    if (drawerLink) {
      closeDrawer(e);
    }
  });

  // 4. Modal Handling (RFQ / Inquiries)
  const openModalBtns = document.querySelectorAll('[data-open-modal]');
  const closeModalBtns = document.querySelectorAll('[data-close-modal]');
  const modalOverlay = document.querySelector('.modal-overlay');

  openModalBtns.forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      const modalId = btn.getAttribute('data-open-modal');
      const targetModal = document.getElementById(modalId);
      if (targetModal) {
        targetModal.classList.add('modal-open');
        document.body.classList.add('modal-active');
        const firstInput = targetModal.querySelector('input, select, textarea');
        if (firstInput && window.innerWidth > 768) {
          setTimeout(() => firstInput.focus({ preventScroll: true }), 50);
        }
      }
    });
  });

  closeModalBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const parentModal = btn.closest('.modal-overlay');
      if (parentModal) {
        parentModal.classList.remove('modal-open');
        document.body.classList.remove('modal-active');
      }
    });
  });

  if (modalOverlay) {
    modalOverlay.addEventListener('click', (e) => {
      if (e.target === modalOverlay) {
        modalOverlay.classList.remove('modal-open');
        document.body.classList.remove('modal-active');
      }
    });
  }

  // 5. Global Escape Key Listener for Modals and Drawers
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      if (document.body.classList.contains('drawer-open')) {
        closeDrawer();
      }
      document.querySelectorAll('.modal-overlay.modal-open').forEach(m => {
        m.classList.remove('modal-open');
      });
      document.body.classList.remove('modal-active');
    }
  });

  // 6. FAQ Accordion
  const faqQuestions = document.querySelectorAll('.faq-question');
  faqQuestions.forEach(btn => {
    btn.addEventListener('click', () => {
      const item = btn.closest('.faq-item');
      const isActive = item.classList.contains('active');

      document.querySelectorAll('.faq-item').forEach(i => {
        i.classList.remove('active');
        const q = i.querySelector('.faq-question');
        if (q) q.setAttribute('aria-expanded', 'false');
      });

      if (!isActive) {
        item.classList.add('active');
        btn.setAttribute('aria-expanded', 'true');
      }
    });
  });

  // 7. Product Filter & Search
  const filterBtns = document.querySelectorAll('.filter-btn');
  const productCards = document.querySelectorAll('.product-card[data-category]');
  const searchInput = document.querySelector('.search-input');

  function filterProducts() {
    const activeBtn = document.querySelector('.filter-btn.active');
    const selectedCategory = activeBtn ? activeBtn.getAttribute('data-filter') : 'all';
    const query = searchInput ? searchInput.value.toLowerCase().trim() : '';

    productCards.forEach(card => {
      const cardCategory = card.getAttribute('data-category');
      const title = (card.querySelector('.product-card-title')?.textContent || '').toLowerCase();
      const desc = (card.querySelector('.product-card-desc')?.textContent || '').toLowerCase();
      const specs = (card.querySelector('.product-specs-list')?.textContent || '').toLowerCase();

      const matchesCat = (selectedCategory === 'all' || cardCategory === selectedCategory);
      const matchesSearch = !query || title.includes(query) || desc.includes(query) || specs.includes(query);

      if (matchesCat && matchesSearch) {
        card.style.display = 'flex';
      } else {
        card.style.display = 'none';
      }
    });
  }

  if (filterBtns.length > 0) {
    filterBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        filterBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        filterProducts();
      });
    });
  }

  if (searchInput) {
    searchInput.addEventListener('input', filterProducts);
  }

  // Preselect product/service dropdown from URL query params (?product=... or ?service=...)
  try {
    const urlParams = new URLSearchParams(window.location.search);
    const preselectedProduct = urlParams.get('product') || urlParams.get('service');
    if (preselectedProduct) {
      document.querySelectorAll('select[name="product"]').forEach(select => {
        const option = select.querySelector('option[value="' + preselectedProduct + '"]');
        if (option) {
          select.value = preselectedProduct;
        }
      });
    }
  } catch (err) {}

  // 8. Form Validation & Submission
  const forms = document.querySelectorAll('form[data-ajax-form]');
  forms.forEach(form => {
    // Clear error state immediately when user edits field
    form.querySelectorAll('[required]').forEach(input => {
      const clearError = () => {
        if (input.value.trim()) {
          input.classList.remove('is-invalid');
          input.setAttribute('aria-invalid', 'false');
          const errorEl = input.parentElement.querySelector('.form-error-msg');
          if (errorEl) errorEl.textContent = '';
        }
      };
      input.addEventListener('input', clearError);
      input.addEventListener('change', clearError);
    });

    form.addEventListener('submit', async (e) => {
      e.preventDefault();

      // Duplicate submission lock
      if (form.getAttribute('data-submitting') === 'true') return;

      const submitBtn = form.querySelector('button[type="submit"]');
      const originalBtnHtml = submitBtn ? submitBtn.innerHTML : '';
      const statusAlert = form.querySelector('.form-status');
      const isEn = document.documentElement.lang === 'en';
      
      // Clean previous states
      if (statusAlert) {
        statusAlert.style.display = 'none';
        statusAlert.className = 'form-status alert';
      }

      // Client-side validation
      let isValid = true;
      let firstInvalidInput = null;
      const requiredInputs = form.querySelectorAll('[required]');
      requiredInputs.forEach(input => {
        const errorEl = input.parentElement.querySelector('.form-error-msg');
        if (errorEl) errorEl.setAttribute('aria-live', 'polite');

        if (!input.value.trim()) {
          isValid = false;
          if (!firstInvalidInput) firstInvalidInput = input;
          input.classList.add('is-invalid');
          input.setAttribute('aria-invalid', 'true');
          if (errorEl) {
            errorEl.textContent = isEn ? 'This field is required.' : 'Bu alan zorunludur.';
          }
        } else {
          // Email validation
          if (input.type === 'email') {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(input.value.trim())) {
              isValid = false;
              if (!firstInvalidInput) firstInvalidInput = input;
              input.classList.add('is-invalid');
              input.setAttribute('aria-invalid', 'true');
              if (errorEl) {
                errorEl.textContent = isEn ? 'Please enter a valid email address.' : 'Lütfen geçerli bir e-posta adresi giriniz.';
              }
              return;
            }
          }
          input.classList.remove('is-invalid');
          input.setAttribute('aria-invalid', 'false');
          if (errorEl) errorEl.textContent = '';
        }
      });

      // Check anti-spam honeypot
      const hp = form.querySelector('.hp-field input');
      if (hp && hp.value) {
        return;
      }

      if (!isValid) {
        if (firstInvalidInput) firstInvalidInput.focus();
        return;
      }

      // Lock form
      form.setAttribute('data-submitting', 'true');
      if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.textContent = isEn ? 'Submitting...' : 'Gönderiliyor...';
      }

      const formData = new FormData(form);
      const payload = Object.fromEntries(formData.entries());

      try {
        const response = await fetch(form.action || '/api/rfq', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
          },
          body: JSON.stringify(payload)
        });

        const resData = await response.json();

        if (response.ok && resData.success) {
          form.reset();
          if (statusAlert) {
            statusAlert.classList.add('alert-success');
            statusAlert.textContent = isEn
              ? 'Your request has been received. Our engineering department will contact you shortly.'
              : (resData.message || 'Talebiniz başarıyla alındı. Mühendislik ekibimiz en kısa sürede sizinle iletişime geçecektir.');
            statusAlert.style.display = 'flex';
          }
        } else {
          throw new Error(resData.message || (isEn ? 'Submission failed.' : 'Gönderim başarısız oldu.'));
        }
      } catch (err) {
        if (statusAlert) {
          statusAlert.classList.add('alert-error');
          statusAlert.textContent = (isEn ? 'Submission error: ' : 'Gönderim hatası: ') + err.message;
          statusAlert.style.display = 'flex';
        }
      } finally {
        form.removeAttribute('data-submitting');
        if (submitBtn) {
          submitBtn.disabled = false;
          submitBtn.innerHTML = originalBtnHtml;
        }
      }
    });
  });

  // 13. Smooth In-Page Anchor Navigation (Prevents Layout Snapping & Header Overlap)
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', (e) => {
      const targetId = anchor.getAttribute('href');
      if (!targetId || targetId === '#' || targetId === '#main-content') return;
      let targetEl;
      try {
        targetEl = document.querySelector(targetId);
      } catch (_) {
        return;
      }
      if (targetEl) {
        e.preventDefault();
        const cat = targetEl.closest('.category-block') || (targetEl.classList.contains('category-block') ? targetEl : null);
        if (cat && cat.classList.contains('is-collapsed')) {
          cat.classList.remove('is-collapsed');
          const toggleBtn = cat.querySelector('[data-category-toggle]');
          if (toggleBtn) toggleBtn.setAttribute('aria-expanded', 'true');
        }
        targetEl.scrollIntoView({ behavior: 'smooth', block: 'start' });
        try {
          history.replaceState(null, '', targetId);
        } catch (_) {}
      }
    });
  });

  // Equipment catalog navigation, including keyboard and direct-link selection.
  const windowNavItems = Array.from(document.querySelectorAll('.window-nav-item'));
  const techPanes = Array.from(document.querySelectorAll('.tech-pane'));
  const catalogNavigation = document.querySelector('.catalog-navigation');
  const storageNavigation = document.querySelector('.storage-nav-group');

  // Keep catalog index and storage group permanently open on both mobile and desktop
  if (catalogNavigation) {
    catalogNavigation.open = true;
  }
  if (storageNavigation) {
    storageNavigation.open = true;
  }

  function activateTechTab(targetId, focusTab = false) {
    const activePane = techPanes.find(pane => pane.id === targetId);
    if (!activePane) return false;

    // Keep navigation group stable — do NOT collapse or shift sidebar
    if (storageNavigation) {
      storageNavigation.open = true;
    }
    if (catalogNavigation) {
      catalogNavigation.open = true;
    }

    techPanes.forEach(pane => {
      pane.classList.toggle('active', pane === activePane);
      pane.setAttribute('tabindex', '0');
    });

    windowNavItems.forEach(item => {
      const match = item.getAttribute('data-tab-target') === targetId;
      item.classList.toggle('active', match);
      item.setAttribute('aria-selected', String(match));
      item.setAttribute('tabindex', match ? '0' : '-1');
      if (match && focusTab) {
        item.focus({ preventScroll: true });
      }
    });
    return true;
  }

  function updateTechHash(targetId) {
    // Local file previews can restrict history updates in some browsers.
    try {
      history.replaceState(null, '', '#' + targetId.replace('pane-', ''));
    } catch (_) {}
  }

  // Delegated click handler: catalog sidebar items ALWAYS respond on mobile & desktop
  document.addEventListener('click', (e) => {
    const item = e.target.closest('.window-nav-item');
    if (item) {
      e.preventDefault();
      const targetId = item.getAttribute('data-tab-target');
      if (targetId && activateTechTab(targetId)) {
        updateTechHash(targetId);
        // On mobile/tablet the sidebar is stacked above the content pane, so bring the
        // selected pane into view below the fixed header; otherwise the tap looks dead.
        if (window.matchMedia('(max-width: 991px)').matches) {
          const viewport = document.querySelector('.tech-window-viewport');
          if (viewport) {
            const headerEl = document.querySelector('.site-header');
            const offset = (headerEl ? headerEl.getBoundingClientRect().height : 76) + 12;
            const top = viewport.getBoundingClientRect().top + window.pageYOffset - offset;
            window.scrollTo({ top: Math.max(top, 0), behavior: 'smooth' });
          }
        }
      }
    }
  });

  windowNavItems.forEach((item, index) => {
    item.addEventListener('keydown', event => {
      let nextIndex;
      if (event.key === 'ArrowDown' || event.key === 'ArrowRight') {
        nextIndex = (index + 1) % windowNavItems.length;
      } else if (event.key === 'ArrowUp' || event.key === 'ArrowLeft') {
        nextIndex = (index - 1 + windowNavItems.length) % windowNavItems.length;
      } else if (event.key === 'Home') {
        nextIndex = 0;
      } else if (event.key === 'End') {
        nextIndex = windowNavItems.length - 1;
      } else {
        return;
      }
      event.preventDefault();
      const targetId = windowNavItems[nextIndex].getAttribute('data-tab-target');
      if (activateTechTab(targetId, true)) updateTechHash(targetId);
    });
  });

  function selectLinkedEquipment() {
    const hash = window.location.hash.slice(1);
    const targetId = hash.startsWith('pane-') ? hash : 'pane-' + hash;
    if (!activateTechTab(targetId) && !techPanes.some(pane => pane.classList.contains('active'))) {
      activateTechTab('pane-pvrv');
    }
  }

  if (windowNavItems.length) {
    activateTechTab('pane-pvrv');
    selectLinkedEquipment();
    window.addEventListener('hashchange', selectLinkedEquipment);
  }

  // 14. Products Catalog Collapsible Categories & Spec Drawers
  document.addEventListener('click', event => {
    const specButton = event.target.closest('.spec-drawer-toggle');
    if (specButton) {
      const drawer = specButton.closest('.spec-drawer');
      if (drawer) {
        const isOpen = !drawer.classList.contains('is-open');
        drawer.classList.toggle('is-open', isOpen);
        specButton.setAttribute('aria-expanded', String(isOpen));
        const content = drawer.querySelector('.spec-drawer-content');
        if (content) content.setAttribute('aria-hidden', String(!isOpen));
      }
      return;
    }

    const categoryButton = event.target.closest('[data-category-toggle]');
    if (categoryButton) {
      const category = categoryButton.closest('.category-block');
      if (category) {
        const isCollapsed = !category.classList.contains('is-collapsed');
        category.classList.toggle('is-collapsed', isCollapsed);
        categoryButton.setAttribute('aria-expanded', String(!isCollapsed));
        const content = category.querySelector('.category-body-collapsible');
        if (content) content.setAttribute('aria-hidden', String(isCollapsed));
      }
      return;
    }

    if (event.target.closest('#btn-expand-all') || event.target.closest('.btn-expand-all')) {
      document.querySelectorAll('.category-block').forEach(c => {
        c.classList.remove('is-collapsed');
        const b = c.querySelector('[data-category-toggle]');
        if (b) b.setAttribute('aria-expanded', 'true');
      });
      document.querySelectorAll('.spec-drawer').forEach(d => {
        d.classList.add('is-open');
        const b = d.querySelector('.spec-drawer-toggle');
        if (b) b.setAttribute('aria-expanded', 'true');
      });
      return;
    }

    if (event.target.closest('#btn-collapse-all') || event.target.closest('.btn-collapse-all')) {
      document.querySelectorAll('.spec-drawer').forEach(d => {
        d.classList.remove('is-open');
        const b = d.querySelector('.spec-drawer-toggle');
        if (b) b.setAttribute('aria-expanded', 'false');
      });
      document.querySelectorAll('.category-block').forEach(c => {
        c.classList.add('is-collapsed');
        const b = c.querySelector('[data-category-toggle]');
        if (b) b.setAttribute('aria-expanded', 'false');
      });
    }
  });

  // 15. Animated Engineering Spec Ledger Counters & Tactical Reveal
  const specsLedger = document.querySelector('.specs-ledger');
  if (specsLedger && 'IntersectionObserver' in window) {
    let hasAnimated = false;
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting && !hasAnimated) {
          hasAnimated = true;
          observer.disconnect();

          const expValEl = specsLedger.querySelector('[data-i18n="spec_exp_val"]');
          const engValEl = specsLedger.querySelector('[data-i18n="spec_eng_val"]');
          const stdValEl = specsLedger.querySelector('[data-i18n="spec_std_val"]');
          const certValEl = specsLedger.querySelector('[data-i18n="spec_cert_val"]');

          // Highlight tactile pop on standard badges
          [stdValEl, certValEl].forEach(el => {
            if (el) {
              el.style.transition = 'transform 0.5s cubic-bezier(0.16, 1, 0.3, 1)';
              el.style.transform = 'scale(1.1)';
              setTimeout(() => { el.style.transform = ''; }, 450);
            }
          });

          // Smooth counter for 10+ Yıl
          if (expValEl) {
            const isEn = (document.documentElement.lang === 'en');
            const suffix = isEn ? '+ Years' : '+ Yıl';
            const target = 10;
            const duration = 1200;
            const startTime = performance.now();

            const step = (now) => {
              const elapsed = now - startTime;
              const progress = Math.min(elapsed / duration, 1);
              const eased = progress === 1 ? 1 : 1 - Math.pow(2, -10 * progress);
              const current = Math.round(eased * target);
              expValEl.textContent = `${current}${suffix}`;
              if (progress < 1) {
                requestAnimationFrame(step);
              } else {
                expValEl.textContent = `10${suffix}`;
              }
            };
            requestAnimationFrame(step);
          }

          // Smooth counter for %100
          if (engValEl) {
            const isEn = (document.documentElement.lang === 'en');
            const target = 100;
            const duration = 1400;
            const startTime = performance.now();

            const step = (now) => {
              const elapsed = now - startTime;
              const progress = Math.min(elapsed / duration, 1);
              const eased = progress === 1 ? 1 : 1 - Math.pow(2, -10 * progress);
              const current = Math.round(eased * target);
              engValEl.textContent = isEn ? `${current}%` : `%${current}`;
              if (progress < 1) {
                requestAnimationFrame(step);
              } else {
                engValEl.textContent = isEn ? `100%` : `%100`;
              }
            };
            requestAnimationFrame(step);
          }
        }
      });
    }, { threshold: 0.2 });
    observer.observe(specsLedger);
  }

});
