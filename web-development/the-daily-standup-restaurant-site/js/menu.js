/* ===========================
   Menu JS - Render menu items from JSON
   =========================== */

(function () {
  'use strict';

  var menuData = null;

  function loadMenu() {
    fetch('data/menu.json')
      .then(function (res) { return res.json(); })
      .then(function (data) {
        menuData = data;
        renderFilters(data.categories);
        renderMenuGrid(data.items, 'all');
      });
  }

  function renderFilters(categories) {
    var container = document.getElementById('menuFilters');
    if (!container) return;

    categories.forEach(function (cat) {
      var btn = document.createElement('button');
      btn.className = 'menu-filter';
      btn.setAttribute('data-category', cat.id);
      btn.textContent = cat.icon + ' ' + cat.name;
      btn.addEventListener('click', function () {
        document.querySelectorAll('.menu-filter').forEach(function (b) {
          b.classList.remove('active');
        });
        btn.classList.add('active');
        renderMenuGrid(menuData.items, cat.id);
      });
      container.appendChild(btn);
    });

    /* All button listener */
    container.querySelector('[data-category="all"]').addEventListener('click', function () {
      document.querySelectorAll('.menu-filter').forEach(function (b) {
        b.classList.remove('active');
      });
      this.classList.add('active');
      renderMenuGrid(menuData.items, 'all');
    });
  }

  function renderMenuGrid(items, category) {
    var grid = document.getElementById('menuGrid');
    if (!grid) return;

    var filtered = category === 'all'
      ? items
      : items.filter(function (item) { return item.category === category; });

    grid.innerHTML = '';

    filtered.forEach(function (item, index) {
      var card = document.createElement('div');
      card.className = 'menu-card';
      card.style.animationDelay = (index * 0.06) + 's';

      var categoryName = '';
      if (menuData) {
        var cat = menuData.categories.find(function (c) { return c.id === item.category; });
        categoryName = cat ? cat.name : item.category;
      }

      card.innerHTML =
        (item.popular ? '<span class="menu-card__badge">Popular</span>' : '') +
        '<div class="menu-card__category">' + categoryName + '</div>' +
        '<h3 class="menu-card__name">' + item.name + '</h3>' +
        '<p class="menu-card__desc">' + item.description + '</p>' +
        '<div class="menu-card__price">$' + item.price.toFixed(2) + '</div>';

      grid.appendChild(card);
    });
  }

  /* Load menu data for use by order.js too */
  window.menuData = null;

  function loadMenuForOrder() {
    return fetch('data/menu.json')
      .then(function (res) { return res.json(); })
      .then(function (data) {
        window.menuData = data;
        return data;
      });
  }

  window.loadMenuForOrder = loadMenuForOrder;

  document.addEventListener('DOMContentLoaded', function () {
    loadMenu();
  });
})();
