#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Barse Kurye — site derleyicisi.
Mevcut 73 sayfanın URL'lerini koruyarak yeni tasarımla yeniden üretir.
İlçe/semt içerikleri hesap.js'teki 323 gerçek koordinat noktasından türetilir.

Kullanım:  python3 build.py
Çıktı   :  cikti/  (cPanel'e yüklenecek klasör)
"""
import json, os, re, math, shutil, unicodedata, collections, html

KOK = os.path.dirname(os.path.abspath(__file__))
KAYNAK = os.path.join(KOK, 'kaynak')          # yüklenen eski site
CIKTI = os.path.join(KOK, 'cikti')

SITE = "https://barsekurye.com"
AD = "Barse Kurye"
TEL_GOSTER = "0534 761 83 88"
TEL = "+905347618388"
WA = "905347618388"
EPOSTA = "info@barsekurye.com"
ADRES = "Talatpaşa Mahallesi, Aydoğan Caddesi No:28 D:3"
ILCE_MERKEZ = "Kağıthane"
YIL = 2026

# ── FİYAT GÖRÜNÜRLÜĞÜ ────────────────────────────────────────────────────────
#  "acik"   : hesaplayıcı + tarife tablosu (formül herkese açık)
#  "sade"   : hesaplayıcı var, tarife tablosu YOK  ← önerilen
#  "kapali" : hesaplayıcı yok, "arayın fiyat verelim" bloğu
import os as _os
FIYAT_MODU = _os.environ.get("FIYAT_MODU", "sade")
FIYAT_BTN = "Fiyat Al" if FIYAT_MODU == "kapali" else "Fiyatı Hesapla"

# ─────────────────────────────────────────────────────────────── veri

def nokta_yukle():
    js = open(os.path.join(KAYNAK, 'hesap.js'), encoding='utf-8').read()
    s = js.find('const NOKTALAR')
    blok = js[s:js.find('];', s)]
    pts = []
    for m in re.finditer(r'\["([^"]+)"\s*,\s*"([^"]+)"\s*,\s*(-?[\d.]+)\s*,\s*(-?[\d.]+)\s*,\s*"([^"]*)"\]', blok):
        pts.append(dict(ad=m.group(1), ilce=m.group(2), lat=float(m.group(3)),
                        lng=float(m.group(4)), yaka=m.group(5)))
    return pts

HQ = (41.079, 28.970)

def km_hesap(a, b):
    R, rad = 6371, math.pi / 180
    dla, dlo = (b[0]-a[0])*rad, (b[1]-a[1])*rad
    h = math.sin(dla/2)**2 + math.cos(a[0]*rad)*math.cos(b[0]*rad)*math.sin(dlo/2)**2
    return 2*R*math.asin(math.sqrt(h))

def taban_fiyat(k):
    f = 380.0
    if k > 5:  f += (min(k, 25) - 5) * 14
    if k > 25: f += (k - 25) * 11
    return int(round(f / 10) * 10)

def sure_araligi(k):
    """Mesafeden gerçekçi teslim aralığı."""
    alt = max(25, int(k * 2.2) + 18)
    ust = max(45, int(k * 3.1) + 30)
    return "%d–%d dk" % (int(round(alt/5)*5), int(round(ust/5)*5))

def slugla(s):
    s = s.replace('ı','i').replace('İ','i').replace('ş','s').replace('Ş','s')
    s = s.replace('ğ','g').replace('Ğ','g').replace('ü','u').replace('Ü','u')
    s = s.replace('ö','o').replace('Ö','o').replace('ç','c').replace('Ç','c')
    s = unicodedata.normalize('NFKD', s).encode('ascii','ignore').decode().lower()
    return re.sub(r'-+','-', re.sub(r'[^a-z0-9]+','-', s)).strip('-')

def ilce_verisi(pts):
    by = collections.OrderedDict()
    for p in pts: by.setdefault(p['ilce'], []).append(p)
    out = collections.OrderedDict()
    for ilce, ps in by.items():
        la = sum(p['lat'] for p in ps)/len(ps)
        ln = sum(p['lng'] for p in ps)/len(ps)
        yk = collections.Counter(p['yaka'] for p in ps).most_common(1)[0][0]
        d = km_hesap(HQ, (la, ln)) * 1.4
        if yk != 'A': d += 6
        d = max(2, round(d))
        out[ilce] = dict(ad=ilce, yaka=('Avrupa' if yk=='A' else 'Anadolu'),
                         lat=la, lng=ln, km=d, fiyat=taban_fiyat(d),
                         sure=sure_araligi(d), noktalar=[p['ad'] for p in ps],
                         slug=slugla(ilce))
    for i, v in out.items():
        ds = sorted((km_hesap((v['lat'],v['lng']), (w['lat'],w['lng'])), j)
                    for j, w in out.items() if j != i)
        v['komsu'] = [j for _, j in ds[:4]]
    return out

# ─────────────────────────────────────────────────────── ortak parçalar

IKONLAR = """<svg width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false">
<symbol id="i-tel" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .3 1.9.6 2.8a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.2-1.2a2 2 0 0 1 2.1-.5c.9.3 1.8.5 2.8.6a2 2 0 0 1 1.7 2z"/></symbol>
<symbol id="i-wa" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2a10 10 0 0 0-8.6 15L2 22l5.2-1.4A10 10 0 1 0 12 2zm0 18.2a8.2 8.2 0 0 1-4.2-1.2l-.3-.2-3.1.8.8-3-.2-.3A8.2 8.2 0 1 1 12 20.2zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8-.2-.1-.4-.1-.6.1l-.8 1c-.2.2-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.2-.4.2-.4.6-1.2.1-.2 0-.4 0-.5L9.4 8c-.2-.5-.4-.4-.6-.4h-.5c-.2 0-.5.1-.7.3-.8.8-1 1.9-.6 3.1a11 11 0 0 0 4.6 4.9c1.7.8 2.5.8 3.4.6.5-.1 1.5-.6 1.7-1.2.2-.6.2-1.1.1-1.2z"/></symbol>
<symbol id="i-ok" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="m5 13 4 4L19 7"/></symbol>
<symbol id="i-ileri" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14m-6-6 6 6-6 6"/></symbol>
<symbol id="i-evrak" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6M9 13h6M9 17h4"/></symbol>
<symbol id="i-ilac" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10.5 20.5a5 5 0 0 1-7-7l6-6a5 5 0 0 1 7 7z"/><path d="m8.5 8.5 7 7"/></symbol>
<symbol id="i-dongu" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m17 2 4 4-4 4"/><path d="M3 11V9a4 4 0 0 1 4-4h14M7 22l-4-4 4-4"/><path d="M21 13v2a4 4 0 0 1-4 4H3"/></symbol>
<symbol id="i-koli" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 16V8a2 2 0 0 0-1-1.7l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.7l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/><path d="m3.3 7 8.7 5 8.7-5M12 22V12"/></symbol>
<symbol id="i-pin" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0z"/><circle cx="12" cy="10" r="3"/></symbol>
<symbol id="i-saat" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></symbol>
<symbol id="i-kalkan" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="m9 12 2 2 4-4"/></symbol>
<symbol id="i-terazi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3v18M7 21h10M5 7h14l3 7a4 4 0 0 1-6 0l3-7M5 7l-3 7a4 4 0 0 0 6 0L5 7z"/></symbol>
<symbol id="i-ucak" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17.8 19.2 16 11l3.5-3.5a2.1 2.1 0 0 0-3-3L13 8 4.8 6.2a.6.6 0 0 0-.5.2l-.9.9a.6.6 0 0 0 .2 1l5 2.4-2.6 2.6-2.1-.4a.6.6 0 0 0-.5.2l-.6.6a.6.6 0 0 0 .2 1l2.7 1.3 1.3 2.7a.6.6 0 0 0 1 .2l.6-.6a.6.6 0 0 0 .2-.5l-.4-2.1L11 16l2.4 5a.6.6 0 0 0 1 .2l.9-.9a.6.6 0 0 0 .2-.5z"/></symbol>
<symbol id="i-moto" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="5.5" cy="17.5" r="3.5"/><circle cx="18.5" cy="17.5" r="3.5"/><path d="M15 6h4l2 5M5.5 17.5 9 9h6l2 8.5M9 9 7 6H4"/></symbol>
<symbol id="i-menu" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M4 7h16M4 12h16M4 17h16"/></symbol>
<symbol id="i-kapat" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M6 6l12 12M18 6 6 18"/></symbol>
<symbol id="i-yildiz" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m12 3 2.7 5.6 6.1.9-4.4 4.3 1 6.1-5.4-2.9-5.4 2.9 1-6.1L3.2 9.5l6.1-.9z"/></symbol>
</svg>"""

MENU = [("index.html","Ana Sayfa"),("moto-kurye.html","Moto Kurye"),("acil-kurye.html","Acil Kurye"),
        ("eczane-kurye.html","Eczane Kurye"),("kurumsal-kurye.html","Kurumsal"),
        ("fiyat-hesaplama.html","Fiyat Hesapla" if FIYAT_MODU!="kapali" else "Fiyat"),("istanbul-ici-kurye.html","Bölgeler"),
        ("hakkimizda.html","Hakkımızda")]

def header(aktif):
    nav = "".join('<a href="%s"%s>%s</a>' % (u, ' aria-current="page"' if u == aktif else '', a)
                  for u, a in MENU)
    mnav = "".join('<a href="%s"%s>%s <svg width="16" height="16" aria-hidden="true"><use href="#i-ileri"/></svg></a>'
                   % (u, ' aria-current="page"' if u == aktif else '', a) for u, a in MENU)
    return f"""<header class="hdr">
<div class="wrap hdr-in">
<a class="logo" href="index.html"><svg aria-hidden="true"><use href="#i-moto"/></svg>Barse<i>Kurye</i></a>
<nav class="nav" aria-label="Ana menü">{nav}</nav>
<a class="btn btn-1 hdr-cta" href="tel:{TEL}"><svg aria-hidden="true"><use href="#i-tel"/></svg>{TEL_GOSTER}</a>
<button class="burger" type="button" aria-expanded="false" aria-controls="mnav" aria-label="Menüyü aç">
<svg class="m" aria-hidden="true"><use href="#i-menu"/></svg><svg class="x" aria-hidden="true"><use href="#i-kapat"/></svg>
</button>
</div>
<div class="mnav" id="mnav" hidden><nav aria-label="Mobil menü">{mnav}</nav>
<div class="btns"><a class="btn btn-1 btn-block" href="tel:{TEL}"><svg aria-hidden="true"><use href="#i-tel"/></svg>{TEL_GOSTER}</a></div>
</div>
</header>"""

def cta_band(baslik="Gönderiniz bekliyor mu?", metin="Tek arama yeterli. En yakın kuryeyi yönlendirelim, siz işinize dönün."):
    return f"""<section class="sec dark cta">
<div class="wrap">
<h2>{baslik}</h2>
<p>{metin}</p>
<div class="btns">
<a class="btn btn-2 btn-lg" href="tel:{TEL}"><svg aria-hidden="true"><use href="#i-tel"/></svg>{TEL_GOSTER}</a>
<a class="btn btn-g btn-lg" href="https://wa.me/{WA}" rel="noopener"><svg aria-hidden="true"><use href="#i-wa"/></svg>WhatsApp</a>
</div>
</div>
</section>"""

def footer(ilceler):
    pop = ["Kadıköy","Şişli","Beşiktaş","Üsküdar","Kağıthane","Ataşehir","Bakırköy","Ümraniye"]
    bl = "".join('<li><a href="%s-kurye.html">%s Kurye</a></li>' % (ilceler[i]['slug'], i)
                 for i in pop if i in ilceler)
    return f"""<footer class="ftr">
<div class="wrap">
<div class="ftr-g">
<div>
<a class="logo" href="index.html"><svg aria-hidden="true"><use href="#i-moto"/></svg>Barse<i style="color:#FFB877">Kurye</i></a>
<p>İstanbul'un 39 ilçesinde 7/24 moto kurye. Evrak, ilaç ve kurumsal gönderiler; Türkiye geneline havayolu ve şehirlerarası taşıma.</p>
<p style="margin-top:16px"><a href="tel:{TEL}" style="font-size:1.15rem;font-weight:700;color:#fff;text-decoration:none">{TEL_GOSTER}</a></p>
<p style="margin-top:6px"><a href="mailto:{EPOSTA}">{EPOSTA}</a></p>
</div>
<div><h3>Hizmetler</h3><ul>
<li><a href="moto-kurye.html">Moto Kurye</a></li>
<li><a href="acil-kurye.html">Acil Kurye</a></li>
<li><a href="eczane-kurye.html">Eczane Kurye</a></li>
<li><a href="kurumsal-kurye.html">Kurumsal Kurye</a></li>
<li><a href="7-24-kurye.html">7/24 Kurye</a></li>
<li><a href="istanbul-ici-kurye.html">İstanbul İçi Kurye</a></li>
</ul></div>
<div><h3>Bölgeler</h3><ul>{bl}
<li><a href="istanbul-ici-kurye.html">Tüm ilçeler</a></li>
</ul></div>
<div><h3>Kurumsal</h3><ul>
<li><a href="hakkimizda.html">Hakkımızda</a></li>
<li><a href="fiyat-hesaplama.html">Fiyat Hesaplama</a></li>
<li><a href="gizlilik-politikasi.html">Gizlilik Politikası</a></li>
<li><a href="kvkk.html">KVKK Aydınlatma Metni</a></li>
</ul>
<h3 style="margin-top:26px">Adres</h3>
<p>{ADRES}<br>{ILCE_MERKEZ} / İstanbul</p>
</div>
</div>
<div class="ftr-b"><span>&copy; {YIL} {AD}. Tüm hakları saklıdır.</span><span>7 gün 24 saat açık</span></div>
</div>
</footer>"""

ALT_CUBUK = f"""<a class="wafloat" href="https://wa.me/{WA}" rel="noopener" aria-label="WhatsApp ile yazın"><svg aria-hidden="true"><use href="#i-wa"/></svg></a>
<div class="callbar">
<a class="btn btn-1" href="tel:{TEL}"><svg aria-hidden="true"><use href="#i-tel"/></svg>Hemen Ara</a>
<a class="btn btn-2" href="https://wa.me/{WA}" rel="noopener"><svg aria-hidden="true"><use href="#i-wa"/></svg>WhatsApp</a>
</div>
<div class="cookie" id="cerez" role="region" aria-label="Çerez bildirimi">
<p>Bu sitede deneyimi geliştirmek için çerez kullanıyoruz. Ayrıntılar <a href="gizlilik-politikasi.html">Gizlilik Politikası</a> sayfasında.</p>
<div class="btns"><button class="btn btn-o" type="button" data-cerez="ret">Reddet</button><button class="btn btn-1" type="button" data-cerez="kabul">Kabul Et</button></div>
</div>"""

def sayfa(dosya, baslik, aciklama, govde, aktif="", ilceler=None, ekjsonld="", ekjs=""):
    kanonik = f"{SITE}/" if dosya == "index.html" else f"{SITE}/{dosya}"
    return f"""<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{baslik}</title>
<meta name="description" content="{aciklama}">
<link rel="canonical" href="{kanonik}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="author" content="{AD}">
<meta property="og:type" content="website">
<meta property="og:locale" content="tr_TR">
<meta property="og:site_name" content="{AD}">
<meta property="og:title" content="{baslik}">
<meta property="og:description" content="{aciklama}">
<meta property="og:url" content="{kanonik}">
<meta property="og:image" content="{SITE}/og-image.jpg">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#0A1422">
<link rel="icon" href="favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="favicon-32x32.png">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Manrope:wght@600;700;800&family=Source+Sans+3:wght@400;600;700&display=swap">
<link rel="stylesheet" href="assets/barse.css">
<script>document.documentElement.className+=" js";</script>
</head>
<body>
<a class="skip" href="#icerik">İçeriğe geç</a>
{IKONLAR}
{header(aktif)}
<main id="icerik">
{govde}
</main>
{footer(ilceler or {})}
{ALT_CUBUK}
{ekjsonld}
<script src="assets/site.js" defer></script>
{ekjs}
</body>
</html>"""

# ─────────────────────────────────────────────────────────── içerikler

HIZLAR = [
    ("Ekonomik", "Normal Kurye", "90 dk – 2 saat",
     "Gün içinde teslim edilmesi gereken evrak ve paketler için planlı, en uygun fiyatlı seçenek.", False),
    ("Öncelikli", "Express Kurye", "45–60 dakika",
     "Gönderiniz başka paketlerle birleştirilmez, öncelikli olarak yönlendirilir.", True),
    ("En hızlı", "VIP Kurye", "30–45 dakika",
     "Gönderinize özel kurye atanır; başka adrese uğramadan doğrudan teslimata gider.", False),
]

def hiz_bloklari():
    p = []
    for lbl, ad, sure, met, hot in HIZLAR:
        p.append(f"""<article class="tier{' hot' if hot else ''}"{' data-tag="En çok tercih edilen"' if hot else ''}>
<div class="lbl">{lbl}</div><h3>{ad}</h3>
<div class="time">{sure}</div><p>{met}</p>
<a class="btn {'btn-1' if hot else 'btn-o'}" href="fiyat-hesaplama.html">{FIYAT_BTN}</a>
</article>""")
    return '<div class="tiers rv">' + "".join(p) + '</div>'

GORSEL_W, GORSEL_H = 1408, 768

def gorsel(yol, alt, sinif="", w=GORSEL_W, h=GORSEL_H, oncelik=False):
    yukleme = '' if oncelik else ' loading="lazy" decoding="async"'
    c = ' class="%s"' % sinif if sinif else ''
    return f'<img src="images/{yol}" alt="{alt}" width="{w}" height="{h}"{yukleme}{c}>'

HIZMET_KART = [
 ("i-evrak","","Evrak ve Dosya Kurye","Sözleşme, fatura, ihale dosyası ve resmi evrakların şehir içi aynı gün teslimi.","moto-kurye.html","01-ofis/kurye-cikis-hazirlik.webp","Kurye çantasına evrak yerleştirirken"),
 ("i-ilac","amber","Eczane ve İlaç Kurye","Eczaneler ve hastalar için öncelikli ilaç teslimatı. Sabit 400 ₺ tarife.","eczane-kurye.html","06-hizmet/eczane-kurye-medikal.webp","Eczaneden alınan ilaç paketi kuryeye teslim edilirken"),
 ("i-dongu","","Kurumsal Düzenli Kurye","Her gün belirli saatte gelen sabit kurye, aylık faturalı çalışma düzeni.","kurumsal-kurye.html","03-teslimat/kurumsal-ofis-teslimat.webp","Ofis resepsiyonunda kurumsal gönderi teslimi"),
 ("i-saat","amber","Acil ve VIP Kurye","Bekleyemeyen gönderiler için gönderiye özel, duraksız motosiklet servisi.","acil-kurye.html","06-hizmet/vip-kurye-ozel-teslimat.webp","VIP kurye gönderiyi doğrudan teslim ederken"),
 ("i-koli","","7/24 ve Gece Kurye","Mesai dışı, gece ve hafta sonu teslimat. Nöbetçi eczaneler ve 7/24 ofisler için.","7-24-kurye.html","04-gece/gece-plaza-levent-teslimat.webp","Gece saatinde plaza girişinde kurye teslimatı"),
 ("i-ucak","","Havayolu ve Şehirlerarası","Türkiye geneline uçak kargo ile gönderi ve gümrük evrak taşıma.","istanbul-ici-kurye.html","03-teslimat/depo-fabrika-teslimat.webp","Depo çıkışında sevkiyat için hazırlanan gönderiler"),
]

def hizmet_kartlari():
    p = []
    for ik, mod, ad, met, url, img, alt in HIZMET_KART:
        p.append(f"""<article class="card pcard link">
{gorsel(img, alt)}
<div class="body">
<h3>{ad}</h3><p>{met}</p>
<a class="go" href="{url}">Detaylar <svg aria-hidden="true"><use href="#i-ileri"/></svg></a>
</div>
</article>""")
    return '<div class="grid g3 rv">' + "".join(p) + '</div>'

def sss_blok(sorular, sinif="sec sec--tint"):
    ic = "".join(f"""<details><summary>{s}</summary><div class="b"><p>{c}</p></div></details>"""
                 for s, c in sorular)
    ld = json.dumps({"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
        {"@type":"Question","name":s,"acceptedAnswer":{"@type":"Answer","text":re.sub(r'<[^>]+>','',c)}}
        for s, c in sorular]}, ensure_ascii=False)
    blok = f"""<section class="{sinif}"><div class="wrap">
<div class="head"><span class="kicker">Sık sorulanlar</span><h2>Merak edilenler</h2></div>
<div class="faq rv">{ic}</div></div></section>"""
    return blok, f'<script type="application/ld+json">{ld}</script>'

TARIFE_SATIR = [
    ("İlk 5 km (taban ücret)", "380 ₺"),
    ("5 – 25 km arası", "km başına +14 ₺"),
    ("25 km üzeri", "km başına +11 ₺"),
    ("Eczane kurye (öncelikli)", "sabit 400 ₺"),
    ("Al-ver — gidiş dönüş, kurye bekler", "×1,7"),
    ("Ek durak / uğrama", "+150 ₺"),
    ("Gece tarifesi (20:00 – 06:00)", "+100 ₺"),
    ("Cumartesi ve Pazar", "+100 ₺"),
]

FIYAT_UNSUR = """<ul class="rv" style="color:var(--muted);display:grid;gap:12px;padding-left:1.2em;font-size:.96rem">
<li>İki nokta arasındaki <strong>yol mesafesi</strong> — yakalar arasında köprü payı eklenir</li>
<li><strong>Teslimat hızı</strong> — Normal, Express veya VIP</li>
<li><strong>Paket boyutu</strong> — zarf ve dosyada ek ücret yok</li>
<li><strong>Al-ver</strong> (kurye bekler) ve <strong>ek durak</strong> talepleri</li>
<li><strong>Saat ve gün</strong> — gece ve hafta sonu tarife farkı</li>
<li><strong>Eczane teslimatı</strong> sabit tarifelidir, mesafe farkı uygulanmaz</li>
</ul>"""

def tarife_tablo():
    r = '<div class="r h"><span>Kalem</span><b>Tutar</b></div>'
    r += "".join(f'<div class="r"><span>{a}</span><b>{b}</b></div>' for a, b in TARIFE_SATIR)
    return f'<div class="tarife rv">{r}</div>'

HESAPLAYICI = """<div class="calc rv">
<div class="calc-step"><span class="no">1</span><span class="ttl">Güzergâh</span></div>
<div class="row" id="satirNereden">
<label for="nereden">Alım noktası</label>
<div class="ara"><input type="text" id="nereden" autocomplete="off" placeholder="Mahalle veya semt yazın (örn. Levent)">
<div class="oneri-liste" id="oneri1" hidden></div></div>
</div>
<div class="row">
<label for="nereye">Teslim noktası</label>
<div class="ara"><input type="text" id="nereye" autocomplete="off" placeholder="Mahalle veya semt yazın (örn. Kadıköy)">
<div class="oneri-liste" id="oneri2" hidden></div></div>
</div>
<div class="calc-step"><span class="no">2</span><span class="ttl">Teslimat türü</span></div>
<div class="row"><label for="hiz">Teslimat hızı</label>
<select id="hiz">
<option value="1">Normal — 90 dk - 2 saat</option>
<option value="1.25">Express — 45-60 dakika</option>
<option value="1.6">VIP — 30-45 dakika (özel kurye)</option>
</select></div>
<div class="row"><label for="boyut">Paket boyutu</label>
<select id="boyut">
<option value="1">Zarf / Dosya — ek ücret yok</option>
<option value="1.10">Küçük paket (ayakkabı kutusu boyutu)</option>
<option value="1.21">Orta paket (sırt çantası boyutu)</option>
<option value="1.33">Büyük paket (koli)</option>
<option value="1.46">Çanta üstü — hacimli gönderi</option>
</select></div>
<div class="hesap-ekler">
<label class="one"><input type="checkbox" id="eczane"> Eczane Kurye — öncelikli sipariş (sabit 400 ₺)</label>
<label><input type="checkbox" id="alver"> Al-ver (gidiş-dönüş, kurye bekler)</label>
<label><input type="checkbox" id="durak"> Ek durak / uğrama (+150 ₺)</label>
</div>
<button type="button" class="btn btn-1 btn-block btn-lg" id="hesaplaBtn">Fiyatı Hesapla</button>
<div class="hesap-uyari" id="uyari" hidden>Lütfen listeden alım ve teslim noktası seçin.</div>
<div class="zam-bilgi" id="zamBilgi" hidden></div>
<div class="hesap-sonuc" id="sonuc" hidden>
<div class="sonuc-mesafe" id="mesafe"></div>
<div class="sonuc-fiyat" id="fiyatTutar"></div>
<div class="sonuc-kiyas" id="kiyas" hidden></div>
<p class="sonuc-not">Bu tutar tahmini bir hesaptır. Trafik, tam adres ve gönderi içeriğine göre kesin fiyat teyit edilir.</p>
<div class="btns" style="margin-top:20px">
<a id="waLink" class="btn btn-2" href="https://wa.me/%s" target="_blank" rel="noopener"><svg aria-hidden="true"><use href="#i-wa"/></svg>WhatsApp ile Talep Et</a>
<a class="btn btn-o" href="tel:%s"><svg aria-hidden="true"><use href="#i-tel"/></svg>Hemen Ara</a>
</div>
<button type="button" class="hesap-sifirla" id="sifirlaBtn">Yeni hesaplama yap</button>
</div>
</div>""" % (WA, TEL)

# ─────────────────────────────────────────────────────────── ANA SAYFA

def fiyat_bolumu():
    """Ana sayfadaki fiyat bölümü — FIYAT_MODU'na göre değişir."""
    if FIYAT_MODU == "kapali":
        return f"""<section class="sec" id="fiyat">
<div class="wrap">
<div class="head"><span class="kicker">Fiyat</span><h2>Gönderiniz için net fiyat alın</h2>
<p>Alım ve teslim adresini iletin, dakikalar içinde kesin fiyatı söyleyelim. Tutar mesafeye, aciliyete ve gönderi türüne göre belirlenir.</p></div>
<div class="btns">
<a class="btn btn-1 btn-lg" href="tel:{TEL}"><svg aria-hidden="true"><use href="#i-tel"/></svg>Hemen Ara — {TEL_GOSTER}</a>
<a class="btn btn-o btn-lg" href="https://wa.me/{WA}" rel="noopener"><svg aria-hidden="true"><use href="#i-wa"/></svg>WhatsApp ile Sor</a>
</div>
</div>
</section>"""
    yan = (f'''<div>
<h3 style="margin-bottom:16px">Tarife kalemleri</h3>
{tarife_tablo()}
<p class="sonuc-not" style="margin-top:14px">Tarife İstanbul içi motosiklet teslimatı içindir. Şehirlerarası ve havayolu gönderilerde fiyat telefonla verilir.</p>
</div>''' if FIYAT_MODU == "acik" else f'''<div>
<h3 style="margin-bottom:16px">Fiyat neye göre belirleniyor?</h3>
<ul style="color:var(--muted);display:grid;gap:10px;padding-left:1.2em">
<li>İki nokta arasındaki <strong>yol mesafesi</strong></li>
<li>Seçtiğiniz <strong>teslimat hızı</strong> — Normal, Express, VIP</li>
<li><strong>Paket boyutu</strong> — zarf ve dosyada ek ücret yok</li>
<li><strong>Al-ver</strong> ve <strong>ek durak</strong> talepleri</li>
<li>Gece ve hafta sonu <strong>tarife farkı</strong></li>
</ul>
<div class="note" style="margin-top:22px">
<p>Yakalar arası geçişlerde güzergâha köprü payı eklenir. <strong>Eczane teslimatları sabit tarifelidir</strong>; mesafe ve saat farkı uygulanmaz.</p>
</div>
<p class="sonuc-not" style="margin-top:14px">Şehirlerarası ve havayolu gönderilerde fiyat telefonla verilir.</p>
</div>''')
    return f"""<section class="sec" id="fiyat">
<div class="wrap">
<div class="head"><span class="kicker">Fiyat</span><h2>Gönderiniz için tahmini tutarı hemen görün</h2>
<p>Alım ve teslim noktasını seçin, tarife anında hesaplansın. Kesin fiyat telefonda teyit edilir.</p></div>
<div class="grid g2" style="align-items:start">
{HESAPLAYICI}
{yan}
</div>
</div>
</section>"""

def anasayfa(ilceler):
    av = [i for i in ilceler.values() if i['yaka'] == 'Avrupa']
    an = [i for i in ilceler.values() if i['yaka'] == 'Anadolu']
    def cip(lst):
        return "".join('<li><a href="%s-kurye.html">%s</a></li>' % (i['slug'], i['ad'])
                       for i in sorted(lst, key=lambda x: x['km']))
    sss = [
      ("Kurye ne kadar sürede geliyor?",
       "Talebiniz alındığı anda size en yakın kurye yönlendirilir. Aynı bölge içindeki gönderilerde teslimat çoğunlukla 30–60 dakikada tamamlanır; yakalar arası gönderilerde süre trafiğe göre 90 dakikayı bulabilir. Express ve VIP taleplerde kurye başka adrese uğramaz."),
      ("Fiyatı önceden öğrenebilir miyim?",
       "Evet. Fiyat Hesaplama sayfasından alım ve teslim noktasını seçtiğinizde tahmini tutarı anında görürsünüz. Taban ücret ilk 5 km için 380 ₺'dir, sonrasında kilometre başına eklenir. Kesin fiyatı telefonda, kurye yola çıkmadan teyit ediyoruz."),
      ("Gece ve hafta sonu çalışıyor musunuz?",
       "Evet, 7 gün 24 saat. Gece 20:00 – 06:00 arası ve hafta sonu teslimatlarda tarifeye 100 ₺ fark eklenir. Nöbetçi eczane teslimatları gece de yapılır."),
      ("Eczane kurye nasıl çalışıyor?",
       "Eczane teslimatları öncelikli sipariş olarak işleme alınır ve sabit 400 ₺ tarifeyle taşınır. Mesafe, saat ve hafta sonu farkı uygulanmaz."),
      ("Al-ver (gidiş-dönüş) hizmeti nedir?",
       "Kurye gönderiyi teslim ettikten sonra adreste bekler ve karşılığında alacağı evrak veya paketle size döner. Tek yön tarifenin 1,7 katı olarak fiyatlanır."),
      ("İstanbul dışına gönderi yapıyor musunuz?",
       "Evet. Türkiye geneline havayolu kargo ve şehirlerarası taşıma yapıyoruz; ayrıca gümrük evrak taşıma hizmetimiz var. Bu gönderiler için telefonla fiyat veriyoruz."),
      ("Hangi gönderileri taşımıyorsunuz?",
       "Motosiklet çantasına sığmayan hacimli yükler, uygun ambalajı bulunmayan kırılgan ürünler ve yasal olarak taşınması yasak maddeler taşınmaz. Emin değilseniz aramadan önce gönderinin ölçüsünü belirtin."),
    ]
    sssblok, sssld = sss_blok(sss)

    govde = f"""<section class="hero">
<canvas id="rota" aria-hidden="true"></canvas>
<div class="wrap hero-in">
<div>
<p class="live"><i></i> Şu anda kurye alımı açık · 7 gün 24 saat</p>
<h1>İstanbul'un 39 ilçesinde <em>moto kurye</em>, gönderiniz aynı gün yerinde</h1>
<p class="hero-lead">Evrak, ilaç ve kurumsal gönderilerinizi motosikletle şehir içinde taşıyoruz. Fiyatı önceden görün, kuryeyi tek aramayla yönlendirin.</p>
<div class="btns">
<a class="btn btn-1 btn-lg" href="tel:{TEL}"><svg aria-hidden="true"><use href="#i-tel"/></svg>Hemen Kurye Çağır</a>
<a class="btn btn-g btn-lg" href="fiyat-hesaplama.html"><svg aria-hidden="true"><use href="#i-ileri"/></svg>{FIYAT_BTN}</a>
</div>
<ul class="hero-pts">
<li><svg aria-hidden="true"><use href="#i-ok"/></svg> Fiyat kurye yola çıkmadan netleşir, sürpriz ücret yok</li>
<li><svg aria-hidden="true"><use href="#i-ok"/></svg> {"Eczane teslimatlarında sabit 400 ₺ öncelikli tarife" if FIYAT_MODU!="kapali" else "Eczane teslimatlarında öncelikli sabit tarife"}</li>
<li><svg aria-hidden="true"><use href="#i-ok"/></svg> Kurumsal müşterilere aylık faturalı çalışma</li>
</ul>
</div>
<div class="glass">
<div class="glass-top">
<span><b>{"Taban tarife" if FIYAT_MODU!="kapali" else "Ortalama teslim"}</b><small>{"İlk 5 kilometre · Kağıthane merkez" if FIYAT_MODU!="kapali" else "İstanbul içi · aynı yaka"}</small></span>
<span class="glass-eta">{"380 ₺" if FIYAT_MODU!="kapali" else "30–60 dk"}</span>
</div>
<ul class="flow">
<li><span class="ic"><svg aria-hidden="true"><use href="#i-tel"/></svg></span><span><b>Arayın veya yazın</b><span>Alım ve teslim adresini alalım</span></span></li>
<li><span class="ic"><svg aria-hidden="true"><use href="#i-moto"/></svg></span><span><b>Kurye yola çıksın</b><span>Size en yakın kurye yönlendirilir</span></span></li>
<li><span class="ic"><svg aria-hidden="true"><use href="#i-ok"/></svg></span><span><b>Teslim edilsin</b><span>Teslimat teyidi tarafınıza iletilir</span></span></li>
</ul>
</div>
</div>
</section>

<section class="sec sec--tight">
<div class="wrap">
<div class="strip rv">
<div><b>39</b><span>İlçede hizmet</span></div>
<div><b>7/24</b><span>Gece dahil çalışma</span></div>
<div><b>{"380 ₺" if FIYAT_MODU!="kapali" else "Aynı gün"}</b><span>{"Taban tarife" if FIYAT_MODU!="kapali" else "Teslimat"}</span></div>
<div><b>3</b><span>Teslimat hızı</span></div>
</div>
</div>
</section>

<section class="sec">
<div class="wrap">
<div class="head"><span class="kicker">Hizmetlerimiz</span><h2>Hangi gönderiyi taşıyoruz?</h2>
<p>Acil evraktan düzenli kurumsal sevkiyata, eczane teslimatından havayolu gönderisine kadar.</p></div>
{hizmet_kartlari()}
</div>
</section>

<section class="sec sec--tint">
<div class="wrap">
<div class="head"><span class="kicker">Sahada</span><h2>Gönderiniz teslim edilene kadar</h2>
<p>Talep alındığı andan teslim teyidine kadar süreç tek elden yürüyor.</p></div>
<div class="serit rv">
<figure>{gorsel("01-ofis/musteri-temsilcisi-telefon.webp","Müşteri temsilcisi telefonla kurye talebi alırken",w=1408,h=768)}<figcaption>Talep alınır</figcaption></figure>
<figure>{gorsel("02-motor/kurye-kask-hazirlik.webp","Kurye kaskını takarak yola çıkmaya hazırlanırken",w=1408,h=768)}<figcaption>Kurye yönlendirilir</figcaption></figure>
<figure>{gorsel("02-motor/istanbul-trafik-moto-kurye.webp","İstanbul trafiğinde ilerleyen moto kurye",w=1408,h=768)}<figcaption>Yola çıkar</figcaption></figure>
<figure>{gorsel("07-musteri/depo-muduru-teslim-onay.webp","Teslim alan yetkili gönderiyi onaylarken",w=1408,h=768)}<figcaption>Teslim teyidi</figcaption></figure>
</div>
</div>
</section>

<section class="sec">
<div class="wrap">
<div class="head"><span class="kicker">Teslimat hızı</span><h2>Gönderinize uygun hızı seçin</h2>
<p>Aynı güzergâhta üç farklı hız. Aradaki fark, kuryenin başka adrese uğrayıp uğramaması.</p></div>
{hiz_bloklari()}
</div>
</section>

{fiyat_bolumu()}

<section class="sec sec--tint">
<div class="wrap">
<div class="head"><span class="kicker">Hizmet bölgeleri</span><h2>İstanbul'un iki yakasında da yanınızdayız</h2>
<p>İlçenizi seçin; o bölgeye ortalama teslim süresini, mesafeyi ve tahmini tarifeyi görün.</p></div>
<div class="yaka rv">
<div><h3><svg aria-hidden="true"><use href="#i-pin"/></svg> Avrupa Yakası</h3><ul class="chips">{cip(av)}</ul></div>
<div><h3><svg aria-hidden="true"><use href="#i-pin"/></svg> Anadolu Yakası</h3><ul class="chips">{cip(an)}</ul></div>
</div>
</div>
</section>

<section class="sec">
<div class="wrap">
<div class="head"><span class="kicker">Kimlere hizmet veriyoruz</span><h2>Sektörünüzün ritmine göre çalışıyoruz</h2></div>
<div class="grid g4 rv">
<article class="card"><span class="ic amber"><svg aria-hidden="true"><use href="#i-ilac"/></svg></span><h3>Eczaneler</h3><p>Acil ilaç, reçete ve depo arası transfer. Nöbet gecelerinde de ulaşılabilir kurye, sabit tarife.</p></article>
<article class="card"><span class="ic"><svg aria-hidden="true"><use href="#i-terazi"/></svg></span><h3>Hukuk Büroları</h3><p>Adliye, icra dairesi ve müvekkil arası evrak taşıma. Süreli dosyalarda gün kaçırmayın.</p></article>
<article class="card"><span class="ic"><svg aria-hidden="true"><use href="#i-evrak"/></svg></span><h3>Muhasebe Ofisleri</h3><p>Ay sonu beyanname yoğunluğunda mükellef evrakı toplama ve teslim turu.</p></article>
<article class="card"><span class="ic"><svg aria-hidden="true"><use href="#i-koli"/></svg></span><h3>E-Ticaret Satıcıları</h3><p>Aynı gün teslimat vaadinizi tutun. Toplu gönderi ve iade toplama desteği.</p></article>
</div>
</div>
</section>

{sssblok}
{cta_band()}"""

    ld = json.dumps({
      "@context":"https://schema.org","@type":"CourierService","@id":SITE+"/#organization",
      "name":AD,"alternateName":["Barse Moto Kurye"],
      "description":"İstanbul'un 39 ilçesinin tamamına 7/24 moto kurye hizmeti veren bağımsız kurye firması. Merkez ofis Kağıthane.",
      "url":SITE+"/","telephone":TEL,"email":EPOSTA,"priceRange":"₺₺",
      "image":SITE+"/og-image.jpg","logo":SITE+"/favicon-512.png",
      "address":{"@type":"PostalAddress","streetAddress":ADRES,"addressLocality":ILCE_MERKEZ,
                 "addressRegion":"İstanbul","addressCountry":"TR"},
      "geo":{"@type":"GeoCoordinates","latitude":41.081,"longitude":28.973},
      "areaServed":{"@type":"City","name":"İstanbul"},
      "sameAs":["https://www.facebook.com/p/Barse-Kurye-61592544492045/",
                "https://www.google.com/search?kgmid=/g/11zh74xy_0"],
      "identifier":{"@type":"PropertyValue",
                    "propertyID":"Google Knowledge Graph ID",
                    "value":"kg:/g/11zh74xy_0"},
      "currenciesAccepted":"TRY","paymentAccepted":"Nakit, Havale/EFT",
      "openingHoursSpecification":{"@type":"OpeningHoursSpecification",
        "dayOfWeek":["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"],
        "opens":"00:00","closes":"23:59"}
    }, ensure_ascii=False)
    js = f'<script type="application/ld+json">{ld}</script>{sssld}'
    return sayfa("index.html",
        "Barse Kurye | İstanbul Moto Kurye — 39 İlçede 7/24 Teslimat",
        "İstanbul'un 39 ilçesinde 7/24 moto kurye. Evrak, ilaç ve kurumsal gönderi; taban tarife 380 ₺. Fiyatı sitede hesaplayın, kuryeyi hemen çağırın.",
        govde, "index.html", ilceler, js,
        '' if FIYAT_MODU == "kapali" else '<script src="hesap.js" defer></script>')

# ─────────────────────────────────────────────────────── BÖLGE SAYFALARI

def bolge_sayfa(dosya, ad, veri, ilceler, ust=None, noktalar=None, aciklama_ek="", foto=None):
    """ad: Kadıköy / Levent  |  ust: bağlı olduğu ilçe (semt sayfalarında)"""
    nk = noktalar if noktalar is not None else veri['noktalar']
    yaka, km, fiyat, sure = veri['yaka'], veri['km'], veri['fiyat'], veri['sure']
    karsi = "Anadolu" if yaka == "Avrupa" else "Avrupa"
    baglam = f"{ad}, {ust} ilçesinde" if ust else f"{ad}, İstanbul'un {yaka} yakasında"

    mahalle = ", ".join(nk[:14]) if nk else ""
    mah_blok = f"""<h2>{ad} genelinde teslimat yaptığımız noktalar</h2>
<p>Kurye yönlendirmesi yaptığımız başlıca mahalle ve merkezler: {mahalle}. Listede olmayan bir adres için de kurye gönderiyoruz; aramanız yeterli.</p>""" if mahalle else ""

    komsu = veri.get('komsu', [])
    kom_cip = "".join('<li><a href="%s-kurye.html">%s</a></li>' % (ilceler[k]['slug'], k)
                      for k in komsu if k in ilceler)

    sss = [
      (f"{ad} bölgesine kurye ne kadar sürede geliyor?",
       f"Merkez ofisimiz Kağıthane'de. {ad} yaklaşık {km} km uzaklıkta ve normal teslimatta süre çoğunlukla {sure} aralığında kalıyor. Express talepte kurye başka adrese uğramaz, VIP talepte gönderiye özel kurye atanır."),
      (f"{ad} için kurye ücreti ne kadar?",
       f"{ad} yönündeki tek yön teslimatlarda taban tarife yaklaşık {fiyat} ₺'den başlıyor. Bu tutar mesafeye göre hesaplanır; paket boyutu, al-ver ve ek durak seçenekleri fiyatı değiştirir. Gece 20:00–06:00 arası ve hafta sonu 100 ₺ fark eklenir. Kesin tutarı Fiyat Hesaplama sayfasından görebilirsiniz."),
      (f"{ad}'dan {karsi} yakasına gönderi taşıyor musunuz?",
       f"Evet. Yakalar arası gönderilerde güzergâha köprü geçişi eklendiği için mesafeye 6 km ilave ediliyor ve süre trafiğe göre uzayabiliyor. Acil işlerde Express veya VIP seçmenizi öneririz."),
      (f"{ad} bölgesine gece kurye geliyor mu?",
       "Geliyor. 7 gün 24 saat çalışıyoruz; nöbetçi eczane teslimatları ve mesai dışı evrak taşımaları gece saatlerinde de yapılıyor. Gece tarifesi 20:00–06:00 arasında geçerlidir."),
    ]
    sssblok, sssld = sss_blok(sss)

    ust_crumb = ('<li><a href="%s-kurye.html">%s</a></li>' % (ilceler[ust]['slug'], ust)) if ust and ust in ilceler else ''
    foto_blok = (f'<div class="wrap"><figure class="sahne rv">{gorsel(foto[0], foto[1], oncelik=True)}</figure></div>'
                 if foto else '')

    govde = f"""<nav class="crumb wrap" aria-label="Site yolu">
<ol><li><a href="index.html">Ana Sayfa</a></li><li><a href="istanbul-ici-kurye.html">İlçeler</a></li>{ust_crumb}<li><span aria-current="page">{ad}</span></li></ol>
</nav>

<section class="sec sec--tight">
<div class="wrap">
<div style="max-width:60ch">
<span class="kicker">{yaka} Yakası</span>
<h1>{ad} Moto Kurye</h1>
<p class="head" style="font-size:1.12rem;color:var(--body);margin-top:16px;margin-bottom:24px">{baglam} bulunuyor. Kağıthane'deki merkezimize yaklaşık {km} km mesafede; normal teslimatta ortalama süre {sure}. Evrak, ilaç ve kurumsal gönderileriniz için kurye yönlendiriyoruz.</p>
<div class="btns">
<a class="btn btn-1 btn-lg" href="tel:{TEL}"><svg aria-hidden="true"><use href="#i-tel"/></svg>Kurye Çağır</a>
<a class="btn btn-o btn-lg" href="fiyat-hesaplama.html">{FIYAT_BTN}</a>
</div>
</div>
</div>
</section>

{foto_blok}
<section class="sec sec--tint sec--tight">
<div class="wrap">
<div class="tbl-x rv">
<table>
<caption>{ad} bölgesi teslimat bilgileri — Kağıthane merkez çıkışlı</caption>
<tbody>
<tr><th scope="row">Yaka</th><td>{yaka} Yakası</td></tr>
<tr><th scope="row">Merkeze uzaklık</th><td class="tnum">yaklaşık {km} km</td></tr>
<tr><th scope="row">Normal teslimat süresi</th><td class="tnum">{sure}</td></tr>
<tr><th scope="row">Taban tarife</th><td class="tnum">yaklaşık {fiyat} ₺'den başlar</td></tr>
<tr><th scope="row">Çalışma saatleri</th><td>7 gün 24 saat</td></tr>
<tr><th scope="row">Eczane kurye</th><td>sabit 400 ₺ — öncelikli sipariş</td></tr>
</tbody>
</table>
</div>
</div>
</section>

<section class="sec">
<div class="wrap" style="display:grid;gap:48px">
<div class="prose">
<h2>{ad} için hangi gönderileri taşıyoruz?</h2>
<p>{ad} bölgesinde en sık taşıdığımız gönderiler ofis evrakları, eczane teslimatları ve kurumsal müşterilerin günlük dosya turları. {aciklama_ek}</p>
<ul>
<li><strong>Evrak ve dosya:</strong> sözleşme, fatura, ihale dosyası ve resmi evrak teslimi.</li>
<li><strong>İlaç ve reçete:</strong> eczaneden hasta adresine öncelikli teslimat, sabit tarife.</li>
<li><strong>Kurumsal düzenli tur:</strong> her gün aynı saatte gelen sabit kurye, aylık faturalı çalışma.</li>
<li><strong>E-ticaret:</strong> aynı gün müşteri teslimi ve iade toplama.</li>
</ul>
{mah_blok}
<div class="note">
<p><strong>Acil gönderiniz mi var?</strong> {ad} çevresinde o an boşta kurye varsa süre belirgin şekilde kısalıyor. Aramanız yeterli: <a href="tel:{TEL}">{TEL_GOSTER}</a></p>
</div>
</div>
<div>
<h2 style="font-size:var(--t-2xl);margin-bottom:20px">Yakındaki diğer bölgeler</h2>
<ul class="chips">{kom_cip}<li><a href="istanbul-ici-kurye.html">Tüm ilçeler</a></li></ul>
</div>
</div>
</section>

<section class="sec sec--tint">
<div class="wrap">
<div class="head"><span class="kicker">Teslimat hızı</span><h2>{ad} için hız seçenekleri</h2></div>
{hiz_bloklari()}
</div>
</section>

{sssblok}
{cta_band(f"{ad}'da kurye mi lazım?", "Arayın, size en yakın moto kuryeyi hemen yönlendirelim.")}"""

    crumb_ld = {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
        {"@type":"ListItem","position":1,"name":"Ana Sayfa","item":SITE+"/"},
        {"@type":"ListItem","position":2,"name":"İlçeler","item":SITE+"/istanbul-ici-kurye.html"},
        {"@type":"ListItem","position":3,"name":ad}]}
    ld = f'<script type="application/ld+json">{json.dumps(crumb_ld, ensure_ascii=False)}</script>{sssld}'
    return sayfa(dosya,
        f"{ad} Kurye | Moto Kurye {ad} — {AD}",
        f"{ad} bölgesinde 7/24 moto kurye. Ortalama {sure} teslimat, taban tarife {fiyat} ₺'den başlar. Evrak, ilaç ve kurumsal gönderi. Hemen arayın: {TEL_GOSTER}",
        govde, "istanbul-ici-kurye.html", ilceler, ld)

