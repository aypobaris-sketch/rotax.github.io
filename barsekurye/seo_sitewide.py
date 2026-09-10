from pathlib import Path
import hashlib
from datetime import date
from xml.etree import ElementTree
import html
import json
import re
import shutil
import subprocess
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
        "İstanbul Kurye | Moto, Eczane ve Evrak Kurye 7/24",
        "İstanbul'un 39 ilçesinde 7/24 moto kurye. Gece nöbetçi eczaneden ilaç, acil evrak ve kurumsal gönderi. Tek arama; ücret yola çıkmadan netleşir."
    ),
    "moto-kurye.html": (
        "Moto Kurye İstanbul | Aynı Gün Teslimat 7/24 — Barse",
        "İstanbul'un 39 ilçesinde motorlu kurye. Evrak, ilaç ve paketiniz aynı gün elden teslim; ekspres 45–75 dk. Ücret kurye yola çıkmadan netleşir."
    ),
    "acil-kurye.html": (
        "Acil Kurye İstanbul | Ekspres 45–75 dk, VIP 30–60 dk",
        "İstanbul'da 7/24 acil ve ekspres moto kurye. Ekspres 45–75 dk, VIP 30–60 dk: kurye sadece sizin gönderinizle, duraksız yola çıkar."
    ),
    "7-24-kurye.html": (
        "7/24 Kurye İstanbul | Gece ve Tatilde Açık — Barse",
        "Gece 03:00'te nöbetçi eczaneden ilaç, sabaha yetişecek acil evrak. İstanbul'un 39 ilçesinde hafta sonu ve resmî tatil dahil 7/24 moto kurye."
    ),
    "eczane-kurye.html": (
        "Eczane Kurye İstanbul | İlaç Kuryesi, Eczane Kuryesi",
        "Eczane kuryesi: ilacı eczaneden alıp İstanbul'daki adresinize getiriyoruz. 39 ilçe, gece dahil 7/24; eczane tarifesi sabit, gece farkı yok."
    ),
    "eczaneden-eve-siparis.html": (
        "Eczaneden Eve İlaç Siparişi | Eve Servis Yapan Eczane",
        "Eczaneye gidemiyor musunuz? Eve ilaç siparişinizi alır, ruhsatlı eczaneden getiririz. İstanbul'un 39 ilçesi, gece dahil 7/24, tek mesajla."
    ),
    "nobetci-eczane-kurye.html": (
        "Nöbetçi Eczane Kurye | Gece İlaç Getiren Kurye",
        "Size en yakın nöbetçi eczaneyi biz buluyoruz, ilacı gecenin ortasında adresinize getiriyoruz. İstanbul'un 39 ilçesinde 7/24, gece farkı yok."
    ),
    "fiyat-hesaplama.html": (
        "Kurye Fiyat Hesaplama | İstanbul Moto Kurye Ücreti",
        "İki ilçe seçin, aradaki yolu ve teslimat süresini anında görün. Kurye ücretini mesafe, hız ve saat belirler; kesin tutarı yola çıkmadan söylüyoruz."
    ),
    "eczaneler-icin-kurye.html": (
        "Eczaneler İçin Kurye | Depo Transferi ve Takas",
        "Eczaneler için kurye: ecza deposundan ürün alımı, meslektaş eczaneyle ödünç ilaç takası ve hastaya reçete teslimi. İstanbul'da 7/24, aylık faturalı."
    ),
    "kurumsal-kurye.html": (
        "Kurumsal Kurye İstanbul | Anlaşmalı, Aylık Faturalı",
        "Her gün sabit saatte gelen anlaşmalı kurye, ay sonunda tek fatura ve gönderi dökümü. Eczane, hukuk, muhasebe ve e-ticaret ofislerine özel."
    ),
    "gumruk-kurye.html": (
        "Gümrük Kurye İstanbul | Beyanname ve Ordino — Barse",
        "Gümrük müşavirleri ve dış ticaret firmaları için 7/24 evrak kuryesi. Beyanname, konşimento, ordino ve fatura teslimatı."
    ),
    "istanbul-ici-kurye.html": (
        "İstanbul İçi Kurye | 39 İlçe Moto Kurye, Gece Dahil",
        "İstanbul içi kurye: 39 ilçede evrak, ilaç ve kurumsal gönderi. Aynı gün elden teslim, gece ve hafta sonu dahil 7/24. Tek arama yeterli."
    ),
    "hakkimizda.html": (
        "Hakkımızda | Barse Kurye — Kağıthane Merkezli Kurye",
        "Barse Kurye, Kağıthane merkezli bağımsız bir moto kurye firmasıdır. İstanbul'un 39 ilçesine 7/24 evrak, eczane ve kurumsal teslimat yapar."
    ),
    "evrak-kurye.html": (
        "Evrak Kurye İstanbul | Noter, Mahkeme ve İhale Evrakı",
        "Islak imzalı sözleşme, noter evrakı, mahkeme dosyası ve ihale zarfı elden teslim. İstanbul'un 39 ilçesinde 7/24 evrak kuryesi."
    ),
    "havalimani-otogar-kurye.html": (
        "Havalimanı ve Otogar Kurye | Aynı Gün Yetiştirme",
        "Havalimanına, otogara veya terminale yetişmesi gereken evrak ve paket. İstanbul'un 39 ilçesinden alım, 7/24 moto kurye."
    ),
    "sikca-sorulan-sorular.html": (
        "Kurye Hakkında Sık Sorulan Sorular | Barse İstanbul",
        "Moto kurye süresi, ücret, gece teslimatı, eczane ve kurumsal çalışma hakkında kısa cevaplar. İstanbul'un 39 ilçesinde 7/24."
    )
}

