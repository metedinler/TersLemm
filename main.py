# main.py
import pygame
import sys
import struct
from ayarlar import *  # AJAN_SAYISI, AJAN_HIZI, araç sayıları dahil
from harita_yoneticisi import HaritaYoneticisi, Mancinik, Ayna, Bariyer, Ates, CikisOku, ZeminDuz
from suru_yoneticisi import SuruYoneticisi # Yeni motorumuzu dahil ediyoruz
from sid_player import SidMusicManager

# Ses sistemi başlat
pygame.mixer.init()

# SID müzik yöneticisi
sid_manager = SidMusicManager(
    root_dir=".",
    memory_dir="sesler",
    sid_dir="sesler",
    player_cmd="sidplayfp"
)
if MUZIK_ACIK and sid_manager.available:
    sid_manager.start()
else:
    print("SID müzik kullanılamıyor, pygame fallback kullanılacak.")
    if MUZIK_ACIK:
        try:
            pygame.mixer.music.load(MUZIK_DOSYASI.replace(".sid", ".wav"))  # Fallback
            pygame.mixer.music.play(-1)
        except:
            print("Fallback müzik de bulunamadı.")

# Ses efektleri
def basit_ses_uret(frekans=440, sure=0.1, sample_rate=44100):
    # Basit bir kısa ton üret (beep değil, yumuşak)
    num_samples = int(sample_rate * sure)
    buffer = b''
    for i in range(num_samples):
        sample = int(32767 * 0.3 * (i / num_samples) * (1 - i / num_samples) * (2**0.5 / 2))  # Yumuşak envelope
        buffer += struct.pack('<h', sample)
    return pygame.mixer.Sound(buffer=buffer)

try:
    ses_arac_yerlestir = pygame.mixer.Sound("sesler/arac_yerlestir.wav")
except:
    ses_arac_yerlestir = basit_ses_uret(660, 0.15)  # Kısa pop sesi

try:
    ses_ajan_ol = pygame.mixer.Sound("sesler/ajan_ol.wav")
except:
    ses_ajan_ol = basit_ses_uret(220, 0.2)  # Düşük ton ölüm sesi

