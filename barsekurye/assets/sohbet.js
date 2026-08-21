/* Barse Kurye — site sohbet balonu.
   Fiyat hesaplamaz, sunucuya sorar. Tarife bu dosyada YOKTUR. */
(function () {
  'use strict';
  if (window.__barseSohbet) return;
  window.__barseSohbet = true;

  var UC = '/sohbet.php';
  var WA = 'https://wa.me/905347618388';
  var ACILIS = 'Merhaba! Barse Kurye yardımcısıyım. Fiyat, süre, bölge — ne merak ediyorsanız yazın.';
  var gecmis = [];
  try { gecmis = JSON.parse(sessionStorage.getItem('barse-sohbet') || '[]'); } catch (e) { gecmis = []; }

  var css = document.createElement('style');
  css.textContent = [
    '.bs-btn{position:fixed;right:16px;bottom:16px;z-index:9998;width:58px;height:58px;border-radius:50%;',
    'border:0;cursor:pointer;background:#1D4ED8;color:#fff;box-shadow:0 6px 22px rgba(29,78,216,.42);',
    'display:grid;place-items:center;transition:transform .18s}',
    '.bs-btn:hover{transform:scale(1.06)}.bs-btn svg{width:26px;height:26px;fill:#fff}',
    '.bs-btn[hidden]{display:none}',
    '.bs-pnl{position:fixed;right:16px;bottom:16px;z-index:9999;width:min(380px,calc(100vw - 32px));',
    'height:min(560px,calc(100vh - 32px));background:#fff;border-radius:16px;display:none;flex-direction:column;',
    'overflow:hidden;box-shadow:0 18px 50px rgba(12,22,38,.28);font:400 15px/1.55 system-ui,-apple-system,sans-serif;color:#0C1626}',
    '.bs-pnl.acik{display:flex}',
    '.bs-ust{background:#1D4ED8;color:#fff;padding:13px 15px;display:flex;align-items:center;gap:10px;flex:none}',
    '.bs-ust b{font-size:15.5px;font-weight:700}.bs-ust span{font-size:12.5px;opacity:.85;display:block}',
    '.bs-kapat{margin-left:auto;background:transparent;border:0;color:#fff;font-size:26px;line-height:1;',
    'cursor:pointer;padding:0 4px;min-width:44px;min-height:44px}',
    '.bs-akis{flex:1;overflow-y:auto;padding:15px;background:#F6F8FC;display:flex;flex-direction:column;gap:10px}',
    '.bs-m{max-width:85%;padding:10px 13px;border-radius:14px;white-space:pre-wrap;word-break:break-word}',
    '.bs-m.bot{background:#fff;border:1px solid #E3E9F2;align-self:flex-start;border-bottom-left-radius:4px}',
    '.bs-m.ben{background:#1D4ED8;color:#fff;align-self:flex-end;border-bottom-right-radius:4px}',
    '.bs-yaz{align-self:flex-start;color:#61738D;font-size:13.5px;padding:6px 2px}',
    '.bs-wa{display:inline-flex;align-items:center;gap:7px;margin-top:9px;background:#25D366;color:#fff;',
    'text-decoration:none;padding:9px 14px;border-radius:9px;font-weight:700;font-size:14px;min-height:44px;box-sizing:border-box}',
    '.bs-alt{flex:none;display:flex;gap:8px;padding:11px;border-top:1px solid #E3E9F2;background:#fff}',
    '.bs-alt input{flex:1;min-width:0;border:2px solid #E3E9F2;border-radius:10px;padding:11px 13px;',
    'font:inherit;font-size:16px;min-height:46px}',
    '.bs-alt input:focus{outline:0;border-color:#1D4ED8}',
    '.bs-gnd{flex:none;border:0;background:#1D4ED8;color:#fff;border-radius:10px;padding:0 16px;',
    'font-weight:700;cursor:pointer;min-height:46px;min-width:46px}',
    '.bs-gnd:disabled{opacity:.45;cursor:default}',
    '.bs-not{font-size:11.5px;color:#8A98AD;text-align:center;padding:0 11px 9px;background:#fff;flex:none}'
  ].join('');
  document.head.appendChild(css);

  var btn = document.createElement('button');
  btn.className = 'bs-btn';
  btn.setAttribute('aria-label', 'Sohbeti aç');
  btn.innerHTML = '<svg viewBox="0 0 24 24"><path d="M12 3C6.99 3 3 6.58 3 11c0 2.35 1.14 4.44 2.95 5.86L5 21l4.5-2.2c.8.2 1.63.3 2.5.3 5.01 0 9-3.58 9-8s-3.99-8-9-8z"/></svg>';

  var pnl = document.createElement('div');
  pnl.className = 'bs-pnl';
  pnl.setAttribute('role', 'dialog');
  pnl.setAttribute('aria-label', 'Barse Kurye sohbet');
  pnl.innerHTML =
    '<div class="bs-ust"><div><b>Barse Kurye</b><span>Genelde birkaç saniyede yanıtlar</span></div>' +
    '<button class="bs-kapat" aria-label="Kapat">&times;</button></div>' +
    '<div class="bs-akis" id="bsAkis"></div>' +
    '<div class="bs-alt"><input id="bsGirdi" type="text" maxlength="500" autocomplete="off" ' +
    'placeholder="Sorunuzu yazın…" aria-label="Mesajınız"><button class="bs-gnd" id="bsGnd">Gönder</button></div>' +
    '<div class="bs-not">Fiyatlar temsilidir. Kesin rakam WhatsApp\'tan verilir.</div>';

  document.body.appendChild(btn);
  document.body.appendChild(pnl);

  var akis  = pnl.querySelector('#bsAkis');
  var girdi = pnl.querySelector('#bsGirdi');
  var gnd   = pnl.querySelector('#bsGnd');

  function ekle(rol, metin, waMetni) {
    var d = document.createElement('div');
    d.className = 'bs-m ' + (rol === 'ben' ? 'ben' : 'bot');
    d.textContent = metin;
    if (waMetni) {
      var a = document.createElement('a');
      a.className = 'bs-wa'; a.target = '_blank'; a.rel = 'noopener';
      a.href = WA + '?text=' + encodeURIComponent(waMetni);
      a.textContent = 'WhatsApp\'tan yaz';
      d.appendChild(a);
    }
    akis.appendChild(d);
    akis.scrollTop = akis.scrollHeight;
    return d;
  }

  function ciz() {
    akis.innerHTML = '';
    if (!gecmis.length) { ekle('bot', ACILIS); return; }
    gecmis.forEach(function (m) { ekle(m.rol === 'user' ? 'ben' : 'bot', m.metin); });
  }

  function kaydet() {
    try { sessionStorage.setItem('barse-sohbet', JSON.stringify(gecmis.slice(-12))); } catch (e) {}
  }

  function ac() {
    pnl.classList.add('acik'); btn.hidden = true; ciz();
    setTimeout(function () { girdi.focus(); }, 60);
  }
  function kapat() { pnl.classList.remove('acik'); btn.hidden = false; }

  btn.addEventListener('click', ac);
  pnl.querySelector('.bs-kapat').addEventListener('click', kapat);
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && pnl.classList.contains('acik')) kapat();
  });

  var mesgul = false;
  function gonder() {
    var t = girdi.value.trim();
    if (!t || mesgul) return;
    mesgul = true; gnd.disabled = true; girdi.value = '';
    ekle('ben', t);
    gecmis.push({ rol: 'user', metin: t }); kaydet();

    var y = document.createElement('div');
    y.className = 'bs-yaz'; y.textContent = 'yazıyor…';
    akis.appendChild(y); akis.scrollTop = akis.scrollHeight;

    fetch(UC, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ mesaj: t, gecmis: gecmis.slice(-12) })
    })
      .then(function (r) { return r.json(); })
      .then(function (d) {
        y.remove();
        var c = d.cevap || 'Bir sorun oldu, WhatsApp\'tan yazar mısınız?';
        ekle('bot', c, d.fiyat ? (t + ' — fiyat sordum, kesin rakam alabilir miyim?') : null);
        gecmis.push({ rol: 'bot', metin: c }); kaydet();
      })
      .catch(function () {
        y.remove();
        ekle('bot', 'Bağlantı kurulamadı. WhatsApp\'tan yazarsanız hemen dönüş yaparız.',
             'Merhaba, siteden yazıyorum.');
      })
      .then(function () { mesgul = false; gnd.disabled = false; girdi.focus(); });
  }

  gnd.addEventListener('click', gonder);
  girdi.addEventListener('keydown', function (e) { if (e.key === 'Enter') gonder(); });
})();