# ─────────────────────────────────────────────────────── HİZMET SAYFALARI

def hizmet_sayfa(dosya, h1, baslik, aciklama, kicker, giris, bolumler, sss, ilceler, aktif="", foto=None):
    ic = "".join(f"<h2>{b}</h2>" + "".join(f"<p>{p}</p>" for p in ps) for b, ps in bolumler)
    sssblok, sssld = sss_blok(sss)
    foto_blok = (f'<div class="wrap"><figure class="sahne rv">{gorsel(foto[0], foto[1], oncelik=True)}</figure></div>'
                 if foto else '')
    govde = f"""<nav class="crumb wrap" aria-label="Site yolu">
<ol><li><a href="index.html">Ana Sayfa</a></li><li><span aria-current="page">{h1}</span></li></ol>
</nav>
<section class="sec sec--tight">
<div class="wrap"><div style="max-width:62ch">
<span class="kicker">{kicker}</span>
<h1>{h1}</h1>
<p style="font-size:1.12rem;color:var(--body);margin:16px 0 24px">{giris}</p>
<div class="btns">
<a class="btn btn-1 btn-lg" href="tel:{TEL}"><svg aria-hidden="true"><use href="#i-tel"/></svg>{TEL_GOSTER}</a>
<a class="btn btn-o btn-lg" href="https://wa.me/{WA}" rel="noopener"><svg aria-hidden="true"><use href="#i-wa"/></svg>WhatsApp</a>
</div>
</div></div>
</section>
{foto_blok}
<section class="sec sec--tight"><div class="wrap"><div class="strip rv">
<div><b>39</b><span>İlçede hizmet</span></div><div><b>7/24</b><span>Kesintisiz</span></div>
<div><b>{"380 ₺" if FIYAT_MODU!="kapali" else "Aynı gün"}</b><span>{"Taban tarife" if FIYAT_MODU!="kapali" else "Teslimat"}</span></div><div><b>3</b><span>Teslimat hızı</span></div>
</div></div></section>
<section class="sec"><div class="wrap"><div class="prose">{ic}</div></div></section>
<section class="sec sec--tint"><div class="wrap">
<div class="head"><span class="kicker">Teslimat hızı</span><h2>Hız seçenekleri</h2></div>
{hiz_bloklari()}
</div></section>
{sssblok}
{cta_band()}"""
    return sayfa(dosya, baslik, aciklama, govde, aktif or dosya, ilceler, sssld)

