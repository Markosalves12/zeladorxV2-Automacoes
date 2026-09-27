(function () {
  'use strict';

  var body = document.body;
  var toggle = document.querySelector('.ops-menu-toggle');
  var overlay = document.querySelector('.ops-overlay');
  var desktop = window.matchMedia('(min-width: 992px)');
  var storageKey = 'zeladorx.sidebar.collapsed';

  if (!toggle) return;

  function syncExpandedState() {
    var expanded = desktop.matches
      ? !body.classList.contains('ops-sidebar-collapsed')
      : body.classList.contains('ops-sidebar-open');
    toggle.setAttribute('aria-expanded', expanded ? 'true' : 'false');
  }

  function restore() {
    body.classList.remove('ops-sidebar-open');
    if (desktop.matches && window.localStorage.getItem(storageKey) === '1') {
      body.classList.add('ops-sidebar-collapsed');
    } else {
      body.classList.remove('ops-sidebar-collapsed');
    }
    syncExpandedState();
  }

  toggle.addEventListener('click', function () {
    if (desktop.matches) {
      body.classList.toggle('ops-sidebar-collapsed');
      window.localStorage.setItem(storageKey, body.classList.contains('ops-sidebar-collapsed') ? '1' : '0');
    } else {
      body.classList.toggle('ops-sidebar-open');
    }
    syncExpandedState();
  });

  if (overlay) {
    overlay.addEventListener('click', function () {
      body.classList.remove('ops-sidebar-open');
      syncExpandedState();
    });
  }

  document.querySelectorAll('.ops-nav a').forEach(function (link) {
    link.addEventListener('click', function () {
      if (!desktop.matches) body.classList.remove('ops-sidebar-open');
    });
  });

  if (desktop.addEventListener) desktop.addEventListener('change', restore);
  else desktop.addListener(restore);
  restore();
}());