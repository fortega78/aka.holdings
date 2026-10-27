/* aka.holdings · site.js · ACA WEB 2026-10-27
   One first-party script for every page: config, measurement, mobile menu, intake forms.
   Third-party analytics load ONLY when an ID is set below (decision 27-oct: GA4 + Clarity, $0). */
(function () {
  'use strict';
  var CONFIG = {
    ga4: '',            // GA4 measurement ID, e.g. 'G-XXXXXXX' (fabian@akaeditions.com) — pending, see _HACIA-CEREBRO.md
    clarity: '',        // Microsoft Clarity project ID — pending
    formEndpoint: '',   // Formspree/Tally endpoint (POST). Empty = the form composes an email instead.
    consultPrice: false,// true only if Instagram post P02 publishes the consultation price (decision 27-oct)
    calendar: 'https://calendar.app.google/4LDyrF8XGdGuoazj6',
    email: 'fabian@aka.holdings'
  };
  window.AKA = { config: CONFIG, track: track };

  var unit = (document.body.className.match(/\b(interior|productions|technologies|fabian|home)\b/) || [, 'home'])[1];

  /* ---------- measurement ---------- */
  window.dataLayer = window.dataLayer || [];
  function gtag() { window.dataLayer.push(arguments); }
  if (CONFIG.ga4) {
    var s = document.createElement('script'); s.async = true;
    s.src = 'https://www.googletagmanager.com/gtag/js?id=' + CONFIG.ga4; document.head.appendChild(s);
    window.gtag = gtag; gtag('js', new Date()); gtag('config', CONFIG.ga4);
  }
  if (CONFIG.clarity) {
    (function (c, l, a, r, i, t, y) { c[a] = c[a] || function () { (c[a].q = c[a].q || []).push(arguments); };
      t = l.createElement(r); t.async = 1; t.src = 'https://www.clarity.ms/tag/' + i;
      y = l.getElementsByTagName(r)[0]; y.parentNode.insertBefore(t, y); })(window, document, 'clarity', 'script', CONFIG.clarity);
  }
  function track(name, params) {
    params = params || {}; params.unit = params.unit || unit;
    if (window.gtag && CONFIG.ga4) window.gtag('event', name, params);
    else window.dataLayer.push({ event: name, params: params });
    if (window.clarity) window.clarity('event', name);
  }

  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('a'); if (!a) return;
    var h = a.getAttribute('href') || '';
    var u = a.getAttribute('data-unit') || unit;
    if (h.indexOf('calendar.app.google') > -1 || h.indexOf('calendar.google.com') > -1) track('book_click', { unit: u, place: a.getAttribute('data-place') || '' });
    else if (h.indexOf('mailto:') === 0) track('email_click', { unit: u });
    else if (h.indexOf('teherrugs.com') > -1) track('outbound_teher');
    else if (/\/cv\/.*\.pdf$/.test(h)) track('cv_download');
    else if (h.indexOf('vimeo.com') > -1) track('video_play', { video: a.getAttribute('data-video') || h });
  });
  document.querySelectorAll('video').forEach(function (v) {
    v.addEventListener('play', function () { track('video_play', { video: v.currentSrc.split('/').pop() }); }, { once: true });
  });

  /* ---------- consultation price (one switch) ---------- */
  document.querySelectorAll('[data-price]').forEach(function (el) { el.hidden = !CONFIG.consultPrice; });

  /* ---------- mobile menu ---------- */
  var btn = document.querySelector('.menu-btn'), nav = document.getElementById('site-nav');
  if (btn && nav) {
    btn.addEventListener('click', function () {
      var open = btn.getAttribute('aria-expanded') === 'true';
      btn.setAttribute('aria-expanded', String(!open)); document.body.classList.toggle('nav-open', !open);
    });
    nav.addEventListener('click', function (e) { if (e.target.closest('a')) { btn.setAttribute('aria-expanded', 'false'); document.body.classList.remove('nav-open'); } });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') { btn.setAttribute('aria-expanded', 'false'); document.body.classList.remove('nav-open'); } });
  }

  /* ---------- sticky mobile CTA: hide while the main CTA or the form is on screen ---------- */
  var bar = document.querySelector('.mbar');
  if (bar && 'IntersectionObserver' in window) {
    var watched = document.querySelectorAll('[data-hide-bar]'), visible = new Set();
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (x) { if (x.isIntersecting) visible.add(x.target); else visible.delete(x.target); });
      bar.classList.toggle('off', visible.size > 0);
    });
    watched.forEach(function (w) { io.observe(w); });
  }

  /* ---------- intake forms ---------- */
  document.querySelectorAll('form.intake').forEach(function (f) {
    var done = f.parentNode.querySelector('.intake-done');
    f.addEventListener('submit', function (e) {
      e.preventDefault();
      if (!f.reportValidity()) return;
      var data = new FormData(f), u = f.getAttribute('data-unit') || unit;
      var subject = f.getAttribute('data-subject') || ('aka.holdings · ' + u);
      var lines = [];
      data.forEach(function (v, k) { if (k.charAt(0) !== '_' && v) lines.push(k + ': ' + v); });
      track('form_submit', { unit: u });
      function finish(mode) {
        f.hidden = true; if (done) { done.hidden = false; done.setAttribute('data-mode', mode); done.focus(); }
      }
      if (CONFIG.formEndpoint) {
        data.append('_subject', subject);
        fetch(CONFIG.formEndpoint, { method: 'POST', body: data, headers: { Accept: 'application/json' } })
          .then(function (r) { if (!r.ok) throw r; finish('sent'); })
          .catch(function () { window.location.href = mailto(subject, lines); finish('mail'); });
      } else {
        window.location.href = mailto(subject, lines); finish('mail');
      }
    });
  });
  function mailto(subject, lines) {
    return 'mailto:' + CONFIG.email + '?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(lines.join('\n') + '\n\n');
  }
})();
