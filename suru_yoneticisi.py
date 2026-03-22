# suru_yoneticisi.py
import random
import os
import json
from datetime import datetime
from ayarlar import *


class KavramsalMotor:
    """Faz 3: Arazi/aletleri kavramsal etiketlere ceviren yorum katmani."""

    def __init__(self):
        self.doku_etiketleri = {
            'YOL': 'KULLANILABILIR',
            'GIRIS': 'KULLANILABILIR',
            'CIKIS_KAPI': 'IYI',
            'CIKIS_DOGRU': 'IYI',
            'ZEMIN_DUZ': 'KULLANILABILIR',
            'OVA': 'KULLANILABILIR',
            'PLATO': 'KULLANILABILIR',
            'CALILIK': 'KULLANILABILIR',
            'TASLIK': 'KULLANILABILIR',
            'DAG': 'CIRKIN',
            'SIKI_ORMAN': 'CIRKIN',
            'COL': 'CIRKIN',
            'SU_GOL': 'KOTU',
            'DENIZ': 'KOTU',
            'CIKIS_SAHTE': 'KOTU',
            'DUVAR_KAYA': 'KULLANILAMAZ',
            'TAS_DUVAR': 'KULLANILAMAZ',
            'DIK_DAG': 'KULLANILAMAZ',
            'BARIYER': 'KULLANILAMAZ',
        }
        self.alet_etiketleri = {
            'CikisOku': 'KULLANILABILIR',
            'SahteYol': 'KOTU',
            'Ates': 'KOTU',
            'GizliCukur': 'KOTU',
            'KiymaMakinesi': 'KOTU',
            'Mancinik': 'CIRKIN',
            'SendeletmeTasi': 'CIRKIN',
            'Ayna': 'CIRKIN',
            'Yonlendirici': 'CIRKIN',
            'Bariyer': 'KULLANILAMAZ',
        }
        self.nesne_davranislari = {
            'YOL': {'onerilen_tepki': 'TAKIP_ET', 'amac': 'hedefe_ilerle', 'ilgili_beceri': 'engelden_kacma'},
            'GIRIS': {'onerilen_tepki': 'TOPARLAN', 'amac': 'suruyu_duzenle', 'ilgili_beceri': 'direnc'},
            'CIKIS_KAPI': {'onerilen_tepki': 'ULAS', 'amac': 'kurtulusu_tamamla', 'ilgili_beceri': 'engelden_kacma'},
            'MERDIVEN_YUKARI': {'onerilen_tepki': 'KULLAN', 'amac': 'katman_degistir', 'ilgili_beceri': 'tirmanma'},
            'MERDIVEN_ASAGI': {'onerilen_tepki': 'KULLAN', 'amac': 'katman_degistir', 'ilgili_beceri': 'tirmanma'},
            'SU_GOL': {'onerilen_tepki': 'TEMKINLI_GEC', 'amac': 'bogulmadan_gec', 'ilgili_beceri': 'yuzme'},
            'DENIZ': {'onerilen_tepki': 'UZAK_DUR', 'amac': 'olumcul_sudan_kacin', 'ilgili_beceri': 'yuzme'},
            'SIKI_ORMAN': {'onerilen_tepki': 'YAVASLA', 'amac': 'guvenli_ilerle', 'ilgili_beceri': 'direnc'},
            'DAG': {'onerilen_tepki': 'DOLAN_VEYA_TIRMAN', 'amac': 'engele_uyum_sagla', 'ilgili_beceri': 'tirmanma'},
            'DIK_DAG': {'onerilen_tepki': 'UZAK_DUR', 'amac': 'gecilemez_alan', 'ilgili_beceri': 'tirmanma'},
            'Bariyer': {'onerilen_tepki': 'DOLAN', 'amac': 'engeli_as', 'ilgili_beceri': 'engelden_kacma'},
            'CikisOku': {'onerilen_tepki': 'YONU_IZLE', 'amac': 'dogru_istikameti_bul', 'ilgili_beceri': 'tuzak_fark_etme'},
            'SahteYol': {'onerilen_tepki': 'KONTROL_ET', 'amac': 'aldatici_yolu_dogrula', 'ilgili_beceri': 'tuzak_fark_etme'},
            'Ates': {'onerilen_tepki': 'KACIN', 'amac': 'yanmadan_uzaklas', 'ilgili_beceri': 'direnc'},
            'GizliCukur': {'onerilen_tepki': 'ISARETLE_VE_KAC', 'amac': 'gizli_tehlikeyi_hatirla', 'ilgili_beceri': 'tuzak_fark_etme'},
            'KiymaMakinesi': {'onerilen_tepki': 'UZAK_DUR', 'amac': 'olumcul_tuzaktan_kacin', 'ilgili_beceri': 'engelden_kacma'},
            'Mancinik': {'onerilen_tepki': 'RISK_DEGERLENDIR', 'amac': 'hizli_gecis_firsati', 'ilgili_beceri': 'engelden_kacma'},
            'SendeletmeTasi': {'onerilen_tepki': 'DENGEYI_KORU', 'amac': 'sendelemeden_gec', 'ilgili_beceri': 'direnc'},
            'Ayna': {'onerilen_tepki': 'YONUNE_SUPHEYLE_BAK', 'amac': 'yon_tuzagini_coz', 'ilgili_beceri': 'tuzak_fark_etme'},
            'Yonlendirici': {'onerilen_tepki': 'ISARETI_TEST_ET', 'amac': 'yonlendirmeyi_dogrula', 'ilgili_beceri': 'tuzak_fark_etme'},
        }

    def parsel_etiketi(self, parsel):
        return self.parsel_profili(parsel)['etiket']

    def parsel_profili(self, parsel):
        if parsel is None:
            return {
                'nesne': 'BOSLUK',
                'kaynak': 'bilinmiyor',
                'etiket': 'KULLANILAMAZ',
                'onerilen_tepki': 'GERI_DON',
                'amac': 'gecilemez_bolgeden_kacin',
                'ilgili_beceri': 'engelden_kacma',
            }

        alet = getattr(parsel, 'uzerindeki_alet', None)
        if alet is not None:
            alet_sinifi = type(alet).__name__
            etiket = self.alet_etiketleri.get(alet_sinifi, 'KULLANILABILIR')
            davranis = self.nesne_davranislari.get(alet_sinifi, {})
            return {
                'nesne': alet_sinifi,
                'kaynak': 'alet',
                'etiket': etiket,
                'onerilen_tepki': davranis.get('onerilen_tepki', 'INCELE'),
                'amac': davranis.get('amac', 'nesneyi_anlamlandir'),
                'ilgili_beceri': davranis.get('ilgili_beceri', 'tuzak_fark_etme'),
            }

        doku = getattr(parsel, 'doku_id', '')
        davranis = self.nesne_davranislari.get(doku, {})
        return {
            'nesne': doku or 'BILINMEYEN_DOKU',
            'kaynak': 'zemin',
            'etiket': self.doku_etiketleri.get(doku, 'KULLANILABILIR'),
            'onerilen_tepki': davranis.get('onerilen_tepki', 'INCELE'),
            'amac': davranis.get('amac', 'zemini_degerlendir'),
            'ilgili_beceri': davranis.get('ilgili_beceri', 'direnc'),
        }

    def baskin_nesne_profili(self, harita_yon, x, y, z, yaricap=2):
        en_iyi = None
        en_iyi_skor = float('-inf')
        etiket_agirlik = {
            'KOTU': 9.0,
            'IYI': 7.0,
            'KULLANILAMAZ': 6.0,
            'CIRKIN': 5.0,
            'KULLANILABILIR': 3.0,
        }
        for dy in range(-yaricap, yaricap + 1):
            for dx in range(-yaricap, yaricap + 1):
                nx, ny = x + dx, y + dy
                if not (0 <= nx < HARITA_GENISLIK_PARSEL and 0 <= ny < HARITA_YUKSEKLIK_PARSEL):
                    continue
                parsel = harita_yon.map_grid[z][ny][nx]
                profil = self.parsel_profili(parsel)
                uzaklik = abs(dx) + abs(dy)
                skor = etiket_agirlik.get(profil['etiket'], 0.0) - uzaklik * 0.8
                if profil['kaynak'] == 'alet':
                    skor += 2.5
                if skor > en_iyi_skor:
                    en_iyi_skor = skor
                    en_iyi = profil
        return en_iyi or self.parsel_profili(None)

    def cevre_ozeti(self, harita_yon, x, y, z, yaricap=2):
        ozet = {
            'IYI': 0,
            'KULLANILABILIR': 0,
            'CIRKIN': 0,
            'KOTU': 0,
            'KULLANILAMAZ': 0,
        }
        for dy in range(-yaricap, yaricap + 1):
            for dx in range(-yaricap, yaricap + 1):
                nx, ny = x + dx, y + dy
                if not (0 <= nx < HARITA_GENISLIK_PARSEL and 0 <= ny < HARITA_YUKSEKLIK_PARSEL):
                    continue
                parsel = harita_yon.map_grid[z][ny][nx]
                etiket = self.parsel_etiketi(parsel)
                ozet[etiket] = ozet.get(etiket, 0) + 1
        return ozet


