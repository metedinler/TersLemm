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
        self.derinlik = 0  # Su türleri için derinlik
        
        # Üzerindeki dinamik nesneler (Oyuncu tuzağı, sürüyü ajanları vb.)
        self.uzerindeki_alet = None
        self.suru_ajanlari = [] # linked list pointerları buraya gelecek

    def render(self, surface, font):
        """Hücreyi ekrana çizer."""
        px_x = self.x * PARSEK_BOYUTU
        px_y = self.y * PARSEK_BOYUTU
        rect = pygame.Rect(px_x, px_y, PARSEK_BOYUTU, PARSEK_BOYUTU)
        
        # Renk belirle
        renk = RENKLER.get(self.doku_id, GRI)
        if self.doku_id in ['SU_GOL', 'DENIZ']:
            # Derinliğe göre mavi tonu
            if self.derinlik <= 5:
                renk = (100, 149, 237)  # Açık mavi
            elif self.derinlik <= 10:
                renk = (0, 0, 139)      # Koyu mavi
            else:
                renk = (0, 0, 50)       # Çok koyu mavi
        
        pygame.draw.rect(surface, renk, rect, 1)

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

class Deniz(Parsel):
    def __init__(self, x, y, z):
        super().__init__(x, y, z, 'DENIZ')
        self.bogulma_riski = True
        self.yavaslatma_katsayisi = 2.0 # Derin su, daha yavaş

class SikiOrman(Parsel):
    def __init__(self, x, y, z):
        super().__init__(x, y, z, 'SIKI_ORMAN')
        self.yavaslatma_katsayisi = 2.0 # Çok yavaş

class Yol(Parsel):
    def __init__(self, x, y, z):
        super().__init__(x, y, z, 'YOL')
        self.yavaslatma_katsayisi = 0.8 # Yol, hızlı

class TasDuvar(Parsel):
    def __init__(self, x, y, z):
        super().__init__(x, y, z, 'TAS_DUVAR')
        self.yurunebilir = False

class Ova(Parsel):
    def __init__(self, x, y, z):
        super().__init__(x, y, z, 'OVA')
        # Normal

class Plato(Parsel):
    def __init__(self, x, y, z):
        super().__init__(x, y, z, 'PLATO')
        self.yavaslatma_katsayisi = 1.2 # Yüksek yer, biraz yavaş

class DikDag(Parsel):
    def __init__(self, x, y, z):
        super().__init__(x, y, z, 'DIK_DAG')
        self.yurunebilir = False  # Tırmanılmaz

class Calilik(Parsel):
    def __init__(self, x, y, z):
        super().__init__(x, y, z, 'CALILIK')
        self.yavaslatma_katsayisi = 1.3 # Çalılık, yavaş

class Taslik(Parsel):
    def __init__(self, x, y, z):
        super().__init__(x, y, z, 'TASLIK')
        self.yavaslatma_katsayisi = 1.4 # Taşlık, yavaş

class Col(Parsel):
    def __init__(self, x, y, z):
        super().__init__(x, y, z, 'COL')
        self.yavaslatma_katsayisi = 1.6 # Çöl, çok yavaş

# --- OYUNCU ALETLERİ ---

class OyuncuAleti:
    def __init__(self, x, y, z, doku_id, arac_turu):
        self.x = x
        self.y = y
        self.z = z
        self.doku_id = doku_id
        self.arac_turu = arac_turu
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
        sembol = str(self.arac_turu)
        px_x = self.x * PARSEK_BOYUTU
        px_y = self.y * PARSEK_BOYUTU
        text_surf = font.render(sembol, True, BEYAZ)
        rect = pygame.Rect(px_x, px_y, PARSEK_BOYUTU, PARSEK_BOYUTU)
        text_rect = text_surf.get_rect(center=rect.center)
        surface.blit(text_surf, text_rect)

class Mancinik(OyuncuAleti):
    def __init__(self, x, y, z, zemin_tipi, arac_turu):
        super().__init__(x, y, z, 'MANCINIK', arac_turu)
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
            if abs(ajan.x - self.x) <= 1 and abs(ajan.y - self.y) <= 1 and abs(ajan.z - self.z) <= 1:
                # Rastgele yön değiştir
                import random
                ajan.yon = random.choice(['yukari', 'asagi', 'sol', 'sag'])
                ajan.hiz *= 2  # Hızlandır

