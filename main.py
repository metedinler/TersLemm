# main.py
import pygame
import sys
from ayarlar import *
from harita_yoneticisi import HaritaYoneticisi, Mancinik
from suru_yoneticisi import SuruYoneticisi # Yeni motorumuzu dahil ediyoruz

# Ses sistemi başlat
pygame.mixer.init()
if MUZIK_ACIK:
    try:
        pygame.mixer.music.load(MUZIK_DOSYASI)
        pygame.mixer.music.play(-1)  # Sonsuz döngü
    except:
        print(".sid müzik dosyası bulunamadı veya desteklenmiyor. .wav/.mp3'ye dönüştürün.")

# Ses efektleri (placeholder, gerçek dosyalar eklenecek)
ses_arac_yerlestir = None  # pygame.mixer.Sound("sesler/arac_yerlestir.wav")
ses_ajan_ol = None  # pygame.mixer.Sound("sesler/ajan_ol.wav")

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

def main():
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
    suru_yon.suru_yarat(baslangic_x=2, baslangic_y=5, boyut=15)

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

        # C. Ekrana Çiz (Render)
        # Önce haritayı, onun üstüne de sürüyü çiziyoruz.
        harita_yon.render(ekran, oyun_fontu)
        suru_yon.render(ekran, oyun_fontu, harita_yon.aktif_katman)
        oyun_yon.render(ekran, oyun_fontu)

        pygame.display.flip() # Çizilenleri ekrana yansıt
        clock.tick(FPS)       # Döngü hızını sabitle

    # --- 5. Çıkış ---
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()