# ─────────────────────────────────────────────────────── SEMT EŞLEŞTİRME
# slug -> (görünen ad, bağlı ilçe, o semte ait nokta filtresi)
SEMTLER = {
 "atasehir-finans": ("Ataşehir Finans Merkezi","Ataşehir",["Finans Merkezi","Ataşehir","Küçükbakkalköy","Barbaros"]),
 "bagdat-caddesi":  ("Bağdat Caddesi","Kadıköy",["Bağdat","Suadiye","Erenköy","Caddebostan","Göztepe"]),
 "bakirkoy-merkez": ("Bakırköy Merkez","Bakırköy",["Bakırköy","İncirli","Ataköy"]),
 "besiktas-carsi":  ("Beşiktaş Çarşı","Beşiktaş",["Beşiktaş","Akaretler","Barbaros","Yıldız"]),
 "caglayan":        ("Çağlayan","Kağıthane",["Çağlayan","Gürsel","Merkez"]),
 "esenyurt-merkez": ("Esenyurt Merkez","Esenyurt",["Esenyurt"]),
 "ikitelli":        ("İkitelli","Başakşehir",["İkitelli","Başakşehir","Güvercintepe"]),
 "kadikoy-moda":    ("Kadıköy Moda","Kadıköy",["Moda","Caferağa","Rıhtım","Kadıköy"]),
 "kartal-merkez":   ("Kartal Merkez","Kartal",["Kartal"]),
 "kozyatagi":       ("Kozyatağı","Kadıköy",["Kozyatağı","Sahrayıcedit","Erenköy"]),
 "levent":          ("Levent","Beşiktaş",["Levent","Kanyon","Metrocity","Etiler"]),
 "maslak":          ("Maslak","Sarıyer",["Maslak","Ayazağa","İTÜ","Vadistanbul"]),
 "mecidiyekoy":     ("Mecidiyeköy","Şişli",["Mecidiyeköy","Fulya","Gülbağ","Cevahir","Trump"]),
 "nisantasi":       ("Nişantaşı","Şişli",["Nişantaşı","Teşvikiye","Maçka","Harbiye","Osmanbey"]),
 "otogar":          ("Otogar (Bayrampaşa)","Bayrampaşa",["Otogar","Bayrampaşa"]),
 "perpa":           ("Perpa Ticaret Merkezi","Şişli",["Perpa","Okmeydanı"]),
 "seyrantepe":      ("Seyrantepe","Kağıthane",["Seyrantepe","Skyland","Sanayi"]),
 "sisli-merkez":    ("Şişli Merkez","Şişli",["Şişli","Halaskargazi","Bomonti"]),
 "taksim-beyoglu":  ("Taksim ve Beyoğlu","Beyoğlu",["Taksim","İstiklal","Galata","Karaköy","Cihangir"]),
 "topkapi":         ("Topkapı","Zeytinburnu",["Topkapı","Merter","Zeytinburnu"]),
 "umraniye-merkez": ("Ümraniye Merkez","Ümraniye",["Ümraniye","Atatürk","Çakmak"]),
 "zincirlikuyu":    ("Zincirlikuyu","Beşiktaş",["Zincirlikuyu","Gayrettepe","Balmumcu","Esentepe"]),
}

