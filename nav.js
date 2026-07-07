/* RELICTUM — универсальное мобильное меню.
   Строит гамбургер + полноэкранную панель из существующих ссылок навигации.
   Поддерживает структуры: .nav-links/.nav-actions (V1) и .nav ul/.nav .right (V2–V4). */
(function () {
  var nav = document.querySelector('.nav');
  if (!nav || nav.querySelector('.nav-burger')) return;

  var sources = ['.nav-links a', '.nav ul a', '.nav-actions a', '.nav .right a'];
  var seen = [];
  sources.forEach(function (sel) {
    nav.querySelectorAll(sel).forEach(function (a) {
      var txt = (a.textContent || '').trim();
      if (!txt || txt === '⌕' || txt.length > 40) return;
      if (seen.some(function (s) { return s.t === txt; })) return;
      seen.push({ t: txt, href: a.getAttribute('href') || '#' });
    });
  });
  if (!seen.length) return;

  var burger = document.createElement('button');
  burger.className = 'nav-burger';
  burger.setAttribute('aria-label', 'Меню');
  burger.innerHTML = '<span></span><span></span><span></span>';
  nav.appendChild(burger);

  var drawer = document.createElement('div');
  drawer.className = 'nav-drawer';
  var inner = document.createElement('nav');
  inner.className = 'nav-drawer-inner';
  seen.forEach(function (l) {
    var a = document.createElement('a');
    a.href = l.href;
    a.textContent = l.t;
    inner.appendChild(a);
  });
  drawer.appendChild(inner);
  document.body.appendChild(drawer);

  function toggle(open) {
    document.body.classList.toggle('nav-open', open);
    burger.classList.toggle('is-open', open);
  }
  burger.addEventListener('click', function () {
    toggle(!document.body.classList.contains('nav-open'));
  });
  drawer.addEventListener('click', function (e) {
    if (e.target.tagName === 'A' || e.target === drawer) toggle(false);
  });
  window.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') toggle(false);
  });
})();
