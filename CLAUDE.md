# Barse Kurye — proje hafızası

İstanbul'da tek kişilik moto-kurye işletmesi (Barse Kurye). Bu depo sitenin
**yalnızca statik ön yüzünü** tutar. Canlı site cPanel'de PHP ile çalışır.

> **Bu depo PUBLIC.** Buraya yazdığın her şey herkese açıktır.
> İş verisi, reklam stratejisi, ciro, müşteri kaydı, anahtar/negatif kelime
> listesi **bu dosyaya veya depoya yazılmaz.** Onlar ayrı özel hafıza
> dosyasındadır (aşağıya bak).

---

## Asla yapılmayacaklar

1. **`panel-sifre.php` depoya girmez.** Şifre ve API anahtarları içerir.
   Barış'a gönderilen hiçbir pakete de konmaz — sunucuda zaten var.
   `.gitignore` içindeki `barsekurye/**/*.php` bunu kazadan korur; kuralı gevşetme.
2. **`barsekurye/data/` asla eski yedekten üzerine yazılmaz.** İçinde canlı
   müşteri kayıtları ve iş geçmişi var. Sunucuya gönderilen zip'lerde bu klasör
   bulunmaz.
3. **API anahtarı değerleri sohbete yazılmaz.** Ne teyit için, ne örnek için.
4. **Panel şifresi ve ORS anahtarı konusu kapalı.** Barış ikisini de
   değiştirmeyeceğini net söyledi; tekrar açma.

## Barış'ın çalışma şekli

- **Bilgisayarı yok, her şeyi telefondan yapıyor.** Çok adımlı talimat işe
  yaramıyor. Tek zip → çıkar → bitti. Adım sayısını en aza indir.
- Geri alınabilir işleri **sorma, yap.** ("kanka önceden herşeyi yapiodun")
- Geri alınamayan / dışarı çıkan işlerde (reklam silme, gönderi yayınlama,
  ödeme) önce sor.
- Türkçe konuşuyor; cevaplar Türkçe olmalı.

---

## Site yapısı

```
barsekurye/
  *.html                 76 sayfa (ilçe + hizmet + kurumsal)
  assets/barse.css       tek stil dosyası
  images/01-ofis .. 08-afis
      08-afis/           39 ilçe afişi, 1408x768 webp (hero görseli)
  og/                    70 paylaşım görseli (sayfa başına bir og:image)
  poster/                39 ilçe afişi, 700x990 (WhatsApp / İşletme Profili)
```

Sunucuda ayrıca (depoda **yok**): `panel.php`, `panel-sifre.php`, `tarife.php`,
`giris-koruma.php`, `bot-koruma.php`, `tuzak.php`, `eylem.php`,
`panel-hesaplayici.php`, `uygulama/index.php`, `data/`.

## Kurallar ve tuzaklar

**Önbellek damgası.** CSS değiştiğinde 76 sayfadaki `barse.css?v=YYYYMMDD`
damgası da güncellenmeli, yoksa telefonlarda eski stil kalır.

**`.sahne--afis` kuralı `barse.css` sonunda durmalı.** Yukarıdaki medya
sorgusuyla aynı özgüllükte; sırayı bozarsan afişler yeniden kırpılmaya başlar.
Afiş tasarlanmış bir görsel — `object-fit:cover` ilçe adını ve telefonu kesiyor,
bu yüzden `contain`.

**Hero görsel eşlemesi.** İlçe adı taşıyan fotoğraf yalnızca kendi ilçesinin
sayfasında kullanılır. Diğer sayfalara nötr fotoğraf gider ve alt metni
sahneyi anlatır, konum iddia etmez. (Bir kez bozuldu: Bayrampaşa sayfası
Kartal fotoğrafı gösteriyordu.)

**Türkçe büyük harf.** Python `.upper()` `BEŞIKTAŞ` üretir. Doğrusu:
```python
s.replace('i','İ').replace('ı','I').upper()
```

**Fiyat tek kaynaktan.** Sunucudaki `tarife.php` tek doğruluk kaynağı:
açılış 400 TL (ilk 10 km dahil) + 26 TL/km, gece +%25, hız çarpanları
normal/express/vip, çarpan tavanı 2.00. Panel, uygulama ve site hesaplayıcısı
`require_once tarife.php` yapar ve `tarife_js()` ile aynı sayıları JS'e basar.
Dördüncü bir kopya açma — daha önce dört kopya dört farklı fiyat veriyordu.

**Tıklama takibi.** 76 sayfada `click` yakalayıcı `tel:` ve `wa.me` linklerini
hem `eylem.php`'ye (çerez izni gerektirmez, sunucu tarafı) hem `gtag`'e yazar.
`data/eylem-kayit.csv` gerçeğin kaynağıdır; Google Ads'in gördüğü sayı değil.

**Google reklam metninde telefon numarası YASAK** (`PHONE_NUMBER_IN_AD_TEXT`).
Hem Google Ads reklam metni hem İşletme Profili gönderi metni için geçerli —
otomatik ret. Görselin içinde numara olabilir.

**Google Ads sınırı:** reklam grubu başına en fazla 3 etkin RSA.

## Ortam

- Site `curl/` user-agent'ını `.htaccess` ile engelliyor; tarayıcı UA gerekir.
- Giden proxy düz HTTP'yi tamamen engelliyor; `www.google.com` de kapalı.
- Chromium: `/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell`
  (`--headless --screenshot --window-size`).
- Google Ads işleri **Opus Growth (Aaa)** bağlantısı üzerinden yapılır.
  Görünen araçlar tam liste değil: önce `search_tools(query)`, sonra
  `call_tool(name, arguments)`. Windsor bağlantısı kullanılmaz (kopuk, ayrıca
  `bid_modifier`, `adgroup_id`, `location_service_area` alanlarını hiç
  doldurmuyordu — oradan okunan "boş" değerler yanlış yorumlanmıştı).

## Bir alan okunamıyorsa

Okunamadığını söyle. Boş dönen bir alanı "demek ki ayarlanmamış" diye yorumlama.
Bu hata bir kez yapıldı ve yanlış öneriye yol açtı.

---

## Özel hafıza dosyası

Reklam hesabı kimlikleri, kampanya durumu, gerçek dönüşüm rakamları, kelime
verimliliği ve strateji **`BARSE-HAFIZA-OZEL.md`** dosyasındadır. Public depoya
konmaz. Barış'ta duruyor — yeni oturumun başında ondan iste, o yükler.
