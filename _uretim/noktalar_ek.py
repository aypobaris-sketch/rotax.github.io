# -*- coding: utf-8 -*-
"""Fiyat hesaplayicidaki NOKTALAR listesini tamamlayan ek mahalle/semt verisi.

Bicim: (ad, ilce, enlem, boylam, yaka)  yaka: A=Avrupa, N=Anadolu
Bu liste uret.py tarafindan mevcut NOKTALAR ile birlestirilir; ayni (ad, ilce)
ikilisi iki kez yazilmis olsa bile tek kayit olarak kalir.
"""

EK_NOKTALAR = [
    # --- Adalar ---
    ("Büyükada", "Adalar", 40.858, 29.124, "N"),
    ("Heybeliada", "Adalar", 40.876, 29.093, "N"),
    ("Burgazada", "Adalar", 40.882, 29.068, "N"),
    ("Kınalıada", "Adalar", 40.908, 29.052, "N"),
    ("Maden", "Adalar", 40.866, 29.126, "N"),
    ("Nizam", "Adalar", 40.856, 29.117, "N"),

    # --- Arnavutköy ---
    ("Yeşilbayır", "Arnavutköy", 41.190, 28.716, "A"),
    ("Boğazköy", "Arnavutköy", 41.174, 28.766, "A"),
    ("Haraççı", "Arnavutköy", 41.147, 28.740, "A"),
    ("Deliklikaya", "Arnavutköy", 41.140, 28.671, "A"),
    ("Hicret", "Arnavutköy", 41.196, 28.746, "A"),
    ("İmrahor", "Arnavutköy", 41.157, 28.755, "A"),
    ("İstanbul Havalimanı", "Arnavutköy", 41.262, 28.742, "A"),

    # --- Avcılar ---
    ("Ambarlı", "Avcılar", 40.972, 28.694, "A"),
    ("Cihangir", "Avcılar", 40.995, 28.712, "A"),
    ("Denizköşkler", "Avcılar", 40.983, 28.707, "A"),
    ("Gümüşpala", "Avcılar", 40.990, 28.703, "A"),
    ("Mustafa Kemal Paşa", "Avcılar", 40.981, 28.727, "A"),
    ("Tahtakale", "Avcılar", 40.987, 28.722, "A"),
    ("Üniversite", "Avcılar", 40.976, 28.699, "A"),
    ("Yeşilkent", "Avcılar", 41.003, 28.678, "A"),

    # --- Bayrampaşa ---
    ("Altıntepsi", "Bayrampaşa", 41.049, 28.907, "A"),
    ("Cevatpaşa", "Bayrampaşa", 41.041, 28.902, "A"),
    ("Kartaltepe", "Bayrampaşa", 41.052, 28.916, "A"),
    ("Kocatepe", "Bayrampaşa", 41.045, 28.919, "A"),
    ("Terazidere", "Bayrampaşa", 41.032, 28.899, "A"),
    ("Vatan", "Bayrampaşa", 41.037, 28.921, "A"),
    ("Yıldırım", "Bayrampaşa", 41.049, 28.899, "A"),

    # --- Beylikdüzü ---
    ("Adnan Kahveci", "Beylikdüzü", 41.004, 28.635, "A"),
    ("Barış", "Beylikdüzü", 41.010, 28.640, "A"),
    ("Büyükşehir", "Beylikdüzü", 41.013, 28.652, "A"),
    ("Dereağzı", "Beylikdüzü", 40.994, 28.646, "A"),
    ("Kavaklı", "Beylikdüzü", 41.017, 28.629, "A"),
    ("Marmara", "Beylikdüzü", 40.998, 28.637, "A"),
    ("Sahil", "Beylikdüzü", 40.990, 28.641, "A"),
    ("Yakuplu", "Beylikdüzü", 40.995, 28.665, "A"),

    # --- Büyükçekmece ---
    ("Celaliye", "Büyükçekmece", 41.017, 28.514, "A"),
    ("Kamiloba", "Büyükçekmece", 41.020, 28.527, "A"),
    ("Güzelce", "Büyükçekmece", 41.014, 28.573, "A"),
    ("Sinanoba", "Büyükçekmece", 41.030, 28.599, "A"),
    ("Türkoba", "Büyükçekmece", 41.058, 28.573, "A"),
    ("Pınartepe", "Büyükçekmece", 41.033, 28.608, "A"),
    ("TÜYAP Fuar Merkezi", "Büyükçekmece", 41.013, 28.649, "A"),

    # --- Çatalca ---
    ("Ferhatpaşa", "Çatalca", 41.144, 28.463, "A"),
    ("Kaleiçi", "Çatalca", 41.140, 28.459, "A"),
    ("Muratbey", "Çatalca", 41.117, 28.505, "A"),
    ("Ovayenice", "Çatalca", 41.106, 28.435, "A"),
    ("Karacaköy", "Çatalca", 41.395, 28.383, "A"),
    ("İnceğiz", "Çatalca", 41.169, 28.484, "A"),
    ("Ormanlı", "Çatalca", 41.310, 28.422, "A"),

    # --- Çekmeköy ---
    ("Taşdelen", "Çekmeköy", 41.023, 29.230, "N"),
    ("Alemdağ", "Çekmeköy", 41.033, 29.226, "N"),
    ("Ömerli", "Çekmeköy", 41.062, 29.245, "N"),
    ("Nişantepe", "Çekmeköy", 41.049, 29.215, "N"),
    ("Mimar Sinan", "Çekmeköy", 41.040, 29.190, "N"),
    ("Çamlık", "Çekmeköy", 41.036, 29.176, "N"),
    ("Hamidiye", "Çekmeköy", 41.043, 29.168, "N"),
    ("Soğukpınar", "Çekmeköy", 41.030, 29.199, "N"),
    ("Aydınlar", "Çekmeköy", 41.026, 29.185, "N"),

    # --- Esenler ---
    ("Atışalanı", "Esenler", 41.055, 28.881, "A"),
    ("Menderes", "Esenler", 41.037, 28.882, "A"),
    ("Fevzi Çakmak", "Esenler", 41.049, 28.869, "A"),
    ("Oruçreis", "Esenler", 41.047, 28.885, "A"),
    ("Nine Hatun", "Esenler", 41.033, 28.878, "A"),
    ("Kemer", "Esenler", 41.055, 28.869, "A"),
    ("Birlik", "Esenler", 41.050, 28.876, "A"),
    ("Çiftehavuzlar", "Esenler", 41.041, 28.888, "A"),

    # --- Gaziosmanpaşa ---
    ("Karayolları", "Gaziosmanpaşa", 41.062, 28.906, "A"),
    ("Yenidoğan", "Gaziosmanpaşa", 41.081, 28.917, "A"),
    ("Sarıgöl", "Gaziosmanpaşa", 41.058, 28.919, "A"),
    ("Barbaros Hayrettin Paşa", "Gaziosmanpaşa", 41.078, 28.901, "A"),
    ("Yıldıztabya", "Gaziosmanpaşa", 41.072, 28.888, "A"),
    ("Hürriyet", "Gaziosmanpaşa", 41.085, 28.909, "A"),
    ("Mevlana", "Gaziosmanpaşa", 41.071, 28.925, "A"),

    # --- Güngören ---
    ("Tozkoparan", "Güngören", 41.017, 28.885, "A"),
    ("Haznedar", "Güngören", 41.014, 28.877, "A"),
    ("Gençosman", "Güngören", 41.028, 28.879, "A"),
    ("Güngören Sanayi", "Güngören", 41.020, 28.870, "A"),
    ("Akıncılar", "Güngören", 41.010, 28.869, "A"),
    ("Güven", "Güngören", 41.024, 28.867, "A"),
    ("Mareşal Çakmak", "Güngören", 41.026, 28.872, "A"),
    ("Abdurrahman Nafiz Gürman", "Güngören", 41.017, 28.867, "A"),

    # --- Sancaktepe ---
    ("Sarıgazi", "Sancaktepe", 41.011, 29.216, "N"),
    ("Yenidoğan", "Sancaktepe", 40.996, 29.243, "N"),
    ("Abdurrahmangazi", "Sancaktepe", 40.999, 29.221, "N"),
    ("Emek", "Sancaktepe", 41.004, 29.234, "N"),
    ("Osmangazi", "Sancaktepe", 40.989, 29.229, "N"),
    ("Meclis", "Sancaktepe", 41.007, 29.203, "N"),
    ("Merve", "Sancaktepe", 40.983, 29.238, "N"),
    ("Akpınar", "Sancaktepe", 41.021, 29.252, "N"),
    ("Paşaköy", "Sancaktepe", 41.036, 29.269, "N"),
    ("Veysel Karani", "Sancaktepe", 40.987, 29.220, "N"),

    # --- Silivri ---
    ("Alibey", "Silivri", 41.076, 28.243, "A"),
    ("Piri Mehmet Paşa", "Silivri", 41.073, 28.247, "A"),
    ("Mimar Sinan", "Silivri", 41.078, 28.236, "A"),
    ("Ortaköy", "Silivri", 41.086, 28.262, "A"),
    ("Gümüşyaka", "Silivri", 41.043, 28.322, "A"),
    ("Kavaklı", "Silivri", 41.062, 28.294, "A"),
    ("Değirmenköy", "Silivri", 41.144, 28.259, "A"),
    ("Çanta", "Silivri", 41.043, 28.354, "A"),

    # --- Sultanbeyli ---
    ("Abdurrahmangazi", "Sultanbeyli", 40.966, 29.263, "N"),
    ("Battalgazi", "Sultanbeyli", 40.957, 29.270, "N"),
    ("Fatih", "Sultanbeyli", 40.963, 29.276, "N"),
    ("Hasanpaşa", "Sultanbeyli", 40.951, 29.259, "N"),
    ("Mecidiye", "Sultanbeyli", 40.968, 29.278, "N"),
    ("Mehmet Akif", "Sultanbeyli", 40.955, 29.281, "N"),
    ("Mimar Sinan", "Sultanbeyli", 40.948, 29.271, "N"),
    ("Necip Fazıl", "Sultanbeyli", 40.962, 29.256, "N"),
    ("Turgut Reis", "Sultanbeyli", 40.953, 29.266, "N"),
    ("Yavuz Selim", "Sultanbeyli", 40.970, 29.270, "N"),

    # --- Sultangazi ---
    ("Esentepe", "Sultangazi", 41.113, 28.876, "A"),
    ("Uğur Mumcu", "Sultangazi", 41.098, 28.882, "A"),
    ("50. Yıl", "Sultangazi", 41.104, 28.877, "A"),
    ("Cumhuriyet", "Sultangazi", 41.116, 28.867, "A"),
    ("İsmetpaşa", "Sultangazi", 41.109, 28.863, "A"),
    ("Yunus Emre", "Sultangazi", 41.093, 28.874, "A"),
    ("Zübeyde Hanım", "Sultangazi", 41.121, 28.884, "A"),
    ("Malkoçoğlu", "Sultangazi", 41.100, 28.858, "A"),

    # --- Şile ---
    ("Şile Merkez", "Şile", 41.176, 29.613, "N"),
    ("Ağva", "Şile", 41.140, 29.847, "N"),
    ("Kumbaba", "Şile", 41.170, 29.588, "N"),
    ("Balibey", "Şile", 41.174, 29.604, "N"),
    ("Çayırbaşı", "Şile", 41.156, 29.615, "N"),
    ("Doğancılı", "Şile", 41.115, 29.578, "N"),
    ("Ahmetli", "Şile", 41.132, 29.630, "N"),

    # --- Tuzla ---
    ("Aydınlı", "Tuzla", 40.860, 29.318, "N"),
    ("Orhanlı", "Tuzla", 40.898, 29.348, "N"),
    ("Akfırat", "Tuzla", 40.911, 29.360, "N"),
    ("Tepeören", "Tuzla", 40.897, 29.322, "N"),
    ("İçmeler", "Tuzla", 40.833, 29.287, "N"),
    ("Postane", "Tuzla", 40.822, 29.296, "N"),
    ("Şifa", "Tuzla", 40.827, 29.311, "N"),
    ("Yayla", "Tuzla", 40.847, 29.303, "N"),
    ("Aydıntepe", "Tuzla", 40.828, 29.276, "N"),
    ("Tuzla Tersaneler", "Tuzla", 40.808, 29.310, "N"),
    ("Anadolu Yakası OSB", "Tuzla", 40.900, 29.334, "N"),

    # --- Onemli lojistik ve is merkezleri (ilcelerine bagli) ---
    ("Sabiha Gökçen Havalimanı", "Pendik", 40.899, 29.309, "N"),
    ("İkitelli OSB", "Başakşehir", 41.078, 28.795, "A"),
    ("Dudullu OSB", "Ümraniye", 41.006, 29.163, "N"),
    ("Şerifali", "Ümraniye", 41.005, 29.135, "N"),
    ("Perpa Ticaret Merkezi", "Şişli", 41.062, 28.966, "A"),
    ("İstanbul Adliyesi (Çağlayan)", "Kağıthane", 41.073, 28.981, "A"),
    ("Anadolu Adalet Sarayı (Kartal)", "Kartal", 40.902, 29.174, "N"),
    ("İSTOÇ", "Bağcılar", 41.070, 28.816, "A"),
    ("Ataşehir Finans Merkezi", "Ataşehir", 40.988, 29.128, "N"),
    ("Halkalı", "Küçükçekmece", 41.033, 28.786, "A"),
]
