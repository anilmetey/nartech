(() => {
  const categories = [...document.querySelectorAll('.category-block')];
  const drawers = [...document.querySelectorAll('.spec-drawer')];

  const setDrawerOpen = (drawer, isOpen) => {
    drawer.classList.toggle('is-open', isOpen);
    const button = drawer.querySelector('.spec-drawer-toggle');
    const content = drawer.querySelector('.spec-drawer-content');
    if (button) {
      button.setAttribute('aria-expanded', String(isOpen));
      if (content) {
        if (!content.id) content.id = 'spec-content-' + (drawers.indexOf(drawer) + 1);
        button.setAttribute('aria-controls', content.id);
      }
    }
    if (content) content.setAttribute('aria-hidden', String(!isOpen));
  };

  const setCategoryCollapsed = (category, isCollapsed) => {
    category.classList.toggle('is-collapsed', isCollapsed);
    const button = category.querySelector('[data-category-toggle]');
    const content = category.querySelector('.category-body-collapsible');
    if (button) button.setAttribute('aria-expanded', String(!isCollapsed));
    if (content) content.setAttribute('aria-hidden', String(isCollapsed));
  };

  drawers.forEach((drawer, index) => {
    const content = drawer.querySelector('.spec-drawer-content');
    if (content && !content.id) content.id = 'spec-content-' + (index + 1);
    setDrawerOpen(drawer, drawer.classList.contains('is-open'));
  });

  document.addEventListener('click', event => {
    const specButton = event.target.closest('.spec-drawer-toggle');
    if (specButton) {
      const drawer = specButton.closest('.spec-drawer');
      if (drawer) setDrawerOpen(drawer, !drawer.classList.contains('is-open'));
      return;
    }

    const categoryButton = event.target.closest('[data-category-toggle]');
    if (categoryButton) {
      const category = categoryButton.closest('.category-block');
      if (category) setCategoryCollapsed(category, !category.classList.contains('is-collapsed'));
      return;
    }

    if (event.target.closest('#btn-expand-all')) {
      categories.forEach(category => setCategoryCollapsed(category, false));
      drawers.forEach(drawer => setDrawerOpen(drawer, true));
      return;
    }

    if (event.target.closest('#btn-collapse-all')) {
      drawers.forEach(drawer => setDrawerOpen(drawer, false));
      categories.forEach(category => setCategoryCollapsed(category, true));
    }
  });

  const expandFromHash = hash => {
    if (!hash || hash === '#') return;
    let target;
    try { target = document.getElementById(decodeURIComponent(hash.slice(1))); } catch (error) { return; }
    if (!target) return;
    const category = target.closest('.category-block');
    if (category) setCategoryCollapsed(category, false);
    const drawer = target.closest('.spec-drawer') || target.querySelector('.spec-drawer');
    if (drawer) setDrawerOpen(drawer, true);
  };

  document.querySelectorAll('.category-anchor-link').forEach(link => {
    link.addEventListener('click', () => expandFromHash(link.hash));
  });
  if (window.location.hash) expandFromHash(window.location.hash);
})();
