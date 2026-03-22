# harita_yoneticisi.py
import pygame
import random
import os
import json
from datetime import datetime
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
    # Faz 5: Mevcut 10 arac için duygu + hormon etki tablosu
    ETKI_TABLOSU = {
        'Mancinik': {
            'duygu': {'korku': 12.0, 'suphe': 4.0, 'merak': -2.0},
            'hormon': {'adrenalin': 8.0, 'kortizol': 5.0, 'husran': 2.0}
        },
        'Ayna': {
            'duygu': {'korku': 6.0, 'suphe': 8.0, 'merak': 0.0},
            'hormon': {'adrenalin': 3.0, 'kortizol': 4.0, 'husran': 1.0}
        },
        'Bariyer': {
            'duygu': {'korku': 2.0, 'suphe': 10.0, 'merak': -2.0},
            'hormon': {'kortizol': 6.0, 'husran': 3.0}
        },
        'Ates': {
            'duygu': {'korku': 18.0, 'suphe': 6.0, 'merak': -4.0},
            'hormon': {'adrenalin': 10.0, 'kortizol': 8.0, 'husran': 4.0}
        },
        'CikisOku': {
            'duygu': {'korku': -3.0, 'suphe': -2.0, 'merak': 6.0},
            'hormon': {'dopamin': 5.0, 'serotonin': 4.0, 'kortizol': -2.0}
        },
        'SahteYol': {
            'duygu': {'korku': 4.0, 'suphe': 10.0, 'merak': 5.0},
            'hormon': {'dopamin': 2.0, 'husran': 6.0, 'kortizol': 3.0}
        },
        'SendeletmeTasi': {
            'duygu': {'korku': 5.0, 'suphe': 7.0, 'merak': 0.0},
            'hormon': {'adrenalin': 4.0, 'kortizol': 3.0}
        },
        'GizliCukur': {
            'duygu': {'korku': 20.0, 'suphe': 15.0, 'merak': -6.0},
            'hormon': {'adrenalin': 12.0, 'kortizol': 10.0, 'husran': 8.0}
        },
        'KiymaMakinesi': {
            'duygu': {'korku': 25.0, 'suphe': 18.0, 'merak': -8.0},
            'hormon': {'adrenalin': 14.0, 'kortizol': 12.0, 'husran': 10.0}
        },
        'Yonlendirici': {
            'duygu': {'korku': 1.0, 'suphe': 5.0, 'merak': 2.0},
            'hormon': {'oksitosin': -2.0, 'kortizol': 2.0, 'dopamin': 1.0}
        },
    }

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
        harfler = {0: 'M', 1: 'A', 2: 'B', 3: 'F', 4: 'C', 5: 'S', 6: 'T', 7: 'G', 8: 'K', 9: 'Y'}
        sembol = harfler.get(self.arac_turu, str(self.arac_turu))
        px_x = self.x * PARSEK_BOYUTU
        px_y = self.y * PARSEK_BOYUTU
        text_surf = font.render(sembol, True, BEYAZ)
        rect = pygame.Rect(px_x, px_y, PARSEK_BOYUTU, PARSEK_BOYUTU)
        text_rect = text_surf.get_rect(center=rect.center)
        surface.blit(text_surf, text_rect)

    def psikobiyolojik_etki_uygula(self, ajan, siddet=1.0):
        """Faz 5: Arac etkisini duygu + hormon katmanina yansitir."""
        arac_adi = type(self).__name__
        tablo = self.ETKI_TABLOSU.get(arac_adi)
        if not tablo:
            return

        duygular = tablo.get('duygu', {})
        for ad, delta in duygular.items():
            mevcut = ajan.duygular.get(ad, 0.0)
            ajan.duygular[ad] = max(0.0, min(100.0, mevcut + delta * siddet))

        biyolojik = getattr(ajan, 'biyolojik_sistem', None)
        if biyolojik:
            hormonlar = tablo.get('hormon', {})
            for ad, delta in hormonlar.items():
                if ad in biyolojik.hormonlar:
                    mevcut = biyolojik.hormonlar.get(ad, 0.0)
                    biyolojik.hormonlar[ad] = max(0.0, min(100.0, mevcut + delta * siddet))

        if arac_adi in ['GizliCukur', 'KiymaMakinesi', 'Ates', 'SahteYol']:
            ajan.kavramsal_durum = 'KOTU'
        elif arac_adi in ['CikisOku']:
            ajan.kavramsal_durum = 'IYI'