# ─────────────────────────────────────────────────────── DURAĞAN SAYFALAR

def basit_sayfa(dosya, h1, baslik, aciklama, kicker, ic, ilceler, aktif=""):
    govde = f"""<nav class="crumb wrap" aria-label="Site yolu">
<ol><li><a href="index.html">Ana Sayfa</a></li><li><span aria-current="page">{h1}</span></li></ol>
</nav>
<section class="sec sec--tight"><div class="wrap"><div style="max-width:62ch">
<span class="kicker">{kicker}</span><h1>{h1}</h1></div></div></section>
<section class="sec" style="padding-top:0"><div class="wrap"><div class="prose">{ic}</div></div></section>
{cta_band()}"""
    return sayfa(dosya, baslik, aciklama, govde, aktif, ilceler)

def bolgeler_hub(ilceler):
    av = sorted([i for i in ilceler.values() if i['yaka']=='Avrupa'], key=lambda x:x['km'])
    an = sorted([i for i in ilceler.values() if i['yaka']=='Anadolu'], key=lambda x:x['km'])
    def satir(lst):
        return "".join(
          f'<tr><th scope="row"><a href="{i["slug"]}-kurye.html">{i["ad"]}</a></th>'
          f'<td class="tnum">{i["km"]} km</td><td class="tnum">{i["sure"]}</td>'
          f'<td class="tnum">{i["fiyat"]} ₺</td></tr>' for i in lst)
    semt = "".join('<li><a href="%s-kurye.html">%s</a></li>' % (s, SEMTLER[s][0]) for s in sorted(SEMTLER))
    govde = f"""<nav class="crumb wrap" aria-label="Site yolu">
<ol><li><a href="index.html">Ana Sayfa</a></li><li><span aria-current="page">İstanbul İçi Kurye</span></li></ol>
</nav>
<section class="sec sec--tight"><div class="wrap"><div style="max-width:64ch">
<span class="kicker">Hizmet bölgeleri</span>
<h1>İstanbul İçi Kurye — 39 İlçe</h1>
<p style="font-size:1.12rem;color:var(--body);margin:16px 0 24px">Aşağıdaki tablo, Kağıthane'deki merkezimizden her ilçeye yaklaşık mesafeyi, normal teslimatta ortalama süreyi ve taban tarifeyi gösterir. İlçe adına dokunarak o bölgenin sayfasına gidebilirsiniz.</p>
<div class="btns"><a class="btn btn-1 btn-lg" href="tel:{TEL}"><svg aria-hidden="true"><use href="#i-tel"/></svg>{TEL_GOSTER}</a>
<a class="btn btn-o btn-lg" href="fiyat-hesaplama.html">{FIYAT_BTN}</a></div>
</div></div></section>

<section class="sec"><div class="wrap">
<h2 style="margin-bottom:20px">Avrupa Yakası</h2>
<div class="tbl-x rv"><table>
<caption>Kağıthane merkez çıkışlı yaklaşık değerler</caption>
<thead><tr><th scope="col">İlçe</th><th scope="col">Mesafe</th><th scope="col">Süre</th><th scope="col">Taban</th></tr></thead>
<tbody>{satir(av)}</tbody></table></div>

<h2 style="margin:48px 0 20px">Anadolu Yakası</h2>
<div class="tbl-x rv"><table>
<caption>Yakalar arası geçişte güzergâha köprü payı eklenir</caption>
<thead><tr><th scope="col">İlçe</th><th scope="col">Mesafe</th><th scope="col">Süre</th><th scope="col">Taban</th></tr></thead>
<tbody>{satir(an)}</tbody></table></div>

<h2 style="margin:48px 0 20px">Semt ve merkez sayfaları</h2>
<ul class="chips">{semt}</ul>

<div class="note amber" style="margin-top:40px">
<p><strong>Tablodaki tutarlar taban tarifedir.</strong> Paket boyutu, al-ver (gidiş-dönüş), ek durak, gece ve hafta sonu farkı tutarı değiştirir. Gönderinize özel tutarı <a href="fiyat-hesaplama.html">Fiyat Hesaplama</a> sayfasından görebilirsiniz.</p>
</div>
</div></section>
{cta_band()}"""
    return sayfa("istanbul-ici-kurye.html",
      "İstanbul İçi Kurye | 39 İlçede Moto Kurye — " + AD,
      "İstanbul'un 39 ilçesine moto kurye. Her ilçe için mesafe, ortalama teslim süresi ve taban tarife tablosu. 7/24 hizmet.",
      govde, "istanbul-ici-kurye.html", ilceler)

