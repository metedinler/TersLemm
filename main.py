# main.py
import pygame
import sys
from ayarlar import *
from harita_yoneticisi import HaritaYoneticisi, OyuncuAleti
from suru_yoneticisi import SuruYoneticisi # Yeni motorumuzu dahil ediyoruz

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
                            parsel.uzerindeki_alet = OyuncuAleti(grid_x, grid_y, harita_yon.aktif_katman, 'MANCINIK')

        # B. Oyun Mantığını Güncelle (Update)
        # Sürünün beyni burada çalışıyor, lider karar veriyor, kuyruk takip ediyor.
        suru_yon.guncelle()

        # C. Ekrana Çiz (Render)
        # Önce haritayı, onun üstüne de sürüyü çiziyoruz.
        harita_yon.render(ekran, oyun_fontu)
        suru_yon.render(ekran, oyun_fontu, harita_yon.aktif_katman)

        pygame.display.flip() # Çizilenleri ekrana yansıt
        clock.tick(FPS)       # Döngü hızını sabitle

    # --- 5. Çıkış ---
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()