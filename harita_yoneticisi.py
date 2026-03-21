# harita_yoneticisi.py
import pygame
from ayarlar import *

# --- 🌳 PASİF HARİTA NESNELERİ HİYERARŞİSİ (OOP) ---

class Parsel:
    """Temel 'Parsel' sınıfı. Excel kutusu. Miras alınır."""
    def __init__(self, x, y, z, doku_id):
        self.x = x  # Grid koordinat X
        self.y = y  # Grid koordinat Y
        self.z = z  # Grid koordinat Z (Katman)
        self.doku_id = doku_id
        
        # Temel Özellikler
        self.yurunebilir = True
        self.yavaslatma_katsayisi = 1.0  # Normal hız
        self.kazilabilir = False
        self.bogulma_riski = False
        self.hasar_verir = False
        
        # Üzerindeki dinamik nesneler (Oyuncu tuzağı, sürüyü ajanları vb.)
        self.uzerindeki_alet = None
        self.suru_ajanlari = [] # linked list pointerları buraya gelecek

    def render(self, surface, font):
        """Hücreyi ekrana çizer."""
        px_x = self.x * PARSEK_BOYUTU
        px_y = self.y * PARSEK_BOYUTU
        rect = pygame.Rect(px_x, px_y, PARSEK_BOYUTU, PARSEK_BOYUTU)
        pygame.draw.rect(surface, GRI, rect, 1)

        # Sembolü çiz
        sembol = DOKULAR.get(self.doku_id, ' ? ')
        text_surf = font.render(sembol, True, BEYAZ)
        
        # Karakteri hücrenin ortasına hizala
        text_rect = text_surf.get_rect(center=rect.center)
        surface.blit(text_surf, text_rect)

        # Üzerindeki aleti çiz
        if self.uzerindeki_alet:
            self.uzerindeki_alet.render(surface, font)

# --- ALT SINIFLAR (Miras ve Özellik Özelleştirme) ---

class ZeminDuz(Parsel):
    def __init__(self, x, y, z):
        super().__init__(x, y, z, 'ZEMIN_DUZ')

class DuvarKaya(Parsel):
    def __init__(self, x, y, z):
        super().__init__(x, y, z, 'DUVAR_KAYA')
        self.yurunebilir = False

class Dag(Parsel):
    def __init__(self, x, y, z):
        super().__init__(x, y, z, 'DAG')
        self.yavaslatma_katsayisi = 2.5 # Sürüyü çok yavaşlatır

class SuGol(Parsel):
    def __init__(self, x, y, z):
        super().__init__(x, y, z, 'SU_GOL')
        self.bogulma_riski = True
        self.yavaslatma_katsayisi = 1.8 # Suda yürümek/yüzmek yavaştır

# --- OYUNCU ALETLERİ ---

class OyuncuAleti:
    def __init__(self, x, y, z, doku_id):
        self.x = x
        self.y = y
        self.z = z
        self.doku_id = doku_id

    def render(self, surface, font):
        sembol = OYUNCU_ALETLERI.get(self.doku_id, ' ? ')
        px_x = self.x * PARSEK_BOYUTU
        px_y = self.y * PARSEK_BOYUTU
        text_surf = font.render(sembol, True, BEYAZ)
        rect = pygame.Rect(px_x, px_y, PARSEK_BOYUTU, PARSEK_BOYUTU)
        text_rect = text_surf.get_rect(center=rect.center)
        surface.blit(text_surf, text_rect)

# --- 🗄️ HARİTA VERİ YÖNETİCİSİ (Çok Boyutlu Dizi) ---

class HaritaYoneticisi:
    def __init__(self):
        # 5 Katmanlı Evren (Z, Y, X)
        # 3D Dizi: self.map_grid[katman][satir][sutun]
        self.max_katman = 5
        self.map_grid = [[[None for _ in range(HARITA_GENISLIK_PARSEL)] 
                          for _ in range(HARITA_YUKSEKLIK_PARSEL)] 
                         for _ in range(self.max_katman)]
        self.aktif_katman = 0 # Şu an ekranda görünen kat

    def txt_den_yukle(self, klasor_yolu):
        """Örn: bolum_1_kat_0.txt dosyalarını okur, OOP nesnelerini oluşturur."""
        
        # Harita dosyasındaki karakterleri nesne sınıfına eşleyen tablo
        eslesme_tablosu = {
            '.': ZeminDuz,
            '#': DuvarKaya,
            '^': Dag,
            '~': SuGol,
        }

        # Şimdilik sadece Kat 0 ve Kat 1'i yükleyelim (Örnek olsun diye)
        for kat in range(2): 
            dosya_adi = f"{klasor_yolu}/bolum_1_kat_{kat}.txt"
            try:
                with open(dosya_adi, 'r') as f:
                    satirlar = f.readlines()
                    
                    for y, satir in enumerate(satirlar):
                        satir = satir.strip() # Satır sonu karakterlerini temizle
                        if y >= HARITA_YUKSEKLIK_PARSEL: break

                        for x, char in enumerate(satir):
                            if x >= HARITA_GENISLIK_PARSEL: break
                            
                            # Karakteri sınıf ile eşleştir
                            parsel_sinifi = eslesme_tablosu.get(char, ZeminDuz)
                            
                            # OOP Nesnesini oluştur ve 3D diziye koy
                            self.map_grid[kat][y][x] = parsel_sinifi(x, y, kat)
            
            except FileNotFoundError:
                print(f"Hata: {dosya_adi} bulunamadı. Boş katman oluşturuldu.")
                # Eğer dosya yoksa varsayılan olarak her yeri düz zemin yap
                for y in range(HARITA_YUKSEKLIK_PARSEL):
                    for x in range(HARITA_GENISLIK_PARSEL):
                        self.map_grid[kat][y][x] = ZeminDuz(x, y, kat)

    def aktif_katmani_degistir(self, yeni_kat):
        """Mini-mapten tıklayınca veya ajan düşünce kat değiştirir."""
        if 0 <= yeni_kat < self.max_katman:
            self.aktif_katman = yeni_kat

    def render(self, surface, font):
        """Sadece ekranda olan aktif katmanı çizer."""
        surface.fill(SIYAH) # Ekranı temizle
        katman = self.map_grid[self.aktif_katman]
        
        for satir in katman:
            for parsel in satir:
                parsel.render(surface, font)