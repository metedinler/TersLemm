# ayarlar.py
import pygame

# --- EKRAN VE PARSEK AYARLARI ---
# Senin tanımınla: İki birim arası parsek (hücre boyutu)
PARSEK_BOYUTU = 32  # Her bir 'parsel' 32x32 piksel olacak. Excel kutusu gibi.
HARITA_GENISLIK_PARSEL = 40
HARITA_YUKSEKLIK_PARSEL = 25
EKRAN_GENISLIK = HARITA_GENISLIK_PARSEL * PARSEK_BOYUTU
EKRAN_YUKSEKLIK = HARITA_YUKSEKLIK_PARSEL * PARSEK_BOYUTU
FPS = 60

# --- OYUN PARAMETRELERİ ---
AJAN_SAYISI = 50  # Lem sayısı
AJAN_HIZI = 0.5   # Çok yavaş hareket için

# --- ARAÇ SAYILARI ---
MANCINIK_SAYISI = 50  # Artırıldı
AYNA_SAYISI = 40      # Artırıldı
BARIYER_SAYISI = 60   # Artırıldı
ATES_SAYISI = 40      # Artırıldı
SAHTE_YOL_SAYISI = 30 # Yeni araç
CIKIS_OKU_SAYISI = 1
SENDELETME_TASI_SAYISI = 30
GIZLI_CUKUR_SAYISI = 20
KIYMA_MAKINESI_SAYISI = 10
YONLENDIRICI_SAYISI = 50

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
    'CIKIS_KAPI': (0, 128, 0),     # Koyu yeşil
    'CIKIS_OKU': (255, 255, 255),  # Beyaz
    'SAHTE_YOL': (139, 69, 19),    # Kahve
}

# Ek renk sabitleri
YESIL = (0, 255, 0)
KIRMIZI = (255, 0, 0)
GRI = (128, 128, 128)
BEYAZ = (255, 255, 255)

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
    'CIKIS_KAPI': ' 🚪 ', # Ana çıkış kapısı
    'CIKIS_OKU': ' ➡️ ', # Düzenleme için çıkış oku
    'SAHTE_YOL': ' 🛣️ ', # Oyuncu yapar, lemler tercih eder
}

OYUNCU_ALETLERI = {
    'MANCINIK': ' 🏹 ',
    'TAS': ' 💎 ',
    'SAHTE_YOL': ' 🛣️ ',
}

SURU_DUYUMLAR = {
    'SAKIN': ' o ',
    'LIDER': ' 👑 ',
    'KORKU': ' 😱 ',
    'MERAK': ' 🤔 ',
    'SUPHE': ' 🤨 ',
}

# Ses ayarları
SES_ACIK = True
MUZIK_ACIK = True
MUZIK_DOSYASI = "sesler/arka_plan.sid"  # .sid uzantılı, ama pygame için .wav/.mp3'ye dönüştürülmeli