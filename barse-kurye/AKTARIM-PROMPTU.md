# Diğer Claude'a Verilecek Prompt

Aşağıdaki metni, Barse Kurye sitesinin bulunduğu projede çalışan Claude'a olduğu gibi
yapıştırın. Yanına şu üç dosyayı da ekleyin: `barse.css`, `ornek-anasayfa.html`,
`sablon-ic-sayfa.html` ve `TASARIM-SISTEMI.md`.

---

## ▼ BURADAN KOPYALA ▼

Barsekurye.com için hazırlanmış bir tasarım sistemi var. Ekteki dosyaları kaynak kabul
et ve siteyi bunlara göre yenile. Site düz HTML + elle yazılmış CSS; React veya Tailwind
kullanma, mevcut yapıyı koru.

**Ekteki dosyalar:**
- `TASARIM-SISTEMI.md` — tüm kurallar, renk/tipografi tokenları, SEO ve teknik plan
- `barse.css` — sitenin tek stil dosyası, hazır
- `ornek-anasayfa.html` — ana sayfanın tam referans kodu
- `sablon-ic-sayfa.html` — hizmet ve ilçe sayfası şablonu

**Yapmanı istediklerim, bu sırayla:**

1. **Önce mevcut durumu çıkar.** 72 sayfayı tara ve bana şunu raporla: hangi sayfalar
   hangi şablona giriyor (ana sayfa / hizmet / ilçe / kurumsal), CSS her sayfanın içinde
   mi yoksa ortak dosyada mı, header-footer blokları birebir aynı mı, hangi sayfalarda
   `<title>` veya meta description eksik/tekrar ediyor. **Bu raporu almadan kod
   değiştirme.**

2. **`barse.css` dosyasını `/assets/barse.css` olarak ekle.** Sonra ana sayfayı
   `ornek-anasayfa.html`'e göre yeniden yaz. Koddaki `{{TELEFON}}`, `{{WHATSAPP}}`,
   `{{FIYAT_1}}` gibi placeholder'ları sitedeki **mevcut gerçek bilgilerle** doldur.
   Gerçek bilgiyi bulamazsan bana sor — **uydurma**.

3. **İstatistik bölümü ve müşteri yorumları:** elinde gerçek rakam/yorum yoksa o bölümü
   tamamen sil. Uydurulmuş sayı veya sahte müşteri yorumu yazma.

4. **Header, footer, ikon seti ve mobil çağrı çubuğunu tek kaynağa taşı.** Site GitHub
   Pages üzerindeyse Jekyll `_includes` kullan (`{% include header.html %}`); bu mümkün
   değilse `parcalar/` klasörü + yayma script'i kur. Amaç: menüye link eklemek için 72
   dosya düzenlemek zorunda kalmamak.

5. **İç sayfaları şablona geçir.** Önce dönüşüm sayfaları (`/kurumsal-kurye/`,
   `/fiyatlar/`, `/iletisim/` + hizmet sayfaları), sonra ilçe sayfaları.

6. **İlçe sayfalarında kopya içerik üretme.** Bu en kritik madde: 50 ilçe sayfası aynı
   metnin ilçe adı değiştirilmiş hâli olursa Google çoğunu indekslemez. Her ilçe
   sayfasında şu üçü gerçekten farklı olmalı:
   - bölgeye özel bilgi tablosu (ortalama süre, sık gidilen noktalar, komşu ilçe geçiş süreleri)
   - o ilçenin gerçek mahalle listesi
   - en az 2 bölgeye özel SSS sorusu

   Bir ilçe hakkında gerçek bilgi bulamıyorsan o sayfayı geçici olarak atla ve bana
   listesini ver.

7. **SEO'yu tamamla:** her sayfaya benzersiz title + description + canonical, ana
   sayfaya `CourierService` şeması, iç sayfalara `BreadcrumbList`, SSS olan sayfalara
   `FAQPage`, tüm sayfaları içeren `sitemap.xml` ve `robots.txt`.

**Uyman gereken kurallar:**
- Renk ve ölçü değerlerini sayfa içine hex olarak yazma; `barse.css`'teki `var(--...)`
  tokenlarını kullan.
- `#EA580C` üzerine küçük beyaz yazı yazma (kontrast 3.56:1, WCAG AA'yı geçmiyor).
  Turuncu buton gerekiyorsa `var(--c-accent-text)` (`#C2410C`) kullan.
- İkon olarak emoji kullanma; sayfadaki SVG `<symbol>` setini `<use href="#i-...">` ile çağır.
- Odak halkasını (`:focus-visible`) hiçbir yerde kaldırma.
- Her sayfada tek `<h1>` olsun, başlık seviyesi atlama.
- Her sayfa 375px genişlikte yatay kaydırma yapmadan çalışsın.
- Buton ve menü öğeleri en az 48px yükseklikte olsun.

Her aşama sonunda ne değiştiğini kısaca özetle ve bir sonraki aşamaya geçmeden önce
onay iste.

## ▲ BURAYA KADAR ▲
