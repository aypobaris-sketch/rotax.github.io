#!/usr/bin/env python3
"""Barse Kurye — hiz kademesi sure ve carpan guncellemesi.

Normal  2-3 saat      x1    ->  90 dk - 2 saat   x1
Express 60-90 dakika  x1.4  ->  45-60 dakika     x1.25
VIP     30-60 dakika  x1.8  ->  30-45 dakika     x1.6

Taban fiyat formulune (380 taban / +14 / +11) DOKUNULMAZ.
"""
import os, glob, collections

SITE = os.path.dirname(os.path.abspath(__file__))

DEGISIM = [
    # --- 1. Hesaplayici acilir menusu (57 sayfa) ---
    ('<option value="1">Normal — 2-3 saat</option>',
     '<option value="1">Normal — 90 dk - 2 saat</option>'),

    ('<option value="1.4">Express — 60-90 dakika</option>',
     '<option value="1.25">Express — 45-60 dakika</option>'),

    ('<option value="1.8">VIP — 30-60 dakika (özel kurye)</option>',
     '<option value="1.6">VIP — 30-45 dakika (özel kurye)</option>'),

    # --- 2. Hizmet kartlarindaki sure rozetleri ---
    ('<div class="time"><span>120–180 dk</span>',
     '<div class="time"><span>90 dk – 2 saat</span>'),

    ('<div class="time"><span>60–90 dk</span>',
     '<div class="time"><span>45–60 dk</span>'),

    ('<div class="time"><span>30–60 dk</span>',
     '<div class="time"><span>30–45 dk</span>'),

    # --- 3. Metin icindeki sure ifadeleri ---
    ('Express ve VIP kurye seçeneklerimizle 30-90 dakika aralığında teslimat sağlıyoruz.',
     'Express ve VIP kurye seçeneklerimizle 30-60 dakika aralığında teslimat sağlıyoruz.'),

    # --- 4. SSS metni + JSON-LD sema (ikisi ayni cumleyi tasiyor) ---
    ('Standart gönderiye göre daha kısa sürede, genellikle 60-90 dakika içinde teslim edilir.',
     'Standart gönderiye göre daha kısa sürede, genellikle 45-60 dakika içinde teslim edilir.'),

    ('acil durumlarda ekspres ve VIP seçenekleriyle bu süre 30-60 dakikaya kadar iner.',
     'acil durumlarda ekspres ve VIP seçenekleriyle bu süre 30-45 dakikaya kadar iner.'),
]

sayim = collections.Counter()
dosya_sayisi = 0

hedefler = sorted(glob.glob(os.path.join(SITE, "*.html")) + glob.glob(os.path.join(SITE, "*.py"))) + [p for p in [os.path.join(SITE,"hesap.js")] if os.path.exists(p)]

for yol in hedefler:
    s = open(yol, encoding="utf-8").read()
    orj = s
    for eski, yeni in DEGISIM:
        if eski in s:
            sayim[eski] += s.count(eski)
            s = s.replace(eski, yeni)
    if s != orj:
        open(yol, "w", encoding="utf-8").write(s)
        dosya_sayisi += 1

print(f"Guncellenen dosya: {dosya_sayisi}\n")
for eski, _ in DEGISIM:
    etiket = eski[:62].replace("\n", " ")
    print(f"  {sayim[eski]:>3} x  {etiket}...")

# --- dogrulama: eski deger kalmis mi? ---
print("\n=== KALINTI KONTROLU ===")
kalinti = 0
for kotu in ['value="1.4"', 'value="1.8"', '2-3 saat', '120–180 dk',
             '60–90 dk', '30–60 dk', '60-90 dakika', '30-90 dakika']:
    bulunan = [os.path.basename(y) for y in hedefler
               if kotu in open(y, encoding="utf-8").read()]
    if bulunan:
        kalinti += 1
        print(f"  KALDI: {kotu}  ->  {bulunan[:4]}{' ...' if len(bulunan) > 4 else ''}")
print("  Temiz - eski deger kalmadi." if not kalinti else f"  {kalinti} kalinti var!")
