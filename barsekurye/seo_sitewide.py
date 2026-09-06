from pathlib import Path
import html
import re

ROOT = Path(__file__).resolve().parent

LOCAL_PAGES = {
    "adalar-kurye.html", "arnavutkoy-kurye.html", "atasehir-kurye.html", "avcilar-kurye.html",
    "bagcilar-kurye.html", "bahcelievler-kurye.html", "bakirkoy-kurye.html", "basaksehir-kurye.html",
    "bayrampasa-kurye.html", "besiktas-kurye.html", "beykoz-kurye.html", "beylikduzu-kurye.html",
    "beyoglu-kurye.html", "buyukcekmece-kurye.html", "catalca-kurye.html", "cekmekoy-kurye.html",
    "esenler-kurye.html", "esenyurt-kurye.html", "eyupsultan-kurye.html", "fatih-kurye.html",
    "gaziosmanpasa-kurye.html", "gungoren-kurye.html", "kadikoy-kurye.html", "kagithane-kurye.html",
    "kartal-kurye.html", "kucukcekmece-kurye.html", "maltepe-kurye.html", "pendik-kurye.html",
    "sancaktepe-kurye.html", "sariyer-kurye.html", "sile-kurye.html", "silivri-kurye.html",
    "sisli-kurye.html", "sultanbeyli-kurye.html", "sultangazi-kurye.html", "tuzla-kurye.html",
    "umraniye-kurye.html", "uskudar-kurye.html", "zeytinburnu-kurye.html",
    "atasehir-finans-kurye.html", "bagdat-caddesi-kurye.html", "bakirkoy-merkez-kurye.html",
    "besiktas-carsi-kurye.html", "caglayan-kurye.html", "esenyurt-merkez-kurye.html",
    "ikitelli-kurye.html", "kadikoy-moda-kurye.html", "kartal-merkez-kurye.html",
    "kozyatagi-kurye.html", "levent-kurye.html", "maslak-kurye.html", "mecidiyekoy-kurye.html",
    "nisantasi-kurye.html", "otogar-kurye.html", "perpa-kurye.html", "seyrantepe-kurye.html",
    "sisli-merkez-kurye.html", "taksim-beyoglu-kurye.html", "topkapi-kurye.html",
    "umraniye-merkez-kurye.html", "zincirlikuyu-kurye.html"
}

META = {
    "index.html": (
        "İstanbul Moto Kurye | 7/24 Kurye Çağır — Barse",
        "İstanbul'un 39 ilçesinde 7/24 moto kurye. Evrak, ilaç ve kurumsal gönderi; ücret kurye yola çıkmadan netleşir."
    ),
    "moto-kurye.html": (
        "Moto Kurye İstanbul | 7/24 Kurye Çağır — Barse",
        "İstanbul'un 39 ilçesinde 7/24 moto kurye çağırın. Evrak, paket ve kurumsal gönderi; ücret yola çıkmadan netleşir."
    ),
    "acil-kurye.html": (
        "Acil Kurye İstanbul | Ekspres ve VIP Kurye — Barse",
        "İstanbul'da 7/24 acil moto kurye. Ekspres ve VIP seçenekleriyle gönderiye özel teslimat; ücret yola çıkmadan netleşir."
    ),
    "7-24-kurye.html": (
        "7/24 Kurye İstanbul | Gece Dahil Net Fiyat — Barse",
        "İstanbul’da gece, hafta sonu ve resmî tatilde 7/24 moto kurye. Evrak ve ilaç teslimatı; ücret kurye yola çıkmadan netleşir."
    ),
    "eczane-kurye.html": (
        "Eczane Kurye İstanbul | 7/24 İlaç Teslimatı — Barse",
        "Eczane, ecza deposu ve hastalar için 7/24 ilaç kuryesi. İstanbul'un 39 ilçesi; ücret mesafe ve saate göre yola çıkmadan netleşir."
    ),
    "eczaneden-eve-siparis.html": (
        "Eczaneden Eve İlaç Teslimatı | 7/24 İstanbul",
        "İlacı ruhsatlı eczaneden alıp İstanbul'daki adresinize getiriyoruz. Reçete ve adresi iletin; kurye ücreti yola çıkmadan netleşir."
    ),
    "nobetci-eczane-kurye.html": (
        "Nöbetçi Eczane Kurye | Gece İlaç Teslimatı İstanbul",
        "Nöbetçi eczaneyi bulup ilacı İstanbul'daki adresinize getiriyoruz. 39 ilçede 7/24; ücret kurye yola çıkmadan netleşir."
    ),
    "evrak-kurye.html": (
        "Evrak Kurye İstanbul | Acil Belge Teslimatı — Barse",
        "Sözleşme, noter, mahkeme ve ihale evrakı için 7/24 moto kurye. İstanbul'un 39 ilçesi; ücret yola çıkmadan netleşir."
    ),
    "fiyat-hesaplama.html": (
        "Moto Kurye Fiyat Hesaplama | Mesafe ve Hız — Barse",
        "İlçeleri seçip yol mesafesi ve teslimat süresini görün. Kurye ücretini mesafe, hız ve saat belirler; kesin tutar yola çıkmadan netleşir."
    ),
    "kurumsal-kurye.html": (
        "Kurumsal Kurye İstanbul | Aylık Faturalı — Barse",
        "Eczane, hukuk, muhasebe ve e-ticaret işletmelerine düzenli kurye. Aylık fatura, gönderi dökümü ve 7/24 destek."
    ),
    "gumruk-kurye.html": (
        "Gümrük Kurye İstanbul | Beyanname ve Ordino — Barse",
        "Gümrük müşavirleri ve dış ticaret firmaları için 7/24 evrak kuryesi. Beyanname, konşimento, ordino ve fatura teslimatı."
    ),
    "sikca-sorulan-sorular.html": (
        "Kurye Hakkında Sık Sorulan Sorular | Barse İstanbul",
        "Moto kurye süresi, ücret, gece teslimatı, eczane ve kurumsal çalışma hakkında kısa cevaplar. İstanbul'un 39 ilçesinde 7/24."
    )
}