class BiyolojikSistem:
    """Faz 4 baslangici: hormon seviyeleri ve karar moduna etkisi."""

    def __init__(self):
        self.hormonlar = {
            'dopamin': 12.0,
            'adrenalin': 8.0,
            'oksitosin': 10.0,
            'endorfin': 8.0,
            'serotonin': 10.0,
            'husran': 0.0,
            'kortizol': 6.0,
        }

    def cevre_uyarimina_tepki(self, ozet):
        kotu = ozet.get('KOTU', 0)
        cirkin = ozet.get('CIRKIN', 0)
        iyi = ozet.get('IYI', 0)
        kullan = ozet.get('KULLANILABILIR', 0)

        self.hormonlar['adrenalin'] = min(100.0, self.hormonlar['adrenalin'] + kotu * 0.6)
        self.hormonlar['kortizol'] = min(100.0, self.hormonlar['kortizol'] + kotu * 0.45 + cirkin * 0.15)
        self.hormonlar['husran'] = min(100.0, self.hormonlar['husran'] + kotu * 0.3)

        self.hormonlar['dopamin'] = min(100.0, self.hormonlar['dopamin'] + iyi * 0.16)
        self.hormonlar['serotonin'] = min(100.0, self.hormonlar['serotonin'] + iyi * 0.10 + kullan * 0.03)
        self.hormonlar['oksitosin'] = max(0.0, min(100.0, self.hormonlar['oksitosin'] + 0.05 - kotu * 0.05))

        # Doğal sönümleme
        self.hormonlar['adrenalin'] = max(0.0, self.hormonlar['adrenalin'] - 0.25)
        self.hormonlar['kortizol'] = max(0.0, self.hormonlar['kortizol'] - 0.2)
        self.hormonlar['husran'] = max(0.0, self.hormonlar['husran'] - 0.1)

    def duygulara_yansit(self, duygular):
        hedef_korku = max(0.0, min(100.0, self.hormonlar['adrenalin'] * 0.55 + self.hormonlar['kortizol'] * 0.30 - self.hormonlar['endorfin'] * 0.12))
        hedef_suphe = max(0.0, min(100.0, self.hormonlar['husran'] * 0.52 + self.hormonlar['kortizol'] * 0.28 - self.hormonlar['oksitosin'] * 0.10))
        hedef_merak = max(0.0, min(100.0, self.hormonlar['dopamin'] * 0.40 + self.hormonlar['serotonin'] * 0.22 - self.hormonlar['kortizol'] * 0.08 - self.hormonlar['husran'] * 0.05))

        duygular['korku'] = max(0.0, min(100.0, duygular['korku'] + (hedef_korku - duygular['korku']) * 0.18))
        duygular['suphe'] = max(0.0, min(100.0, duygular['suphe'] + (hedef_suphe - duygular['suphe']) * 0.16))
        duygular['merak'] = max(0.0, min(100.0, duygular['merak'] + (hedef_merak - duygular['merak']) * 0.14))

    def mod(self):
        if self.hormonlar['adrenalin'] + self.hormonlar['kortizol'] > 120:
            return 'TEHDIT'
        if self.hormonlar['dopamin'] + self.hormonlar['serotonin'] > 130:
            return 'KESIF'
        return 'DENGELI'

    def karar_matrisi(self, duygular):
        """Faz 4: Hormon + duygu birleşiminden lider karar puanları üretir."""
        korku = duygular.get('korku', 0.0)
        suphe = duygular.get('suphe', 0.0)
        merak = duygular.get('merak', 0.0)

        retreat = korku * 0.7 + self.hormonlar['adrenalin'] * 0.9 + self.hormonlar['kortizol'] * 0.6
        pause = suphe * 0.8 + self.hormonlar['husran'] * 0.7 + self.hormonlar['kortizol'] * 0.4
        explore = merak * 0.6 + self.hormonlar['dopamin'] * 0.9 + self.hormonlar['serotonin'] * 0.4
        route = 50 + self.hormonlar['oksitosin'] * 0.2 + self.hormonlar['endorfin'] * 0.3 - self.hormonlar['husran'] * 0.4

        return {
            'RETREAT': retreat,
            'PAUSE': pause,
            'EXPLORE': explore,
            'ROUTE': route,
        }


class EvrimselHafiza:
    """Faz 7 başlangıcı: dosya tabanlı genom/ajan arşivi."""

    def __init__(self, taban_klasor='evrimsel_hafiza'):
        self.taban_klasor = taban_klasor
        self.baslangic_klasor = os.path.join(self.taban_klasor, 'baslangic_genom')
        self.arsiv_klasor = os.path.join(self.taban_klasor, 'egitimli_arsiv')
        self.migrasyon_durumu_yolu = os.path.join(self.taban_klasor, 'semantik_migrasyon_v2.flag')
        os.makedirs(self.baslangic_klasor, exist_ok=True)
        os.makedirs(self.arsiv_klasor, exist_ok=True)
        self.baslangic_genom_yolu = os.path.join(self.baslangic_klasor, 'genom_v1.json')
        self._baslangic_genomunu_hazirla()
        self.migrate_arsiv_semantik_schema(force=False)

    def _legacy_semantikten_nesneye(self, kayit):
        etiket = str(kayit.get('etiket', 'KULLANILABILIR'))
        tepki = {
            'IYI': 'ULAS',
            'KOTU': 'KACIN',
            'CIRKIN': 'KONTROL_ET',
            'KULLANILAMAZ': 'GERI_DON',
            'KULLANILABILIR': 'INCELE',
        }.get(etiket, 'INCELE')
        amac = {
            'IYI': 'faydali_nesneyi_kullan',
            'KOTU': 'tehlikeden_kacin',
            'CIRKIN': 'riski_dogrula',
            'KULLANILAMAZ': 'alternatif_yol_bul',
            'KULLANILABILIR': 'duruma_gore_degerlendir',
        }.get(etiket, 'duruma_gore_degerlendir')

        return {
            'nesne': f'LEGACY_{etiket}',
            'kaynak': 'legacy_koordinat',
            'etiket': etiket,
            'onerilen_tepki': tepki,
            'amac': amac,
            'ilgili_beceri': 'tuzak_fark_etme',
        }

    def migrate_arsiv_semantik_schema(self, force=False):
        if (not force) and os.path.exists(self.migrasyon_durumu_yolu):
            return 0

        degisen_sayi = 0
        dosyalar = [f for f in os.listdir(self.arsiv_klasor) if f.endswith('.json')]
        for dosya in dosyalar:
            tam_yol = os.path.join(self.arsiv_klasor, dosya)
            try:
                with open(tam_yol, 'r', encoding='utf-8') as f:
                    veri = json.load(f)
            except Exception:
                continue

            hafiza = veri.get('semantik_hafiza', [])
            if not isinstance(hafiza, list) or not hafiza:
                continue

            eski_format = any(('x' in k or 'y' in k or 'z' in k) and ('nesne' not in k) for k in hafiza if isinstance(k, dict))
            if not eski_format:
                continue

            yeni_hafiza = []
            for kayit in hafiza:
                if not isinstance(kayit, dict):
                    continue
                if 'nesne' in kayit and 'onerilen_tepki' in kayit:
                    yeni_hafiza.append(kayit)
                else:
                    yeni_hafiza.append(self._legacy_semantikten_nesneye(kayit))

            veri['semantik_hafiza'] = yeni_hafiza
            veri['semantik_schema'] = 'v2_nesne_tabanli'
            try:
                with open(tam_yol, 'w', encoding='utf-8') as f:
                    json.dump(veri, f, ensure_ascii=False, indent=2)
                degisen_sayi += 1
            except Exception:
                continue

        if degisen_sayi > 0 or (not force):
            with open(self.migrasyon_durumu_yolu, 'w', encoding='utf-8') as f:
                f.write(datetime.utcnow().isoformat() + 'Z\n')
                f.write(f'migrated={degisen_sayi}\n')
        return degisen_sayi

    def _baslangic_genomunu_hazirla(self):
        if os.path.exists(self.baslangic_genom_yolu):
            return
        genom = {
            'surum': 1,
            'aciklama': 'Tabula rasa baslangic genomu',
            'duygular': {'korku': 0.0, 'merak': 0.0, 'suphe': 0.0},
            'beceriler': {'yuzme': 0.0, 'tirmanma': 0.0, 'tuzak_fark_etme': 0.0, 'engelden_kacma': 0.0, 'direnc': 0.0},
            'hormonlar': {
                'dopamin': 12.0,
                'adrenalin': 8.0,
                'oksitosin': 10.0,
                'endorfin': 8.0,
                'serotonin': 10.0,
                'husran': 0.0,
                'kortizol': 6.0,
            }
        }
        with open(self.baslangic_genom_yolu, 'w', encoding='utf-8') as f:
            json.dump(genom, f, ensure_ascii=False, indent=2)

    def baslangic_genomu_yukle(self):
        with open(self.baslangic_genom_yolu, 'r', encoding='utf-8') as f:
            return json.load(f)

    def ilk_oyun_mu(self):
        """Faz 7 madde 2: İlk oyun flag dosyası yoksa True (tabula rasa), varsa False."""
        return not os.path.exists(os.path.join(self.taban_klasor, 'ilk_oyun.flag'))

    def ilk_oyun_bitti_isaretle(self):
        """Faz 7 madde 2: İlk oyun tamamlandı; sonraki oyun seçilimli başlar."""
        flag_yolu = os.path.join(self.taban_klasor, 'ilk_oyun.flag')
        if not os.path.exists(flag_yolu):
            with open(flag_yolu, 'w', encoding='utf-8') as f:
                f.write(datetime.utcnow().isoformat() + 'Z\n')

    def reset_ve_arsivle(self, suru_yon, tick):
        """Faz 7 madde 3: Reset öncesi eğitimli verileri benzersiz zaman damgalı klasöre taşır, flag sıfırlar."""
        self.arsive_yaz(suru_yon, tick)
        zaman_damgasi = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
        arsiv_hedef = os.path.join(self.taban_klasor, f'arsiv_{zaman_damgasi}')
        dosyalar = [f for f in os.listdir(self.arsiv_klasor) if f.endswith('.json')]
        if dosyalar:
            os.makedirs(arsiv_hedef, exist_ok=True)
            for dosya in dosyalar:
                os.rename(
                    os.path.join(self.arsiv_klasor, dosya),
                    os.path.join(arsiv_hedef, dosya)
                )
        flag_yolu = os.path.join(self.taban_klasor, 'ilk_oyun.flag')
        if os.path.exists(flag_yolu):
            os.remove(flag_yolu)

    def en_iyi_arsivi_yukle(self):
        """Faz 7 madde 2: Eğitimli arşivden en yüksek puanlı ajan verisini döndürür; yoksa None."""
        dosyalar = [f for f in os.listdir(self.arsiv_klasor) if f.endswith('.json')]
        if not dosyalar:
            return None
        en_iyi = None
        en_yuksek_puan = float('-inf')
        for dosya in dosyalar:
            try:
                with open(os.path.join(self.arsiv_klasor, dosya), 'r', encoding='utf-8') as f:
                    veri = json.load(f)
                puan = (
                    veri.get('can', 0) * 0.5
                    + sum(veri.get('beceriler', {}).values()) * 2.0
                    + len(veri.get('semantik_hafiza', [])) * 0.4
                )
                if puan > en_yuksek_puan:
                    en_yuksek_puan = puan
                    en_iyi = veri
            except Exception:
                pass
        return en_iyi

    def _ajan_skoru(self, ajan, harita):
        hedef_mesafe = abs(ajan.x - harita.cikis_x) + abs(ajan.y - harita.cikis_y) + abs(ajan.z - harita.cikis_katman) * 5
        beceri_toplam = sum(ajan.beceriler.values())
        semantik_bonus = len(getattr(ajan, 'aktarilabilir_semantik_hafiza', [])) * 0.4
        can_bonus = ajan.can * 0.5
        return can_bonus + beceri_toplam * 2.0 + semantik_bonus - hedef_mesafe

    def arsive_yaz(self, suru_yon, tick):
        yasayanlar = [a for a in suru_yon.ajanlar if a.hayatta]
        if not yasayanlar:
            return

        en_iyi = max(yasayanlar, key=lambda a: self._ajan_skoru(a, suru_yon.harita))
        veri = {
            'zaman': datetime.utcnow().isoformat() + 'Z',
            'tick': int(tick),
            'ajan_id': int(en_iyi.id),
            'lider': bool(en_iyi.lider_mi),
            'gazi': bool(getattr(en_iyi, 'gazi_mi', False)),
            'gazi_puani': float(getattr(en_iyi, 'gazi_puani', 0.0)),
            'can': float(en_iyi.can),
            'konum': {'x': int(en_iyi.x), 'y': int(en_iyi.y), 'z': int(en_iyi.z)},
            'duygular': dict(en_iyi.duygular),
            'hormonlar': dict(en_iyi.biyolojik_sistem.hormonlar),
            'beceriler': dict(en_iyi.beceriler),
            'kavramsal_durum': str(getattr(en_iyi, 'kavramsal_durum', 'KULLANILABILIR')),
            'semantik_hafiza': list(getattr(en_iyi, 'aktarilabilir_semantik_hafiza', [])),
        }

        dosya_adi = f"ajan_{en_iyi.id}_tick_{int(tick)}.json"
        tam_yol = os.path.join(self.arsiv_klasor, dosya_adi)
        with open(tam_yol, 'w', encoding='utf-8') as f:
            json.dump(veri, f, ensure_ascii=False, indent=2)
        # Faz 7 madde 2: İlk arşiv yazımında ilk oyun tamamlandı işareti koy.
        self.ilk_oyun_bitti_isaretle()

