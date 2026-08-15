#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Barse Kurye bolge sayfasi ureteci.

Kullanim:  python3 _uretim/uret.py

Yaptiklari
----------
1. fiyat-hesaplama.html icindeki NOKTALAR listesini okur, noktalar_ek.py ile
   birlestirir ve guncellenmis listeyi ayni dosyaya geri yazar.
2. bolgeler.py icindeki her kayit icin barsekurye/<dosya>-kurye.html uretir.
   Mesafe, sure ve ucret degerleri fiyat hesaplayicinin tarifesiyle birebir
   ayni formulden hesaplanir; boylece sayfadaki rakamlarla hesaplayicinin
   verdigi rakam celiskiye dusmez.
3. sitemap.xml dosyasini butun sayfalari ve lastmod bilgisini iceren sekilde
   yeniden yazar.
"""

import json
import math
import os
import re
import sys
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from bolgeler import BOLGELER          # noqa: E402
from hizmetler import HIZMETLER        # noqa: E402
from noktalar_ek import EK_NOKTALAR    # noqa: E402

KOK = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "barsekurye")
SITE = "https://barsekurye.com"
TEL = "0534 761 83 88"
TEL_URI = "+905347618388"
WA = "https://wa.me/905347618388"
BUGUN = date.today().isoformat()

# --- Fiyat tarifesi: fiyat-hesaplama.html ile ayni ---------------------------
TABAN, TABAN_KM, KADEME, KM_YAKIN, KM_UZAK = 380, 5, 25, 14, 11

# --- Rota tablosunda kullanilan sabit hedefler ------------------------------
HEDEFLER = [
    ("Kadıköy", 40.990, 29.028, "N"),
    ("Üsküdar", 41.023, 29.015, "N"),
    ("Ataşehir Finans Merkezi", 40.988, 29.128, "N"),
    ("Ümraniye Şerifali", 41.005, 29.135, "N"),
    ("Kartal Adliye", 40.902, 29.174, "N"),
    ("Levent", 41.082, 29.011, "A"),
    ("Maslak", 41.111, 29.020, "A"),
    ("Mecidiyeköy", 41.067, 28.997, "A"),
    ("Çağlayan Adliyesi", 41.073, 28.981, "A"),
    ("Perpa", 41.062, 28.966, "A"),
    ("Taksim", 41.037, 28.985, "A"),
    ("Bakırköy", 40.980, 28.872, "A"),
    ("İkitelli OSB", 41.078, 28.795, "A"),
    ("İstanbul Otogarı", 41.041, 28.892, "A"),
]
HAVALIMANI = [
    ("Sabiha Gökçen Havalimanı", 40.899, 29.309, "N"),
    ("İstanbul Havalimanı", 41.262, 28.742, "A"),
]

# Bolgeye ozel cekilmis fotograflar: yalnizca kendi bolgelerinde kullanilir.
GORSEL_OZEL = {
    "levent": ("images/04-gece/gece-plaza-levent-teslimat.webp",
               "Levent Büyükdere Caddesi'nde bir plazanın resepsiyonuna gece teslimat yapan Barse kuryesi"),
    "maslak": ("images/05-bolge/levent-maslak-kurye.webp",
               "Maslak plazaları önünde gönderi teslimine hazırlanan Barse moto kuryesi"),
    "zincirlikuyu": ("images/04-gece/gece-ofis-teslimat.webp",
                     "Zincirlikuyu çevresinde akşam saatlerinde ofis teslimatı yapan kurye"),
    "kadikoy-moda": ("images/05-bolge/kadikoy-moda-kurye.webp",
                     "Kadıköy Moda sokaklarında teslimat yapan Barse moto kuryesi"),
    "kadikoy": ("images/05-bolge/kadikoy-moda-kurye.webp",
                "Kadıköy sokaklarında gönderi taşıyan Barse moto kuryesi"),
    "kartal": ("images/05-bolge/kartal-sanayi-kurye.webp",
               "Kartal sanayi bölgesinde teslimat yapan Barse kuryesi"),
    "kartal-merkez": ("images/05-bolge/kartal-sanayi-kurye.webp",
                      "Kartal Merkez çevresinde gönderi teslim eden Barse kuryesi"),
    "perpa": ("images/05-bolge/perpa-kurye.webp",
              "Perpa Ticaret Merkezi girişinde teslimat yapan Barse moto kuryesi"),
    "sisli": ("images/05-bolge/perpa-kurye.webp",
              "Şişli Perpa çevresinde gönderi teslim eden Barse moto kuryesi"),
    "beyoglu": ("images/04-gece/gece-beyoglu-moto-kurye.webp",
                "Beyoğlu sokaklarında gece teslimat yapan Barse moto kuryesi"),
    "taksim-beyoglu": ("images/04-gece/gece-beyoglu-moto-kurye.webp",
                       "Taksim ve Beyoğlu çevresinde gece çalışan Barse moto kuryesi"),
    "besiktas": ("images/02-motor/gece-bogazici-koprusu-kurye.webp",
                 "Boğaziçi Köprüsü üzerinden yaka geçişi yapan Barse moto kuryesi"),
    "uskudar": ("images/02-motor/gece-bogazici-koprusu-kurye.webp",
                "Üsküdar yönünde Boğaz köprüsünden geçen Barse moto kuryesi"),
    "kagithane": ("images/01-ofis/operasyon-merkezi-genel.webp",
                  "Kağıthane'deki Barse Kurye operasyon merkezi ve yönlendirme ekibi"),
    "caglayan": ("images/01-ofis/kurye-cikis-hazirlik.webp",
                 "Çağlayan Adliyesi'ne gidecek dosya için çıkışa hazırlanan Barse kuryesi"),
}

# Genel havuz: her sayfada slug'a gore dondurulerek dagitilir.
GORSEL_HAVUZ = [
    ("images/02-motor/moto-kurye-motosiklet.webp",
     "{ad} bölgesine yönlendirilen Barse Kurye moto kuryesi ve motosikleti"),
    ("images/03-teslimat/kurumsal-ofis-teslimat.webp",
     "{ad} bölgesinde kurumsal bir ofise evrak teslim eden Barse kuryesi"),
    ("images/06-hizmet/express-kurye-sure.webp",
     "{ad} için express kurye hizmetiyle taşınan acil gönderi"),
    ("images/02-motor/istanbul-trafik-moto-kurye.webp",
     "{ad} yönünde İstanbul trafiğinde ilerleyen Barse moto kuryesi"),
    ("images/03-teslimat/eve-paket-teslimat.webp",
     "{ad} bölgesinde bir eve paket teslim eden Barse kuryesi"),
    ("images/06-hizmet/al-ver-kurye-gidis-donus.webp",
     "{ad} bölgesinde al-ver kurye ile gidiş dönüş teslimat"),
    ("images/02-motor/kurye-kask-hazirlik.webp",
     "{ad} teslimatı için kaskını takıp yola çıkan Barse kuryesi"),
    ("images/03-teslimat/depo-fabrika-teslimat.webp",
     "{ad} bölgesinde depo ve fabrika teslimatı yapan Barse kuryesi"),
    ("images/07-musteri/kurumsal-musteri-kurye-cagiriyor.webp",
     "{ad} bölgesindeki bir firmadan Barse Kurye'ye teslimat talebi"),
    ("images/06-hizmet/vip-kurye-ozel-teslimat.webp",
     "{ad} için VIP kurye ile doğrudan yapılan özel teslimat"),
    ("images/03-teslimat/restoran-teslimat.webp",
     "{ad} bölgesinde bir işletmeye yapılan kurye teslimatı"),
    ("images/04-gece/gece-apartman-teslimat.webp",
     "{ad} bölgesinde gece saatlerinde apartman teslimatı"),
]


# ============================================================== turkce ekler
KALIN = set("aıou")
INCE = set("eiöü")
SERT = set("pçtkfhsş")
# Sonu iyelik ekiyle biten adlar kaynastirma "n"si alir: Beyoğlu'nda, Merkezi'ne
N_TAMPON = {"Beyoğlu", "Zeytinburnu", "Kozyatağı", "Taksim ve Beyoğlu",
            "Ataşehir Finans Merkezi", "Bağdat Caddesi", "Beylikdüzü",
            "Nişantaşı", "Zincirlikuyu"}


def _son_sesli(ad):
    for h in reversed(ad.lower()):
        if h in KALIN:
            return "kalın"
        if h in INCE:
            return "ince"
    return "kalın"


def _sert_biter(ad):
    return ad and ad[-1] in SERT


def bulunma(ad):
    """-da / -de / -ta / -te  (Beşiktaş'ta, Kadıköy'de)"""
    if ad in N_TAMPON:
        return "%s'nda" % ad if _son_sesli(ad) == "kalın" else "%s'nde" % ad
    e = ("ta" if _sert_biter(ad) else "da") if _son_sesli(ad) == "kalın" else \
        ("te" if _sert_biter(ad) else "de")
    return "%s'%s" % (ad, e)


def cikma(ad):
    """-dan / -den / -tan / -ten  (Maslak'tan, Kadıköy'den)"""
    if ad in N_TAMPON:
        return "%s'ndan" % ad if _son_sesli(ad) == "kalın" else "%s'nden" % ad
    e = ("tan" if _sert_biter(ad) else "dan") if _son_sesli(ad) == "kalın" else \
        ("ten" if _sert_biter(ad) else "den")
    return "%s'%s" % (ad, e)


def yonelme(ad):
    """-a / -e / -ya / -ye  (Beşiktaş'a, Şile'ye, Beyoğlu'na)"""
    if ad in N_TAMPON:
        return "%s'na" % ad if _son_sesli(ad) == "kalın" else "%s'ne" % ad
    kalin = _son_sesli(ad) == "kalın"
    if ad and ad[-1].lower() in (KALIN | INCE):
        return "%s'ya" % ad if kalin else "%s'ye" % ad
    return "%s'a" % ad if kalin else "%s'e" % ad


# ============================================================== yardimcilar
def kacis(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
             .replace('"', "&quot;"))


def js(s):
    return json.dumps(s, ensure_ascii=False)


def mesafe_km(a, b):
    """fiyat-hesaplama.html icindeki mesafe() fonksiyonunun birebir karsiligi."""
    R, rad = 6371, math.pi / 180
    dlat = (b[0] - a[0]) * rad
    dlon = (b[1] - a[1]) * rad
    h = math.sin(dlat / 2) ** 2 + math.cos(a[0] * rad) * math.cos(b[0] * rad) * math.sin(dlon / 2) ** 2
    km = 2 * R * math.asin(math.sqrt(h)) * 1.4
    if a[2] != b[2]:
        km += 6
    return max(2, round(km))


def taban_fiyat(km, carpan=1.0):
    """Hesaplayicidaki tabanFiyat() + hiz/boyut carpani, 10'a yuvarlanmis."""
    f = TABAN
    if km > TABAN_KM:
        f += (min(km, KADEME) - TABAN_KM) * KM_YAKIN
    if km > KADEME:
        f += (km - KADEME) * KM_UZAK
    return int(round(f * carpan / 10.0) * 10)


def sure(km, yaka_farki):
    """Kapidan kapiya tahmini motor kurye suresi (dakika araligi)."""
    alt = 10 + km * 1.5
    ust = 20 + km * 2.6
    if yaka_farki:
        alt += 8
        ust += 12
    yuvarla = lambda x: int(5 * round(x / 5))
    return max(20, yuvarla(alt)), max(35, yuvarla(ust))


# ============================================================== nokta verisi
def noktalari_yukle():
    yol = os.path.join(KOK, "fiyat-hesaplama.html")
    ham = open(yol, encoding="utf-8").read()
    govde = re.search(r"const NOKTALAR = \[(.*?)\n\];", ham, re.S).group(1)
    satirlar = re.findall(r'\["(.*?)","(.*?)",([\d.]+),([\d.]+),"([AN])"\]', govde)
    liste = [(a, b, float(c), float(d), e) for a, b, c, d, e in satirlar]

    gorulen = {(n[0], n[1]) for n in liste}
    for n in EK_NOKTALAR:
        if (n[0], n[1]) not in gorulen:
            liste.append(n)
            gorulen.add((n[0], n[1]))
    liste.sort(key=lambda n: (n[1], n[0]))
    return liste


def noktalari_geri_yaz(liste):
    """Hesaplayicinin nokta listesini zenginlestirilmis haliyle gunceller."""
    yol = os.path.join(KOK, "fiyat-hesaplama.html")
    ham = open(yol, encoding="utf-8").read()
    govde = "\n".join(
        '  ["%s","%s",%s,%s,"%s"],' % (n[0], n[1], n[2], n[3], n[4]) for n in liste
    ).rstrip(",")
    yeni = re.sub(r"const NOKTALAR = \[.*?\n\];",
                  "const NOKTALAR = [\n%s\n];" % govde, ham, flags=re.S)
    open(yol, "w", encoding="utf-8").write(yeni)
    return len(liste)


# ============================================================== sayfa parcalari
def bas(slug, veri, mahalleler):
    ad = veri["ad"]
    yaka = veri["yaka"]
    dosya = slug + "-kurye.html"
    url = "%s/%s" % (SITE, dosya)

    if veri["tip"] == "ilce":
        baslik = "%s Kurye | Moto Kurye ve Aynı Gün Teslimat – Barse Kurye" % ad
        aciklama = ("%s kurye hizmeti: %s mahallelerinde 7/24 moto kurye, aynı gün ve acil teslimat. "
                    "Süre, güzergâh ve ücret örnekleriyle net bilgi. %s" %
                    (ad, ad, TEL))
    else:
        baslik = "%s Kurye | %s Moto Kurye – Barse Kurye" % (ad, veri["ilce"])
        aciklama = ("%s ve çevresine 7/24 moto kurye hizmeti. %s içindeki ofis, mağaza ve iş merkezlerine "
                    "aynı gün teslimat. Süre ve ücret örnekleriyle: %s" % (ad, veri["ilce"], TEL))
    aciklama = aciklama[:300]

    if slug in GORSEL_OZEL:
        gorsel, gorsel_alt = GORSEL_OZEL[slug]
    else:
        gorsel, gorsel_alt = GORSEL_HAVUZ[sum(ord(c) for c in slug) % len(GORSEL_HAVUZ)]
    return baslik, aciklama, url, dosya, gorsel, gorsel_alt.format(ad=ad)


def sema(slug, veri, baslik, aciklama, url, sss):
    ad = veri["ad"]
    lat, lon = veri["merkez"]
    alan = ("AdministrativeArea" if veri["tip"] == "ilce" else "Place")
    alan_adi = "%s, İstanbul" % ad if veri["tip"] == "ilce" else "%s, %s, İstanbul" % (ad, veri["ilce"])

    hizmet = {
        "@context": "https://schema.org",
        "@type": "Service",
        "serviceType": "Moto kurye ve aynı gün teslimat",
        "name": "%s Kurye Hizmeti" % ad,
        "description": aciklama,
        "url": url,
        "provider": {
            "@type": "LocalBusiness",
            "@id": SITE + "/#organization",
            "name": "Barse Kurye",
            "telephone": "+905347618388",
            "email": "info@barsekurye.com",
            "url": SITE + "/",
            "image": SITE + "/og-image.jpg",
            "priceRange": "₺₺",
            "address": {
                "@type": "PostalAddress",
                "streetAddress": "Talatpaşa Mahallesi, Aydoğan Caddesi No:28 D:3",
                "addressLocality": "Kağıthane",
                "addressRegion": "İstanbul",
                "postalCode": "34400",
                "addressCountry": "TR",
            },
            "openingHoursSpecification": {
                "@type": "OpeningHoursSpecification",
                "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
                "opens": "00:00", "closes": "23:59",
            },
        },
        "areaServed": {
            "@type": alan, "name": alan_adi,
            "geo": {"@type": "GeoCoordinates", "latitude": lat, "longitude": lon},
        },
        "hasOfferCatalog": {
            "@type": "OfferCatalog",
            "name": "%s kurye hizmet seçenekleri" % ad,
            "itemListElement": [
                {"@type": "Offer", "name": "Normal Kurye",
                 "description": "Gün içinde planlı teslimat"},
                {"@type": "Offer", "name": "Express Kurye",
                 "description": "Öncelikli, hızlandırılmış teslimat"},
                {"@type": "Offer", "name": "VIP Kurye",
                 "description": "Gönderiye özel kurye, doğrudan teslimat"},
            ],
        },
    }

    kirinti = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Anasayfa", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": "İstanbul İçi Kurye",
             "item": SITE + "/istanbul-ici-kurye.html"},
            {"@type": "ListItem", "position": 3, "name": "%s Kurye" % ad, "item": url},
        ],
    }

    sorular = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q,
             "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in sss
        ],
    }

    return "\n".join(
        '<script type="application/ld+json">\n%s\n</script>' %
        json.dumps(x, ensure_ascii=False, indent=2) for x in (hizmet, kirinti, sorular)
    )


