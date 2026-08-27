/* Barse Kurye — hızlı rota aracı
   ================================
   Sayfaya <div id="rotaArac"></div> koyup bu dosyayı çağırmak yeterli.

   Ne yapar: iki ilçe ve bir teslimat hızı seçtirir, yaklaşık yolu ve o
   hıza göre süreyi gösterir, WhatsApp mesajını rotayla doldurur.
   FİYAT GÖSTERMEZ — tarife bu dosyada yok, olmayacak da.

   Mesafe önce assets/mesafeler.json'dan (ORS'ten üretilmiş gerçek sürüş
   mesafesi) okunur; dosya yoksa kuş uçuşu tahminine düşer. */
(function(){
  var kap = document.getElementById('rotaArac');
  if (!kap) return;

  var IL = [["Adalar", 40.858, 29.123, "N"], ["Arnavutköy", 41.184, 28.74, "A"], ["Ataşehir", 40.9891, 29.1216, "N"], ["Avcılar", 40.982, 28.7107, "A"], ["Bahçelievler", 40.9989, 28.8476, "A"], ["Bakırköy", 40.9799, 28.8509, "A"], ["Bayrampaşa", 41.044, 28.9037, "A"], ["Bağcılar", 41.0369, 28.8355, "A"], ["Başakşehir", 41.0794, 28.7774, "A"], ["Beykoz", 41.1024, 29.0791, "N"], ["Beylikdüzü", 40.9917, 28.6407, "A"], ["Beyoğlu", 41.0359, 28.9711, "A"], ["Beşiktaş", 41.0631, 29.0161, "A"], ["Büyükçekmece", 41.0173, 28.5623, "A"], ["Esenler", 41.0415, 28.88, "A"], ["Esenyurt", 41.0215, 28.6896, "A"], ["Eyüpsultan", 41.0945, 28.916, "A"], ["Fatih", 41.0144, 28.948, "A"], ["Gaziosmanpaşa", 41.0673, 28.9063, "A"], ["Güngören", 41.021, 28.872, "A"], ["Kadıköy", 40.9795, 29.0564, "N"], ["Kartal", 40.8969, 29.1885, "N"], ["Kağıthane", 41.0841, 28.9763, "A"], ["Kocaeli", 40.8085, 29.485, "N"], ["Küçükçekmece", 41.0134, 28.786, "A"], ["Maltepe", 40.9334, 29.1439, "N"], ["Pendik", 40.8934, 29.2632, "N"], ["Sancaktepe", 41.0016, 29.2172, "N"], ["Sarıyer", 41.1222, 29.0354, "A"], ["Silivri", 41.0736, 28.247, "A"], ["Sultanbeyli", 40.967, 29.267, "N"], ["Sultangazi", 41.11, 28.884, "A"], ["Tuzla", 40.8439, 29.3007, "N"], ["Zeytinburnu", 41.0021, 28.9069, "A"], ["Çatalca", 41.144, 28.461, "A"], ["Çekmeköy", 41.047, 29.2065, "N"], ["Ümraniye", 41.0213, 29.1383, "N"], ["Üsküdar", 41.0266, 29.0444, "N"], ["Şile", 41.175, 29.613, "N"], ["Şişli", 41.0582, 28.9846, "A"]];

  /* Adalar'a karayolu yok; vapurla gidiliyor, mesafe hesabı anlamsız. */
  var GENIS = ['Silivri','Çatalca','Şile','Arnavutköy','Beykoz','Kocaeli','Büyükçekmece'];

  /* Sure once hizmet seviyesinden gelir: Normal'de is baska islerle
     birlestigi icin 2 km de olsa beklemesi var. Taban budur, dusmez.
     Mesafe terimi yalnizca uzun yolda tabani yukari iter - yoksa 83 km
     Sile'ye de tabani yazip tutamayacagimiz soz veriyorduk.
     Tabanlar Baris'in bildirdigi gercek sureler: Normal 2-3 saat,
     Express 45-75 dk, VIP 30-60 dk. */
  var HIZ = [
    { ad:'Normal',  aciklama:'Aynı gün içinde', sbt:[17.5,29.5], alt:2.2, ust:3.1, taban:[120,180] },
    { ad:'Express', aciklama:'Öncelikli sırada', sbt:[12.5,22.0], alt:1.6, ust:2.3, taban:[45,75] },
    { ad:'VIP',     aciklama:'Kurye başka adrese uğramaz', sbt:[10.0,18.0], alt:1.3, ust:1.9, taban:[30,60] }
  ];
  var secilenHiz = 0;

  var TABLO = null;
  if (window.fetch) {
    fetch('assets/mesafeler.json')
      .then(function(r){ return r.ok ? r.json() : null; })
      .then(function(j){ if (j && j.km) { TABLO = j.km; ciz(); } })
      .catch(function(){});
  }

  function tabloKm(x,y){
    if (!TABLO) return null;
    var k = x <= y ? x+'|'+y : y+'|'+x;
    return typeof TABLO[k] === 'number' ? TABLO[k] : null;
  }

  function km(p,q){
    var kesin = tabloKm(p[0], q[0]);
    if (kesin !== null) return kesin;
    var R = 6371, t = Math.PI/180;
    var dLat = (q[1]-p[1])*t, dLon = (q[2]-p[2])*t;
    var s = Math.sin(dLat/2)*Math.sin(dLat/2) +
            Math.cos(p[1]*t)*Math.cos(q[1]*t)*Math.sin(dLon/2)*Math.sin(dLon/2);
    var d = R*2*Math.atan2(Math.sqrt(s), Math.sqrt(1-s));
    d = d * (d < 25 ? 1.55 : 1.25);
    if (p[3] !== q[3]) d += 6;
    return Math.max(2, Math.round(d));
  }

  /* Süre mesafeyle birlikte uzuyor. Sabit "30-45 dk" yazmak 60 km'lik
     bir işte tutmayacak bir söz vermek olurdu. */
  function sure(k, h){
    var a = Math.max(h.taban[0], Math.round((h.sbt[0] + k*h.alt)/5)*5);
    var b = Math.max(h.taban[1], Math.round((h.sbt[1] + k*h.ust)/5)*5);
    /* Ikisi de saate dusuyorsa birimi bir kez yaz: "1,5 – 2 saat" */
    if (a >= 90) return saat(a) + ' – ' + saat(b) + ' saat';
    if (b >= 90) return a + ' dk – ' + saat(b) + ' saat';
    return a + ' – ' + b + ' dk';
  }
  function saat(dk){
    return (Math.round(dk/60*2)/2).toString().replace('.',',');
  }

  kap.innerHTML =
    '<div class="ra">' +
      '<p class="ra-bas">Nereden nereye?</p>' +
      '<div class="ra-alanlar">' +
        '<label class="ra-alan"><span>ALIM</span><select id="raA"></select></label>' +
        '<label class="ra-alan"><span>TESLİM</span><select id="raB"></select></label>' +
      '</div>' +
      '<div class="ra-hiz" id="raHiz" role="group" aria-label="Teslimat hızı"></div>' +
      '<div class="ra-sonuc" id="raSonuc" hidden>' +
        '<div class="ra-kutu"><small>yaklaşık yol</small><b id="raKm">—</b></div>' +
        '<div class="ra-kutu ra-sag"><small id="raHizAd">teslimat</small><b id="raSure">—</b></div>' +
      '</div>' +
      '<p class="ra-not" id="raNot"></p>' +
      '<a class="ra-cta" id="raWa" href="#" rel="noopener">Bu rota için fiyat al</a>' +
      '<p class="ra-mini">Fiyatı kurye yola çıkmadan telefonda netleştiriyoruz.</p>' +
    '</div>';

  var a = document.getElementById('raA'), b = document.getElementById('raB');
  IL.sort(function(x,y){ return x[0].localeCompare(y[0],'tr'); });
  var bos = '<option value="">Seçiniz…</option>';
  a.innerHTML = bos; b.innerHTML = bos;
  IL.forEach(function(k,i){
    var o = '<option value="'+i+'">'+k[0]+'</option>';
    a.insertAdjacentHTML('beforeend', o);
    b.insertAdjacentHTML('beforeend', o);
  });

  var hizKap = document.getElementById('raHiz');
  HIZ.forEach(function(h,i){
    var d = document.createElement('button');
    d.type = 'button';
    d.className = 'ra-h';
    d.setAttribute('aria-pressed', i === secilenHiz ? 'true' : 'false');
    d.innerHTML = '<b>'+h.ad+'</b><small>'+h.aciklama+'</small>';
    d.addEventListener('click', function(){
      secilenHiz = i;
      [].forEach.call(hizKap.children, function(c,j){
        c.setAttribute('aria-pressed', j === i ? 'true' : 'false');
      });
      ciz();
    });
    hizKap.appendChild(d);
  });

  function ciz(){
    var i = a.value, j = b.value;
    var sonuc = document.getElementById('raSonuc');
    var not = document.getElementById('raNot');
    var wa = document.getElementById('raWa');
    if (i === '' || j === '') { sonuc.hidden = true; not.textContent = ''; return; }

    var p = IL[+i], q = IL[+j], h = HIZ[secilenHiz];
    sonuc.hidden = false;
    document.getElementById('raHizAd').textContent = h.ad.toLowerCase() + ' teslimat';

    if (p[0] !== q[0] && (p[0] === 'Adalar' || q[0] === 'Adalar')) {
      document.getElementById('raKm').textContent = 'Vapurla';
      document.getElementById('raSure').textContent = 'Vapur saatine göre';
      not.textContent = 'Adalar\u0027a karayolu yok, teslimat vapurla yapılıyor. Süre ve ücret için yazın.';
    } else if (p[0] === q[0]) {
      document.getElementById('raKm').textContent = 'İlçe içi';
      document.getElementById('raSure').textContent = sure(4, h);
      not.textContent = p[0] + ' içindeki teslimatlar en kısa mesafe grubuna giriyor.';
    } else {
      var d = km(p,q);
      document.getElementById('raKm').textContent = d + ' km';
      document.getElementById('raSure').textContent = sure(d, h);
      not.textContent = p[3] !== q[3]
        ? p[0] + ' → ' + q[0] + ' yakalar arası; güzergâh köprüden geçiyor.'
        : p[0] + ' → ' + q[0] + ' aynı yakada.';
      var genis = [p[0], q[0]].filter(function(n){ return GENIS.indexOf(n) > -1; });
      if (genis.length) {
        not.textContent += ' ' + genis.join(' ve ') + ' geniş bir ilçe; rakam ilçe merkezine göre.';
      }
    }

    var mesaj = 'Merhaba, ' + p[0] + ' → ' + q[0] + ' için ' + h.ad.toLowerCase() +
                ' kurye fiyatı öğrenmek istiyorum.';
    wa.href = 'https://wa.me/905347618388?text=' + encodeURIComponent(mesaj);
  }

  a.addEventListener('change', ciz);
  b.addEventListener('change', ciz);
})();
