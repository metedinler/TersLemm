import json
import math
import os
from datetime import datetime

import pygame

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
        cubuk_y = HARITA_ALAN_YUKSEKLIK + ARAC_PANEL_YUKSEKLIK
        pygame.draw.rect(surface, KOYU_GRI, pygame.Rect(0, cubuk_y, EKRAN_GENISLIK, DURUM_CUBUGU_YUKSEKLIK))
        pygame.draw.line(surface, GRI, (0, cubuk_y), (EKRAN_GENISLIK, cubuk_y), 2)
        yazi = (
            f"F1: Ses Menusu | 1 Sessiz: {'ACIK' if self.sessiz else 'KAPALI'} | "
            f"2 Efekt: {'ACIK' if self.efekt_aktif() else 'KAPALI'} | "
            f"3 Muzik: {'ACIK' if self.muzik_aktif() else 'KAPALI'}"
        )
        surface.blit(font.render(yazi, True, (235, 235, 235)), (10, cubuk_y + 16))


class AjanBilgiOverlay:
    """Oyun alaninin saginda acilip kapanan sabit bilgi paneli."""

    def __init__(self, kutu_sayisi=50, panel_genislik=YAN_PANEL_GENISLIK):
        self.acik = False
        self.kutu_sayisi = kutu_sayisi
        self.panel_genislik = panel_genislik
        self.ajanlar = []
        self.suru_yon = None
        self.secili_idx = None
        self.detay_scroll = 0
        self.ham_veri_modu = False
        self._sutun = 10
        try:
            self._fb = pygame.font.SysFont("Consolas", 14, bold=True)
            self._fa = pygame.font.SysFont("Consolas", 12, bold=True)
            self._fk = pygame.font.SysFont("Consolas", 11)
        except Exception:
            self._fb = pygame.font.SysFont(None, 15, bold=True)
            self._fa = pygame.font.SysFont(None, 13, bold=True)
            self._fk = pygame.font.SysFont(None, 12)

    def ac(self):
        self.acik = True

    def ac_kapat(self):
        self.acik = not self.acik

    def guncelle(self, ajanlar, suru_yon=None):
        self.ajanlar = list(ajanlar)
        if suru_yon is not None:
            self.suru_yon = suru_yon
        if self.secili_idx is not None and self.secili_idx >= len(self.ajanlar):
            self.secili_idx = None
            self.detay_scroll = 0

    def tamamen_kapat(self):
        self.acik = False

    def tus_isle(self, event):
        if event.type == pygame.KEYDOWN and (event.key == pygame.K_F2 or event.key == pygame.K_BACKQUOTE):
            self.ac_kapat()
            return True
        if self.acik and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_TAB:
                self.ham_veri_modu = not self.ham_veri_modu
                self.detay_scroll = 0
                return True
            if event.key == pygame.K_PAGEUP:
                self.detay_scroll = max(0, self.detay_scroll - 8)
                return True
            if event.key == pygame.K_PAGEDOWN:
                self.detay_scroll += 8
                return True
            if event.key == pygame.K_HOME:
                self.detay_scroll = 0
                return True
        if self.acik and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pw = self.panel_genislik
            px = OYUN_ALAN_GENISLIK
            gbs = 36
            x0 = px + 10
            y0 = 58
            mx, my = event.pos
            if mx >= px:
                for i in range(min(len(self.ajanlar), self.kutu_sayisi)):
                    col = i % self._sutun
                    sat = i // self._sutun
                    ax = x0 + col * (gbs + 4)
                    ay = y0 + sat * (gbs + 4)
                    if ax <= mx <= ax + gbs and ay <= my <= ay + gbs:
                        self.secili_idx = i
                        self.detay_scroll = 0
                        return True
        return False

    def _secili_ajan(self):
        if self.secili_idx is None or self.secili_idx >= len(self.ajanlar):
            return None
        return self.ajanlar[self.secili_idx]

    def _detay_satirlari(self, ajan):
        satirlar = [
            f"=== AJAN {ajan.id} DETAYLARI ===",
            f"Kimlik : {ajan.id}",
            f"Konum  : ({ajan.x}, {ajan.y}, {ajan.z})",
            f"Yon    : {getattr(ajan, 'yon', '?')}",
            f"Hayatta: {ajan.hayatta}",
            f"Lider  : {ajan.lider_mi}",
            f"Can    : {ajan.can:6.2f}",
            "Zincir Durumu:",
            f"  Oncu: {ajan.onumdeki_ajan.id if ajan.onumdeki_ajan else 'Yok'}",
            f"  Arka: {ajan.arkamdaki_ajan.id if ajan.arkamdaki_ajan else 'Yok'}",
            "",
            "DUYGULAR:",
        ]
        for ad, deger in ajan.duygular.items():
            satirlar.append(f"  {ad:12s}: {deger:6.1f}")
        satirlar.append("")
        satirlar.append("BECERILER:")
        for ad, deger in ajan.beceriler.items():
            satirlar.append(f"  {ad:12s}: {deger:6.2f}")
        satirlar.append("")
        satirlar.append(f"Cikis Bilgisi: {getattr(ajan, 'cikis_bilgisi', 0.0):6.2f}")
        satirlar.append(f"Gazi        : {getattr(ajan, 'gazi_mi', False)} ({getattr(ajan, 'gazi_puani', 0.0):6.1f})")
        return satirlar

    def _ai_satirlari(self, ajan):
        satirlar = [f"=== YAPAY ZEKA [{ajan.id}] ==="]
        satirlar.append(f"Mod         : {getattr(ajan, 'mod', '?')}")
        satirlar.append(f"Kavramsal   : {getattr(ajan, 'kavramsal_durum', '?')}")
        if hasattr(ajan, 'yol') and ajan.yol:
            satirlar.append(f"Yol Takibi  : {ajan.yol_index}/{len(ajan.yol)}")
            if ajan.yol_index < len(ajan.yol):
                hedef = ajan.yol[ajan.yol_index]
                satirlar.append(f"Hedef       : ({hedef[0]}, {hedef[1]}, {hedef[2]})")
            else:
                satirlar.append("Hedef       : Varis Noktasi")
        else:
            satirlar.append("Yol         : Bulunamadi")

        son_semantik = getattr(ajan, 'semantik_iz', [])[-1] if getattr(ajan, 'semantik_iz', None) else None
        if son_semantik:
            satirlar.append("")
            satirlar.append("SON ETKILESIM:")
            satirlar.append(f"  Nesne      : {son_semantik.get('nesne', 'BILINMEYEN')}")
            satirlar.append(f"  Kaynak     : {son_semantik.get('kaynak', 'bilinmiyor')}")
            satirlar.append(f"  Etiket     : {son_semantik.get('etiket', 'KULLANILABILIR')}")
            satirlar.append(f"  Tepki      : {son_semantik.get('onerilen_tepki', 'INCELE')}")
            satirlar.append(f"  Amac       : {son_semantik.get('amac', 'nesneyi_anlamlandir')}")

        if hasattr(ajan, 'biyolojik_sistem'):
            satirlar.append("")
            satirlar.append("HORMONLAR:")
            for ad, deger in ajan.biyolojik_sistem.hormonlar.items():
                satirlar.append(f"  {ad:12s}: {deger:6.1f}")

        satirlar.append("")
        satirlar.append(f"Kopma Islendi: {getattr(ajan, 'kopma_islendi', False)}")
        return satirlar

    def _deger_metni(self, deger):
        if isinstance(deger, float):
            return f"{deger:.4f}"
        if isinstance(deger, (int, bool, str)):
            return str(deger)
        if isinstance(deger, dict):
            return f"dict[{len(deger)}]"
        if isinstance(deger, list):
            return f"list[{len(deger)}]"
        if hasattr(deger, "id"):
            return f"<{type(deger).__name__} id={getattr(deger, 'id', '?')}>"
        return f"<{type(deger).__name__}>"

    def _ham_ajan_satirlari(self, ajan):
        satirlar = [f"=== AJAN {ajan.id} HAM DEGISKENLER ==="]
        for ad in sorted(ajan.__dict__.keys()):
            if ad in ["beyin", "biyolojik_sistem", "onumdeki_ajan", "arkamdaki_ajan"]:
                continue
            deger = getattr(ajan, ad, None)
            satirlar.append(f"{ad:20s}: {self._deger_metni(deger)}")

        satirlar.append("")
        satirlar.append("-- BAGLANTILAR --")
        satirlar.append(f"onumdeki_ajan       : {getattr(getattr(ajan, 'onumdeki_ajan', None), 'id', None)}")
        satirlar.append(f"arkamdaki_ajan      : {getattr(getattr(ajan, 'arkamdaki_ajan', None), 'id', None)}")

        satirlar.append("")
        satirlar.append("-- BIYOLOJIK SISTEM --")
        for ad, deger in sorted(getattr(getattr(ajan, "biyolojik_sistem", None), "__dict__", {}).items()):
            satirlar.append(f"bio.{ad:16s}: {self._deger_metni(deger)}")

        satirlar.append("")
        satirlar.append("-- BEYIN --")
        beyin = getattr(ajan, "beyin", None)
        if beyin is not None:
            for ad in ["girdi_sayisi", "gizli_sayisi", "cikti_sayisi"]:
                satirlar.append(f"beyin.{ad:12s}: {self._deger_metni(getattr(beyin, ad, None))}")
            for ad in ["w1", "w2"]:
                agirlik = getattr(beyin, ad, None)
                satirlar.append(f"beyin.{ad:12s}: {self._deger_metni(agirlik)}")
        return satirlar

    def _ust_akil_satirlari(self):
        satirlar = ["=== UST AKIL ==="]
        if self.suru_yon is None:
            satirlar.append("Ust akil bagli degil")
            return satirlar
        satirlar.append(f"Oyun Modu  : {self.suru_yon.oyun_modu_etiket()}")
        satirlar.append(f"Toplam Tick: {getattr(self.suru_yon, 'toplam_tick', 0)}")
        ua = getattr(self.suru_yon, "ust_akil", None)
        if ua is None:
            satirlar.append("Ust akil nesnesi yok")
            return satirlar
        satirlar.append(f"Son Mod    : {getattr(ua, 'son_mod', '?')}")
        son_karar = getattr(ua, "son_karar", {})
        for ad, deger in son_karar.items():
            satirlar.append(f"{ad:10s}: {deger:7.3f}")
        return satirlar

    def _suru_satirlari(self):
        ajanlar = self.ajanlar
        satirlar = [f"=== SURU ISTATISTIKLERI ({len(ajanlar)} Ajan) ==="]
        hayatta = sum(1 for a in ajanlar if a.hayatta)
        liderler = sum(1 for a in ajanlar if a.lider_mi)
        gaziler = sum(1 for a in ajanlar if getattr(a, 'gazi_mi', False))
        satirlar.append(f"Toplam: {len(ajanlar)} | Hayatta: {hayatta} | Liderler: {liderler} | Gaziler: {gaziler}")
        if ajanlar:
            ort_korku = sum(a.duygular.get('korku', 0) for a in ajanlar) / len(ajanlar)
            ort_merak = sum(a.duygular.get('merak', 0) for a in ajanlar) / len(ajanlar)
            ort_suphe = sum(a.duygular.get('suphe', 0) for a in ajanlar) / len(ajanlar)
            satirlar.append("")
            satirlar.append("Duygu Ortalamalari")
            satirlar.append(f"  Korku : {ort_korku:6.1f}")
            satirlar.append(f"  Merak : {ort_merak:6.1f}")
            satirlar.append(f"  Suphe : {ort_suphe:6.1f}")
        satirlar.append("")
        satirlar.append("ZINCIR YAPISI:")
        lider_ajanlar = [a for a in ajanlar if a.lider_mi]
        for idx, lider in enumerate(lider_ajanlar):
            zincir_boyutu = 1
            aday = lider
            while aday.arkamdaki_ajan:
                aday = aday.arkamdaki_ajan
                zincir_boyutu += 1
            satirlar.append(f"  Suru {idx + 1}: Lider={lider.id:02d} Uzunluk={zincir_boyutu:02d}")
        return satirlar

    def ciz(self, surface, _font=None):
        if not self.acik:
            return
        pw = self.panel_genislik
        ph = HARITA_ALAN_YUKSEKLIK
        px = OYUN_ALAN_GENISLIK
        py = 0

        pygame.draw.rect(surface, (10, 12, 18), pygame.Rect(px, py, pw, ph))
        pygame.draw.line(surface, (68, 108, 198), (px, py), (px, py + ph), 2)
        pygame.draw.rect(surface, (22, 26, 34), pygame.Rect(px + 4, py + 4, pw - 8, ph - 8), border_radius=6)

        fb = self._fb
        fa = self._fa
        fk = self._fk

        surface.blit(fb.render("OYUN BILGI EKRANI  [F2 / `]", True, (128, 172, 255)), (px + 10, py + 8))
        pygame.draw.line(surface, (55, 85, 155), (px + 6, py + 30), (px + pw - 6, py + 30), 1)

        hayatta = sum(1 for a in self.ajanlar if a.hayatta)
        liderler = sum(1 for a in self.ajanlar if a.lider_mi)
        gaziler = sum(1 for a in self.ajanlar if getattr(a, 'gazi_mi', False))
        surface.blit(
            fk.render(f"T:{len(self.ajanlar)} H:{hayatta} L:{liderler} G:{gaziler}", True, (175, 205, 255)),
            (px + 10, py + 36),
        )
        pygame.draw.line(surface, (48, 68, 115), (px + 6, py + 52), (px + pw - 6, py + 52), 1)

        gbs = 36
        x0 = px + 10
        y0 = py + 58
        for i, ajan in enumerate(self.ajanlar[: self.kutu_sayisi]):
            col = i % self._sutun
            sat = i // self._sutun
            ax = x0 + col * (gbs + 4)
            ay = y0 + sat * (gbs + 4)
            if ajan.lider_mi:
                fill = (28, 75, 165)
            elif getattr(ajan, 'gazi_mi', False):
                fill = (175, 95, 18)
            elif not ajan.hayatta:
                fill = (70, 70, 70)
            elif ajan.duygular.get('korku', 0) > 50:
                fill = (138, 28, 38)
            elif ajan.duygular.get('merak', 0) > 50:
                fill = (148, 138, 18)
            else:
                fill = (28, 98, 42)
            outline = (255, 238, 75) if i == self.secili_idx else (58, 72, 98)
            bw = 2 if i == self.secili_idx else 1
            pygame.draw.rect(surface, fill, pygame.Rect(ax, ay, gbs, gbs), border_radius=2)
            pygame.draw.rect(surface, outline, pygame.Rect(ax, ay, gbs, gbs), bw, border_radius=2)
            id_s = fk.render(str(ajan.id), True, (215, 222, 232))
            surface.blit(id_s, (ax + gbs // 2 - id_s.get_width() // 2, ay + 1))
            can_r = max(0.0, min(1.0, ajan.can / 100.0))
            cw = int((gbs - 2) * can_r)
            pygame.draw.rect(surface, (75, 215, 75), pygame.Rect(ax + 1, ay + gbs - 5, cw, 4))

        detail_y = y0 + (5 * (gbs + 4)) + 10
        pygame.draw.line(surface, (48, 68, 115), (px + 6, detail_y - 4), (px + pw - 6, detail_y - 4), 1)

        secili = self._secili_ajan()
        sol_x = px + 10
        sat_h = 13
        alt_limit = py + ph - 10

        if secili is None:
            satirlar = ["=== SECIM ===", "Grid'den bir ajan sec.", ""] + self._ust_akil_satirlari() + [""] + self._suru_satirlari()
        else:
            if self.ham_veri_modu:
                satirlar = self._ham_ajan_satirlari(secili) + [""] + self._ust_akil_satirlari() + [""] + self._suru_satirlari()
            else:
                satirlar = (
                    self._detay_satirlari(secili)
                    + [""]
                    + self._ai_satirlari(secili)
                    + [""]
                    + self._ust_akil_satirlari()
                    + [""]
                    + self._suru_satirlari()
                )

        baslik = "DETAY [TAB: Ozet/Ham | PgUp/PgDn: Kaydir]"
        surface.blit(fa.render(baslik, True, (210, 225, 255)), (sol_x, detail_y))

        icerik_y = detail_y + 18
        gorunen_satir = max(4, (alt_limit - icerik_y) // sat_h)
        max_scroll = max(0, len(satirlar) - gorunen_satir)
        self.detay_scroll = max(0, min(self.detay_scroll, max_scroll))

        for ciz_idx, line in enumerate(satirlar[self.detay_scroll:self.detay_scroll + gorunen_satir]):
            y = icerik_y + ciz_idx * sat_h
            if y >= alt_limit:
                break
            renk = (198, 218, 255) if line.startswith("===") else (165, 185, 218)
            surface.blit(fk.render(line, True, renk), (sol_x, y))


# Geriye donuk uyumluluk icin takma ad
AjanIzlemePenceresi = AjanBilgiOverlay


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

    def _r(self, deger):
        if isinstance(deger, float):
            return round(deger, 4)
        if isinstance(deger, dict):
            return {k: self._r(v) for k, v in deger.items()}
        if isinstance(deger, list):
            return [self._r(v) for v in deger]
        return deger

    def anlik_durum_yaz(self, tick, ajanlar, suru_yon=None):
        ust_akil = {}
        oyun_modu = None
        if suru_yon is not None:
            oyun_modu = getattr(suru_yon, "oyun_modu", None)
            ua = getattr(suru_yon, "ust_akil", None)
            if ua is not None:
                ust_akil = {
                    "son_mod": getattr(ua, "son_mod", None),
                    "son_karar": self._r(getattr(ua, "son_karar", {})),
                }

        self._yaz(
            {
                "tip": "anlik_durum",
                "zaman": datetime.now().isoformat(timespec="seconds"),
                "tick": tick,
                "oyun_modu": oyun_modu,
                "ust_akil": ust_akil,
                "ajanlar": [
                    {
                        "id": a.id,
                        "lider": a.lider_mi,
                        "x": a.x,
                        "y": a.y,
                        "z": a.z,
                        "can": round(a.can, 2),
                        "hayatta": a.hayatta,
                        "yon": getattr(a, "yon", None),
                        "hiz": round(getattr(a, "hiz", 0.0), 4),
                        "temel_hiz": round(getattr(a, "temel_hiz", 0.0), 4),
                        "hareket_birikimi": round(getattr(a, "hareket_birikimi", 0.0), 4),
                        "duygular": self._r(getattr(a, "duygular", {})),
                        "mizac": self._r(getattr(a, "mizac", {})),
                        "beceriler": self._r(getattr(a, "beceriler", {})),
                        "hormonlar": self._r(getattr(getattr(a, "biyolojik_sistem", None), "hormonlar", {})),
                        "nn_karar": self._r(getattr(a, "nn_karar", {})),
                        "kavramsal_durum": getattr(a, "kavramsal_durum", "KULLANILABILIR"),
                        "mod": getattr(a, "mod", "DENGELI"),
                        "durum_modu": getattr(a, "durum_modu", "NORMAL"),
                        "kopma_egilimi": round(getattr(a, "kopma_egilimi", 0.0), 4),
                        "kopma_islendi": bool(getattr(a, "kopma_islendi", False)),
                        "gazi": getattr(a, "gazi_mi", False),
                        "gazi_puani": round(getattr(a, "gazi_puani", 0.0), 3),
                        "gazi_omur": int(getattr(a, "gazi_omur", 0)),
                        "cikis_bilgisi": round(getattr(a, "cikis_bilgisi", 0.0), 4),
                        "oncu_id": getattr(getattr(a, "onumdeki_ajan", None), "id", None),
                        "arka_id": getattr(getattr(a, "arkamdaki_ajan", None), "id", None),
                        "nesne_tercihleri": self._r(getattr(a, "nesne_tercihleri", {})),
                        "semantik_son": self._r((getattr(a, "semantik_iz", [])[-1] if getattr(a, "semantik_iz", None) else None)),
                        "semantik_uzunluk": len(getattr(a, "semantik_iz", [])),
                        "yol_index": getattr(a, "yol_index", 0),
                        "yol_uzunlugu": len(getattr(a, "yol", [])),
                        "yol_hedef": self._r(
                            getattr(a, "yol", [])[getattr(a, "yol_index", 0)]
                            if getattr(a, "yol", None) and getattr(a, "yol_index", 0) < len(getattr(a, "yol", []))
                            else None
                        ),
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
        self.evrimsel_sicrama_tetiklendi = False

    def _evrimsel_sicrama_uygula(self):
        """Belgedeki %30 esiginde surunun genel ogrenme katsayisini bir kere artirir."""
        for ajan in self.suru_yon.ajanlar:
            for beceri, deger in ajan.beceriler.items():
                artis = 0.55 if ajan.lider_mi else 0.28
                ajan.beceriler[beceri] = min(10.0, deger + artis)

            hormonlar = ajan.biyolojik_sistem.hormonlar
            hormonlar['dopamin'] = min(100.0, hormonlar.get('dopamin', 0.0) + (8.0 if ajan.lider_mi else 4.0))
            hormonlar['serotonin'] = min(100.0, hormonlar.get('serotonin', 0.0) + (6.0 if ajan.lider_mi else 3.0))
            hormonlar['kortizol'] = max(0.0, hormonlar.get('kortizol', 0.0) - (5.0 if ajan.lider_mi else 2.0))

        try:
            self.suru_yon.evrimsel_hafiza.arsive_yaz(self.suru_yon, self.suru_yon.toplam_tick)
        except Exception:
            pass

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

        if (not self.evrimsel_sicrama_tetiklendi) and self.baslangic_nufusu > 0:
            oran = self.dogru_cikis / float(self.baslangic_nufusu)
            if oran >= 0.30:
                self._evrimsel_sicrama_uygula()
                self.evrimsel_sicrama_tetiklendi = True

        kalan = self.baslangic_nufusu - self.olenler - self.dogru_cikis - self.sahte_cikis
        if kalan == 0:
            if self.dogru_cikis / self.baslangic_nufusu <= 0.1:
                self.kazanma_kosulu = True
            else:
                self.kaybetme_kosulu = True

    def render(self, surface, font):
        yazi = f"Olen: {self.olenler} | Dogru: {self.dogru_cikis} | Sahte: {self.sahte_cikis}"
        surface.blit(font.render(yazi, True, KIRMIZI), (10, 10))

        sag_yazi = f"OLUM: {self.olenler}"
        sag_surf = font.render(sag_yazi, True, (255, 210, 210))
        panel_w, panel_h = 170, 30
        panel_x = EKRAN_GENISLIK - panel_w - 12
        panel_y = 50
        pygame.draw.rect(surface, (32, 8, 8), pygame.Rect(panel_x, panel_y, panel_w, panel_h), border_radius=5)
        pygame.draw.rect(surface, (180, 40, 40), pygame.Rect(panel_x, panel_y, panel_w, panel_h), 2, border_radius=5)
        surface.blit(sag_surf, (panel_x + 12, panel_y + 6))

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


class AracPaneli:
    """Harita altina yerlesen 20 slotluk (2x10) grafik arac secim paneli."""

    def __init__(self, arac_adlari, mevcut_arac_sayisi=10):
        self.arac_adlari = list(arac_adlari)
        self.mevcut_arac_sayisi = int(max(0, mevcut_arac_sayisi))
        self.secili_index = 0

        self.panel_rect = pygame.Rect(0, HARITA_ALAN_YUKSEKLIK, EKRAN_GENISLIK, ARAC_PANEL_YUKSEKLIK)
        self.kenar_bosluk = 8
        self.hucre_bosluk = 6
        self.sutun = 10
        self.satir = 2
        self.hucre_w = (self.panel_rect.width - self.kenar_bosluk * 2 - self.hucre_bosluk * (self.sutun - 1)) // self.sutun
        self.hucre_h = (self.panel_rect.height - self.kenar_bosluk * 2 - self.hucre_bosluk * (self.satir - 1)) // self.satir

    def secili_arac_adi(self):
        if 0 <= self.secili_index < len(self.arac_adlari):
            return self.arac_adlari[self.secili_index]
        return "Bilinmeyen"

    def secili_arac_kullanilabilir_mi(self):
        return self.secili_index < self.mevcut_arac_sayisi

    def klavye_secimi(self, event):
        tus_haritasi = {
            pygame.K_1: 0,
            pygame.K_2: 1,
            pygame.K_3: 2,
            pygame.K_4: 3,
            pygame.K_5: 4,
            pygame.K_6: 5,
            pygame.K_7: 6,
            pygame.K_8: 7,
            pygame.K_9: 8,
            pygame.K_0: 9,
        }
        if event.key not in tus_haritasi:
            return False

        hedef = tus_haritasi[event.key]
        mods = pygame.key.get_mods()
        if mods & pygame.KMOD_SHIFT:
            hedef += 10

        if 0 <= hedef < len(self.arac_adlari):
            self.secili_index = hedef
            return True
        return False

    def _hucre_recti(self, index):
        satir = index // self.sutun
        sutun = index % self.sutun
        x = self.panel_rect.x + self.kenar_bosluk + sutun * (self.hucre_w + self.hucre_bosluk)
        y = self.panel_rect.y + self.kenar_bosluk + satir * (self.hucre_h + self.hucre_bosluk)
        return pygame.Rect(x, y, self.hucre_w, self.hucre_h)

    def mouse_secimi(self, event):
        if event.type != pygame.MOUSEBUTTONDOWN or event.button != 1:
            return False
        if not self.panel_rect.collidepoint(event.pos):
            return False

        for i in range(min(20, len(self.arac_adlari))):
            rect = self._hucre_recti(i)
            if rect.collidepoint(event.pos):
                self.secili_index = i
                return True
        return False

    def ciz(self, surface, font, arac_kullanim, arac_limitleri):
        pygame.draw.rect(surface, (16, 20, 24), self.panel_rect)
        pygame.draw.line(surface, GRI, (0, self.panel_rect.y), (EKRAN_GENISLIK, self.panel_rect.y), 2)

        for i in range(min(20, len(self.arac_adlari))):
            rect = self._hucre_recti(i)
            arac_adi = self.arac_adlari[i]
            kullanilabilir = i < self.mevcut_arac_sayisi

            dolgu = (42, 50, 58) if kullanilabilir else (28, 32, 36)
            kenar = (95, 112, 128) if kullanilabilir else (62, 70, 78)
            if i == self.secili_index:
                kenar = (255, 214, 90)
                dolgu = (66, 76, 88) if kullanilabilir else (50, 54, 60)

            pygame.draw.rect(surface, dolgu, rect, border_radius=4)
            pygame.draw.rect(surface, kenar, rect, 2, border_radius=4)

            if i < 10:
                kisayol = str((i + 1) % 10)
            else:
                kisayol = f"S+{(i - 9) % 10}"

            kisayol_txt = font.render(kisayol, True, (180, 198, 216))
            surface.blit(kisayol_txt, (rect.x + 4, rect.y + 2))

            ad_kisa = arac_adi if len(arac_adi) <= 10 else arac_adi[:10]
            ad_txt = font.render(ad_kisa, True, (235, 238, 242) if kullanilabilir else (142, 150, 160))
            surface.blit(ad_txt, (rect.x + 4, rect.y + rect.height // 2 - 9))

            kullanilan = arac_kullanim.get(arac_adi, 0)
            limit = arac_limitleri.get(arac_adi, 0)
            sayi_renk = (190, 230, 190) if kullanilabilir else (120, 126, 132)
            sayi_txt = font.render(f"{kullanilan}/{limit}", True, sayi_renk)
            sx = rect.right - sayi_txt.get_width() - 4
            sy = rect.bottom - sayi_txt.get_height() - 2
            surface.blit(sayi_txt, (sx, sy))


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
