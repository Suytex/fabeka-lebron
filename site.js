/* Fabeka Lebrón — comportamiento común del sitio */
(function () {
  'use strict';

  /* ---------- Menú móvil ---------- */
  var toggle = document.querySelector('.nav-toggle');
  var panel = document.getElementById('mobile-menu');

  function closeMenu() {
    if (!toggle || !panel) return;
    toggle.setAttribute('aria-expanded', 'false');
    panel.classList.remove('open');
    document.body.classList.remove('no-scroll');
  }

  if (toggle && panel) {
    toggle.addEventListener('click', function () {
      var open = toggle.getAttribute('aria-expanded') === 'true';
      toggle.setAttribute('aria-expanded', String(!open));
      panel.classList.toggle('open', !open);
      document.body.classList.toggle('no-scroll', !open);
    });

    panel.addEventListener('click', function (e) {
      if (e.target.tagName === 'A') closeMenu();
    });

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') closeMenu();
    });

    window.addEventListener('resize', function () {
      if (window.innerWidth > 1000) closeMenu();
    });
  }

  /* ---------- Reveal on scroll ---------- */
  var targets = document.querySelectorAll('.rv');
  if (!('IntersectionObserver' in window)) {
    Array.prototype.forEach.call(targets, function (el) { el.classList.add('on'); });
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add('on'); io.unobserve(e.target); }
      });
    }, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });
    Array.prototype.forEach.call(targets, function (el) { io.observe(el); });
  }
})();
