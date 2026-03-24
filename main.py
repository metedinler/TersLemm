# main.py
import pygame
import sys
import struct
import suru_yoneticisi as suru_mod
from ayarlar import *  # AJAN_SAYISI, AJAN_HIZI, araç sayıları dahil
from harita_yoneticisi import (
    HaritaYoneticisi,
    Mancinik,
    Ayna,
    Bariyer,
    Ates,
    CikisOku,
    ZeminDuz,
    SahteYol,
    SendeletmeTasi,
    GizliCukur,
    KiymaMakinesi,
    Yonlendirici,
    FeromonIstasyonu,
    OforiGazi,
    KorkuGazi,
    DonmaAlani,
    DepresifAlan,
    SosyalAyna,
    EngelYansitici,
    SesYayici,
    GolgeRehber,
    KaosCekirdegi,
)
from suru_yoneticisi import SuruYoneticisi # Yeni motorumuzu dahil ediyoruz
from sid_player import SidMusicManager
from oyun_bilesenleri import (
    SesAyarMenusu,
    AjanIzlemePenceresi,
    OyunKayitYonetici,
    OyunYoneticisi,
    AracPaneli,
    secili_arac_etiketi_ciz,
    oyun_ici_menu,
)

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

SES_DURUM = {"efekt": SES_ACIK}

# Bu dosya artik sadece oyun akisina odaklanir; detayli bileşenler oyun_bilesenleri.py icine ayrildi.


def ciz_giris_cikis_isaretleri(ekran, harita_yon):
    if harita_yon.aktif_katman == harita_yon.giris_katman:
        giris_px_x = harita_yon.giris_x * PARSEK_BOYUTU + PARSEK_BOYUTU // 2
        giris_px_y = harita_yon.giris_y * PARSEK_BOYUTU + PARSEK_BOYUTU // 2
        pygame.draw.circle(ekran, (245, 245, 245), (giris_px_x, giris_px_y), 14, 3)
        pygame.draw.polygon(ekran, (255, 255, 255), [
            (giris_px_x - 10, giris_px_y),
            (giris_px_x + 10, giris_px_y - 10),
            (giris_px_x + 10, giris_px_y + 10)
        ])

    if harita_yon.aktif_katman == harita_yon.cikis_katman:
        cikis_px_x = harita_yon.cikis_x * PARSEK_BOYUTU + PARSEK_BOYUTU // 2
        cikis_px_y = harita_yon.cikis_y * PARSEK_BOYUTU + PARSEK_BOYUTU // 2
        pygame.draw.circle(ekran, (60, 220, 80), (cikis_px_x, cikis_px_y), 14, 3)
        pygame.draw.polygon(ekran, (0, 160, 0), [
            (cikis_px_x + 10, cikis_px_y),
            (cikis_px_x - 10, cikis_px_y - 10),
            (cikis_px_x - 10, cikis_px_y + 10)
        ])


def mod_dugmeleri_uret(suru_yon):
    taban_x = 10
    taban_y = 42
    dugme_w = 118
    dugme_h = 28
    bosluk = 8
    sira = [
        ("normal", "Normal"),
        ("kesif", "Kesif"),
        ("gezinti", "Gezinti"),
        ("yol_izleme", "Yol Izleme"),
    ]
    dugmeler = []
    for i, (mod, etiket) in enumerate(sira):
        rx = taban_x + i * (dugme_w + bosluk)
        ry = taban_y
        dugmeler.append({"mod": mod, "etiket": etiket, "rect": pygame.Rect(rx, ry, dugme_w, dugme_h)})
    return dugmeler


def ciz_mod_dugmeleri(ekran, font, suru_yon):
    dugmeler = mod_dugmeleri_uret(suru_yon)
    for d in dugmeler:
        aktif = (suru_yon.oyun_modu == d["mod"])
        dolgu = (38, 84, 152) if aktif else (26, 32, 42)
        kenar = (122, 190, 255) if aktif else (82, 98, 120)
        pygame.draw.rect(ekran, dolgu, d["rect"], border_radius=6)
        pygame.draw.rect(ekran, kenar, d["rect"], 2, border_radius=6)
        txt = font.render(d["etiket"], True, (238, 245, 255))
        ekran.blit(
            txt,
            (
                d["rect"].x + d["rect"].width // 2 - txt.get_width() // 2,
                d["rect"].y + d["rect"].height // 2 - txt.get_height() // 2,
            ),
        )
    return dugmeler


