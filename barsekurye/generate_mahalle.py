import os

# Öne çıkan mahalleler (İhtiyaca göre çoğaltılabilir)
mahalleler = [
    {"ilce": "Kadıköy", "mahalle": "Moda"},
    {"ilce": "Beşiktaş", "mahalle": "Çarşı"},
    {"ilce": "Ataşehir", "mahalle": "Finans Merkezi"},
    {"ilce": "Şişli", "mahalle": "Merkez"},
    {"ilce": "Kartal", "mahalle": "Sanayi"},
    {"ilce": "Bağdat Caddesi", "mahalle": "Kurye"}
]

def slugify(text):
    charmap = {'ı': 'i', 'İ': 'i', 'ğ': 'g', 'Ğ': 'g', 'ü': 'u', 'Ü': 'u', 'ş': 's', 'Ş': 's', 'ö': 'o', 'Ö': 'o', 'ç': 'c', 'Ç': 'c'}
    for k, v in charmap.items():
        text = text.replace(k, v)
    return text.lower().replace(' ', '-')

def generate_mahalle_pages():
    try:
        with open('sablon.html', 'r', encoding='utf-8') as f:
            template = f.read()
    except FileNotFoundError:
        template = "<html>\n<head>\n<title>{title}</title>\n</head>\n<body>\n<h1>{baslik}</h1>\n<p>{icerik}</p>\n</body>\n</html>"

    for item in mahalleler:
        ilce = item['ilce']
        mahalle = item['mahalle']
        ilce_slug = slugify(ilce)
        mahalle_slug = slugify(mahalle)
        
        if mahalle == "Kurye":
            filename = f"{ilce_slug}-{mahalle_slug}.html"
        else:
            filename = f"{ilce_slug}-{mahalle_slug}-kurye.html"
        
        title = f"{ilce} {mahalle} Kurye | Barse Kurye"
        baslik = f"{ilce} {mahalle} Hızlı Kurye"
        icerik = f"{ilce} ilçesi {mahalle} bölgesinde gönderileriniz için rota kıyaslaması yapan sistemimizle maksimum 16 pakete kadar kusursuz teslimat sunuyoruz."
        
        content = template.replace('{{TITLE}}', title).replace('{{BASLIK}}', baslik).replace('{{ICERIK}}', icerik).replace('{{MAHALLE_ADI}}', mahalle).replace('{{ILCE_ADI}}', ilce)
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Oluşturuldu: {filename}")

if __name__ == "__main__":
    generate_mahalle_pages()
