/* =====================================================================
   Barse Kurye — hareket katmanı
   Kütüphane yok: IntersectionObserver + rAF, yalnızca transform/opacity.
   prefers-reduced-motion açıksa hiçbir şey çalışmaz, içerik olduğu gibi durur.
   ===================================================================== */
(function () {
  "use strict";

  var kok = document.documentElement;
  if (!kok.classList.contains("hareket")) return;      // azaltılmış hareket
  window.__hareketCalisti = true;                      // güvenlik ağını devre dışı bırakır

  /* ---------------------------------------------------------------
     1) Görünüre girince ortaya çıkma (kademeli)
     --------------------------------------------------------------- */
  var TEKIL = [".district-hero .eyebrow", ".district-hero h1", ".district-hero p.lead",
               ".district-hero .hero-ctas", ".section > .wrap > .kicker",
               ".section > .wrap > h2", ".section > .wrap > p.sub",
               ".bolge-gorsel", ".rota-not", ".cta-strip .wrap > *"];
  var KUME = [".services", ".services-4", ".why-grid", ".odak-liste", ".nokta-liste",
              ".foto-serit", ".stats-grid", ".sss-liste", ".rota-tablo", ".tarife-tablo",
              ".ikili", ".hub-groups"];

  function isaretle() {
    TEKIL.forEach(function (s) {
      Array.prototype.forEach.call(document.querySelectorAll(s), function (el) {
        el.classList.add("h-gir");
      });
    });
    KUME.forEach(function (s) {
      Array.prototype.forEach.call(document.querySelectorAll(s), function (kap) {
        var cocuk = Array.prototype.slice.call(kap.children);
        cocuk.slice(0, 10).forEach(function (el, i) {
          el.classList.add("h-gir");
          el.style.setProperty("--gecikme", (i * 55) + "ms");
        });
        cocuk.slice(10).forEach(function (el) { el.classList.add("h-gorunur"); });
      });
    });
  }

  function goster(el) {
    el.classList.add("h-gorunur");
  }

  /* ---------------------------------------------------------------
     2) Sayı sayacı (tablo rakamı kullanıldığı için genişlik oynamaz)
     --------------------------------------------------------------- */
  function sayacKur(el) {
    var metin = el.textContent.trim();
    if (metin.indexOf("/") !== -1) return null;   // "7/24" bir miktar değil, sayılmaz
    var m = metin.match(/^(\D*)(\d+)(.*)$/);
    if (!m) return null;
    var hedef = parseInt(m[2], 10);
    if (hedef < 5 || hedef > 100000) return null;
    return function () {
      var bas = performance.now(), sure = 900;
      (function adim(t) {
        var o = Math.min(1, (t - bas) / sure);
        var yumusak = 1 - Math.pow(1 - o, 3);
        el.textContent = m[1] + Math.round(hedef * yumusak) + m[3];
        if (o < 1) requestAnimationFrame(adim);
      })(bas);
    };
  }

  /* ---------------------------------------------------------------
     3) Güzergâh: yol çizilir, kurye yol boyunca ilerler
     --------------------------------------------------------------- */
  function guzergahKur() {
    var sahne = document.querySelector(".guzergah-sahne");
    if (!sahne) return;
    var yol = sahne.querySelector(".guzergah-cizgi");
    var kurye = sahne.querySelector(".guzergah-kurye");
    var duraklar = sahne.querySelectorAll(".guzergah-durak");
    if (!yol) return;

    var uzunluk = yol.getTotalLength();
    yol.style.strokeDasharray = uzunluk;
    yol.style.strokeDashoffset = uzunluk;

    // Durak işaretlerini yolun üzerine tam oturt
    Array.prototype.forEach.call(duraklar, function (d, i) {
      var oran = duraklar.length > 1 ? i / (duraklar.length - 1) : 0;
      var n = yol.getPointAtLength(uzunluk * oran);
      d.setAttribute("cx", n.x);
      d.setAttribute("cy", n.y);
    });

    var bekliyor = false;
    function guncelle() {
      bekliyor = false;
      var k = sahne.getBoundingClientRect();
      var ph = window.innerHeight;
      // bölüm ekranın altından girip ortasına gelene kadar 0 → 1
      var o = (ph - k.top) / (ph * 0.55 + k.height * 0.5);
      o = Math.max(0, Math.min(1, o));

      yol.style.strokeDashoffset = uzunluk * (1 - o);
      var n = yol.getPointAtLength(uzunluk * o);
      if (kurye) kurye.setAttribute("transform", "translate(" + n.x + "," + n.y + ")");

      Array.prototype.forEach.call(duraklar, function (d, i) {
        var esik = duraklar.length > 1 ? i / (duraklar.length - 1) : 0;
        var etiket = sahne.querySelector('.guzergah-adim li:nth-child(' + (i + 1) + ')');
        var gecti = o >= esik - 0.02;
        d.classList.toggle("gecildi", gecti);
        if (etiket) etiket.classList.toggle("gecildi", gecti);
      });
    }
    function tetikle() {
      if (!bekliyor) { bekliyor = true; requestAnimationFrame(guncelle); }
    }
    window.addEventListener("scroll", tetikle, { passive: true });
    window.addEventListener("resize", tetikle);
    guncelle();
  }

  /* ---------------------------------------------------------------
     4) Hafif derinlik: sevk fişi ve bölge görseli kaydırmada gecikir
     --------------------------------------------------------------- */
  function derinlikKur() {
    var ogeler = Array.prototype.slice.call(document.querySelectorAll("[data-derinlik]"));
    if (!ogeler.length) return;
    var bekliyor = false;
    function guncelle() {
      bekliyor = false;
      ogeler.forEach(function (el) {
        var k = el.getBoundingClientRect();
        var merkez = k.top + k.height / 2 - window.innerHeight / 2;
        var kat = parseFloat(el.getAttribute("data-derinlik")) || 0.04;
        el.style.transform = "translate3d(0," + (-merkez * kat).toFixed(1) + "px,0)";
      });
    }
    window.addEventListener("scroll", function () {
      if (!bekliyor) { bekliyor = true; requestAnimationFrame(guncelle); }
    }, { passive: true });
    guncelle();
  }

  /* ---------------------------------------------------------------
     5) Okuma ilerlemesi — üstte ince güzergâh çizgisi
     --------------------------------------------------------------- */
  function ilerlemeKur() {
    var cubuk = document.createElement("div");
    cubuk.className = "okuma-ilerleme";
    cubuk.setAttribute("aria-hidden", "true");
    document.body.appendChild(cubuk);
    var bekliyor = false;
    function guncelle() {
      bekliyor = false;
      var y = window.scrollY || window.pageYOffset;
      var toplam = document.documentElement.scrollHeight - window.innerHeight;
      cubuk.style.transform = "scaleX(" + (toplam > 0 ? Math.min(1, y / toplam) : 0) + ")";
    }
    window.addEventListener("scroll", function () {
      if (!bekliyor) { bekliyor = true; requestAnimationFrame(guncelle); }
    }, { passive: true });
    guncelle();
  }

  /* --------------------------------------------------------------- */
  function baslat() {
    isaretle();

    // Görünürlük kontrolü kaydırma tabanlı: IntersectionObserver hızlı
    // kaydırmada ögeleri atlayabiliyor ve içerik kalıcı gizli kalabiliyor.
    var bekleyen = Array.prototype.slice.call(document.querySelectorAll(".h-gir"));
    var bekliyor = false;

    function tara() {
      bekliyor = false;
      var esik = window.innerHeight * 0.92;
      for (var i = bekleyen.length - 1; i >= 0; i--) {
        var el = bekleyen[i];
        if (el.getBoundingClientRect().top < esik) {
          goster(el);
          if (el.classList.contains("stat")) {
            var b = el.querySelector("b");
            if (b && !b.dataset.sayildi) {
              var calistir = sayacKur(b);
              if (calistir) { b.dataset.sayildi = "1"; calistir(); }
            }
          }
          bekleyen.splice(i, 1);
        }
      }
      if (!bekleyen.length) {
        window.removeEventListener("scroll", tetikle);
        window.removeEventListener("resize", tetikle);
      }
    }
    function tetikle() {
      if (!bekliyor) { bekliyor = true; requestAnimationFrame(tara); }
    }

    window.addEventListener("scroll", tetikle, { passive: true });
    window.addEventListener("resize", tetikle);
    tara();

    // Sonradan eklenen ya da yeniden gösterilen içerik için:
    // BarseHareket.yenile(kapsayici) çağrısı ögeleri tekrar sıraya alır.
    window.BarseHareket = {
      yenile: function (kap) {
        var alan = kap || document;
        Array.prototype.forEach.call(alan.querySelectorAll(".h-gir"), function (el) {
          el.classList.remove("h-gorunur");
          if (bekleyen.indexOf(el) === -1) bekleyen.push(el);
        });
        window.addEventListener("scroll", tetikle, { passive: true });
        window.addEventListener("resize", tetikle);
        tetikle();
      }
    };

    guzergahKur();
    derinlikKur();
    ilerlemeKur();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", baslat);
  } else {
    baslat();
  }
})();