def baslangic_menusu():
    """Gerçek başlangıç menüsü: başlat/çıkış ve zorluk seçimi."""
    pygame.init()
    pygame.font.init()

    ekran = pygame.display.set_mode((EKRAN_GENISLIK, EKRAN_YUKSEKLIK), pygame.RESIZABLE)
    pygame.display.set_caption("Ters Lemmings - Baslangic Menusu")
    clock = pygame.time.Clock()

    baslik_font = pygame.font.SysFont("Segoe UI", 48, bold=True)
    menu_font = pygame.font.SysFont("Segoe UI", 30, bold=True)
    bilgi_font = pygame.font.SysFont("Segoe UI", 22)

    # Zorluk tanımlarını ayarlar.py'deki katsayılardan dinamik oluştur
    zorluklar = []
    for zorluk_adi, katsayilar in ZORLUK_KATSAYILARI.items():
        zorluklar.append({
            "ad": zorluk_adi,
            "ajan_sayisi": int(AJAN_SAYISI_TEMEL * katsayilar['ajan_sayisi_x']),
            "karar_hz": int(AJAN_KARAR_HZ_TEMEL * katsayilar['karar_hz_x']),
            "ogrenme_aralik": int(OGRENME_TIK_ARALIGI_TEMEL / katsayilar['ogrenme_aralik_x']),
            "ogrenme_miktari": OGRENME_MIKTARI_TEMEL * katsayilar['ogrenme_miktari_x'],
            "cikis_artis": CIKIS_BILGISI_ARTIS_TEMEL * katsayilar['cikis_artis_x'],
            "baslangic_bekleme": int(SURU_BASLANGIC_BEKLEME_TIK_TEMEL * katsayilar['baslangic_bekleme_x']),
            "duygu_sonum_aralik": max(2, int(DUYGU_SONUM_TIK_ARALIGI_TEMEL / max(0.35, katsayilar['karar_hz_x']))),
            "grup_koruma_tik": int(SURU_GRUP_KORUMA_TIK_TEMEL * (1.15 if zorluk_adi == 'Kolay' else (1.0 if zorluk_adi == 'Orta' else 0.9))),
        })

    secili_zorluk = 1
    kayitli_haritalar = HaritaYoneticisi.kayitli_haritalari_listele()
    secili_harita_idx = 0
    kayitli_harita_modu = len(kayitli_haritalar) > 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return None
                if event.key == pygame.K_LEFT:
                    secili_zorluk = (secili_zorluk - 1) % len(zorluklar)
                elif event.key == pygame.K_RIGHT:
                    secili_zorluk = (secili_zorluk + 1) % len(zorluklar)
                elif event.key == pygame.K_k:
                    if kayitli_haritalar:
                        kayitli_harita_modu = not kayitli_harita_modu
                elif event.key == pygame.K_q:
                    if kayitli_harita_modu and kayitli_haritalar:
                        secili_harita_idx = (secili_harita_idx - 1) % len(kayitli_haritalar)
                elif event.key == pygame.K_e:
                    if kayitli_harita_modu and kayitli_haritalar:
                        secili_harita_idx = (secili_harita_idx + 1) % len(kayitli_haritalar)
                elif event.key == pygame.K_RETURN:
                    secim = dict(zorluklar[secili_zorluk])
                    secim["harita_dosyasi"] = None
                    if kayitli_harita_modu and kayitli_haritalar:
                        secim["harita_dosyasi"] = kayitli_haritalar[secili_harita_idx]
                    return secim

        ekran.fill((14, 18, 24))
        pygame.draw.rect(ekran, (30, 36, 44), pygame.Rect(90, 90, EKRAN_GENISLIK - 180, EKRAN_YUKSEKLIK - 180), border_radius=12)
        pygame.draw.rect(ekran, (74, 168, 255), pygame.Rect(90, 90, EKRAN_GENISLIK - 180, EKRAN_YUKSEKLIK - 180), 2, border_radius=12)

        ekran.blit(baslik_font.render("TERS LEMMINGS", True, (220, 230, 242)), (430, 140))
        ekran.blit(menu_font.render("Gercek Oyun Menusu", True, (148, 202, 255)), (485, 205))

        z = zorluklar[secili_zorluk]
        ekran.blit(menu_font.render(f"Zorluk: {z['ad']}", True, (255, 236, 160)), (500, 300))
        ekran.blit(bilgi_font.render(f"Ajan: {z['ajan_sayisi']}  |  Karar Hizi: {z['karar_hz']}/sn", True, (205, 214, 224)), (430, 355))
        if kayitli_harita_modu and kayitli_haritalar:
            secili_harita = kayitli_haritalar[secili_harita_idx].replace('\\', '/').split('/')[-1]
            harita_satiri = f"Harita Modu: KAYITLI | Dosya: {secili_harita}"
        else:
            harita_satiri = "Harita Modu: YENI RASTGELE"

        ekran.blit(bilgi_font.render(harita_satiri, True, (180, 222, 255)), (360, 400))
        ekran.blit(bilgi_font.render("K: Mod Degistir | Q/E: Kayitli Harita Sec | Enter: Baslat | ESC: Cikis", True, (188, 196, 206)), (250, 440))

        pygame.display.flip()
        clock.tick(FPS)