REPLACEMENTS = {
    "Sabit tarife — mesafe, gece ve hafta sonu farkı yok.": "Ücret mesafe ve saate göre kurye yola çıkmadan netleşir.",
    "Sabit tarife; mesafe, saat ve hafta sonu farkı uygulanmaz.": "Ücret mesafe ve saate göre kurye yola çıkmadan netleşir.",
    "Sabit tarife uygulanır. Mesafe, saat ve hafta sonu farkı uygulanmaz.": "Ücret mesafe ve saate göre kurye yola çıkmadan netleşir.",
    "Eczane gönderilerinde gece ve hafta sonu farkı uygulanmıyor.": "Eczane gönderilerinde ücret mesafe ve saate göre kurye yola çıkmadan netleşir.",
    "Eczane teslimatlarında mesafeden bağımsız sabit tarife uyguluyoruz.": "Eczane teslimatlarında ücret mesafe ve saate göre kurye yola çıkmadan netleşir.",
    "Eczane gönderileri bunun dışındadır: eczane tarifesine gece farkı eklenmez.": "Eczane gönderilerinde de ücret mesafe ve saate göre kurye yola çıkmadan netleşir.",
    "Eczane gönderilerinde hafta sonu farkı da uygulanmaz.": "Eczane gönderilerinde de ücret kurye yola çıkmadan netleşir.",
    "Eczane kurye sabit tarife'dir; gece ve hafta sonu farkı uygulanmaz.": "Eczane kurye ücreti mesafe ve saate göre yola çıkmadan netleşir.",
    "Eczane gönderilerinde bu fark uygulanmıyor.": "Eczane gönderilerinde de ücret mesafe ve saate göre yola çıkmadan netleşir.",
    "Hafta sonu ve resmî tatillerde de aynı — eczane gönderilerinde ek ücret yok.": "Hafta sonu ve resmî tatillerde de ücret kurye yola çıkmadan netleşir.",
    "Gece 3'te de, öğlen 3'te de aynı fiyat.": "Gece ve gündüz ücreti mesafe ve saate göre değişebilir.",
    "gece farkı almadan.": "ücreti yola çıkmadan netleştirerek.",
    "Kuyruk yok, arama yok, gece farkı yok.": "Kurye ücreti yola çıkmadan netleşir.",
    "Eczane siparişlerinde <b>sabit tarife</b> uyguluyoruz: gece, hafta sonu ya da nöbetçi eczane farkı yok. Gece iki buçukta arayan biriyle öğlen arayan biri aynı ücreti ödüyor.": "Eczane siparişlerinde ücret mesafe ve saate göre belirlenir. Kesin tutarı kurye yola çıkmadan söylüyoruz; kapıda sürpriz çıkmıyor.",
    "ve eczane teslimatlarında gece farkı uygulamıyoruz.": "ve ücreti kurye yola çıkmadan netleştiriyoruz.",
    "ücret yine sabit kalıyor.": "ücret yola çıkmadan netleşiyor.",
    "eczane teslimatlarında sabit tarife uyguluyoruz — gece ve hafta sonu farkı yok.": "eczane teslimatlarında ücreti mesafe ve saate göre kurye yola çıkmadan netleştiriyoruz.",
    "Acil ilaç, reçete ve depo arası transfer. Nöbet gecelerinde de ulaşılabilir kurye, sabit tarife.": "Acil ilaç, reçete ve depo arası transfer. Nöbet gecelerinde de ulaşılabilir kurye; ücret yola çıkmadan netleşir.",
    "eczane kurye taleplerini sabit tarifeyle, öncelikli sipariş": "eczane kurye taleplerini ücreti yola çıkmadan netleştirerek, öncelikli sipariş",
    "aynı sabit tarife geçerli.": "ücret yola çıkmadan netleşir.",
    "İstanbul içi, 7/24, sabit tarife.": "İstanbul içi, 7/24; ücret yola çıkmadan netleşir.",
    "İstanbul'un 39 ilçesinde 7/24, sabit tarifeyle.": "İstanbul'un 39 ilçesinde 7/24; ücret yola çıkmadan netleşir.",
    "<h2>Neden sabit tarife?</h2>": "<h2>Eczane kurye ücreti nasıl belirlenir?</h2>",
    "öncelikli teslimat, sabit tarife.": "öncelikli teslimat; ücret yola çıkmadan netleşir.",
    "4,4 ortalama": "4,5 ortalama",
    "27 Google yorumu": "31 Google yorumu",
    "30 yorum": "31 yorum",
    "content=\"Eczaneden Eve İlaç Siparişi | İstanbul, 7/24 Kurye\">>": "content=\"Eczaneden Eve İlaç Teslimatı | 7/24 İstanbul\">"
}