def rotalar(veri):
    """Bolgeye en yakin hedeflere mesafe, sure ve tahmini ucret tablosu."""
    lat, lon = veri["merkez"]
    yaka = "A" if veri["yaka"] == "Avrupa" else "N"
    kaynak = (lat, lon, yaka)

    olcum = []
    for ad, hlat, hlon, hyaka in HEDEFLER:
        if ad.lower().startswith(veri["ad"].lower()[:6]):
            continue
        km = mesafe_km(kaynak, (hlat, hlon, hyaka))
        olcum.append((km, ad, hyaka))
    olcum.sort()
    secim = olcum[:5]

    # Her sayfada en yakin havalimani da yer alsin: kargo saatine yetisen
    # gonderiler bu sayfalarin en sik gelen sorusu.
    hava = min(
        ((mesafe_km(kaynak, (h[1], h[2], h[3])), h[0], h[3]) for h in HAVALIMANI),
        key=lambda x: x[0],
    )
    if all(hava[1] != s[1] for s in secim):
        secim.append(hava)

    satir = []
    for km, ad, hyaka in secim:
        dk_alt, dk_ust = sure(km, hyaka != yaka)
        satir.append((ad, km, dk_alt, dk_ust, taban_fiyat(km)))
    return satir


def mahalle_listesi(slug, veri, noktalar):
    """Sayfaya yazilacak mahalle/semt adlari."""
    if veri["tip"] == "ilce":
        adlar = [n[0] for n in noktalar if n[1] == veri["ad"]]
    else:
        lat, lon = veri["merkez"]
        yakin = sorted(
            ((mesafe_km((lat, lon, "A"), (n[2], n[3], "A")), n[0]) for n in noktalar
             if n[1] == veri["ilce"]),
            key=lambda x: x[0],
        )
        adlar = [a for _, a in yakin[:14]]
    # "Kadikoy Merkez" gibi ilce adini tekrarlayan kayitlari sadelestir
    temiz, gorulen = [], set()
    for a in adlar:
        k = a.strip()
        if k.lower() in gorulen:
            continue
        gorulen.add(k.lower())
        temiz.append(k)
    return temiz


