# -*- coding: utf-8 -*-
"""Bolge sayfalarinin editoryal verisi.

Her kayit tek bir HTML sayfasina karsilik gelir. Dosya adlari mevcut URL'lerle
birebir ayni tutulur; degistirilmemelidir.

Alanlar
-------
ad      : Sayfada gecen bolge adi
tip     : "ilce" | "bolge"  (bolge = ilce icindeki mikro bolge)
ilce    : tip="bolge" ise bagli oldugu ilce
yaka    : "Avrupa" | "Anadolu"
merkez  : (enlem, boylam) - rota ve sure hesabinda kullanilir
giris   : Sayfaya ozgu acilis paragrafi
odak    : Bolgede en cok tasidigimiz gonderi tipleri
nokta   : Sik teslimat yapilan somut noktalar
komsu   : Ic linki verilecek komsu bolge dosya adlari (uzantisiz)
sss     : Bolgeye ozgu soru-cevap ciftleri
"""

BOLGELER = {

# =====================================================================
#  ANADOLU YAKASI - ILCELER
# =====================================================================

"kadikoy": dict(
    ad="Kadıköy", tip="ilce", yaka="Anadolu", merkez=(40.990, 29.028),
    giris="Kadıköy, Anadolu yakasının en yoğun evrak ve numune trafiğini taşıyan ilçesi. "
          "Bahariye ve Söğütlüçeşme çevresindeki ofisler, Moda'daki ajanslar, Bağdat Caddesi mağazaları "
          "ve Kozyatağı plazaları gün içinde birbirinden çok farklı hızlarda gönderi üretiyor. "
          "Kadıköy'de sürekli devrede kuryemiz olduğu için talebi aldığımız anda en yakın motor bölgeye yönleniyor.",
    odak=["Ajans ve ofis evrakları", "Bağdat Caddesi mağaza gönderileri", "Numune ve laboratuvar teslimatları"],
    nokta=["Kadıköy İskelesi ve Bahariye Caddesi", "Söğütlüçeşme ofisleri", "Moda ve Caferağa",
           "Bağdat Caddesi mağazaları", "Kozyatağı plazaları", "Acıbadem ve Fikirtepe hastane çevresi"],
    komsu=["uskudar", "atasehir", "maltepe", "kadikoy-moda", "bagdat-caddesi", "kozyatagi"],
    sss=[("Kadıköy'den Avrupa yakasına kurye ne kadar sürer?",
          "Köprü ve trafik durumuna göre Kadıköy'den Şişli, Beşiktaş ve Levent hattına ortalama 55–80 dakikada "
          "teslimat yapıyoruz. Acil işlerde VIP kurye seçeneğiyle motor başka hiçbir adrese uğramadan doğrudan gider."),
         ("Bağdat Caddesi'ndeki mağazama gün içinde birden fazla kurye gönderebilir misiniz?",
          "Evet. Bağdat Caddesi ve Suadiye hattındaki mağazalar için gün içi düzenli kurye planlıyoruz; "
          "sabah ve akşamüstü olmak üzere sabit saatli çalışma da kurabiliriz.")],
),

"uskudar": dict(
    ad="Üsküdar", tip="ilce", yaka="Anadolu", merkez=(41.023, 29.015),
    giris="Üsküdar, sahil hattındaki resmi kurumlar ile Altunizade'deki iş merkezleri ve hastaneler arasında "
          "gün boyu evrak trafiği olan bir ilçe. Boğaz köyleri tarafında ise Kuzguncuk'tan Kandilli'ye kadar "
          "dar sokaklı bir yerleşim var; buralarda motor kurye, araçlı taşımaya göre belirgin şekilde daha hızlı.",
    odak=["Resmi kurum ve noter evrakları", "Altunizade ofis gönderileri", "Hastane ve tahlil numuneleri"],
    nokta=["Üsküdar Meydanı ve Marmaray çıkışı", "Altunizade iş merkezleri", "Acıbadem Hastanesi çevresi",
           "Kuzguncuk, Beylerbeyi, Çengelköy sahili", "Bulgurlu ve Kısıklı", "Ünalan metro çevresi"],
    komsu=["kadikoy", "umraniye", "beykoz", "atasehir"],
    sss=[("Üsküdar'daki noterden evrak alıp aynı gün teslim edebilir misiniz?",
          "Evet. Üsküdar Meydanı çevresindeki noterlerden evrak alımı yapıp aynı gün içinde İstanbul'un "
          "herhangi bir ilçesine teslim ediyoruz. Al-ver işlerde kurye işlem bitene kadar bekler."),
         ("Boğaz köylerine motor kurye giriyor mu?",
          "Kuzguncuk, Beylerbeyi, Çengelköy ve Kandilli dahil tüm sahil yerleşimlerine giriyoruz. "
          "Dar sokak ve yokuş yapısı nedeniyle bu bölgede motor kurye en pratik çözüm.")],
),

"atasehir": dict(
    ad="Ataşehir", tip="ilce", yaka="Anadolu", merkez=(40.984, 29.107),
    giris="Ataşehir, Finans Merkezi ve çevresindeki plazalarla birlikte Anadolu yakasının kurumsal evrak "
          "merkezine dönüştü. Banka genel müdürlükleri, denetim şirketleri ve hukuk büroları burada; "
          "imzalı sözleşme ve teminat evrakı trafiği gün içinde kesintisiz sürüyor.",
    odak=["Banka ve finans evrakları", "Sözleşme ve imza sirküleri", "Plaza içi ofisler arası taşımalar"],
    nokta=["Ataşehir Finans Merkezi", "Palladium ve Watergarden", "Brandium ve Metropol İstanbul",
           "Barbaros Mahallesi plazaları", "Küçükbakkalköy iş merkezleri", "İçerenköy sanayi çevresi"],
    komsu=["kadikoy", "umraniye", "maltepe", "atasehir-finans", "kozyatagi"],
    sss=[("Finans Merkezi'ndeki plazalara kurye girişi nasıl oluyor?",
          "Kuryelerimiz plaza giriş prosedürlerine alışkın; kimlik bırakma ve ziyaretçi kaydı gereken binalarda "
          "süreç zaten hesaba katılıyor. Kat ve blok bilgisini paylaşmanız teslim süresini kısaltır."),
         ("Ataşehir'den şehir dışına gönderi çıkarabilir miyiz?",
          "Evet. Ataşehir'den aldığımız gönderiyi aynı gün havayolu kargoya veya şehirler arası hatta teslim "
          "ederek Türkiye geneline ulaştırıyoruz.")],
),

"umraniye": dict(
    ad="Ümraniye", tip="ilce", yaka="Anadolu", merkez=(41.016, 29.121),
    giris="Ümraniye, Şerifali ve Dudullu hattındaki iş merkezleriyle Anadolu yakasının en yüksek B2B kurye "
          "hacmine sahip ilçelerinden biri. Sanayi sitelerinden çıkan yedek parça ve numune gönderileri ile "
          "Meydan çevresindeki ofis evrakları aynı gün içinde farklı hızlarda taşınıyor.",
    odak=["Sanayi ve yedek parça gönderileri", "Şerifali ofis evrakları", "Numune ve prototip taşıma"],
    nokta=["Şerifali iş merkezleri", "Dudullu OSB ve İMES", "Ümraniye Meydan ve Meydan İstanbul AVM",
           "Yukarı Dudullu sanayi siteleri", "Ümraniye Eğitim ve Araştırma Hastanesi", "Çakmak ve Atakent"],
    komsu=["uskudar", "atasehir", "cekmekoy", "sancaktepe", "umraniye-merkez"],
    sss=[("Dudullu OSB'den düzenli kurye hizmeti alabilir miyiz?",
          "Evet. Dudullu ve İMES bölgesindeki firmalar için gün içi sabit saatli kurye planı kuruyoruz; "
          "böylece her gönderi için ayrı ayrı arama yapmanız gerekmiyor."),
         ("Şerifali'den Avrupa yakasına acil evrak nasıl gider?",
          "Şerifali'den Levent, Maslak ve Şişli hattına VIP kurye ile doğrudan çıkış yapıyoruz; "
          "kurye yol boyunca başka adrese uğramaz.")],
),

"maltepe": dict(
    ad="Maltepe", tip="ilce", yaka="Anadolu", merkez=(40.936, 29.131),
    giris="Maltepe, sahil hattındaki yeni yerleşimler ile Bağlarbaşı ve Cevizli'deki eski ticaret dokusunu "
          "birlikte barındırıyor. Küçükyalı iş merkezleri ile üniversite ve hastane çevresi, gün içinde "
          "birbirine yakın ama farklı önceliklerde gönderi üretiyor.",
    odak=["Ofis ve iş merkezi evrakları", "Hastane ve laboratuvar gönderileri", "E-ticaret paket teslimatları"],
    nokta=["Maltepe Sahil ve Piazza AVM", "Küçükyalı iş merkezleri", "Bağlarbaşı ve Cevizli çarşı",
           "Maltepe Üniversitesi ve hastanesi", "Zümrütevler ve Altayçeşme", "İdealtepe Marmaray çevresi"],
    komsu=["kadikoy", "kartal", "atasehir", "bagdat-caddesi"],
    sss=[("Maltepe'den Kadıköy'e evrak kaç dakikada gider?",
          "Sahil yolu üzerinden ortalama 25–40 dakika. Trafiğin yoğun olduğu akşam saatlerinde express veya "
          "VIP kurye seçmenizi öneririz."),
         ("Sahil hattındaki sitelere teslimat yapıyor musunuz?",
          "Evet. Site içi teslimatlarda kurye güvenliğe kaydını yaptırıp kapıya kadar çıkar; "
          "site kuralı gereği paketin güvenlikte bırakılması gerekiyorsa sizi bilgilendiririz.")],
),

"kartal": dict(
    ad="Kartal", tip="ilce", yaka="Anadolu", merkez=(40.888, 29.190),
    giris="Kartal, Anadolu Adalet Sarayı sayesinde yoğun bir dava dosyası ve tebligat trafiğine sahip. "
          "Buna Soğanlık ve Yakacık'taki sanayi dokusu ile sahil hattındaki yeni konut projeleri ekleniyor; "
          "sonuçta hem hukuki evrak hem de ticari paket taşımacılığı bir arada yürüyor.",
    odak=["Adliye evrakı ve dava dosyaları", "Sanayi ve imalat gönderileri", "Hastane ve eczane teslimatları"],
    nokta=["Anadolu Adalet Sarayı", "Kartal Meydan ve Kordonboyu", "Soğanlık sanayi bölgesi",
           "Yakacık ve Atalar", "Dr. Lütfi Kırdar Şehir Hastanesi", "Dragos sahil hattı"],
    komsu=["maltepe", "pendik", "sancaktepe", "kartal-merkez"],
    sss=[("Anadolu Adalet Sarayı'na evrak teslimi yapıyor musunuz?",
          "Evet. Kartal'daki Anadolu Adalet Sarayı'na dosya ve dilekçe teslimi bizim en sık yaptığımız işlerden. "
          "Kurye teslim sonrası fotoğrafla bilgi verir."),
         ("Kartal'dan Sabiha Gökçen'e kaç dakikada ulaşırsınız?",
          "Trafiğe göre ortalama 25–40 dakika. Uçak kargo saatine yetiştirilmesi gereken gönderilerde "
          "çıkış saatini birlikte planlıyoruz.")],
),

"pendik": dict(
    ad="Pendik", tip="ilce", yaka="Anadolu", merkez=(40.877, 29.234),
    giris="Pendik, Sabiha Gökçen Havalimanı'na ev sahipliği yaptığı için kurye açısından İstanbul'un en "
          "kritik ilçelerinden biri. Uçak kargoya yetiştirilmesi gereken gönderiler, Kurtköy'deki teknoloji "
          "firmaları ve tersane bölgesindeki sanayi trafiği burada iç içe geçiyor.",
    odak=["Havalimanı ve uçak kargo gönderileri", "Kurtköy ofis ve teknoloji firmaları", "Tersane ve sanayi evrakları"],
    nokta=["Sabiha Gökçen Havalimanı", "Kurtköy ve Teknopark", "Pendik Marina ve sahil",
           "Viaport ve Yenişehir", "Pendik Devlet Hastanesi", "Esenyalı ve Kaynarca"],
    komsu=["kartal", "tuzla", "sultanbeyli", "sancaktepe"],
    sss=[("Sabiha Gökçen'e uçak kargo gönderisi yetiştirebilir misiniz?",
          "Evet. Uçuş ve kargo kabul saatini bize söylediğinizde geri sayımı ona göre planlıyoruz; "
          "kritik saatlerde VIP kurye ile doğrudan çıkış yapıyoruz."),
         ("Kurtköy'den Kadıköy'e günlük evrak taşınabilir mi?",
          "Evet. Kurtköy–Kadıköy hattı için sabit saatli günlük kurye planı kuruyoruz; kurumsal müşterilerimizde "
          "en sık tercih edilen düzenlerden biri.")],
),

"tuzla": dict(
    ad="Tuzla", tip="ilce", yaka="Anadolu", merkez=(40.816, 29.301),
    giris="Tuzla, tersaneler ve organize sanayi bölgeleriyle İstanbul'un ağır sanayi ucu. Burada kurye işi "
          "çoğunlukla gümrük evrakı, iş makinesi parçası ve kalite belgesi taşımak anlamına geliyor; "
          "mesafeler uzun olduğu için çıkış saatinin doğru planlanması teslim süresini belirliyor.",
    odak=["Tersane ve gemi evrakları", "OSB firmalarının numune gönderileri", "Gümrük ve ihracat belgeleri"],
    nokta=["Tuzla Tersaneler Bölgesi", "Anadolu Yakası OSB", "Orhanlı ve Tepeören lojistik depoları",
           "Akfırat ve Formula çevresi", "Tuzla Marina", "İçmeler ve Aydınlı"],
    komsu=["pendik", "sultanbeyli", "kartal"],
    sss=[("Tuzla tersanelerine kurye girişi nasıl yapılıyor?",
          "Tersane girişlerinde kayıt ve güvenlik prosedürü var; kurye bunu bilerek gidiyor. "
          "İlgili kişinin adı ve telefonu paylaşıldığında teslim çok daha hızlı tamamlanıyor."),
         ("Tuzla'dan Avrupa yakasına gönderi mantıklı mı?",
          "Mesafe uzun ama düzenli yaptığımız bir hat. Aynı gün teslim için sabah saatlerinde çıkış yapmanızı, "
          "acil işlerde ise VIP kurye seçmenizi öneririz.")],
),

"sancaktepe": dict(
    ad="Sancaktepe", tip="ilce", yaka="Anadolu", merkez=(41.001, 29.231),
    giris="Sancaktepe, Sarıgazi ve Samandıra hattındaki hızlı yapılaşmayla birlikte hem konut hem küçük "
          "sanayi gönderisi üreten bir ilçe. TEM bağlantısı sayesinde Ümraniye ve Çekmeköy tarafına geçişler "
          "kısa; ilçe içi teslimatlarda motor kurye açık ara en hızlı seçenek.",
    odak=["Küçük imalat ve atölye gönderileri", "Konut bölgesi paket teslimatları", "Eczane ve ilaç taşıma"],
    nokta=["Sarıgazi merkez", "Samandıra ve Abdurrahmangazi", "Yenidoğan", "Şehit Prof. Dr. İlhan Varank Hastanesi",
           "Paşaköy ve Akpınar", "TEM bağlantı yolu çevresi"],
    komsu=["umraniye", "cekmekoy", "sultanbeyli", "kartal"],
    sss=[("Sancaktepe'de aynı gün teslimat mümkün mü?",
          "Evet. İlçe içi teslimatları çoğunlukla 30–60 dakika bandında tamamlıyoruz; "
          "İstanbul'un diğer ilçelerine aynı gün çıkış her zaman mümkün."),
         ("Samandıra'daki atölyelerden düzenli parça taşıyabilir misiniz?",
          "Evet. Sabit güzergâhlı günlük taşımalarda gönderi başına değil, plan üzerinden çalışıyoruz; "
          "bu da toplam maliyeti düşürüyor.")],
),

"cekmekoy": dict(
    ad="Çekmeköy", tip="ilce", yaka="Anadolu", merkez=(41.038, 29.184),
    giris="Çekmeköy, Taşdelen ve Alemdağ çevresindeki yerleşim ile Nişantepe tarafındaki villa bölgelerini "
          "kapsıyor. Adresler birbirinden uzak ve sokak yapısı dağınık olduğu için, doğru mahalle bilgisi "
          "teslim süresini doğrudan etkiliyor.",
    odak=["Villa ve site teslimatları", "Eczane ve ilaç gönderileri", "Ofis evrakı ve fatura taşıma"],
    nokta=["Taşdelen merkez", "Alemdağ", "Çekmeköy metro çevresi", "Nişantepe villa bölgesi",
           "Ömerli", "Mimar Sinan ve Çamlık"],
    komsu=["umraniye", "sancaktepe", "beykoz", "uskudar"],
    sss=[("Nişantepe'deki sitelere teslimat yapıyor musunuz?",
          "Evet. Villa ve site bölgelerine giriyoruz. Site adı, blok ve kapı bilgisini paylaşmanız "
          "kuryenin adresi ilk seferde bulmasını sağlıyor."),
         ("Çekmeköy'den Kadıköy'e gönderi ne kadar sürer?",
          "Ortalama 40–65 dakika. Sabah ve akşam zirve saatlerinde express veya VIP kurye seçmek "
          "süreyi belirgin şekilde kısaltıyor.")],
),

"sultanbeyli": dict(
    ad="Sultanbeyli", tip="ilce", yaka="Anadolu", merkez=(40.960, 29.267),
    giris="Sultanbeyli, E-5 hattına yakınlığı sayesinde Anadolu yakasının doğu ucundaki en pratik kurye "
          "duraklarından biri. İlçe içi mesafeler kısa; buna karşılık merkeze doğru çıkışlarda güzergâh "
          "planı toplam süreyi belirliyor.",
    odak=["Ticari evrak ve fatura", "Küçük sanayi gönderileri", "Eczane ve market teslimatları"],
    nokta=["Sultanbeyli Belediye çevresi", "Abdurrahmangazi ve Fatih", "Mehmet Akif",
           "Sultanbeyli Devlet Hastanesi", "Sanayi sitesi", "E-5 bağlantı yolu"],
    komsu=["sancaktepe", "pendik", "tuzla"],
    sss=[("Sultanbeyli'den merkeze aynı gün gönderi çıkar mı?",
          "Evet. Sabah saatlerinde alınan gönderileri aynı gün içinde Kadıköy, Ataşehir ve Avrupa yakası "
          "hattına ulaştırıyoruz."),
         ("İlçe içi teslimat ücreti nasıl hesaplanıyor?",
          "İlk 5 kilometreye kadar taban ücret geçerli; ilçe içi işlerin büyük bölümü bu bandın içinde kalıyor.")],
),

"beykoz": dict(
    ad="Beykoz", tip="ilce", yaka="Anadolu", merkez=(41.125, 29.100),
    giris="Beykoz, Kavacık'taki plaza yoğunluğu ile Boğaz kıyısındaki yerleşimleri aynı ilçede birleştiriyor. "
          "Kavacık ve Rüzgarlıbahçe hattı gün içinde kurumsal evrak üretirken, Paşabahçe ve Anadolu Kavağı "
          "tarafında mesafeler uzuyor ve planlama önem kazanıyor.",
    odak=["Kavacık plaza evrakları", "Boğaz hattı ev ve villa teslimatları", "Kurumsal sözleşme taşıma"],
    nokta=["Kavacık ve Rüzgarlıbahçe plazaları", "Acarkent", "Çubuklu ve Kanlıca",
           "Paşabahçe ve Beykoz merkez", "Anadolu Hisarı", "Riva"],
    komsu=["uskudar", "umraniye", "cekmekoy", "sariyer"],
    sss=[("Kavacık'tan Maslak'a köprüden kurye ne kadar sürer?",
          "FSM köprüsü üzerinden ortalama 30–50 dakika. Köprü trafiğinin kilitlendiği saatlerde motor kurye "
          "araca göre belirgin avantaj sağlıyor."),
         ("Riva ve Anadolu Kavağı'na teslimat yapıyor musunuz?",
          "Evet, ilçenin tamamına çıkıyoruz. Bu uzak noktalarda mesafe ücrete yansıdığı için önceden "
          "net fiyat vermemizi isteyebilirsiniz.")],
),

"adalar": dict(
    ad="Adalar", tip="ilce", yaka="Anadolu", merkez=(40.876, 29.093),
    giris="Adalar'a teslimat, İstanbul'un başka hiçbir ilçesine benzemiyor: gönderi Bostancı veya Kabataş "
          "iskelesinden vapurla gidiyor, adada motorlu araç kısıtı olduğu için son teslim yürüyerek ya da "
          "elektrikli araçla tamamlanıyor. Bu yüzden Adalar gönderilerinde vapur saati planın merkezinde.",
    odak=["Ada işletmelerinin evrak ve fatura gönderileri", "Otel ve pansiyon teslimatları", "Kişisel acil gönderiler"],
    nokta=["Büyükada", "Heybeliada", "Burgazada", "Kınalıada", "Bostancı İskelesi çıkışı", "Kabataş İskelesi çıkışı"],
    komsu=["kartal", "maltepe", "kadikoy"],
    sss=[("Adalar'a teslimat ne kadar sürer?",
          "Süre tamamen vapur saatine bağlı. Gönderiyi bir sonraki sefere yetiştirecek şekilde planlıyor, "
          "tahmini teslim saatini baştan söylüyoruz."),
         ("Adalar'a hafta sonu gönderi yapılabiliyor mu?",
          "Evet, sefer saatleri uygun olduğu sürece hafta sonu da teslimat yapıyoruz. "
          "Hafta sonu tarifesi ücrete yansır.")],
),

"sile": dict(
    ad="Şile", tip="ilce", yaka="Anadolu", merkez=(41.176, 29.613),
    giris="Şile, İstanbul'un Karadeniz kıyısındaki en uzak ilçesi. Şehir merkezinden çıkış uzun sürdüğü için "
          "buradaki işleri gün içine yayılmış tekil teslimatlar yerine planlı çıkışlarla yürütüyoruz. "
          "Ağva tarafına giden gönderilerde mesafe daha da artıyor.",
    odak=["Otel ve işletme evrakları", "Yazlık konut teslimatları", "Acil ilaç ve belge taşıma"],
    nokta=["Şile merkez", "Ağva", "Kumbaba sahili", "Çayırbaşı", "Şile Otoyolu bağlantısı", "Doğancılı"],
    komsu=["cekmekoy", "beykoz", "sancaktepe"],
    sss=[("Şile'ye aynı gün teslimat yapılıyor mu?",
          "Evet, ancak çıkış saatinin erken olması gerekiyor. Sabah verilen gönderiler aynı gün Şile ve "
          "Ağva'ya ulaşır."),
         ("Şile teslimatı neden diğer ilçelerden pahalı?",
          "Ücret mesafeye bağlı hesaplandığı için merkeze uzaklık fiyata yansıyor. Net rakamı çıkış öncesi "
          "paylaşıyoruz, sürpriz ücret olmuyor.")],
),

# =====================================================================
#  AVRUPA YAKASI - ILCELER
# =====================================================================

"sisli": dict(
    ad="Şişli", tip="ilce", yaka="Avrupa", merkez=(41.060, 28.987),
    giris="Şişli, İstanbul'da kurye trafiğinin en yoğun olduğu ilçe. Mecidiyeköy ve Esentepe'deki plazalar, "
          "Nişantaşı'ndaki showroomlar, Osmanbey'deki tekstil firmaları ve Perpa'daki binlerce ofis "
          "aynı anda gönderi üretiyor. Bölgede kalıcı kurye bulundurduğumuz için alım süresi çok kısa.",
    odak=["Plaza ve ofis evrakları", "Tekstil numunesi ve koleksiyon taşıma", "Showroom ve mağaza gönderileri"],
    nokta=["Mecidiyeköy ve Trump Towers", "Esentepe ve Gülbahar plazaları", "Nişantaşı ve Teşvikiye",
           "Osmanbey tekstil ofisleri", "Perpa Ticaret Merkezi", "Bomonti ve Fulya"],
    komsu=["besiktas", "beyoglu", "kagithane", "sisli-merkez", "mecidiyekoy", "nisantasi", "perpa"],
    sss=[("Perpa'dan gün içinde kaç kez kurye alabilirim?",
          "Sınır yok. Perpa'da sürekli iş olduğu için gün içinde ihtiyaç duydukça kurye yönlendiriyoruz; "
          "yoğun çalışan firmalar için sabit saatli plan da kuruyoruz."),
         ("Osmanbey'den numune gönderisi nasıl taşınıyor?",
          "Askılı ürün ve koleksiyon çantaları için uygun ekipmanlı kurye yönlendiriyoruz. "
          "Hacimli gönderilerde paket boyutu ücrete yansır, bunu baştan söylüyoruz.")],
),

"besiktas": dict(
    ad="Beşiktaş", tip="ilce", yaka="Avrupa", merkez=(41.043, 29.008),
    giris="Beşiktaş, Levent'teki genel müdürlüklerden Çarşı'daki küçük işletmelere kadar çok katmanlı bir "
          "kurye talebi üretiyor. Barbaros Bulvarı hattı gün boyu yoğun; buna karşılık motor kurye bu "
          "koridorda trafikten en az etkilenen taşıma biçimi.",
    odak=["Genel müdürlük ve banka evrakları", "Restoran ve işletme gönderileri", "Boğaz hattı ev teslimatları"],
    nokta=["Levent plazaları ve Kanyon", "Zorlu Center ve Zincirlikuyu", "Barbaros Bulvarı",
           "Beşiktaş Çarşı ve iskele", "Ortaköy, Kuruçeşme, Bebek", "Etiler ve Akatlar"],
    komsu=["sisli", "sariyer", "kagithane", "levent", "besiktas-carsi", "zincirlikuyu"],
    sss=[("Levent'teki plazalara kaç dakikada kurye gelir?",
          "Beşiktaş ve çevresinde sürekli kuryemiz olduğu için alım genellikle 15–25 dakika içinde yapılır."),
         ("Bebek ve Ortaköy'e akşam saatlerinde teslimat yapıyor musunuz?",
          "Evet, 7/24 çalışıyoruz. 20:00 sonrası gece tarifesi uygulanır; ücreti önceden bildiririz.")],
),

"beyoglu": dict(
    ad="Beyoğlu", tip="ilce", yaka="Avrupa", merkez=(41.033, 28.977),
    giris="Beyoğlu, dar sokakları ve yaya bölgeleriyle araçlı teslimatın en zorlandığı ilçelerden biri. "
          "İstiklal çevresindeki işletmeler, Karaköy'deki ajanslar ve Cihangir'deki ofisler için motor kurye "
          "çoğu zaman tek pratik çözüm.",
    odak=["Ajans ve prodüksiyon gönderileri", "Kafe, restoran ve otel teslimatları", "Galeri ve mağaza taşımaları"],
    nokta=["İstiklal Caddesi ve Taksim", "Karaköy ve Galata", "Cihangir ve Firuzağa",
           "Asmalımescit", "Tarlabaşı Bulvarı", "Kasımpaşa ve Halıcıoğlu"],
    komsu=["sisli", "besiktas", "fatih", "kagithane", "taksim-beyoglu"],
    sss=[("İstiklal Caddesi'ne kurye girebiliyor mu?",
          "Yaya bölgesinde motor giriş kısıtı var; kurye en yakın noktaya kadar gelip teslimatı yürüyerek "
          "tamamlıyor. Bu, sürede birkaç dakikalık fark yaratır."),
         ("Karaköy'den Kadıköy'e gönderi ne kadar sürer?",
          "Ortalama 40–60 dakika. Vapur değil kara yolu üzerinden gidilir; acil işlerde VIP kurye önerilir.")],
),

"kagithane": dict(
    ad="Kağıthane", tip="ilce", yaka="Avrupa", merkez=(41.081, 28.972),
    giris="Kağıthane bizim merkez üssümüz: operasyon ofisimiz Talatpaşa Mahallesi'nde. Cendere Vadisi "
          "boyunca sıralanan ofis kuleleri, Çağlayan'daki adliye ve Seyrantepe'deki iş merkezleri sayesinde "
          "ilçe hem en hızlı hizmet verdiğimiz hem de en çok iş çıkardığımız bölge.",
    odak=["Adliye evrakı ve dosya teslimi", "Ofis kuleleri arası evrak", "Ajans ve matbaa gönderileri"],
    nokta=["İstanbul Adliyesi (Çağlayan)", "Cendere Vadisi ofis kuleleri", "Vadistanbul",
           "Seyrantepe ve Skyland", "Talatpaşa ve Merkez Mahallesi", "Gültepe ve Çeliktepe"],
    komsu=["sisli", "besiktas", "eyupsultan", "sariyer", "caglayan", "seyrantepe"],
    sss=[("Kağıthane'de kurye ne kadar sürede geliyor?",
          "Operasyon merkezimiz Kağıthane'de olduğu için alım çoğu zaman 10–20 dakika içinde yapılıyor."),
         ("Çağlayan Adliyesi'ne dosya teslimi yapıyor musunuz?",
          "Evet, en sık yaptığımız işlerden biri. Duruşma saatine yetişmesi gereken dosyalarda "
          "geri sayımı birlikte planlıyoruz.")],
),

"fatih": dict(
    ad="Fatih", tip="ilce", yaka="Avrupa", merkez=(41.016, 28.940),
    giris="Fatih, İstanbul'un toptan ticaret kalbi. Kapalıçarşı, Mahmutpaşa ve Tahtakale'deki iş hanları "
          "gün boyu küçük hacimli ama çok sayıda gönderi üretiyor. Bu sokaklarda araçla ilerlemek neredeyse "
          "imkânsız olduğu için motor kurye burada standart çözüm.",
    odak=["Toptancı ve iş hanı gönderileri", "Kuyum ve değerli küçük paketler", "Hastane ve üniversite evrakları"],
    nokta=["Kapalıçarşı ve Mahmutpaşa", "Tahtakale ve Eminönü", "Laleli tekstil hanları",
           "Çapa Tıp Fakültesi", "Cerrahpaşa Hastanesi", "Sirkeci ve Sultanahmet"],
    komsu=["beyoglu", "zeytinburnu", "bayrampasa", "eyupsultan", "topkapi"],
    sss=[("Kapalıçarşı içindeki dükkâna kurye geliyor mu?",
          "Evet. Kurye en yakın kapıya kadar motorla gelir, çarşı içindeki teslimi yürüyerek tamamlar. "
          "Kapı adını ve dükkân numarasını paylaşmanız süreyi kısaltır."),
         ("Değerli küçük gönderiler için özel bir hizmetiniz var mı?",
          "VIP kurye seçeneğinde gönderi tek başına taşınır, kurye başka adrese uğramaz ve teslim "
          "doğrudan alıcıya yapılır.")],
),

"zeytinburnu": dict(
    ad="Zeytinburnu", tip="ilce", yaka="Avrupa", merkez=(40.994, 28.902),
    giris="Zeytinburnu, deri ve tekstil imalatının yoğunlaştığı bir üretim ilçesi. Kazlıçeşme ve Merkezefendi "
          "çevresindeki atölyeler numune ve model gönderisi üretirken, Marmaray ve sahil hattı bu gönderilerin "
          "şehrin geri kalanına dağıldığı çıkış noktası.",
    odak=["Tekstil ve deri numuneleri", "Atölye–showroom taşımaları", "E-ticaret paket gönderileri"],
    nokta=["Kazlıçeşme", "Merkezefendi ve Telsiz", "Zeytinburnu Marmaray çevresi",
           "Olivium ve çevresi", "Veliefendi", "Seyitnizam sanayi"],
    komsu=["fatih", "bakirkoy", "bahcelievler", "gungoren", "topkapi"],
    sss=[("Atölyeden showroom'a günlük numune taşıyabilir misiniz?",
          "Evet. Zeytinburnu–Osmanbey ve Zeytinburnu–Nişantaşı hatlarında günlük düzenli numune taşıyoruz."),
         ("Hacimli tekstil gönderileri motorla taşınır mı?",
          "Belirli bir boyuta kadar taşınır. Çanta üstü hacimlerde ücret kademeli artar; "
          "çok büyük gönderilerde uygun aracı yönlendiririz.")],
),

"bakirkoy": dict(
    ad="Bakırköy", tip="ilce", yaka="Avrupa", merkez=(40.980, 28.872),
    giris="Bakırköy, Ataköy ve Yeşilköy hattındaki yerleşimlerle çarşı bölgesindeki yoğun ticareti birlikte "
          "barındırıyor. Atatürk Havalimanı çevresi ve fuar alanı, ilçeyi aynı zamanda kurumsal gönderiler "
          "için önemli bir düğüm noktası yapıyor.",
    odak=["Havalimanı çevresi kurumsal gönderiler", "Çarşı ve AVM mağaza teslimatları", "Hastane ve poliklinik evrakları"],
    nokta=["Bakırköy Çarşı ve İncirli", "Ataköy ve Galleria", "Yeşilköy ve Florya",
           "Atatürk Havalimanı çevresi", "Capacity AVM", "Bakırköy sahil hattı"],
    komsu=["bahcelievler", "zeytinburnu", "kucukcekmece", "bakirkoy-merkez"],
    sss=[("Yeşilköy'deki firmalara sabah erken kurye gelir mi?",
          "Evet. 7/24 çalıştığımız için sabah 06:00 öncesi de dahil olmak üzere her saatte alım yapabiliyoruz."),
         ("Bakırköy'den Anadolu yakasına aynı gün teslim olur mu?",
          "Olur. Sabah ve öğle saatlerinde çıkan gönderiler aynı gün Kadıköy, Ataşehir ve Ümraniye hattına ulaşır.")],
),

"bahcelievler": dict(
    ad="Bahçelievler", tip="ilce", yaka="Avrupa", merkez=(41.000, 28.859),
    giris="Bahçelievler, Yenibosna ve Basın Ekspres hattı sayesinde plaza ve lojistik firmalarının "
          "yoğunlaştığı bir ilçe. Şirinevler çevresindeki ticari yoğunluk ile Basın Ekspres'teki kurumsal "
          "ofisler birbirinden farklı iki kurye trafiği oluşturuyor.",
    odak=["Basın Ekspres plaza evrakları", "Lojistik firması belgeleri", "Mağaza ve ticari gönderiler"],
    nokta=["Yenibosna ve Basın Ekspres", "Şirinevler metro çevresi", "Metroport ve çevresi",
           "Kocasinan ve Soğanlı", "Siyavuşpaşa", "Çobançeşme"],
    komsu=["bakirkoy", "gungoren", "bagcilar", "kucukcekmece", "zeytinburnu"],
    sss=[("Basın Ekspres'teki ofislere kurye ne kadar sürede ulaşır?",
          "Bölge ana arterlere yakın olduğu için alım genellikle 20–30 dakika içinde yapılır."),
         ("Yenibosna'dan havalimanına gönderi çıkarabilir misiniz?",
          "Evet. Hem İstanbul Havalimanı hem Sabiha Gökçen için uçuş saatine göre planlı çıkış yapıyoruz.")],
),

"bagcilar": dict(
    ad="Bağcılar", tip="ilce", yaka="Avrupa", merkez=(41.039, 28.856),
    giris="Bağcılar, İSTOÇ ve Güneşli hattıyla İstanbul'un en büyük toptan ticaret ve imalat bölgelerinden "
          "birini barındırıyor. Binlerce firmanın aynı alanda toplanması, gün içinde çok sayıda kısa mesafeli "
          "ama zamana duyarlı gönderi anlamına geliyor.",
    odak=["İSTOÇ toptancı gönderileri", "Matbaa ve ambalaj numuneleri", "İmalat firmaları arası taşımalar"],
    nokta=["İSTOÇ", "Güneşli iş merkezleri", "Mahmutbey ve Kirazlı",
           "Bağcılar Meydan", "Basın Ekspres bağlantısı", "Bağcılar Eğitim ve Araştırma Hastanesi"],
    komsu=["bahcelievler", "gungoren", "esenler", "basaksehir", "kucukcekmece", "ikitelli"],
    sss=[("İSTOÇ içindeki bloklara teslimat yapıyor musunuz?",
          "Evet, İSTOÇ bizim en yoğun çalıştığımız noktalardan biri. Ada ve blok numarasını paylaşmanız yeterli."),
         ("Bağcılar'dan gün içinde birden çok adrese dağıtım yapabilir misiniz?",
          "Evet. Çok duraklı işlerde güzergâhı optimize ediyor, tek kurye ile birden fazla teslimatı "
          "tamamlayarak maliyeti düşürüyoruz.")],
),

"gungoren": dict(
    ad="Güngören", tip="ilce", yaka="Avrupa", merkez=(41.021, 28.874),
    giris="Güngören, küçük ölçekli tekstil atölyelerinin yoğunlaştığı, sokak aralarına yayılmış bir üretim "
          "ilçesi. Adreslerin çoğu apartman katlarındaki atölyeler olduğu için kurye burada sadece taşımıyor, "
          "doğru katı da buluyor.",
    odak=["Tekstil atölyesi numuneleri", "Fason üretim evrakları", "Küçük paket ve model taşıma"],
    nokta=["Güngören Merkez", "Tozkoparan", "Haznedar", "Gençosman", "Güngören sanayi sokakları", "Akıncılar"],
    komsu=["bahcelievler", "bagcilar", "esenler", "zeytinburnu"],
    sss=[("Atölye adresim tarif gerektiriyor, sorun olur mu?",
          "Olmaz. Kuryemiz gerektiğinde sizi arayarak tarif alır; bölgede düzenli çalıştığımız için "
          "sokakları zaten biliyoruz."),
         ("Güngören'den Osmanbey'e numune kaç dakikada gider?",
          "Ortalama 35–55 dakika. Koleksiyon dönemlerinde günlük sabit saatli taşıma planı da kuruyoruz.")],
),

"esenler": dict(
    ad="Esenler", tip="ilce", yaka="Avrupa", merkez=(41.043, 28.876),
    giris="Esenler, İstanbul Otogarı ve Davutpaşa hattıyla hem şehirler arası çıkışların hem de üniversite "
          "ve sanayi trafiğinin kesiştiği bir ilçe. Otogar üzerinden yapılan şehirler arası gönderilerde "
          "otobüs saatine yetişmek işin en kritik parçası.",
    odak=["Otogar üzerinden şehirler arası gönderi", "Üniversite ve öğrenci evrakları", "Küçük sanayi taşımaları"],
    nokta=["İstanbul Otogarı", "Davutpaşa ve YTÜ kampüsü", "Atışalanı", "Esenler Meydan",
           "Menderes ve Oruçreis", "Kemer"],
    komsu=["bagcilar", "bayrampasa", "gungoren", "gaziosmanpasa", "otogar"],
    sss=[("Otogar'dan şehirler arası gönderi yapabiliyor musunuz?",
          "Evet. Gönderiyi alıp otogardaki firmaya teslim ediyor, kayıt bilgisini size iletiyoruz."),
         ("Davutpaşa kampüsüne evrak teslimi yapılıyor mu?",
          "Evet, kampüs içi birimlere teslimat yapıyoruz; hangi fakülte ve birim olduğunu belirtmeniz yeterli.")],
),

"bayrampasa": dict(
    ad="Bayrampaşa", tip="ilce", yaka="Avrupa", merkez=(41.045, 28.912),
    giris="Bayrampaşa, iş hanları ve tekstil atölyeleriyle yoğun bir ticaret dokusuna sahip. Otogar ve "
          "Vatan Caddesi bağlantısı sayesinde şehrin hem batı hem merkez hattına hızlı çıkış veriyor.",
    odak=["Tekstil ve ambalaj gönderileri", "İş hanı ofis evrakları", "Şehirler arası aktarma taşımaları"],
    nokta=["Bayrampaşa Çarşı Merkezi", "Forum İstanbul", "Otogar çevresi",
           "Altıntepsi", "Terazidere", "Vatan Caddesi bağlantısı"],
    komsu=["esenler", "gaziosmanpasa", "eyupsultan", "fatih", "otogar"],
    sss=[("Bayrampaşa'dan Perpa'ya kurye kaç dakikada gider?",
          "Ortalama 25–40 dakika. İki bölge arasında düzenli çalıştığımız için bu hat bizde standart."),
         ("İş hanındaki dükkâna kurye çıkıyor mu?",
          "Evet, kurye kat ve dükkân numarasına kadar çıkar; teslim sonrası bilgi verir.")],
),

"gaziosmanpasa": dict(
    ad="Gaziosmanpaşa", tip="ilce", yaka="Avrupa", merkez=(41.076, 28.912),
    giris="Gaziosmanpaşa, yoğun konut dokusunun içine yayılmış küçük işletmeleriyle gün boyu düzenli ama "
          "kısa mesafeli kurye talebi üretiyor. Karayolları ve Küçükköy hattı ilçenin en hareketli ticaret "
          "koridoru.",
    odak=["Mahalle esnafı ve market gönderileri", "Eczane ve ilaç teslimatı", "Küçük ticari evrak"],
    nokta=["GOP Merkez", "Karayolları", "Küçükköy", "Yenidoğan", "Sarıgöl", "Barbaros Hayrettin Paşa"],
    komsu=["eyupsultan", "sultangazi", "bayrampasa", "esenler"],
    sss=[("Gaziosmanpaşa'da ilçe içi teslimat ne kadar sürer?",
          "Çoğu ilçe içi iş 30–50 dakika bandında tamamlanır."),
         ("Eczaneden hastaya ilaç taşıyor musunuz?",
          "Evet, eczane teslimatı ayrı bir hizmet başlığımız. Reçeteli ilaç taşımalarında teslim "
          "doğrudan hastaya yapılır.")],
),

"sultangazi": dict(
    ad="Sultangazi", tip="ilce", yaka="Avrupa", merkez=(41.107, 28.870),
    giris="Sultangazi, Cebeci sanayi sitesi ve çevresindeki imalatçılarla birlikte teknik parça ve numune "
          "gönderisinin yoğun olduğu bir ilçe. Metro hattı boyunca uzanan yerleşim ise günlük paket "
          "teslimatlarını besliyor.",
    odak=["Sanayi sitesi parça gönderileri", "Ticari evrak ve fatura", "Konut bölgesi paket teslimatları"],
    nokta=["Cebeci Sanayi Sitesi", "Sultançiftliği metro çevresi", "50. Yıl", "Habibler",
           "Esentepe", "Uğur Mumcu"],
    komsu=["gaziosmanpasa", "eyupsultan", "basaksehir", "arnavutkoy"],
    sss=[("Cebeci sanayiden parça taşıması yapıyor musunuz?",
          "Evet. Küçük ve orta boy teknik parçalar motor kurye ile taşınabiliyor; ağırlık ve hacim "
          "durumunda uygun aracı yönlendiriyoruz."),
         ("Sultangazi'den merkeze evrak ne kadar sürede ulaşır?",
          "Şişli ve Kağıthane hattına ortalama 35–55 dakikada ulaşıyoruz.")],
),

"eyupsultan": dict(
    ad="Eyüpsultan", tip="ilce", yaka="Avrupa", merkez=(41.048, 28.933),
    giris="Eyüpsultan, Haliç kıyısındaki tarihi merkezden Göktürk ve Kemerburgaz'daki yeni yerleşimlere kadar "
          "çok geniş bir alana yayılıyor. Alibeyköy'deki ticaret ile Göktürk'teki konut bölgeleri arasında "
          "mesafe belirgin; bu yüzden çıkış planı burada önemli.",
    odak=["Alibeyköy ticari gönderileri", "Göktürk ve Kemerburgaz konut teslimatları", "Topçular sanayi evrakları"],
    nokta=["Eyüpsultan merkez", "Alibeyköy metro ve otogar", "Göktürk", "Kemerburgaz",
           "Topçular sanayi", "Rami ve Yeşilpınar"],
    komsu=["kagithane", "gaziosmanpasa", "bayrampasa", "fatih", "sariyer"],
    sss=[("Göktürk'e teslimat yapıyor musunuz?",
          "Evet. Göktürk ve Kemerburgaz'daki site ve villalara düzenli teslimat yapıyoruz; "
          "mesafe uzun olduğu için ücreti önceden bildiriyoruz."),
         ("Alibeyköy'den Kağıthane'ye kurye kaç dakika?",
          "Çok kısa bir hat; ortalama 15–30 dakika içinde tamamlanıyor.")],
),

"sariyer": dict(
    ad="Sarıyer", tip="ilce", yaka="Avrupa", merkez=(41.166, 29.057),
    giris="Sarıyer, Maslak'taki plaza yoğunluğu ile Boğaz kıyısındaki yerleşimleri ve kuzeydeki orman "
          "köylerini aynı ilçede topluyor. Maslak hattı kurumsal evrak üretirken, Zekeriyaköy ve Kilyos "
          "tarafında mesafeler ciddi biçimde artıyor.",
    odak=["Maslak plaza ve genel müdürlük evrakları", "Villa ve site teslimatları", "Üniversite kampüsü gönderileri"],
    nokta=["Maslak plazaları", "İstinyePark ve İstinye", "Zekeriyaköy ve Demirciköy",
           "Tarabya, Yeniköy, Emirgan", "İTÜ Ayazağa Kampüsü", "Kilyos"],
    komsu=["besiktas", "kagithane", "sisli", "eyupsultan", "maslak", "levent"],
    sss=[("Maslak'taki plazalara kurye ne kadar sürede gelir?",
          "Maslak ve Levent hattında sürekli kuryemiz bulunduğu için alım genellikle 15–25 dakikada yapılır."),
         ("Zekeriyaköy ve Kilyos'a teslimat var mı?",
          "Var. Bu bölgelerde mesafe uzun olduğu için ücret mesafeye göre hesaplanır; "
          "çıkış öncesi net fiyat veriyoruz.")],
),

"kucukcekmece": dict(
    ad="Küçükçekmece", tip="ilce", yaka="Avrupa", merkez=(41.000, 28.786),
    giris="Küçükçekmece, Halkalı ve Sefaköy hattındaki ticaret ve sanayi dokusuyla batı yakasının en yoğun "
          "kurye bölgelerinden biri. Halkalı'daki lojistik tesisleri ile Sefaköy'deki küçük imalat "
          "birbirini besleyen iki ayrı gönderi akışı oluşturuyor.",
    odak=["Lojistik ve depo evrakları", "İmalat numuneleri", "Toplu konut bölgesi teslimatları"],
    nokta=["Halkalı ve Marmaray çevresi", "Sefaköy", "Atakent ve Cennet",
           "Beşyol", "Kanarya ve Yeşilova", "İkitelli bağlantısı"],
    komsu=["bakirkoy", "bahcelievler", "avcilar", "basaksehir", "bagcilar", "ikitelli"],
    sss=[("Halkalı'daki depolardan çıkış yapıyor musunuz?",
          "Evet. Depo ve lojistik tesislerinden evrak ve numune alımı düzenli işlerimiz arasında."),
         ("Küçükçekmece'den Avrupa yakası merkezine süre ne kadar?",
          "Şişli ve Beşiktaş hattına ortalama 45–70 dakika; acil işlerde VIP kurye öneriyoruz.")],
),

"avcilar": dict(
    ad="Avcılar", tip="ilce", yaka="Avrupa", merkez=(40.980, 28.717),
    giris="Avcılar, üniversite kampüsü, Ambarlı Limanı ve E-5 hattı boyunca uzanan ticaret alanlarıyla "
          "birbirinden farklı üç kurye talebini bir arada barındırıyor. Liman çevresindeki firmalar için "
          "gümrük ve sevkiyat evrakı taşımak en sık yaptığımız iş.",
    odak=["Liman ve gümrük evrakları", "Üniversite ve öğrenci belgeleri", "E-5 hattı ticari gönderiler"],
    nokta=["Ambarlı Limanı", "İstanbul Üniversitesi-Cerrahpaşa Avcılar Kampüsü", "Avcılar Merkez ve E-5",
           "Yeşilkent", "Firuzköy", "Denizköşkler"],
    komsu=["kucukcekmece", "beylikduzu", "esenyurt", "basaksehir"],
    sss=[("Ambarlı'dan gümrük evrakı taşıyor musunuz?",
          "Evet. Liman ve gümrük çevresindeki evrak taşımaları düzenli hizmetlerimizden; "
          "zaman kritik olduğunda express veya VIP kurye öneriyoruz."),
         ("Avcılar'dan merkeze aynı gün gönderi olur mu?",
          "Olur. Sabah ve öğle çıkışlarında aynı gün teslim garanti altında; akşam saatlerinde "
          "trafik nedeniyle süre uzayabilir.")],
),

"beylikduzu": dict(
    ad="Beylikdüzü", tip="ilce", yaka="Avrupa", merkez=(41.001, 28.641),
    giris="Beylikdüzü, planlı yerleşimi ve geniş caddeleriyle teslimatın hızlı ilerlediği bir ilçe. "
          "Yakuplu tarafındaki iş merkezleri ile sahil hattındaki konut siteleri, gün içinde birbirinden "
          "bağımsız iki ayrı kurye akışı oluşturuyor.",
    odak=["İş merkezi ofis evrakları", "Site ve konut teslimatları", "Mağaza ve AVM gönderileri"],
    nokta=["Yakuplu iş merkezleri", "Beylicium ve Marmara Park", "Adnan Kahveci",
           "Beylikdüzü sahil", "Gürpınar", "Kavaklı"],
    komsu=["esenyurt", "avcilar", "buyukcekmece"],
    sss=[("Beylikdüzü'nden merkeze kurye mantıklı mı?",
          "Evet, ancak mesafe uzun. Aynı gün teslim için sabah çıkış, acil işler için VIP kurye öneriyoruz."),
         ("İlçe içi teslimat ne kadar sürüyor?",
          "Beylikdüzü içi işler genellikle 25–45 dakika bandında tamamlanıyor.")],
),

"esenyurt": dict(
    ad="Esenyurt", tip="ilce", yaka="Avrupa", merkez=(41.029, 28.680),
    giris="Esenyurt, nüfusuyla İstanbul'un en kalabalık ilçesi ve Akçaburgaz'daki sanayi bölgesiyle ciddi bir "
          "üretim merkezi. Yoğun yerleşim nedeniyle adres tarifi burada işin en önemli parçası; "
          "mahalle ve cadde bilgisini net paylaşmak teslim süresini kısaltıyor.",
    odak=["Akçaburgaz sanayi gönderileri", "Yoğun konut bölgesi teslimatları", "Ticari evrak ve fatura"],
    nokta=["Akçaburgaz sanayi bölgesi", "Doğan Araslı Bulvarı", "Haramidere",
           "Torium ve Marmara Park", "Esenkent", "Kıraç"],
    komsu=["beylikduzu", "avcilar", "basaksehir", "buyukcekmece", "esenyurt-merkez"],
    sss=[("Akçaburgaz'daki fabrikalardan çıkış yapıyor musunuz?",
          "Evet. Sanayi bölgesindeki firmalar için numune, kalıp ve evrak taşımaları düzenli işlerimizden."),
         ("Esenyurt'ta adres bulmak sorun oluyor mu?",
          "Bölgeyi tanıyan kuryelerle çalışıyoruz. Mahalle, cadde ve bina numarasını paylaşmanız "
          "ilk seferde doğru adrese gitmemiz için yeterli.")],
),

"basaksehir": dict(
    ad="Başakşehir", tip="ilce", yaka="Avrupa", merkez=(41.093, 28.802),
    giris="Başakşehir, İkitelli OSB'yi sınırları içinde barındırdığı için İstanbul'un en yüksek sanayi kurye "
          "hacmine sahip ilçelerinden biri. Buna Kayaşehir'deki toplu konutlar ve Çam ve Sakura Şehir "
          "Hastanesi'nin oluşturduğu trafik ekleniyor.",
    odak=["İkitelli OSB sanayi gönderileri", "Matbaa ve baskı işleri", "Hastane ve sağlık evrakları"],
    nokta=["İkitelli OSB", "Başakşehir Çam ve Sakura Şehir Hastanesi", "Kayaşehir",
           "Bahçeşehir", "Mall of İstanbul", "Metrokent"],
    komsu=["bagcilar", "kucukcekmece", "esenyurt", "sultangazi", "arnavutkoy", "ikitelli"],
    sss=[("İkitelli OSB içindeki bloklara teslimat yapıyor musunuz?",
          "Evet, OSB bizim en yoğun çalıştığımız bölgelerden. Ada, blok ve kapı numarasını paylaşmanız yeterli."),
         ("Şehir Hastanesi'ne evrak veya numune taşıyor musunuz?",
          "Evet. Sağlık kuruluşlarına yapılan teslimatlarda kurye ilgili birime kadar çıkar.")],
),

"arnavutkoy": dict(
    ad="Arnavutköy", tip="ilce", yaka="Avrupa", merkez=(41.184, 28.740),
    giris="Arnavutköy, İstanbul Havalimanı ve Hadımköy sanayi bölgesiyle şehrin kuzeybatı lojistik "
          "koridorunun merkezinde. Havalimanına yetişmesi gereken gönderiler ile OSB firmalarının "
          "sevkiyat evrakları ilçedeki kurye trafiğinin büyük kısmını oluşturuyor.",
    odak=["Havalimanı ve uçak kargo gönderileri", "Hadımköy sanayi evrakları", "Depo ve lojistik taşımaları"],
    nokta=["İstanbul Havalimanı", "Hadımköy sanayi bölgesi", "Deliklikaya OSB",
           "Taşoluk", "Bolluca", "Arnavutköy merkez"],
    komsu=["basaksehir", "sultangazi", "eyupsultan", "catalca"],
    sss=[("İstanbul Havalimanı'na kurye ile gönderi ulaştırıyor musunuz?",
          "Evet. Kargo kabul saatine göre planlı çıkış yapıyor, gerekirse VIP kurye ile doğrudan gidiyoruz."),
         ("Hadımköy'den merkeze evrak süresi nedir?",
          "Şişli ve Kağıthane hattına ortalama 50–75 dakika; sabah erken çıkışlar belirgin şekilde daha hızlı.")],
),

"buyukcekmece": dict(
    ad="Büyükçekmece", tip="ilce", yaka="Avrupa", merkez=(41.020, 28.585),
    giris="Büyükçekmece, TÜYAP Fuar Merkezi sayesinde fuar dönemlerinde yoğun bir gönderi trafiğine sahne "
          "oluyor. Fuar dışındaki günlerde ise Mimarsinan sanayi ve sahil hattındaki yerleşimler "
          "düzenli kurye talebi üretiyor.",
    odak=["Fuar ve stand malzemesi gönderileri", "Sanayi ve imalat evrakları", "Sahil hattı konut teslimatları"],
    nokta=["TÜYAP Fuar Merkezi", "Mimarsinan sanayi", "Kumburgaz sahil",
           "Büyükçekmece merkez", "Celaliye ve Kamiloba", "Güzelce"],
    komsu=["beylikduzu", "esenyurt", "silivri", "catalca"],
    sss=[("Fuar sırasında TÜYAP'a acil gönderi ulaştırabilir misiniz?",
          "Evet. Fuar günlerinde stand numarasını paylaşmanız yeterli; kurye doğrudan hole kadar gider."),
         ("Kumburgaz'a teslimat yapıyor musunuz?",
          "Yapıyoruz. Mesafe uzun olduğu için ücret mesafeye göre hesaplanır ve çıkış öncesi bildirilir.")],
),

"catalca": dict(
    ad="Çatalca", tip="ilce", yaka="Avrupa", merkez=(41.143, 28.461),
    giris="Çatalca, İstanbul'un batı ucundaki en geniş yüzölçümlü ilçelerinden biri ve köyleri birbirinden "
          "uzak. Muratbey OSB çevresindeki firmalar ile merkezdeki resmi kurumlar arasındaki evrak trafiği "
          "burada en sık yaptığımız iş.",
    odak=["OSB firmalarının sevkiyat evrakları", "Resmi kurum ve belediye evrakları", "Uzun mesafe planlı teslimatlar"],
    nokta=["Çatalca merkez ve Kaleiçi", "Muratbey OSB", "Ferhatpaşa",
           "Ormanlı ve Karacaköy", "İnceğiz", "Kuzey Marmara Otoyolu bağlantısı"],
    komsu=["arnavutkoy", "buyukcekmece", "silivri", "basaksehir"],
    sss=[("Çatalca'ya aynı gün gönderi çıkabiliyor mu?",
          "Evet, ancak mesafe nedeniyle çıkış saatinin erken olması gerekiyor. Sabah verilen işleri "
          "aynı gün teslim ediyoruz."),
         ("Köylere teslimat yapıyor musunuz?",
          "Yapıyoruz. Karacaköy, Ormanlı gibi uzak yerleşimlere de çıkıyoruz; ücret mesafeye göre hesaplanır.")],
),

"silivri": dict(
    ad="Silivri", tip="ilce", yaka="Avrupa", merkez=(41.073, 28.246),
    giris="Silivri, İstanbul'un batı sınırındaki en uzak ilçe. Merkezdeki ticaret ile Selimpaşa ve Çanta "
          "hattındaki yerleşimler arasındaki mesafeler bile tek başına ciddi; bu yüzden buradaki işleri "
          "planlı çıkışlarla yürütüyoruz.",
    odak=["Resmi kurum ve noter evrakları", "İşletme ve otel gönderileri", "Planlı uzun mesafe teslimatlar"],
    nokta=["Silivri merkez", "Selimpaşa", "Çanta", "Gümüşyaka", "Değirmenköy", "Silivri sahil hattı"],
    komsu=["buyukcekmece", "catalca"],
    sss=[("Silivri'ye aynı gün teslimat mümkün mü?",
          "Sabah saatlerinde verilen gönderiler için mümkün. Öğleden sonra alınan işlerde teslim "
          "ertesi güne kalabilir; net bilgiyi baştan veriyoruz."),
         ("Silivri'den İstanbul merkezine gönderi alıyor musunuz?",
          "Evet, iki yönlü çalışıyoruz. Dönüş yükü planlanabildiği için bu hatta uygun fiyat verebiliyoruz.")],
),

# =====================================================================
#  MIKRO BOLGELER
# =====================================================================

"levent": dict(
    ad="Levent", tip="bolge", ilce="Beşiktaş", yaka="Avrupa", merkez=(41.082, 29.011),
    giris="Levent, İstanbul'un finans ve genel müdürlük omurgası. Büyükdere Caddesi boyunca sıralanan "
          "kulelerde her gün imzalı sözleşme, teminat mektubu ve ihale dosyası hareket ediyor. "
          "Bölgede sürekli kuryemiz bulunduğu için alım süresi burada en kısa seviyede.",
    odak=["Sözleşme ve ihale dosyaları", "Banka ve teminat evrakları", "Kule içi ofisler arası taşıma"],
    nokta=["Kanyon ve Metrocity", "Sapphire ve Özdilek", "Büyükdere Caddesi kuleleri",
           "4. Levent iş merkezleri", "Nispetiye ve Akatlar", "Etiler"],
    komsu=["besiktas", "sariyer", "maslak", "zincirlikuyu", "kagithane"],
    sss=[("Levent'teki kulelere kurye kaç dakikada gelir?",
          "Bölgede sürekli kurye bulundurduğumuz için alım genellikle 15–25 dakika içinde yapılır."),
         ("Plaza girişlerinde kimlik zorunluluğu süreyi uzatır mı?",
          "Kuryelerimiz bu prosedüre alışkın ve süreyi hesaba katıyoruz. Kat, blok ve ilgili kişi bilgisini "
          "paylaşmanız teslim süresini birkaç dakika daha kısaltır.")],
),

"maslak": dict(
    ad="Maslak", tip="bolge", ilce="Sarıyer", yaka="Avrupa", merkez=(41.111, 29.020),
    giris="Maslak, teknoloji şirketleri, mimarlık ofisleri ve genel müdürlüklerin yoğunlaştığı bir plaza "
          "koridoru. Buradaki gönderiler çoğunlukla zamana duyarlı: ihale saati, imza randevusu ya da "
          "üretim onayı bekleyen dosyalar.",
    odak=["Proje ve ihale dosyaları", "Teknoloji şirketi ekipman ve evrakları", "Genel müdürlük yazışmaları"],
    nokta=["Maslak 1453 ve çevresi", "Uniq İstanbul", "Nurol Plaza ve çevresi",
           "İTÜ Ayazağa Kampüsü", "Büyükdere Caddesi kuzey hattı", "Ayazağa"],
    komsu=["sariyer", "levent", "kagithane", "seyrantepe", "besiktas"],
    sss=[("Maslak'tan Anadolu yakasına acil evrak nasıl gider?",
          "FSM köprüsü üzerinden VIP kurye ile doğrudan çıkış yapıyoruz; kurye yolda başka adrese uğramaz."),
         ("Maslak'ta gece geç saatte kurye bulunur mu?",
          "Evet, 7/24 çalışıyoruz. 20:00 sonrasında gece tarifesi uygulanır ve ücreti önceden bildiririz.")],
),

"nisantasi": dict(
    ad="Nişantaşı", tip="bolge", ilce="Şişli", yaka="Avrupa", merkez=(41.048, 28.994),
    giris="Nişantaşı, showroom ve butiklerin yoğunlaştığı bir bölge; gönderilerin çoğu değerli, kırılgan ya da "
          "sunum kalitesi önemli ürünler. Dar sokaklar ve park sorunu nedeniyle motor kurye burada "
          "araçlı taşımanın önüne geçiyor.",
    odak=["Butik ve showroom gönderileri", "Değerli ve kırılgan ürünler", "Klinik ve muayenehane evrakları"],
    nokta=["Abdi İpekçi Caddesi", "Teşvikiye ve Maçka", "Vali Konağı Caddesi",
           "City's Nişantaşı", "Rumeli Caddesi", "Osmanbey sınırı"],
    komsu=["sisli", "besiktas", "sisli-merkez", "mecidiyekoy", "beyoglu"],
    sss=[("Butiğimden müşteriye özel paket gönderebilir misiniz?",
          "Evet. Sunum kalitesi önemli gönderilerde VIP kurye öneriyoruz; paket tek başına taşınır "
          "ve doğrudan alıcıya teslim edilir."),
         ("Nişantaşı'nda park sorunu teslimatı geciktirir mi?",
          "Motor kurye bu sorundan etkilenmiyor; teslimat kapıya kadar sorunsuz tamamlanıyor.")],
),

"mecidiyekoy": dict(
    ad="Mecidiyeköy", tip="bolge", ilce="Şişli", yaka="Avrupa", merkez=(41.067, 28.997),
    giris="Mecidiyeköy, İstanbul'un en yoğun ulaşım ve ofis kavşağı. Metrobüs hattı, plazalar ve iş hanları "
          "aynı noktada toplandığı için burası hem gönderi çıkışının hem de aktarmanın en sık yapıldığı "
          "bölgelerden biri.",
    odak=["Ofis ve iş hanı evrakları", "Plaza içi teslimatlar", "Hızlı aktarma gönderileri"],
    nokta=["Trump Towers", "Profilo ve çevresi", "Metrobüs durağı çevresi",
           "Gülbahar ve Fulya", "Esentepe iş merkezleri", "Ali Sami Yen çevresi"],
    komsu=["sisli", "sisli-merkez", "zincirlikuyu", "nisantasi", "kagithane", "levent"],
    sss=[("Mecidiyeköy'den kurye ne kadar sürede alınır?",
          "Bölge merkez üssümüze çok yakın olduğu için alım genellikle 10–20 dakikada yapılır."),
         ("Trafik yoğunluğu Mecidiyeköy teslimatlarını etkiliyor mu?",
          "Motor kurye bu koridorda trafikten en az etkilenen taşıma biçimi; araçla 40 dakika süren yol "
          "motorla çoğu zaman yarı sürede tamamlanıyor.")],
),

"zincirlikuyu": dict(
    ad="Zincirlikuyu", tip="bolge", ilce="Beşiktaş", yaka="Avrupa", merkez=(41.068, 29.010),
    giris="Zincirlikuyu, Büyükdere Caddesi'nin en yoğun kesiti ve köprü çıkışına doğrudan bağlanıyor. "
          "Bu konum, Anadolu yakasına acil çıkacak gönderiler için bölgeyi doğal bir başlangıç noktası "
          "hâline getiriyor.",
    odak=["Yaka geçişli acil evraklar", "Plaza ve ofis gönderileri", "AVM ve mağaza teslimatları"],
    nokta=["Zorlu Center", "Büyükdere Caddesi ofisleri", "Zincirlikuyu metro çevresi",
           "Esentepe sınırı", "Levent bağlantısı", "Boğaziçi Köprüsü çıkışı"],
    komsu=["besiktas", "levent", "mecidiyekoy", "sisli", "kadikoy"],
    sss=[("Zincirlikuyu'dan Anadolu yakasına süre ne kadar?",
          "Köprü trafiğine bağlı olarak Kadıköy ve Ataşehir hattına ortalama 35–60 dakika."),
         ("Zorlu Center içindeki mağazalara teslimat yapıyor musunuz?",
          "Evet. AVM içi teslimatlarda kurye mağaza kapısına kadar gider.")],
),

"sisli-merkez": dict(
    ad="Şişli Merkez", tip="bolge", ilce="Şişli", yaka="Avrupa", merkez=(41.060, 28.987),
    giris="Şişli Merkez, Halaskargazi Caddesi boyunca uzanan ofis, klinik ve mağaza yoğunluğuyla gün içinde "
          "kesintisiz kurye trafiği üretiyor. Cevahir çevresindeki iş merkezleri ile Osmanbey'deki tekstil "
          "ofisleri bu talebin omurgasını oluşturuyor.",
    odak=["Klinik ve muayenehane evrakları", "Tekstil ofisi numuneleri", "Mağaza ve ofis gönderileri"],
    nokta=["Halaskargazi Caddesi", "Şişli Cevahir", "Osmanbey", "Şişli Etfal Hastanesi",
           "Bomonti", "Kurtuluş"],
    komsu=["sisli", "nisantasi", "mecidiyekoy", "perpa", "kagithane"],
    sss=[("Şişli'deki kliniklere numune taşıyor musunuz?",
          "Evet. Tahlil ve numune taşımalarında kurye doğrudan ilgili birime teslim eder."),
         ("Şişli merkezde alım süresi ne kadar?",
          "Merkez üssümüze yakın olduğu için genellikle 10–20 dakika içinde alım yapılıyor.")],
),

"taksim-beyoglu": dict(
    ad="Taksim ve Beyoğlu", tip="bolge", ilce="Beyoğlu", yaka="Avrupa", merkez=(41.037, 28.985),
    giris="Taksim ve çevresi, otel, ajans ve işletme yoğunluğu ile yaya trafiğinin en yüksek olduğu bölge. "
          "Araçla girişin neredeyse imkânsız olduğu sokaklarda motor kurye teslimatı ayakta tutan tek "
          "pratik çözüm.",
    odak=["Otel ve misafir teslimatları", "Ajans ve prodüksiyon gönderileri", "Restoran ve işletme evrakları"],
    nokta=["Taksim Meydanı", "İstiklal Caddesi", "Gümüşsuyu otelleri",
           "Cihangir", "Asmalımescit", "Tarlabaşı Bulvarı"],
    komsu=["beyoglu", "sisli", "besiktas", "fatih", "nisantasi"],
    sss=[("Oteldeki misafire acil belge ulaştırabilir misiniz?",
          "Evet. Otel resepsiyonuna ya da doğrudan misafire teslim yapıyoruz; hangi yöntemi istediğinizi "
          "belirtmeniz yeterli."),
         ("Yaya bölgesine motor giriyor mu?",
          "Kısıtlı bölgelerde kurye en yakın noktaya kadar motorla gelip teslimatı yürüyerek tamamlıyor.")],
),

"caglayan": dict(
    ad="Çağlayan", tip="bolge", ilce="Kağıthane", yaka="Avrupa", merkez=(41.073, 28.981),
    giris="Çağlayan denince akla İstanbul Adliyesi geliyor: Avrupa'nın en büyük adliye binalarından biri. "
          "Buradaki kurye işi süreyle yarışıyor; dilekçe, dosya ve tebligatın gün içinde belirli bir saate "
          "yetişmesi gerekiyor. Merkez ofisimiz Çağlayan'a birkaç dakika uzaklıkta.",
    odak=["Dava dosyası ve dilekçe teslimi", "Hukuk bürosu evrakları", "Bilirkişi ve tebligat taşıma"],
    nokta=["İstanbul Adliyesi", "Adliye çevresi hukuk büroları", "Çağlayan Meydan",
           "Vadistanbul bağlantısı", "Kağıthane merkez", "Gürsel ve Talatpaşa"],
    komsu=["kagithane", "sisli", "seyrantepe", "sisli-merkez", "mecidiyekoy"],
    sss=[("Duruşma saatine yetişecek dosya teslimi yapabilir misiniz?",
          "Evet, en sık yaptığımız işlerden biri. Saati söylediğinizde geri sayımı ona göre planlıyor, "
          "gerekirse VIP kurye ile doğrudan çıkıyoruz."),
         ("Adliyeye teslim sonrası bilgi veriyor musunuz?",
          "Veriyoruz. Teslim tamamlandığında kurye bilgi geçer; talep ederseniz teslim fotoğrafı da paylaşılır.")],
),

"seyrantepe": dict(
    ad="Seyrantepe", tip="bolge", ilce="Kağıthane", yaka="Avrupa", merkez=(41.099, 28.997),
    giris="Seyrantepe, Cendere Vadisi boyunca yükselen ofis kuleleri ve teknoloji firmalarıyla hızla büyüyen "
          "bir iş bölgesi. Skyland ve çevresindeki kulelerden çıkan gönderiler çoğunlukla kurumsal ve "
          "zamana duyarlı.",
    odak=["Ofis kulesi evrakları", "Teknoloji firması gönderileri", "Ajans ve matbaa işleri"],
    nokta=["Skyland İstanbul", "Cendere Caddesi ofisleri", "Vadistanbul",
           "Seyrantepe metro çevresi", "Sanayi Mahallesi", "Hamidiye"],
    komsu=["kagithane", "caglayan", "maslak", "levent", "sariyer"],
    sss=[("Seyrantepe'deki kulelere kurye ne kadar sürede gelir?",
          "Merkez ofisimize çok yakın olduğu için alım genellikle 10–20 dakikada yapılır."),
         ("Cendere hattından Maslak'a gönderi ne kadar sürer?",
          "Çok kısa bir hat; ortalama 15–25 dakika içinde teslim ediliyor.")],
),

"perpa": dict(
    ad="Perpa", tip="bolge", ilce="Şişli", yaka="Avrupa", merkez=(41.062, 28.966),
    giris="Perpa Ticaret Merkezi, tek çatı altında binlerce firmayı barındıran devasa bir iş merkezi. "
          "Bloklar ve katlar arasında bile ciddi mesafe olduğu için buradaki kurye işi adres bulmaktan çok "
          "doğru katı ve kapıyı bilmekle ilgili.",
    odak=["Firma içi ve firmalar arası evrak", "Elektronik ve teknik parça gönderileri", "Toptan ticaret paketleri"],
    nokta=["Perpa A Blok", "Perpa B Blok", "Perpa çevresi ofisler",
           "Okmeydanı", "Bomonti bağlantısı", "Halıcıoğlu yönü"],
    komsu=["sisli", "kagithane", "beyoglu", "sisli-merkez", "eyupsultan"],
    sss=[("Perpa'da kat ve kapı numarası şart mı?",
          "Şart değil ama çok işe yarıyor. Blok, kat ve kapı bilgisi verildiğinde teslimat belirgin "
          "şekilde hızlanıyor."),
         ("Perpa'dan gün içinde düzenli kurye alabilir miyim?",
          "Evet. Perpa'da yoğun çalışan firmalar için sabit saatli günlük kurye planı kuruyoruz.")],
),

"otogar": dict(
    ad="Otogar", tip="bolge", ilce="Bayrampaşa", yaka="Avrupa", merkez=(41.041, 28.892),
    giris="15 Temmuz Demokrasi Otogarı, şehirler arası gönderilerin İstanbul'daki en büyük çıkış kapısı. "
          "Buradaki kurye işi otobüs saatiyle yarışıyor: gönderinin firmaya kaydının zamanında yapılması "
          "teslimin tamamını belirliyor.",
    odak=["Şehirler arası gönderi teslimi", "Otobüs firmalarına kayıt", "Acil evrak aktarımı"],
    nokta=["15 Temmuz Demokrasi Otogarı", "Otogar peron bölgesi", "Kargo firmaları hattı",
           "Bayrampaşa çıkışı", "Esenler bağlantısı", "Metro istasyonu çevresi"],
    komsu=["bayrampasa", "esenler", "gaziosmanpasa", "fatih"],
    sss=[("Otobüs saatine yetişecek gönderi taşıyor musunuz?",
          "Evet. Kalkış saatini söylediğinizde çıkışı ona göre planlıyor, kayıt bilgisini size iletiyoruz."),
         ("Otogardan gelen gönderiyi teslim alıp adrese getirir misiniz?",
          "Getiririz. Kargo kodu ve firma bilgisini paylaşmanız yeterli; gönderiyi alıp adresinize ulaştırıyoruz.")],
),

"topkapi": dict(
    ad="Topkapı", tip="bolge", ilce="Zeytinburnu", yaka="Avrupa", merkez=(41.023, 28.917),
    giris="Topkapı ve Cevizlibağ hattı, tekstil ve matbaa firmalarının yoğunlaştığı bir üretim koridoru. "
          "Ana arterlere yakınlığı sayesinde hem merkeze hem batıya çıkış hızlı; bu da bölgeyi aktarma "
          "için elverişli kılıyor.",
    odak=["Tekstil ve matbaa gönderileri", "İş merkezi ofis evrakları", "Numune ve model taşıma"],
    nokta=["Topkapı iş merkezleri", "Cevizlibağ", "Merkezefendi sınırı",
           "Maltepe Mahallesi sanayi", "Vatan Caddesi bağlantısı", "Litros Yolu"],
    komsu=["zeytinburnu", "fatih", "bayrampasa", "gungoren", "esenler"],
    sss=[("Litros Yolu'ndaki matbaalardan çıkış yapıyor musunuz?",
          "Evet. Matbaa provası ve baskı işleri düzenli taşıdığımız gönderiler arasında."),
         ("Topkapı'dan Anadolu yakasına gönderi ne kadar sürer?",
          "Kadıköy hattına ortalama 55–80 dakika; acil işlerde VIP kurye öneriyoruz.")],
),

"ikitelli": dict(
    ad="İkitelli", tip="bolge", ilce="Başakşehir", yaka="Avrupa", merkez=(41.078, 28.795),
    giris="İkitelli Organize Sanayi Bölgesi, on binlerce firmayı barındıran bir üretim şehri. Bloklar arası "
          "mesafeler yüksek, adres yapısı ada–blok sistemine dayanıyor. Bölgeyi tanımayan kurye burada "
          "kolayca zaman kaybeder; bizim kuryelerimiz bu düzeni biliyor.",
    odak=["Matbaa ve baskı işleri", "Makine ve yedek parça gönderileri", "Numune ve prototip taşıma"],
    nokta=["İkitelli OSB blokları", "Masko ve çevresi", "İkitelli sanayi siteleri",
           "Başakşehir bağlantısı", "Bağcılar sınırı", "İkitelli metro çevresi"],
    komsu=["basaksehir", "bagcilar", "kucukcekmece", "esenyurt", "sultangazi"],
    sss=[("İkitelli'de ada ve blok bilgisi olmadan teslimat olur mu?",
          "Firma adı ve telefonuyla da buluyoruz, ancak ada–blok bilgisi verildiğinde teslimat çok daha hızlı."),
         ("OSB içinde birden fazla firmaya aynı anda dağıtım yapılabilir mi?",
          "Evet. Çok duraklı işlerde güzergâhı optimize ediyoruz; bu, gönderi başına maliyeti belirgin şekilde düşürüyor.")],
),

"bakirkoy-merkez": dict(
    ad="Bakırköy Merkez", tip="bolge", ilce="Bakırköy", yaka="Avrupa", merkez=(40.978, 28.872),
    giris="Bakırköy Çarşı ve İncirli hattı, mağaza yoğunluğu yüksek bir yaya bölgesi. Araç girişinin "
          "kısıtlı olduğu bu sokaklarda motor kurye teslimatı hem hızlı hem sorunsuz tamamlıyor.",
    odak=["Mağaza ve butik gönderileri", "Ofis ve muhasebe evrakları", "Sağlık kuruluşu teslimatları"],
    nokta=["Bakırköy Çarşı", "İncirli Caddesi", "Özgürlük Meydanı",
           "Bakırköy Devlet Hastanesi", "Marmaray ve metro çevresi", "Ataköy sınırı"],
    komsu=["bakirkoy", "bahcelievler", "zeytinburnu", "kucukcekmece"],
    sss=[("Çarşı içindeki mağazalara motor giriyor mu?",
          "Yaya bölgesinde kurye en yakın noktaya kadar gelip teslimi yürüyerek tamamlıyor."),
         ("Bakırköy merkezden alım ne kadar sürer?",
          "Bölgede düzenli çalıştığımız için alım genellikle 20–35 dakika içinde yapılır.")],
),

"besiktas-carsi": dict(
    ad="Beşiktaş Çarşı", tip="bolge", ilce="Beşiktaş", yaka="Avrupa", merkez=(41.043, 29.006),
    giris="Beşiktaş Çarşı, küçük işletme ve restoran yoğunluğuyla gün içinde sürekli hareket eden bir bölge. "
          "Dar sokaklar ve park sorunu nedeniyle buradaki teslimatların neredeyse tamamı motor kurye ile "
          "yapılıyor.",
    odak=["Restoran ve kafe gönderileri", "Esnaf ve işletme evrakları", "İskele çevresi acil teslimatlar"],
    nokta=["Beşiktaş Çarşı", "Beşiktaş İskelesi", "Barbaros Bulvarı girişi",
           "Akaretler", "Sinanpaşa ve Türkali", "Abbasağa"],
    komsu=["besiktas", "levent", "zincirlikuyu", "taksim-beyoglu", "sisli"],
    sss=[("Çarşı'daki işletmeme gün içinde birden fazla kurye gelebilir mi?",
          "Evet. Yoğun çalışan işletmeler için gün içi düzenli kurye planı kuruyoruz."),
         ("Beşiktaş'tan Kadıköy'e vapurla mı gidiyorsunuz?",
          "Hayır, teslimat kara yolu üzerinden yapılıyor; süre köprü trafiğine göre değişiyor.")],
),

"bagdat-caddesi": dict(
    ad="Bağdat Caddesi", tip="bolge", ilce="Kadıköy", yaka="Anadolu", merkez=(40.964, 29.079),
    giris="Bağdat Caddesi, Anadolu yakasının en uzun mağaza koridoru. Kalamış'tan Bostancı'ya uzanan hat "
          "boyunca butikler, showroomlar ve kafeler gün içinde sürekli gönderi üretiyor; caddede park "
          "sorunu olduğu için motor kurye burada standart çözüm.",
    odak=["Butik ve mağaza gönderileri", "Müşteriye özel paket teslimi", "Kafe ve restoran taşımaları"],
    nokta=["Caddebostan", "Suadiye", "Erenköy ve Şaşkınbakkal",
           "Göztepe", "Bostancı", "Kalamış ve Fenerbahçe"],
    komsu=["kadikoy", "maltepe", "kozyatagi", "kadikoy-moda", "atasehir"],
    sss=[("Cadde üzerindeki mağazamdan müşteriye paket gönderebilir misiniz?",
          "Evet. Sunum önemliyse VIP kurye öneriyoruz; paket tek başına taşınır ve doğrudan alıcıya teslim edilir."),
         ("Bağdat Caddesi'nde park sorunu teslimatı etkiliyor mu?",
          "Motor kurye bu sorundan etkilenmiyor; teslimat kapıya kadar yapılıyor.")],
),

"kadikoy-moda": dict(
    ad="Moda", tip="bolge", ilce="Kadıköy", yaka="Anadolu", merkez=(40.981, 29.026),
    giris="Moda, ajans, yayınevi ve küçük ölçekli yaratıcı ofislerin yoğunlaştığı bir semt. Sokak yapısı dar "
          "ve tek yönlü; bu yüzden buradaki teslimatlarda motor kurye araçlı taşımaya göre belirgin "
          "zaman avantajı sağlıyor.",
    odak=["Ajans ve yayınevi gönderileri", "Kafe ve butik teslimatları", "Kişisel acil gönderiler"],
    nokta=["Moda Caddesi", "Caferağa", "Bahariye Caddesi", "Kadıköy İskelesi",
           "Yeldeğirmeni", "Moda sahil"],
    komsu=["kadikoy", "bagdat-caddesi", "uskudar", "kozyatagi"],
    sss=[("Moda'daki dar sokaklara teslimat sorun oluyor mu?",
          "Hayır, motor kurye için sorun değil. Bina adı ve kat bilgisini paylaşmanız yeterli."),
         ("Moda'dan Avrupa yakasına gönderi ne kadar sürer?",
          "Şişli ve Beşiktaş hattına ortalama 55–80 dakika; acil işlerde VIP kurye öneriyoruz.")],
),

"kozyatagi": dict(
    ad="Kozyatağı", tip="bolge", ilce="Kadıköy", yaka="Anadolu", merkez=(40.972, 29.098),
    giris="Kozyatağı, Anadolu yakasının plaza hattının başlangıcı. Ataşehir Finans Merkezi'ne komşu konumu "
          "sayesinde kurumsal evrak trafiği yüksek; ofisler arası kısa mesafeli taşımalar burada günün "
          "her saatinde sürüyor.",
    odak=["Plaza ve ofis evrakları", "Finans ve muhasebe belgeleri", "Kurumsal numune taşıma"],
    nokta=["Kozyatağı plazaları", "Palladium çevresi", "Değirmen Sokak ofisleri",
           "Sahrayıcedit", "İçerenköy sınırı", "Kozyatağı metro çevresi"],
    komsu=["kadikoy", "atasehir", "atasehir-finans", "bagdat-caddesi", "maltepe"],
    sss=[("Kozyatağı'ndan Finans Merkezi'ne kurye ne kadar sürer?",
          "Çok kısa bir hat; ortalama 15–25 dakikada tamamlanıyor."),
         ("Plaza içi ofisler arası taşıma yapıyor musunuz?",
          "Evet. Aynı bina veya komşu binalar arasındaki taşımalar için de kurye yönlendiriyoruz.")],
),

"atasehir-finans": dict(
    ad="Ataşehir Finans Merkezi", tip="bolge", ilce="Ataşehir", yaka="Anadolu", merkez=(40.988, 29.128),
    giris="İstanbul Finans Merkezi, banka genel müdürlükleri ve düzenleyici kurumların toplandığı bir "
          "kampüs. Buradaki gönderiler neredeyse istisnasız zamana duyarlı: imza, teminat ve rapor "
          "teslimleri belirli saatlere kilitli.",
    odak=["Banka ve finans evrakları", "Teminat mektubu ve sözleşme", "Denetim ve rapor teslimi"],
    nokta=["İstanbul Finans Merkezi kuleleri", "Barbaros Mahallesi plazaları", "Watergarden",
           "Metropol İstanbul", "Brandium", "Küçükbakkalköy iş merkezleri"],
    komsu=["atasehir", "kozyatagi", "umraniye", "kadikoy", "umraniye-merkez"],
    sss=[("Finans Merkezi'ndeki kulelere giriş prosedürü var mı?",
          "Var; kuryelerimiz ziyaretçi kaydı ve kimlik bırakma prosedürüne alışkın. Kule, kat ve "
          "ilgili kişi bilgisini paylaşmanız teslimi hızlandırır."),
         ("Kapanış saatine yetişmesi gereken evrak için ne öneriyorsunuz?",
          "VIP kurye. Gönderi tek başına taşınır, kurye yol boyunca başka adrese uğramaz.")],
),

"umraniye-merkez": dict(
    ad="Ümraniye Merkez", tip="bolge", ilce="Ümraniye", yaka="Anadolu", merkez=(41.026, 29.098),
    giris="Ümraniye Merkez, Meydan çevresindeki ofisler ve çarşı esnafıyla gün boyu hareketli. Şerifali ve "
          "Dudullu hattına yakınlığı sayesinde ticari gönderiler için pratik bir toplanma noktası.",
    odak=["Ofis ve muhasebe evrakları", "Çarşı esnafı gönderileri", "Sanayi bölgesine aktarma"],
    nokta=["Ümraniye Meydan", "Meydan İstanbul AVM", "Ümraniye çarşı",
           "Şerifali bağlantısı", "Atatürk Mahallesi", "Ümraniye Eğitim ve Araştırma Hastanesi"],
    komsu=["umraniye", "uskudar", "atasehir", "atasehir-finans", "cekmekoy"],
    sss=[("Ümraniye merkezden Şerifali'ye kurye kaç dakika?",
          "Kısa bir hat; ortalama 15–25 dakika içinde tamamlanıyor."),
         ("Merkezden Avrupa yakasına aynı gün teslim olur mu?",
          "Olur. Sabah ve öğle çıkışlarında aynı gün teslim standart; akşam saatlerinde süre uzayabilir.")],
),

"kartal-merkez": dict(
    ad="Kartal Merkez", tip="bolge", ilce="Kartal", yaka="Anadolu", merkez=(40.890, 29.183),
    giris="Kartal Merkez, meydan çevresindeki ticaret ile Anadolu Adalet Sarayı'nın yarattığı evrak "
          "trafiğini bir arada barındırıyor. Sahil hattına ve E-5'e yakınlığı, buradan çıkan gönderilerin "
          "hızlı yayılmasını sağlıyor.",
    odak=["Adliye evrakı ve dosya", "Meydan çevresi ticari gönderiler", "Sağlık kuruluşu teslimatları"],
    nokta=["Kartal Meydan", "Anadolu Adalet Sarayı", "Kordonboyu ve sahil",
           "Kartal Marmaray çevresi", "Dr. Lütfi Kırdar Şehir Hastanesi", "Soğanlık bağlantısı"],
    komsu=["kartal", "maltepe", "pendik", "sancaktepe"],
    sss=[("Adliyeye dosya teslimi yapıyor musunuz?",
          "Evet, Anadolu Adalet Sarayı'na dosya ve dilekçe teslimi düzenli işlerimizden. "
          "Teslim sonrası bilgi veriyoruz."),
         ("Kartal merkezden alım süresi ne kadar?",
          "Bölgede düzenli çalıştığımız için alım genellikle 20–35 dakika içinde yapılıyor.")],
),

"esenyurt-merkez": dict(
    ad="Esenyurt Merkez", tip="bolge", ilce="Esenyurt", yaka="Avrupa", merkez=(41.033, 28.673),
    giris="Esenyurt Merkez, Doğan Araslı Bulvarı çevresinde yoğunlaşan esnaf ve ofis trafiğinin kalbi. "
          "Nüfus yoğunluğu yüksek olduğu için burada teslimatın hızını belirleyen şey mesafeden çok "
          "adresin doğru tarif edilmesi.",
    odak=["Esnaf ve mağaza gönderileri", "Ofis evrakı ve fatura", "Konut bölgesi paket teslimatları"],
    nokta=["Doğan Araslı Bulvarı", "Esenyurt Meydan", "Cumhuriyet Mahallesi",
           "Esenkent", "Torium çevresi", "Haramidere bağlantısı"],
    komsu=["esenyurt", "beylikduzu", "avcilar", "basaksehir"],
    sss=[("Esenyurt merkezde teslimat ne kadar sürüyor?",
          "Bölge içi işler genellikle 25–45 dakika bandında tamamlanıyor."),
         ("Adres tarifi vermem gerekiyor mu?",
          "Mahalle, cadde ve bina numarası yeterli. Gerekirse kurye sizi arayıp tarif alır.")],
),

}