def fiyat_sayfa_kapali(ilceler):
    """Hesaplayıcı kapalıyken de /fiyat-hesaplama.html yaşamaya devam eder:
       URL'yi öldürmek mevcut arama sıralamasını kaybettirir."""
    sss = [
      ("Kurye ücreti neye göre belirleniyor?",
       "Tutar; alım ve teslim noktası arasındaki yol mesafesine, seçtiğiniz teslimat hızına, paket boyutuna ve varsa al-ver / ek durak taleplerine göre belirlenir. Gece ve hafta sonu teslimatlarda tarife farkı uygulanır."),
      ("Fiyatı önceden öğrenebilir miyim?",
       "Evet. Alım ve teslim adresini telefonla ya da WhatsApp'tan iletin, dakikalar içinde kesin tutarı söyleyelim. Kurye yola çıkmadan önce fiyat netleşir, sonradan ek ücret çıkmaz."),
      ("Eczane teslimatı nasıl fiyatlanıyor?",
       "Eczane teslimatları öncelikli sipariş olarak sabit tarifeyle taşınır; mesafe, saat ve hafta sonu farkı uygulanmaz."),
      ("Al-ver (gidiş-dönüş) ne demek?",
       "Kurye gönderiyi teslim ettikten sonra adreste bekler ve karşılığında alacağı evrak veya paketle size döner. Tek yön teslimata göre farklı fiyatlanır."),
      ("Kurumsal müşteriler için farklı tarife var mı?",
       "Var. Aylık gönderi adedinize göre sözleşmeli tarife belirliyoruz; düzenli hacimde birim fiyat tek gönderiye göre daha uygun oluyor."),
    ]
    sssblok, sssld = sss_blok(sss)
    govde = f"""<nav class="crumb wrap" aria-label="Site yolu">
<ol><li><a href="index.html">Ana Sayfa</a></li><li><span aria-current="page">Fiyat</span></li></ol>
</nav>
<section class="sec sec--tight"><div class="wrap"><div style="max-width:62ch">
<span class="kicker">Fiyat</span><h1>Kurye Fiyatları</h1>
<p style="font-size:1.12rem;color:var(--body);margin:16px 0 24px">Her gönderi farklı olduğu için tek bir liste fiyatı vermiyoruz. Alım ve teslim adresini iletin, dakikalar içinde kesin tutarı söyleyelim — kurye yola çıkmadan önce.</p>
<div class="btns">
<a class="btn btn-1 btn-lg" href="tel:{TEL}"><svg aria-hidden="true"><use href="#i-tel"/></svg>Hemen Ara — {TEL_GOSTER}</a>
<a class="btn btn-o btn-lg" href="https://wa.me/{WA}" rel="noopener"><svg aria-hidden="true"><use href="#i-wa"/></svg>WhatsApp ile Sor</a>
</div>
</div></div></section>
<section class="sec" style="padding-top:0"><div class="wrap"><div class="prose">
<h2>Fiyatı belirleyen beş şey</h2>
<ul>
<li><strong>Mesafe:</strong> alım ve teslim noktası arasındaki yol uzunluğu. Yakalar arası geçişlerde güzergâha köprü payı eklenir.</li>
<li><strong>Teslimat hızı:</strong> Normal, Express veya VIP. Express ve VIP'te kurye başka adrese uğramaz.</li>
<li><strong>Paket boyutu:</strong> zarf ve dosyada ek ücret yok; hacimli gönderilerde kademeli fark uygulanır.</li>
<li><strong>Al-ver ve ek durak:</strong> kuryenin beklemesi veya yolda başka adrese uğraması.</li>
<li><strong>Saat ve gün:</strong> gece ve hafta sonu teslimatlarda tarife farkı eklenir.</li>
</ul>
<div class="note amber">
<p><strong>Eczane teslimatları sabit tarifelidir.</strong> Mesafe, saat ve hafta sonu farkı uygulanmaz; talep öncelikli sipariş olarak işleme alınır.</p>
</div>
<h2>Neden liste fiyatı yayınlamıyoruz?</h2>
<p>İstanbul içi kurye fiyatı iki adres arasındaki gerçek güzergâha bağlı. Aynı iki ilçe arasında bile trafik, tam adres ve gönderi türü tutarı değiştiriyor. Baştan yanlış bir rakam vermektense, adresi alıp doğru fiyatı söylemeyi tercih ediyoruz.</p>
<p>Kurumsal müşterilerimiz için aylık gönderi hacmine göre sözleşmeli tarife belirliyoruz. <a href="kurumsal-kurye.html">Kurumsal kurye sayfasına</a> bakabilirsiniz.</p>
</div></div></section>
{sssblok}
{cta_band()}"""
    return sayfa("fiyat-hesaplama.html",
      "Kurye Fiyatları | İstanbul Moto Kurye Ücreti — " + AD,
      "İstanbul içi kurye ücreti mesafeye, teslimat hızına ve gönderi türüne göre belirlenir. Adresi iletin, dakikalar içinde net fiyat alın.",
      govde, "fiyat-hesaplama.html", ilceler, sssld)

