/* ===========================
   Order JS - Item selection, cart, form logic
   =========================== */

(function () {
  'use strict';

  var cart = {};
  var menuData = null;

  function initOrder() {
    loadMenuForOrder().then(function (data) {
      menuData = data;
      renderOrderCategories(data.categories);
      renderOrderItems(data.items, 'all');
      populateTableNumbers(data.tables);
    });

    document.getElementById('placeOrderBtn').addEventListener('click', placeOrder);

    /* Format card number as user types */
    var cardNumber = document.getElementById('cardNumber');
    if (cardNumber) {
      cardNumber.addEventListener('input', function (e) {
        var value = e.target.value.replace(/\D/g, '');
        var formatted = value.match(/.{1,4}/g);
        e.target.value = formatted ? formatted.join(' ') : '';
      });
    }

    /* Format expiry as user types */
    var cardExpiry = document.getElementById('cardExpiry');
    if (cardExpiry) {
      cardExpiry.addEventListener('input', function (e) {
        var value = e.target.value.replace(/\D/g, '');
        if (value.length >= 2) {
          value = value.substring(0, 2) + '/' + value.substring(2);
        }
        e.target.value = value;
      });
    }
  }

  function renderOrderCategories(categories) {
    var container = document.getElementById('orderCategories');
    if (!container) return;

    /* All button */
    var allBtn = document.createElement('button');
    allBtn.className = 'menu-filter active';
    allBtn.setAttribute('data-category', 'all');
    allBtn.textContent = 'All';
    allBtn.addEventListener('click', function () {
      setActiveFilter(container, this);
      renderOrderItems(menuData.items, 'all');
    });
    container.appendChild(allBtn);

    categories.forEach(function (cat) {
      var btn = document.createElement('button');
      btn.className = 'menu-filter';
      btn.setAttribute('data-category', cat.id);
      btn.textContent = cat.icon + ' ' + cat.name;
      btn.addEventListener('click', function () {
        setActiveFilter(container, this);
        renderOrderItems(menuData.items, cat.id);
      });
      container.appendChild(btn);
    });
  }

  function setActiveFilter(container, activeBtn) {
    container.querySelectorAll('.menu-filter').forEach(function (b) {
      b.classList.remove('active');
    });
    activeBtn.classList.add('active');
  }

  function renderOrderItems(items, category) {
    var list = document.getElementById('orderItemList');
    if (!list) return;

    var filtered = category === 'all'
      ? items
      : items.filter(function (item) { return item.category === category; });

    list.innerHTML = '';

    filtered.forEach(function (item) {
      var qty = cart[item.id] || 0;
      var row = document.createElement('div');
      row.className = 'order-item-row';
      row.innerHTML =
        '<div class="order-item-row__info">' +
          '<div class="order-item-row__name">' + item.name + '</div>' +
          '<div class="order-item-row__price">$' + item.price.toFixed(2) + '</div>' +
        '</div>' +
        '<div class="order-item-row__controls">' +
          '<button class="qty-btn qty-minus" data-id="' + item.id + '">&#8722;</button>' +
          '<span class="order-item-row__qty" data-qty-id="' + item.id + '">' + qty + '</span>' +
          '<button class="qty-btn qty-plus" data-id="' + item.id + '">+</button>' +
        '</div>';

      row.querySelector('.qty-minus').addEventListener('click', function () {
        updateQty(item.id, -1);
      });

      row.querySelector('.qty-plus').addEventListener('click', function () {
        updateQty(item.id, 1);
      });

      list.appendChild(row);
    });
  }

  function updateQty(itemId, delta) {
    var current = cart[itemId] || 0;
    var next = Math.max(0, current + delta);

    if (next === 0) {
      delete cart[itemId];
    } else {
      cart[itemId] = next;
    }

    /* Update quantity display */
    var qtyEl = document.querySelector('[data-qty-id="' + itemId + '"]');
    if (qtyEl) qtyEl.textContent = next;

    updateSummary();
  }

  function updateSummary() {
    var summary = document.getElementById('orderSummary');
    var totalEl = document.getElementById('totalPrice');
    if (!summary || !menuData) return;

    var keys = Object.keys(cart);
    var total = 0;

    if (keys.length === 0) {
      summary.innerHTML = '<p class="order-empty">No items selected yet.</p>';
      totalEl.textContent = '$0.00';
      return;
    }

    var html = '';
    keys.forEach(function (id) {
      var item = menuData.items.find(function (i) { return i.id === parseInt(id); });
      if (item) {
        var lineTotal = item.price * cart[id];
        total += lineTotal;
        html +=
          '<div class="order-summary-item">' +
            '<span class="order-summary-item__name">' + item.name +
              ' <span class="order-summary-item__qty">&times; ' + cart[id] + '</span>' +
            '</span>' +
            '<span class="order-summary-item__price">$' + lineTotal.toFixed(2) + '</span>' +
          '</div>';
      }
    });

    summary.innerHTML = html;
    totalEl.textContent = '$' + total.toFixed(2);
  }

  function populateTableNumbers(tables) {
    var select = document.getElementById('tableNumber');
    if (!select || !tables) return;

    for (var i = tables.min; i <= tables.max; i++) {
      var option = document.createElement('option');
      option.value = i;
      option.textContent = 'Table ' + i;
      select.appendChild(option);
    }
  }

  function placeOrder() {
    var name = document.getElementById('customerName').value.trim();
    var table = document.getElementById('tableNumber').value;
    var cardName = document.getElementById('cardName').value.trim();
    var cardNumber = document.getElementById('cardNumber').value.trim();
    var cardExpiry = document.getElementById('cardExpiry').value.trim();
    var cardCVV = document.getElementById('cardCVV').value.trim();

    if (Object.keys(cart).length === 0) {
      alert('Please add at least one item to your order.');
      return;
    }

    if (!name) {
      alert('Please enter your name.');
      return;
    }

    if (!table) {
      alert('Please select a table.');
      return;
    }

    if (!cardName || !cardNumber || !cardExpiry || !cardCVV) {
      alert('Please fill in all payment details.');
      return;
    }

    /* Show toast */
    var toast = document.getElementById('orderToast');
    toast.classList.add('show');
    setTimeout(function () {
      toast.classList.remove('show');
    }, 3000);

    /* Reset everything */
    cart = {};
    updateSummary();
    document.getElementById('customerName').value = '';
    document.getElementById('tableNumber').value = '';
    document.getElementById('cardName').value = '';
    document.getElementById('cardNumber').value = '';
    document.getElementById('cardExpiry').value = '';
    document.getElementById('cardCVV').value = '';

    /* Reset qty displays */
    document.querySelectorAll('.order-item-row__qty').forEach(function (el) {
      el.textContent = '0';
    });
  }

  document.addEventListener('DOMContentLoaded', initOrder);
})();