# ============================================================== sablon
def sayfa(slug, veri, noktalar):
    ad = veri["ad"]
    mahalleler = mahalle_listesi(slug, veri, noktalar)
    baslik, aciklama, url, dosya, gorsel, gorsel_alt = bas(slug, veri, mahalleler)
    rota = rotalar(veri)

    # --- SSS: bolgeye ozgu iki soru + veriden turetilen iki soru ---
    en_yakin = rota[0]
    sss = list(veri["sss"])
    sss.append((
        "%s kurye kaç dakikada gelir?" % bulunma(ad),
        "Talebi aldığımız anda bölgeye en yakın kurye yönlendirilir. %s ve çevresinde alım genellikle "
        "20–40 dakika içinde yapılır; teslim süresi ise mesafeye göre değişir. Örneğin %s yönüne "
        "yaklaşık %d km'lik güzergâhta teslim ortalama %d–%d dakika sürer." %
        (ad, en_yakin[0], en_yakin[1], en_yakin[2], en_yakin[3]),
    ))
    sss.append((
        "%s kurye ücreti ne kadar?" % ad,
        "Ücret mesafeye, teslimat hızına, paket boyutuna ve saate göre belirlenir. İstanbul içi "
        "teslimatlarımız %d ₺ taban ücretten başlar; ilk 5 kilometre bu ücrete dahildir. "
        "%s–%s gibi yaklaşık %d km'lik bir güzergâhta standart tarife tahmini %d ₺ civarındadır. "
        "Kesin fiyat için adresleri iletmeniz yeterli." %
        (TABAN, ad, en_yakin[0], en_yakin[1], en_yakin[4]),
    ))

    # --- parcalar ---
    mahalle_html = "\n".join(
        '        <li>%s <span>kurye</span></li>' % kacis(m) for m in mahalleler
    )
    nokta_html = "\n".join(
        '        <li>%s</li>' % kacis(n) for n in veri["nokta"]
    )
    odak_html = "\n".join(
        "      <li>%s</li>" % kacis(o) for o in veri["odak"]
    )
    rota_html = "\n".join(
        """      <div class="rota-satir">
        <span class="rota-yol"><b>%s</b> → %s</span>
        <span class="rota-km">~%d km</span>
        <span class="rota-dk">%d–%d dk</span>
        <span class="rota-tl">%d ₺'den</span>
      </div>""" % (kacis(ad), kacis(r[0]), r[1], r[2], r[3], r[4]) for r in rota
    )
    sss_html = "\n".join(
        """      <details class="sss-madde"%s>
        <summary>%s</summary>
        <div class="sss-cevap"><p>%s</p></div>
      </details>""" % (" open" if i == 0 else "", kacis(q), kacis(a))
        for i, (q, a) in enumerate(sss)
    )
    komsu_html = "\n".join(
        '        <a href="%s-kurye.html">%s Kurye</a>' % (k, kacis(BOLGELER[k]["ad"]))
        for k in veri["komsu"] if k in BOLGELER
    )

    ust_bolge = ("%s ilçesine bağlı" % veri["ilce"]) if veri["tip"] == "bolge" else "İstanbul %s Yakası" % veri["yaka"]

    return TEMPLATE.format(
        baslik=kacis(baslik), aciklama=kacis(aciklama), url=url, dosya=dosya,
        ad=kacis(ad), ad_da=kacis(bulunma(ad)), ad_dan=kacis(cikma(ad)),
        ad_a=kacis(yonelme(ad)), sema=sema(slug, veri, baslik, aciklama, url, sss),
        giris=kacis(veri["giris"]), ust_bolge=kacis(ust_bolge),
        mahalle_html=mahalle_html, mahalle_sayi=len(mahalleler),
        nokta_html=nokta_html, odak_html=odak_html, rota_html=rota_html,
        sss_html=sss_html, komsu_html=komsu_html,
        gorsel=gorsel, gorsel_alt=kacis(gorsel_alt),
        taban=TABAN, tel=TEL, tel_uri=TEL_URI, wa=WA,
        js_ad=js(veri["ad"]),
    )