# ── Dağıtım anında metin değiştirme YOK ──────────────────────────────────
# 9 Eylül 2026'ya kadar burada bir REPLACEMENTS sözlüğü vardı: puan, yorum
# sayısı, adres ve birkaç cümle yalnızca dağıtım anında düzeltiliyordu.
# Sonuç: HTML bir şey diyor, canlı site başka bir şey diyordu; kaynağı
# düzenleyen kişi neyin yayına gittiğini göremiyordu. Hepsi kaynak HTML'e
# yazıldı. Bir metni değiştirmek gerekiyorsa HTML'de değiştirin.
#
# Başlık ve açıklamalar bilerek burada kalıyor (META / LOCAL_PAGES): tek
# yerden yönetilmeleri isteniyor. Kaynak HTML onlarla eşitlenmiş durumda,
# yani betiği çalıştırmak artık başlıkları değiştirmiyor - sadece doğruluyor.

# ── Önbellek damgası: içerikten üretilir ─────────────────────────────────
# Eskiden CSS her değiştiğinde 76 sayfadaki "?v=YYYYMMDD" elle güncellenmek
# zorundaydı; unutulunca telefonlarda eski stil kalıyordu. Artık damga
# dosyanın kendi özetinden yazılıyor: dosya değişirse damga değişir,
# değişmezse tarayıcı önbelleği bozulmadan kalır. Elle iş kalmadı.
STAMPED_ASSETS = (
    "assets/barse.css", "assets/site.js", "assets/sohbet.js",
    "assets/rota-arac.js", "assets/barse-logo.png",
)
ASSET_STAMPS = {
    yol: hashlib.sha1((ROOT / yol).read_bytes()).hexdigest()[:10]
    for yol in STAMPED_ASSETS if (ROOT / yol).exists()
}


def stamp_assets(document):
    for yol, imza in ASSET_STAMPS.items():
        document = re.sub(rf"({re.escape(yol)})\?v=[^\"'\s>]*", rf"\1?v={imza}", document)
    return document


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