def fiyat_sayfa(ilceler):
    if FIYAT_MODU == "kapali":
        return fiyat_sayfa_kapali(ilceler)
    sss = [
      ("Sitedeki fiyat kesin mi?",
       "Hesaplayıcı, seçtiğiniz iki nokta arasındaki mesafeden tahmini bir tutar üretir. Tam adres, trafik ve gönderi içeriğine göre kesin fiyat telefonda teyit edilir. Kurye yola çıkmadan önce tutarı netleştiriyoruz."),
      ("Taban ücret neyi kapsıyor?",
       "Taban ücret 380 ₺'dir ve ilk 5 kilometreyi kapsar. 5–25 km arası her kilometre için 14 ₺, 25 km üzerindeki her kilometre için 11 ₺ eklenir."),
      ("Paket boyutu fiyatı nasıl etkiliyor?",
       "Zarf ve dosya için ek ücret yoktur. Küçük paketten çanta üstü hacimli gönderiye doğru kademeli bir çarpan uygulanır; hesaplayıcıda boyutu seçtiğinizde tutara yansır."),
      ("Al-ver ne demek?",
       "Kurye gönderiyi teslim ettikten sonra adreste bekler ve karşılığında alacağı evrak veya paketle size döner. Tek yön tarifenin 1,7 katı olarak fiyatlanır."),
      ("Eczane teslimatında mesafe farkı var mı?",
       "Yok. Eczane kurye sabit 400 ₺ tarifelidir; mesafe, saat ve hafta sonu farkı uygulanmaz."),
    ]
    sssblok, sssld = sss_blok(sss)
    govde = f"""<nav class="crumb wrap" aria-label="Site yolu">
<ol><li><a href="index.html">Ana Sayfa</a></li><li><span aria-current="page">Fiyat Hesaplama</span></li></ol>
</nav>
<section class="sec sec--tight"><div class="wrap"><div style="max-width:62ch">
<span class="kicker">Fiyat</span><h1>Kurye Fiyat Hesaplama</h1>
<p style="font-size:1.12rem;color:var(--body);margin-top:16px">Alım ve teslim noktasını yazın, listeden seçin. Tahmini tutarı anında görün, isterseniz tek dokunuşla WhatsApp'tan talep oluşturun.</p>
</div></div></section>
<section class="sec" style="padding-top:0"><div class="wrap">
<div class="grid g2" style="align-items:start">
{HESAPLAYICI}
<div>
<h2 style="font-size:var(--t-2xl);margin-bottom:16px">{"Tarife kalemleri" if FIYAT_MODU=="acik" else "Fiyatı belirleyen unsurlar"}</h2>
{tarife_tablo() if FIYAT_MODU=="acik" else FIYAT_UNSUR}
<div class="note" style="margin-top:24px">
<p><strong>Neye göre hesaplanıyor?</strong> Tutar, iki nokta arasındaki yol mesafesinden üretilir. Yakalar arası geçişlerde güzergâha köprü payı eklenir. Gece ve hafta sonu farkı, hesaplama anındaki saate göre otomatik uygulanır.</p>
</div>
</div>
</div>
</div></section>
{sssblok}
{cta_band()}"""
    return sayfa("fiyat-hesaplama.html",
      "Kurye Fiyat Hesaplama | İstanbul Moto Kurye Ücreti — " + AD,
      "İstanbul içi kurye ücretini anında hesaplayın. Taban tarife 380 ₺, mesafeye göre kademeli fiyat. Eczane kurye sabit 400 ₺.",
      govde, "fiyat-hesaplama.html", ilceler, sssld,
      '<script src="hesap.js" defer></script>')

# ─────────────────────────────────────────────────────── HİZMET İÇERİKLERİ

def hizmet_sayfalari(ilceler):
    S = {}
    S["moto-kurye.html"] = hizmet_sayfa("moto-kurye.html","İstanbul Moto Kurye",
      "Moto Kurye İstanbul | Aynı Gün Evrak ve Paket Teslimatı — "+AD,
      "İstanbul'da moto kurye hizmeti. Evrak, dosya ve paket gönderileri aynı gün teslim. 39 ilçede 7/24, taban tarife 380 ₺.",
      "Temel hizmet",
      "Motosiklet, İstanbul trafiğinde bir gönderiyi bir noktadan diğerine ulaştırmanın en hızlı yolu. Evrak ve paket gönderilerinizi 39 ilçede motorlu kuryelerimizle taşıyoruz.",
      [("Moto kurye ne zaman doğru seçim?",
        ["Gönderiniz motosiklet çantasına sığıyorsa ve aynı gün içinde yerine ulaşması gerekiyorsa moto kurye en hızlı çözümdür. Trafiğin yoğun olduğu saatlerde motosiklet, dört tekerlekli bir araca göre belirgin biçimde daha kısa sürede varır.",
         "Sözleşme, fatura, ihale dosyası, numune, yedek parça, reçete ve küçük e-ticaret paketleri en sık taşıdığımız gönderiler. Hacimli kolilerde ise gönderinin ölçüsünü aramadan önce belirtmenizi rica ediyoruz."]),
       ("Süreç nasıl işliyor?",
        ["Telefon ya da WhatsApp ile alım ve teslim adresini iletiyorsunuz. Fiyat, kurye yola çıkmadan önce netleşiyor. Talebiniz alındığı anda size en yakın kurye yönlendiriliyor ve gönderi teslim edildiğinde teyit tarafınıza bildiriliyor.",
         "Gönderiniz için üç hız seçeneği var: Normal, Express ve VIP. Aradaki temel fark kuryenin yol boyunca başka adrese uğrayıp uğramaması."]),
       ("Fiyat nasıl belirleniyor?",
        ["Taban ücret ilk 5 kilometre için 380 ₺. Sonrasında 25 kilometreye kadar her kilometre 14 ₺, 25 kilometrenin üzerinde her kilometre 11 ₺ ekleniyor. Paket boyutu, al-ver ve ek durak seçenekleri tutarı değiştiriyor.",
         "Gönderinize özel tahmini tutarı Fiyat Hesaplama sayfasından anında görebilirsiniz."])],
      [("Moto kurye en fazla ne kadar yük taşır?",
        "Motosiklet çantasına sığan, taşınması güvenli gönderiler taşınır. Hacimli koliler ve uygun ambalajı olmayan kırılgan ürünler için önce aramanızı öneriyoruz."),
       ("Gönderim sigortalı mı?",
        "Gönderi teslim alındığı andan itibaren kurye sorumluluğundadır. Yüksek değerli gönderilerde içeriği önceden bildirmenizi rica ediyoruz."),
       ("Aynı gün teslimat garantisi var mı?",
        "İstanbul içi gönderilerde aynı gün teslimat standardımızdır. Kesin saat taahhüdü gereken işlerde Express veya VIP seçeneğini öneriyoruz.")],
      ilceler, "moto-kurye.html",
      ("02-motor/moto-kurye-motosiklet.webp","Barse Kurye moto kuryesi İstanbul trafiğinde yola çıkarken"))

    S["acil-kurye.html"] = hizmet_sayfa("acil-kurye.html","Acil Kurye İstanbul",
      "Acil Kurye İstanbul | Express ve VIP Moto Kurye — "+AD,
      "İstanbul'da acil kurye. Express 45-60 dk, VIP 30-45 dk. Gönderiye özel kurye, duraksız teslimat. 7/24 arayın: "+TEL_GOSTER,
      "En hızlı seçenek",
      "Bekleyemeyen gönderiler için Express ve VIP kurye. Kurye başka adrese uğramadan doğrudan teslimata gider.",
      [("Express ile VIP arasındaki fark",
        ["Express kurye, gönderinizi başka paketlerle birleştirmeden öncelikli olarak taşır. Teslimat çoğunlukla 45–60 dakikada tamamlanır ve tarifeye 1,25 katsayı uygulanır.",
         "VIP kurye ise gönderinize özel atanır. Kurye yol boyunca hiçbir adrese uğramaz, doğrudan teslimata gider. Süre 30–45 dakikaya iner, tarifeye 1,6 katsayı uygulanır."]),
       ("Hangi durumlarda acil kurye gerekir?",
        ["Süreli evrak teslimi, ihale dosyası, imza gerektiren sözleşme, acil ilaç, üretimi durduran yedek parça ve gün içinde yetişmesi gereken numune gönderileri en sık karşılaştığımız acil talepler.",
         "Adliye ve resmî kurum teslimlerinde saat sınırı olduğu için bu işlerde VIP kurye öneriyoruz."]),
       ("Gece acil kurye",
        ["7 gün 24 saat çalışıyoruz. Gece 20:00 – 06:00 arasında tarifeye 100 ₺ fark ekleniyor; hafta sonu için de aynı tutarda fark uygulanıyor. Nöbetçi eczane teslimatları gece de yapılıyor."])],
      [("Acil kurye ne kadar sürede gelir?",
        "Kurye yönlendirmesi talebiniz alındığı anda yapılır. Alım noktasına varış çoğunlukla 15–30 dakika içinde olur; toplam teslim süresi mesafeye göre değişir."),
       ("VIP kurye ne kadar tutuyor?",
        "VIP tarifesi, aynı güzergâhın normal tarifesinin 1,6 katıdır. Fiyat Hesaplama sayfasından hızı VIP seçerek tam tutarı görebilirsiniz."),
       ("Gece acil kurye çağırabilir miyim?",
        "Evet, 7/24 hizmet veriyoruz. Gece 20:00–06:00 arasında 100 ₺ gece tarifesi farkı uygulanır.")],
      ilceler, "acil-kurye.html",
      ("06-hizmet/express-kurye-sure.webp","Express kurye gönderiyi öncelikli olarak teslim ederken"))

    S["eczane-kurye.html"] = hizmet_sayfa("eczane-kurye.html","Eczane ve İlaç Kurye",
      "Eczane Kurye İstanbul | Sabit 400 ₺ İlaç Teslimatı — "+AD,
      "İstanbul'da eczane ve ilaç kurye. Sabit 400 ₺ öncelikli tarife, mesafe farkı yok. Nöbetçi eczane teslimatları için 7/24 hizmet.",
      "Sabit tarife",
      "Eczaneler, hastalar ve medikal firmalar için öncelikli ilaç teslimatı. Sabit 400 ₺ tarife; mesafe, saat ve hafta sonu farkı uygulanmaz.",
      [("Neden sabit tarife?",
        ["İlaç teslimatı çoğunlukla acildir ve fiyat pazarlığına ayıracak vakit yoktur. Bu yüzden eczane kurye taleplerini sabit 400 ₺ tarifeyle, öncelikli sipariş olarak işleme alıyoruz.",
         "Bu tarifeye mesafe farkı, gece farkı ve hafta sonu farkı eklenmez. Hesaplayıcıda Eczane Kurye kutusunu işaretlediğinizde tutar doğrudan 400 ₺ olarak görünür."]),
       ("Kimler kullanıyor?",
        ["Eczaneler hastaya ilaç ulaştırmak, depo ile aralarındaki transferi tamamlamak ve nöbet gecelerinde reçete teslimi yapmak için düzenli olarak çalışıyor.",
         "Hastalar ve hasta yakınları da doğrudan arayarak nöbetçi eczaneden ilaç getirtebiliyor. Reçete bilgisini WhatsApp'tan iletmeniz yeterli."]),
       ("Gece ve nöbet teslimatı",
        ["Nöbetçi eczane teslimatlarını gece saatlerinde de yapıyoruz. 7 gün 24 saat açığız ve eczane taleplerinde gece farkı uygulamıyoruz."])],
      [("Eczane kurye ücreti ne kadar?",
        "Sabit 400 ₺'dir. Mesafe, saat ve hafta sonu farkı uygulanmaz."),
       ("Nöbetçi eczaneden gece ilaç getirir misiniz?",
        "Evet. 7/24 çalışıyoruz ve eczane teslimatlarında gece tarifesi farkı uygulanmıyor."),
       ("Reçeteyi nasıl iletirim?",
        "Reçete görselini WhatsApp'tan gönderebilirsiniz. Kurye eczaneden teslim alır ve adresinize ulaştırır.")],
      ilceler, "eczane-kurye.html",
      ("01-ofis/eczane-teslimat-tezgah.webp","Eczane tezgâhında kuryeye teslim edilen ilaç paketi"))

    S["kurumsal-kurye.html"] = hizmet_sayfa("kurumsal-kurye.html","Kurumsal Kurye Hizmeti",
      "Kurumsal Kurye İstanbul | Aylık Faturalı Düzenli Kurye — "+AD,
      "İşletmeler için düzenli kurye. Her gün sabit saatte gelen kurye, aylık toplu fatura, gönderi dökümü. Hukuk, muhasebe ve e-ticaret firmalarına özel düzen.",
      "İşletmeler için",
      "Her gün aynı saatte gelen sabit kurye, aylık toplu fatura ve ay sonunda gönderi dökümü. İşletmenizin ritmine göre kurulan bir çalışma düzeni.",
      [("Nasıl bir düzen kuruyoruz?",
        ["Gönderi hacminizi ve günlük akışınızı konuşarak başlıyoruz. Sabit saatli tur mu gerekiyor, yoksa gün içinde çağrı üzerine mi kurye istiyorsunuz — düzeni buna göre kuruyoruz.",
         "Sabit turlarda kurye her gün belirlenen saatte adresinize gelir, o günün gönderilerini alır ve teslim eder. Ay sonunda tek fatura ve gönderi dökümü tarafınıza iletilir."]),
       ("Hangi sektörlerle çalışıyoruz?",
        ["Hukuk büroları adliye, icra dairesi ve müvekkil arası evrak taşıma için; muhasebe ofisleri ay sonu beyanname yoğunluğunda mükellef evrakı toplamak için çalışıyor.",
         "E-ticaret satıcıları aynı gün teslimat ve iade toplama için, medikal firmalar ise numune ve cihaz sevkiyatı için düzenli kurye kullanıyor."]),
       ("Fiyatlandırma",
        ["Kurumsal çalışmada aylık gönderi adedine göre tarife belirliyoruz. Düzenli hacimde tek gönderi tarifesine göre daha uygun bir birim fiyat çıkıyor.",
         "Teklif için gönderi hacminizi ve tipik güzergâhlarınızı paylaşmanız yeterli."])],
      [("Aylık fatura kesiyor musunuz?",
        "Evet. Kurumsal müşterilerimize aylık toplu fatura düzenliyoruz ve ay sonunda gönderi dökümünü iletiyoruz."),
       ("Sözleşme şart mı?",
        "Düzenli çalışmada tarafların hak ve yükümlülüklerini netleştirmek için sözleşme yapıyoruz. Tek seferlik gönderilerde sözleşme gerekmez."),
       ("Her gün aynı kurye mi geliyor?",
        "Sabit turlarda bölgeyi ve adresi bilen kuryeyi sabitlemeye çalışıyoruz; bu, süreci belirgin şekilde hızlandırıyor.")],
      ilceler, "kurumsal-kurye.html",
      ("07-musteri/kurumsal-musteri-kurye-cagiriyor.webp","Ofisten telefonla kurye çağıran kurumsal müşteri"))

    S["7-24-kurye.html"] = hizmet_sayfa("7-24-kurye.html","7/24 Kurye Hizmeti",
      "7/24 Kurye İstanbul | Gece ve Hafta Sonu Teslimat — "+AD,
      "İstanbul'da 7 gün 24 saat kurye. Gece 20:00-06:00 ve hafta sonu teslimat. Nöbetçi eczane ve mesai dışı evrak taşıma.",
      "Kesintisiz",
      "Gece, hafta sonu ve resmî tatil fark etmeksizin kurye yönlendiriyoruz. İşiniz mesai saatine sığmadığında da hattımız açık.",
      [("Gece kurye nasıl çalışıyor?",
        ["Gece 20:00 – 06:00 arasındaki teslimatlarda tarifeye 100 ₺ fark ekleniyor. Bunun dışında süreç gündüzle aynı: arıyorsunuz, kurye yönlendiriliyor, gönderi teslim ediliyor.",
         "Gece saatlerinde trafik açık olduğu için teslim süreleri gündüze göre çoğunlukla daha kısa oluyor."]),
       ("Hafta sonu ve tatil",
        ["Cumartesi ve Pazar günleri de çalışıyoruz; bu günlerde tarifeye 100 ₺ fark ekleniyor. Resmî tatillerde de kurye yönlendirmesi yapıyoruz.",
         "Gece ve hafta sonu farkı aynı anda geçerliyse iki fark da tutara eklenir; hesaplayıcı bunu otomatik gösterir."]),
       ("En sık gelen gece talepleri",
        ["Nöbetçi eczaneden ilaç teslimi, 7/24 çalışan ofis ve çağrı merkezlerinin evrak taşımaları, gece vardiyasında biten üretim numunelerinin sevki ve havalimanına yetişmesi gereken gönderiler."])],
      [("Gece tarifesi ne zaman başlıyor?",
        "20:00'de başlar, 06:00'da biter. Bu aralıkta tarifeye 100 ₺ fark eklenir."),
       ("Pazar günü kurye bulabilir miyim?",
        "Evet. Hafta sonu da çalışıyoruz; Cumartesi ve Pazar için 100 ₺ tarife farkı uygulanır."),
       ("Eczane teslimatında gece farkı var mı?",
        "Yok. Eczane kurye sabit 400 ₺'dir; gece ve hafta sonu farkı uygulanmaz.")],
      ilceler, "7-24-kurye.html",
      ("02-motor/gece-bogazici-koprusu-kurye.webp","Gece Boğaziçi Köprüsü üzerinde ilerleyen moto kurye"))
    return S