TEMPLATE = """<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{baslik}</title>
<meta name="description" content="{aciklama}">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">
<link rel="canonical" href="{url}">
<meta name="geo.region" content="TR-34">
<meta name="geo.placename" content="{ad}, İstanbul">
<meta property="og:type" content="website">
<meta property="og:locale" content="tr_TR">
<meta property="og:site_name" content="Barse Kurye">
<meta property="og:title" content="{baslik}">
<meta property="og:description" content="{aciklama}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="https://barsekurye.com/og-image.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{baslik}">
<meta name="twitter:description" content="{aciklama}">
<meta name="twitter:image" content="https://barsekurye.com/og-image.jpg">
<link rel="icon" type="image/x-icon" href="favicon.ico">
<link rel="icon" type="image/png" sizes="32x32" href="favicon-32x32.png">
<link rel="icon" type="image/png" sizes="16x16" href="favicon-16x16.png">
<link rel="apple-touch-icon" sizes="180x180" href="apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,400..900&family=IBM+Plex+Mono:wght@500;600&family=Public+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="style.css">
<link rel="llms" href="https://barsekurye.com/llms.txt">
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-KWNMNWRF9J"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('consent','default',{{
    analytics_storage:'denied', ad_storage:'denied',
    ad_user_data:'denied', ad_personalization:'denied'
  }});
  gtag('js', new Date());
  gtag('config', 'G-KWNMNWRF9J');
</script>
{sema}
</head>
<body>

<div class="sticky-call"><a href="tel:{tel_uri}">📞 Hemen Ara — {tel}</a></div>

<a href="{wa}" class="whatsapp-float" target="_blank" rel="noopener" aria-label="WhatsApp ile yaz">
  <svg viewBox="0 0 32 32" fill="white" xmlns="http://www.w3.org/2000/svg" aria-hidden="true"><path d="M16 3C8.8 3 3 8.6 3 15.5c0 2.5.8 4.8 2.1 6.8L3 29l7-2c1.8.9 3.8 1.4 6 1.4 7.2 0 13-5.6 13-12.5S23.2 3 16 3zm7.6 17.8c-.3.9-1.7 1.7-2.4 1.8-.6.1-1.4.1-2.2-.1-.5-.2-1.2-.4-2-.8-3.5-1.5-5.8-5-6-5.3-.2-.2-1.4-1.9-1.4-3.6 0-1.7.9-2.6 1.2-2.9.3-.3.7-.4 1-.4h.7c.2 0 .5 0 .8.6.3.7 1 2.4 1.1 2.6.1.2.2.4 0 .7-.1.2-.2.4-.4.6-.2.2-.4.5-.6.6-.2.2-.4.4-.2.8.2.4 1 1.6 2.1 2.6 1.4 1.3 2.6 1.7 3 1.9.4.2.6.1.8-.1.2-.2.9-1 1.1-1.4.2-.4.5-.3.8-.2.3.1 2 1 2.4 1.1.4.2.6.3.7.4.1.2.1 1-.2 1.9z"/></svg>
</a>

<a href="#icerik" class="skip-link">İçeriğe geç</a>
<header>
  <div class="nav">
    <div class="brand"><a href="index.html" style="display:flex;align-items:center;gap:10px;"><span class="dot"></span>BARSE<span style="color:var(--muted);font-weight:600;">KURYE</span></a></div>
    <nav class="links" aria-label="Ana menü">
      <a href="acil-kurye.html">Acil Kurye</a>
      <a href="moto-kurye.html">Moto Kurye</a>
      <a href="kurye-fiyatlari.html">Fiyatlar</a>
      <a href="istanbul-ici-kurye.html">Bölgeler</a>
      <a href="hakkimizda.html">Hakkımızda</a>
    </nav>
    <div class="nav-cta">
      <span class="phone-chip">{tel}</span>
      <a class="btn btn-primary" href="tel:{tel_uri}">Kurye Çağır</a>
    </div>
  </div>
</header>

<main id="icerik">
<section class="district-hero">
  <div class="wrap">
    <nav class="breadcrumb" aria-label="Sayfa yolu"><a href="index.html">Anasayfa</a> / <a href="istanbul-ici-kurye.html">İstanbul İçi Kurye</a> / <span>{ad}</span></nav>
    <div class="eyebrow">{ust_bolge} · 7/24 açık</div>
    <h1>{ad} Kurye</h1>
    <p class="lead">{giris}</p>
    <div class="hero-ctas">
      <a class="btn btn-primary" href="tel:{tel_uri}">Hemen Ara — {tel}</a>
      <a class="btn btn-ghost" href="{wa}" target="_blank" rel="noopener">WhatsApp'tan Yaz</a>
    </div>
  </div>
</section>

<div class="stats">
  <div class="wrap stats-grid">
    <div class="stat"><b>{mahalle_sayi}</b><span>MAHALLE VE SEMT</span></div>
    <div class="stat"><b>30dk</b><span>EN HIZLI TESLİMAT</span></div>
    <div class="stat"><b>7/24</b><span>KESİNTİSİZ HİZMET</span></div>
    <div class="stat"><b>{taban} ₺</b><span>TABAN ÜCRET</span></div>
  </div>
</div>

<section class="section">
  <div class="wrap">
    <div class="kicker">{ad_da} ne taşıyoruz</div>
    <h2>{ad} bölgesinde en çok taşıdığımız gönderiler</h2>
    <p class="sub">Her bölgenin kendine göre bir ritmi var. {ad} tarafında gün içinde en sık karşımıza çıkan işler bunlar.</p>
    <ul class="odak-liste">
{odak_html}
    </ul>

    <figure class="bolge-gorsel">
      <img src="{gorsel}" alt="{gorsel_alt}" loading="lazy" decoding="async" width="1408" height="768">
      <figcaption>{ad} ve çevresinde teslimatlar 7/24 moto kurye ekibimizle yapılır.</figcaption>
    </figure>
  </div>
</section>

<section class="section" id="hizmetler" style="background:var(--bg-2);border-block:1px solid var(--line);">
  <div class="wrap">
    <div class="kicker">Teslimat hızı</div>
    <h2>{ad} için üç farklı hız</h2>
    <p class="sub">Gönderinizin aciliyetine göre seçin; üçünde de aynı kurye kalitesi ve aynı takip düzeni geçerli.</p>
    <div class="services">
      <div class="svc">
        <div class="tag">EKONOMİK</div>
        <h3>Normal Kurye</h3>
        <p>Gün içinde teslim edilmesi yeterli olan evrak ve paketler için planlı, en uygun maliyetli seçenek.</p>
        <div class="time"><span>120–180 dk</span><span class="arrow">→</span></div>
      </div>
      <div class="svc">
        <div class="tag">ÖNCELİKLİ</div>
        <h3>Express Kurye</h3>
        <p>{ad} bölgesindeki en yakın kurye öncelikli olarak yönlendirilir, teslimat sıraya girmez.</p>
        <div class="time"><span>60–90 dk</span><span class="arrow">→</span></div>
      </div>
      <div class="svc">
        <div class="tag">EN HIZLI</div>
        <h3>VIP Kurye</h3>
        <p>Gönderinize özel kurye atanır; yol boyunca başka hiçbir adrese uğramadan doğrudan teslimata gider.</p>
        <div class="time"><span>30–60 dk</span><span class="arrow">→</span></div>
      </div>
    </div>
  </div>
</section>

<section class="section" id="mahalleler">
  <div class="wrap">
    <div class="kicker">Hizmet alanı</div>
    <h2>{ad} genelinde kurye hizmeti verdiğimiz noktalar</h2>
    <p class="sub">Aşağıdaki mahalle ve semtlerin tamamına alım ve teslim yapıyoruz. Listede göremediğiniz bir adres varsa da çıkıyoruz; arayıp sormanız yeterli.</p>
    <ul class="mahalle-grid">
{mahalle_html}
    </ul>
  </div>
</section>

<section class="section" id="noktalar" style="background:var(--bg-2);border-block:1px solid var(--line);">
  <div class="wrap">
    <div class="ikili">
      <div>
        <div class="kicker">Sık gidilen adresler</div>
        <h2>{ad_da} en çok teslimat yaptığımız yerler</h2>
        <p class="sub">Bu noktalarda giriş prosedürünü, otoparkı ve teslim akışını zaten biliyoruz; bu da her seferinde birkaç dakika kazandırıyor.</p>
      </div>
      <ul class="nokta-liste">
{nokta_html}
      </ul>
    </div>
  </div>
</section>

<section class="section" id="sure-fiyat">
  <div class="wrap">
    <div class="kicker">Süre ve ücret</div>
    <h2>{ad_dan} çıkan gönderilerde tahmini süre ve ücret</h2>
    <p class="sub">Aşağıdaki rakamlar hafta içi gündüz saatleri, standart paket ve normal tarife içindir. Mesafe ve ücret, fiyat hesaplayıcımızla aynı formülden hesaplanır.</p>
    <div class="rota-tablo">
      <div class="rota-satir rota-bas">
        <span class="rota-yol">Güzergâh</span>
        <span class="rota-km">Mesafe</span>
        <span class="rota-dk">Süre</span>
        <span class="rota-tl">Ücret</span>
      </div>
{rota_html}
    </div>
    <p class="rota-not">Gece (20:00–06:00) ve hafta sonu tarifesi ile hacimli gönderilerde ücret farklılaşır.
      Kesin fiyat için <a href="kurye-fiyatlari.html">kurye fiyatları</a> sayfamıza bakabilir ya da
      <a href="fiyat-hesaplama.html">fiyat hesaplama</a> aracını kullanabilirsiniz.</p>
    <div class="hero-ctas" style="margin-top:26px;">
      <a class="btn btn-primary" href="tel:{tel_uri}">Net fiyat için ara</a>
      <a class="btn btn-ghost" href="fiyat-hesaplama.html">Fiyat hesapla</a>
    </div>
  </div>
</section>

<section class="section" id="sss" style="background:var(--bg-2);border-block:1px solid var(--line);">
  <div class="wrap">
    <div class="kicker">Sık sorulanlar</div>
    <h2>{ad} kurye hizmeti hakkında sorular</h2>
    <div class="sss-liste">
{sss_html}
    </div>
  </div>
</section>

<section class="section" id="komsu">
  <div class="wrap">
    <div class="kicker">Yakın bölgeler</div>
    <h2>{ad} çevresinde hizmet verdiğimiz diğer bölgeler</h2>
    <div class="komsu-liste">
{komsu_html}
    </div>
    <div class="komsu-liste komsu-hizmet">
      <a href="acil-kurye.html">Acil Kurye</a>
      <a href="7-24-kurye.html">7/24 Kurye</a>
      <a href="moto-kurye.html">Moto Kurye</a>
      <a href="eczane-kurye.html">Eczane Kurye</a>
      <a href="kurumsal-kurye.html">Kurumsal Kurye</a>
      <a href="istanbul-ici-kurye.html">Tüm İlçeler</a>
    </div>
  </div>
</section>

<section class="cta-strip" id="talep">
  <div class="wrap">
    <h2>{ad_a} kurye mi lazım?</h2>
    <p>Alım ve teslim adresini söyleyin; net fiyatı dakikalar içinde verelim, kuryeyi hemen yönlendirelim.</p>
    <div class="cta-buttons">
      <a class="btn btn-primary" href="tel:{tel_uri}">📞 {tel}</a>
      <a class="btn btn-ghost" href="{wa}" target="_blank" rel="noopener">WhatsApp ile Talep Et</a>
    </div>
  </div>
</section>
</main>

<footer id="iletisim">
  <div class="wrap">
    <div class="foot-grid">
      <div>
        <div class="brand" style="margin-bottom:14px;"><span class="dot"></span>BARSE<span style="color:var(--muted);font-weight:600;">KURYE</span></div>
        <p style="color:var(--muted);font-size:0.88rem;max-width:32ch;">İstanbul genelinde hızlı, güvenli ve planlı moto kurye hizmeti.</p>
        <div class="sosyal-linkler">
          <a href="https://www.instagram.com/barsekurye" target="_blank" rel="noopener" aria-label="Instagram">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1" fill="currentColor" stroke="none"/></svg>
          </a>
          <a href="https://www.facebook.com/61592544492045" target="_blank" rel="noopener" aria-label="Facebook">
            <svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M14 9h3V6h-3c-2.2 0-4 1.8-4 4v2H8v3h2v7h3v-7h3l1-3h-4v-2c0-.6.4-1 1-1z"/></svg>
          </a>
          <a href="{wa}" target="_blank" rel="noopener" aria-label="WhatsApp">
            <svg viewBox="0 0 32 32" fill="currentColor" aria-hidden="true"><path d="M16 3C8.8 3 3 8.6 3 15.5c0 2.5.8 4.8 2.1 6.8L3 29l7-2c1.8.9 3.8 1.4 6 1.4 7.2 0 13-5.6 13-12.5S23.2 3 16 3zm7.6 17.8c-.3.9-1.7 1.7-2.4 1.8-.6.1-1.4.1-2.2-.1-.5-.2-1.2-.4-2-.8-3.5-1.5-5.8-5-6-5.3-.2-.2-1.4-1.9-1.4-3.6 0-1.7.9-2.6 1.2-2.9.3-.3.7-.4 1-.4h.7c.2 0 .5 0 .8.6.3.7 1 2.4 1.1 2.6.1.2.2.4 0 .7-.1.2-.2.4-.4.6-.2.2-.4.5-.6.6-.2.2-.4.4-.2.8.2.4 1 1.6 2.1 2.6 1.4 1.3 2.6 1.7 3 1.9.4.2.6.1.8-.1.2-.2.9-1 1.1-1.4.2-.4.5-.3.8-.2.3.1 2 1 2.4 1.1.4.2.6.3.7.4.1.2.1 1-.2 1.9z"/></svg>
          </a>
        </div>
      </div>
      <div>
        <h3>Hizmetlerimiz</h3>
        <ul>
          <li><a href="acil-kurye.html">Acil Kurye</a></li>
          <li><a href="7-24-kurye.html">7/24 Kurye</a></li>
          <li><a href="moto-kurye.html">Moto Kurye</a></li>
          <li><a href="eczane-kurye.html">Eczane Kurye</a></li>
          <li><a href="kurumsal-kurye.html">Kurumsal Kurye</a></li>
        </ul>
      </div>
      <div>
        <h3>Kurumsal</h3>
        <ul>
          <li><a href="index.html">Anasayfa</a></li>
          <li><a href="hakkimizda.html">Hakkımızda</a></li>
          <li><a href="istanbul-ici-kurye.html">Tüm İlçeler</a></li>
          <li><a href="kurye-fiyatlari.html">Kurye Fiyatları</a></li>
          <li><a href="fiyat-hesaplama.html">Fiyat Hesaplama</a></li>
        </ul>
      </div>
      <div>
        <h3>İletişim</h3>
        <ul>
          <li><a href="tel:{tel_uri}">{tel}</a></li>
          <li><a href="mailto:info@barsekurye.com">info@barsekurye.com</a></li>
          <li><a href="https://www.google.com/maps/search/?api=1&amp;query=Talatpa%C5%9Fa+Mahallesi+Ayd%C4%9Fo%C4%9Fan+Caddesi+No%3A28+D%3A3+Ka%C4%9F%C4%B1thane+%C4%B0stanbul" target="_blank" rel="noopener">Talatpaşa Mah. Aydoğan Cad. No:28 D:3, Kağıthane / İstanbul</a></li>
        </ul>
      </div>
    </div>
    <div class="foot-bottom">
      <span>© 2026 Barse Kurye. Tüm hakları saklıdır.</span>
      <span><a href="kvkk.html">KVKK</a> · <a href="gizlilik-politikasi.html">Gizlilik Politikası</a></span>
    </div>
  </div>
</footer>
<script>window.VARSAYILAN_ILCE = {js_ad};</script>
<script>
(function(){{
  try{{
    var p = new URLSearchParams(location.search);
    var g = p.get('gclid');
    if(!g) return;
    if(sessionStorage.getItem('bk_hit')) return;
    sessionStorage.setItem('bk_hit','1');
    var q = 'gclid=' + encodeURIComponent(g)
          + '&kelime=' + encodeURIComponent(p.get('keyword') || p.get('utm_term') || '')
          + '&sayfa=' + encodeURIComponent(location.pathname);
    fetch('hit.php?' + q, {{keepalive:true}}).catch(function(){{}});
  }}catch(e){{}}
}})();
</script>
<script>
(function(){{
  try{{
    var q = 'sayfa=' + encodeURIComponent(location.pathname)
          + '&ref=' + encodeURIComponent(document.referrer || '');
    fetch('/ziyaret-kaydet.php?' + q, {{keepalive:true}}).catch(function(){{}});
  }}catch(e){{}}
}})();
</script>
<div class="cerez-kutu" id="cerezKutu" hidden>
  <div class="cerez-metin">
    Bu sitede deneyimi geliştirmek ve ziyaret istatistiklerini ölçmek için çerezler kullanılıyor.
    Ayrıntılar için <a href="gizlilik-politikasi.html">Gizlilik Politikası</a> sayfamıza bakabilirsiniz.
  </div>
  <div class="cerez-butonlar">
    <button type="button" class="cerez-btn cerez-red" id="cerezRed">Reddet</button>
    <button type="button" class="cerez-btn cerez-kabul" id="cerezKabul">Kabul Et</button>
  </div>
</div>
<script>
(function(){{
  var K='bk_cerez';
  function izinGuncelle(durum){{
    if (typeof gtag === 'function') {{
      gtag('consent','update',{{
        analytics_storage: durum, ad_storage: durum,
        ad_user_data: durum, ad_personalization: durum
      }});
    }}
  }}
  function kapat(){{ var k=document.getElementById('cerezKutu'); if(k) k.hidden=true; }}
  try{{
    var secim = localStorage.getItem(K);
    if (secim === 'kabul') {{ izinGuncelle('granted'); }}
    else if (secim !== 'red') {{
      var k=document.getElementById('cerezKutu'); if(k) k.hidden=false;
    }}
    var kb=document.getElementById('cerezKabul');
    var rd=document.getElementById('cerezRed');
    if(kb) kb.addEventListener('click',function(){{ try{{localStorage.setItem(K,'kabul');}}catch(e){{}} izinGuncelle('granted'); kapat(); }});
    if(rd) rd.addEventListener('click',function(){{ try{{localStorage.setItem(K,'red');}}catch(e){{}} izinGuncelle('denied'); kapat(); }});
  }}catch(e){{}}
}})();
</script>
</body>
</html>
"""


