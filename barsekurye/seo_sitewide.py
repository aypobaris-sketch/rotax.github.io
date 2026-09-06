from pathlib import Path
from datetime import date
from xml.etree import ElementTree
import html
import json
import re
import shutil
import sys

ROOT = Path(__file__).resolve().parent
if len(sys.argv) != 2:
    raise SystemExit("Usage: seo_sitewide.py /absolute/stage/path")
STAGE = Path(sys.argv[1]).resolve()
if STAGE == ROOT or ROOT in STAGE.parents:
    raise SystemExit("Stage path must be outside the repository source folder")
shutil.rmtree(STAGE, ignore_errors=True)
STAGE.mkdir(parents=True, exist_ok=True)

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
        "İstanbul Kurye | 7/24 Evrak, İlaç ve Moto Kurye — Barse",
        "İstanbul'un 39 ilçesinde 7/24 kurye. Evrak, ilaç ve kurumsal gönderi; ücret kurye yola çıkmadan netleşir."
    ),
    "moto-kurye.html": (
        "Moto Kurye İstanbul | Aynı Gün 39 İlçe — Barse",
        "İstanbul'un 39 ilçesinde 7/24 moto kurye. Evrak ve paketler aynı gün teslim edilir; ücret yola çıkmadan netleşir."
    ),
    "acil-kurye.html": (
        "Acil ve Ekspres Kurye İstanbul | VIP 7/24 — Barse",
        "İstanbul'da 7/24 acil, hızlı, ekspres ve VIP moto kurye. Gönderiye özel teslimat; ücret yola çıkmadan netleşir."
    ),
    "7-24-kurye.html": (
        "7/24 Kurye İstanbul | Gece Dahil Net Fiyat — Barse",
        "İstanbul’da gece, hafta sonu ve resmî tatilde 7/24 moto kurye. Evrak ve ilaç teslimatı; ücret kurye yola çıkmadan netleşir."
    ),
    "eczane-kurye.html": (
        "Eczane ve İlaç Kurye İstanbul | 7/24 — Barse",
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
        "Moto Kurye Fiyatları ve Hesaplama | İstanbul — Barse",
        "İlçeleri seçip mesafe ve süreyi görün. Kurye ücretini mesafe, hız ve saat belirler; kesin tutar yola çıkmadan netleşir."
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
    ">4,4</a>": ">4,5</a>",
    "27 Google yorumu": "31 Google yorumu",
    "30 yorum": "31 yorum",
    "content=\"Eczaneden Eve İlaç Siparişi | İstanbul, 7/24 Kurye\">>": "content=\"Eczaneden Eve İlaç Teslimatı | 7/24 İstanbul\">",
    "English-speaking, all 39 districts, flat pharmacy rate.": "English-speaking service across all 39 districts; the courier price is confirmed before departure.",
    "Pharmacy deliveries use a flat rate with no night or weekend surcharge.": "The courier price depends on distance and time and is confirmed before departure.",
    "Pharmacy deliveries use a <b>flat rate</b> — no distance, night or weekend surcharge. We tell you the amount before the courier leaves.": "The courier fee depends on distance and time. We confirm the exact amount before departure, so there is no surprise at the door.",
    "İstanbul'un 39 ilçesinde 7/24 moto kurye. Evrak, ilaç ve kurumsal gönderiler; Türkiye geneline havayolu ve şehirlerarası taşıma.": "Moto kurye İstanbul'un 39 ilçesinde 7/24; havayolu ve şehirlerarası gönderiler ayrı planlanır.",
    "Türkiye geneline uçak kargo ile gönderi ve gümrük evrak taşıma.": "İstanbul dışı havayolu ve şehirlerarası gönderiler ayrı planlanır; gümrük evrak taşıması yapılır.",
    "Evet. Türkiye geneline havayolu kargo ve şehirlerarası taşıma yapıyoruz; ayrıca gümrük evrak taşıma hizmetimiz var. Bu gönderiler için telefonla fiyat veriyoruz.": "Moto kurye hizmetimiz İstanbul içidir. İstanbul dışı havayolu ve şehirlerarası gönderiler ayrı planlanır; gümrük evrak taşıması için ücreti önceden bildiriyoruz.",
    "لتوصيل الأدوية نطبّق <b>تعرفة ثابتة</b> — دون فرق للمسافة أو الليل أو عطلة نهاية الأسبوع. نُعلمك بالمبلغ قبل انطلاق الكوريير.": "يعتمد سعر الكوريير على المسافة والوقت، ونُعلمك بالمبلغ قبل انطلاقه.",
    "لتوصيل الأدوية نطبّق تعرفة ثابتة دون فرق ليلي أو فرق لعطلة نهاية الأسبوع.": "يعتمد سعر الكوريير على المسافة والوقت، ونُعلمك بالمبلغ قبل انطلاقه."
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
    document = re.sub(r'<meta\s+property="og:title"\s+content="[^"]*"\s*/?>>?', f'<meta property="og:title" content="{title}">', document, count=1, flags=re.I)
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

    document = re.sub(r"(?i)sabit tarife", "önceden netleşen tarife", document)
    document = re.sub(r"(?i)gece farkı yok", "ücret yola çıkmadan netleşir", document)
    document = re.sub(r"(?i)gece farkı uygulanmıyor", "ücret yola çıkmadan netleşiyor", document)
    document = re.sub(r"(?i)hafta sonu farkı uygulanmıyor", "ücret yola çıkmadan netleşiyor", document)
    document = re.sub(r"(?i)mesafeden bağımsız önceden netleşen tarife", "mesafe ve saate göre yola çıkmadan netleşen tarife", document)

    document = document.replace(ADDRESS_OLD, ADDRESS_NEW)
    document = document.replace('href="index.html"', 'href="/"')
    document = document.replace("href='index.html'", "href='/'")

    if path.name in {"404.html", "gizlilik-politikasi.html", "kvkk.html"}:
        document = set_robots(document, "noindex, follow")

    if path.name not in {"404.html", "gizlilik-politikasi.html", "kvkk.html"}:
        required = ("<title>", 'name="description"', 'rel="canonical"', "<h1")
        missing = [token for token in required if token not in document]
        if missing:
            raise ValueError(f"{path.name}: missing SEO fields: {', '.join(missing)}")
    if ">>" in document.split("</head>", 1)[0]:
        raise ValueError(f"{path.name}: malformed head tag")

    (STAGE / path.name).write_text(document, encoding="utf-8")
    return document != original


def update_sitemap(changed_html):
    path = ROOT / "sitemap.xml"
    original = path.read_text(encoding="utf-8")
    document = re.sub(
        r"\s*<url>\s*<loc>https://barsekurye\.com/(?:gizlilik-politikasi|kvkk)\.html</loc>.*?</url>",
        "",
        original,
        flags=re.S,
    )
    today = date.today().isoformat()
    for filename in changed_html:
        location = "https://barsekurye.com/" if filename == "index.html" else f"https://barsekurye.com/{filename}"
        pattern = rf"(<loc>{re.escape(location)}</loc>\s*<lastmod>)[^<]+(</lastmod>)"
        document = re.sub(pattern, rf"\g<1>{today}\g<2>", document, count=1)
    (STAGE / path.name).write_text(document, encoding="utf-8")
    return document != original


def validate_stage():
    index_exclusions = {"404.html", "gizlilik-politikasi.html", "kvkk.html"}
    expected_indexable = {
        path.name for path in ROOT.glob("*.html")
        if path.name not in {"404.html", "index-eski.html", "gizlilik-politikasi.html", "kvkk.html"}
    }
    titles = {}
    descriptions = {}
    canonicals = {}
    warnings = []

    for path in sorted(STAGE.glob("*.html")):
        document = path.read_text(encoding="utf-8")
        head = document.split("</head>", 1)[0]
        if ">>" in head:
            raise ValueError(f"{path.name}: malformed head tag")
        if 'href="index.html"' in document or "href='index.html'" in document:
            raise ValueError(f"{path.name}: legacy index.html internal link remains")

        if path.name in index_exclusions:
            if "noindex" not in head.lower():
                raise ValueError(f"{path.name}: noindex missing")
            continue

        title_match = re.search(r"<title>(.*?)</title>", head, flags=re.I | re.S)
        desc_match = re.search(r'<meta\s+name="description"\s+content="([^"]+)"', head, flags=re.I)
        canonical_match = re.search(r'<link\s+rel="canonical"\s+href="([^"]+)"', head, flags=re.I)
        h1_count = len(re.findall(r"<h1(?:\s|>)", document, flags=re.I))
        if not title_match or not desc_match or not canonical_match or h1_count != 1:
            raise ValueError(f"{path.name}: title, description, canonical or single H1 check failed")

        title = clean_text(title_match.group(1))
        description = clean_text(desc_match.group(1))
        canonical = canonical_match.group(1)
        expected_canonical = "https://barsekurye.com/" if path.name == "index.html" else f"https://barsekurye.com/{path.name}"
        if canonical != expected_canonical:
            raise ValueError(f"{path.name}: canonical mismatch ({canonical})")
        if title in titles:
            raise ValueError(f"Duplicate title: {path.name} and {titles[title]}")
        if description in descriptions:
            raise ValueError(f"Duplicate description: {path.name} and {descriptions[description]}")
        if canonical in canonicals:
            raise ValueError(f"Duplicate canonical: {path.name} and {canonicals[canonical]}")
        titles[title] = path.name
        descriptions[description] = path.name
        canonicals[canonical] = path.name

        if len(title) > 65:
            warnings.append(f"{path.name}: title {len(title)} chars")
        if len(description) < 80 or len(description) > 165:
            warnings.append(f"{path.name}: description {len(description)} chars")

        for payload in re.findall(r'<script[^>]+type="application/ld\+json"[^>]*>(.*?)</script>', document, flags=re.I | re.S):
            json.loads(payload)

        stale_claims = (
            "sabit tarife", "gece farkı yok", "gece farkı uygulanmıyor",
            "hafta sonu farkı uygulanmıyor", "flat rate"
        )
        lowered = clean_text(document).lower()
        for claim in stale_claims:
            if claim in lowered:
                raise ValueError(f"{path.name}: stale pricing claim remains: {claim}")

    sitemap_path = STAGE / "sitemap.xml"
    root = ElementTree.parse(sitemap_path).getroot()
    namespace = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    sitemap_files = set()
    for loc in root.findall("sm:url/sm:loc", namespace):
        url = (loc.text or "").strip()
        sitemap_files.add("index.html" if url == "https://barsekurye.com/" else url.rsplit("/", 1)[-1])
    if sitemap_files != expected_indexable:
        missing = sorted(expected_indexable - sitemap_files)
        extra = sorted(sitemap_files - expected_indexable)
        raise ValueError(f"Sitemap mismatch. Missing={missing}; Extra={extra}")

    print(f"SEO validation passed: {len(expected_indexable)} indexable pages; {len(warnings)} non-blocking length warnings")
    for warning in warnings:
        print(f"WARNING: {warning}")


changed = []
for html_file in sorted(ROOT.glob("*.html")):
    if html_file.name == "index-eski.html":
        continue
    if update_html(html_file):
        changed.append(html_file.name)

if update_sitemap(changed):
    changed.append("sitemap.xml")

validate_stage()
print(f"SEO cleanup complete: {len(changed)} files updated")
