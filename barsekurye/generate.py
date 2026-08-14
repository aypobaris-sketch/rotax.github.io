import os

# İstanbul ilçeleri
ilceler = [
    "Adalar", "Arnavutköy", "Ataşehir", "Avcılar", "Bağcılar", "Bahçelievler", "Bakırköy",
    "Başakşehir", "Bayrampaşa", "Beşiktaş", "Beykoz", "Beylikdüzü", "Beyoğlu", "Büyükçekmece",
    "Çatalca", "Çekmeköy", "Esenler", "Esenyurt", "Eyüpsultan", "Fatih", "Gaziosmanpaşa",
    "Güngören", "Kadıköy", "Kağıthane", "Kartal", "Küçükçekmece", "Maltepe", "Pendik",
    "Sancaktepe", "Sarıyer", "Silivri", "Sultanbeyli", "Sultangazi", "Şile", "Şişli",
    "Tuzla", "Ümraniye", "Üsküdar", "Zeytinburnu"
]

def slugify(text):
    charmap = {'ı': 'i', 'İ': 'i', 'ğ': 'g', 'Ğ': 'g', 'ü': 'u', 'Ü': 'u', 'ş': 's', 'Ş': 's', 'ö': 'o', 'Ö': 'o', 'ç': 'c', 'Ç': 'c'}
    for k, v in charmap.items():
        text = text.replace(k, v)
    return text.lower().replace(' ', '-')

def generate_ilce_pages():
    try:
        with open('sablon.html', 'r', encoding='utf-8') as f:
            template = f.read()
    except FileNotFoundError:
        # Şablon bulunamazsa basit bir taslak kullan
        template = "<html>\n<head>\n<title>{title}</title>\n</head>\n<body>\n<h1>{baslik}</h1>\n<p>{icerik}</p>\n</body>\n</html>"

    for ilce in ilceler:
        slug = slugify(ilce)
        filename = f"{slug}-kurye.html"
        
        title = f"{ilce} Kurye | Barse Kurye - Rota Kıyaslamalı Teslimat"
        baslik = f"{ilce} Kurye Hizmeti"
        icerik = f"Barse Kurye olarak {ilce} bölgesinde en uygun rotayı belirleyerek gönderilerinizi hızla ulaştırıyoruz. Akıllı rota kıyaslaması sayesinde 16 pakete kadar olan teslimatlarınızı güvenle ve en iyi sürelerde taşıyoruz."
        
        # Etiketleri değiştir
        content = template.replace('{{TITLE}}', title).replace('{{BASLIK}}', baslik).replace('{{ICERIK}}', icerik).replace('{{ILCE_ADI}}', ilce)
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Oluşturuldu: {filename}")

if __name__ == "__main__":
    generate_ilce_pages()