# ============================================================== fiyat sayfasi
# Hesaplayicidaki carpanlarla birebir ayni
HIZ = [("Normal", 1.00, "90 dk – 2 saat"),
       ("Express", 1.25, "45 – 60 dakika"),
       ("VIP", 1.60, "30 – 45 dakika")]
BOYUT = [("Zarf / dosya", 1.00, "Ek ücret yok"),
         ("Küçük paket", 1.10, "Ayakkabı kutusu boyutu"),
         ("Orta paket", 1.21, "Sırt çantası boyutu"),
         ("Büyük paket", 1.33, "Koli"),
         ("Çanta üstü", 1.46, "Hacimli gönderi")]
KM_BANT = [3, 5, 8, 10, 15, 20, 25, 30, 40, 50]
ORNEK_ROTA = [
    ("Kağıthane", "Levent"), ("Kadıköy", "Ataşehir Finans Merkezi"),
    ("Şişli", "Beşiktaş"), ("Mecidiyeköy", "Kadıköy"),
    ("Levent", "Ümraniye Şerifali"), ("Bakırköy", "Şişli"),
    ("İkitelli OSB", "Perpa"), ("Ataşehir Finans Merkezi", "Maslak"),
    ("Kartal Adliye", "Kadıköy"), ("Pendik", "Kadıköy"),
    ("Beyoğlu", "Üsküdar"), ("Başakşehir", "İstanbul Havalimanı"),
]
ROTA_KONUM = {
    "Kağıthane": (41.081, 28.972, "A"), "Levent": (41.082, 29.011, "A"),
    "Kadıköy": (40.990, 29.028, "N"), "Ataşehir Finans Merkezi": (40.988, 29.128, "N"),
    "Şişli": (41.060, 28.987, "A"), "Beşiktaş": (41.043, 29.008, "A"),
    "Mecidiyeköy": (41.067, 28.997, "A"), "Ümraniye Şerifali": (41.005, 29.135, "N"),
    "Bakırköy": (40.980, 28.872, "A"), "İkitelli OSB": (41.078, 28.795, "A"),
    "Perpa": (41.062, 28.966, "A"), "Maslak": (41.111, 29.020, "A"),
    "Kartal Adliye": (40.902, 29.174, "N"), "Pendik": (40.877, 29.234, "N"),
    "Beyoğlu": (41.033, 28.977, "A"), "Üsküdar": (41.023, 29.015, "N"),
    "Başakşehir": (41.093, 28.802, "A"), "İstanbul Havalimanı": (41.262, 28.742, "A"),
}

FIYAT_SSS = [
    ("İstanbul'da kurye ücreti ne kadar?",
     "Barse Kurye'de İstanbul içi teslimatlar %d ₺ taban ücretten başlar ve ilk 5 kilometre bu ücrete dahildir. "
     "5 kilometreden sonrası kilometre başına ücretlendirilir; 25 kilometreden sonra kilometre ücreti düşer. "
     "Örneğin 10 kilometrelik bir teslimat %d ₺, 20 kilometrelik bir teslimat %d ₺ civarındadır." %
     (TABAN, taban_fiyat(10), taban_fiyat(20))),
    ("Express ve VIP kurye ne kadar fark ettiriyor?",
     "Express kurye normal tarifenin 1,25 katı, VIP kurye ise 1,6 katıdır. Express'te gönderiniz sıraya "
     "girmeden önceliklendirilir; VIP'te ise gönderiye özel kurye atanır ve kurye başka hiçbir adrese uğramaz."),
    ("Gece ve hafta sonu kurye fiyatları değişiyor mu?",
     "Evet. 20:00 – 06:00 arası gece tarifesinde +100 ₺, Cumartesi ve Pazar günlerinde +100 ₺ fark uygulanır. "
     "Hafta sonu gece saatlerinde bu iki fark birlikte geçerli olur."),
    ("Paket boyutu fiyatı nasıl etkiliyor?",
     "Zarf ve dosya için ek ücret yoktur. Küçük paketten çanta üstü hacimli gönderiye doğru ücret kademeli "
     "olarak artar: küçük pakette %%10, orta pakette %%21, büyük pakette %%33, çanta üstü gönderide %%46."),
    ("Al-ver (gidiş-dönüş) teslimat nasıl ücretlendiriliyor?",
     "Kuryenin adreste bekleyip evrakı geri getirdiği al-ver işlerde ücret normal tarifenin 1,7 katıdır. "
     "İlk 15 dakikalık bekleme ücretsizdir."),
    ("Eczane kurye ücreti ne kadar?",
     "Eczane teslimatları sabit %d ₺'dir; mesafe, hız ve paket boyutu farkı uygulanmaz. Reçeteli ilaç "
     "gönderileri öncelikli olarak yönlendirilir." % 400),
    ("Kurye fiyatına KDV dahil mi, fatura kesiliyor mu?",
     "Kurumsal müşterilerimize fatura düzenliyoruz. Sözleşmeli çalışan firmalar için aylık toplu faturalandırma "
     "ve gönderi hacmine göre indirimli tarife uygulanabiliyor."),
    ("Şehirler arası ve uçak kurye fiyatı nasıl belirleniyor?",
     "Şehirler arası gönderilerde ücret; İstanbul içi alım, seçilen aktarma yöntemi (uçak kargo, otobüs) ve "
     "varış şehrindeki teslimat kalemlerinden oluşur. Güzergâhı ilettiğinizde net fiyatı dakikalar içinde veriyoruz."),
]


def fiyat_sayfasi():
    url = SITE + "/kurye-fiyatlari.html"
    baslik = "Kurye Fiyatları 2026 | İstanbul Moto Kurye Ücretleri – Barse Kurye"
    aciklama = ("İstanbul kurye fiyatları 2026: %d ₺ taban ücret, kilometre kademeleri, express ve VIP "
                "farkı, gece ve hafta sonu tarifesi. Güncel fiyat tablosu ve örnek güzergâh ücretleri." % TABAN)

    bant = "\n".join(
        """      <div class="rota-satir">
        <span class="rota-yol"><b>%s km</b>%s</span>
        <span class="rota-km">%s ₺</span>
        <span class="rota-dk">%s ₺</span>
        <span class="rota-tl">%s ₺</span>
      </div>""" % (km, " <small>(taban ücret)</small>" if km <= TABAN_KM else "",
                   taban_fiyat(km), taban_fiyat(km, 1.25), taban_fiyat(km, 1.60))
        for km in KM_BANT
    )

    ornek = []
    for a, b in ORNEK_ROTA:
        ka, kb = ROTA_KONUM[a], ROTA_KONUM[b]
        km = mesafe_km(ka, kb)
        dk_alt, dk_ust = sure(km, ka[2] != kb[2])
        ornek.append(
            """      <div class="rota-satir">
        <span class="rota-yol"><b>%s</b> → %s</span>
        <span class="rota-km">~%d km</span>
        <span class="rota-dk">%d–%d dk</span>
        <span class="rota-tl">%d ₺'den</span>
      </div>""" % (kacis(a), kacis(b), km, dk_alt, dk_ust, taban_fiyat(km)))
    ornek = "\n".join(ornek)

    hiz_html = "\n".join(
        """      <div class="rota-satir">
        <span class="rota-yol"><b>%s Kurye</b> — %s</span>
        <span class="rota-km">×%s</span>
        <span class="rota-tl">%d ₺'den</span>
      </div>""" % (ad, sur, ("%.2f" % c).replace(".", ","), taban_fiyat(TABAN_KM, c))
        for ad, c, sur in HIZ
    )
    boyut_html = "\n".join(
        """      <div class="rota-satir">
        <span class="rota-yol"><b>%s</b> — %s</span>
        <span class="rota-km">×%s</span>
        <span class="rota-tl">%s</span>
      </div>""" % (ad, not_, ("%.2f" % c).replace(".", ","),
                   "Ek ücret yok" if c == 1 else "+%%%d" % round((c - 1) * 100))
        for ad, c, not_ in BOYUT
    )
    sss_html = "\n".join(
        """      <details class="sss-madde"%s>
        <summary>%s</summary>
        <div class="sss-cevap"><p>%s</p></div>
      </details>""" % (" open" if i == 0 else "", kacis(q), kacis(a))
        for i, (q, a) in enumerate(FIYAT_SSS)
    )

    semalar = [
        {
            "@context": "https://schema.org", "@type": "Service",
            "serviceType": "Moto kurye", "name": "İstanbul Kurye Hizmeti Fiyatlandırması",
            "url": url, "description": aciklama,
            "provider": {"@type": "LocalBusiness", "@id": SITE + "/#organization", "name": "Barse Kurye",
                         "telephone": "+905347618388"},
            "areaServed": {"@type": "City", "name": "İstanbul"},
            "offers": {
                "@type": "Offer", "priceCurrency": "TRY",
                "priceSpecification": {
                    "@type": "PriceSpecification", "priceCurrency": "TRY",
                    "minPrice": TABAN,
                    "description": "İlk 5 kilometreye kadar taban ücret; sonrası kilometre başına hesaplanır.",
                },
                "availability": "https://schema.org/InStock",
            },
        },
        {
            "@context": "https://schema.org", "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Anasayfa", "item": SITE + "/"},
                {"@type": "ListItem", "position": 2, "name": "Kurye Fiyatları", "item": url},
            ],
        },
        {
            "@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q,
                            "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FIYAT_SSS],
        },
    ]
    sema_html = "\n".join('<script type="application/ld+json">\n%s\n</script>' %
                          json.dumps(x, ensure_ascii=False, indent=2) for x in semalar)

    govde = FIYAT_GOVDE.format(
        taban=TABAN, bant=bant, ornek=ornek, hiz_html=hiz_html, boyut_html=boyut_html,
        sss_html=sss_html, tel=TEL, tel_uri=TEL_URI, wa=WA,
        eczane=400, durak=150, gece=100,
    )
    html = cerceve(baslik, aciklama, url, sema_html, govde, "İstanbul", "Kurye Fiyatları")
    open(os.path.join(KOK, "kurye-fiyatlari.html"), "w", encoding="utf-8").write(html)