class Mancinik(OyuncuAleti):
    def __init__(self, x, y, z, zemin_tipi, arac_turu):
        super().__init__(x, y, z, 'MANCINIK', arac_turu)
        if zemin_tipi == 'sert':
            self.maks_kapasite = 50
        else:
            self.maks_kapasite = 20
        self.mevcut_kapasite = self.maks_kapasite
        self.zemin_katsayisi = 1.0 if zemin_tipi == 'sert' else 2.5
        self.etki_altindakiler = set()

    def etki_uygula(self, ajanlar, harita_yon=None):
        """Etki alanına yeni giren ajanı fırlatır."""
        if not self.kullan():
            return

        mevcutlar = set()
        for ajan in ajanlar:
            if not ajan.hayatta:
                continue
            if ajan.z != self.z:
                continue
            if abs(ajan.x - self.x) <= ETKI_YARICAPI and abs(ajan.y - self.y) <= ETKI_YARICAPI:
                mevcutlar.add(ajan.id)
                if ajan.id in self.etki_altindakiler:
                    continue

                if not hasattr(ajan, 'yon'):
                    ajan.yon = random.choice(['yukari', 'asagi', 'sol', 'sag'])

                dx = ajan.x - self.x
                dy = ajan.y - self.y
                if dx == 0 and dy == 0:
                    dx, dy = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])

                adim_x = 1 if dx > 0 else (-1 if dx < 0 else 0)
                adim_y = 1 if dy > 0 else (-1 if dy < 0 else 0)
                kuvvet = random.randint(2, 4)
                hedef_x = max(0, min(HARITA_GENISLIK_PARSEL - 1, ajan.x + adim_x * kuvvet))
                hedef_y = max(0, min(HARITA_YUKSEKLIK_PARSEL - 1, ajan.y + adim_y * kuvvet))

                if harita_yon is not None:
                    hedef_parsel = harita_yon.map_grid[ajan.z][hedef_y][hedef_x]
                    if hedef_parsel and hedef_parsel.yurunebilir and not hedef_parsel.hasar_verir:
                        ajan.x = hedef_x
                        ajan.y = hedef_y
                    else:
                        # Güvenli değilse kısa itiş uygula.
                        kisa_x = max(0, min(HARITA_GENISLIK_PARSEL - 1, ajan.x + adim_x))
                        kisa_y = max(0, min(HARITA_YUKSEKLIK_PARSEL - 1, ajan.y + adim_y))
                        kisa_parsel = harita_yon.map_grid[ajan.z][kisa_y][kisa_x]
                        if kisa_parsel and kisa_parsel.yurunebilir and not kisa_parsel.hasar_verir:
                            ajan.x = kisa_x
                            ajan.y = kisa_y
                else:
                    ajan.x = hedef_x
                    ajan.y = hedef_y

                ajan.hiz *= 1.6
                ajan.duygular['korku'] = min(100, ajan.duygular.get('korku', 0) + 18)
                self.psikobiyolojik_etki_uygula(ajan, siddet=1.0)

        self.etki_altindakiler = mevcutlar

class SendeletmeTasi(OyuncuAleti):
    def __init__(self, x, y, z, arac_turu):
        super().__init__(x, y, z, 'TAS', arac_turu)
        self.maks_kapasite = 5
        self.mevcut_kapasite = 5

    def etki_uygula(self, ajanlar, harita_yon=None):
        """Ajanları sendeletir, yön değiştirir."""
        if not self.kullan():
            return
        for ajan in ajanlar:
            if abs(ajan.x - self.x) <= ETKI_YARICAPI and abs(ajan.y - self.y) <= ETKI_YARICAPI and abs(ajan.z - self.z) <= ETKI_YARICAPI:
                if not hasattr(ajan, 'yon'):
                    ajan.yon = random.choice(['yukari', 'asagi', 'sol', 'sag'])
                ajan.yon = random.choice(['yukari', 'asagi', 'sol', 'sag'])
                ajan.hiz *= 0.5  # Yavaşlat
                self.psikobiyolojik_etki_uygula(ajan, siddet=0.8)

class GizliCukur(OyuncuAleti):
    def __init__(self, x, y, z, arac_turu):
        super().__init__(x, y, z, 'CIKIS_SAHTE', arac_turu)  # Sahte çıkış gibi
        self.maks_kapasite = 1  # Tek seferlik

    def etki_uygula(self, ajanlar, harita_yon=None):
        """Ajanları düşürür, öldürür."""
        if not self.kullan():
            return
        for ajan in ajanlar:
            if ajan.x == self.x and ajan.y == self.y:
                self.psikobiyolojik_etki_uygula(ajan, siddet=1.4)
                ajan.hayatta = False  # Öldür

class KiymaMakinesi(OyuncuAleti):
    def __init__(self, x, y, z, arac_turu):
        super().__init__(x, y, z, 'CIKIS_DOGRU', arac_turu)  # Tehlikeli çıkış
        self.maks_kapasite = 100  # Sürekli

    def etki_uygula(self, ajanlar, harita_yon=None):
        """Ajanları öldürür."""
        if not self.kullan():
            return
        for ajan in ajanlar:
            if ajan.x == self.x and ajan.y == self.y:
                self.psikobiyolojik_etki_uygula(ajan, siddet=1.6)
                ajan.hayatta = False  # Öldür

