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
MANCINIK_SAYISI = 20  # Artırıldı
AYNA_SAYISI = 20      # Artırıldı
BARIYER_SAYISI = 30   # Artırıldı
ATES_SAYISI = 20      # Artırıldı
SAHTE_YOL_SAYISI = 15 # Yeni araç
CIKIS_OKU_SAYISI = 1

# --- RENK TANIMLARI ---
SIYAH = (0, 0, 0)
BEYAZ = (255, 255, 255)
GRI = (128, 128, 128)
KIRMIZI = (255, 0, 0)
YESIL = (0, 255, 0)
MAVI = (0, 0, 255)
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