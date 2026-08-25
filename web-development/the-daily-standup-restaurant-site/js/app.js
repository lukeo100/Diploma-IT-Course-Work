/* ===========================
   App JS - Router, Theme, Scroll Reveal, Shared Logic
   =========================== */

(function () {
  'use strict';

  /* --- Theme --- */
  const THEME_KEY = 'tds-theme';

  function getPreferredTheme() {
    const stored = localStorage.getItem(THEME_KEY);
    if (stored) return stored;
    return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  }

  function setTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem(THEME_KEY, theme);
  }

  function initTheme() {
    setTheme(getPreferredTheme());
  }

  function toggleTheme() {
    const current = document.documentElement.getAttribute('data-theme');
    const next = current === 'dark' ? 'light' : 'dark';
    setTheme(next);
  }

  /* Listen for system theme changes */
  window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', function (e) {
    if (!localStorage.getItem(THEME_KEY)) {
      setTheme(e.matches ? 'dark' : 'light');
    }
  });

  /* --- Router --- */
  const routes = {
    home: 'page-home',
    menu: 'page-menu',
    order: 'page-order',
    history: 'page-history',
    contact: 'page-contact'
  };

  let currentPage = null;

  function getRoute() {
    const hash = window.location.hash.replace('#/', '') || 'home';
    return routes[hash] ? hash : 'home';
  }

  function navigate(route) {
    if (currentPage === route) return;

    const oldPage = currentPage ? document.getElementById(routes[currentPage]) : null;
    const newPage = document.getElementById(routes[route]);

    if (!newPage) return;

    /* Animate out old page */
    if (oldPage) {
      oldPage.style.animation = 'pageOut 0.2s ease forwards';
      setTimeout(function () {
        oldPage.classList.remove('active');
        oldPage.style.animation = '';
      }, 180);
    }

    /* Animate in new page after short delay */
    setTimeout(function () {
      newPage.classList.add('active');
      window.scrollTo({ top: 0, behavior: 'instant' });
      currentPage = route;
      updateNav(route);
      triggerReveal();
    }, oldPage ? 200 : 0);

    if (!oldPage) {
      currentPage = route;
      updateNav(route);
    }
  }

  function updateNav(route) {
    var links = document.querySelectorAll('.header__nav-link');
    links.forEach(function (link) {
      link.classList.toggle('active', link.getAttribute('data-page') === route);
    });

    /* Close mobile nav */
    var nav = document.getElementById('mainNav');
    var hamburger = document.getElementById('hamburgerBtn');
    nav.classList.remove('open');
    hamburger.classList.remove('open');
  }

  /* --- Scroll Reveal --- */
  var revealObserver = null;

  function triggerReveal() {
    var elements = document.querySelectorAll('.reveal');
    if (revealObserver) {
      elements.forEach(function (el) {
        revealObserver.observe(el);
      });
    }
  }

  function initReveal() {
    revealObserver = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
          revealObserver.unobserve(entry.target);
        }
      });
    }, {
      threshold: 0.1,
      rootMargin: '0px 0px -40px 0px'
    });

    triggerReveal();
  }

  /* --- Header Scroll Effect --- */
  var header = null;

  function initHeaderScroll() {
    header = document.getElementById('header');
    window.addEventListener('scroll', function () {
      if (window.scrollY > 20) {
        header.style.boxShadow = 'var(--shadow-sm)';
      } else {
        header.style.boxShadow = 'none';
      }
    }, { passive: true });
  }

  /* --- Mobile Hamburger --- */
  function initHamburger() {
    var hamburger = document.getElementById('hamburgerBtn');
    var nav = document.getElementById('mainNav');

    hamburger.addEventListener('click', function () {
      hamburger.classList.toggle('open');
      nav.classList.toggle('open');
    });
  }

  /* --- Init --- */
  document.addEventListener('DOMContentLoaded', function () {
    initTheme();
    initReveal();
    initHeaderScroll();
    initHamburger();

    /* Theme toggle */
    document.getElementById('themeToggle').addEventListener('click', toggleTheme);

    /* Hash routing */
    window.addEventListener('hashchange', function () {
      navigate(getRoute());
    });

    /* Initial route */
    navigate(getRoute());
  });

  /* Contact form (placeholder) */
  document.addEventListener('DOMContentLoaded', function () {
    var contactForm = document.getElementById('contactForm');
    var contactToast = document.getElementById('contactToast');

    if (contactForm) {
      contactForm.addEventListener('submit', function (e) {
        e.preventDefault();
        contactToast.classList.add('show');
        contactForm.reset();
        setTimeout(function () {
          contactToast.classList.remove('show');
        }, 3000);
      });
    }
  });
})();
