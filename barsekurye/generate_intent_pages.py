import os

intents = [
    {"isim": "Moto Kurye", "slug": "moto-kurye"},
    {"isim": "Acil Kurye", "slug": "acil-kurye"},
    {"isim": "7/24 Kurye", "slug": "7-24-kurye"},
    {"isim": "Kurumsal Kurye", "slug": "kurumsal-kurye"},
    {"isim": "Eczane Kurye", "slug": "eczane-kurye"},
    {"isim": "Gümrük Kurye", "slug": "gumruk-kurye"},
    {"isim": "Vip Kurye", "slug": "vip-kurye"},
    {"isim": "Express Kurye", "slug": "express-kurye"}
]

def generate_intent_pages():
    try:
        with open('sablon.html', 'r', encoding='utf-8') as f:
            template = f.read()
    except FileNotFoundError:
        template = "<html>\n<head>\n<title>{title}</title>\n</head>\n<body>\n<h1>{baslik}</h1>\n<p>{icerik}</p>\n</body>\n</html>"

    for intent in intents:
        isim = intent['isim']
        slug = intent['slug']
        filename = f"{slug}.html"
        
        title = f"{isim} Hizmeti | Barse Kurye"
        baslik = f"Profesyonel {isim} Çözümleri"
        icerik = f"Barse Kurye olarak İstanbul genelinde {isim} ihtiyaçlarınız için buradayız. Gelişmiş rota kıyaslamasıyla 16 pakete kadar çoklu gönderilerinizi optimize ediyor ve güvenilir teslimat sağlıyoruz."
        
        content = template.replace('{{TITLE}}', title).replace('{{BASLIK}}', baslik).replace('{{ICERIK}}', icerik).replace('{{INTENT_ADI}}', isim)
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Oluşturuldu: {filename}")

if __name__ == "__main__":
    generate_intent_pages()