# ── CSS matematik denetimi ───────────────────────────────────────────────
# clamp() / calc() / min() / max() icinde "+" ve "-" isaretinin IKI YANINDA
# da bosluk olmak zorunda. "clamp(2.1rem,1.5rem+2.9vw,3.5rem)" gecersizdir:
# tarayici hata vermez, kurali sessizce duserir. Bu yuzden barse.css'te
# --t-2xl/3xl/4xl aylarca gecersiz kaldi ve 81 sayfanin TAMAMINDA h1 ile h2
# govde yazisi boyutuna (16 piksel) dustu. Gozle fark edilmesi zor, bedeli
# buyuk. Ayni hata bir daha yayina cikmasin diye dagitim burada duruyor.
CSS_MATH = re.compile(r"(?:clamp|calc|min|max)\([^)]*[0-9a-zA-Z%)][+\-][0-9.]")


def validate_css():
    errors = []
    sheets = sorted((ROOT / "assets").glob("*.css"))
    for sheet in sheets:
        for line_no, line in enumerate(sheet.read_text(encoding="utf-8").splitlines(), 1):
            if CSS_MATH.search(line):
                errors.append(
                    f"{sheet.name}:{line_no}: clamp/calc icinde bosluksuz +/- "
                    f"- tarayici bu kurali sessizce duserir"
                )
    if errors:
        raise ValueError("CSS matematik hatasi:\n  " + "\n  ".join(errors))
    print(f"CSS validation passed: {len(sheets)} stylesheet(s)")



def update_html(path):
    original = path.read_text(encoding="utf-8")
    document = original

    if path.name in META:
        document = set_meta(document, *META[path.name])
    elif path.name in LOCAL_PAGES:
        name = local_name(document, path.stem.replace("-kurye", "").replace("-", " ").title())
        title = f"{name} Kurye | Eczane, İlaç ve Moto Kurye 7/24"
        if len(title) > 60:
            title = f"{name} Kurye | Eczane ve Moto Kurye 7/24"
        description = (
            f"{name} bölgesinde 7/24 kurye. Nöbetçi eczaneden ilaç, evrak ve "
            f"kurumsal gönderi kapınıza gelir; eczane teslimatında gece farkı yok."
        )
        document = set_meta(document, title, description)

    # 9 Eylul 2026 - FIYAT VAADINI SILEN DONUSUMLER KALDIRILDI.
    # Buradaki regex'ler "sabit tarife" / "gece farki yok" ifadelerini
    # dagitim aninda siliyordu. Eczane tarifesi tarife.php'de GERCEKTEN
    # sabit (T_ECZANE, mesafe/hiz/boyut/zam uygulanmaz) ve bu, rakibe
    # karsi tek gercek ayrisma noktasi. Reklam metni de "Sabit Tarife,
    # Mesafe Yok" diyor; sayfa tersini soyleyince ikisi celisiyordu.

    # Icerik degisikligi burada bitiyor. Asagidaki iki islem bicimsel:
    # kok baglanti duzeltmesi her sayfada, onbellek damgasi CSS/JS her
    # degistiginde tetiklenir. Ikisi de "sayfa degisti" sayilirsa sitemap'teki
    # lastmod tarihleri her dagitimda topluca bugune ceker; Google surekli
    # degisen lastmod'a guvenmeyi birakir.
    content_changed = document != original

    # Kok baglanti: kaynakta "index.html" duruyor ki dosyalar yerelde de
    # gezilebilsin; yayinda tek kanonik adres "/" olmali.
    document = document.replace('href="index.html"', 'href="/"')
    document = document.replace("href='index.html'", "href='/'")
    document = stamp_assets(document)

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
    return content_changed


