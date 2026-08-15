/* Barse Kurye — site.js
   Mobil menü, scroll animasyonu, çerez bildirimi ve hero rota animasyonu.
   Harici kütüphane yok. */
(function () {
  'use strict';
  var azHareket = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ── Mobil menü ─────────────────────────────────────────────── */
  var btn = document.querySelector('.burger');
  var mnav = document.getElementById('mnav');
  if (btn && mnav) {
    var ac = function (open) {
      btn.setAttribute('aria-expanded', String(open));
      btn.setAttribute('aria-label', open ? 'Menüyü kapat' : 'Menüyü aç');
      mnav.classList.toggle('open', open);
      mnav.hidden = !open;
      document.body.style.overflow = open ? 'hidden' : '';
    };
    btn.addEventListener('click', function () {
      ac(btn.getAttribute('aria-expanded') !== 'true');
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && btn.getAttribute('aria-expanded') === 'true') { ac(false); btn.focus(); }
    });
    window.matchMedia('(min-width: 1060px)').addEventListener('change', function (e) {
      if (e.matches) ac(false);
    });
  }

  /* ── Scroll ile beliren bölümler ────────────────────────────── */
  var hedefler = document.querySelectorAll('.rv');
  function acA(el) { el.classList.add('in'); }
  function hepsiniAc() { hedefler.forEach(acA); }

  if (hedefler.length && !azHareket && 'IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (girisler) {
      girisler.forEach(function (g) {
        if (g.isIntersecting) { acA(g.target); io.unobserve(g.target); }
      });
    }, { rootMargin: '0px 0px -60px 0px', threshold: 0.08 });
    hedefler.forEach(function (el) { io.observe(el); });

    // Emniyet: gözlemci herhangi bir nedenle tetiklenmezse (hızlı kaydırma,
    // geri yüklenen kaydırma konumu, tarayıcı farkı) içerik gizli kalmasın.
    setTimeout(hepsiniAc, 2500);
    window.addEventListener('beforeprint', hepsiniAc);
  } else {
    hepsiniAc();
  }

  /* ── Çerez bildirimi ────────────────────────────────────────── */
  /* Not: #cerez kaldirildi; cerez onayi index icindeki #cerezKutu
     blogunda, Consent Mode guncellemesiyle birlikte yonetiliyor. */
  var cz = document.getElementById('cerez');
  if (cz) {
    var anahtar = 'barse-cerez';
    var kayit = null;
    try { kayit = localStorage.getItem(anahtar); } catch (e) {}
    if (!kayit) setTimeout(function () { cz.classList.add('show'); }, 1200);
    cz.addEventListener('click', function (e) {
      var t = e.target.closest('[data-cerez]');
      if (!t) return;
      try { localStorage.setItem(anahtar, t.getAttribute('data-cerez')); } catch (er) {}
      cz.classList.remove('show');
    });
  }

  /* ── Hero: şehir ızgarası üzerinde ilerleyen rota ────────────
     Canvas, hiçbir görsel dosyası indirmeden derinlik veriyor.
     Hareket azaltma açıksa tek kare çizilir, animasyon çalışmaz. */
  var cv = document.getElementById('rota');
  if (cv && cv.getContext) {
    var cx = cv.getContext('2d'), G = 46, yollar = [], son = 0, calisiyor = true;

    function olcekle() {
      var dpr = Math.min(window.devicePixelRatio || 1, 2);
      var r = cv.getBoundingClientRect();
      cv.width = Math.max(1, Math.floor(r.width * dpr));
      cv.height = Math.max(1, Math.floor(r.height * dpr));
      cx.setTransform(dpr, 0, 0, dpr, 0, 0);
      kur(r.width, r.height);
    }

    function kur(w, h) {
      yollar = [];
      var n = w < 700 ? 4 : 7;
      for (var i = 0; i < n; i++) {
        var yatay = Math.random() < 0.5;
        var nokta = [], adet = 3 + Math.floor(Math.random() * 3);
        var x = Math.round(Math.random() * w / G) * G;
        var y = Math.round(Math.random() * h / G) * G;
        nokta.push({ x: x, y: y });
        for (var j = 0; j < adet; j++) {
          var uz = (2 + Math.floor(Math.random() * 4)) * G * (Math.random() < 0.5 ? -1 : 1);
          if (yatay) x += uz; else y += uz;
          nokta.push({ x: x, y: y });
          yatay = !yatay;
        }
        yollar.push({ p: nokta, t: Math.random(), hiz: 0.00016 + Math.random() * 0.00022 });
      }
    }

    function konum(p, t) {
      var toplam = 0, i, uz = [];
      for (i = 0; i < p.length - 1; i++) {
        var d = Math.abs(p[i + 1].x - p[i].x) + Math.abs(p[i + 1].y - p[i].y);
        uz.push(d); toplam += d;
      }
      var hedef = t * toplam, gecen = 0;
      for (i = 0; i < uz.length; i++) {
        if (gecen + uz[i] >= hedef) {
          var k = uz[i] ? (hedef - gecen) / uz[i] : 0;
          return { x: p[i].x + (p[i + 1].x - p[i].x) * k, y: p[i].y + (p[i + 1].y - p[i].y) * k };
        }
        gecen += uz[i];
      }
      return p[p.length - 1];
    }

    function ciz(dt) {
      var w = cv.clientWidth, h = cv.clientHeight;
      cx.clearRect(0, 0, w, h);

      // ızgara
      cx.strokeStyle = 'rgba(120,165,240,0.10)';
      cx.lineWidth = 1;
      cx.beginPath();
      for (var x = 0; x <= w; x += G) { cx.moveTo(x + .5, 0); cx.lineTo(x + .5, h); }
      for (var y = 0; y <= h; y += G) { cx.moveTo(0, y + .5); cx.lineTo(w, y + .5); }
      cx.stroke();

      yollar.forEach(function (r) {
        // güzergâh
        cx.strokeStyle = 'rgba(77,139,255,0.20)';
        cx.lineWidth = 2; cx.lineCap = 'round'; cx.lineJoin = 'round';
        cx.beginPath();
        cx.moveTo(r.p[0].x, r.p[0].y);
        for (var i = 1; i < r.p.length; i++) cx.lineTo(r.p[i].x, r.p[i].y);
        cx.stroke();

        // ilerleyen kurye
        r.t += r.hiz * dt;
        if (r.t > 1) r.t = 0;
        var k = konum(r.p, r.t);
        var gr = cx.createRadialGradient(k.x, k.y, 0, k.x, k.y, 16);
        gr.addColorStop(0, 'rgba(255,175,110,0.85)');
        gr.addColorStop(1, 'rgba(255,138,31,0)');
        cx.fillStyle = gr;
        cx.beginPath(); cx.arc(k.x, k.y, 16, 0, 6.2832); cx.fill();
        cx.fillStyle = '#FFC08A';
        cx.beginPath(); cx.arc(k.x, k.y, 2.6, 0, 6.2832); cx.fill();
      });
    }

    function dongu(zaman) {
      if (!calisiyor) return;
      var dt = Math.min(zaman - son, 60); son = zaman;
      ciz(dt);
      requestAnimationFrame(dongu);
    }

    olcekle();
    var zamanlayici;
    window.addEventListener('resize', function () {
      clearTimeout(zamanlayici); zamanlayici = setTimeout(olcekle, 180);
    });

    if (azHareket) {
      ciz(0); // tek kare, hareketsiz
    } else {
      // sekme görünmezken çizim yapma
      document.addEventListener('visibilitychange', function () {
        if (document.hidden) { calisiyor = false; }
        else if (!calisiyor) { calisiyor = true; son = performance.now(); requestAnimationFrame(dongu); }
      });
      requestAnimationFrame(function (t) { son = t; dongu(t); });
    }
  }
})();
