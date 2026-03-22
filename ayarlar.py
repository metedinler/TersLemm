# ayarlar.py
import pygame

# --- EKRAN VE PARSEK AYARLARI ---
# Senin tanımınla: İki birim arası parsek (hücre boyutu)
PARSEK_BOYUTU = 32  # Her bir 'parsel' 32x32 piksel olacak. Excel kutusu gibi.
HARITA_GENISLIK_PARSEL = 40
HARITA_YUKSEKLIK_PARSEL = 25
HARITA_ALAN_YUKSEKLIK = HARITA_YUKSEKLIK_PARSEL * PARSEK_BOYUTU
# Iki satirlik arac/kisayol metni tasmasin diye durum cubugu yuksekligi artirildi.
DURUM_CUBUGU_YUKSEKLIK = 92
EKRAN_GENISLIK = HARITA_GENISLIK_PARSEL * PARSEK_BOYUTU
EKRAN_YUKSEKLIK = HARITA_ALAN_YUKSEKLIK + DURUM_CUBUGU_YUKSEKLIK
FPS = 60

# --- OYUN PARAMETRELERİ (Temel Değerler) ---
# Zorluk seçilerek bu değerler katsayı ile çarpılır
AJAN_SAYISI_TEMEL = 50          # Temel lem sayısı
AJAN_HIZI = 0.9                 # Çok yavaş hareket için
AJAN_KARAR_HZ_TEMEL = 5         # Temel karar/hareket sayısı (saniyede)
OGRENME_TIK_ARALIGI_TEMEL = FPS * 9  # Temel öğrenme güncellemesi aralığı
OGRENME_MIKTARI_TEMEL = 0.10    # Temel öğrenme miktarı
CIKIS_BILGISI_ARTIS_TEMEL = 1   # Temel çıkış öğrenme hızı
SURU_BASLANGIC_BEKLEME_TIK_TEMEL = FPS * 4  # Temel başlangıç bekleme
LOG_KARE_ARALIGI = 15           # Kaç karede bir tüm ajan durumunu logla

# --- ZORLUK KATSAYILARI ---
# Her zorluk seviyesinde temel parametreler bu katsayılarla çarpılır
ZORLUK_KATSAYILARI = {
    'Kolay': {
        'ajan_sayisi_x': 0.7,           # 50 * 0.7 = 35
        'karar_hz_x': 0.2,              # 5 * 0.2 = 1
        'ogrenme_aralik_x': 1.33,       # 9 / 1.33 ≈ 6.75
        'ogrenme_miktari_x': 0.2,       # 0.10 * 0.2 = 0.02
        'cikis_artis_x': 0.04,          # 1 * 0.04 = 0.04
        'baslangic_bekleme_x': 1.25,    # 4 * 1.25 = 5
    },
    'Orta': {
        'ajan_sayisi_x': 1.0,           # 50 * 1.0 = 50
        'karar_hz_x': 0.4,              # 5 * 0.4 = 2
        'ogrenme_aralik_x': 1.5,        # 9 / 1.5 = 6
        'ogrenme_miktari_x': 0.3,       # 0.10 * 0.3 = 0.03
        'cikis_artis_x': 0.06,          # 1 * 0.06 = 0.06
        'baslangic_bekleme_x': 1.0,     # 4 * 1.0 = 4
    },
    'Zor': {
        'ajan_sayisi_x': 1.2,           # 50 * 1.2 = 60
        'karar_hz_x': 0.6,              # 5 * 0.6 = 3
        'ogrenme_aralik_x': 2.25,       # 9 / 2.25 = 4
        'ogrenme_miktari_x': 0.5,       # 0.10 * 0.5 = 0.05
        'cikis_artis_x': 0.08,          # 1 * 0.08 = 0.08
        'baslangic_bekleme_x': 0.5,     # 4 * 0.5 = 2
    },
}

# --- ETKİ ALANI VE KAPSAMA HEDEFİ ---
KATMAN_SAYISI = 5
ETKI_YARICAPI = 2  # ±2 => 5x5x5
HARITA_TOPLAM_PARSEL = HARITA_GENISLIK_PARSEL * HARITA_YUKSEKLIK_PARSEL * KATMAN_SAYISI
HEDEF_ETKI_KAPSAM_ORANI = 0.55
HEDEF_ETKI_PARSEL = int(HARITA_TOPLAM_PARSEL * HEDEF_ETKI_KAPSAM_ORANI)
TEK_ARAC_NOMINAL_ETKI = (2 * ETKI_YARICAPI + 1) ** 3

# --- ARAÇ SAYILARI ---
MANCINIK_SAYISI = 50
AYNA_SAYISI = 60
BARIYER_SAYISI = 100
ATES_SAYISI = 45
SAHTE_YOL_SAYISI = 50
CIKIS_OKU_SAYISI = 1
SENDELETME_TASI_SAYISI = 30
GIZLI_CUKUR_SAYISI = 20
KIYMA_MAKINESI_SAYISI = 10
YONLENDIRICI_SAYISI = 50

