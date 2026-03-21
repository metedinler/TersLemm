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

# --- RENKLER (ASCII Görünüm İçin) ---
SIYAH = (0, 0, 0)
BEYAZ = (255, 255, 255)
GRI = (100, 100, 100)
KIRMIZI = (200, 50, 50)
MAVI = (50, 50, 200)
YESIL = (50, 200, 50)
KAHVERENGI = (139, 69, 19)

# --- HARİTA DOKULARI VE NESNE EMOJİLERİ ---
# Windows ortamında standart Truetype fontlar emojileri destekler.
# Eğer özel pixel font kullanırsan bu karakterleri o fontta tasarlaman gerekir.
DOKULAR = {
    'ZEMIN_DUZ': ' . ',  # Yürünür
    'DUVAR_KAYA': ' 🧱 ', # Yürünmez
    'SU_GOL': ' 💧 ',    # Boğulur
    'DAG': ' ⛰️ ',     # Yavaşlatır
    'ORMAN': ' 🌳 ',    # Görüşü azaltır
    'KAZILABILIR': ' 🤎 ', # Oyuncu delik açabilir
    'CIKIS_DOGRU': ' ✅ ', # Kazanma kapısı
    'CIKIS_SAHTE': ' ❌ ', # Kaybetme kapısı
}

OYUNCU_ALETLERI = {
    'MANCINIK': ' 🏹 ',
    'TAS': ' 💎 ',
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