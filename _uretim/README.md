# Bölge sayfası üretimi

`barsekurye/` altındaki bölge sayfaları elle düzenlenmez — hepsi buradan üretilir.
Bir sayfayı elle değiştirirsen bir sonraki üretimde değişiklik kaybolur.

```bash
python3 _uretim/uret.py
```

## Dosyalar

| Dosya | İşi |
|---|---|
| `bolgeler.py` | Her bölgenin editoryal verisi: giriş metni, taşıdığımız gönderi tipleri, sık gidilen noktalar, komşu bölgeler, bölgeye özel S.S.S. |
| `noktalar_ek.py` | Fiyat hesaplayıcıdaki mahalle/semt listesini tamamlayan ek koordinat verisi |
| `uret.py` | Üretici |

## Üretilen çıktılar

- `barsekurye/<slug>-kurye.html` — 61 bölge sayfası (39 ilçe + 22 mikro bölge)
- `barsekurye/kurye-fiyatlari.html` — güncel tarife sayfası
- `barsekurye/istanbul-ici-kurye.html` — tüm bölgelere iç link veren hub
- `barsekurye/sitemap.xml` — bütün sayfalar + `lastmod`
- `barsekurye/llms.txt` — AI arama motorları için site özeti
- `barsekurye/fiyat-hesaplama.html` içindeki `NOKTALAR` listesi (birleştirilip geri yazılır)

## Tarife tek kaynaktan

Sayfalardaki mesafe, süre ve ücret değerleri `uret.py` içindeki tarife sabitlerinden
hesaplanır; bu sabitler `fiyat-hesaplama.html` içindeki hesaplayıcıyla birebir aynıdır
(taban 380 ₺ / ilk 5 km, 5–25 km 14 ₺, 25 km üzeri 11 ₺, Express ×1,25, VIP ×1,6).
**Fiyat değişirse** `uret.py` içindeki sabitler ile hesaplayıcının JS sabitleri
birlikte güncellenmeli, sonra üretim yeniden çalıştırılmalı.

## Yeni bölge sayfası eklemek

`bolgeler.py` içine yeni bir kayıt ekle (`komsu` alanındaki her slug tanımlı olmalı;
üretici tanımsız komşu bulursa hata verip durur) ve `uret.py`'yi çalıştır.
Sayfa, sitemap ve llms.txt otomatik güncellenir.