TOPLAM_ETKI_ARACI = (
    MANCINIK_SAYISI + AYNA_SAYISI + BARIYER_SAYISI + ATES_SAYISI +
    SAHTE_YOL_SAYISI + SENDELETME_TASI_SAYISI + GIZLI_CUKUR_SAYISI +
    KIYMA_MAKINESI_SAYISI + YONLENDIRICI_SAYISI
)
NOMINAL_TOPLAM_ETKI = TOPLAM_ETKI_ARACI * TEK_ARAC_NOMINAL_ETKI

# --- PARSEL RENKLERİ ---
RENKLER = {
    'ZEMIN_DUZ': (128, 128, 128),  # Gri
    'DUVAR_KAYA': (64, 64, 64),    # Koyu gri
    'SU_GOL': (100, 149, 237),     # Açık mavi (derinliğe göre değişir)
    'DENIZ': (0, 0, 139),          # Koyu mavi (derinliğe göre)
    'DAG': (139, 69, 19),          # Kahve
    'DIK_DAG': (105, 105, 105),    # Gri
    'ORMAN': (34, 139, 34),        # Yeşil
    'SIKI_ORMAN': (0, 100, 0),     # Koyu yeşil
    'YOL': (139, 69, 19),          # Kahve
    'TAS_DUVAR': (64, 64, 64),     # Koyu gri
    'OVA': (144, 238, 144),        # Açık yeşil
    'PLATO': (169, 169, 169),      # Gri
    'CALILIK': (173, 255, 47),     # Açık yeşil
    'TASLIK': (128, 128, 128),     # Gri
    'COL': (255, 215, 0),          # Sarı (kum)
    'KAZILABILIR': (160, 82, 45),  # Kahve
    'CIKIS_DOGRU': (0, 255, 0),    # Yeşil
    'CIKIS_SAHTE': (255, 0, 0),    # Kırmızı
    'GIRIS': (255, 255, 255),      # Beyaz giriş noktası
    'CIKIS_KAPI': (0, 128, 0),     # Koyu yeşil
    'CIKIS_OKU': (255, 255, 255),  # Beyaz
    'SAHTE_YOL': (139, 69, 19),    # Kahve
    'MERDIVEN_YUKARI': (180, 220, 255),  # Açık mavi
    'MERDIVEN_ASAGI': (140, 190, 235),   # Mavi
}

# Ek renk sabitleri
YESIL = (0, 255, 0)
KIRMIZI = (255, 0, 0)
GRI = (128, 128, 128)
BEYAZ = (255, 255, 255)
KOYU_GRI = (35, 35, 35)

# Windows ortamında standart Truetype fontlar emojileri destekler.
# Eğer özel pixel font kullanırsan bu karakterleri o fontta tasarlaman gerekir.
DOKULAR = {
    'ZEMIN_DUZ': ' . ',  # Yürünür
    'DUVAR_KAYA': ' 🧱 ', # Yürünmez
    'SU_GOL': ' 💧 ',    # Boğulur
    'DENIZ': ' 🌊 ',     # Boğulur, daha derin
    'DAG': ' ⛰️ ',     # Yavaşlatır
    'DIK_DAG': ' 🏔️ ',  # Çok yavaşlatır, tırmanılmaz
    'ORMAN': ' 🌳 ',    # Görüşü azaltır, yavaşlatır
    'SIKI_ORMAN': ' 🌲 ', # Daha yavaş, görüş az
    'YOL': ' 🛤️ ',      # Hızlı yürünür
    'TAS_DUVAR': ' 🧱 ', # Yürünmez
    'OVA': ' 🌾 ',      # Normal
    'PLATO': ' 🏞️ ',    # Yüksek, yavaş
    'CALILIK': ' 🌿 ',   # Yavaşlatır
    'TASLIK': ' 🪨 ',   # Yavaşlatır
    'COL': ' 🏜️ ',     # Çok yavaş, susuz
    'KAZILABILIR': ' 🤎 ', # Oyuncu delik açabilir
    'CIKIS_DOGRU': ' ✅ ', # Kazanma kapısı
    'CIKIS_SAHTE': ' ❌ ', # Kaybetme kapısı
    'GIRIS': ' ⬅️ ',      # Başlangıç noktası
    'CIKIS_KAPI': ' 🚪 ', # Ana çıkış kapısı
    'CIKIS_OKU': ' ➡️ ', # Düzenleme için çıkış oku
    'SAHTE_YOL': ' 🛣️ ', # Oyuncu yapar, lemler tercih eder
    'MERDIVEN_YUKARI': ' ⬆️ ', # Üst katmana çıkış
    'MERDIVEN_ASAGI': ' ⬇️ ', # Alt katmana iniş
}

OYUNCU_ALETLERI = {
    'MANCINIK': ' 🏹 ',
    'TAS': ' 💎 ',
    'SAHTE_YOL': ' 🛣️ ',
}

SURU_DUYUMLAR = {
    'SAKIN': ' o ',
    'LIDER': ' \U0001f451 ',
    'KORKU': ' \U0001f631 ',
    'MERAK': ' \U0001f914 ',
    'SUPHE': ' \U0001f928 ',
    'GAZI': ' \u26a1 ',   # Faz 8: gazi mod sembol\u00fc
}

# Ses ayarları
SES_ACIK = True
MUZIK_ACIK = True
MUZIK_DOSYASI = "sesler/arka_plan.sid"  # .sid uzantılı, ama pygame için .wav/.mp3'ye dönüştürülmeli