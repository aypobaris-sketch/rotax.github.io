# Barse Kurye — Tasarım Sistemi ve Uygulama Planı

Bu doküman, mevcut 72 sayfalık `barsekurye.com` sitesinin yeniden tasarımı, SEO ve
teknik iyileştirmesi için hazırlanmış **uygulama şartnamesidir**. Yanındaki üç dosya
doğrudan siteye taşınabilir:

| Dosya | Ne işe yarar | Nereye gider |
|---|---|---|
| `barse.css` | Tüm sitenin tek stil dosyası | `/assets/barse.css` |
| `ornek-anasayfa.html` | Ana sayfanın tam referans kodu | `/index.html` |
| `sablon-ic-sayfa.html` | Hizmet ve ilçe sayfası şablonu | ~60 sayfanın iskeleti |

> **Doldurulacak alanlar:** Kodda `{{TELEFON}}`, `{{WHATSAPP}}`, `{{FIYAT_1}}`,
> `{{ADRES}}` gibi süslü parantezli her şey placeholder'dır. Yayına almadan önce
> gerçek bilgilerle değiştirilmelidir. **Uydurma rakam, uydurma yorum ve uydurma
> referans yazılmamalıdır** — istatistik bölümü ve müşteri yorumları için gerçek
> veri yoksa o bölüm tamamen silinmelidir.

---

## 1. Tasarım kararları ve gerekçeleri

| Karar | Gerekçe |
|---|---|
| **Ana renk: güven mavisi** | Kurye/lojistikte mavi "takip edilebilirlik ve kurumsallık" sinyali verir. Hedef kitle (hukuk, muhasebe, eczane) kurumsal alıcı. |
| **Vurgu rengi: turuncu** | Aciliyeti temsil eder ve mavinin tamamlayıcısıdır. Sadece "hemen ara" niyetli yerlerde kullanılır; her yerde kullanılırsa vurgu olmaktan çıkar. |
| **Stil: Swiss / minimal, ızgara temelli** | Bu segmentte dönüşümü artıran şey görsel efekt değil, *bilginin hızlı okunması*: süre, fiyat, telefon. Ağır gölge/gradient dönüşümü düşürür. |
| **Sayfa başına tek birincil CTA** | Her sayfada tek bir birincil aksiyon var: **ara**. WhatsApp ikincil. Form üçüncül. |
| **Mobilde sabit alt çağrı çubuğu** | Bu sektörde trafiğin büyük kısmı mobil ve niyet "şimdi lazım". Ekranın altında sürekli duran "Ara / WhatsApp" çifti, mobil dönüşümü en çok etkileyen tek bileşendir. |
| **Görsel yerine "durum kartı"** | Hero'da stok fotoğraf yerine CSS ile çizilen süre/adım kartı var. Hiç resim yüklenmez → sayfa anında açılır, telifli görsel riski olmaz. |

**Kaçınılacaklar:** yapay zekâ estetiği mor/pembe gradientler, emoji ikonlar, stok
"gülümseyen kurye" fotoğrafları, otomatik dönen slider'lar, açılışta çıkan pop-up'lar.

---

## 2. Renk tokenları

Tümü `barse.css` içinde `:root` altında tanımlı. **Sayfa içine hex yazılmaz**,
her zaman `var(--c-...)` kullanılır.

| Token | Değer | Kullanım | Kontrast |
|---|---|---|---|
| `--c-primary` | `#1D4ED8` | Birincil buton, link | Beyaz yazı **6.70:1** ✅ AAA |
| `--c-primary-dark` | `#1E3A8A` | Hover | — |
| `--c-primary-tint` | `#EFF6FF` | Açık mavi zemin, hero | — |
| `--c-accent` | `#EA580C` | **Sadece grafik/ikon/çizgi** | Beyaz yazıyla 3.56:1 ❌ küçük yazı için yetersiz |
| `--c-accent-text` | `#C2410C` | Turuncu buton ve turuncu yazı | Beyaz yazı **5.18:1** ✅ AA |
| `--c-navy` | `#0B1A33` | Footer, koyu CTA bandı | — |
| `--c-ink` | `#0F172A` | Başlıklar | 17.9:1 ✅ |
| `--c-body` | `#334155` | Gövde metni | **10.4:1** ✅ AAA |
| `--c-muted` | `#64748B` | İkincil metin | **4.76:1** ✅ AA (bunun altına inilmez) |
| `--c-border` | `#E2E8F0` | Çizgi ve kart kenarı | — |
| `--c-success` / `--c-warning` / `--c-danger` | `#15803D` / `#B45309` / `#B91C1C` | Durum | ✅ AA |