class Yonlendirici(OyuncuAleti):
    def __init__(self, x, y, z, arac_turu):
        super().__init__(x, y, z, 'ORMAN', arac_turu)  # Orman gibi
        self.maks_kapasite = 20

    def etki_uygula(self, ajanlar, harita_yon=None):
        """Ajanların yönünü değiştirir."""
        if not self.kullan():
            return
        for ajan in ajanlar:
            if abs(ajan.x - self.x) <= ETKI_YARICAPI and abs(ajan.y - self.y) <= ETKI_YARICAPI and abs(ajan.z - self.z) <= ETKI_YARICAPI:
                # Belirli bir yöne yönlendir, örneğin sağa
                if not hasattr(ajan, 'yon'):
                    ajan.yon = 'sag'
                ajan.yon = 'sag'
                self.psikobiyolojik_etki_uygula(ajan, siddet=0.6)

class Ayna(OyuncuAleti):
    def __init__(self, x, y, z, arac_turu):
        super().__init__(x, y, z, 'AYNA', arac_turu)  # Ayna emoji
        self.maks_kapasite = 15

    def etki_uygula(self, ajanlar, harita_yon=None):
        """Ajanların yönünü ters çevirir."""
        if not self.kullan():
            return
        for ajan in ajanlar:
            if abs(ajan.x - self.x) <= ETKI_YARICAPI and abs(ajan.y - self.y) <= ETKI_YARICAPI and abs(ajan.z - self.z) <= ETKI_YARICAPI:
                if not hasattr(ajan, 'yon'):
                    ajan.yon = random.choice(['yukari', 'asagi', 'sol', 'sag'])
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
                self.psikobiyolojik_etki_uygula(ajan, siddet=0.7)

class Bariyer(OyuncuAleti):
    def __init__(self, x, y, z, arac_turu):
        super().__init__(x, y, z, 'BARIYER', arac_turu)  # Bariyer emoji
        self.maks_kapasite = 30

    def etki_uygula(self, ajanlar, harita_yon=None):
        """Engel koyar, ajanları yavaşlatır."""
        if not self.kullan():
            return
        # Yakındaki ajanları yavaşlat
        for ajan in ajanlar:
            if abs(ajan.x - self.x) <= ETKI_YARICAPI and abs(ajan.y - self.y) <= ETKI_YARICAPI and abs(ajan.z - self.z) <= ETKI_YARICAPI:
                ajan.hiz *= 0.8  # Yavaşlat
                ajan.duygular['suphe'] += 0.1
                self.psikobiyolojik_etki_uygula(ajan, siddet=0.9)

class Ates(OyuncuAleti):
    def __init__(self, x, y, z, arac_turu):
        super().__init__(x, y, z, 'ATES', arac_turu)  # Ateş emoji
        self.maks_kapasite = 10

    def etki_uygula(self, ajanlar, harita_yon=None):
        """Ajanları yakar, hasar verir ve hızlandırır."""
        if not self.kullan():
            return
        for ajan in ajanlar:
            if abs(ajan.x - self.x) <= ETKI_YARICAPI and abs(ajan.y - self.y) <= ETKI_YARICAPI and abs(ajan.z - self.z) <= ETKI_YARICAPI:
                ajan.can -= 20  # Hasar ver
                ajan.hiz *= 1.2  # Hızlandır
                ajan.duygular['korku'] += 0.2
                self.psikobiyolojik_etki_uygula(ajan, siddet=1.2)

class CikisOku(OyuncuAleti):
    def __init__(self, x, y, z, arac_turu):
        super().__init__(x, y, z, 'CIKIS_OKU', arac_turu)  # Çıkış oku emoji
        self.maks_kapasite = 1  # Sadece bir çıkış

    def etki_uygula(self, ajanlar, harita_yon=None):
        """Çıkış oku, fiziksel etki vermez; psikolojik olarak yönlendirir."""
        if not self.kullan():
            return
        for ajan in ajanlar:
            if abs(ajan.x - self.x) <= ETKI_YARICAPI and abs(ajan.y - self.y) <= ETKI_YARICAPI and abs(ajan.z - self.z) <= ETKI_YARICAPI:
                self.psikobiyolojik_etki_uygula(ajan, siddet=0.8)

class SahteYol(OyuncuAleti):
    def __init__(self, x, y, z, arac_turu):
        super().__init__(x, y, z, 'SAHTE_YOL', arac_turu)  # Sahte yol emoji
        self.maks_kapasite = 50  # Sürekli

    def etki_uygula(self, ajanlar, harita_yon=None):
        """Sahte yol fiziksel yol gibi görünür; psikolojik olarak şüphe biriktirir."""
        if not self.kullan():
            return
        for ajan in ajanlar:
            if abs(ajan.x - self.x) <= ETKI_YARICAPI and abs(ajan.y - self.y) <= ETKI_YARICAPI and abs(ajan.z - self.z) <= ETKI_YARICAPI:
                self.psikobiyolojik_etki_uygula(ajan, siddet=1.0)