class OyunYoneticisi:
    def __init__(self, suru_yon):
        self.suru_yon = suru_yon
        self.baslangic_nufusu = len(suru_yon.ajanlar)
        self.olenler = 0
        self.dogru_cikis = 0
        self.sahte_cikis = 0
        self.kazanma_kosulu = False
        self.kaybetme_kosulu = False

    def guncelle(self):
        # Ajanları kontrol et
        for ajan in self.suru_yon.ajanlar[:]:  # Kopya al, silme sırasında sorun olmasın
            if ajan.can <= 0:
                self.olenler += 1
                self.suru_yon.ajanlar.remove(ajan)
                if SES_ACIK and ses_ajan_ol:
                    ses_ajan_ol.play()
                continue
            # Çıkış kontrolü
            parsel = self.suru_yon.harita.map_grid[ajan.z][ajan.y][ajan.x]
            if parsel.doku_id == 'CIKIS_DOGRU':
                self.dogru_cikis += 1
                self.suru_yon.ajanlar.remove(ajan)
            elif parsel.doku_id == 'CIKIS_SAHTE':
                self.sahte_cikis += 1
                self.suru_yon.ajanlar.remove(ajan)

        # Kazanma/Kaybetme
        kalan = self.baslangic_nufusu - self.olenler - self.dogru_cikis - self.sahte_cikis
        if kalan == 0:
            if self.dogru_cikis / self.baslangic_nufusu <= 0.1:
                self.kazanma_kosulu = True
            else:
                self.kaybetme_kosulu = True

    def render(self, surface, font):
        # UI göster
        yazi = f"Olen: {self.olenler} | Dogru: {self.dogru_cikis} | Sahte: {self.sahte_cikis}"
        text_surf = font.render(yazi, True, KIRMIZI)
        surface.blit(text_surf, (10, 10))
        if self.kazanma_kosulu:
            kazandi_surf = font.render("KAZANDIN!", True, YESIL)
            surface.blit(kazandi_surf, (EKRAN_GENISLIK // 2 - 50, EKRAN_YUKSEKLIK // 2))
        elif self.kaybetme_kosulu:
            kaybetti_surf = font.render("KAYBETTIN!", True, KIRMIZI)
            surface.blit(kaybetti_surf, (EKRAN_GENISLIK // 2 - 50, EKRAN_YUKSEKLIK // 2))

def duzenleme_modu():
    """Oyun başlamadan önce harita ve tuzakları düzenleme modu."""
    pygame.init()
    pygame.font.init()
    harita_yon = HaritaYoneticisi()
    # Haritayı boş olarak başlat (tüm katmanları ZeminDuz ile doldur)
    for kat in range(harita_yon.max_katman):
        for y in range(HARITA_YUKSEKLIK_PARSEL):
            for x in range(HARITA_GENISLIK_PARSEL):
                harita_yon.map_grid[kat][y][x] = ZeminDuz(x, y, kat)
    
    ekran = pygame.display.set_mode((EKRAN_GENISLIK, EKRAN_YUKSEKLIK))
    pygame.display.set_caption("Ters Lemmings - Düzenleme Modu")
    clock = pygame.time.Clock()
    
    try:
        font = pygame.font.SysFont("Segoe UI Emoji", PARSEK_BOYUTU - 4)
    except:
        font = pygame.font.SysFont(None, PARSEK_BOYUTU)
    
    arac_secimi = 0  # 0: Mancinik, 1: Ayna, 2: Bariyer, 3: Ateş, 4: Çıkış Oku
    arac_listesi = [Mancinik, Ayna, Bariyer, Ates, CikisOku]
    arac_adlari = ['Mancinik', 'Ayna', 'Bariyer', 'Ates', 'CikisOku']
    arac_kullanim = {'Mancinik': 0, 'Ayna': 0, 'Bariyer': 0, 'Ates': 0, 'CikisOku': 0}
    arac_limitleri = {'Mancinik': MANCINIK_SAYISI, 'Ayna': AYNA_SAYISI, 'Bariyer': BARIYER_SAYISI, 'Ates': ATES_SAYISI, 'CikisOku': 1}
    
    calisiyor = True
    while calisiyor:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    harita_yon.aktif_katmani_degistir(harita_yon.aktif_katman + 1)
                elif event.key == pygame.K_DOWN:
                    harita_yon.aktif_katmani_degistir(harita_yon.aktif_katman - 1)
                elif event.key == pygame.K_1:
                    arac_secimi = 0
                elif event.key == pygame.K_2:
                    arac_secimi = 1
                elif event.key == pygame.K_3:
                    arac_secimi = 2
                elif event.key == pygame.K_4:
                    arac_secimi = 3
                elif event.key == pygame.K_5:
                    arac_secimi = 4
                elif event.key == pygame.K_s:
                    # Kaydet
                    print("Harita kaydedildi.")
                elif event.key == pygame.K_ESCAPE:
                    calisiyor = False  # Düzenleme bitir, oyun başlat
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Sol tıklama
                    mx, my = pygame.mouse.get_pos()
                    grid_x = mx // PARSEK_BOYUTU
                    grid_y = my // PARSEK_BOYUTU
                    if 0 <= grid_x < HARITA_GENISLIK_PARSEL and 0 <= grid_y < HARITA_YUKSEKLIK_PARSEL:
                        parsel = harita_yon.map_grid[harita_yon.aktif_katman][grid_y][grid_x]
                        if parsel.uzerindeki_alet is None:
                            arac_adi = arac_adlari[arac_secimi]
                            if arac_kullanim[arac_adi] < arac_limitleri[arac_adi]:
                                if arac_adi == 'CikisOku':
                                    # Sadece kenarlarda
                                    if grid_x == 0 or grid_x == HARITA_GENISLIK_PARSEL-1 or grid_y == 0 or grid_y == HARITA_YUKSEKLIK_PARSEL-1:
                                        parsel.uzerindeki_alet = CikisOku(grid_x, grid_y, harita_yon.aktif_katman)
                                        arac_kullanim[arac_adi] += 1
                                        if SES_ACIK and ses_arac_yerlestir:
                                            ses_arac_yerlestir.play()
                                else:
                                    arac_sinif = arac_listesi[arac_secimi]
                                    if arac_sinif == Mancinik:
                                        parsel.uzerindeki_alet = arac_sinif(grid_x, grid_y, harita_yon.aktif_katman, 'sert')
                                    else:
                                        parsel.uzerindeki_alet = arac_sinif(grid_x, grid_y, harita_yon.aktif_katman)
                                    arac_kullanim[arac_adi] += 1
                                    if SES_ACIK and ses_arac_yerlestir:
                                        ses_arac_yerlestir.play()
        
        # Render
        harita_yon.render(ekran, font)
        
        # UI
        arac_adi = arac_adlari[arac_secimi]
        ui_yazi = f"Katman: {harita_yon.aktif_katman} | Araç: {arac_adi} ({arac_kullanim[arac_adi]}/{arac_limitleri[arac_adi]}) | 1-4: Araç Seç | S: Kaydet | ESC: Oyun Başlat"
        ui_surf = font.render(ui_yazi, True, (50, 50, 200))
        ekran.blit(ui_surf, (10, EKRAN_YUKSEKLIK - 30))
        
        pygame.display.flip()
        clock.tick(FPS)
    
    return harita_yon  # Düzenlenmiş haritayı döndür

def main():
    # --- 0. Düzenleme Modu ---
    print("Düzenleme modu başlatılıyor...")
    harita_yon = duzenleme_modu()
    harita_yon.cikis_oklarini_kapiya_cevir()  # Çıkış oklarını kapıya çevir
    
    # --- 1. Başlangıç Ayarları ---
    pygame.init()
    pygame.font.init()
    
    ekran = pygame.display.set_mode((EKRAN_GENISLIK, EKRAN_YUKSEKLIK))
    pygame.display.set_caption("Ters Lemmings - Sürü Simülasyonu Testi")
    clock = pygame.time.Clock()

    try:
        oyun_fontu = pygame.font.SysFont("Segoe UI Emoji", PARSEK_BOYUTU - 4)
    except:
        oyun_fontu = pygame.font.SysFont(None, PARSEK_BOYUTU)

    # --- 2. Haritayı Yükle ---
    harita_yon = HaritaYoneticisi()
    harita_yon.txt_den_yukle("haritalar")

    # --- 3. Sürü Yöneticisini Başlat ve Sürüyü Doğur ---
    suru_yon = SuruYoneticisi(harita_yon)
    
    # Katman 0'da, X=2, Y=5 koordinatlarında 15 kişilik bir sürü yaratalım!
    suru_yon.suru_yarat(baslangic_x=2, baslangic_y=5, boyut=AJAN_SAYISI)

    # --- 4. Oyun Yöneticisini Başlat ---
    oyun_yon = OyunYoneticisi(suru_yon)
    
    # --- 4. Ana Oyun Döngüsü ---
    calisiyor = True
    while calisiyor:
        # A. Olayları Dinle (Input Handling)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                calisiyor = False
            
            # Klavye Kontrolleri (Katman Değiştirme)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    harita_yon.aktif_katmani_degistir(harita_yon.aktif_katman + 1)
                elif event.key == pygame.K_DOWN:
                    harita_yon.aktif_katmani_degistir(harita_yon.aktif_katman - 1)
            
            # Fare Kontrolleri (Alet Yerleştirme)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Sol tıklama
                    mx, my = pygame.mouse.get_pos()
                    grid_x = mx // PARSEK_BOYUTU
                    grid_y = my // PARSEK_BOYUTU
                    if 0 <= grid_x < HARITA_GENISLIK_PARSEL and 0 <= grid_y < HARITA_YUKSEKLIK_PARSEL:
                        parsel = harita_yon.map_grid[harita_yon.aktif_katman][grid_y][grid_x]
                        if parsel.uzerindeki_alet is None:
                            parsel.uzerindeki_alet = Mancinik(grid_x, grid_y, harita_yon.aktif_katman, 'sert')
                            if SES_ACIK and ses_arac_yerlestir:
                                ses_arac_yerlestir.play()

        # B. Oyun Mantığını Güncelle (Update)
        # Araç etkilerini uygula
        harita_yon.arac_etkilerini_uygula(suru_yon.ajanlar)
        # Sürünün beyni burada çalışıyor, lider karar veriyor, kuyruk takip ediyor.
        suru_yon.guncelle()
        oyun_yon.guncelle()
        # SID müzik güncelle
        if sid_manager.available:
            sid_manager.update()

        # C. Ekrana Çiz (Render)
        # Önce haritayı, onun üstüne de sürüyü çiziyoruz.
        harita_yon.render(ekran, oyun_fontu)
        suru_yon.render(ekran, oyun_fontu, harita_yon.aktif_katman)
        oyun_yon.render(ekran, oyun_fontu)

        pygame.display.flip() # Çizilenleri ekrana yansıt
        clock.tick(FPS)       # Döngü hızını sabitle

    # --- 5. Çıkış ---
    if sid_manager.available:
        sid_manager.stop()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()