class SendeletmeTasi(OyuncuAleti):
    def __init__(self, x, y, z, arac_turu):
        super().__init__(x, y, z, 'TAS', arac_turu)
        self.maks_kapasite = 5
        self.mevcut_kapasite = 5

    def etki_uygula(self, ajanlar):
        """Ajanları sendeletir, yön değiştirir."""
        if not self.kullan():
            return
        for ajan in ajanlar:
            if abs(ajan.x - self.x) <= 1 and abs(ajan.y - self.y) <= 1 and abs(ajan.z - self.z) <= 1:
                import random
                ajan.yon = random.choice(['yukari', 'asagi', 'sol', 'sag'])
                ajan.hiz *= 0.5  # Yavaşlat

class GizliCukur(OyuncuAleti):
    def __init__(self, x, y, z, arac_turu):
        super().__init__(x, y, z, 'CIKIS_SAHTE', arac_turu)  # Sahte çıkış gibi
        self.maks_kapasite = 1  # Tek seferlik

    def etki_uygula(self, ajanlar):
        """Ajanları düşürür, öldürür."""
        if not self.kullan():
            return
        for ajan in ajanlar:
            if ajan.x == self.x and ajan.y == self.y:
                ajan.hayatta = False  # Öldür

class KiymaMakinesi(OyuncuAleti):
    def __init__(self, x, y, z, arac_turu):
        super().__init__(x, y, z, 'CIKIS_DOGRU', arac_turu)  # Tehlikeli çıkış
        self.maks_kapasite = 100  # Sürekli

    def etki_uygula(self, ajanlar):
        """Ajanları öldürür."""
        if not self.kullan():
            return
        for ajan in ajanlar:
            if ajan.x == self.x and ajan.y == self.y:
                ajan.hayatta = False  # Öldür

class Yonlendirici(OyuncuAleti):
    def __init__(self, x, y, z, arac_turu):
        super().__init__(x, y, z, 'ORMAN', arac_turu)  # Orman gibi
        self.maks_kapasite = 20

    def etki_uygula(self, ajanlar):
        """Ajanların yönünü değiştirir."""
        if not self.kullan():
            return
        for ajan in ajanlar:
            if abs(ajan.x - self.x) <= 1 and abs(ajan.y - self.y) <= 1 and abs(ajan.z - self.z) <= 1:
                # Belirli bir yöne yönlendir, örneğin sağa
                ajan.yon = 'sag'

class Ayna(OyuncuAleti):
    def __init__(self, x, y, z, arac_turu):
        super().__init__(x, y, z, 'AYNA', arac_turu)  # Ayna emoji
        self.maks_kapasite = 15

    def etki_uygula(self, ajanlar):
        """Ajanların yönünü ters çevirir."""
        if not self.kullan():
            return
        for ajan in ajanlar:
            if abs(ajan.x - self.x) <= 1 and abs(ajan.y - self.y) <= 1 and abs(ajan.z - self.z) <= 1:
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
    def __init__(self, x, y, z, arac_turu):
        super().__init__(x, y, z, 'BARIYER', arac_turu)  # Bariyer emoji
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
            if abs(ajan.x - self.x) <= 1 and abs(ajan.y - self.y) <= 1 and abs(ajan.z - self.z) <= 1:
                ajan.hiz *= 0.8  # Yavaşlat
                ajan.duygular['suphe'] += 0.1

class Ates(OyuncuAleti):
    def __init__(self, x, y, z, arac_turu):
        super().__init__(x, y, z, 'ATES', arac_turu)  # Ateş emoji
        self.maks_kapasite = 10

    def etki_uygula(self, ajanlar):
        """Ajanları yakar, hasar verir ve hızlandırır."""
        if not self.kullan():
            return
        for ajan in ajanlar:
            if abs(ajan.x - self.x) <= 1 and abs(ajan.y - self.y) <= 1 and abs(ajan.z - self.z) <= 1:
                ajan.can -= 20  # Hasar ver
                ajan.hiz *= 1.2  # Hızlandır
                ajan.duygular['korku'] += 0.2

class CikisOku(OyuncuAleti):
    def __init__(self, x, y, z, arac_turu):
        super().__init__(x, y, z, 'CIKIS_OKU', arac_turu)  # Çıkış oku emoji
        self.maks_kapasite = 1  # Sadece bir çıkış

    def etki_uygula(self, ajanlar):
        """Çıkış oku, etki yok, sadece işaret."""
        pass  # Oyun başlayınca kapıya dönüşür  # Korku artır