FIYAT_GOVDE = """<section class="district-hero">
  <div class="wrap">
    <nav class="breadcrumb" aria-label="Sayfa yolu"><a href="index.html">Anasayfa</a> / <span>Kurye Fiyatları</span></nav>
    <div class="eyebrow">2026 güncel tarife · 7/24 açık</div>
    <h1>Kurye Fiyatları 2026</h1>
    <p class="lead">İstanbul içi moto kurye teslimatlarımız <strong>{taban} ₺</strong> taban ücretten başlar ve ilk 5 kilometre bu ücrete dahildir.
      Aşağıdaki tabloların tamamı, fiyat hesaplama aracımızın kullandığı tarifenin birebir aynısıdır; sürpriz kalem yoktur.</p>
    <div class="hero-ctas">
      <a class="btn btn-primary" href="fiyat-hesaplama.html">Kendi güzergâhını hesapla</a>
      <a class="btn btn-ghost" href="tel:{tel_uri}">Net fiyat için ara</a>
    </div>
  </div>
</section>

<div class="stats">
  <div class="wrap stats-grid">
    <div class="stat"><b>{taban} ₺</b><span>TABAN ÜCRET</span></div>
    <div class="stat"><b>5 km</b><span>ÜCRETE DAHİL MESAFE</span></div>
    <div class="stat"><b>7/24</b><span>KESİNTİSİZ HİZMET</span></div>
    <div class="stat"><b>39</b><span>İLÇEDE HİZMET</span></div>
  </div>
</div>

<section class="section" id="mesafe">
  <div class="wrap">
    <div class="kicker">Mesafeye göre</div>
    <h2>Kilometreye göre kurye fiyatları</h2>
    <p class="sub">Hafta içi 06:00 – 20:00 arası, zarf/dosya boyutunda gönderi içindir. Mesafe, alım ve teslim
      noktası arasındaki gerçek güzergâh üzerinden hesaplanır; yaka geçişlerinde köprü güzergâhı eklenir.</p>
    <div class="rota-tablo">
      <div class="rota-satir rota-bas">
        <span class="rota-yol">Mesafe</span>
        <span class="rota-km">Normal</span>
        <span class="rota-dk">Express</span>
        <span class="rota-tl">VIP</span>
      </div>
{bant}
    </div>
    <p class="rota-not">İlk 5 kilometre taban ücrete dahildir. 5 – 25 km arası kilometre başına ilave ücret alınır;
      25 kilometreden sonra kilometre ücreti kademeli olarak düşer, yani uzun mesafede kilometre başı maliyet azalır.</p>
  </div>
</section>

<section class="section" id="hiz" style="background:var(--bg-2);border-block:1px solid var(--line);">
  <div class="wrap">
    <div class="kicker">Teslimat hızı</div>
    <h2>Normal, Express ve VIP kurye farkı</h2>
    <p class="sub">Üç seçenekte de aynı ekip ve aynı takip düzeni geçerli; değişen tek şey gönderinizin önceliği.
      Aşağıdaki başlangıç tutarları 5 kilometreye kadar olan teslimatlar içindir.</p>
    <div class="rota-tablo">
      <div class="rota-satir rota-bas">
        <span class="rota-yol">Hizmet</span>
        <span class="rota-km">Çarpan</span>
        <span class="rota-tl">Başlangıç</span>
      </div>
{hiz_html}
    </div>
  </div>
</section>

<section class="section" id="boyut">
  <div class="wrap">
    <div class="kicker">Paket boyutu</div>
    <h2>Gönderi boyutuna göre ücret farkı</h2>
    <p class="sub">Zarf ve dosya gönderilerinde ek ücret yoktur. Hacim büyüdükçe ücret kademeli olarak artar.</p>
    <div class="rota-tablo">
      <div class="rota-satir rota-bas">
        <span class="rota-yol">Boyut</span>
        <span class="rota-km">Çarpan</span>
        <span class="rota-tl">Fark</span>
      </div>
{boyut_html}
    </div>
  </div>
</section>

<section class="section" id="zaman" style="background:var(--bg-2);border-block:1px solid var(--line);">
  <div class="wrap">
    <div class="ikili">
      <div>
        <div class="kicker">Saat ve gün</div>
        <h2>Gece ve hafta sonu tarifesi</h2>
        <p class="sub">Gece ve hafta sonu farkları sabit tutardır; yüzde üzerinden artmaz. İki durum
          birlikte geçerliyse farklar toplanır.</p>
      </div>
      <ul class="nokta-liste">
        <li>Hafta içi 06:00 – 20:00 → fark yok</li>
        <li>Hafta içi 20:00 – 06:00 → +{gece} ₺</li>
        <li>Cumartesi ve Pazar (gündüz) → +{gece} ₺</li>
        <li>Cumartesi ve Pazar (gece) → +{gece} ₺ + {gece} ₺</li>
        <li>Ek durak / uğrama → +{durak} ₺</li>
        <li>Al-ver (gidiş-dönüş, kurye bekler) → ×1,7</li>
        <li>Eczane kurye → sabit {eczane} ₺</li>
      </ul>
    </div>
  </div>
</section>

<section class="section" id="ornek">
  <div class="wrap">
    <div class="kicker">Örnek güzergâhlar</div>
    <h2>İstanbul'da sık kullanılan güzergâhlarda kurye ücreti</h2>
    <p class="sub">Aşağıdaki tutarlar normal tarife, zarf/dosya boyutu ve hafta içi gündüz saatleri içindir.
      Kendi adreslerinizle hesaplamak için fiyat hesaplama aracını kullanabilirsiniz.</p>
    <div class="rota-tablo">
      <div class="rota-satir rota-bas">
        <span class="rota-yol">Güzergâh</span>
        <span class="rota-km">Mesafe</span>
        <span class="rota-dk">Süre</span>
        <span class="rota-tl">Ücret</span>
      </div>
{ornek}
    </div>
    <div class="hero-ctas" style="margin-top:26px;">
      <a class="btn btn-primary" href="fiyat-hesaplama.html">Fiyat hesapla</a>
      <a class="btn btn-ghost" href="istanbul-ici-kurye.html">İlçe sayfalarına göz at</a>
    </div>
  </div>
</section>

<section class="section" id="sss" style="background:var(--bg-2);border-block:1px solid var(--line);">
  <div class="wrap">
    <div class="kicker">Sık sorulanlar</div>
    <h2>Kurye fiyatları hakkında sorular</h2>
    <div class="sss-liste">
{sss_html}
    </div>
  </div>
</section>

<section class="cta-strip" id="talep">
  <div class="wrap">
    <h2>Net fiyat mı istiyorsunuz?</h2>
    <p>Alım ve teslim adresini iletin; kesin tutarı dakikalar içinde söyleyelim.</p>
    <div class="cta-buttons">
      <a class="btn btn-primary" href="tel:{tel_uri}">📞 {tel}</a>
      <a class="btn btn-ghost" href="{wa}" target="_blank" rel="noopener">WhatsApp ile Talep Et</a>
    </div>
  </div>
</section>
"""


# ============================================================== hizmet sayfalari
def blok_html(blok):
    tip = blok[0]
    if tip == "metin":
        _, kicker, h2, paragraflar = blok
        return """    <div class="kicker">%s</div>
    <h2>%s</h2>
    <div class="info-block">
%s
    </div>""" % (kacis(kicker), kacis(h2),
                 "\n".join("      <p>%s</p>" % kacis(p) for p in paragraflar))

    if tip == "kartlar":
        _, kicker, h2, alt, kartlar = blok
        sinif = "services services-4" if len(kartlar) == 4 else "services"
        return """    <div class="kicker">%s</div>
    <h2>%s</h2>
    <p class="sub">%s</p>
    <div class="%s">
%s
    </div>""" % (kacis(kicker), kacis(h2), kacis(alt), sinif, "\n".join(
            """      <div class="svc">
        <div class="tag">%s</div>
        <h3>%s</h3>
        <p>%s</p>
      </div>""" % (kacis(e), kacis(b), kacis(m)) for e, b, m in kartlar))

    if tip == "liste":
        _, kicker, h2, alt, maddeler = blok
        return """    <div class="ikili">
      <div>
        <div class="kicker">%s</div>
        <h2>%s</h2>
        <p class="sub">%s</p>
      </div>
      <ul class="nokta-liste">
%s
      </ul>
    </div>""" % (kacis(kicker), kacis(h2), kacis(alt),
                 "\n".join("        <li>%s</li>" % kacis(m) for m in maddeler))

    if tip == "tablo":
        _, kicker, h2, alt, basliklar, satirlar = blok
        sinif = ["rota-yol", "rota-km", "rota-dk", "rota-tl"]

        def satir(hucreler, bas=False):
            ic = "\n".join('        <span class="%s">%s</span>' % (sinif[i] if i < 4 else "rota-tl", h)
                           for i, h in enumerate(hucreler))
            return '      <div class="rota-satir%s">\n%s\n      </div>' % (" rota-bas" if bas else "", ic)

        govde = [satir([kacis(b) for b in basliklar], True)]
        for s in satirlar:
            hucre = ["<b>%s</b>" % kacis(s[0])] + [kacis(x) for x in s[1:]]
            govde.append(satir(hucre))
        return """    <div class="kicker">%s</div>
    <h2>%s</h2>
    <p class="sub">%s</p>
    <div class="rota-tablo">
%s
    </div>""" % (kacis(kicker), kacis(h2), kacis(alt), "\n".join(govde))

    raise ValueError("bilinmeyen blok tipi: %s" % tip)


