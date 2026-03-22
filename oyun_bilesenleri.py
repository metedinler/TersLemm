import json
import os
from datetime import datetime

import pygame

try:
    import tkinter as tk
except Exception:
    tk = None

from ayarlar import *


class SesAyarMenusu:
    """Ses/efekt/muzik anahtarlarini tek bir yerde yoneten basit menudur."""

    def __init__(self, sid_manager, ses_durum):
        self.acik = False
        self.sessiz = False
        self.efekt = SES_ACIK
        self.muzik = MUZIK_ACIK
        self.sid_manager = sid_manager
        self.ses_durum = ses_durum

    def muzik_aktif(self):
        return (not self.sessiz) and self.muzik

    def efekt_aktif(self):
        return (not self.sessiz) and self.efekt

    def uygula(self):
        self.ses_durum["efekt"] = self.efekt_aktif()
        if self.sid_manager.available:
            if self.muzik_aktif():
                self.sid_manager.start()
            else:
                self.sid_manager.stop()
        else:
            if self.muzik_aktif():
                try:
                    if not pygame.mixer.music.get_busy():
                        pygame.mixer.music.load(MUZIK_DOSYASI.replace(".sid", ".wav"))
                        pygame.mixer.music.play(-1)
                    else:
                        pygame.mixer.music.unpause()
                except Exception:
                    pass
            else:
                pygame.mixer.music.pause()

    def tus_isle(self, event):
        if event.key == pygame.K_F1:
            self.acik = not self.acik
            return True
        if not self.acik:
            return False
        if event.key == pygame.K_1:
            self.sessiz = not self.sessiz
            self.uygula()
            return True
        if event.key == pygame.K_2:
            self.efekt = not self.efekt
            self.uygula()
            return True
        if event.key == pygame.K_3:
            self.muzik = not self.muzik
            self.uygula()
            return True
        return False

    def ciz(self, surface, font):
        cubuk_y = HARITA_ALAN_YUKSEKLIK
        pygame.draw.rect(surface, KOYU_GRI, pygame.Rect(0, cubuk_y, EKRAN_GENISLIK, DURUM_CUBUGU_YUKSEKLIK))
        pygame.draw.line(surface, GRI, (0, cubuk_y), (EKRAN_GENISLIK, cubuk_y), 2)
        yazi = (
            f"F1: Ses Menusu | 1 Sessiz: {'ACIK' if self.sessiz else 'KAPALI'} | "
            f"2 Efekt: {'ACIK' if self.efekt_aktif() else 'KAPALI'} | "
            f"3 Muzik: {'ACIK' if self.muzik_aktif() else 'KAPALI'}"
        )
        surface.blit(font.render(yazi, True, (235, 235, 235)), (10, cubuk_y + 16))


