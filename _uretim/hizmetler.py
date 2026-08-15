# -*- coding: utf-8 -*-
"""Hizmet sayfalarinin icerigi.

Blok tipleri
------------
("metin",   kicker, h2, [paragraf, ...])
("kartlar", kicker, h2, alt, [(etiket, baslik, metin), ...])
("liste",   kicker, h2, alt, [madde, ...])
("tablo",   kicker, h2, alt, [sutun basliklari], [(satir hucreleri), ...])
"""

HIZMETLER = {

# =====================================================================
"acil-kurye": dict(
    ad="Acil Kurye",
    h1="Acil Kurye",
    baslik="Acil Kurye İstanbul | 30 Dakikada Yola Çıkan Kurye – Barse Kurye",
    aciklama="İstanbul'da acil kurye: talebi aldığımız anda en yakın motor yönlendirilir, "
             "gönderi başka adrese uğramadan teslim edilir. 7/24 açık, 0534 761 83 88.",
    eyebrow="Ortalama 20 dakikada alım · 7/24 açık",
    gorsel=("images/06-hizmet/express-kurye-sure.webp",
            "Acil gönderiyi teslim etmek için yola çıkan Barse Kurye moto kuryesi"),
    giris="Acil iş, planlanmış işten farklı yönetilir. Sıraya alınmaz, güzergâha eklenmez ve "
          "başka teslimatla birleştirilmez. Talebi aldığımız anda bölgeye en yakın kurye bulunur, "
          "gönderi doğrudan alınır ve tek durak olarak teslim edilir.",
    bloklar=[
        ("kartlar", "Nasıl işliyor", "Acil talep geldiğinde ne oluyor?",
         "Telefon açıldığı andan teslime kadar dört adım; aradaki her adımda bilgi veriyoruz.",
         [("01", "Talep alınır", "Alım ve teslim adresini, gönderinin ne olduğunu söylüyorsunuz. Net fiyatı aynı konuşmada veriyoruz."),
          ("02", "Kurye atanır", "Operasyon ekibi bölgedeki en yakın motoru bulur ve doğrudan yönlendirir; başka iş yüklenmez."),
          ("03", "Alım yapılır", "Kurye adrese ulaştığında haber veriyoruz. Ortalama alım süresi merkez ilçelerde 15–25 dakika."),
          ("04", "Teslim edilir", "Teslim tamamlandığında bilgi geçilir; istenirse teslim fotoğrafı paylaşılır.")]),

        ("metin", "Hangi işler acil", "Acil kurye en çok hangi durumlarda çağrılıyor?",
         ["En sık gelen acil talep, saate kilitli evraklar: duruşma dosyası, ihale zarfı, imza bekleyen sözleşme, "
          "gün sonuna yetişmesi gereken teminat mektubu. Bu işlerde teslim süresi değil, teslimin belirli bir "
          "saatten önce tamamlanması önemli; biz de planı o saatten geriye doğru kuruyoruz.",
          "İkinci sırada sağlıkla ilgili gönderiler geliyor: reçeteli ilaç, tahlil numunesi, hastaneye ulaştırılması "
          "gereken rapor. Üçüncü sırada ise üretimi durduran teknik parçalar var — bir yedek parça beklerken duran "
          "makine, kurye ücretinden çok daha pahalıya mal olur.",
          "Ticari tarafta ise unutulan anahtar ve kart, müşteriye yetiştirilmesi gereken numune, havalimanına "
          "yetişecek belge gibi işler sık karşımıza çıkıyor. Hepsinde ortak nokta aynı: gönderinin beklemeye tahammülü yok."]),

        ("tablo", "Süre", "Acil teslimatta gerçekçi süreler",
         "Aşağıdaki süreler kapıdan kapıya, hafta içi gündüz saatleri içindir. Yaka geçişlerinde köprü trafiğine göre 15–25 dakika eklenir.",
         ["Mesafe", "Alım", "Teslim", "Toplam"],
         [("0 – 5 km", "15–25 dk", "10–20 dk", "25–45 dk"),
          ("5 – 10 km", "15–25 dk", "20–35 dk", "35–60 dk"),
          ("10 – 20 km", "20–30 dk", "35–55 dk", "55–85 dk"),
          ("20 km ve üzeri", "20–30 dk", "55–90 dk", "75–120 dk")]),

        ("liste", "Bilmekte fayda var", "Acil işi hızlandıran şeyler",
         "Aşağıdakileri baştan paylaşırsanız teslim süresi belirgin biçimde kısalıyor.",
         ["Tam adres: bina adı, kat, daire ya da blok numarası",
          "Adreste gönderiyi teslim edecek ve teslim alacak kişinin telefonu",
          "Gönderinin ne olduğu ve yaklaşık boyutu — motorla taşınıp taşınamayacağını buradan biliyoruz",
          "Varsa son teslim saati; planı bu saate göre kuruyoruz",
          "Bina girişinde kimlik veya ziyaretçi kaydı gerekiyorsa bunun bilgisi",
          "Ödemeyi gönderen mi alıcı mı yapacak"]),
    ],
    sss=[("Acil kurye kaç dakikada gelir?",
          "Merkez ilçelerde alım genellikle 15–25 dakika içinde yapılır. Talebi aldığımız anda bölgedeki en yakın "
          "kurye yönlendirilir; kurye yolda başka hiçbir adrese uğramaz."),
         ("Gece veya hafta sonu acil kurye bulabilir miyim?",
          "Evet, 7/24 çalışıyoruz. 20:00 – 06:00 arası gece tarifesi, Cumartesi ve Pazar günlerinde hafta sonu "
          "tarifesi uygulanır; farkı çıkıştan önce söylüyoruz."),
         ("Acil kurye ile normal kurye arasındaki fiyat farkı ne?",
          "Acil işlerde genellikle Express (×1,25) veya VIP (×1,6) tarifesi geçerli olur. VIP'te gönderiye özel "
          "kurye atanır ve başka teslimatla birleştirilmez."),
         ("Duruşma veya ihale saatine yetişmesi gerekiyor, garanti verir misiniz?",
          "Trafik nedeniyle dakika garantisi vermiyoruz; bunun yerine hedef saati baştan konuşup çıkışı ona göre "
          "planlıyoruz. Süre riskliyse bunu açıkça söyler, daha erken çıkış öneririz."),
         ("Acil gönderiyi takip edebilir miyim?",
          "Alım yapıldığında ve teslim tamamlandığında bilgilendiriyoruz. Ara durumu telefon veya WhatsApp "
          "üzerinden istediğiniz an sorabilirsiniz.")],
    ilgili=["7-24-kurye", "moto-kurye", "kurumsal-kurye"],
    bolge=["kagithane", "sisli", "levent", "kadikoy", "atasehir-finans", "caglayan"],
),

# =====================================================================
"moto-kurye": dict(
    ad="Moto Kurye",
    h1="Moto Kurye",
    baslik="Moto Kurye İstanbul | Trafiğe Takılmadan Teslimat – Barse Kurye",
    aciklama="İstanbul'da moto kurye hizmeti: 39 ilçede 7/24 motorlu teslimat. Hangi gönderiler taşınır, "
             "ağırlık sınırı nedir, araçlı taşımaya göre ne kadar hızlı? 0534 761 83 88.",
    eyebrow="39 ilçede motorlu teslimat · 7/24 açık",
    gorsel=("images/02-motor/istanbul-trafik-moto-kurye.webp",
            "İstanbul trafiğinde ilerleyen Barse Kurye moto kuryesi"),
    giris="İstanbul'da bir gönderiyi hızlı taşımanın yolu, kısa güzergâh bulmaktan değil, trafikten en az "
          "etkilenen taşıma biçimini seçmekten geçiyor. Motor kurye tam da bunu yapar: yoğun saatlerde araçla "
          "40–50 dakika süren bir güzergâhı çoğu zaman yarı sürede tamamlar, park sorunu yaşamaz ve yaya "
          "bölgelerinin kapısına kadar gider.",
    bloklar=[
        ("metin", "Neden motor", "Motor kurye ne zaman gerçekten avantajlı?",
         ["Motorun kazandırdığı zaman, güzergâhın yoğunluğuyla doğru orantılı. Barbaros Bulvarı, Büyükdere Caddesi, "
          "E-5 ve köprü çıkışları gibi tıkanan koridorlarda fark saatlerle ölçülebilir hâle gelir. Buna karşılık "
          "boş bir güzergâhta motor ile aracın süresi birbirine yakındır.",
          "İkinci avantaj park. Kapalıçarşı, Beşiktaş Çarşı, İstiklal, Bakırköy Çarşı, Bağdat Caddesi gibi yerlerde "
          "aracın duracak yeri yoktur; motor kapıya kadar gider ve teslimi dakikalar içinde tamamlar.",
          "Üçüncüsü adres yapısı. Perpa, İSTOÇ ve İkitelli OSB gibi ada–blok düzenindeki dev iş merkezlerinde, "
          "ya da Moda, Cihangir, Kuzguncuk gibi dar ve tek yönlü sokaklarda motor ile araç arasındaki fark "
          "yalnızca hız değil, adrese ulaşabilme meselesidir."]),

        ("tablo", "Karşılaştırma", "Aynı güzergâh, iki farklı taşıma biçimi",
         "Hafta içi 17:00 – 19:00 arası, yoğun saat tahminleridir. Gece ve hafta sonu farkları ayrıca hesaplanır.",
         ["Güzergâh", "Motor kurye", "Araçlı taşıma"],
         [("Şişli → Beşiktaş", "20–35 dk", "35–60 dk"),
          ("Levent → Kadıköy", "45–75 dk", "70–110 dk"),
          ("Kağıthane → Perpa", "20–30 dk", "25–45 dk"),
          ("Bakırköy → Şişli", "40–70 dk", "60–100 dk"),
          ("Ataşehir → Ümraniye Şerifali", "25–40 dk", "35–60 dk")]),

        ("kartlar", "Taşınabilirlik", "Motorla ne taşınır, ne taşınmaz?",
         "Sınır ağırlıktan çok hacim ve kırılganlıkla ilgili. Emin değilseniz gönderiyi tarif etmeniz yeterli, doğru yöntemi birlikte seçelim.",
         [("TAŞINIR", "Evrak ve dosya", "Sözleşme, tapu, noter evrakı, ihale dosyası, fatura. Zarf ve dosyada ek ücret yoktur."),
          ("TAŞINIR", "Küçük ve orta paket", "Numune, yedek parça, elektronik, kozmetik, e-ticaret siparişi, ilaç."),
          ("SINIRLI", "Hacimli gönderi", "Çanta üstü hacimli gönderiler taşınır ancak ücret kademeli artar; çok büyük kolilerde araç öneririz."),
          ("TAŞINMAZ", "Yasaklı ve tehlikeli madde", "Yanıcı, parlayıcı, patlayıcı maddeler ve yasal olarak taşınması yasak gönderiler kabul edilmez.")]),

        ("liste", "Sık taşıdıklarımız", "Motor kuryeyle en çok taşıdığımız gönderiler",
         "İstanbul'da gün içinde en çok karşımıza çıkan işler bunlar.",
         ["Noter, tapu ve adliye evrakları",
          "İhale dosyaları ve imza bekleyen sözleşmeler",
          "Tekstil ve deri numuneleri, koleksiyon parçaları",
          "Reçeteli ilaç ve tahlil numuneleri",
          "Makine ve elektronik yedek parçaları",
          "E-ticaret siparişleri ve iade gönderileri",
          "Mağazalar arası ürün transferi",
          "Anahtar, kart ve unutulmuş kişisel eşya"]),
    ],
    sss=[("Moto kurye kaç kilograma kadar taşır?",
          "Motosikletle taşınan gönderiler genellikle 15 kilograma kadardır. Asıl belirleyici ağırlıktan çok hacimdir; "
          "çanta üstü hacimli gönderilerde ücret kademeli artar, çok büyük gönderilerde araçlı taşıma öneririz."),
         ("Moto kurye ile araçlı kurye arasında fiyat farkı var mı?",
          "Fiyatlandırmamız mesafe, hız ve paket boyutu üzerinden yapılır. Motorla taşınabilen bir gönderi için "
          "motor her zaman daha ekonomik ve çoğu güzergâhta daha hızlıdır."),
         ("Yağmurlu havada gönderim ıslanır mı?",
          "Kuryelerimiz su geçirmez kurye çantası kullanır; evrak ve elektronik gönderiler ayrıca korumaya alınır. "
          "Kırılgan gönderiyi baştan belirtmeniz yeterli."),
         ("Kırılgan gönderi motorla taşınabilir mi?",
          "Cam, çiçek gibi kırılgan gönderiler taşınabilir ancak paketlemenin uygun olması gerekir. "
          "Gönderiyi tarif ettiğinizde uygun taşıma biçimini birlikte belirliyoruz."),
         ("İstanbul'un tamamında moto kurye bulunuyor mu?",
          "Evet, 39 ilçenin tamamında motorlu teslimat yapıyoruz. Şile ve Silivri gibi uzak ilçelerde çıkış saatinin "
          "erken planlanması gerekir.")],
    ilgili=["acil-kurye", "7-24-kurye", "kurumsal-kurye"],
    bolge=["sisli", "besiktas", "kadikoy", "fatih", "perpa", "ikitelli"],
),

# =====================================================================
"7-24-kurye": dict(
    ad="7/24 Kurye",
    h1="7/24 Kurye",
    baslik="7/24 Kurye İstanbul | Gece ve Hafta Sonu Teslimat – Barse Kurye",
    aciklama="İstanbul'da 7/24 kurye: gece, hafta sonu ve resmi tatillerde de açık. Gece tarifesi, "
             "gece teslimatının kuralları ve süreler. 0534 761 83 88.",
    eyebrow="Gece · hafta sonu · resmi tatil",
    gorsel=("images/04-gece/gece-ofis-teslimat.webp",
            "Gece saatlerinde ofise teslimat yapan Barse Kurye kuryesi"),
    giris="Kurye ihtiyacı mesai saatiyle sınırlı değil. Gece devreye giren bir üretim hattı, sabaha yetişmesi "
          "gereken bir evrak, hafta sonu nöbetteki bir eczane ya da gece yarısı biten bir çekim — hepsi mesai "
          "dışında kurye ister. Barse Kurye'de gece ve hafta sonu ayrı bir hizmet değil, aynı operasyonun devamıdır.",
    bloklar=[
        ("metin", "Gece operasyonu", "Gece kurye nasıl çalışıyor?",
         ["Gece saatlerinde trafik açıldığı için teslim süreleri gündüze göre belirgin biçimde kısalır; "
          "gündüz 70 dakika süren bir yaka geçişi gece çoğu zaman 35–45 dakikada tamamlanır. Buna karşılık "
          "adres bulmak zorlaşır: kapalı iş yerleri, kilitli site girişleri ve boş resepsiyonlar gece teslimatın "
          "asıl sorunudur.",
          "Bu yüzden gece işlerinde teslim alacak kişinin telefonunu ve varsa güvenlik bilgisini baştan alıyoruz. "
          "Alıcıya ulaşılamayan durumlarda kurye gönderiyle birlikte bekler; ne yapılacağına siz karar verene "
          "kadar gönderi kuryede kalır, kapıya bırakılmaz."]),

        ("tablo", "Tarife", "Gece ve hafta sonu ücret farkı",
         "Farklar sabit tutardır, yüzde üzerinden artmaz. İki durum birlikteyse farklar toplanır.",
         ["Zaman dilimi", "Tarife farkı"],
         [("Hafta içi 06:00 – 20:00", "Fark yok"),
          ("Hafta içi 20:00 – 06:00", "+100 ₺"),
          ("Cumartesi ve Pazar (gündüz)", "+100 ₺"),
          ("Cumartesi ve Pazar (gece)", "+200 ₺")]),

        ("kartlar", "Kimler kullanıyor", "Gece ve hafta sonu en çok kimler kurye çağırıyor?",
         "Mesai dışı taleplerin büyük bölümü belirli sektörlerden geliyor.",
         [("SAĞLIK", "Nöbetçi eczane ve hastane", "Reçeteli ilaç, tahlil numunesi ve acil rapor teslimatı; gece en sık gelen taleptir."),
          ("ÜRETİM", "Vardiyalı fabrika", "Gece vardiyasında biten parça, kalıp ve numune gönderileri."),
          ("MEDYA", "Prodüksiyon ve ajans", "Çekim sonrası disk, ekipman ve baskı provası teslimleri."),
          ("OTEL", "Otel ve konaklama", "Misafire ulaştırılacak belge, unutulan eşya ve acil gönderiler.")]),

        ("liste", "Gece teslimatta", "Gece işlerinde dikkat ettiğimiz noktalar",
         "Gece teslimatın kuralları gündüzden farklı; bunları baştan konuşuyoruz.",
         ["Teslim alacak kişinin telefonu mutlaka alınır",
          "Site ve iş merkezi girişlerinde güvenlik prosedürü önceden sorulur",
          "Alıcıya ulaşılamazsa gönderi kapıya bırakılmaz, kurye bekler",
          "Gece tarifesi çıkıştan önce bildirilir, teslimden sonra sürpriz ücret çıkmaz",
          "Gece güzergâhları açık olduğu için süre tahminleri gündüze göre daha isabetlidir"]),
    ],
    sss=[("Gece kaça kadar kurye gönderiyorsunuz?",
          "Saat sınırı yok; operasyonumuz 7/24 açık. Gece 03:00'te de talep alıyor ve kurye yönlendiriyoruz."),
         ("Hafta sonu kurye ücreti ne kadar?",
          "Cumartesi ve Pazar günleri normal tarifeye +100 ₺ eklenir. Aynı gün gece saatlerindeyse gece farkı da "
          "eklenerek toplam +200 ₺ olur."),
         ("Resmi tatillerde çalışıyor musunuz?",
          "Evet, resmi tatillerde de kurye yönlendiriyoruz. Tatil günlerinde hafta sonu tarifesi geçerlidir."),
         ("Gece teslimat daha mı hızlı?",
          "Genellikle evet. Trafik açık olduğu için özellikle yaka geçişli güzergâhlarda süre gündüze göre "
          "belirgin biçimde kısalır."),
         ("Gece gönderi güvenli mi?",
          "Gönderi alımdan teslime kadar kuryenin sorumluluğundadır ve alıcıya ulaşılamadığında kapıya bırakılmaz. "
          "Teslim tamamlandığında bilgi veriyoruz.")],
    ilgili=["acil-kurye", "eczane-kurye", "moto-kurye"],
    bolge=["taksim-beyoglu", "levent", "kadikoy", "sisli", "besiktas", "umraniye"],
),

# =====================================================================
"eczane-kurye": dict(
    ad="Eczane Kurye",
    h1="Eczane Kurye",
    baslik="Eczane Kurye İstanbul | Reçeteli İlaç Teslimatı – Barse Kurye",
    aciklama="Eczane kurye hizmeti: reçeteli ilaç ve medikal ürün teslimatı, sabit 400 ₺ ücret, "
             "öncelikli yönlendirme, 7/24 açık. 0534 761 83 88.",
    eyebrow="Sabit 400 ₺ · öncelikli yönlendirme",
    gorsel=("images/06-hizmet/eczane-kurye-medikal.webp",
            "Eczaneden alınan reçeteli ilacı teslim eden Barse Kurye kuryesi"),
    giris="İlaç teslimatı, sıradan bir paket teslimatı değil. Alıcı çoğu zaman evden çıkamayacak durumda, "
          "gönderi zamana duyarlı ve teslimin doğru kişiye yapılması gerekiyor. Bu yüzden eczane gönderilerini "
          "ayrı bir akışta, öncelikli olarak yönlendiriyoruz ve ücreti mesafeden bağımsız sabit tutuyoruz.",
    bloklar=[
        ("metin", "Nasıl çalışıyor", "Eczaneler için nasıl bir düzen kuruyoruz?",
         ["Çalıştığımız eczaneler bizi arayıp hasta adresini iletiyor; kurye ilacı tezgâhtan teslim alıyor ve "
          "doğrudan hastaya götürüyor. Ara durak yok, başka teslimatla birleştirme yok. Teslim tamamlandığında "
          "eczaneye bilgi geçiyoruz.",
          "Yoğun çalışan eczaneler için gün içi düzenli çalışma da kuruyoruz: belirli saatlerde kurye eczaneye "
          "uğruyor, biriken teslimatları alıp güzergâh üzerinde dağıtıyor. Bu yöntem, tekil çağrılara göre "
          "belirgin biçimde daha ekonomik.",
          "Nöbetçi eczane çalışmalarında gece talebi de karşılıyoruz. Gece saatlerinde teslim alacak kişinin "
          "telefonu mutlaka alınır; hastaya ulaşılamadığında ilaç kapıya bırakılmaz."]),

        ("kartlar", "Ne taşıyoruz", "Eczane ve medikal gönderilerde en sık işlerimiz",
         "Sağlıkla ilgili gönderilerde önceliği her zaman zaman baskısı belirler.",
         [("REÇETELİ", "İlaç teslimatı", "Eczaneden hastanın adresine doğrudan teslim; en sık yaptığımız iştir."),
          ("NUMUNE", "Tahlil ve laboratuvar", "Laboratuvara ulaştırılması gereken numune ve sonuç raporları."),
          ("MEDİKAL", "Medikal ürün", "Cihaz, sarf malzemesi ve medikal ekipman teslimatı."),
          ("KURUM", "Hastane evrakı", "Hastane ve poliklinikler arasında rapor, dosya ve belge taşıma.")]),

        ("tablo", "Ücret", "Eczane kurye ücreti",
         "Eczane teslimatlarında ücret sabittir: mesafe, hız ve paket boyutu farkı uygulanmaz.",
         ["Hizmet", "Ücret", "Not"],
         [("Eczane kurye (reçeteli ilaç)", "400 ₺ sabit", "Mesafe farkı yok"),
          ("Standart teslimat", "380 ₺'den başlar", "Mesafeye göre artar"),
          ("Düzenli eczane çalışması", "Plana göre", "Gün içi sabit saatli, gönderi başına daha uygun")]),

        ("liste", "Dikkat ettiklerimiz", "İlaç teslimatında uyduğumuz kurallar",
         "Sağlık gönderilerinde küçük ayrıntılar sonucu değiştirir.",
         ["İlaç doğrudan hastaya veya belirtilen kişiye teslim edilir, kapıya bırakılmaz",
          "Teslim tamamlandığında eczaneye geri bilgi verilir",
          "Yaşlı ve hareket kısıtlı hastalarda kurye kapıya kadar çıkar",
          "Gönderi başka teslimatla birleştirilmez, öncelikli taşınır",
          "Gece ve hafta sonu dahil 7/24 talep alınır"]),
    ],
    sss=[("Eczane kurye ücreti ne kadar?",
          "Eczane teslimatları sabit 400 ₺'dir. Mesafe, teslimat hızı ve paket boyutu farkı uygulanmaz."),
         ("Reçeteli ilaç teslimatı yapıyor musunuz?",
          "Evet. İlacı eczaneden teslim alıp doğrudan hastanın adresine götürüyoruz. Teslim doğrudan hastaya "
          "veya eczanenin belirttiği kişiye yapılır."),
         ("Hastaya ulaşılamazsa ne oluyor?",
          "İlaç kapıya bırakılmaz. Kurye bekler, eczaneyi bilgilendirir ve ne yapılacağına dair talimatı bekler."),
         ("Eczanem için düzenli kurye planı kurabilir miyiz?",
          "Evet. Gün içi sabit saatlerde eczaneye uğrayıp biriken teslimatları dağıtan bir düzen kuruyoruz; "
          "bu yöntem tekil çağrılara göre daha ekonomik oluyor."),
         ("Gece nöbetinde de kurye bulabilir miyim?",
          "Evet, 7/24 çalışıyoruz. Nöbetçi eczane teslimatları gece de öncelikli olarak yönlendirilir.")],
    ilgili=["acil-kurye", "7-24-kurye", "kurumsal-kurye"],
    bolge=["kadikoy", "sisli", "uskudar", "bakirkoy", "gaziosmanpasa", "umraniye"],
),

# =====================================================================
"kurumsal-kurye": dict(
    ad="Kurumsal Kurye",
    h1="Kurumsal Kurye",
    baslik="Kurumsal Kurye ve Sözleşmeli Çalışma | Barse Kurye İstanbul",
    aciklama="Firmalar için kurumsal kurye: sabit saatli günlük plan, çok duraklı dağıtım, aylık toplu "
             "faturalandırma ve hacme göre indirimli tarife. 0534 761 83 88.",
    eyebrow="Sözleşmeli çalışma · aylık faturalandırma",
    gorsel=("images/07-musteri/kurumsal-musteri-kurye-cagiriyor.webp",
            "Kurumsal müşterisi için kurye planlayan Barse Kurye ekibi"),
    giris="Düzenli gönderisi olan bir firma için her seferinde arayıp fiyat sormak zaman kaybı. Kurumsal "
          "çalışmada işi tersine çeviriyoruz: gönderi hacminizi ve güzergâhlarınızı bir kez konuşuyoruz, "
          "sonrasında kurye planlı biçimde geliyor, faturalandırma ay sonunda tek seferde yapılıyor.",
    bloklar=[
        ("kartlar", "Çalışma biçimleri", "Firmalarla nasıl çalışıyoruz?",
         "Gönderi hacminize ve düzeninize göre üç farklı model kuruyoruz.",
         [("PLANLI", "Sabit saatli kurye", "Kurye her gün belirlediğiniz saatlerde ofisinize uğrar, biriken gönderileri alır."),
          ("DAĞITIM", "Çok duraklı güzergâh", "Tek kuryeyle birden fazla adrese dağıtım; güzergâh optimize edilir, gönderi başına maliyet düşer."),
          ("ÇAĞRI", "Talep üzerine", "Sabit plan yerine ihtiyaç oldukça çağırırsınız; sözleşmeli tarife yine geçerlidir."),
          ("KARMA", "Karma düzen", "Rutin gönderiler planlı, acil işler çağrı üzerine — en sık tercih edilen model budur.")]),

        ("metin", "Faturalandırma", "Ödeme ve faturalandırma nasıl işliyor?",
         ["Kurumsal müşterilerimizde her gönderi için ayrı ödeme almıyoruz. Ay boyunca yapılan teslimatlar "
          "kayıt altına alınıyor, ay sonunda tek fatura düzenleniyor. Fatura ekinde tarih, güzergâh ve tutar "
          "dökümü yer alıyor; muhasebe tarafında ek iş çıkarmıyor.",
          "Gönderi hacmi belirli bir seviyeyi geçen firmalarda indirimli tarife uyguluyoruz. Tarife, aylık "
          "gönderi adedi ve ağırlıklı güzergâhlarınıza göre belirleniyor — sabit bir liste yerine sizin "
          "trafiğinize göre hesaplanan bir yapı."]),

        ("liste", "Sektörler", "Düzenli çalıştığımız sektörler",
         "Her sektörün kurye ihtiyacı farklı; düzeni buna göre kuruyoruz.",
         ["Hukuk büroları — adliye dosyaları, tebligat ve noter evrakı",
          "Finans ve denetim — sözleşme, teminat mektubu ve rapor teslimi",
          "Tekstil ve konfeksiyon — atölye ile showroom arasında numune trafiği",
          "Sanayi ve imalat — yedek parça, kalıp ve kalite belgesi",
          "Eczane ve sağlık — reçeteli ilaç, numune ve rapor",
          "E-ticaret ve perakende — sipariş, iade ve mağazalar arası transfer",
          "Ajans ve matbaa — baskı provası, tasarım dosyası ve ekipman"]),

        ("tablo", "Örnek düzen", "Sabit saatli çalışmada tipik bir gün",
         "Aşağıdaki düzen bir hukuk bürosu için kurduğumuz plana benziyor; sizinki gönderi trafiğinize göre şekillenir.",
         ["Saat", "İş", "Not"],
         [("09:30", "Ofisten alım", "Gece biriken evrak ve dosyalar toplanır"),
          ("10:30", "Adliye teslimi", "Çağlayan veya Kartal adliyesine dosya teslimi"),
          ("14:00", "İkinci alım", "Öğleden sonra hazırlanan evraklar alınır"),
          ("16:30", "Dağıtım", "Güzergâh üzerindeki adreslere çok duraklı dağıtım"),
          ("Gün içi", "Acil çağrı", "Plan dışı acil işler için ayrı kurye yönlendirilir")]),
    ],
    sss=[("Kurumsal kurye anlaşması için minimum gönderi sayısı var mı?",
          "Katı bir alt sınır koymuyoruz. Düzenli gönderisi olan her firmayla sözleşmeli çalışabiliyoruz; "
          "indirimli tarife ise aylık hacme göre belirleniyor."),
         ("Fatura kesiyor musunuz?",
          "Evet. Kurumsal müşterilerimize fatura düzenliyoruz; aylık toplu faturalandırma ile her gönderi için "
          "ayrı ödeme yapmanız gerekmiyor."),
         ("Çok duraklı dağıtımda ücret nasıl hesaplanıyor?",
          "Tek tek gönderi ücreti yerine güzergâh üzerinden hesap yapıyoruz. Duraklar birbirine yakınsa "
          "gönderi başına maliyet belirgin biçimde düşer."),
         ("Sabit saatli kurye planı değiştirilebilir mi?",
          "Elbette. Plan sizin gönderi trafiğinize göre kurulur ve ihtiyaç değiştikçe güncellenir."),
         ("Sözleşmeli çalışmada acil işler ne oluyor?",
          "Planlı düzenin dışında kalan acil işler için ayrı kurye yönlendiriyoruz; sözleşmeli tarifeniz "
          "bu işlerde de geçerli olur.")],
    ilgili=["acil-kurye", "moto-kurye", "7-24-kurye"],
    bolge=["levent", "maslak", "atasehir-finans", "ikitelli", "perpa", "caglayan"],
),

}