def hizmet_sayfasi(slug, veri):
    url = "%s/%s.html" % (SITE, slug)
    ad = veri["ad"]

    bolumler = []
    for i, blok in enumerate(veri["bloklar"]):
        stil = ' style="background:var(--bg-2);border-block:1px solid var(--line);"' if i % 2 else ""
        bolumler.append('<section class="section"%s>\n  <div class="wrap">\n%s\n  </div>\n</section>\n'
                        % (stil, blok_html(blok)))

    sss_html = "\n".join(
        """      <details class="sss-madde"%s>
        <summary>%s</summary>
        <div class="sss-cevap"><p>%s</p></div>
      </details>""" % (" open" if i == 0 else "", kacis(q), kacis(a))
        for i, (q, a) in enumerate(veri["sss"])
    )
    ilgili = "\n".join('        <a href="%s.html">%s</a>' % (s, kacis(HIZMETLER[s]["ad"]))
                       for s in veri["ilgili"] if s in HIZMETLER)
    bolge = "\n".join('        <a href="%s-kurye.html">%s Kurye</a>' % (s, kacis(BOLGELER[s]["ad"]))
                      for s in veri["bolge"] if s in BOLGELER)

    semalar = [
        {
            "@context": "https://schema.org", "@type": "Service",
            "serviceType": ad, "name": "%s – Barse Kurye" % ad, "url": url,
            "description": veri["aciklama"],
            "provider": {"@type": "LocalBusiness", "@id": SITE + "/#organization", "name": "Barse Kurye",
                         "telephone": "+905347618388", "url": SITE + "/"},
            "areaServed": {"@type": "City", "name": "İstanbul"},
            "availableChannel": {
                "@type": "ServiceChannel", "servicePhone": {"@type": "ContactPoint", "telephone": "+905347618388"},
                "serviceUrl": url,
            },
        },
        {
            "@context": "https://schema.org", "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Anasayfa", "item": SITE + "/"},
                {"@type": "ListItem", "position": 2, "name": ad, "item": url},
            ],
        },
        {
            "@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q,
                            "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in veri["sss"]],
        },
    ]
    sema_html = "\n".join('<script type="application/ld+json">\n%s\n</script>' %
                          json.dumps(x, ensure_ascii=False, indent=2) for x in semalar)

    gorsel, gorsel_alt = veri["gorsel"]
    govde = HIZMET_GOVDE.format(
        h1=kacis(veri["h1"]), eyebrow=kacis(veri["eyebrow"]), giris=kacis(veri["giris"]),
        ad=kacis(ad), gorsel=gorsel, gorsel_alt=kacis(gorsel_alt),
        bolumler="\n".join(bolumler), sss_html=sss_html, ilgili=ilgili, bolge=bolge,
        tel=TEL, tel_uri=TEL_URI, wa=WA, taban=TABAN,
    )
    html = cerceve(veri["baslik"], veri["aciklama"], url, sema_html, govde, "İstanbul", "")
    open(os.path.join(KOK, slug + ".html"), "w", encoding="utf-8").write(html)


HIZMET_GOVDE = """<section class="district-hero">
  <div class="wrap">
    <nav class="breadcrumb" aria-label="Sayfa yolu"><a href="index.html">Anasayfa</a> / <span>{ad}</span></nav>
    <div class="eyebrow">{eyebrow}</div>
    <h1>{h1}</h1>
    <p class="lead">{giris}</p>
    <div class="hero-ctas">
      <a class="btn btn-primary" href="tel:{tel_uri}">Hemen Ara — {tel}</a>
      <a class="btn btn-ghost" href="{wa}" target="_blank" rel="noopener">WhatsApp'tan Yaz</a>
    </div>
  </div>
</section>

<div class="stats">
  <div class="wrap stats-grid">
    <div class="stat"><b>39</b><span>İLÇEDE HİZMET</span></div>
    <div class="stat"><b>30dk</b><span>EN HIZLI TESLİMAT</span></div>
    <div class="stat"><b>7/24</b><span>KESİNTİSİZ HİZMET</span></div>
    <div class="stat"><b>{taban} ₺</b><span>TABAN ÜCRET</span></div>
  </div>
</div>

<section class="section">
  <div class="wrap">
    <figure class="bolge-gorsel" style="margin-top:0;">
      <img src="{gorsel}" alt="{gorsel_alt}" loading="lazy" decoding="async" width="1408" height="768">
      <figcaption>{ad} taleplerini 7/24 açık operasyon merkezimizden yönlendiriyoruz.</figcaption>
    </figure>
  </div>
</section>

{bolumler}
<section class="section" id="sss">
  <div class="wrap">
    <div class="kicker">Sık sorulanlar</div>
    <h2>{ad} hakkında sorular</h2>
    <div class="sss-liste">
{sss_html}
    </div>
  </div>
</section>

<section class="section" id="ilgili" style="background:var(--bg-2);border-block:1px solid var(--line);">
  <div class="wrap">
    <div class="kicker">Diğer hizmetler</div>
    <h2>Birlikte en çok kullanılan hizmetler</h2>
    <div class="komsu-liste komsu-hizmet">
{ilgili}
      <a href="kurye-fiyatlari.html">Kurye Fiyatları</a>
      <a href="fiyat-hesaplama.html">Fiyat Hesaplama</a>
    </div>

    <h3 class="grup-baslik">Yoğun çalıştığımız bölgeler</h3>
    <div class="komsu-liste">
{bolge}
      <a href="istanbul-ici-kurye.html">Tüm bölgeler →</a>
    </div>
  </div>
</section>

<section class="cta-strip" id="talep">
  <div class="wrap">
    <h2>Gönderiniz hazır mı?</h2>
    <p>Alım ve teslim adresini iletin; net fiyatı söyleyip kuryeyi hemen yönlendirelim.</p>
    <div class="cta-buttons">
      <a class="btn btn-primary" href="tel:{tel_uri}">📞 {tel}</a>
      <a class="btn btn-ghost" href="{wa}" target="_blank" rel="noopener">WhatsApp ile Talep Et</a>
    </div>
  </div>
</section>
"""


# ============================================================== ilce hub sayfasi
HUB_SSS = [
    ("İstanbul'un hangi ilçelerine kurye gönderiyorsunuz?",
     "İstanbul'un 39 ilçesinin tamamına hizmet veriyoruz. Avrupa ve Anadolu yakasındaki tüm ilçelerde "
     "alım ve teslim yapıyor, Adalar dahil olmak üzere ulaşımı özel planlama gerektiren bölgelere de çıkıyoruz."),
    ("Yaka geçişli (Avrupa – Anadolu) gönderilerde süre ne kadar uzuyor?",
     "Köprü güzergâhı nedeniyle mesafeye ortalama 6 kilometre ekleniyor ve teslim süresi trafiğe bağlı olarak "
     "15–25 dakika uzayabiliyor. Acil işlerde VIP kurye ile doğrudan çıkış yapıyoruz."),
    ("İlçe sayfalarındaki süre ve ücretler kesin mi?",
     "Bu değerler hafta içi gündüz saatleri, standart paket ve normal tarife için hesaplanmış tahminlerdir. "
     "Kesin tutar; tam adres, gönderi boyutu, saat ve teslimat hızına göre belirlenir."),
    ("Aynı gün teslimat hangi saate kadar mümkün?",
     "İstanbul içi teslimatlarda 7/24 çalıştığımız için aynı gün sınırı yok. Uzak ilçelerde (Şile, Silivri, "
     "Çatalca) aynı gün teslim için sabah saatlerinde çıkış yapılması gerekir."),
]


def hub_sayfasi():
    url = SITE + "/istanbul-ici-kurye.html"
    baslik = "İstanbul İçi Kurye | 39 İlçede Moto Kurye Hizmeti – Barse Kurye"
    aciklama = ("İstanbul'un 39 ilçesinde ve %d bölgede 7/24 moto kurye hizmeti. İlçe sayfalarında süre, "
                "güzergâh ve ücret örnekleriyle birlikte tüm hizmet alanlarımız." % len(BOLGELER))

    def liste(yaka, tip):
        ogeler = sorted(
            ((v["ad"], s) for s, v in BOLGELER.items() if v["yaka"] == yaka and v["tip"] == tip),
            key=lambda x: x[0].lower(),
        )
        return "\n".join('        <a href="%s-kurye.html">%s Kurye</a>' % (s, kacis(a))
                         for a, s in ogeler)

    ilce_sayi = sum(1 for v in BOLGELER.values() if v["tip"] == "ilce")
    bolge_sayi = len(BOLGELER) - ilce_sayi

    sss_html = "\n".join(
        """      <details class="sss-madde"%s>
        <summary>%s</summary>
        <div class="sss-cevap"><p>%s</p></div>
      </details>""" % (" open" if i == 0 else "", kacis(q), kacis(a))
        for i, (q, a) in enumerate(HUB_SSS)
    )

    semalar = [
        {
            "@context": "https://schema.org", "@type": "CollectionPage",
            "name": baslik, "url": url, "description": aciklama,
            "about": {"@type": "Service", "serviceType": "Moto kurye",
                      "provider": {"@type": "LocalBusiness", "@id": SITE + "/#organization",
                                   "name": "Barse Kurye", "telephone": "+905347618388"}},
            "mainEntity": {
                "@type": "ItemList",
                "numberOfItems": len(BOLGELER),
                "itemListElement": [
                    {"@type": "ListItem", "position": i + 1,
                     "name": "%s Kurye" % v["ad"],
                     "url": "%s/%s-kurye.html" % (SITE, s)}
                    for i, (s, v) in enumerate(sorted(BOLGELER.items(), key=lambda x: x[1]["ad"]))
                ],
            },
        },
        {
            "@context": "https://schema.org", "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Anasayfa", "item": SITE + "/"},
                {"@type": "ListItem", "position": 2, "name": "İstanbul İçi Kurye", "item": url},
            ],
        },
        {
            "@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q,
                            "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in HUB_SSS],
        },
    ]
    sema_html = "\n".join('<script type="application/ld+json">\n%s\n</script>' %
                          json.dumps(x, ensure_ascii=False, indent=2) for x in semalar)

    govde = HUB_GOVDE.format(
        ilce_sayi=ilce_sayi, bolge_sayi=bolge_sayi, toplam=len(BOLGELER),
        avrupa_ilce=liste("Avrupa", "ilce"), anadolu_ilce=liste("Anadolu", "ilce"),
        avrupa_bolge=liste("Avrupa", "bolge"), anadolu_bolge=liste("Anadolu", "bolge"),
        sss_html=sss_html, tel=TEL, tel_uri=TEL_URI, wa=WA, taban=TABAN,
    )
    html = cerceve(baslik, aciklama, url, sema_html, govde, "İstanbul", "")
    open(os.path.join(KOK, "istanbul-ici-kurye.html"), "w", encoding="utf-8").write(html)


