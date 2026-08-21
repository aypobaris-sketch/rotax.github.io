/* Barse Kurye — WhatsApp çağrı balonu.
   Sohbet botunun yerine geçti: bekleme yok, maliyet yok, doğrudan WhatsApp.
   Bot dosyaları sunucuda duruyor; geri açmak istenirse bu dosya değiştirilir. */
(function () {
  'use strict';
  if (window.__barseWa) return;
  window.__barseWa = true;

  var TEL  = '905347618388';
  var METIN = 'Merhaba, siteden yazıyorum. Bir gönderim var.';
  var SELAM = 'Merhaba! Nasıl yardımcı olabiliriz?';
  var GECIKME = 2600;      // balon kaç ms sonra çıksın
  var kapatildi = false;
  try { kapatildi = sessionStorage.getItem('barse-wa-kapali') === '1'; } catch (e) {}

  var css = document.createElement('style');
  css.textContent = [
    '.bw{position:fixed;right:16px;bottom:16px;z-index:9998;display:flex;align-items:flex-end;gap:10px}',
    '.bw-btn{position:relative;width:60px;height:60px;flex:none;border-radius:50%;border:0;cursor:pointer;',
    'background:#25D366;display:grid;place-items:center;box-shadow:0 6px 20px rgba(37,211,102,.45);',
    'text-decoration:none;transition:transform .18s ease}',
    '.bw-btn:hover,.bw-btn:focus-visible{transform:scale(1.07)}',
    '.bw-btn svg{width:33px;height:33px;fill:#fff;position:relative;z-index:2}',
    /* nabız halkası */
    '.bw-btn::before{content:"";position:absolute;inset:0;border-radius:50%;background:#25D366;',
    'animation:bwNabiz 2.4s ease-out infinite;z-index:1}',
    '@keyframes bwNabiz{0%{transform:scale(1);opacity:.55}70%{transform:scale(1.75);opacity:0}100%{opacity:0}}',
    /* konuşma balonu */
    '.bw-balon{position:relative;max-width:min(230px,calc(100vw - 110px));background:#fff;color:#0C1626;',
    'border:1px solid #E3E9F2;border-radius:14px;border-bottom-right-radius:4px;padding:11px 34px 11px 14px;',
    'font:600 14.5px/1.45 system-ui,-apple-system,sans-serif;box-shadow:0 8px 24px rgba(12,22,38,.16);',
    'opacity:0;transform:translateY(8px) scale(.96);transition:opacity .3s ease,transform .3s ease;',
    'pointer-events:none;text-decoration:none}',
    '.bw-balon.gor{opacity:1;transform:none;pointer-events:auto}',
    '.bw-balon small{display:block;font-weight:500;font-size:12.5px;color:#61738D;margin-top:2px}',
    '.bw-kapat{position:absolute;top:2px;right:2px;width:30px;height:30px;border:0;background:transparent;',
    'color:#9AA9BF;font-size:19px;line-height:1;cursor:pointer;border-radius:50%}',
    '.bw-kapat:hover{background:#F2F5F9;color:#0C1626}',
    '@media (prefers-reduced-motion:reduce){.bw-btn::before{animation:none}',
    '.bw-balon{transition:none}.bw-btn{transition:none}}'
  ].join('');
  document.head.appendChild(css);

  var sar = document.createElement('div');
  sar.className = 'bw';

  var balon = document.createElement('a');
  balon.className = 'bw-balon';
  balon.href = 'https://wa.me/' + TEL + '?text=' + encodeURIComponent(METIN);
  balon.target = '_blank';
  balon.rel = 'noopener';
  balon.innerHTML = SELAM + '<small>WhatsApp\'tan yazın, hemen dönelim</small>';

  var kapat = document.createElement('button');
  kapat.className = 'bw-kapat';
  kapat.setAttribute('aria-label', 'Kapat');
  kapat.innerHTML = '&times;';
  kapat.addEventListener('click', function (e) {
    e.preventDefault(); e.stopPropagation();
    balon.classList.remove('gor');
    try { sessionStorage.setItem('barse-wa-kapali', '1'); } catch (er) {}
  });
  balon.appendChild(kapat);

  var btn = document.createElement('a');
  btn.className = 'bw-btn';
  btn.href = 'https://wa.me/' + TEL + '?text=' + encodeURIComponent(METIN);
  btn.target = '_blank';
  btn.rel = 'noopener';
  btn.setAttribute('aria-label', 'WhatsApp ile yazın');
  btn.innerHTML = '<svg viewBox="0 0 32 32"><path d="M16 3C8.8 3 3 8.6 3 15.5c0 2.4.7 4.6 1.9 6.5L3 29l7.3-1.9c1.8.9 3.8 1.4 6 1.4' +
    ' 7.2 0 13-5.6 13-12.5S23.2 3 16 3zm7.6 17.8c-.3.9-1.7 1.7-2.4 1.8-.6.1-1.4.1-2.2-.1-.5-.2-1.2-.4-2-.8' +
    '-3.5-1.5-5.8-5-6-5.3-.2-.2-1.4-1.9-1.4-3.6 0-1.7.9-2.6 1.2-2.9.3-.3.7-.4 1-.4h.7c.2 0 .5 0 .8.6.3.7 1 2.4 1.1 2.6' +
    '.1.2.2.4 0 .6-.2.4-.4.6-.6.6-.2.2-.4.4-.2.8.2.4 1 1.6 2.1 2.6 1.4 1.3 2.6 1.7 3 1.9.4.2.6.1.8-.1' +
    '.2-.2.9-1 1.1-1.4.2-.4.5-.3.8-.2.3.1 2 .9 2.3 1.1.3.2.6.2.7.4.1.1.1.8-.2 1.6z"/></svg>';

  sar.appendChild(balon);
  sar.appendChild(btn);
  document.body.appendChild(sar);

  if (!kapatildi) {
    setTimeout(function () { balon.classList.add('gor'); }, GECIKME);
  }
})();