**Kritik kural:** `#EA580C` üzerine beyaz küçük yazı **yazılmaz** (3.56:1, WCAG AA'yı
geçmez). Turuncu buton gerektiğinde `--c-accent-text` (`#C2410C`) kullanılır.

---

## 3. Tipografi

Doğrulanmış eşleşme: **"Corporate Trust"** — okunabilirlik için tasarlanmış Lexend +
küçük punto performansı yüksek Source Sans 3. İkisi de Türkçe glifleri (ş ğ ı İ ö ü ç)
tam destekler.

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Lexend:wght@500;600;700;800&family=Source+Sans+3:wght@400;600;700&display=swap">
```

- **Başlık:** Lexend — 600/700/800
- **Gövde:** Source Sans 3 — 400/600/700
- **Ölçek:** 12 / 14 / 16 / 18 / 20 / 24 → başlıklar `clamp()` ile akışkan
- **Mobil gövde minimumu 16px** — altına inilirse iOS sayfayı otomatik zoomlar
- **Satır yüksekliği** gövdede 1.65, başlıkta 1.2
- **Satır uzunluğu** `max-width: 70ch` (`.prose`) — 100+ karakterlik satır okunmaz
- Fiyat/süre gibi rakamlarda `.num` sınıfı → `tabular-nums`, tabloda zıplama olmaz

Ağırlıklar yalnızca yüklenenlerle sınırlıdır; `font-weight: 900` gibi yüklenmemiş bir
değer yazılırsa tarayıcı fontu yapay olarak kalınlaştırır ve bozuk görünür.

---

## 4. Ölçü sistemi

- **Boşluk (4/8 ritmi):** 4, 8, 12, 16, 24, 32, 48, 64, 96 → `--sp-1` … `--sp-9`
- **Bölüm arası:** mobil 48px, masaüstü 96px (`.section`)
- **Köşe:** 6 / 10 / 16px, hap butonlar 999px
- **Gölge:** üç kademe (`--shadow-sm/-/-lg`), rastgele gölge değeri yazılmaz
- **Konteyner:** `max-width: 1160px` (`.wrap`)
- **Kırılma noktaları:** 640 / 768 / 900 / 1024px — mobil önce yazılır
- **Dokunma alanı:** her buton ve menü öğesi **min 48px** yükseklik

---

## 5. Bileşen envanteri

`barse.css` içinde hazır gelen bileşenler:

| Sınıf | Bileşen |
|---|---|
| `.header` `.nav` `.nav-toggle` `.mobile-menu` | Yapışkan üst menü + mobil menü |
| `.callbar` | Mobil sabit Ara/WhatsApp çubuğu |
| `.hero` `.status-card` `.badge` `.trust-list` | Hero bloğu |
| `.btn` (`--primary` `--accent` `--outline` `--ghost-light` `--lg` `--block`) | Butonlar |
| `.card` `.card--link` `.card__icon` | Hizmet ve sektör kartları |
| `.steps` | Numaralı "nasıl çalışır" |
| `.stats` `.stat-value` | İstatistik şeridi |
| `.chips` | İlçe/bölge etiket linkleri |
| `.table-scroll` + `table` | Fiyat tablosu (mobilde yatay kayar) |
| `.faq` + `<details>` | SSS — JavaScript gerekmez |
| `.form` `.field` | Teklif formu |
| `.breadcrumb` | İç sayfa yol göstergesi |
| `.prose` `.callout` | Uzun metin ve vurgu kutusu |
| `.cta-band` `.footer` | Kapanış ve alt bilgi |

**İkonlar:** Sayfanın başındaki `<svg><symbol>` bloğu 15 ikon içerir, `<use href="#i-...">`
ile çağrılır. Emoji kullanılmaz — emoji her cihazda farklı görünür ve renk tokenıyla
yönetilemez.

---

## 6. 72 sayfanın yapısı

Sayfalar dört şablona indirgenir. Bu, hem bakımı hem tutarlılığı çözer:

| Şablon | Yaklaşık adet | Dosya |
|---|---|---|
| **A — Ana sayfa** | 1 | `ornek-anasayfa.html` |
| **B — Hizmet sayfası** (evrak, ilaç, kurumsal, e-ticaret, acil, gece…) | ~10 | `sablon-ic-sayfa.html` |
| **C — Bölge/ilçe sayfası** (Kadıköy, Şişli, Beşiktaş…) | ~50 | `sablon-ic-sayfa.html` |
| **D — Kurumsal sayfalar** (hakkımızda, iletişim, fiyatlar, gizlilik) | ~8 | `sablon-ic-sayfa.html` (sade varyant) |

### İç link omurgası
```
Ana sayfa
 ├── /hizmetler/ ──── 10 hizmet sayfası ──┐
 ├── /bolgeler/ ───── 50 ilçe sayfası ────┤→ hepsi birbirine ve /iletisim/'e bağlanır
 └── /kurumsal-kurye/ (dönüşüm sayfası) ──┘