HUB_GOVDE = """<section class="district-hero">
  <div class="wrap">
    <nav class="breadcrumb" aria-label="Sayfa yolu"><a href="index.html">Anasayfa</a> / <span>İstanbul İçi Kurye</span></nav>
    <div class="eyebrow">{ilce_sayi} ilçe · {bolge_sayi} mikro bölge · 7/24 açık</div>
    <h1>İstanbul İçi Kurye</h1>
    <p class="lead">İstanbul'un {ilce_sayi} ilçesinin tamamında moto kurye hizmeti veriyoruz. Aşağıdaki sayfaların her birinde
      o bölgede hizmet verdiğimiz mahalleler, en sık teslimat yaptığımız noktalar ve o bölgeden çıkan gönderiler için
      tahmini süre – ücret tablosu yer alıyor.</p>
    <div class="hero-ctas">
      <a class="btn btn-primary" href="tel:{tel_uri}">Hemen Ara — {tel}</a>
      <a class="btn btn-ghost" href="kurye-fiyatlari.html">Fiyat tablosuna bak</a>
    </div>
  </div>
</section>

<div class="stats">
  <div class="wrap stats-grid">
    <div class="stat"><b>{ilce_sayi}</b><span>İLÇEDE HİZMET</span></div>
    <div class="stat"><b>{toplam}</b><span>BÖLGE SAYFASI</span></div>
    <div class="stat"><b>7/24</b><span>KESİNTİSİZ HİZMET</span></div>
    <div class="stat"><b>{taban} ₺</b><span>TABAN ÜCRET</span></div>
  </div>
</div>

<section class="section" id="ilceler">
  <div class="wrap">
    <div class="kicker">İlçeler</div>
    <h2>İstanbul'un {ilce_sayi} ilçesinde kurye hizmeti</h2>
    <p class="sub">Bölgenizi seçin; o ilçeye özel süre, güzergâh ve ücret bilgisine ulaşın.</p>

    <h3 class="grup-baslik">Avrupa Yakası</h3>
    <div class="komsu-liste">
{avrupa_ilce}
    </div>

    <h3 class="grup-baslik">Anadolu Yakası</h3>
    <div class="komsu-liste">
{anadolu_ilce}
    </div>
  </div>
</section>

<section class="section" id="bolgeler" style="background:var(--bg-2);border-block:1px solid var(--line);">
  <div class="wrap">
    <div class="kicker">Mikro bölgeler</div>
    <h2>İş merkezleri ve yoğun teslimat bölgeleri</h2>
    <p class="sub">Plaza hatları, sanayi bölgeleri, adliye ve fuar alanları gibi kendine özgü teslimat düzeni olan
      {bolge_sayi} bölge için ayrı sayfa hazırladık.</p>

    <h3 class="grup-baslik">Avrupa Yakası</h3>
    <div class="komsu-liste">
{avrupa_bolge}
    </div>

    <h3 class="grup-baslik">Anadolu Yakası</h3>
    <div class="komsu-liste">
{anadolu_bolge}
    </div>
  </div>
</section>

<section class="section" id="sss">
  <div class="wrap">
    <div class="kicker">Sık sorulanlar</div>
    <h2>İstanbul içi kurye hakkında sorular</h2>
    <div class="sss-liste">
{sss_html}
    </div>
  </div>
</section>

<section class="cta-strip" id="talep">
  <div class="wrap">
    <h2>İstanbul'un neresine gidecek?</h2>
    <p>Alım ve teslim adresini söyleyin; kuryeyi hemen yönlendirelim.</p>
    <div class="cta-buttons">
      <a class="btn btn-primary" href="tel:{tel_uri}">📞 {tel}</a>
      <a class="btn btn-ghost" href="{wa}" target="_blank" rel="noopener">WhatsApp ile Talep Et</a>
    </div>
  </div>
</section>
"""


# Bolge sablonunun ust ve alt cercevesi, diger sayfalarda da kullanilir.
_BAS, _KALAN = TEMPLATE.split('<main id="icerik">\n')
_, _SON = _KALAN.split('</main>\n')


def cerceve(baslik, aciklama, url, sema_html, govde, ad, varsayilan_ilce):
    """Ortak head + header + footer icine verilen govdeyi yerlestirir."""
    ortak = dict(tel=TEL, tel_uri=TEL_URI, wa=WA)
    ust = _BAS.format(baslik=kacis(baslik), aciklama=kacis(aciklama), url=url,
                      ad=kacis(ad), sema=sema_html, dosya=url.rsplit("/", 1)[-1], **ortak)
    alt = _SON.format(js_ad=js(varsayilan_ilce), **ortak)
    return ust + '<main id="icerik">\n' + govde + '</main>\n' + alt


# ============================================================== sitemap
def sitemap():
    oncelik = {
        "index.html": ("1.0", "daily"),
        "istanbul-ici-kurye.html": ("0.9", "weekly"),
        "kurye-fiyatlari.html": ("0.9", "weekly"),
        "fiyat-hesaplama.html": ("0.8", "monthly"),
        "acil-kurye.html": ("0.8", "weekly"),
        "moto-kurye.html": ("0.8", "weekly"),
        "7-24-kurye.html": ("0.8", "weekly"),
        "eczane-kurye.html": ("0.8", "weekly"),
        "kurumsal-kurye.html": ("0.8", "weekly"),
        "hakkimizda.html": ("0.5", "monthly"),
        "kvkk.html": ("0.3", "yearly"),
        "gizlilik-politikasi.html": ("0.3", "yearly"),
    }
    atla = {"404.html", "index-yeni.html"}

    dosyalar = sorted(f for f in os.listdir(KOK) if f.endswith(".html") and f not in atla)
    satir = []
    for f in dosyalar:
        loc = SITE + "/" if f == "index.html" else "%s/%s" % (SITE, f)
        p, cf = oncelik.get(f, ("0.7", "weekly"))
        satir.append(
            "  <url>\n    <loc>%s</loc>\n    <lastmod>%s</lastmod>\n"
            "    <changefreq>%s</changefreq>\n    <priority>%s</priority>\n  </url>" %
            (loc, BUGUN, cf, p)
        )
    icerik = ('<?xml version="1.0" encoding="UTF-8"?>\n'
              '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
              + "\n".join(satir) + "\n</urlset>\n")
    open(os.path.join(KOK, "sitemap.xml"), "w", encoding="utf-8").write(icerik)
    return len(dosyalar)



# ============================================================== llms.txt
def llms():
    """AI arama motorlari icin site ozeti."""
    ilce = sorted((v["ad"], s) for s, v in BOLGELER.items() if v["tip"] == "ilce")
    bolge = sorted((v["ad"], s) for s, v in BOLGELER.items() if v["tip"] == "bolge")
    satir = ["# Barse Kurye",
             "",
             "> İstanbul'un 39 ilçesinde 7/24 moto kurye, aynı gün ve acil teslimat hizmeti veren kurye firması. "
             "Türkiye geneline uçak ve şehirler arası kurye gönderisi yapılır.",
             "",
             "## Temel bilgiler",
             "- Hizmet bölgesi: İstanbul (39 ilçe) + Türkiye geneli",
             "- Çalışma saatleri: 7/24 (gece ve hafta sonu dahil)",
             "- Telefon: %s" % TEL,
             "- WhatsApp: %s" % WA,
             "- E-posta: info@barsekurye.com",
             "- Adres: Talatpaşa Mah. Aydoğan Cad. No:28 D:3, Kağıthane / İstanbul",
             "",
             "## Fiyatlandırma",
             "- Taban ücret: %d ₺ (ilk 5 km dahil)" % TABAN,
             "- 5–25 km arası: kilometre başına %d ₺" % KM_YAKIN,
             "- 25 km üzeri: kilometre başına %d ₺" % KM_UZAK,
             "- Express kurye ×1,25 · VIP kurye ×1,6 · Al-ver ×1,7",
             "- Gece (20:00–06:00) +100 ₺ · Hafta sonu +100 ₺ · Ek durak +150 ₺",
             "- Eczane kurye: sabit 400 ₺",
             "- Ayrıntılı tarife: %s/kurye-fiyatlari.html" % SITE,
             "",
             "## Ana sayfalar",
             "- Anasayfa: %s/" % SITE,
             "- Kurye fiyatları: %s/kurye-fiyatlari.html" % SITE,
             "- Fiyat hesaplama: %s/fiyat-hesaplama.html" % SITE,
             "- İstanbul içi kurye (tüm bölgeler): %s/istanbul-ici-kurye.html" % SITE,
             "- Hakkımızda: %s/hakkimizda.html" % SITE,
             "",
             "## Hizmetler",
             "- Acil kurye: %s/acil-kurye.html" % SITE,
             "- 7/24 kurye: %s/7-24-kurye.html" % SITE,
             "- Moto kurye: %s/moto-kurye.html" % SITE,
             "- Eczane kurye: %s/eczane-kurye.html" % SITE,
             "- Kurumsal kurye: %s/kurumsal-kurye.html" % SITE,
             "",
             "## İlçe sayfaları (%d)" % len(ilce)]
    satir += ["- %s Kurye: %s/%s-kurye.html" % (a, SITE, s) for a, s in ilce]
    satir += ["", "## Bölge sayfaları (%d)" % len(bolge)]
    satir += ["- %s Kurye: %s/%s-kurye.html" % (a, SITE, s) for a, s in bolge]
    satir += ["", "## Not", "Süre ve ücret bilgileri hafta içi gündüz saatleri ve standart paket içindir; "
              "kesin fiyat adres bilgisiyle teyit edilir."]
    open(os.path.join(KOK, "llms.txt"), "w", encoding="utf-8").write("\n".join(satir) + "\n")
    return len(ilce) + len(bolge)


# ============================================================== main
def main():
    noktalar = noktalari_yukle()
    sayi = noktalari_geri_yaz(noktalar)
    print("nokta listesi  : %d kayıt" % sayi)

    # komsu tanimlarindaki yazim hatalarini erken yakala
    for slug, veri in BOLGELER.items():
        for k in veri["komsu"]:
            if k not in BOLGELER:
                raise SystemExit("HATA: %s içinde tanımsız komşu: %s" % (slug, k))

    for slug, veri in BOLGELER.items():
        yol = os.path.join(KOK, slug + "-kurye.html")
        open(yol, "w", encoding="utf-8").write(sayfa(slug, veri, noktalar))
    print("bölge sayfası  : %d dosya" % len(BOLGELER))

    fiyat_sayfasi()
    print("fiyat sayfası  : kurye-fiyatlari.html")

    hub_sayfasi()
    print("ilçe hub       : istanbul-ici-kurye.html")

    for slug, veri in HIZMETLER.items():
        hizmet_sayfasi(slug, veri)
    print("hizmet sayfası : %d dosya" % len(HIZMETLER))

    print("sitemap        : %d URL" % sitemap())
    print("llms.txt       : %d bölge listelendi" % llms())


if __name__ == "__main__":
    main()