# --- 🗄️ HARİTA VERİ YÖNETİCİSİ (Çok Boyutlu Dizi) ---

class HaritaYoneticisi:
    def __init__(self):
        # 5 Katmanlı Evren (Z, Y, X)
        # 3D Dizi: self.map_grid[katman][satir][sutun]
        self.max_katman = KATMAN_SAYISI
        self.map_grid = [[[None for _ in range(HARITA_GENISLIK_PARSEL)] 
                          for _ in range(HARITA_YUKSEKLIK_PARSEL)] 
                         for _ in range(self.max_katman)]
        self.aktif_katman = 0 # Şu an ekranda görünen kat
        self.merdiven_ciftleri = []
        self.omurga_rota = []  # Faz 1: giristen cikisa tam (x,y,z) adim listesi
        
        # Rastgele giriş/çıkış
        self.giris_katman = random.randint(0, self.max_katman - 1)
        self.cikis_katman = random.randint(0, self.max_katman - 1)
        while self.cikis_katman == self.giris_katman:
            self.cikis_katman = random.randint(0, self.max_katman - 1)
        self.giris_x, self.giris_y = 0, random.randint(0, HARITA_YUKSEKLIK_PARSEL - 1)
        self.cikis_x, self.cikis_y = HARITA_GENISLIK_PARSEL - 1, random.randint(0, HARITA_YUKSEKLIK_PARSEL - 1)
        
        # Haritayı rastgele oluştur
        self.rastgele_harita_olustur()

    @staticmethod
    def kayitli_haritalari_listele(haritalar_klasoru='haritalar'):
        """Kayitli harita dosyalarini yeni tarihten eskiye listeler."""
        os.makedirs(haritalar_klasoru, exist_ok=True)
        adaylar = []
        for ad in os.listdir(haritalar_klasoru):
            if not ad.lower().endswith('.json'):
                continue
            tam_yol = os.path.join(haritalar_klasoru, ad)
            if os.path.isfile(tam_yol):
                adaylar.append((os.path.getmtime(tam_yol), tam_yol))
        adaylar.sort(key=lambda x: x[0], reverse=True)
        return [yol for _, yol in adaylar]

    def _harita_seri_veri_olustur(self):
        """Haritayi JSON'a yazilabilir sade veri yapisina cevirir."""
        arac_sinif_adi = {
            Mancinik: 'Mancinik',
            Ayna: 'Ayna',
            Bariyer: 'Bariyer',
            Ates: 'Ates',
            CikisOku: 'CikisOku',
            SahteYol: 'SahteYol',
            SendeletmeTasi: 'SendeletmeTasi',
            GizliCukur: 'GizliCukur',
            KiymaMakinesi: 'KiymaMakinesi',
            Yonlendirici: 'Yonlendirici',
        }

        grid = []
        for kat in range(self.max_katman):
            katman_veri = []
            for y in range(HARITA_YUKSEKLIK_PARSEL):
                satir = []
                for x in range(HARITA_GENISLIK_PARSEL):
                    parsel = self.map_grid[kat][y][x]
                    hucre = {
                        'doku_id': parsel.doku_id,
                        'yurunebilir': parsel.yurunebilir,
                        'yavaslatma_katsayisi': parsel.yavaslatma_katsayisi,
                        'kazilabilir': parsel.kazilabilir,
                        'bogulma_riski': parsel.bogulma_riski,
                        'hasar_verir': parsel.hasar_verir,
                        'derinlik': parsel.derinlik,
                        'alet': None,
                    }
                    if parsel.uzerindeki_alet is not None:
                        alet = parsel.uzerindeki_alet
                        hucre['alet'] = {
                            'sinif': arac_sinif_adi.get(type(alet), type(alet).__name__),
                            'arac_turu': getattr(alet, 'arac_turu', 0),
                            'maks_kapasite': getattr(alet, 'maks_kapasite', 0),
                            'mevcut_kapasite': getattr(alet, 'mevcut_kapasite', 0),
                            'gizlilik_carpani': getattr(alet, 'gizlilik_carpani', 0.5),
                            'zemin_katsayisi': getattr(alet, 'zemin_katsayisi', 1.0),
                        }
                    satir.append(hucre)
                katman_veri.append(satir)
            grid.append(katman_veri)

        return {
            'surum': 1,
            'kayit_zamani': datetime.now().isoformat(timespec='seconds'),
            'boyut': {
                'genislik': HARITA_GENISLIK_PARSEL,
                'yukseklik': HARITA_YUKSEKLIK_PARSEL,
                'katman': self.max_katman,
            },
            'meta': {
                'aktif_katman': self.aktif_katman,
                'giris_katman': self.giris_katman,
                'cikis_katman': self.cikis_katman,
                'giris_x': self.giris_x,
                'giris_y': self.giris_y,
                'cikis_x': self.cikis_x,
                'cikis_y': self.cikis_y,
                'merdiven_ciftleri': self.merdiven_ciftleri,
                'omurga_rota': self.omurga_rota,
            },
            'grid': grid,
        }

    def haritayi_kaydet(self, dosya_adi=None, haritalar_klasoru='haritalar'):
        """Mevcut haritayi haritalar klasorune JSON olarak yazar."""
        os.makedirs(haritalar_klasoru, exist_ok=True)
        if not dosya_adi:
            damga = datetime.now().strftime('%Y%m%d_%H%M%S')
            dosya_adi = f'harita_{damga}.json'
        if not dosya_adi.lower().endswith('.json'):
            dosya_adi += '.json'

        tam_yol = os.path.join(haritalar_klasoru, dosya_adi)
        veri = self._harita_seri_veri_olustur()
        with open(tam_yol, 'w', encoding='utf-8') as f:
            json.dump(veri, f, ensure_ascii=False, indent=2)
        return tam_yol

    @classmethod
    def dosyadan_yukle(cls, dosya_yolu):
        """Kayitli bir harita dosyasindan HaritaYoneticisi nesnesi uretir."""
        with open(dosya_yolu, 'r', encoding='utf-8') as f:
            veri = json.load(f)

        nesne = cls()
        meta = veri.get('meta', {})
        nesne.aktif_katman = int(meta.get('aktif_katman', 0))
        nesne.giris_katman = int(meta.get('giris_katman', 0))
        nesne.cikis_katman = int(meta.get('cikis_katman', 0))
        nesne.giris_x = int(meta.get('giris_x', 0))
        nesne.giris_y = int(meta.get('giris_y', 0))
        nesne.cikis_x = int(meta.get('cikis_x', HARITA_GENISLIK_PARSEL - 1))
        nesne.cikis_y = int(meta.get('cikis_y', 0))
        nesne.merdiven_ciftleri = [tuple(m) for m in meta.get('merdiven_ciftleri', [])]
        nesne.omurga_rota = [tuple(p) for p in meta.get('omurga_rota', [])]

        parsel_siniflari = {
            'ZEMIN_DUZ': ZeminDuz,
            'DAG': Dag,
            'SU_GOL': SuGol,
            'DENIZ': Deniz,
            'SIKI_ORMAN': SikiOrman,
            'YOL': Yol,
            'TAS_DUVAR': TasDuvar,
            'OVA': Ova,
            'PLATO': Plato,
            'DIK_DAG': DikDag,
            'CALILIK': Calilik,
            'TASLIK': Taslik,
            'COL': Col,
        }

        alet_siniflari = {
            'Mancinik': Mancinik,
            'Ayna': Ayna,
            'Bariyer': Bariyer,
            'Ates': Ates,
            'CikisOku': CikisOku,
            'SahteYol': SahteYol,
            'SendeletmeTasi': SendeletmeTasi,
            'GizliCukur': GizliCukur,
            'KiymaMakinesi': KiymaMakinesi,
            'Yonlendirici': Yonlendirici,
        }

        grid = veri.get('grid', [])
        for kat in range(min(nesne.max_katman, len(grid))):
            for y in range(min(HARITA_YUKSEKLIK_PARSEL, len(grid[kat]))):
                satir = grid[kat][y]
                for x in range(min(HARITA_GENISLIK_PARSEL, len(satir))):
                    hucre = satir[x]
                    doku_id = hucre.get('doku_id', 'ZEMIN_DUZ')
                    parsel_sinifi = parsel_siniflari.get(doku_id, ZeminDuz)
                    parsel = parsel_sinifi(x, y, kat)
                    parsel.doku_id = doku_id
                    parsel.yurunebilir = bool(hucre.get('yurunebilir', parsel.yurunebilir))
                    parsel.yavaslatma_katsayisi = float(hucre.get('yavaslatma_katsayisi', parsel.yavaslatma_katsayisi))
                    parsel.kazilabilir = bool(hucre.get('kazilabilir', parsel.kazilabilir))
                    parsel.bogulma_riski = bool(hucre.get('bogulma_riski', parsel.bogulma_riski))
                    parsel.hasar_verir = bool(hucre.get('hasar_verir', parsel.hasar_verir))
                    parsel.derinlik = int(hucre.get('derinlik', parsel.derinlik))

                    alet_bilgi = hucre.get('alet')
                    if isinstance(alet_bilgi, dict):
                        sinif_adi = alet_bilgi.get('sinif')
                        arac_turu = int(alet_bilgi.get('arac_turu', 0))
                        alet_sinifi = alet_siniflari.get(sinif_adi)
                        if alet_sinifi is not None:
                            if alet_sinifi == Mancinik:
                                alet = alet_sinifi(x, y, kat, 'sert', arac_turu)
                            else:
                                alet = alet_sinifi(x, y, kat, arac_turu)
                            alet.maks_kapasite = float(alet_bilgi.get('maks_kapasite', alet.maks_kapasite))
                            alet.mevcut_kapasite = float(alet_bilgi.get('mevcut_kapasite', alet.mevcut_kapasite))
                            alet.gizlilik_carpani = float(alet_bilgi.get('gizlilik_carpani', alet.gizlilik_carpani))
                            alet.zemin_katsayisi = float(alet_bilgi.get('zemin_katsayisi', alet.zemin_katsayisi))
                            parsel.uzerindeki_alet = alet

                    nesne.map_grid[kat][y][x] = parsel

        return nesne

    def rastgele_harita_olustur(self):
        """Doğal görünümlü, kümelenmiş ve yumuşak geçişli katmanlar üretir."""

        sinif_eslesme = {
            'ZEMIN_DUZ': ZeminDuz,
            'DAG': Dag,
            'SU_GOL': SuGol,
            'DENIZ': Deniz,
            'SIKI_ORMAN': SikiOrman,
            'YOL': Yol,
            'TAS_DUVAR': TasDuvar,
            'OVA': Ova,
            'PLATO': Plato,
            'DIK_DAG': DikDag,
            'CALILIK': Calilik,
            'TASLIK': Taslik,
            'COL': Col,
        }

        komsular = [
            (-1, -1), (0, -1), (1, -1),
            (-1, 0),            (1, 0),
            (-1, 1),  (0, 1),  (1, 1),
        ]

        dogal_turler = [
            ('OVA', 24), ('ZEMIN_DUZ', 18), ('CALILIK', 12), ('SIKI_ORMAN', 10),
            ('TASLIK', 9), ('DAG', 9), ('PLATO', 7), ('SU_GOL', 6),
            ('DENIZ', 3), ('COL', 4), ('DIK_DAG', 3), ('TAS_DUVAR', 2),
        ]

        def agirlikli_secim(liste):
            toplam = sum(agirlik for _, agirlik in liste)
            esik = random.randint(1, toplam)
            birikim = 0
            for tur, agirlik in liste:
                birikim += agirlik
                if esik <= birikim:
                    return tur
            return 'ZEMIN_DUZ'

        def su_derinligi_hesapla(x, y, secilen_tur):
            kenar_mesafesi = min(x, y, HARITA_GENISLIK_PARSEL - 1 - x, HARITA_YUKSEKLIK_PARSEL - 1 - y)
            merkez_potansiyeli = min(15, max(1, kenar_mesafesi + random.randint(-2, 2)))
            if secilen_tur == 'DENIZ':
                return min(15, max(1, merkez_potansiyeli + 2))
            return min(12, max(1, merkez_potansiyeli))

        for kat in range(self.max_katman):
            doku_grid = [['ZEMIN_DUZ' for _ in range(HARITA_GENISLIK_PARSEL)] for _ in range(HARITA_YUKSEKLIK_PARSEL)]

            # Katman bazlı hafif iklim farklılığı ile kümeli alan üretimi.
            blob_sayisi = 22 + kat * 2
            for _ in range(blob_sayisi):
                tur = agirlikli_secim(dogal_turler)
                merkez_x = random.randint(0, HARITA_GENISLIK_PARSEL - 1)
                merkez_y = random.randint(0, HARITA_YUKSEKLIK_PARSEL - 1)
                yari_cap_x = random.randint(3, 8)
                yari_cap_y = random.randint(2, 6)

                for y in range(HARITA_YUKSEKLIK_PARSEL):
                    for x in range(HARITA_GENISLIK_PARSEL):
                        nx = (x - merkez_x) / max(1, yari_cap_x)
                        ny = (y - merkez_y) / max(1, yari_cap_y)
                        uzaklik = (nx * nx + ny * ny) ** 0.5
                        olasilik = max(0.0, 1.0 - uzaklik)
                        if random.random() < olasilik * 0.75:
                            doku_grid[y][x] = tur

            # Gürültüyü azalt ve komşu kümelenmesini güçlendir.
            for _ in range(2):
                yeni_grid = [satir[:] for satir in doku_grid]
                for y in range(HARITA_YUKSEKLIK_PARSEL):
                    for x in range(HARITA_GENISLIK_PARSEL):
                        saya = {}
                        for dx, dy in komsular:
                            nx, ny = x + dx, y + dy
                            if 0 <= nx < HARITA_GENISLIK_PARSEL and 0 <= ny < HARITA_YUKSEKLIK_PARSEL:
                                tur = doku_grid[ny][nx]
                                saya[tur] = saya.get(tur, 0) + 1
                        if saya:
                            baskin_tur = max(saya, key=saya.get)
                            if saya[baskin_tur] >= 5:
                                yeni_grid[y][x] = baskin_tur
                doku_grid = yeni_grid

            for y in range(HARITA_YUKSEKLIK_PARSEL):
                for x in range(HARITA_GENISLIK_PARSEL):
                    secilen_tur = doku_grid[y][x]
                    parsel_sinifi = sinif_eslesme.get(secilen_tur, ZeminDuz)
                    parsel = parsel_sinifi(x, y, kat)
                    if secilen_tur in ['SU_GOL', 'DENIZ']:
                        parsel.derinlik = su_derinligi_hesapla(x, y, secilen_tur)
                    self.map_grid[kat][y][x] = parsel

            # Her katmanda en az bir yürünebilir omurga yol.
            yol_y = random.randint(0, HARITA_YUKSEKLIK_PARSEL - 1)
            for x in range(HARITA_GENISLIK_PARSEL):
                self.map_grid[kat][yol_y][x] = Yol(x, yol_y, kat)
        
        # Giriş ve çıkış ayarla
        if self.map_grid[self.giris_katman][self.giris_y][self.giris_x]:
            self.map_grid[self.giris_katman][self.giris_y][self.giris_x].doku_id = 'GIRIS'
            self.map_grid[self.giris_katman][self.giris_y][self.giris_x].yurunebilir = True
        if self.map_grid[self.cikis_katman][self.cikis_y][self.cikis_x]:
            self.map_grid[self.cikis_katman][self.cikis_y][self.cikis_x].doku_id = 'CIKIS_SAHTE'
            self.map_grid[self.cikis_katman][self.cikis_y][self.cikis_x].yurunebilir = True

        self._rastgele_merdivenleri_olustur()
        self.uc_boyutlu_yol_ve_merdiven_yarat()

    def _rastgele_merdivenleri_olustur(self):
        """Her komşu katman çifti için bir adet yukarı ve bir adet aşağı merdiven yerleştirir."""
        self.merdiven_ciftleri = []
        for alt_kat in range(self.max_katman - 1):
            ust_kat = alt_kat + 1

            # Kenarlardan uzak, rastgele bir koordinat seç.
            x = random.randint(1, HARITA_GENISLIK_PARSEL - 2)
            y = random.randint(1, HARITA_YUKSEKLIK_PARSEL - 2)

            alt_parsel = self.map_grid[alt_kat][y][x]
            ust_parsel = self.map_grid[ust_kat][y][x]

            if alt_parsel is None:
                alt_parsel = ZeminDuz(x, y, alt_kat)
                self.map_grid[alt_kat][y][x] = alt_parsel
            if ust_parsel is None:
                ust_parsel = ZeminDuz(x, y, ust_kat)
                self.map_grid[ust_kat][y][x] = ust_parsel

            alt_parsel.doku_id = 'MERDIVEN_YUKARI'
            alt_parsel.yurunebilir = True
            alt_parsel.yavaslatma_katsayisi = 1.0

            ust_parsel.doku_id = 'MERDIVEN_ASAGI'
            ust_parsel.yurunebilir = True
            ust_parsel.yavaslatma_katsayisi = 1.0

            self.merdiven_ciftleri.append((x, y, alt_kat, ust_kat))

    def _omurga_rota_segment(self, kat, x1, y1, x2, y2):
        """(x1,y1)→(x2,y2) arasını L-şekilde geçen (x,y,z) tuple listesi döndürür."""
        sonuc = [(x1, y1, kat)]
        x = x1
        while x != x2:
            x += 1 if x2 > x1 else -1
            sonuc.append((x, y1, kat))
        y = y1
        while y != y2:
            y += 1 if y2 > y1 else -1
            sonuc.append((x2, y, kat))
        return sonuc

    def _yol_oyu(self, kat, x1, y1, x2, y2):
        """İki nokta arasını YOL dokusuyla L-şekli izde kaplar. Merdiven/giriş/çıkış hücrelerini korur."""
        korunan = {'MERDIVEN_YUKARI', 'MERDIVEN_ASAGI', 'GIRIS', 'CIKIS_SAHTE', 'CIKIS_KAPI'}
        # Yatay hareket: (x1, y1) → (x2-1, y1)
        x = x1
        while x != x2:
            if 0 <= x < HARITA_GENISLIK_PARSEL and 0 <= y1 < HARITA_YUKSEKLIK_PARSEL:
                parsel = self.map_grid[kat][y1][x]
                if parsel is not None and parsel.doku_id not in korunan:
                    self.map_grid[kat][y1][x] = Yol(x, y1, kat)
            x += 1 if x2 > x1 else -1
        # Dikey hareket: (x2, y1) → (x2, y2-1)
        y = y1
        while y != y2:
            if 0 <= x2 < HARITA_GENISLIK_PARSEL and 0 <= y < HARITA_YUKSEKLIK_PARSEL:
                parsel = self.map_grid[kat][y][x2]
                if parsel is not None and parsel.doku_id not in korunan:
                    self.map_grid[kat][y][x2] = Yol(x2, y, kat)
            y += 1 if y2 > y1 else -1
        # Uç nokta
        if 0 <= x2 < HARITA_GENISLIK_PARSEL and 0 <= y2 < HARITA_YUKSEKLIK_PARSEL:
            parsel = self.map_grid[kat][y2][x2]
            if parsel is not None and parsel.doku_id not in korunan:
                self.map_grid[kat][y2][x2] = Yol(x2, y2, kat)

    def uc_boyutlu_yol_ve_merdiven_yarat(self):
        """Girişten çıkışa YOL dokusu çizer ve omurga_rota listesi hesaplar.
        Lider AI'nın katman geçişli yol takibi için kullanılır."""
        self.omurga_rota = []
        cur_x, cur_y = self.giris_x, self.giris_y

        if self.giris_katman == self.cikis_katman:
            segman = self._omurga_rota_segment(self.giris_katman, cur_x, cur_y, self.cikis_x, self.cikis_y)
            self._yol_oyu(self.giris_katman, cur_x, cur_y, self.cikis_x, self.cikis_y)
            self.omurga_rota = segman
            return

        going_up = self.giris_katman < self.cikis_katman
        if going_up:
            for kat in range(self.giris_katman, self.cikis_katman):
                stair = next((s for s in self.merdiven_ciftleri if s[2] == kat), None)
                if stair is None:
                    continue
                mx, my = stair[0], stair[1]
                segman = self._omurga_rota_segment(kat, cur_x, cur_y, mx, my)
                self._yol_oyu(kat, cur_x, cur_y, mx, my)
                if self.omurga_rota and segman and self.omurga_rota[-1] == segman[0]:
                    self.omurga_rota.extend(segman[1:])
                else:
                    self.omurga_rota.extend(segman)
                self.omurga_rota.append((mx, my, kat + 1))
                cur_x, cur_y = mx, my
        else:
            for kat in range(self.giris_katman, self.cikis_katman, -1):
                stair = next((s for s in self.merdiven_ciftleri if s[3] == kat), None)
                if stair is None:
                    continue
                mx, my = stair[0], stair[1]
                segman = self._omurga_rota_segment(kat, cur_x, cur_y, mx, my)
                self._yol_oyu(kat, cur_x, cur_y, mx, my)
                if self.omurga_rota and segman and self.omurga_rota[-1] == segman[0]:
                    self.omurga_rota.extend(segman[1:])
                else:
                    self.omurga_rota.extend(segman)
                self.omurga_rota.append((mx, my, kat - 1))
                cur_x, cur_y = mx, my
        # Son katman: son merdivenden cikisa
        segman = self._omurga_rota_segment(self.cikis_katman, cur_x, cur_y, self.cikis_x, self.cikis_y)
        self._yol_oyu(self.cikis_katman, cur_x, cur_y, self.cikis_x, self.cikis_y)
        if self.omurga_rota and segman and self.omurga_rota[-1] == segman[0]:
            self.omurga_rota.extend(segman[1:])
        else:
            self.omurga_rota.extend(segman)

    def cikis_oklarini_kapiya_cevir(self):
        """Düzenleme sonrası çıkış oklarını kapıya çevir."""
        for kat in range(self.max_katman):
            for y in range(HARITA_YUKSEKLIK_PARSEL):
                for x in range(HARITA_GENISLIK_PARSEL):
                    parsel = self.map_grid[kat][y][x]
                    if parsel.uzerindeki_alet and isinstance(parsel.uzerindeki_alet, CikisOku):
                        parsel.doku_id = 'CIKIS_KAPI'
                        parsel.uzerindeki_alet = None  # Araç kaldır, parsel çıkış olsun

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
        for katman in self.map_grid:
            for satir in katman:
                for parsel in satir:
                    if not parsel or parsel.uzerindeki_alet is None or not hasattr(parsel.uzerindeki_alet, 'etki_uygula'):
                        continue

                    yakinda_ajan_var = any(
                        ajan.hayatta
                        and ajan.z == parsel.z
                        and abs(ajan.x - parsel.x) <= ETKI_YARICAPI
                        and abs(ajan.y - parsel.y) <= ETKI_YARICAPI
                        for ajan in ajanlar
                    )
                    if not yakinda_ajan_var:
                        continue

                    try:
                        parsel.uzerindeki_alet.etki_uygula(ajanlar, self)
                        if getattr(parsel.uzerindeki_alet, 'mevcut_kapasite', 1) <= 0:
                            if getattr(parsel, 'doku_id', '') == 'BARIYER':
                                parsel.yurunebilir = True
                            parsel.uzerindeki_alet = None
                    except Exception as ex:
                        print(f"Arac etki hatasi ({type(parsel.uzerindeki_alet).__name__} @ {parsel.x},{parsel.y},{parsel.z}): {ex}")