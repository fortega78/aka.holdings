/* aka.holdings · site.js · ACA WEB 2026-10-27
   One first-party script for every page: config, measurement, mobile menu, intake forms.
   Third-party analytics load ONLY when an ID is set below (decision 27-oct: GA4 + Clarity, $0). */
(function () {
  'use strict';
  var CONFIG = {
    ga4: '',            // GA4 measurement ID, e.g. 'G-XXXXXXX' (fabian@akaeditions.com) — pending, see _HACIA-CEREBRO.md
    clarity: '',        // Microsoft Clarity project ID — pending
    formEndpoint: '',   // Formspree/Tally endpoint (POST). Empty = the form composes an email instead.
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


  /* ---------- accordions: open on desktop, closed on phones ---------- */
  if (window.matchMedia('(min-width:761px)').matches) document.querySelectorAll('details.acc').forEach(function (d) { d.open = true; });

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

/* ---------- motion v1 (CEREBRO 12:06 #7): reveal, count-up, clip respects reduced motion ---------- */
(function(){
  var rm=window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  /* the demo clip loads only after the page is done, on wide screens, when motion is welcome */
  var wide=window.matchMedia('(min-width:701px)').matches;
  if(wide){document.querySelectorAll('video.vclip[data-poster]').forEach(function(v){v.poster=v.dataset.poster});}
  function loadClips(){
    if(rm||!wide)return;
    if(navigator.connection&&navigator.connection.saveData)return;
    document.querySelectorAll('video.vclip[data-webm]').forEach(function(v){
      var s1=document.createElement('source');s1.src=v.dataset.webm;s1.type='video/webm';
      var s2=document.createElement('source');s2.src=v.dataset.mp4;s2.type='video/mp4';
      v.appendChild(s1);v.appendChild(s2);v.load();v.play().catch(function(){});
    });
  }
  if(document.readyState==='complete')setTimeout(loadClips,300);else window.addEventListener('load',function(){setTimeout(loadClips,300)});
  if(rm||!('IntersectionObserver' in window))return;
  var els=document.querySelectorAll('main > section, main .wrap > section, main .wide > section, main .pj, main .ch, main .also, main .sub-pj');
  var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('rv-in');io.unobserve(e.target)}})},{rootMargin:'0px 0px -5% 0px',threshold:0});
  var vh=window.innerHeight||800;
  els.forEach(function(el){
    if(el.getBoundingClientRect().top<vh*.92)return; /* already on screen: never hidden, LCP intact */
    el.classList.add('rv');io.observe(el);
  });
  /* count-up, once, <=0.8s (home operating record) */
  var cu=document.querySelectorAll('.record b');
  if(cu.length){
    var done=false;
    var io2=new IntersectionObserver(function(es){
      es.forEach(function(e){
        if(!e.isIntersecting||done)return; done=true;
        cu.forEach(function(b){
          var txt=b.textContent;var m=txt.match(/(\d+)(?!.*\d)/);if(!m)return;
          var end=parseInt(m[1],10),idx=m.index,pre=txt.slice(0,idx),post=txt.slice(idx+m[1].length);
          var t0=null;function step(ts){if(!t0)t0=ts;var p=Math.min((ts-t0)/800,1);var v=Math.round(end*(1-Math.pow(1-p,3)));b.textContent=pre+v+post;if(p<1)requestAnimationFrame(step)}
          requestAnimationFrame(step);
        });
        io2.disconnect();
      });
    },{threshold:.4});
    io2.observe(cu[0].closest('.record'));
  }
})();