# ─────────────────────────────────────────────────────── DURAĞAN İÇERİK

def duragan(ilceler):
    D = {}
    D["hakkimizda.html"] = basit_sayfa("hakkimizda.html","Hakkımızda",
      "Hakkımızda | "+AD+" — İstanbul Moto Kurye",
      "Barse Kurye, Kağıthane merkezli bağımsız bir kurye firmasıdır. İstanbul'un 39 ilçesine 7/24 moto kurye hizmeti verir.",
      "Kurumsal",
      f"""<p>Barse Kurye, Kağıthane merkezli bağımsız bir kurye firmasıdır. İstanbul'un 39 ilçesinin tamamına motorlu kurye hizmeti veriyor; Türkiye geneline havayolu kargo, şehirlerarası taşıma ve gümrük evrak taşıma işleri yapıyoruz.</p>
<h2>Ne yapıyoruz?</h2>
<p>İşimiz tek cümleyle şu: bir gönderiyi bulunduğu yerden alıp gitmesi gereken yere, söz verdiğimiz sürede ulaştırmak. Bunu yaparken iki şeye dikkat ediyoruz — fiyatı kurye yola çıkmadan netleştirmek ve gönderi teslim edildiğinde bunu size bildirmek.</p>
<h2>Kimlerle çalışıyoruz?</h2>
<p>Müşterilerimizin büyük kısmı eczaneler, hukuk büroları, muhasebe ofisleri, e-ticaret satıcıları ve şehir içinde düzenli evrak dolaştıran işletmeler. Bunun yanında bireysel gönderiler için de kurye yönlendiriyoruz.</p>
<h2>Çalışma saatlerimiz</h2>
<p>7 gün 24 saat. Gece 20:00 – 06:00 arası ve hafta sonu teslimatlarda tarifeye 100 ₺ fark ekleniyor. Eczane teslimatlarında bu farklar uygulanmıyor.</p>
<h2>İletişim</h2>
<p><strong>Telefon:</strong> <a href="tel:{TEL}">{TEL_GOSTER}</a><br>
<strong>WhatsApp:</strong> <a href="https://wa.me/{WA}" rel="noopener">{TEL_GOSTER}</a><br>
<strong>E-posta:</strong> <a href="mailto:{EPOSTA}">{EPOSTA}</a><br>
<strong>Adres:</strong> {ADRES}, {ILCE_MERKEZ} / İstanbul</p>""",
      ilceler, "hakkimizda.html")

    gizlilik = f"""<p>Bu politika, {SITE} adresini ziyaret ettiğinizde hangi verilerin işlendiğini açıklar.</p>
<h2>Toplanan veriler</h2>
<p>Site ziyaretlerinde teknik nitelikte kayıtlar tutulur: ziyaret zamanı, görüntülenen sayfa, tarayıcı ve işletim sistemi bilgisi ile IP adresi. Bu kayıtlar sitenin güvenliğini sağlamak ve ziyaret istatistiklerini ölçmek için kullanılır.</p>
<p>Fiyat hesaplama aracını kullandığınızda seçtiğiniz alım ve teslim noktası ile hesaplanan tutar kaydedilir. Bu kayıt hizmet kalitesini ölçmek içindir ve kimliğinizle ilişkilendirilmez.</p>
<h2>Çerezler</h2>
<p>Sitede yalnızca sitenin çalışması ve ziyaret istatistikleri için gerekli çerezler kullanılır. Tarayıcı ayarlarınızdan çerezleri reddedebilirsiniz; bu durumda sitenin bazı bölümleri sınırlı çalışabilir.</p>
<h2>Verilerin paylaşımı</h2>
<p>Toplanan veriler üçüncü kişilere satılmaz ve pazarlama amacıyla paylaşılmaz. Yasal olarak zorunlu hâller dışında hiçbir kurumla paylaşılmaz.</p>
<h2>Saklama süresi</h2>
<p>Teknik kayıtlar makul bir süre saklanır ve sonrasında silinir. Talebiniz üzerine size ait kayıtların silinmesi sağlanır.</p>
<h2>İletişim</h2>
<p>Gizlilikle ilgili sorularınız için <a href="mailto:{EPOSTA}">{EPOSTA}</a> adresine yazabilir veya <a href="tel:{TEL}">{TEL_GOSTER}</a> numarasını arayabilirsiniz.</p>"""
    D["gizlilik-politikasi.html"] = basit_sayfa("gizlilik-politikasi.html","Gizlilik Politikası",
      "Gizlilik Politikası | "+AD,
      "Barse Kurye gizlilik politikası: toplanan veriler, çerez kullanımı, saklama süresi ve iletişim bilgileri.",
      "Yasal", gizlilik, ilceler)

    kvkk = f"""<p>6698 sayılı Kişisel Verilerin Korunması Kanunu ("KVKK") uyarınca, veri sorumlusu sıfatıyla {AD} tarafından yapılan bilgilendirmedir.</p>
<h2>Veri sorumlusu</h2>
<p>{AD}<br>{ADRES}, {ILCE_MERKEZ} / İstanbul<br>Telefon: <a href="tel:{TEL}">{TEL_GOSTER}</a> · E-posta: <a href="mailto:{EPOSTA}">{EPOSTA}</a></p>
<h2>İşlenen kişisel veriler</h2>
<p>Kurye hizmeti verebilmek için gönderici ve alıcıya ait ad-soyad, telefon numarası ve adres bilgisi işlenir. Site ziyaretlerinde ayrıca IP adresi ve tarayıcı bilgisi gibi teknik veriler kaydedilir.</p>
<h2>İşleme amaçları</h2>
<p>Veriler; teslimatın planlanması ve gerçekleştirilmesi, gönderi durumunun bildirilmesi, faturalandırma, hizmet kalitesinin ölçülmesi ve yasal yükümlülüklerin yerine getirilmesi amacıyla işlenir.</p>
<h2>Hukuki sebep</h2>
<p>Veriler, sözleşmenin kurulması ve ifası ile veri sorumlusunun hukuki yükümlülüğünü yerine getirmesi hukuki sebeplerine dayanarak işlenir.</p>
<h2>Aktarım</h2>
<p>Kişisel veriler, teslimatın yapılabilmesi için görevlendirilen kurye ile sınırlı olarak paylaşılır. Bunun dışında yasal zorunluluk hâlleri hariç üçüncü kişilere aktarılmaz.</p>
<h2>Haklarınız</h2>
<p>KVKK'nın 11. maddesi uyarınca; kişisel verilerinizin işlenip işlenmediğini öğrenme, işlenmişse buna ilişkin bilgi talep etme, düzeltilmesini veya silinmesini isteme ve işlemenin kanuna aykırı olması hâlinde zararınızın giderilmesini talep etme haklarına sahipsiniz.</p>
<p>Taleplerinizi <a href="mailto:{EPOSTA}">{EPOSTA}</a> adresine iletebilirsiniz.</p>"""
    D["kvkk.html"] = basit_sayfa("kvkk.html","KVKK Aydınlatma Metni",
      "KVKK Aydınlatma Metni | "+AD,
      "Barse Kurye KVKK aydınlatma metni: işlenen kişisel veriler, işleme amaçları, aktarım ve ilgili kişi hakları.",
      "Yasal", kvkk, ilceler)
    return D