def git_last_modified():
    """Her sayfanin son gercek degisiklik tarihi (git gecmisinden).

    Onceki hali her dagitimda o gunku tarihi yaziyordu: bir sayfa
    degistiginde digerlerinin lastmod'u depodaki eski degere geri donuyor,
    ertesi gun baska bir sayfa bugune ceviriliyordu. Boyle zikzaklayan bir
    lastmod Google icin gurultudur ve dikkate alinmayi birakir. Git ne
    zaman gercekten degistigini biliyor; kaynagi o olsun. Git okunamazsa
    bos sozluk doner ve eski davranisa (yalnizca bu kosuda degisenler
    bugune cekilir) duselir - dagitim asla bu yuzden durmaz."""
    try:
        proc = subprocess.run(
            ["git", "log", "--name-only", "--format=%x00%cs", "--", "."],
            cwd=str(ROOT), capture_output=True, text=True, timeout=90, check=True,
        )
    except Exception:
        return {}
    dates = {}
    for chunk in proc.stdout.split("\x00"):
        lines = [line.strip() for line in chunk.splitlines() if line.strip()]
        if len(lines) < 2:
            continue
        day = lines[0]
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", day):
            continue
        for repo_path in lines[1:]:
            # git log yeniden eskiye gider; ilk gorulen tarih en yenisidir.
            dates.setdefault(repo_path.rsplit("/", 1)[-1], day)
    return dates


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
    git_dates = git_last_modified()
    pages = {path.name for path in ROOT.glob("*.html")} | set(changed_html)
    for filename in sorted(pages):
        day = git_dates.get(filename)
        if day is None:
            day = today if filename in changed_html else None
        if day is None:
            continue
        location = "https://barsekurye.com/" if filename == "index.html" else f"https://barsekurye.com/{filename}"
        pattern = rf"(<loc>{re.escape(location)}</loc>\s*<lastmod>)[^<]+(</lastmod>)"
        document = re.sub(pattern, rf"\g<1>{day}\g<2>", document, count=1)
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

        breadcrumb = None
        for payload in re.findall(r'<script[^>]+type="application/ld\+json"[^>]*>(.*?)</script>', document, flags=re.I | re.S):
            data = json.loads(payload)
            for node in (data.get("@graph") or [data]) if isinstance(data, dict) else []:
                if isinstance(node, dict) and node.get("@type") == "BreadcrumbList":
                    breadcrumb = [item["name"] for item in node["itemListElement"]]

        # Google, isaretlenen yolun sayfada GORUNEN yolla ayni olmasini istiyor.
        # Semt sayfalarinda gorunur yol dort basamakti, semada uc basamak vardi.
        crumb = re.search(r'<nav class="crumb[^"]*"[^>]*>(.*?)</nav>', document, flags=re.S)
        if crumb and breadcrumb is not None:
            visible = [clean_text(item) for item in re.findall(r"<li>(.*?)</li>", crumb.group(1), flags=re.S)]
            if visible != breadcrumb:
                raise ValueError(
                    f"{path.name}: BreadcrumbList gorunur yolla ayni degil "
                    f"(gorunur={visible}, sema={breadcrumb})"
                )

        # 9 Eylul 2026 - BEKCI TERS CEVRILDI.
        # Eskiden "sabit tarife" bir "eskimis iddia" sayilip dagitim
        # patlatiliyordu. Yanlis olan o degil, tersi: eczane sayfalarinda
        # "mesafe ve saate gore" demek tarife.php ile CELISIYOR
        # (eczanede mesafe/saat carpani hic uygulanmaz).
        eczane_sayfalari = {
            "eczane-kurye.html", "eczaneden-eve-siparis.html",
            "nobetci-eczane-kurye.html",
        }
        lowered = clean_text(document).lower()
        if path.name in eczane_sayfalari:
            for claim in ("mesafe ve saate", "mesafeye göre değişir"):
                if claim in lowered:
                    raise ValueError(
                        f"{path.name}: eczane sayfasinda yanlis fiyat iddiasi: {claim}"
                    )

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


validate_css()

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
