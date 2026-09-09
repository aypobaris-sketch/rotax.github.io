import os

intents = [
    {"isim": "Moto Kurye", "slug": "moto-kurye"},
    {"isim": "Acil Kurye", "slug": "acil-kurye"},
    {"isim": "7/24 Kurye", "slug": "7-24-kurye"},
    {"isim": "Kurumsal Kurye", "slug": "kurumsal-kurye"},
    {"isim": "Eczane Kurye", "slug": "eczane-kurye"},
    {"isim": "Gümrük Kurye", "slug": "gumruk-kurye"}
]
# VIP, hızlı ve express aramaları acil-kurye.html altında birlikte hedeflenir;
# ayrı sayfalar açmak aynı niyette sayfa çakışması yaratır.

def generate_intent_pages():
    try:
        with open('sablon.html', 'r', encoding='utf-8') as f:
            template = f.read()
    except FileNotFoundError:
        raise SystemExit("sablon.html bulunamadı; mevcut SEO sayfalarını korumak için üretim durduruldu")

    for intent in intents:
        isim = intent['isim']
        slug = intent['slug']
        filename = f"{slug}.html"
        if os.path.exists(filename):
            print(f"Atlandı, mevcut sayfa korundu: {filename}")
            continue

        title = f"{isim} İstanbul | 7/24 Net Fiyat — Barse"
        baslik = f"İstanbul {isim}"
        icerik = f"İstanbul'un 39 ilçesinde {isim} hizmeti sağlıyoruz. Evrak, ilaç ve kurumsal gönderiler için ücret kurye yola çıkmadan netleşir."
        
        content = template.replace('{{TITLE}}', title).replace('{{BASLIK}}', baslik).replace('{{ICERIK}}', icerik).replace('{{INTENT_ADI}}', isim)
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Oluşturuldu: {filename}")

if __name__ == "__main__":
    generate_intent_pages()