class SuruAjani:
    def __init__(self, x, y, ajan_id):
        # 1. KİMLİK VE POZİSYON
        self.id = ajan_id
        self.x = x
        self.y = y
        self.z = 0  # Katman
        self.yon = 'sag'
        self.hayatta = True
        
        # 2. ZİNCİR BAĞLANTILARI (Linked List Mantığı)
        self.onumdeki_ajan = None  # Liderse bu None'dır
        self.arkamdaki_ajan = None
        self.lider_mi = False
        
        # 3. TEMEL STATLAR
        self.can = 100.0
        self.temel_hiz = AJAN_HIZI
        self.hiz = self.temel_hiz  # Parsek geçiş hızı
        # 4. DUYGU MATRİSİ (0 - 100)
        self.duygular = {
            "korku": 0.0,
            "merak": 0.0,
            "suphe": 0.0
        }
        
        # 5. UYKUDAKİ BECERİLER (Senin harika tasarımın)
        # 0: Hiç bilmiyor, 10: Usta (Efor harcamaz)
        self.beceriler = {
            "yuzme": 0.0,
            "tirmanma": 0.0,
            "tuzak_fark_etme": 0.0,
            "engelden_kacma": 0.0,
            "direnc": 0.0
        }
        
        # 6. YOL BULMA
        self.yol = []  # [(x, y, z), ...] hedefe giden yol
        self.yol_index = 0
        self.cikis_bilgisi = 0.0
        self.kavramsal_durum = 'KULLANILABILIR'
        self.kopma_islendi = False
        self.biyolojik_sistem = BiyolojikSistem()
        self.mod = 'DENGELI'
        self.semantik_iz = []
        self.aktarilabilir_semantik_hafiza = []
        self.gazi_puani = 0.0
        self.gazi_mi = False
        self.gazi_omur = 0
        self.hareket_birikimi = random.uniform(0.45, 1.1)
        self.nesne_tercihleri = {}
        self.alt_grup_egilimi = 0.0

    def baslangic_mizaci_ata(self, lider_mi=False):
        merak_taban = 14.0 if lider_mi else 6.0
        merak_tavan = 34.0 if lider_mi else 24.0
        self.duygular['merak'] = round(random.uniform(merak_taban, merak_tavan), 2)
        self.duygular['suphe'] = round(random.uniform(0.0, 16.0), 2)
        self.duygular['korku'] = round(random.uniform(0.0, 12.0), 2)

        hormonlar = self.biyolojik_sistem.hormonlar
        hormonlar['dopamin'] = round(max(0.0, min(100.0, random.uniform(10.0, 24.0) + self.duygular['merak'] * 0.35)), 2)
        hormonlar['serotonin'] = round(max(0.0, min(100.0, random.uniform(8.0, 18.0) + self.duygular['merak'] * 0.18)), 2)
        hormonlar['adrenalin'] = round(max(0.0, min(100.0, random.uniform(4.0, 12.0) + self.duygular['korku'] * 0.25)), 2)
        hormonlar['kortizol'] = round(max(0.0, min(100.0, random.uniform(3.0, 10.0) + self.duygular['suphe'] * 0.22)), 2)
        hormonlar['oksitosin'] = round(random.uniform(8.0, 18.0), 2)
        hormonlar['endorfin'] = round(random.uniform(6.0, 14.0), 2)
        hormonlar['husran'] = round(random.uniform(0.0, 6.0), 2)

        self.temel_hiz = round(AJAN_HIZI * random.uniform(0.92, 1.12), 3)
        self.hiz = self.temel_hiz

        beceri_sayisi = 1 if random.random() < 0.45 else 0
        if lider_mi and random.random() < 0.50:
            beceri_sayisi += 1
        havuz = list(self.beceriler.keys())
        random.shuffle(havuz)
        for beceri in havuz[:beceri_sayisi]:
            ust_sinir = 2.4 if lider_mi else 1.8
            self.beceriler[beceri] = round(random.uniform(0.6, ust_sinir), 2)

        tercih_havuzu = [
            'YOL', 'CikisOku', 'SahteYol', 'Yonlendirici', 'Ayna',
            'Mancinik', 'MERDIVEN_YUKARI', 'MERDIVEN_ASAGI',
            'Ates', 'GizliCukur', 'KiymaMakinesi', 'Bariyer'
        ]
        self.nesne_tercihleri = {ad: 0.0 for ad in tercih_havuzu}
        random.shuffle(tercih_havuzu)
        pozitif_adet = 4 if lider_mi else 3
        negatif_adet = 2
        for ad in tercih_havuzu[:pozitif_adet]:
            self.nesne_tercihleri[ad] = round(random.uniform(0.6, 1.8), 2)
        for ad in tercih_havuzu[pozitif_adet:pozitif_adet + negatif_adet]:
            self.nesne_tercihleri[ad] = round(random.uniform(-1.8, -0.6), 2)

        if lider_mi:
            self.alt_grup_egilimi = 0.0
        else:
            if random.random() < 0.22:
                self.alt_grup_egilimi = round(random.uniform(0.72, 1.0), 2)
            else:
                self.alt_grup_egilimi = round(random.uniform(0.08, 0.62), 2)

    def ozguven_puani(self):
        hormonlar = self.biyolojik_sistem.hormonlar
        beceri_ortalama = sum(self.beceriler.values()) / max(1, len(self.beceriler))
        puan = (
            self.duygular['merak'] * 0.45
            + hormonlar.get('dopamin', 0.0) * 0.28
            + hormonlar.get('serotonin', 0.0) * 0.20
            + hormonlar.get('oksitosin', 0.0) * 0.08
            + beceri_ortalama * 4.5
            - self.duygular['korku'] * 0.22
            - self.duygular['suphe'] * 0.18
            - hormonlar.get('husran', 0.0) * 0.12
        )
        return max(0.0, min(100.0, puan))

    def hareket_cevrimine_hazirla(self):
        self.hiz = self.temel_hiz

    def hareket_hakki_var_mi(self, harita_yon):
        katsayi = self._zemin_hareket_katsayisi(harita_yon)
        gazi_bonus = 0.12 if self.gazi_mi else 0.0
        artis = max(0.35, (self.hiz * 1.35 + gazi_bonus) / max(0.45, katsayi))
        self.hareket_birikimi = min(2.5, self.hareket_birikimi + artis)
        if self.hareket_birikimi < 1.0:
            return False
        self.hareket_birikimi -= 1.0
        return True

    def _zemin_hareket_katsayisi(self, harita_yon):
        if not (0 <= self.x < HARITA_GENISLIK_PARSEL and 0 <= self.y < HARITA_YUKSEKLIK_PARSEL and 0 <= self.z < harita_yon.max_katman):
            return 1.0
        parsel = harita_yon.map_grid[self.z][self.y][self.x]
        if not parsel:
            return 1.0

        katsayi = getattr(parsel, 'yavaslatma_katsayisi', 1.0) or 1.0
        doku = getattr(parsel, 'doku_id', '')
        if doku in ['SU_GOL', 'DENIZ']:
            katsayi *= max(0.55, 1.0 - self.beceriler.get('yuzme', 0.0) * 0.06)
        elif doku in ['DAG', 'PLATO', 'DIK_DAG']:
            katsayi *= max(0.60, 1.0 - self.beceriler.get('tirmanma', 0.0) * 0.05)
        elif doku in ['SIKI_ORMAN', 'CALILIK', 'TASLIK', 'COL']:
            katsayi *= max(0.65, 1.0 - self.beceriler.get('direnc', 0.0) * 0.04)
        return katsayi

    def semantik_iz_kaydet(self, tick, profil):
        kayit = {
            'tick': int(tick),
            'nesne': str(profil.get('nesne', 'BILINMEYEN')),
            'kaynak': str(profil.get('kaynak', 'bilinmiyor')),
            'etiket': str(profil.get('etiket', 'KULLANILABILIR')),
            'onerilen_tepki': str(profil.get('onerilen_tepki', 'INCELE')),
            'amac': str(profil.get('amac', 'nesneyi_anlamlandir')),
            'ilgili_beceri': str(profil.get('ilgili_beceri', 'direnc')),
        }
        self.semantik_iz.append(kayit)
        if len(self.semantik_iz) > 40:
            self.semantik_iz.pop(0)

        # Faz 3 madde 4: evrimsel hafizaya aktarilabilir sade JSON-benzeri yapı.
        self.aktarilabilir_semantik_hafiza = [
            {
                'nesne': k['nesne'],
                'kaynak': k['kaynak'],
                'etiket': k['etiket'],
                'onerilen_tepki': k['onerilen_tepki'],
                'amac': k['amac'],
                'ilgili_beceri': k['ilgili_beceri'],
            }
            for k in self.semantik_iz[-20:]
        ]

    def katman_gecisi_izinli_mi(self, harita_yon, mevcut_x, mevcut_y, mevcut_z, hedef_z):
        """Katman değişimi sadece özel geçiş hücrelerinden yapılır."""
        if hedef_z == mevcut_z:
            return True
        if abs(hedef_z - mevcut_z) != 1:
            return False

        mevcut_parsel = harita_yon.map_grid[mevcut_z][mevcut_y][mevcut_x]
        hedef_parsel = harita_yon.map_grid[hedef_z][mevcut_y][mevcut_x]
        if not mevcut_parsel or not hedef_parsel:
            return False

        if hedef_z > mevcut_z:
            return mevcut_parsel.doku_id == 'MERDIVEN_YUKARI' and hedef_parsel.doku_id == 'MERDIVEN_ASAGI'
        return mevcut_parsel.doku_id == 'MERDIVEN_ASAGI' and hedef_parsel.doku_id == 'MERDIVEN_YUKARI'
    
    def yol_bul(self, harita_yon):
        """Omurga rotadan yararlanarak giristen cikisa yol olusturur. Omurga yoksa A* fallback."""
        import heapq
        try:
            # --- Birincil: Omurga rota (harita olusumunda garantilenmis yol) ---
            omurga = getattr(harita_yon, 'omurga_rota', [])
            if omurga:
                # Mevcut pozisyona en yakin omurga noktasini bul
                best_idx = None
                best_dist = float('inf')
                for i, (wx, wy, wz) in enumerate(omurga):
                    dist = abs(wx - self.x) + abs(wy - self.y) + abs(wz - self.z) * 20
                    if dist < best_dist:
                        best_dist = dist
                        best_idx = i
                if best_idx is not None:
                    self.yol = list(omurga[best_idx:])
                    self.yol_index = 0
                    return

            # --- Yedek: A* (omurga rota bos ise) ---
            hedef_x = harita_yon.cikis_x
            hedef_y = harita_yon.cikis_y
            hedef_z = harita_yon.cikis_katman
            start = (self.x, self.y, self.z)
            goal = (hedef_x, hedef_y, hedef_z)

            if start == goal:
                self.yol = []
                self.yol_index = 0
                return

            def h(x, y, z):
                return abs(x - hedef_x) + abs(y - hedef_y) + abs(z - hedef_z) * 8

            onceki = {start: None}
            g_tablo = {start: 0.0}
            pq = [(h(*start), 0.0, start)]
            bulundu = False

            while pq and len(onceki) < 2000:
                _, g, dugum = heapq.heappop(pq)
                cx, cy, cz = dugum
                if dugum == goal:
                    bulundu = True
                    break
                if g > g_tablo.get(dugum, float('inf')):
                    continue
                for dx, dy, dz in [(-1,0,0),(1,0,0),(0,-1,0),(0,1,0),(0,0,-1),(0,0,1)]:
                    nx, ny, nz = cx + dx, cy + dy, cz + dz
                    if not (0 <= nx < HARITA_GENISLIK_PARSEL and
                            0 <= ny < HARITA_YUKSEKLIK_PARSEL and
                            0 <= nz < harita_yon.max_katman):
                        continue
                    if nz != cz and not self.katman_gecisi_izinli_mi(harita_yon, cx, cy, cz, nz):
                        continue
                    parsel = harita_yon.map_grid[nz][ny][nx]
                    if not parsel or not parsel.yurunebilir:
                        continue
                    maliyet = 0.5 if getattr(parsel, 'doku_id', '') == 'YOL' else 1.0
                    yeni_g = g + maliyet
                    komsu = (nx, ny, nz)
                    if yeni_g < g_tablo.get(komsu, float('inf')):
                        g_tablo[komsu] = yeni_g
                        onceki[komsu] = dugum
                        f = yeni_g + h(nx, ny, nz)
                        heapq.heappush(pq, (f, yeni_g, komsu))

            if bulundu:
                yol = []
                k = goal
                while k != start:
                    yol.append(k)
                    k = onceki[k]
                yol.reverse()
                self.yol = yol
                self.yol_index = 0
                return

            self._greedy_yedek(harita_yon)

        except Exception as e:
            print(f"[HATA] Yol arama basarisiz: {e}")
            self.yol = []
            self.yol_index = 0

    def _greedy_yedek(self, harita_yon):
        """A* basarisiz olursa calisan yedek greedy yol bulma."""
        hedef_x = harita_yon.cikis_x
        hedef_y = harita_yon.cikis_y
        hedef_z = harita_yon.cikis_katman
        self.yol = []
        cx, cy, cz = self.x, self.y, self.z
        visited = set()
        for _ in range(300):
            if (cx, cy, cz) in visited:
                break
            visited.add((cx, cy, cz))
            if abs(cx - hedef_x) + abs(cy - hedef_y) + abs(cz - hedef_z) < 2:
                break
            best = None
            best_cost = float('inf')
            for dx, dy, dz in [(-1,0,0),(1,0,0),(0,-1,0),(0,1,0),(0,0,-1),(0,0,1)]:
                nx, ny, nz = cx + dx, cy + dy, cz + dz
                if not (0 <= nx < HARITA_GENISLIK_PARSEL and 0 <= ny < HARITA_YUKSEKLIK_PARSEL and 0 <= nz < harita_yon.max_katman):
                    continue
                if not self.katman_gecisi_izinli_mi(harita_yon, cx, cy, cz, nz):
                    continue
                parsel = harita_yon.map_grid[nz][ny][nx]
                if parsel and parsel.yurunebilir and (nx, ny, nz) not in visited:
                    cost = abs(nx - hedef_x) + abs(ny - hedef_y) + abs(nz - hedef_z)
                    cost += getattr(parsel, 'yavaslatma_katsayisi', 1.0) or 1.0
                    if getattr(parsel, 'doku_id', '') == 'YOL':
                        cost *= 0.6
                    if cost < best_cost:
                        best_cost = cost
                        best = (nx, ny, nz)
            if best:
                self.yol.append(best)
                cx, cy, cz = best
            else:
                break
        self.yol_index = 0
    
    # --- BECERİ VE ÖĞRENME METOTLARI ---

    def beceri_ogren(self, beceri_adi, miktar):
        """Arkaya doğru yayılan bilgi transferi bu metodu tetikler."""
        if beceri_adi in self.beceriler:
            self.beceriler[beceri_adi] = min(10.0, self.beceriler[beceri_adi] + miktar)

    def arkaya_bilgi_ilet(self, beceri_adi, ogretme_miktari=1.0):
        """Liderde öğrenilen bilginin zincir boyunca zayıflayarak aktarımı."""
        aktarim = ogretme_miktari
        hedef = self.arkamdaki_ajan
        while hedef is not None and aktarim > 0.05:
            hedef.beceri_ogren(beceri_adi, aktarim)
            aktarim *= 0.7
            hedef = hedef.arkamdaki_ajan
    
    # --- AKSİYON METOTLARI (Geniş metot, parametre kısıtlaması) ---

    def suya_gir(self, zemin_zorlugu):
        """Zemin nesnesi 'Su/Göl' olduğunda bu devasa metot çağrılır."""
        
        # Beceri 0 ise yorulma maksimumdur, beceri 10 ise yorulma sıfıra yakındır.
        direnc = self.beceriler["yuzme"]
        harcanan_efor = zemin_zorlugu - (direnc * 0.5) 
        
        if harcanan_efor > 0:
            self.can -= harcanan_efor
            self.duygular["korku"] += harcanan_efor * 2 # Canı yandıkça korkar
            
        if self.can <= 0:
            self.ol()
        else:
            # Hayatta kaldı ama canı yandı. Liderse arkadakilere uyarı/bilgi gönder!
            if self.lider_mi and harcanan_efor > 2:
                self.arkaya_bilgi_ilet("yuzme", ogretme_miktari=2.0)
            # Hayatta kalınca merak artar
            self.duygular["merak"] += 10

    def zemin_kontrol(self, harita_yon):
        """Hareket sonrası zeminin zorluğunu kontrol et."""
        if not (0 <= self.x < HARITA_GENISLIK_PARSEL and 0 <= self.y < HARITA_YUKSEKLIK_PARSEL and 0 <= self.z < harita_yon.max_katman):
            return
        parsel = harita_yon.map_grid[self.z][self.y][self.x]
        if not parsel:
            return
        
        zemin_zorlugu = 0
        if parsel.doku_id == 'SIKI_ORMAN':
            zemin_zorlugu = 2.0  # Çok zor
        elif parsel.doku_id in ['SU_GOL', 'DENIZ']:
            if parsel.derinlik > 10:
                zemin_zorlugu = 5.0  # Çok derin, boğulma
            elif parsel.derinlik > 5:
                zemin_zorlugu = 3.0  # Orta derin
            else:
                zemin_zorlugu = 1.0  # Az derin
            self.suya_gir(zemin_zorlugu)
            return
        elif parsel.doku_id in ['DAG', 'DIK_DAG']:
            zemin_zorlugu = 1.5  # Yavaşlatır
        elif parsel.doku_id == 'COL':
            zemin_zorlugu = 1.5  # Çöl susuzluk
        
        if zemin_zorlugu > 0:
            direnc = self.beceriler.get("direnc", 0)
            harcanan_efor = zemin_zorlugu - (direnc * 0.5)
            if harcanan_efor > 0:
                self.can -= harcanan_efor
                self.duygular["korku"] += harcanan_efor * 2
                if self.can <= 0:
                    self.ol()
                elif self.lider_mi and harcanan_efor > 1:
                    self.arkaya_bilgi_ilet("direnc", 1.0)

    # --- DURUM METOTLARI ---

    def ol(self):
        self.hayatta = False
        # Zinciri koparma işlemi: Arkamdaki ajan lidersiz kaldı!
        if self.arkamdaki_ajan:
            self.arkamdaki_ajan.onumdeki_ajan = None
            self.arkamdaki_ajan.lider_mi = True # O artık yeni lider!
            self.arkamdaki_ajan.duygular["suphe"] += 50 # Şok etkisi