ADDRESS_OLD = '"address": {"@type": "PostalAddress", "addressLocality": "Kağıthane", "addressRegion": "İstanbul", "addressCountry": "TR"}'
ADDRESS_NEW = '"address": {"@type": "PostalAddress", "streetAddress": "Talatpaşa Mahallesi, Aydoğan Caddesi No:28 D:3", "addressLocality": "Kağıthane", "addressRegion": "İstanbul", "postalCode": "34333", "addressCountry": "TR"}'


def clean_text(value):
    value = re.sub(r"<[^>]+>", " ", value)
    value = html.unescape(value)
    return re.sub(r"\s+", " ", value).strip()


def local_name(document, fallback):
    match = re.search(r"<h1[^>]*>(.*?)</h1>", document, flags=re.I | re.S)
    name = clean_text(match.group(1)) if match else fallback
    name = re.sub(r"\s+(?:Moto\s+)?Kurye(?:\s+Hizmeti)?(?:\s+—\s+39\s+İlçe)?$", "", name, flags=re.I).strip(" —")
    return name or fallback


def set_meta(document, title, description):
    document = re.sub(r"<title>.*?</title>", f"<title>{title}</title>", document, count=1, flags=re.I | re.S)
    document = re.sub(r'<meta\s+name="description"\s+content="[^"]*"\s*/?>', f'<meta name="description" content="{description}">', document, count=1, flags=re.I)
    document = re.sub(r'<meta\s+property="og:title"\s+content="[^"]*"\s*/?>', f'<meta property="og:title" content="{title}">', document, count=1, flags=re.I)
    document = re.sub(r'<meta\s+property="og:description"\s+content="[^"]*"\s*/?>', f'<meta property="og:description" content="{description}">', document, count=1, flags=re.I)
    return document


def set_robots(document, value):
    pattern = r'<meta\s+name="robots"\s+content="[^"]*"\s*/?>'
    tag = f'<meta name="robots" content="{value}">'
    if re.search(pattern, document, flags=re.I):
        return re.sub(pattern, tag, document, count=1, flags=re.I)
    return document.replace("</title>", f"</title>\n{tag}", 1)


def update_html(path):
    original = path.read_text(encoding="utf-8")
    document = original

    if path.name in META:
        document = set_meta(document, *META[path.name])
    elif path.name in LOCAL_PAGES:
        name = local_name(document, path.stem.replace("-kurye", "").replace("-", " ").title())
        title = f"{name} Moto Kurye | 7/24 Net Fiyat — Barse"
        if len(title) > 60:
            title = f"{name} Kurye | 7/24 — Barse"
        description = f"{name} bölgesinde 7/24 moto kurye. Evrak, ilaç ve kurumsal gönderi; ücret kurye yola çıkmadan netleşir."
        document = set_meta(document, title, description)

    for old, new in REPLACEMENTS.items():
        document = document.replace(old, new)

    document = document.replace(ADDRESS_OLD, ADDRESS_NEW)

    if path.name in {"gizlilik-politikasi.html", "kvkk.html"}:
        document = set_robots(document, "noindex, follow")

    if document != original:
        path.write_text(document, encoding="utf-8")
        return True
    return False


def update_sitemap():
    path = ROOT / "sitemap.xml"
    original = path.read_text(encoding="utf-8")
    document = re.sub(
        r"\s*<url>\s*<loc>https://barsekurye\.com/(?:gizlilik-politikasi|kvkk)\.html</loc>.*?</url>",
        "",
        original,
        flags=re.S,
    )
    if document != original:
        path.write_text(document, encoding="utf-8")
        return True
    return False


changed = []
for html_file in sorted(ROOT.glob("*.html")):
    if html_file.name in {"404.html", "index-eski.html"}:
        continue
    if update_html(html_file):
        changed.append(html_file.name)

if update_sitemap():
    changed.append("sitemap.xml")

print(f"SEO cleanup complete: {len(changed)} files updated")