```
Her ilçe sayfası **komşu 4 ilçeye** ve **ilgili 2 hizmete** link verir. Böylece hiçbir
sayfa "yetim" kalmaz ve Google tüm sayfaları tarayabilir.

---

## 7. SEO planı

### 7.1 En büyük risk: kopya içerik
50 ilçe sayfası aynı metnin ilçe adı değiştirilmiş hâliyse Google bunların çoğunu
indekslemez. Her ilçe sayfasında **en az şu üçü gerçekten farklı olmalı**:

1. Bölgeye özel bilgi tablosu (ortalama süre, sık gidilen noktalar, komşu ilçe geçiş süreleri)
2. Mahalle listesi (o ilçenin gerçek mahalleleri)
3. En az 2 bölgeye özel SSS sorusu

Şablondaki "Kadıköy Adliyesi", "Söğütlüçeşme akşam trafiği" gibi ayrıntılar tam olarak
bunun örneğidir. **Hedef: sayfa başına 400–700 kelime gerçek bilgi.**

### 7.2 Title ve description formülleri

| Sayfa tipi | Title (50–60 karakter) | Description (140–155 karakter) |
|---|---|---|
| Ana sayfa | `İstanbul Moto Kurye \| 30 Dakikada Teslimat – Barse Kurye` | Hizmet + bölge + vaat + telefon |
| İlçe | `[İlçe] Moto Kurye \| 30 Dakikada Teslimat – Barse Kurye` | `[İlçe] ve çevresinde 7/24 moto kurye…` + telefon |
| Hizmet | `[Hizmet] \| İstanbul 7/24 Kurye – Barse Kurye` | Hizmetin ne olduğu + kime + süre |

Her sayfada `<title>`, `<meta description>` ve `<link rel="canonical">` **benzersiz** olmalı.
Aynı title'ı taşıyan iki sayfa varsa biri elenir.

### 7.3 Yapısal veri (schema.org)

| Şema | Nerede |
|---|---|
| `CourierService` (LocalBusiness alt tipi) | **Sadece ana sayfada**, `@id` ile |
| `BreadcrumbList` | Tüm iç sayfalarda |
| `FAQPage` | SSS içeren her sayfada (sorular sayfada **görünür** olmalı) |

`openingHoursSpecification` 00:00–23:59 olarak verilir — 7/24 çalışma böyle işaretlenir.
`areaServed` İstanbul; ilçe sayfalarında ilçe adıyla daraltılabilir.

### 7.4 Teknik SEO kontrol listesi
- [ ] `sitemap.xml` — 72 sayfanın tamamı, `robots.txt` içinde referansı
- [ ] `robots.txt` — hiçbir içerik sayfası engellenmemeli
- [ ] Tek URL biçimi: `https://www.barsekurye.com/kadikoy-kurye/` (sonda slash, hep aynı)
- [ ] `http://` ve slash'sız sürümler 301 ile tek sürüme yönlendirilir
- [ ] Her sayfada **tek bir `<h1>`**, ardından atlamasız h2 → h3
- [ ] Görsellerde açıklayıcı `alt`; dekoratif SVG'lerde `aria-hidden="true"`
- [ ] Google Business Profile ile ad/adres/telefon **birebir aynı** yazılır (NAP tutarlılığı)
- [ ] 404 sayfası siteye link veren gerçek bir sayfa olmalı

---

## 8. Teknik iyileştirmeler