class SuruYoneticisi:
    def __init__(self, harita_yoneticisi):
        self.harita = harita_yoneticisi
        self.kavramsal_motor = KavramsalMotor()
        self.evrimsel_hafiza = EvrimselHafiza()
        self.arac_etkilesim_matrisi = {
            ('Ates', 'Bariyer'): {'korku': 6.0, 'suphe': 4.0, 'kortizol': 4.0},
            ('Ates', 'SahteYol'): {'korku': 5.0, 'suphe': 6.0, 'husran': 5.0},
            ('Mancinik', 'SendeletmeTasi'): {'korku': 4.0, 'adrenalin': 4.0},
            ('Ayna', 'Yonlendirici'): {'suphe': 6.0, 'kortizol': 3.0},
            ('CikisOku', 'SahteYol'): {'suphe': 8.0, 'husran': 6.0},
            ('CikisOku', 'Bariyer'): {'merak': -2.0, 'suphe': 5.0},
            ('KiymaMakinesi', 'GizliCukur'): {'korku': 10.0, 'suphe': 9.0, 'adrenalin': 8.0, 'kortizol': 8.0},
        }
        self.ajanlar = []       # Haritadaki tüm yaşayan ajanlar
        self.liderler = []      # Sadece lider olanlar (Max 4 kuralı için)
        self.maks_lider = 4
        self.tick_sayaci = 0    # Yapay zekanın düşünme hızını ayarlamak için
        self.ogrenme_sayaci = 0
        self.baslangic_bekleme = 0
        self.toplam_tick = 0
        self._olum_olaylari = []
        self._son_arsiv_tick = 0

    def kayit_olum_olayi(self, ajan, neden="bilinmiyor"):
        self._olum_olaylari.append({
            "tip": "olum",
            "neden": neden,
            "tick": self.toplam_tick,
            "ajan_id": ajan.id,
            "lider": ajan.lider_mi,
            "x": ajan.x,
            "y": ajan.y,
            "z": ajan.z,
            "can": ajan.can,
            "duygular": dict(ajan.duygular),
        })

    def olum_olaylarini_al(self):
        olaylar = self._olum_olaylari[:]
        self._olum_olaylari.clear()
        return olaylar
    
    def suru_yarat(self, baslangic_x, baslangic_y, boyut):
        """Bölüm başında sürüyü birbirine bağlı bir zincir olarak yaratır."""
        onceki_ajan = None
        
        for i in range(boyut):
            yeni_ajan = SuruAjani(baslangic_x, baslangic_y, i)
            # Faz 2: Tüm ajanlar haritanın gerçek giriş katmanında başlar.
            yeni_ajan.z = self.harita.giris_katman
            
            # İlk doğan ajan Liderdir
            if i == 0:
                yeni_ajan.lider_mi = True
                yeni_ajan.baslangic_mizaci_ata(lider_mi=True)
                self.liderler.append(yeni_ajan)
            else:
                yeni_ajan.baslangic_mizaci_ata(lider_mi=False)
                # Arkadan gelenleri birbirine bağla (Linked List)
                yeni_ajan.onumdeki_ajan = onceki_ajan
                onceki_ajan.arkamdaki_ajan = yeni_ajan
            
            self.ajanlar.append(yeni_ajan)
            onceki_ajan = yeni_ajan
            
        # Faz 2: Tüm liderler için yol bulma başlat
        for lider in self.liderler:
            lider.yol_bul(self.harita)
        
        # Faz 7 madde 2: İlk oyun değilse eğitimli arşivden lider ajanı seed et.
        if not self.evrimsel_hafiza.ilk_oyun_mu():
            en_iyi = self.evrimsel_hafiza.en_iyi_arsivi_yukle()
            if en_iyi and self.ajanlar:
                lider = self.ajanlar[0]
                for beceri, deger in en_iyi.get('beceriler', {}).items():
                    if beceri in lider.beceriler:
                        lider.beceriler[beceri] = min(10.0, max(lider.beceriler[beceri], float(deger) * 0.85))
                for h, v in en_iyi.get('hormonlar', {}).items():
                    if h in lider.biyolojik_sistem.hormonlar:
                        lider.biyolojik_sistem.hormonlar[h] = max(0.0, min(100.0, lider.biyolojik_sistem.hormonlar[h] * 0.35 + float(v) * 0.65))
                for duygu, deger in en_iyi.get('duygular', {}).items():
                    if duygu in lider.duygular:
                        lider.duygular[duygu] = max(0.0, min(100.0, lider.duygular[duygu] * 0.45 + float(deger) * 0.55))

    def zinciri_kopar(self, kopan_ajan):
        """Bir ajan ölürse veya merakına yenilip ayrılırsa çalışır."""
        # Eğer zaten liderse yapacak bir şey yok
        if kopan_ajan.lider_mi:
            return

        # 1. Önündeki ile bağını kopar
        eski_oncu = kopan_ajan.onumdeki_ajan
        if eski_oncu:
            eski_oncu.arkamdaki_ajan = None
            kopan_ajan.onumdeki_ajan = None

        # 2. Max 4 Lider kuralını kontrol et
        if len(self.liderler) < self.maks_lider:
            kopan_ajan.lider_mi = True
            kopan_ajan.kopma_islendi = True
            self.liderler.append(kopan_ajan)
            # Faz 2: Yeni lider anında yol takibi moduna geçer (rol tabanlı davranış)
            kopan_ajan.yol = []
            kopan_ajan.yol_index = 0
            kopan_ajan.yol_bul(self.harita)
        else:
            kopan_ajan.kopma_islendi = True
            kopan_ajan.duygular["korku"] += 80  # Lidersiz kaldılar, panik!

    def _kavramsal_basinci_duygulara_yansit(self, ajan):
        ozet = self.kavramsal_motor.cevre_ozeti(self.harita, ajan.x, ajan.y, ajan.z, yaricap=2)
        baskin_profil = self.kavramsal_motor.baskin_nesne_profili(self.harita, ajan.x, ajan.y, ajan.z, yaricap=2)
        yenilik = self._anlamsal_yenilik_katsayisi(ajan, baskin_profil)
        kotu = ozet.get('KOTU', 0)
        cirkin = ozet.get('CIRKIN', 0)
        iyi = ozet.get('IYI', 0)

        # Faz 4 baslangici: biyolojik sistem kavramsal çevreye tepki verir.
        ajan.biyolojik_sistem.cevre_uyarimina_tepki(ozet)
        ajan.biyolojik_sistem.duygulara_yansit(ajan.duygular)
        ajan.mod = ajan.biyolojik_sistem.mod()

        if kotu > 4:
            ajan.duygular['korku'] = min(100, ajan.duygular['korku'] + 6 * yenilik)
            ajan.duygular['suphe'] = min(100, ajan.duygular['suphe'] + 4 * yenilik)
            ajan.kavramsal_durum = 'KOTU'
        elif cirkin > 6:
            ajan.duygular['suphe'] = min(100, ajan.duygular['suphe'] + 3 * yenilik)
            ajan.kavramsal_durum = 'CIRKIN'
        elif iyi > 6:
            ajan.duygular['merak'] = min(100, ajan.duygular['merak'] + 1.2 * yenilik)
            ajan.kavramsal_durum = 'IYI'
        else:
            ajan.kavramsal_durum = baskin_profil['etiket']

        ajan.semantik_iz_kaydet(self.toplam_tick, baskin_profil)

    def _anlamsal_yenilik_katsayisi(self, ajan, profil):
        son_kayitlar = getattr(ajan, 'semantik_iz', [])[-6:]
        ayni_nesne = sum(1 for kayit in son_kayitlar if kayit.get('nesne') == profil.get('nesne'))
        ayni_tepki = sum(1 for kayit in son_kayitlar if kayit.get('onerilen_tepki') == profil.get('onerilen_tepki'))
        katsayi = 1.0 - ayni_nesne * 0.15 - ayni_tepki * 0.08
        return max(0.18, katsayi)

    def _hormon_ogrenme_carpani(self, ajan):
        h = ajan.biyolojik_sistem.hormonlar
        olumlu = h.get('dopamin', 0.0) * 0.02 + h.get('serotonin', 0.0) * 0.02
        olumsuz = h.get('kortizol', 0.0) * 0.015 + h.get('husran', 0.0) * 0.015
        carpan = 1.0 + olumlu - olumsuz
        if carpan < 0.45:
            return 0.45
        if carpan > 1.75:
            return 1.75
        return carpan

    def _ajan_uzerindeki_arac_etkilesimi(self, ajan):
        """Faz 5: Ajan yakınındaki birden fazla aracın birleşik psikolojik etkisi."""
        bulunanlar = []
        z = ajan.z
        for dy in range(-ETKI_YARICAPI, ETKI_YARICAPI + 1):
            for dx in range(-ETKI_YARICAPI, ETKI_YARICAPI + 1):
                nx, ny = ajan.x + dx, ajan.y + dy
                if not (0 <= nx < HARITA_GENISLIK_PARSEL and 0 <= ny < HARITA_YUKSEKLIK_PARSEL):
                    continue
                parsel = self.harita.map_grid[z][ny][nx]
                if parsel and parsel.uzerindeki_alet is not None:
                    bulunanlar.append(type(parsel.uzerindeki_alet).__name__)

        if len(bulunanlar) < 2:
            return

        # Aynı turda tekrar tekrar eklenmesin diye benzersiz sırala.
        benzersiz = sorted(set(bulunanlar))
        for i in range(len(benzersiz)):
            for j in range(i + 1, len(benzersiz)):
                a, b = benzersiz[i], benzersiz[j]
                etki = self.arac_etkilesim_matrisi.get((a, b)) or self.arac_etkilesim_matrisi.get((b, a))
                if not etki:
                    continue

                if 'korku' in etki:
                    ajan.duygular['korku'] = min(100.0, ajan.duygular['korku'] + etki['korku'])
                if 'suphe' in etki:
                    ajan.duygular['suphe'] = min(100.0, ajan.duygular['suphe'] + etki['suphe'])
                if 'merak' in etki:
                    ajan.duygular['merak'] = max(0.0, min(100.0, ajan.duygular['merak'] + etki['merak']))

                bio = ajan.biyolojik_sistem.hormonlar
                for h in ['adrenalin', 'kortizol', 'husran']:
                    if h in etki:
                        bio[h] = max(0.0, min(100.0, bio.get(h, 0.0) + etki[h]))

    def _gazi_modunu_guncelle(self, ajan):
        """Faz 6: krizden çıkan ajanların gazi puanını biriktirir ve geçici mod üretir."""
        kriz_baskisi = 0.0
        if ajan.can < 55:
            kriz_baskisi += (55 - ajan.can) * 0.12
        kriz_baskisi += ajan.duygular.get('korku', 0.0) * 0.03
        kriz_baskisi += ajan.duygular.get('suphe', 0.0) * 0.02
        kriz_baskisi += ajan.biyolojik_sistem.hormonlar.get('adrenalin', 0.0) * 0.05

        if kriz_baskisi > 3.0 and ajan.hayatta:
            ajan.gazi_puani = min(200.0, ajan.gazi_puani + kriz_baskisi * 0.55)
        else:
            ajan.gazi_puani = max(0.0, ajan.gazi_puani - 0.08)

        if (not ajan.gazi_mi) and ajan.gazi_puani >= 12.0:
            ajan.gazi_mi = True
            ajan.gazi_omur = 160
        elif ajan.gazi_mi:
            ajan.gazi_omur -= 1
            if ajan.gazi_omur <= 0:
                ajan.gazi_mi = False

    def _gazi_liderlik_devri(self, ajan):
        """Faz 6: Gazi ajan uygun koşulda liderliği devralabilir."""
        if ajan.lider_mi or not ajan.gazi_mi:
            return
        if len(self.liderler) >= self.maks_lider:
            return
        if ajan.gazi_puani < 16.0:
            return
        self.zinciri_kopar(ajan)

    def _alt_grup_kesif_tetikle(self, ajan, oncu):
        if ajan.lider_mi or not ajan.hayatta:
            return False
        if len(self.liderler) >= self.maks_lider:
            return False
        if oncu is None or not oncu.hayatta:
            return False

        merak = ajan.duygular.get('merak', 0.0)
        ozguven = ajan.ozguven_puani()
        egilim = getattr(ajan, 'alt_grup_egilimi', 0.0)
        if merak < 32 and ozguven < 32 and egilim < 0.75:
            return False

        profil = self.kavramsal_motor.baskin_nesne_profili(self.harita, ajan.x, ajan.y, ajan.z, yaricap=3)
        tetik = 0.04 + egilim * 0.32 + max(0.0, merak - 35.0) * 0.002 + max(0.0, ozguven - 35.0) * 0.0012
        if profil.get('etiket') in ['IYI', 'CIRKIN']:
            tetik += 0.06
        if profil.get('onerilen_tepki') in ['KULLAN', 'KONTROL_ET', 'YONU_IZLE', 'ISARETI_TEST_ET']:
            tetik += 0.05

        if egilim > 0.90 and random.random() < 0.22:
            self.zinciri_kopar(ajan)
            if ajan.lider_mi:
                ajan.duygular['suphe'] = max(0.0, ajan.duygular.get('suphe', 0.0) - 6.0)
                ajan.duygular['merak'] = min(100.0, ajan.duygular.get('merak', 0.0) + 4.0)
                return True
            return False

        if random.random() >= min(0.70, tetik):
            return False

        self.zinciri_kopar(ajan)
        if ajan.lider_mi:
            ajan.duygular['suphe'] = max(0.0, ajan.duygular.get('suphe', 0.0) - 5.0)
            ajan.duygular['merak'] = min(100.0, ajan.duygular.get('merak', 0.0) + 3.0)
            return True
        return False

    def _kacanlari_topla(self, gazi_ajan):
        """Faz 6: Gazi ajanlar yakınındaki lidersiz/öncüsüz ajanları kendi zincirine toplar."""
        if not gazi_ajan.gazi_mi or not gazi_ajan.hayatta:
            return

        for aday in self.ajanlar:
            if aday is gazi_ajan or not aday.hayatta:
                continue
            if aday.lider_mi:
                continue
            if aday.onumdeki_ajan is not None:
                continue
            if aday.arkamdaki_ajan is gazi_ajan:
                continue

            if abs(aday.x - gazi_ajan.x) <= 2 and abs(aday.y - gazi_ajan.y) <= 2 and aday.z == gazi_ajan.z:
                # Gazi ajanı yeni öncü yap.
                aday.onumdeki_ajan = gazi_ajan
                if gazi_ajan.arkamdaki_ajan is None:
                    gazi_ajan.arkamdaki_ajan = aday
                aday.duygular['korku'] = max(0.0, aday.duygular.get('korku', 0.0) - 8.0)
                aday.duygular['suphe'] = max(0.0, aday.duygular.get('suphe', 0.0) - 6.0)
                gazi_ajan.gazi_puani = min(200.0, gazi_ajan.gazi_puani + 1.2)

    def guncelle(self):
        """Bu fonksiyon main.py içindeki oyun döngüsünde sürekli çağrılacak."""
        # Zorluk menüsü henüz çalışmadıysa modül içi dinamik sabitler tanımlı olmayabilir.
        # Bu durumda _TEMEL değerleriyle güvenli fallback kullan.
        ogrenme_tik_araligi = globals().get("OGRENME_TIK_ARALIGI", OGRENME_TIK_ARALIGI_TEMEL)
        ogrenme_miktari = globals().get("OGRENME_MIKTARI", OGRENME_MIKTARI_TEMEL)
        cikis_bilgisi_artis = globals().get("CIKIS_BILGISI_ARTIS", CIKIS_BILGISI_ARTIS_TEMEL)
        ajan_karar_hz = globals().get("AJAN_KARAR_HZ", AJAN_KARAR_HZ_TEMEL)
        baslangic_bekleme_tik = globals().get("SURU_BASLANGIC_BEKLEME_TIK", SURU_BASLANGIC_BEKLEME_TIK_TEMEL)

        self.toplam_tick += 1
        self.baslangic_bekleme += 1
        if self.baslangic_bekleme < baslangic_bekleme_tik:
            return

        self.tick_sayaci += 1
        self.ogrenme_sayaci += 1

        # Faz 7: Belirli aralıkta en iyi ajanı dosya tabanlı arşive yaz.
        if self.toplam_tick - self._son_arsiv_tick >= 600:
            self.evrimsel_hafiza.arsive_yaz(self, self.toplam_tick)
            self._son_arsiv_tick = self.toplam_tick
        
        # Ölü ajanları önce log kuyruğuna al, sonra listeden temizle.
        for ajan in self.ajanlar:
            if not ajan.hayatta:
                self.kayit_olum_olayi(ajan, neden="hayatta_degil")

        # Ölü ajanları kaldır
        self.ajanlar = [ajan for ajan in self.ajanlar if ajan.hayatta]
        self.liderler = [lider for lider in self.liderler if lider.hayatta]
        
        # Öğrenme: Sürünün bilgisi daha yavaş artsın.
        if self.ogrenme_sayaci >= ogrenme_tik_araligi:
            self.ogrenme_sayaci = 0
            for ajan in self.ajanlar:
                if ajan.hayatta and random.random() < 0.35:
                    beceri_adi = random.choice(list(ajan.beceriler.keys()))
                    carpan = self._hormon_ogrenme_carpani(ajan)
                    ajan.beceri_ogren(beceri_adi, ogrenme_miktari * carpan)
                if ajan.lider_mi:
                    ajan.cikis_bilgisi = min(1.0, ajan.cikis_bilgisi + cikis_bilgisi_artis)
        
        # Yapay zeka her karede (frame) düşünmez. Saniyede örneğin 5 kez karar verir.
        # Bu da hem oyunu satranç gibi oynanabilir kılar hem işlemciyi rahatlatır.
        karar_araligi = max(1, FPS // max(1, ajan_karar_hz))
        if self.tick_sayaci >= karar_araligi:
            self.tick_sayaci = 0
            
            # 1. Aşama: Tüm ajanların mevcut konumunu hafızaya al
            for ajan in self.ajanlar:
                ajan.hareket_cevrimine_hazirla()
                ajan.eski_x = ajan.x
                ajan.eski_y = ajan.y
                ajan.eski_z = ajan.z

            # 2. Aşama: Liderler karar verir ve hareket eder
            for lider in self.liderler:
                self._kavramsal_basinci_duygulara_yansit(lider)
                self._ajan_uzerindeki_arac_etkilesimi(lider)
                self._gazi_modunu_guncelle(lider)
                if lider.hareket_hakki_var_mi(self.harita):
                    self.lider_yapay_zeka(lider, self.harita)
                lider.zemin_kontrol(self.harita)

            # 3. Aşama: Takipçilerde lider izleme birincil davranıştır.
            # Zincir bağlantısı koparsa ajan yeni lider statüsüne yükselir.
            for ajan in self.ajanlar:
                if ajan.lider_mi:
                    continue

                oncu = ajan.onumdeki_ajan
                if oncu and oncu.hayatta:
                    self._kavramsal_basinci_duygulara_yansit(ajan)
                    self._ajan_uzerindeki_arac_etkilesimi(ajan)
                    self._gazi_modunu_guncelle(ajan)
                    self._gazi_liderlik_devri(ajan)
                    if self._alt_grup_kesif_tetikle(ajan, oncu):
                        continue

                    # Faz 2 kalan: duygu + nesne etkisi, takipçide kopma tetikleyebilir.
                    ozet = self.kavramsal_motor.cevre_ozeti(self.harita, ajan.x, ajan.y, ajan.z, yaricap=2)
                    kopma_olasilik = 0.0
                    if ozet.get('KOTU', 0) >= 3:
                        kopma_olasilik += 0.10
                    if ajan.duygular['korku'] > 65:
                        kopma_olasilik += 0.12
                    if ajan.duygular['suphe'] > 70:
                        kopma_olasilik += 0.12

                    if (not ajan.kopma_islendi) and random.random() < kopma_olasilik:
                        self.zinciri_kopar(ajan)
                        continue

                    if not ajan.hareket_hakki_var_mi(self.harita):
                        ajan.zemin_kontrol(self.harita)
                        continue

                    if self._takipci_serbest_adim(ajan, oncu):
                        ajan.zemin_kontrol(self.harita)
                        if ajan.gazi_mi:
                            self._kacanlari_topla(ajan)
                        continue

                    ajan.x = oncu.eski_x
                    ajan.y = oncu.eski_y
                    ajan.z = oncu.eski_z
                    ajan.zemin_kontrol(self.harita)
                    if ajan.gazi_mi:
                        self._kacanlari_topla(ajan)
                    continue

                # Faz 2: Sürü parçası koptuysa takipçi modundan çıkıp yeni lider olur.
                if not ajan.kopma_islendi:
                    self.zinciri_kopar(ajan)

            # 4. Aşama: Liderlerde gazi toplama davranışı
            for lider in self.liderler:
                if lider.gazi_mi:
                    self._kacanlari_topla(lider)

    def lider_yapay_zeka(self, lider, harita_yon):
        """Lider AI - Faz 2 (Rol Tabanlı): Yol takibi birincil, duygu sapmaları ikincil davranış.
        Takipçiler lider izler; lider yolu izler; kopan sürü yeni lider → yol takibine geçer."""

        # --- Kolektif zeka: Diğer liderlerin korku ortalamasını erken uygula ---
        toplam_korku = sum(l.duygular["korku"] for l in self.liderler)
        ortalama_korku = toplam_korku / len(self.liderler) if self.liderler else 0
        if ortalama_korku > 60:
            lider.duygular["korku"] = min(100, lider.duygular["korku"] + 20)

        korku = lider.duygular["korku"]
        suphe = lider.duygular["suphe"]
        merak = lider.duygular["merak"]
        ozguven = lider.ozguven_puani()

        # Faz 4 baslangici: hormon modu, karar önceliğini etkiler.
        if lider.mod == 'TEHDIT':
            korku = min(100, korku + 10)
            suphe = min(100, suphe + 8)
        elif lider.mod == 'KESIF':
            merak = min(100, merak + 10)

        kararlar = lider.biyolojik_sistem.karar_matrisi({
            'korku': korku,
            'suphe': suphe,
            'merak': merak,
        })
        serbest_dolasim = (
            merak > 34
            or ozguven > 46
            or kararlar['EXPLORE'] >= kararlar['ROUTE'] * 0.82
        )

        # --- Şiddetli duygu sapmaları: yol takibini geçersiz kılar ---
        if suphe > 60 or kararlar['PAUSE'] > max(kararlar['RETREAT'], kararlar['EXPLORE'], kararlar['ROUTE']):
            return  # Dur, hareket etme

        if korku > 70 or kararlar['RETREAT'] > max(kararlar['PAUSE'], kararlar['EXPLORE'], kararlar['ROUTE']):
            # Geri çekil, yol takibini kes
            dx, dy = -1, 0
            hedef = self._sinirda_sapmali_hedef(lider, dx, dy)
            if hedef is not None:
                hedef_x, hedef_y = hedef
                lider.yon = 'sol'
                if 0 <= hedef_x < HARITA_GENISLIK_PARSEL and 0 <= hedef_y < HARITA_YUKSEKLIK_PARSEL:
                    geri_parsel = harita_yon.map_grid[lider.z][hedef_y][hedef_x]
                    if geri_parsel and geri_parsel.yurunebilir and not geri_parsel.hasar_verir:
                        lider.x, lider.y = hedef_x, hedef_y
            return

        if serbest_dolasim:
            serbest_adim = self._serbest_adim_sec(lider, harita_yon, merak_agirlikli=True)
            if serbest_adim is not None and (not lider.yol or random.random() < 0.35 + min(0.25, merak / 180.0)):
                self._adimi_uygula(lider, *serbest_adim)
                return

        # --- Yol takibi artık öneri ağırlıklıdır; lider isterse keşfe sapabilir ---
        if not lider.yol or lider.yol_index >= len(lider.yol):
            lider.yol_bul(harita_yon)

        yol_onceligi = kararlar['ROUTE'] + lider.cikis_bilgisi * 35.0 - merak * 0.35 + max(0.0, 55.0 - ozguven) * 0.20
        kesif_onceligi = kararlar['EXPLORE'] + merak * 0.35 + ozguven * 0.20

        if lider.yol and lider.yol_index < len(lider.yol) and yol_onceligi >= kesif_onceligi * 0.92:
            hedef_x, hedef_y, hedef_z = lider.yol[lider.yol_index]
            hedef_parsel = self.harita.map_grid[hedef_z][hedef_y][hedef_x]
            hedef_etiketi = self.kavramsal_motor.parsel_etiketi(hedef_parsel)

            # Faz 2 kalan + Faz 3 başlangıcı: kavramsal riskte yoldan sapma kararı.
            if hedef_etiketi in ['KOTU', 'KULLANILAMAZ']:
                lider.duygular['korku'] = min(100, lider.duygular['korku'] + 10)
                lider.duygular['suphe'] = min(100, lider.duygular['suphe'] + 8)
                lider.yol = []
                lider.yol_index = 0
                return

            if hedef_etiketi == 'CIRKIN' and (lider.duygular['suphe'] > 55 or lider.duygular['korku'] > 55):
                lider.duygular['suphe'] = min(100, lider.duygular['suphe'] + 3)
                lider.yol = []
                lider.yol_index = 0
                return

            if self._hedefe_gecis_izinli(lider, hedef_x, hedef_y, hedef_z):
                dx = hedef_x - lider.x
                dy = hedef_y - lider.y
                if abs(dx) >= abs(dy):
                    lider.yon = 'sag' if dx >= 0 else 'sol'
                else:
                    lider.yon = 'asagi' if dy >= 0 else 'yukari'
                lider.x, lider.y, lider.z = hedef_x, hedef_y, hedef_z
                lider.yol_index += 1
                return
            lider.yol = []
            lider.yol_index = 0

        # --- İkincil davranış: Keşif yürüyüşü (yol bulunamadığında devreye girer) ---
        serbest_adim = self._serbest_adim_sec(lider, harita_yon, merak_agirlikli=(merak > 28 or kararlar['EXPLORE'] > kararlar['ROUTE']))
        if serbest_adim is not None:
            self._adimi_uygula(lider, *serbest_adim)
            return

        if merak > 50 or kararlar['EXPLORE'] > kararlar['ROUTE']:
            yonler = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        else:
            yonler = [(1, 0), (1, 0), (0, 1), (0, -1), (-1, 0)]
        dx, dy = random.choice(yonler)

        hedef = self._sinirda_sapmali_hedef(lider, dx, dy)
        if hedef is None:
            return
        hedef_x, hedef_y = hedef

        if abs(hedef_x - lider.x) >= abs(hedef_y - lider.y):
            lider.yon = 'sag' if hedef_x >= lider.x else 'sol'
        else:
            lider.yon = 'asagi' if hedef_y >= lider.y else 'yukari'

        if not (0 <= hedef_x < HARITA_GENISLIK_PARSEL and 0 <= hedef_y < HARITA_YUKSEKLIK_PARSEL):
            return

        hedef_parsel = self.harita.map_grid[lider.z][hedef_y][hedef_x]

        if not hedef_parsel.yurunebilir or hedef_parsel.hasar_verir:
            lider.yol = []
            lider.yol_index = 0
            lider.yol_bul(self.harita)
            hedef_y_alt = lider.y + 1
            if 0 <= hedef_y_alt < HARITA_YUKSEKLIK_PARSEL:
                alt_parsel = self.harita.map_grid[lider.z][hedef_y_alt][lider.x]
                if alt_parsel.yurunebilir and not alt_parsel.hasar_verir:
                    lider.y = hedef_y_alt
                    return
            hedef_y_ust = lider.y - 1
            if 0 <= hedef_y_ust < HARITA_YUKSEKLIK_PARSEL:
                ust_parsel = self.harita.map_grid[lider.z][hedef_y_ust][lider.x]
                if ust_parsel.yurunebilir and not ust_parsel.hasar_verir:
                    lider.y = hedef_y_ust
                    return
            return

        if hedef_parsel.uzerindeki_alet:
            lider.duygular["korku"] += 20
            lider.yol = []
            lider.yol_index = 0
            lider.yol_bul(self.harita)
            return

        lider.x = hedef_x
        lider.y = hedef_y

    def _serbest_adim_sec(self, ajan, harita_yon, merak_agirlikli=False):
        en_iyi = None
        en_iyi_skor = float('-inf')
        ozguven = ajan.ozguven_puani()
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nx, ny = ajan.x + dx, ajan.y + dy
            if not (0 <= nx < HARITA_GENISLIK_PARSEL and 0 <= ny < HARITA_YUKSEKLIK_PARSEL):
                continue
            parsel = harita_yon.map_grid[ajan.z][ny][nx]
            if not parsel or not parsel.yurunebilir or parsel.hasar_verir:
                continue

            profil = self.kavramsal_motor.parsel_profili(parsel)
            etiket = profil['etiket']
            skor = 0.0
            if etiket == 'IYI':
                skor += 8.0
            elif etiket == 'KULLANILABILIR':
                skor += 4.5
            elif etiket == 'CIRKIN':
                skor += 2.0 if ozguven > 55 and merak_agirlikli else -3.0
            else:
                skor -= 10.0

            if getattr(parsel, 'doku_id', '') == 'YOL':
                skor += 4.0

            ilgili_beceri = profil.get('ilgili_beceri', 'direnc')
            beceri_seviyesi = ajan.beceriler.get(ilgili_beceri, 0.0)
            skor += beceri_seviyesi * (1.8 if etiket in ['IYI', 'KULLANILABILIR'] else 0.9)

            tepki = profil.get('onerilen_tepki', '')
            if tepki in ['TAKIP_ET', 'ULAS', 'YONU_IZLE', 'KULLAN']:
                skor += 4.0 + beceri_seviyesi * 0.8
            elif tepki in ['KONTROL_ET', 'ISARETI_TEST_ET', 'YONUNE_SUPHEYLE_BAK', 'RISK_DEGERLENDIR']:
                skor += (5.5 if merak_agirlikli else 1.5) + ajan.beceriler.get('tuzak_fark_etme', 0.0) * 1.2
            elif tepki in ['KACIN', 'UZAK_DUR', 'ISARETLE_VE_KAC', 'GERI_DON']:
                skor -= max(6.0, 14.0 - beceri_seviyesi * 1.1)
            elif tepki in ['TEMKINLI_GEC', 'DENGEYI_KORU', 'DOLAN_VEYA_TIRMAN', 'DOLAN']:
                skor += beceri_seviyesi * 1.1

            tercih = ajan.nesne_tercihleri.get(profil.get('nesne', ''), 0.0)
            skor += tercih * (2.4 if merak_agirlikli else 1.2)

            skor += ajan.duygular.get('merak', 0.0) * (0.20 if merak_agirlikli else 0.08)
            skor += ozguven * 0.10
            skor -= ajan.duygular.get('korku', 0.0) * 0.08
            skor -= ajan.duygular.get('suphe', 0.0) * 0.07
            skor -= (getattr(parsel, 'yavaslatma_katsayisi', 1.0) - 1.0) * 1.8

            if skor > en_iyi_skor:
                en_iyi_skor = skor
                en_iyi = (nx, ny, ajan.z)

        if en_iyi_skor < 2.0:
            return None
        return en_iyi

    def _adimi_uygula(self, ajan, hedef_x, hedef_y, hedef_z):
        dx = hedef_x - ajan.x
        dy = hedef_y - ajan.y
        if abs(dx) >= abs(dy):
            ajan.yon = 'sag' if dx >= 0 else 'sol'
        else:
            ajan.yon = 'asagi' if dy >= 0 else 'yukari'
        ajan.x, ajan.y, ajan.z = hedef_x, hedef_y, hedef_z

    def _takipci_serbest_adim(self, ajan, oncu):
        if ajan.duygular.get('merak', 0.0) < 28 and ajan.ozguven_puani() < 44:
            return False
        if random.random() > 0.18:
            return False

        hedef = self._serbest_adim_sec(ajan, self.harita, merak_agirlikli=True)
        if hedef is None:
            return False

        hedef_x, hedef_y, hedef_z = hedef
        if hedef_z != oncu.eski_z:
            return False
        if abs(hedef_x - oncu.eski_x) > 2 or abs(hedef_y - oncu.eski_y) > 2:
            return False

        self._adimi_uygula(ajan, hedef_x, hedef_y, hedef_z)
        return True

    def _hedefe_gecis_izinli(self, lider, hedef_x, hedef_y, hedef_z):
        if hedef_z == lider.z:
            return True
        if abs(hedef_z - lider.z) != 1:
            return False

        mevcut = self.harita.map_grid[lider.z][lider.y][lider.x]
        hedef = self.harita.map_grid[hedef_z][hedef_y][hedef_x]
        if mevcut is None or hedef is None:
            return False

        if hedef_z > lider.z:
            return mevcut.doku_id == 'MERDIVEN_YUKARI' and hedef.doku_id == 'MERDIVEN_ASAGI'
        return mevcut.doku_id == 'MERDIVEN_ASAGI' and hedef.doku_id == 'MERDIVEN_YUKARI'

    def _sinirda_sapmali_hedef(self, lider, dx, dy):
        """Sınırda takılmayı azaltmak için 45/135 derece benzeri sapmalarla alternatif hedef üretir.
        Eğer kenara çarpılırsa, korku artırılır ve geri çekilme sağlanır."""
        
        # Hedef koordinatları (sapmasız)
        nx_primary, ny_primary = lider.x + dx, lider.y + dy
        
        # Sınır kontrolü ve kenar tespit
        kenara_carp = False
        if not (0 <= nx_primary < HARITA_GENISLIK_PARSEL and 0 <= ny_primary < HARITA_YUKSEKLIK_PARSEL):
            kenara_carp = True
            lider.duygular["korku"] = min(100, lider.duygular["korku"] + 15)  # Korku artır
        
        # Eğer kenara çarptıysa, aşağıdaki sırayı kullan
        adaylar = []
        if not kenara_carp:
            adaylar = [(dx, dy)]  # Önce normal yön
        
        # Sapma alternatifleri (kenardan kaçışa yönelik)
        if dx != 0 and dy == 0:
            # Yatay hareket yapıyorsa, sapık yönler: tersine ve dikey
            adaylar.extend([(-dx, 1), (-dx, -1), (0, 1), (0, -1), (-dx, 0)])
        elif dy != 0 and dx == 0:
            # Dikey hareket yapıyorsa, sapık yönler: tersine ve yatay
            adaylar.extend([(1, -dy), (-1, -dy), (1, 0), (-1, 0), (0, -dy)])
        else:
            # Köşegen hareketi varsa, türlü sapkınlıklar içeren alternatifler
            adaylar.extend([(-dx, dy), (dx, -dy), (-dx, -dy), (1, 0), (-1, 0), (0, 1), (0, -1)])

        gorulen = set()
        for adx, ady in adaylar:
            if (adx, ady) in gorulen:
                continue
            gorulen.add((adx, ady))
            nx, ny = lider.x + adx, lider.y + ady
            if 0 <= nx < HARITA_GENISLIK_PARSEL and 0 <= ny < HARITA_YUKSEKLIK_PARSEL:
                return nx, ny

        # Hiçbir alternatif bulamadı (çok dar alan), hareket etme
        return None

    def render(self, surface, font, aktif_katman):
        """Faz 8: Ajanları mod rengi + kavramsal nokta + gazi çerçeve ile çizer."""
        # Faz 8: kavramsal_durum → nokta renk tablosu
        _kd_renkleri = {
            'IYI': (80, 230, 80),
            'KULLANILABILIR': (180, 180, 180),
            'CIRKAN': (255, 190, 40),
            'KOTU': (240, 60, 60),
            'KULLANILAMAZ': (180, 40, 200),
        }

        for ajan in self.ajanlar:
            if not ajan.hayatta or ajan.z != aktif_katman:
                continue

            px_x = ajan.x * PARSEK_BOYUTU
            px_y = ajan.y * PARSEK_BOYUTU
            bg_rect = pygame.Rect(px_x + 1, px_y + 1, PARSEK_BOYUTU - 2, PARSEK_BOYUTU - 2)

            # Faz 8 madde 2: Mod / gazi arka plan rengi
            gazi = getattr(ajan, 'gazi_mi', False)
            mod = getattr(ajan, 'mod', 'DENGELI')
            if gazi:
                bg_renk = (160, 120, 0)   # Koyu altın — gazi
            elif mod == 'TEHDIT':
                bg_renk = (140, 20, 20)   # Koyu kırmızı — tehdit
            elif mod == 'KESIF':
                bg_renk = (20, 60, 160)   # Koyu mavi — keşif
            else:
                bg_renk = (20, 80, 35)    # Koyu yeşil — dengeli
            pygame.draw.rect(surface, bg_renk, bg_rect, border_radius=3)

            # Gazi altın çerçeve
            if gazi:
                pygame.draw.rect(surface, (255, 200, 0), bg_rect, 2, border_radius=3)

            # Faz 8 madde 1: Sembol (emoji balon)
            if ajan.lider_mi:
                sembol = SURU_DUYUMLAR['LIDER']
            elif gazi:
                sembol = SURU_DUYUMLAR.get('GAZI', ' G ')
            elif ajan.duygular["korku"] > 50:
                sembol = SURU_DUYUMLAR['KORKU']
            elif ajan.duygular["merak"] > 50:
                sembol = SURU_DUYUMLAR['MERAK']
            else:
                sembol = SURU_DUYUMLAR['SAKIN']

            text_surf = font.render(sembol, True, BEYAZ)
            rect = pygame.Rect(px_x, px_y, PARSEK_BOYUTU, PARSEK_BOYUTU)
            text_rect = text_surf.get_rect(center=rect.center)
            surface.blit(text_surf, text_rect)

            # Faz 8 madde 2: Kavramsal durum — sağ üst köşe küçük renkli nokta
            kd = getattr(ajan, 'kavramsal_durum', 'KULLANILABILIR')
            nokta_renk = _kd_renkleri.get(kd, (180, 180, 180))
            pygame.draw.circle(surface, nokta_renk, (px_x + PARSEK_BOYUTU - 5, px_y + 5), 3)