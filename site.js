/* Fabeka Lebrón — comportamiento común del sitio (v2.7)
 * Construye el menú móvil a partir de los enlaces del <nav> de cada página,
 * de modo que el menú se mantiene en un solo sitio: el propio <nav>.
 */
(function () {
  'use strict';

  /* ---------- Estilos del menú móvil ---------- */
  var css =
    '.nav-toggle{display:none;background:none;border:none;cursor:pointer;width:34px;height:26px;position:relative;padding:0;z-index:210}' +
    '.nav-toggle span{display:block;position:absolute;left:0;height:1px;width:100%;background:var(--ink);transition:transform .4s ease,opacity .3s ease,background .3s}' +
    '.nav-toggle span:nth-child(1){top:4px}.nav-toggle span:nth-child(2){top:12px}.nav-toggle span:nth-child(3){top:20px}' +
    '.nav-toggle[aria-expanded="true"] span:nth-child(1){transform:translateY(8px) rotate(45deg);background:var(--gold)}' +
    '.nav-toggle[aria-expanded="true"] span:nth-child(2){opacity:0}' +
    '.nav-toggle[aria-expanded="true"] span:nth-child(3){transform:translateY(-8px) rotate(-45deg);background:var(--gold)}' +
    '#mobile-menu{position:fixed;inset:0;z-index:190;background:var(--paper);display:flex;flex-direction:column;align-items:center;justify-content:flex-start;' +
    'opacity:0;visibility:hidden;transform:translateY(-12px);transition:opacity .45s ease,transform .45s ease,visibility .45s;padding:130px 8vw 60px;overflow-y:auto}' +
    '#mobile-menu.open{opacity:1;visibility:visible;transform:none}' +
    '#mobile-menu a{font-family:"Cormorant Garamond",serif;font-weight:300;font-size:26px;color:var(--ink);text-decoration:none;padding:11px 0;letter-spacing:.04em;transition:color .3s}' +
    '#mobile-menu a:hover,#mobile-menu a.now{color:var(--gold)}' +
    'body.no-scroll{overflow:hidden}' +
    '@media(max-width:1000px){.nav-toggle{display:block}nav .links{display:none!important}}' +
    ':focus-visible{outline:1px solid var(--gold);outline-offset:4px}' +
    '@media(prefers-reduced-motion:reduce){.rv{opacity:1!important;transform:none!important;transition:none!important}}';
  var style = document.createElement('style');
  style.textContent = css;
  document.head.appendChild(style);

  /* ---------- Menú móvil ---------- */
  var nav = document.querySelector('nav');
  var links = nav && nav.querySelector('.links');
  if (nav && links) {
    var toggle = document.createElement('button');
    toggle.className = 'nav-toggle';
    toggle.setAttribute('aria-label', 'Abrir menú');
    toggle.setAttribute('aria-controls', 'mobile-menu');
    toggle.setAttribute('aria-expanded', 'false');
    toggle.innerHTML = '<span></span><span></span><span></span>';
    nav.appendChild(toggle);

    var panel = document.createElement('div');
    panel.id = 'mobile-menu';
    Array.prototype.forEach.call(links.querySelectorAll('a'), function (a) {
      var c = a.cloneNode(true);
      c.removeAttribute('style');
      panel.appendChild(c);
    });
    document.body.appendChild(panel);

    var setOpen = function (open) {
      toggle.setAttribute('aria-expanded', String(open));
      toggle.setAttribute('aria-label', open ? 'Cerrar menú' : 'Abrir menú');
      panel.classList.toggle('open', open);
      document.body.classList.toggle('no-scroll', open);
    };
    toggle.addEventListener('click', function () {
      setOpen(toggle.getAttribute('aria-expanded') !== 'true');
    });
    panel.addEventListener('click', function (e) {
      if (e.target.tagName === 'A') setOpen(false);
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') setOpen(false);
    });
    window.addEventListener('resize', function () {
      if (window.innerWidth > 1000) setOpen(false);
    });
  }

  /* ---------- Respaldo de aparición: si el navegador no tiene IntersectionObserver ---------- */
  if (!('IntersectionObserver' in window)) {
    Array.prototype.forEach.call(document.querySelectorAll('.rv'), function (el) {
      el.classList.add('on');
    });
  }
})();
