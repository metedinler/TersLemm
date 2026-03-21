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
        self.maks_kapasite = 50
        self.mevcut_kapasite = 50
        self.gizlilik_carpani = 0.5
        self.zemin_katsayisi = 1.0

    def kullan(self):
        if self.mevcut_kapasite > 0:
            self.mevcut_kapasite -= 0.3 * self.zemin_katsayisi
            return True
        return False

    def render(self, surface, font):
        sembol = OYUNCU_ALETLERI.get(self.doku_id, ' ? ')
        px_x = self.x * PARSEK_BOYUTU
        px_y = self.y * PARSEK_BOYUTU
        text_surf = font.render(sembol, True, BEYAZ)
        rect = pygame.Rect(px_x, px_y, PARSEK_BOYUTU, PARSEK_BOYUTU)
        text_rect = text_surf.get_rect(center=rect.center)
        surface.blit(text_surf, text_rect)

class Mancinik(OyuncuAleti):
    def __init__(self, x, y, z, zemin_tipi):
        super().__init__(x, y, z, 'MANCINIK')
        if zemin_tipi == 'sert':
            self.maks_kapasite = 50
        else:
            self.maks_kapasite = 20
        self.mevcut_kapasite = self.maks_kapasite
        self.zemin_katsayisi = 1.0 if zemin_tipi == 'sert' else 2.5

    def etki_uygula(self, ajanlar):
        """Yakındaki ajanları fırlatır (yön değiştirir ve hızlandırır)."""
        if not self.kullan():
            return
        for ajan in ajanlar:
            if abs(ajan.x - self.x) <= 1 and abs(ajan.y - self.y) <= 1:
                # Rastgele yön değiştir
                import random
                ajan.yon = random.choice(['yukari', 'asagi', 'sol', 'sag'])
                ajan.hiz *= 2  # Hızlandır

class SendeletmeTasi(OyuncuAleti):
    def __init__(self, x, y, z):
        super().__init__(x, y, z, 'TAS')
        self.maks_kapasite = 5
        self.mevcut_kapasite = 5

    def etki_uygula(self, ajanlar):
        """Ajanları sendeletir, yön değiştirir."""
        if not self.kullan():
            return
        for ajan in ajanlar:
            if abs(ajan.x - self.x) <= 1 and abs(ajan.y - self.y) <= 1:
                import random
                ajan.yon = random.choice(['yukari', 'asagi', 'sol', 'sag'])
                ajan.hiz *= 0.5  # Yavaşlat

class GizliCukur(OyuncuAleti):
    def __init__(self, x, y, z):
        super().__init__(x, y, z, 'CIKIS_SAHTE')  # Sahte çıkış gibi
        self.maks_kapasite = 1  # Tek seferlik

    def etki_uygula(self, ajanlar):
        """Ajanları düşürür, öldürür."""
        if not self.kullan():
            return
        for ajan in ajanlar:
            if ajan.x == self.x and ajan.y == self.y:
                ajan.hayatta = False  # Öldür

class KiymaMakinesi(OyuncuAleti):
    def __init__(self, x, y, z):
        super().__init__(x, y, z, 'CIKIS_DOGRU')  # Tehlikeli çıkış
        self.maks_kapasite = 100  # Sürekli

    def etki_uygula(self, ajanlar):
        """Ajanları öldürür."""
        if not self.kullan():
            return
        for ajan in ajanlar:
            if ajan.x == self.x and ajan.y == self.y:
                ajan.hayatta = False  # Öldür

class Yonlendirici(OyuncuAleti):
    def __init__(self, x, y, z):
        super().__init__(x, y, z, 'ORMAN')  # Orman gibi
        self.maks_kapasite = 20

    def etki_uygula(self, ajanlar):
        """Ajanların yönünü değiştirir."""
        if not self.kullan():
            return
        for ajan in ajanlar:
            if abs(ajan.x - self.x) <= 1 and abs(ajan.y - self.y) <= 1:
                # Belirli bir yöne yönlendir, örneğin sağa
                ajan.yon = 'sag'

class Ayna(OyuncuAleti):
    def __init__(self, x, y, z):
        super().__init__(x, y, z, 'AYNA')  # Ayna emoji
        self.maks_kapasite = 15

    def etki_uygula(self, ajanlar):
        """Ajanların yönünü ters çevirir."""
        if not self.kullan():
            return
        for ajan in ajanlar:
            if abs(ajan.x - self.x) <= 1 and abs(ajan.y - self.y) <= 1:
                # Yönü ters çevir (180 derece)
                if ajan.yon == 'sag':
                    ajan.yon = 'sol'
                elif ajan.yon == 'sol':
                    ajan.yon = 'sag'
                elif ajan.yon == 'yukari':
                    ajan.yon = 'asagi'
                elif ajan.yon == 'asagi':
                    ajan.yon = 'yukari'
                ajan.duygular['korku'] += 0.1  # Korku artır

class Bariyer(OyuncuAleti):
    def __init__(self, x, y, z):
        super().__init__(x, y, z, 'BARIYER')  # Bariyer emoji
        self.maks_kapasite = 30

    def etki_uygula(self, ajanlar):
        """Engel koyar, ajanları yavaşlatır."""
        if not self.kullan():
            return
        # Bariyer yerleştirildiğinde parseli engel yap
        parsel = self.harita_yon.map_grid[self.z][self.y][self.x]
        if parsel:
            parsel.yurunebilir = False
            parsel.doku_id = 'BARIYER'
        # Yakındaki ajanları yavaşlat
        for ajan in ajanlar:
            if abs(ajan.x - self.x) <= 1 and abs(ajan.y - self.y) <= 1:
                ajan.hiz *= 0.8  # Yavaşlat
                ajan.duygular['suphe'] += 0.1

class Ates(OyuncuAleti):
    def __init__(self, x, y, z):
        super().__init__(x, y, z, 'ATES')  # Ateş emoji
        self.maks_kapasite = 10

    def etki_uygula(self, ajanlar):
        """Ajanları yakar, hasar verir ve hızlandırır."""
        if not self.kullan():
            return
        for ajan in ajanlar:
            if abs(ajan.x - self.x) <= 1 and abs(ajan.y - self.y) <= 1:
                ajan.can -= 20  # Hasar ver
                ajan.hiz *= 1.2  # Hızlandır
                ajan.duygular['korku'] += 0.2  # Korku artır

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
            'X': lambda x, y, z: Parsel(x, y, z, 'CIKIS_DOGRU'),  # Basit sınıf
            'O': lambda x, y, z: Parsel(x, y, z, 'CIKIS_SAHTE'),
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
                if parsel:
                    parsel.render(surface, font)

    def arac_etkilerini_uygula(self, ajanlar):
        """Tüm araçların etkilerini ajanlara uygular."""
        katman = self.map_grid[self.aktif_katman]
        for satir in katman:
            for parsel in satir:
                if parsel and parsel.uzerindeki_alet and hasattr(parsel.uzerindeki_alet, 'etki_uygula'):
                    parsel.uzerindeki_alet.etki_uygula(ajanlar)