def duzenleme_modu(yuklenecek_harita_yolu=None):
    """Oyun başlamadan önce harita ve tuzakları düzenleme modu."""
    def yerlestir_arac(harita_yon, arac_secimi, arac_adlari, arac_kullanim, arac_limitleri, arac_listesi):
        if arac_secimi < 0 or arac_secimi >= len(arac_listesi):
            return
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
                            parsel.uzerindeki_alet = CikisOku(grid_x, grid_y, harita_yon.aktif_katman, arac_secimi)
                            arac_kullanim[arac_adi] += 1
                            if SES_DURUM["efekt"] and ses_arac_yerlestir:
                                ses_arac_yerlestir.play()
                    else:
                        arac_sinif = arac_listesi[arac_secimi]
                        if arac_sinif == Mancinik:
                            parsel.uzerindeki_alet = arac_sinif(grid_x, grid_y, harita_yon.aktif_katman, 'sert', arac_secimi)
                        else:
                            parsel.uzerindeki_alet = arac_sinif(grid_x, grid_y, harita_yon.aktif_katman, arac_secimi)
                        arac_kullanim[arac_adi] += 1
                        if SES_DURUM["efekt"] and ses_arac_yerlestir:
                            ses_arac_yerlestir.play()

    def kaldir_arac(harita_yon, arac_kullanim, arac_adlari):
        mx, my = pygame.mouse.get_pos()
        grid_x = mx // PARSEK_BOYUTU
        grid_y = my // PARSEK_BOYUTU
        if 0 <= grid_x < HARITA_GENISLIK_PARSEL and 0 <= grid_y < HARITA_YUKSEKLIK_PARSEL:
            parsel = harita_yon.map_grid[harita_yon.aktif_katman][grid_y][grid_x]
            if parsel and parsel.uzerindeki_alet:
                arac_turu = parsel.uzerindeki_alet.arac_turu
                if isinstance(arac_turu, int) and 0 <= arac_turu < len(arac_adlari):
                    arac_adi = arac_adlari[arac_turu]
                    arac_kullanim[arac_adi] = max(0, arac_kullanim[arac_adi] - 1)
                parsel.uzerindeki_alet = None

    def etki_alani_goster(ekran, arac_secimi, arac_listesi):
        mx, my = pygame.mouse.get_pos()
        grid_x = mx // PARSEK_BOYUTU
        grid_y = my // PARSEK_BOYUTU
        if 0 <= grid_x < HARITA_GENISLIK_PARSEL and 0 <= grid_y < HARITA_YUKSEKLIK_PARSEL:
            # Etki alanı ±2 (5x5x5)
            for dz in range(-ETKI_YARICAPI, ETKI_YARICAPI + 1):
                for dy in range(-ETKI_YARICAPI, ETKI_YARICAPI + 1):
                    for dx in range(-ETKI_YARICAPI, ETKI_YARICAPI + 1):
                        nx, ny = grid_x + dx, grid_y + dy
                        if 0 <= nx < HARITA_GENISLIK_PARSEL and 0 <= ny < HARITA_YUKSEKLIK_PARSEL:
                            px_x = nx * PARSEK_BOYUTU
                            px_y = ny * PARSEK_BOYUTU
                            rect = pygame.Rect(px_x, px_y, PARSEK_BOYUTU, PARSEK_BOYUTU)
                            pygame.draw.rect(ekran, (255, 255, 0), rect, 2)  # Sarı çerçeve

    pygame.init()
    pygame.font.init()
    # Kullanici isterse onceki kayitli haritayi ac, yoksa yeni rastgele harita uret.
    if yuklenecek_harita_yolu:
        try:
            harita_yon = HaritaYoneticisi.dosyadan_yukle(yuklenecek_harita_yolu)
            print(f"Kayitli harita yuklendi: {yuklenecek_harita_yolu}")
        except Exception as ex:
            print(f"Kayitli harita yuklenemedi, rastgele haritaya donuluyor: {ex}")
            harita_yon = HaritaYoneticisi()
    else:
        harita_yon = HaritaYoneticisi()

    ses_menusu = SesAyarMenusu(sid_manager, SES_DURUM)
    ses_menusu.uygula()
    
    ekran = pygame.display.set_mode((EKRAN_GENISLIK, EKRAN_YUKSEKLIK), pygame.RESIZABLE)
    pygame.display.set_caption("Ters Lemmings - Düzenleme Modu")
    clock = pygame.time.Clock()
    
    try:
        font = pygame.font.SysFont("Segoe UI Emoji", PARSEK_BOYUTU - 4, bold=True)
        ui_font = pygame.font.SysFont("Segoe UI", 22, bold=True)
    except:
        font = pygame.font.SysFont(None, PARSEK_BOYUTU)
        ui_font = pygame.font.SysFont(None, 22, bold=True)
    
    arac_secimi = 0
    arac_listesi = [
        Mancinik, Ayna, Bariyer, Ates, CikisOku, SahteYol, SendeletmeTasi, GizliCukur, KiymaMakinesi, Yonlendirici,
        FeromonIstasyonu, OforiGazi, KorkuGazi, DonmaAlani, DepresifAlan, SosyalAyna, EngelYansitici, SesYayici, GolgeRehber, KaosCekirdegi,
    ]
    arac_adlari = [
        'Mancinik', 'Ayna', 'Bariyer', 'Ates', 'CikisOku', 'SahteYol', 'SendeletmeTasi', 'GizliCukur', 'KiymaMakinesi', 'Yonlendirici',
        'FeromonIstasyonu', 'OforiGazi', 'KorkuGazi', 'DonmaAlani', 'DepresifAlan', 'SosyalAyna', 'EngelYansitici', 'SesYayici', 'GolgeRehber', 'KaosCekirdegi'
    ]
    arac_kullanim = {ad: 0 for ad in arac_adlari}
    arac_limitleri = {
        'Mancinik': MANCINIK_SAYISI, 'Ayna': AYNA_SAYISI, 'Bariyer': BARIYER_SAYISI, 'Ates': ATES_SAYISI,
        'CikisOku': CIKIS_OKU_SAYISI, 'SahteYol': SAHTE_YOL_SAYISI, 'SendeletmeTasi': SENDELETME_TASI_SAYISI,
        'GizliCukur': GIZLI_CUKUR_SAYISI, 'KiymaMakinesi': KIYMA_MAKINESI_SAYISI, 'Yonlendirici': YONLENDIRICI_SAYISI,
        'FeromonIstasyonu': FEROMON_ISTASYONU_SAYISI,
        'OforiGazi': OFORI_GAZI_SAYISI,
        'KorkuGazi': KORKU_GAZI_SAYISI,
        'DonmaAlani': DONMA_ALANI_SAYISI,
        'DepresifAlan': DEPRESIF_ALAN_SAYISI,
        'SosyalAyna': SOSYAL_AYNA_SAYISI,
        'EngelYansitici': ENGEL_YANSITICI_SAYISI,
        'SesYayici': SES_YAYICI_SAYISI,
        'GolgeRehber': GOLGE_REHBER_SAYISI,
        'KaosCekirdegi': KAOS_CEKIRDEGI_SAYISI,
    }
    arac_paneli = AracPaneli(arac_adlari, mevcut_arac_sayisi=len(arac_listesi))
    
    calisiyor = True
    mouse_basili = False
    while calisiyor:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if ses_menusu.tus_isle(event):
                    continue
                if event.key == pygame.K_UP:
                    harita_yon.aktif_katmani_degistir(harita_yon.aktif_katman + 1)
                elif event.key == pygame.K_DOWN:
                    harita_yon.aktif_katmani_degistir(harita_yon.aktif_katman - 1)
                elif arac_paneli.klavye_secimi(event):
                    arac_secimi = arac_paneli.secili_index
                elif event.key == pygame.K_s:
                    # Haritayi manuel olarak kaydetmek icin S kisayolu.
                    try:
                        kayit_yolu = harita_yon.haritayi_kaydet()
                        print(f"Harita kaydedildi: {kayit_yolu}")
                    except Exception as ex:
                        print(f"Harita kaydetme hatasi: {ex}")
                elif event.key == pygame.K_RETURN:
                    return harita_yon  # Düzenleme tamam, oyuna geç
                elif event.key == pygame.K_ESCAPE:
                    return None  # Ana menüye geri dön
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if arac_paneli.mouse_secimi(event):
                    arac_secimi = arac_paneli.secili_index
                    continue
                if event.button == 1:  # Sol tıklama - yerleştir
                    mouse_basili = True
                    yerlestir_arac(harita_yon, arac_secimi, arac_adlari, arac_kullanim, arac_limitleri, arac_listesi)
                elif event.button == 3:  # Sağ tıklama - kaldır
                    kaldir_arac(harita_yon, arac_kullanim, arac_adlari)
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    mouse_basili = False
            elif event.type == pygame.MOUSEMOTION and mouse_basili:
                yerlestir_arac(harita_yon, arac_secimi, arac_adlari, arac_kullanim, arac_limitleri, arac_listesi)
        
        # Render
        harita_yon.render(ekran, font)
        
        # Etki alanı göster (araç seçiliyse)
        if arac_secimi >= 0:
            etki_alani_goster(ekran, arac_secimi, arac_listesi)
        
        ciz_giris_cikis_isaretleri(ekran, harita_yon)
        arac_paneli.ciz(ekran, ui_font, arac_kullanim, arac_limitleri)
        
        # UI
        arac_adi = arac_adlari[arac_secimi]
        if ses_menusu.acik:
            ses_menusu.ciz(ekran, ui_font)
        else:
            cubuk_y = HARITA_ALAN_YUKSEKLIK + ARAC_PANEL_YUKSEKLIK
            pygame.draw.rect(ekran, KOYU_GRI, pygame.Rect(0, cubuk_y, EKRAN_GENISLIK, DURUM_CUBUGU_YUKSEKLIK))
            pygame.draw.line(ekran, GRI, (0, cubuk_y), (EKRAN_GENISLIK, cubuk_y), 2)
            ui_yazi = (
                f"Katman: {harita_yon.aktif_katman + 1}/{harita_yon.max_katman} | "
                f"Araç: {arac_adi} ({arac_kullanim[arac_adi]}/{arac_limitleri[arac_adi]}) | "
                "Etki: 5x5x5 | 1-0 ve Shift+1-0 sec | Yukari/Asagi: Katman | ENTER: Oyuna Gec | ESC: Menu | F1: Ses"
            )
            ui_surf = ui_font.render(ui_yazi, True, (235, 235, 235))
            ekran.blit(ui_surf, (10, cubuk_y + 16))
        
        pygame.display.flip()
        clock.tick(FPS)
    
    return None