class SahteYol(OyuncuAleti):
    def __init__(self, x, y, z, arac_turu):
        super().__init__(x, y, z, 'SAHTE_YOL', arac_turu)  # Sahte yol emoji
        self.maks_kapasite = 50  # Sürekli

    def etki_uygula(self, ajanlar):
        """Sahte yol, etki yok, sadece yol gibi davranır."""
        pass  # Lemler yolları tercih eder
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
        
        # Rastgele giriş/çıkış
        import random
        self.giris_katman = random.randint(0, self.max_katman - 1)
        self.cikis_katman = random.randint(0, self.max_katman - 1)
        self.giris_x, self.giris_y = 0, random.randint(0, HARITA_YUKSEKLIK_PARSEL - 1)
        self.cikis_x, self.cikis_y = HARITA_GENISLIK_PARSEL - 1, random.randint(0, HARITA_YUKSEKLIK_PARSEL - 1)
        
        # Haritayı rastgele oluştur
        self.rastgele_harita_olustur()

    def rastgele_harita_olustur(self):
        """Rastgele harita oluştur, doğal ortamlar ve yollarla."""
        import random
        
        # Parsel türleri listesi (ağırlıklı)
        parsel_turleri = [
            ('ZeminDuz', 30), ('Dag', 10), ('SuGol', 5), ('Deniz', 3), ('SikiOrman', 8),
            ('Yol', 5), ('TasDuvar', 5), ('Ova', 15), ('Plato', 5), ('DikDag', 3),
            ('Calilik', 5), ('Taslik', 5), ('Col', 3)
        ]
        
        for kat in range(self.max_katman):
            for y in range(HARITA_YUKSEKLIK_PARSEL):
                for x in range(HARITA_GENISLIK_PARSEL):
                    # Rastgele tür seç (ağırlıklı)
                    toplam_agirlik = sum(agirlik for _, agirlik in parsel_turleri)
                    rastgele = random.randint(1, toplam_agirlik)
                    kumulatif = 0
                    secilen_tur = 'ZeminDuz'  # Varsayılan
                    for tur, agirlik in parsel_turleri:
                        kumulatif += agirlik
                        if rastgele <= kumulatif:
                            secilen_tur = tur
                            break
                    
                    # Sınıf eşleşmesi
                    sinif_eslesme = {
                        'ZeminDuz': ZeminDuz, 'Dag': Dag, 'SuGol': SuGol, 'Deniz': Deniz,
                        'SikiOrman': SikiOrman, 'Yol': Yol, 'TasDuvar': TasDuvar,
                        'Ova': Ova, 'Plato': Plato, 'DikDag': DikDag,
                        'Calilik': Calilik, 'Taslik': Taslik, 'Col': Col
                    }
                    parsel_sinifi = sinif_eslesme.get(secilen_tur, ZeminDuz)
                    parsel = parsel_sinifi(x, y, kat)
                    
                    # Su türleri için derinlik ata
                    if secilen_tur in ['SuGol', 'Deniz']:
                        import random
                        parsel.derinlik = random.randint(1, 15)  # 1-5 az, 6-10 orta, 11+ çok
                    
                    self.map_grid[kat][y][x] = parsel
            
            # Yol oluştur: Girişten çıkışa basit yol
            if kat == self.giris_katman:
                # Yatay yol çiz
                for x in range(self.giris_x, self.cikis_x + 1):
                    if 0 <= x < HARITA_GENISLIK_PARSEL and 0 <= self.giris_y < HARITA_YUKSEKLIK_PARSEL:
                        self.map_grid[kat][self.giris_y][x] = Yol(x, self.giris_y, kat)
            elif kat == self.cikis_katman:
                # Çıkış katmanında da yol
                for x in range(self.giris_x, self.cikis_x + 1):
                    if 0 <= x < HARITA_GENISLIK_PARSEL and 0 <= self.cikis_y < HARITA_YUKSEKLIK_PARSEL:
                        self.map_grid[kat][self.cikis_y][x] = Yol(x, self.cikis_y, kat)
        
        # Giriş ve çıkış ayarla
        if self.map_grid[self.giris_katman][self.giris_y][self.giris_x]:
            self.map_grid[self.giris_katman][self.giris_y][self.giris_x].doku_id = 'CIKIS_DOGRU'
        if self.map_grid[self.cikis_katman][self.cikis_y][self.cikis_x]:
            self.map_grid[self.cikis_katman][self.cikis_y][self.cikis_x].doku_id = 'CIKIS_SAHTE'

    def cikis_oklarini_kapiya_cevir(self):
        """Düzenleme sonrası çıkış oklarını kapıya çevir."""
        for kat in range(self.max_katman):
            for y in range(HARITA_YUKSEKLIK_PARSEL):
                for x in range(HARITA_GENISLIK_PARSEL):
                    parsel = self.map_grid[kat][y][x]
                    if parsel.uzerindeki_alet and isinstance(parsel.uzerindeki_alet, CikisOku):
                        parsel.doku_id = 'CIKIS_KAPI'
                        parsel.uzerindeki_alet = None  # Araç kaldır, parsel çıkış olsun
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
        surface.fill((0, 0, 0)) # Ekranı temizle
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