class AjanIzlemePenceresi:
    """Ajanlari canli izlemek icin acilir/kapanir ikinci pencere."""

    def __init__(self, kutu_sayisi=50):
        self.kutu_sayisi = kutu_sayisi
        self.acik = False
        self.root = None
        self.canvas = None
        self.kutular = []
        self.etiketler = []
        self.secili_ajan_id = None
        self.ajanlar_kaynagi = []

    def _pencere_kur(self):
        if tk is None:
            print("Tkinter bulunamadi.")
            return False
        if self.root is not None:
            return True

        try:
            self.root = tk.Tk()
            self.root.title("Ajan Durum Izleyici")
            # Oyun penceresi (1280px) ile yan yana sigmasi icin dar bir genislik secildi.
            self.root.geometry("640x900")
            self.root.config(bg="#111111")

            # Tek sutun duzen: en ustte kutular, altta 3 farkli bilgi paneli.
            self.root.grid_rowconfigure(0, weight=3)
            self.root.grid_rowconfigure(1, weight=2)
            self.root.grid_rowconfigure(2, weight=2)
            self.root.grid_rowconfigure(3, weight=2)
            self.root.grid_columnconfigure(0, weight=1)

            self.canvas = tk.Canvas(self.root, width=620, height=340, bg="#1a1a1a", highlightthickness=0)
            self.canvas.grid(row=0, column=0, padx=8, pady=8, sticky="nsew")
            self.canvas.bind("<Button-1>", self._canvas_click)
            self._kutulari_olustur()

            frame_detay = tk.LabelFrame(self.root, text="Ajan Detaylari", bg="#1a1a1a", fg="#ccc", font=("Consolas", 10, "bold"))
            frame_detay.grid(row=1, column=0, padx=8, pady=4, sticky="nsew")
            self.text_detay = tk.Text(frame_detay, height=12, width=72, bg="#0a0a0a", fg="#0f0", font=("Consolas", 9))
            self.text_detay.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

            frame_ai = tk.LabelFrame(self.root, text="Yapay Zeka Bilgileri", bg="#1a1a1a", fg="#ccc", font=("Consolas", 10, "bold"))
            frame_ai.grid(row=2, column=0, padx=8, pady=4, sticky="nsew")
            self.text_ai = tk.Text(frame_ai, height=10, width=72, bg="#0a0a0a", fg="#0ff", font=("Consolas", 9))
            self.text_ai.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

            frame_suru = tk.LabelFrame(self.root, text="Suru Istatistikleri", bg="#1a1a1a", fg="#ccc", font=("Consolas", 10, "bold"))
            frame_suru.grid(row=3, column=0, padx=8, pady=4, sticky="nsew")
            self.text_suru = tk.Text(frame_suru, height=8, width=72, bg="#0a0a0a", fg="#ff0", font=("Consolas", 9))
            self.text_suru.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

            self.root.protocol("WM_DELETE_WINDOW", self.kapat)
            # Baslangicta secili/acik gelmesin diye gizli baslatilir.
            self.root.withdraw()
            self.acik = False
            return True
        except Exception as ex:
            print(f"Ajan pencere kurulum hatasi: {ex}")
            self.acik = False
            return False

    def ac(self):
        if not self._pencere_kur():
            return
        self.acik = True
        self.root.deiconify()
        self.root.lift()

    def ac_kapat(self):
        if self.acik:
            self.kapat()
        else:
            self.ac()

    def _kutulari_olustur(self):
        sutun = 10
        satir = 5
        kutu_w = 58
        kutu_h = 58
        bosluk = 4
        idx = 0

        for r in range(satir):
            for c in range(sutun):
                if idx >= self.kutu_sayisi:
                    return
                x1 = c * (kutu_w + bosluk)
                y1 = r * (kutu_h + bosluk)
                x2 = x1 + kutu_w
                y2 = y1 + kutu_h
                rect = self.canvas.create_rectangle(x1, y1, x2, y2, fill="#2d2d2d", outline="#666666", width=1, tags=f"ajan_{idx}")
                txt = self.canvas.create_text((x1 + x2) // 2, (y1 + y2) // 2, text=f"{idx}\n-", fill="#f0f0f0", font=("Consolas", 9, "bold"), tags=f"txt_{idx}")
                self.kutular.append(rect)
                self.etiketler.append(txt)
                idx += 1

    def _canvas_click(self, event):
        x, y = event.x, event.y
        kutu_w = 58
        kutu_h = 58
        bosluk = 4

        col = x // (kutu_w + bosluk)
        row = y // (kutu_h + bosluk)

        if 0 <= col < 10 and 0 <= row < 5:
            ajan_idx = row * 10 + col
            if ajan_idx < len(self.ajanlar_kaynagi):
                self.secili_ajan_id = ajan_idx
                self.canvas.itemconfig(self.kutular[ajan_idx], outline="#ffff00", width=3)

    def _olustur_detay_metni(self, ajan):
        detay = f"=== AJAN {ajan.id} DETAYLARI ===\n"
        detay += f"Kimlik : {ajan.id}\n"
        detay += f"Konum  : ({ajan.x}, {ajan.y}, {ajan.z})\n"
        detay += f"Yon    : {ajan.yon}\n"
        detay += f"Hayatta: {ajan.hayatta}\n"
        detay += f"Lider  : {ajan.lider_mi}\n"
        detay += f"Can    : {ajan.can:6.2f}\n"
        detay += "Zincir Durumu:\n"
        detay += f"  Oncu: {ajan.onumdeki_ajan.id if ajan.onumdeki_ajan else 'Yok'}\n"
        detay += f"  Arka: {ajan.arkamdaki_ajan.id if ajan.arkamdaki_ajan else 'Yok'}\n"

        detay += "\nDUYGULAR:\n"
        # Sayisal hizalama icin sabit kolonlar kullanilir.
        for d, v in ajan.duygular.items():
            detay += f"  {d:12s}: {v:6.1f}\n"

        detay += "\nBECERILER:\n"
        for b, v in ajan.beceriler.items():
            detay += f"  {b:12s}: {v:6.2f}\n"

        if hasattr(ajan, "cikis_bilgisi"):
            detay += f"\nCikis Bilgisi: {ajan.cikis_bilgisi:6.2f}\n"

        if hasattr(ajan, "gazi_mi"):
            detay += f"Gazi: {ajan.gazi_mi} (puan: {ajan.gazi_puani:6.1f})\n"

        return detay

    def _olustur_ai_metni(self, ajan):
        ai = f"=== YAPAY ZEKA [{ajan.id}] ===\n"

        if hasattr(ajan, "mod"):
            ai += f"Mod       : {ajan.mod}\n"

        if hasattr(ajan, "kavramsal_durum"):
            ai += f"Kavramsal : {ajan.kavramsal_durum}\n"

        if hasattr(ajan, "yol") and ajan.yol:
            ai += f"Yol Takibi: {ajan.yol_index}/{len(ajan.yol)}\n"
            if ajan.yol_index < len(ajan.yol):
                hedef = ajan.yol[ajan.yol_index]
                ai += f"Hedef     : ({hedef[0]}, {hedef[1]}, {hedef[2]})\n"
            else:
                ai += "Hedef     : Varis Noktasi\n"
        else:
            ai += "Yol       : Bulunamadi\n"

        if hasattr(ajan, "biyolojik_sistem"):
            bio = ajan.biyolojik_sistem
            ai += "\nHORMONLAR:\n"
            # Kullanici istegine gore hormonlar alt alta ve hizali yazilir.
            for h, v in bio.hormonlar.items():
                ai += f"  {h:12s}: {v:6.1f}\n"

        if hasattr(ajan, "kopma_islendi"):
            ai += f"\nKopma Islendi: {ajan.kopma_islendi}\n"

        return ai

    def _olustur_suru_metni(self, ajanlar):
        suru = f"=== SURU ISTATISTIKLERI ({len(ajanlar)} Ajan) ===\n"

        hayatta = sum(1 for a in ajanlar if a.hayatta)
        liderler = sum(1 for a in ajanlar if a.lider_mi)
        gaziler = sum(1 for a in ajanlar if getattr(a, "gazi_mi", False))

        suru += f"Toplam: {len(ajanlar)} | Hayatta: {hayatta} | Liderler: {liderler} | Gaziler: {gaziler}\n"

        if ajanlar:
            ort_korku = sum(a.duygular.get("korku", 0) for a in ajanlar) / len(ajanlar)
            ort_merak = sum(a.duygular.get("merak", 0) for a in ajanlar) / len(ajanlar)
            ort_suphe = sum(a.duygular.get("suphe", 0) for a in ajanlar) / len(ajanlar)
            suru += f"\nDuygu Ortalamalari\n"
            suru += f"  Korku : {ort_korku:6.1f}\n"
            suru += f"  Merak : {ort_merak:6.1f}\n"
            suru += f"  Suphe : {ort_suphe:6.1f}\n"

        suru += "\nZINCIR YAPISI:\n"
        lider_ajanlar = [a for a in ajanlar if a.lider_mi]
        for idx, lider in enumerate(lider_ajanlar):
            zincir_boyutu = 1
            ajan = lider
            while ajan.arkamdaki_ajan:
                ajan = ajan.arkamdaki_ajan
                zincir_boyutu += 1
            suru += f"  Suru {idx+1}: Lider={lider.id} Uzunluk={zincir_boyutu}\n"

        tek_ajanlar = [a for a in ajanlar if not a.lider_mi and not a.onumdeki_ajan]
        if tek_ajanlar:
            suru += f"\nTek Ajanlar: {[a.id for a in tek_ajanlar]}\n"

        return suru

    def guncelle(self, ajanlar):
        if not self.acik:
            return
        try:
            self.ajanlar_kaynagi = ajanlar

            for i in range(self.kutu_sayisi):
                if i < len(ajanlar):
                    ajan = ajanlar[i]
                    if ajan.lider_mi:
                        renk = "#1f6feb"
                        durum = "L"
                    elif getattr(ajan, "gazi_mi", False):
                        renk = "#ff8800"
                        durum = "G"
                    elif ajan.duygular.get("korku", 0) > 50:
                        renk = "#d73a49"
                        durum = "K"
                    elif ajan.duygular.get("merak", 0) > 50:
                        renk = "#f2cc60"
                        durum = "M"
                    else:
                        renk = "#2ea043"
                        durum = "S"

                    outline = "#ffff00" if i == self.secili_ajan_id else "#666666"
                    width = 3 if i == self.secili_ajan_id else 1
                    self.canvas.itemconfig(self.kutular[i], fill=renk, outline=outline, width=width)
                    self.canvas.itemconfig(self.etiketler[i], text=f"{ajan.id}\n{durum}:{int(ajan.can)}")
                else:
                    self.canvas.itemconfig(self.kutular[i], fill="#2d2d2d", outline="#666666", width=1)
                    self.canvas.itemconfig(self.etiketler[i], text=f"{i}\n-")

            self.text_detay.config(state=tk.NORMAL)
            self.text_detay.delete("1.0", tk.END)
            if self.secili_ajan_id is not None and self.secili_ajan_id < len(ajanlar):
                self.text_detay.insert("1.0", self._olustur_detay_metni(ajanlar[self.secili_ajan_id]))
            self.text_detay.config(state=tk.DISABLED)

            self.text_ai.config(state=tk.NORMAL)
            self.text_ai.delete("1.0", tk.END)
            if self.secili_ajan_id is not None and self.secili_ajan_id < len(ajanlar):
                self.text_ai.insert("1.0", self._olustur_ai_metni(ajanlar[self.secili_ajan_id]))
            self.text_ai.config(state=tk.DISABLED)

            self.text_suru.config(state=tk.NORMAL)
            self.text_suru.delete("1.0", tk.END)
            self.text_suru.insert("1.0", self._olustur_suru_metni(ajanlar))
            self.text_suru.config(state=tk.DISABLED)

            self.root.update_idletasks()
            self.root.update()
        except Exception as ex:
            print(f"Ajan izleme guncelleme hatasi: {ex}")
            self.kapat()

    def kapat(self):
        self.acik = False
        if self.root is not None:
            try:
                self.root.withdraw()
            except Exception:
                pass

    def tamamen_kapat(self):
        self.acik = False
        if self.root is not None:
            try:
                self.root.destroy()
            except Exception:
                pass
            self.root = None


class OyunKayitYonetici:
    """Oyundaki olaylari ve anlik suru durumunu JSONL olarak saklar."""

    def __init__(self):
        self.acik = False
        self.dosya = None
        try:
            log_dir = os.path.join(".", "loglar")
            os.makedirs(log_dir, exist_ok=True)
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            self.log_yolu = os.path.join(log_dir, f"oyun_log_{ts}.jsonl")
            self.dosya = open(self.log_yolu, "a", encoding="utf-8")
            self.acik = True
            print(f"LOG: {self.log_yolu}")
        except Exception as ex:
            self.log_yolu = None
            print(f"Log dosyasi acilamadi: {ex}")

    def _yaz(self, kayit):
        if not self.acik or self.dosya is None:
            return
        self.dosya.write(json.dumps(kayit, ensure_ascii=False) + "\n")
        self.dosya.flush()

    def baslangic(self, zorluk_ayari, ajan_sayisi):
        self._yaz(
            {
                "tip": "baslangic",
                "zaman": datetime.now().isoformat(timespec="seconds"),
                "zorluk": zorluk_ayari,
                "ajan_sayisi": ajan_sayisi,
            }
        )

    def olaylari_yaz(self, olaylar):
        for olay in olaylar:
            self._yaz({"tip": "olay", "zaman": datetime.now().isoformat(timespec="seconds"), "veri": olay})

    def anlik_durum_yaz(self, tick, ajanlar):
        self._yaz(
            {
                "tip": "anlik_durum",
                "zaman": datetime.now().isoformat(timespec="seconds"),
                "tick": tick,
                "ajanlar": [
                    {
                        "id": a.id,
                        "lider": a.lider_mi,
                        "x": a.x,
                        "y": a.y,
                        "z": a.z,
                        "can": round(a.can, 2),
                        "hayatta": a.hayatta,
                        "duygular": {
                            "korku": round(a.duygular.get("korku", 0), 2),
                            "merak": round(a.duygular.get("merak", 0), 2),
                            "suphe": round(a.duygular.get("suphe", 0), 2),
                        },
                        "hormonlar": {
                            k: round(v, 2)
                            for k, v in getattr(getattr(a, "biyolojik_sistem", None), "hormonlar", {}).items()
                        },
                        "kavramsal_durum": getattr(a, "kavramsal_durum", "KULLANILABILIR"),
                        "mod": getattr(a, "mod", "DENGELI"),
                        "gazi": getattr(a, "gazi_mi", False),
                        "yol_index": getattr(a, "yol_index", 0),
                    }
                    for a in ajanlar
                ],
            }
        )

    def kapat(self):
        if self.dosya is not None:
            try:
                self.dosya.close()
            except Exception:
                pass
        self.acik = False


class OyunYoneticisi:
    """Kazanma/kaybetme ve can/cikis sayimlarini yonetir."""

    def __init__(self, suru_yon, ses_durum, ses_ajan_ol):
        self.suru_yon = suru_yon
        self.ses_durum = ses_durum
        self.ses_ajan_ol = ses_ajan_ol
        self.baslangic_nufusu = len(suru_yon.ajanlar)
        self.olenler = 0
        self.dogru_cikis = 0
        self.sahte_cikis = 0
        self.kazanma_kosulu = False
        self.kaybetme_kosulu = False

    def guncelle(self):
        for ajan in self.suru_yon.ajanlar[:]:
            if ajan.can <= 0:
                ajan.hayatta = False
                self.suru_yon.kayit_olum_olayi(ajan, neden="can_bitti")
                self.suru_yon.ajanlar.remove(ajan)
                if self.ses_durum["efekt"] and self.ses_ajan_ol:
                    self.ses_ajan_ol.play()
                continue

            parsel = self.suru_yon.harita.map_grid[ajan.z][ajan.y][ajan.x]
            if parsel.doku_id == "CIKIS_DOGRU":
                self.dogru_cikis += 1
                self.suru_yon.ajanlar.remove(ajan)
            elif parsel.doku_id == "CIKIS_SAHTE":
                self.sahte_cikis += 1
                self.suru_yon.ajanlar.remove(ajan)

        self.olenler = max(0, self.baslangic_nufusu - len(self.suru_yon.ajanlar) - self.dogru_cikis - self.sahte_cikis)

        kalan = self.baslangic_nufusu - self.olenler - self.dogru_cikis - self.sahte_cikis
        if kalan == 0:
            if self.dogru_cikis / self.baslangic_nufusu <= 0.1:
                self.kazanma_kosulu = True
            else:
                self.kaybetme_kosulu = True

    def render(self, surface, font):
        yazi = f"Olen: {self.olenler} | Dogru: {self.dogru_cikis} | Sahte: {self.sahte_cikis}"
        surface.blit(font.render(yazi, True, KIRMIZI), (10, 10))
        if self.kazanma_kosulu:
            surface.blit(font.render("KAZANDIN!", True, YESIL), (EKRAN_GENISLIK // 2 - 50, EKRAN_YUKSEKLIK // 2))
        elif self.kaybetme_kosulu:
            surface.blit(font.render("KAYBETTIN!", True, KIRMIZI), (EKRAN_GENISLIK // 2 - 50, EKRAN_YUKSEKLIK // 2))


def secili_arac_etiketi_ciz(surface, font, arac_adi):
    panel = pygame.Rect(EKRAN_GENISLIK - 290, 8, 280, 36)
    pygame.draw.rect(surface, (20, 20, 20), panel)
    pygame.draw.rect(surface, (240, 210, 90), panel, 2)
    yazi = font.render(f"Secili Arac: {arac_adi}", True, (255, 245, 180))
    surface.blit(yazi, (panel.x + 10, panel.y + 8))


def oyun_ici_menu(ekran, baslik_font, bilgi_font, clock):
    """ESC ile acilan kucuk menu: devam veya oyunu menuye don."""
    secim = 0
    secenekler = ["Devam Et", "Menuden Oyunu Bitir"]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "devam"
                if event.key == pygame.K_UP:
                    secim = (secim - 1) % len(secenekler)
                elif event.key == pygame.K_DOWN:
                    secim = (secim + 1) % len(secenekler)
                elif event.key == pygame.K_RETURN:
                    return "devam" if secim == 0 else "menu"

        panel = pygame.Rect(EKRAN_GENISLIK // 2 - 260, EKRAN_YUKSEKLIK // 2 - 120, 520, 220)
        pygame.draw.rect(ekran, (20, 24, 30), panel)
        pygame.draw.rect(ekran, (120, 170, 230), panel, 2)

        ekran.blit(baslik_font.render("OYUN MENUSU", True, (230, 236, 245)), (panel.x + 145, panel.y + 24))
        for i, secenek in enumerate(secenekler):
            renk = (255, 225, 120) if i == secim else (205, 214, 224)
            on_ek = "> " if i == secim else "  "
            ekran.blit(baslik_font.render(on_ek + secenek, True, renk), (panel.x + 70, panel.y + 78 + i * 44))

        ekran.blit(
            bilgi_font.render("Yukari/Asagi: Secim  |  Enter: Onay  |  ESC: Devam", True, (165, 176, 190)),
            (panel.x + 36, panel.y + 185),
        )
        pygame.display.flip()
        clock.tick(FPS)