def hata_sayfa(ilceler):
    govde = f"""<section class="sec"><div class="wrap" style="text-align:center;max-width:56ch;margin-inline:auto">
<span class="kicker" style="justify-content:center">404</span>
<h1>Bu sayfayı bulamadık</h1>
<p style="font-size:1.1rem;margin:16px 0 28px">Aradığınız sayfa taşınmış veya adres yanlış yazılmış olabilir. Aşağıdan devam edebilirsiniz.</p>
<div class="btns" style="justify-content:center">
<a class="btn btn-1 btn-lg" href="index.html">Ana sayfaya dön</a>
<a class="btn btn-o btn-lg" href="istanbul-ici-kurye.html">Bölgeler</a>
</div>
<p style="margin-top:32px">Acil gönderiniz varsa doğrudan arayın: <a href="tel:{TEL}"><strong>{TEL_GOSTER}</strong></a></p>
</div></section>"""
    h = sayfa("404.html","Sayfa bulunamadı | "+AD,"Aradığınız sayfa bulunamadı. Barse Kurye ana sayfasına dönebilir veya bizi arayabilirsiniz.",govde,"",ilceler)
    return h.replace('<meta name="robots" content="index, follow, max-image-preview:large">',
                     '<meta name="robots" content="noindex, follow">')

# ─────────────────────────────────────────────────────────────── DERLEME

OKU_BENI = """BARSE KURYE — YENİ SİTE
=======================

CPANEL'E NASIL YÜKLENİR
-----------------------
1. cPanel > Dosya Yoneticisi (File Manager) > public_html klasorunu acin.
2. ONCE YEDEK ALIN: public_html icindeki her seyi secip "Compress" ile
   yedek.zip yapin ve indirin. Bir sey ters giderse geri donebilirsiniz.
3. barse-site.zip dosyasini public_html icine yukleyin (Upload).
4. Yuklenen zip'e sag tiklayip "Extract" (Cikart) deyin.
5. Zip dosyasini ve bu OKU-BENI.txt dosyasini silin.
6. Siteyi acip kontrol edin.

ONEMLI: Eski sitedeki PHP dosyalari (panel.php, hesapla.php, hit.php,
sayac.php, takip.php, log-kaydet.php, ziyaret-kaydet.php, bot-koruma.php,
rapor.php, sifirla.php, ziyaretci.php) ve data/ klasoru bu pakette YOK.
Ziyaretci sayacinizi ve panelinizi kullanmaya devam edecekseniz o
dosyalari SILMEYIN - yeni dosyalari uzerine yazin, PHP'ler yerinde kalsin.


NE DEGISTI
----------
- 73 sayfanin tamami yeni tasarimla yeniden yazildi.
- URL'LERIN HICBIRI DEGISMEDI - Google'daki siralamaniz korunur.
- Fiyat hesaplayici aynen korundu (hesap.js'e dokunulmadi).
  Taban 380 TL, eczane sabit 400 TL, gece/hafta sonu +100 TL.
- Her ilce sayfasi artik gercek veriye dayali: merkeze uzaklik,
  ortalama teslim suresi, taban tarife, mahalle listesi, komsu ilceler.
- Mobilde ekranin altinda sabit "Hemen Ara / WhatsApp" cubugu eklendi.
- sitemap.xml, robots.txt ve .htaccess yenilendi.
- Facebook sayfasi ve Google isletme kimligi yapisal veriye eklendi.


TELEFON VEYA ADRES DEGISIRSE
----------------------------
Numaraniz 0534 761 83 88 olarak 73 sayfaya islendi. Degisirse tek tek
duzeltmek yerine haber verin, tum siteyi yeniden uretip gonderelim.


KONTROL LISTESI (yukledikten sonra)
-----------------------------------
[ ] Ana sayfa aciliyor mu?
[ ] Telefon numarasina dokununca arama basliyor mu?
[ ] WhatsApp butonu dogru numaraya gidiyor mu?
[ ] Fiyat hesaplama calisiyor mu? (Levent -> Kadikoy deneyin)
[ ] Bir ilce sayfasi aciliyor mu? (or. kadikoy-kurye.html)
[ ] Olmayan bir adres yazinca 404 sayfasi cikiyor mu?
[ ] Google Search Console'da sitemap.xml'i yeniden gonderin.
"""

HTACCESS = """# Barse Kurye — Apache ayarları
DirectoryIndex index.html
ErrorDocument 404 /404.html
AddDefaultCharset UTF-8

# HTTPS ve www yönlendirmesi (tek URL biçimi)
<IfModule mod_rewrite.c>
  RewriteEngine On
  RewriteCond %{HTTPS} !=on
  RewriteRule ^(.*)$ https://%{HTTP_HOST}/$1 [R=301,L]
  RewriteCond %{HTTP_HOST} ^www\\.(.+)$ [NC]
  RewriteRule ^(.*)$ https://%1/$1 [R=301,L]
</IfModule>

# Sıkıştırma
<IfModule mod_deflate.c>
  AddOutputFilterByType DEFLATE text/html text/css text/plain text/xml application/javascript application/json image/svg+xml
</IfModule>

# Önbellek
<IfModule mod_expires.c>
  ExpiresActive On
  ExpiresByType text/css "access plus 1 year"
  ExpiresByType application/javascript "access plus 1 year"
  ExpiresByType image/webp "access plus 1 year"
  ExpiresByType image/jpeg "access plus 1 year"
  ExpiresByType image/png "access plus 1 year"
  ExpiresByType image/x-icon "access plus 1 year"
  ExpiresByType text/html "access plus 1 hour"
</IfModule>

# Güvenlik başlıkları
<IfModule mod_headers.c>
  Header set X-Content-Type-Options "nosniff"
  Header set Referrer-Policy "strict-origin-when-cross-origin"
  Header set X-Frame-Options "SAMEORIGIN"
</IfModule>
"""

ROBOTS = f"""User-agent: *
Allow: /
Disallow: /data/
Disallow: /panel.php
Disallow: /rapor.php

Sitemap: {SITE}/sitemap.xml
"""

def sitemap(dosyalar):
    from datetime import date
    bugun = date.today().isoformat()
    g = []
    for d in dosyalar:
        if d == '404.html': continue
        loc = f"{SITE}/" if d == 'index.html' else f"{SITE}/{d}"
        oncelik = "1.0" if d == 'index.html' else ("0.9" if d in ('fiyat-hesaplama.html','istanbul-ici-kurye.html') else "0.7")
        g.append(f"  <url>\n    <loc>{loc}</loc>\n    <lastmod>{bugun}</lastmod>\n    <priority>{oncelik}</priority>\n  </url>")
    return '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.w3.org/1999/xhtml/sitemap">\n'.replace(
        'http://www.w3.org/1999/xhtml/sitemap','http://www.sitemaps.org/schemas/sitemap/0.9') + "\n".join(g) + "\n</urlset>\n"

def main():
    pts = nokta_yukle()
    ilceler = ilce_verisi(pts)
    print("• %d nokta, %d ilçe okundu" % (len(pts), len(ilceler)))

    sayfalar = {}
    sayfalar["index.html"] = anasayfa(ilceler)
    sayfalar["istanbul-ici-kurye.html"] = bolgeler_hub(ilceler)
    sayfalar["fiyat-hesaplama.html"] = fiyat_sayfa(ilceler)
    sayfalar.update(hizmet_sayfalari(ilceler))
    sayfalar.update(duragan(ilceler))
    sayfalar["404.html"] = hata_sayfa(ilceler)

    # İlçe sayfaları — bölge fotoğrafı dönüşümlü atanır
    BOLGE_FOTO = [
      ("05-bolge/levent-maslak-kurye.webp","Levent–Maslak plaza hattında kurye teslimatı"),
      ("02-motor/istanbul-trafik-moto-kurye.webp","İstanbul trafiğinde ilerleyen moto kurye"),
      ("05-bolge/kadikoy-moda-kurye.webp","Kadıköy Moda çevresinde kurye teslimatı"),
      ("03-teslimat/eve-paket-teslimat.webp","Apartman girişinde paket teslimi"),
      ("05-bolge/kartal-sanayi-kurye.webp","Kartal sanayi bölgesinde kurye teslimatı"),
      ("02-motor/kurye-portre-sokak.webp","Sokakta gönderiyi teslim almaya hazırlanan kurye"),
      ("05-bolge/perpa-kurye.webp","Perpa Ticaret Merkezi'nde kurye teslimatı"),
      ("04-gece/gece-apartman-teslimat.webp","Gece saatinde apartman girişinde teslimat"),
    ]
    for k, (ad, v) in enumerate(ilceler.items()):
        sayfalar["%s-kurye.html" % v['slug']] = bolge_sayfa("%s-kurye.html" % v['slug'], ad, v, ilceler,
                                                            foto=BOLGE_FOTO[k % len(BOLGE_FOTO)])

    # Semt sayfaları — üst ilçenin verisinden türetilir, noktalar semte göre filtrelenir
    for slug, (ad, ust, filtre) in SEMTLER.items():
        v = dict(ilceler[ust])
        nk = [n for n in ilceler[ust]['noktalar'] if any(f.lower() in n.lower() for f in filtre)]
        if not nk: nk = ilceler[ust]['noktalar'][:8]
        ek = f"Bu sayfa {ust} ilçesine bağlı {ad} çevresini kapsar; aynı ilçedeki diğer noktalar için <a href=\"{ilceler[ust]['slug']}-kurye.html\">{ust} sayfasına</a> bakabilirsiniz."
        sayfalar["%s-kurye.html" % slug] = bolge_sayfa("%s-kurye.html" % slug, ad, v, ilceler,
                                                       ust=ust, noktalar=nk, aciklama_ek=ek,
                                                       foto=BOLGE_FOTO[(len(slug)) % len(BOLGE_FOTO)])

    # Yaz
    if os.path.isdir(CIKTI): shutil.rmtree(CIKTI)
    os.makedirs(CIKTI)
    for d, ic in sayfalar.items():
        open(os.path.join(CIKTI, d), 'w', encoding='utf-8').write(ic)

    os.makedirs(os.path.join(CIKTI, 'assets'), exist_ok=True)
    for f in ('barse.css', 'site.js'):
        shutil.copy(os.path.join(KOK, 'assets', f), os.path.join(CIKTI, 'assets', f))
    shutil.copy(os.path.join(KAYNAK, 'hesap.js'), os.path.join(CIKTI, 'hesap.js'))

    for f in ('favicon.ico','favicon-16x16.png','favicon-32x32.png','favicon-512.png',
              'apple-touch-icon.png','og-image.jpg'):
        k = os.path.join(KAYNAK, f)
        if os.path.exists(k): shutil.copy(k, os.path.join(CIKTI, f))
    if os.path.isdir(os.path.join(KAYNAK, 'images')):
        shutil.copytree(os.path.join(KAYNAK,'images'), os.path.join(CIKTI,'images'))

    open(os.path.join(CIKTI,'OKU-BENI.txt'),'w',encoding='utf-8').write(OKU_BENI)
    open(os.path.join(CIKTI,'.htaccess'),'w',encoding='utf-8').write(HTACCESS)
    open(os.path.join(CIKTI,'robots.txt'),'w',encoding='utf-8').write(ROBOTS)
    open(os.path.join(CIKTI,'sitemap.xml'),'w',encoding='utf-8').write(sitemap(sorted(sayfalar)))

    print("• %d HTML sayfa üretildi" % len(sayfalar))
    return sayfalar

if __name__ == '__main__':
    main()