### 8.1 En kritik: stilin tek dosyaya taşınması
72 sayfada CSS her sayfanın içinde ayrı ayrı duruyorsa:
- Tek renk değişikliği 72 dosya düzenlemek demektir
- Tarayıcı her sayfada stili yeniden indirir (önbelleğe alamaz)

**Yapılacak:** tüm stil `/assets/barse.css` dosyasına alınır, her sayfa tek satırla
bağlanır. İkinci sayfadan itibaren CSS önbellekten gelir → site belirgin şekilde hızlanır.

### 8.2 Tekrarlayan blokların tek kaynağa indirilmesi
Header, footer, ikon seti ve mobil çubuk 72 sayfada birebir aynı. Bunlar bugün elle
kopyalanıyorsa menüye bir link eklemek 72 dosya değişikliği demektir.

Site düz HTML ve GitHub Pages üzerinde olduğu için iki gerçekçi yol var:
1. **Basit yol:** blokları `parcalar/` altında tutup değişiklikleri küçük bir script'le
   72 dosyaya yaymak.
2. **Kalıcı yol:** GitHub Pages'in Jekyll desteğini kullanmak —
   `_includes/header.html` yazılır, sayfalarda `{% include header.html %}` çağrılır.
   Ek araç kurulumu gerekmez, Pages bunu kendisi derler.

### 8.3 Performans
- [ ] Fontlarda `preconnect` + `display=swap` (yapıldı) — metin asla görünmez kalmaz
- [ ] Görsellerde `width`/`height` verilir → sayfa zıplaması (CLS) olmaz
- [ ] Ekranın altındaki görsellerde `loading="lazy"`
- [ ] Görseller WebP'ye çevrilir
- [ ] Harici script (chat widget, analytics) `defer` ile yüklenir; gerekmeyeni kaldırılır
- [ ] Slider/animasyon kütüphanesi kullanılmaz — bu sitede ihtiyaç yok

### 8.4 Erişilebilirlik
- [ ] "İçeriğe geç" bağlantısı (yapıldı)
- [ ] Klavye odak halkası hiçbir yerde `outline: none` ile silinmez
- [ ] Menü butonunda `aria-expanded`, Esc ile kapanma (yapıldı)
- [ ] Bulunduğun sayfa menüde `aria-current="page"` ile işaretlenir
- [ ] `prefers-reduced-motion` desteklenir (yapıldı)
- [ ] Telefon numarası `tel:` linki olarak verilir, düz metin bırakılmaz

---

## 9. Uygulama sırası

Hepsini aynı anda değiştirmeye çalışmak riskli. Önerilen sıra:

**1. Aşama — Temel (en yüksek kazanç)**
`barse.css` yayına alınır, ana sayfa yeni tasarımla değiştirilir, mobil çağrı çubuğu
tüm sayfalara eklenir, header/footer tek kaynağa taşınır.

**2. Aşama — Dönüşüm sayfaları**
`/kurumsal-kurye/`, `/fiyatlar/`, `/iletisim/` ve 10 hizmet sayfası yeni şablona geçirilir.

**3. Aşama — Bölge sayfaları**
50 ilçe sayfası şablona geçirilir. Bu aşamada asıl iş tasarım değil, **her ilçeye özel
gerçek içeriğin yazılmasıdır**; kopya metinle geçirilirse SEO açısından zarar verir.

**4. Aşama — SEO tamamlama**
Sitemap, schema, canonical, yönlendirmeler, Google Business Profile eşitlemesi.

---

## 10. Yayın öncesi kontrol listesi

- [ ] 375px genişlikte yatay kaydırma yok
- [ ] Tüm buton ve menü öğeleri en az 48px yükseklikte
- [ ] Gövde metni beyaz üzerinde en az 4.5:1 kontrastta
- [ ] `#EA580C` üzerine küçük beyaz yazı hiçbir yerde yok
- [ ] Klavyeyle sekme yapıldığında odak her adımda görünüyor
- [ ] Emoji ikon yok, tüm ikonlar SVG
- [ ] Her sayfada tek `<h1>`, benzersiz title ve canonical
- [ ] `{{...}}` placeholder'ların hiçbiri yayında kalmadı
- [ ] Uydurma istatistik / uydurma müşteri yorumu yok
- [ ] Telefon numarası mobilde tek dokunuşla aranıyor