def main():
    while True:
        zorluk_ayari = baslangic_menusu()
        if zorluk_ayari is None:
            pygame.quit()
            sys.exit()

        suru_mod.AJAN_KARAR_HZ = zorluk_ayari["karar_hz"]
        suru_mod.OGRENME_TIK_ARALIGI = zorluk_ayari["ogrenme_aralik"]
        suru_mod.OGRENME_MIKTARI = zorluk_ayari["ogrenme_miktari"]
        suru_mod.CIKIS_BILGISI_ARTIS = zorluk_ayari["cikis_artis"]
        suru_mod.SURU_BASLANGIC_BEKLEME_TIK = zorluk_ayari["baslangic_bekleme"]
        suru_mod.DUYGU_SONUM_TIK_ARALIGI = zorluk_ayari["duygu_sonum_aralik"]
        suru_mod.SURU_GRUP_KORUMA_TIK = zorluk_ayari["grup_koruma_tik"]

        print("Duzenleme modu baslatiliyor...")
        harita_yon = duzenleme_modu(zorluk_ayari.get("harita_dosyasi"))
        if harita_yon is None:
            continue
        harita_yon.cikis_oklarini_kapiya_cevir()
        # Her oyun baslangicinda aktif haritanin bir kopyasi haritalar klasorune kaydedilir.
        try:
            otomatik_kayit = harita_yon.haritayi_kaydet()
            print(f"Otomatik harita kaydi: {otomatik_kayit}")
        except Exception as ex:
            print(f"Otomatik harita kaydi basarisiz: {ex}")

        pygame.init()
        pygame.font.init()
        ekran = pygame.display.set_mode((EKRAN_GENISLIK, EKRAN_YUKSEKLIK), pygame.RESIZABLE)
        pygame.display.set_caption("Ters Lemmings - Sürü Simülasyonu Testi")
        clock = pygame.time.Clock()

        try:
            oyun_fontu = pygame.font.SysFont("Segoe UI Emoji", PARSEK_BOYUTU - 4, bold=True)
            ui_fontu = pygame.font.SysFont("Segoe UI", 22, bold=True)
        except:
            oyun_fontu = pygame.font.SysFont(None, PARSEK_BOYUTU)
            ui_fontu = pygame.font.SysFont(None, 22, bold=True)

        ses_menusu = SesAyarMenusu(sid_manager, SES_DURUM)
        ses_menusu.uygula()

        suru_yon = SuruYoneticisi(harita_yon)
        suru_yon.suru_yarat(harita_yon.giris_x, harita_yon.giris_y, zorluk_ayari["ajan_sayisi"])
        oyun_yon = OyunYoneticisi(suru_yon, SES_DURUM, ses_ajan_ol)
        log_yon = OyunKayitYonetici()
        log_yon.baslangic(zorluk_ayari, len(suru_yon.ajanlar))

        arac_listesi = [
            Mancinik, Ayna, Bariyer, Ates, CikisOku, SahteYol, SendeletmeTasi, GizliCukur, KiymaMakinesi, Yonlendirici,
            FeromonIstasyonu, OforiGazi, KorkuGazi, DonmaAlani, DepresifAlan, SosyalAyna, EngelYansitici, SesYayici, GolgeRehber, KaosCekirdegi,
        ]
        arac_adlari = [
            'Mancinik', 'Ayna', 'Bariyer', 'Ates', 'CikisOku', 'SahteYol', 'SendeletmeTasi', 'GizliCukur', 'KiymaMakinesi', 'Yonlendirici',
            'FeromonIstasyonu', 'OforiGazi', 'KorkuGazi', 'DonmaAlani', 'DepresifAlan', 'SosyalAyna', 'EngelYansitici', 'SesYayici', 'GolgeRehber', 'KaosCekirdegi'
        ]
        arac_limitleri = {
            'Mancinik': MANCINIK_SAYISI, 'Ayna': AYNA_SAYISI, 'Bariyer': BARIYER_SAYISI, 'Ates': ATES_SAYISI,
            'CikisOku': CIKIS_OKU_SAYISI, 'SahteYol': SAHTE_YOL_SAYISI, 'SendeletmeTasi': SENDELETME_TASI_SAYISI,
            'GizliCukur': GIZLI_CUKUR_SAYISI, 'KiymaMakinesi': KIYMA_MAKINESI_SAYISI, 'Yonlendirici': YONLENDIRICI_SAYISI,
            'FeromonIstasyonu': FEROMON_ISTASYONU_SAYISI,
            'OforiGazi': OFORI_GAZI_SAYISI,
            'KorkuGazi': KORKU_GAZI_SAYISI,
            'DonmaAlani': DONMA_ALANI_SAYISI,
            'DepresifAlan': DEPRESIF_ALAN_SAYISI,
            'SosyalAyna': SOSYAL_AYNA_SAYISI,
            'EngelYansitici': ENGEL_YANSITICI_SAYISI,
            'SesYayici': SES_YAYICI_SAYISI,
            'GolgeRehber': GOLGE_REHBER_SAYISI,
            'KaosCekirdegi': KAOS_CEKIRDEGI_SAYISI,
        }
        arac_kullanim = {ad: 0 for ad in arac_adlari}
        arac_secimi = 0
        arac_paneli = AracPaneli(arac_adlari, mevcut_arac_sayisi=len(arac_listesi))

        for kat in range(harita_yon.max_katman):
            for y in range(HARITA_YUKSEKLIK_PARSEL):
                for x in range(HARITA_GENISLIK_PARSEL):
                    parsel = harita_yon.map_grid[kat][y][x]
                    if parsel and parsel.uzerindeki_alet:
                        tur = parsel.uzerindeki_alet.arac_turu
                        if isinstance(tur, int) and 0 <= tur < len(arac_adlari):
                            arac_kullanim[arac_adlari[tur]] += 1

        def oyunda_arac_yerlestir():
            if arac_secimi < 0 or arac_secimi >= len(arac_listesi):
                return
            mx, my = pygame.mouse.get_pos()
            grid_x = mx // PARSEK_BOYUTU
            grid_y = my // PARSEK_BOYUTU
            if 0 <= grid_x < HARITA_GENISLIK_PARSEL and 0 <= grid_y < HARITA_YUKSEKLIK_PARSEL:
                parsel = harita_yon.map_grid[harita_yon.aktif_katman][grid_y][grid_x]
                if parsel.uzerindeki_alet is None:
                    arac_adi = arac_adlari[arac_secimi]
                    if arac_kullanim[arac_adi] < arac_limitleri[arac_adi]:
                        try:
                            arac_sinif = arac_listesi[arac_secimi]
                            if arac_sinif == Mancinik:
                                parsel.uzerindeki_alet = arac_sinif(grid_x, grid_y, harita_yon.aktif_katman, 'sert', arac_secimi)
                            else:
                                parsel.uzerindeki_alet = arac_sinif(grid_x, grid_y, harita_yon.aktif_katman, arac_secimi)
                            if arac_sinif == Bariyer:
                                parsel.yurunebilir = False
                            arac_kullanim[arac_adi] += 1
                        except Exception as ex:
                            print(f"Arac yerlestirme hatasi ({arac_adi}): {ex}")

        def oyunda_arac_kaldir():
            mx, my = pygame.mouse.get_pos()
            grid_x = mx // PARSEK_BOYUTU
            grid_y = my // PARSEK_BOYUTU
            if 0 <= grid_x < HARITA_GENISLIK_PARSEL and 0 <= grid_y < HARITA_YUKSEKLIK_PARSEL:
                parsel = harita_yon.map_grid[harita_yon.aktif_katman][grid_y][grid_x]
                if parsel and parsel.uzerindeki_alet:
                    tur = parsel.uzerindeki_alet.arac_turu
                    if isinstance(tur, int) and 0 <= tur < len(arac_adlari):
                        arac_kullanim[arac_adlari[tur]] = max(0, arac_kullanim[arac_adlari[tur]] - 1)
                    parsel.uzerindeki_alet = None
                    parsel.yurunebilir = True

        def oyunda_etki_alani_goster(surface):
            mx, my = pygame.mouse.get_pos()
            grid_x = mx // PARSEK_BOYUTU
            grid_y = my // PARSEK_BOYUTU
            if 0 <= grid_x < HARITA_GENISLIK_PARSEL and 0 <= grid_y < HARITA_YUKSEKLIK_PARSEL:
                for dy in range(-ETKI_YARICAPI, ETKI_YARICAPI + 1):
                    for dx in range(-ETKI_YARICAPI, ETKI_YARICAPI + 1):
                        nx, ny = grid_x + dx, grid_y + dy
                        if 0 <= nx < HARITA_GENISLIK_PARSEL and 0 <= ny < HARITA_YUKSEKLIK_PARSEL:
                            px_x = nx * PARSEK_BOYUTU
                            px_y = ny * PARSEK_BOYUTU
                            pygame.draw.rect(surface, (255, 255, 0), pygame.Rect(px_x, px_y, PARSEK_BOYUTU, PARSEK_BOYUTU), 2)

        ajan_izleyici = AjanIzlemePenceresi(kutu_sayisi=50)
        calisiyor = True
        oyun_sonucu = "menu"
        kare_sayaci = 0

        while calisiyor:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    calisiyor = False
                    oyun_sonucu = "quit"
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        secim = oyun_ici_menu(ekran, ui_fontu, ui_fontu, clock)
                        if secim == "quit":
                            calisiyor = False
                            oyun_sonucu = "quit"
                        elif secim == "menu":
                            calisiyor = False
                            oyun_sonucu = "menu"
                        continue

                    if ses_menusu.tus_isle(event):
                        continue
                    if ajan_izleyici.tus_isle(event):
                        continue
                    if event.key == pygame.K_m:
                        yeni_mod = suru_yon.oyun_modu_degistir(1)
                        log_yon.olaylari_yaz([
                            {
                                "tip": "mod_degisim",
                                "tick": suru_yon.toplam_tick,
                                "mod": yeni_mod,
                                "kaynak": "M",
                            }
                        ])
                        continue
                    if event.key == pygame.K_F3:
                        if suru_yon.oyun_modu_ayarla("normal"):
                            log_yon.olaylari_yaz([{"tip": "mod_degisim", "tick": suru_yon.toplam_tick, "mod": "normal", "kaynak": "F3"}])
                        continue
                    if event.key == pygame.K_F4:
                        if suru_yon.oyun_modu_ayarla("kesif"):
                            log_yon.olaylari_yaz([{"tip": "mod_degisim", "tick": suru_yon.toplam_tick, "mod": "kesif", "kaynak": "F4"}])
                        continue
                    if event.key == pygame.K_F5:
                        if suru_yon.oyun_modu_ayarla("gezinti"):
                            log_yon.olaylari_yaz([{"tip": "mod_degisim", "tick": suru_yon.toplam_tick, "mod": "gezinti", "kaynak": "F5"}])
                        continue
                    if event.key == pygame.K_F6:
                        if suru_yon.oyun_modu_ayarla("yol_izleme"):
                            log_yon.olaylari_yaz([{"tip": "mod_degisim", "tick": suru_yon.toplam_tick, "mod": "yol_izleme", "kaynak": "F6"}])
                        continue
                    if event.key == pygame.K_UP:
                        harita_yon.aktif_katmani_degistir(harita_yon.aktif_katman + 1)
                    elif event.key == pygame.K_DOWN:
                        harita_yon.aktif_katmani_degistir(harita_yon.aktif_katman - 1)
                    elif arac_paneli.klavye_secimi(event):
                        arac_secimi = arac_paneli.secili_index
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if ajan_izleyici.tus_isle(event):
                        continue
                    if arac_paneli.mouse_secimi(event):
                        arac_secimi = arac_paneli.secili_index
                        continue
                    if event.button == 1:
                        mod_degisti = False
                        for dugme in mod_dugmeleri_uret(suru_yon):
                            if dugme["rect"].collidepoint(event.pos):
                                if suru_yon.oyun_modu_ayarla(dugme["mod"]):
                                    log_yon.olaylari_yaz([
                                        {
                                            "tip": "mod_degisim",
                                            "tick": suru_yon.toplam_tick,
                                            "mod": dugme["mod"],
                                            "kaynak": "harita_dugme",
                                        }
                                    ])
                                mod_degisti = True
                                break
                        if mod_degisti:
                            continue
                        oyunda_arac_yerlestir()
                        if ses_menusu.efekt_aktif() and ses_arac_yerlestir:
                            ses_arac_yerlestir.play()
                    elif event.button == 3:
                        oyunda_arac_kaldir()

            if not calisiyor:
                break

            harita_yon.arac_etkilerini_uygula(suru_yon.ajanlar)
            suru_yon.guncelle()
            oyun_yon.guncelle()
            ajan_izleyici.guncelle(suru_yon.ajanlar, suru_yon)

            log_yon.olaylari_yaz(suru_yon.olum_olaylarini_al())
            kare_sayaci += 1
            if kare_sayaci % max(1, LOG_KARE_ARALIGI) == 0:
                log_yon.anlik_durum_yaz(suru_yon.toplam_tick, suru_yon.ajanlar, suru_yon)

            if sid_manager.available:
                sid_manager.update()

            harita_yon.render(ekran, oyun_fontu)
            suru_yon.render(ekran, oyun_fontu, harita_yon.aktif_katman)
            ciz_giris_cikis_isaretleri(ekran, harita_yon)
            ciz_mod_dugmeleri(ekran, ui_fontu, suru_yon)

            oyunda_etki_alani_goster(ekran)
            oyun_yon.render(ekran, oyun_fontu)
            arac_paneli.ciz(ekran, ui_fontu, arac_kullanim, arac_limitleri)

            ajan_izleyici.ciz(ekran)
            arac_adi = arac_adlari[arac_secimi]
            secili_arac_etiketi_ciz(ekran, ui_fontu, arac_adi)
            if ses_menusu.acik:
                ses_menusu.ciz(ekran, ui_fontu)
            else:
                cubuk_y = HARITA_ALAN_YUKSEKLIK + ARAC_PANEL_YUKSEKLIK
                pygame.draw.rect(ekran, KOYU_GRI, pygame.Rect(0, cubuk_y, EKRAN_GENISLIK, DURUM_CUBUGU_YUKSEKLIK))
                pygame.draw.line(ekran, GRI, (0, cubuk_y), (EKRAN_GENISLIK, cubuk_y), 2)

                toplam_ajan = max(1, oyun_yon.baslangic_nufusu)
                cikis_sayisi = oyun_yon.dogru_cikis
                basari_orani = (cikis_sayisi * 100.0) / toplam_ajan
                kalan_sayi = len(suru_yon.ajanlar)

                bilgi = (
                    f"Katman: {harita_yon.aktif_katman + 1}/{harita_yon.max_katman} | Basari: {basari_orani:.0f}% ({cikis_sayisi}/{toplam_ajan}) | Suru: {kalan_sayi}/{toplam_ajan} | "
                    f"Araç: {arac_adi} ({arac_kullanim[arac_adi]}/{arac_limitleri[arac_adi]}) | "
                    f"Mod: {suru_yon.oyun_modu_etiket()} | "
                    "Etki: 5x5x5 | Harita Ustu Dugmeler: Mod Degistir | 1-0 / Shift+1-0 sec | Sol: yerlestir | Sag: kaldir | Yukari/Asagi: Katman | M: Mod Siradaki | F3:F6 Mod Sec | ESC: Oyun Menusu | F1: Ses | F2 / `: Oyun Bilgi"
                )
                ekran.blit(ui_fontu.render(bilgi, True, (235, 235, 235)), (10, cubuk_y + 8))
                # Faz 8 madde 3: araç mini satırı — tüm araçların kısayol/miktar özeti
                _harf = '1234567890' * 2
                _kisa_adlar = ['Mnc', 'Ayn', 'Bar', 'Ats', 'CkO', 'ShY', 'Snd', 'GCk', 'KMk', 'Ynl', 'Frm', 'Efg', 'Krg', 'Dnm', 'Dpr', 'SyA', 'EyN', 'SsY', 'GlR', 'KsC']
                mini_parcalar = [
                    f"[{_harf[i]}]{_kisa_adlar[i]}:{arac_kullanim.get(arac_adlari[i],0)}/{arac_limitleri.get(arac_adlari[i],0)}"
                    for i in range(len(arac_adlari))
                ]
                mini_yazi = '  '.join(mini_parcalar)
                mini_surf = ui_fontu.render(mini_yazi, True, (200, 215, 235))
                ekran.blit(mini_surf, (10, cubuk_y + 34))

            pygame.display.flip()
            clock.tick(FPS)

        if sid_manager.available:
            sid_manager.stop()
        ajan_izleyici.tamamen_kapat()
        log_yon.kapat()

        if oyun_sonucu == "menu":
            continue

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    main()