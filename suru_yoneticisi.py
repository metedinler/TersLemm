# suru_yoneticisi.py
import random
from ayarlar import *

class SuruAjani:
    def __init__(self, x, y, ajan_id):
        # 1. KİMLİK VE POZİSYON
        self.id = ajan_id
        self.x = x
        self.y = y
        self.z = 0  # Katman
        self.hayatta = True
        
        # 2. ZİNCİR BAĞLANTILARI (Linked List Mantığı)
        self.onumdeki_ajan = None  # Liderse bu None'dır
        self.arkamdaki_ajan = None
        self.lider_mi = False
        
        # 3. TEMEL STATLAR
        self.can = 100.0
        self.hiz = 1.0  # Parsek geçiş hızı
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
            "engelden_kacma": 0.0
        }
    
    # --- BECERİ VE ÖĞRENME METOTLARI ---

    def beceri_ogren(self, beceri_adi, miktar):
        """Arkaya doğru yayılan bilgi transferi bu metodu tetikler."""
        if beceri_adi in self.beceriler:
            self.beceriler[beceri_adi] += miktar
            # Kapasite sınırı (Max 10)
            if self.beceriler[beceri_adi] > 10.0:
                self.beceriler[beceri_adi] = 10.0
            print(f"Ajan {self.id} {beceri_adi} becerisini geliştirdi! Yeni Seviye: {self.beceriler[beceri_adi]}")
    
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

    def arkaya_bilgi_ilet(self, beceri_adi, ogretme_miktari):
        """Bilgi zincir boyunca geriye akar, gittikçe güçlenir (veya zayıflar)."""
        if self.arkamdaki_ajan:
            # Arkadaki ajan bu bilgiyi alır
            self.arkamdaki_ajan.beceri_ogren(beceri_adi, ogretme_miktari)
            
            # Senin kuralın: En arkadakiler daha iyi öğrenir! 
            # Bilgi arkaya gittikçe çarpanı artırabiliriz.
            yeni_miktar = ogretme_miktari * 1.1 
            self.arkamdaki_ajan.arkaya_bilgi_ilet(beceri_adi, yeni_miktar)

    # --- DURUM METOTLARI ---

    def ol(self):
        print(f"Ajan {self.id} öldü!")
        self.hayatta = False
        # Zinciri koparma işlemi: Arkamdaki ajan lidersiz kaldı!
        if self.arkamdaki_ajan:
            self.arkamdaki_ajan.onumdeki_ajan = None
            self.arkamdaki_ajan.lider_mi = True # O artık yeni lider!
            self.arkamdaki_ajan.duygular["suphe"] += 50 # Şok etkisi

class SuruYoneticisi:
    def __init__(self, harita_yoneticisi):
        self.harita = harita_yoneticisi
        self.ajanlar = []       # Haritadaki tüm yaşayan ajanlar
        self.liderler = []      # Sadece lider olanlar (Max 4 kuralı için)
        self.maks_lider = 4
        self.tick_sayaci = 0    # Yapay zekanın düşünme hızını ayarlamak için
    
    def suru_yarat(self, baslangic_x, baslangic_y, boyut):
        """Bölüm başında sürüyü birbirine bağlı bir zincir olarak yaratır."""
        onceki_ajan = None
        
        for i in range(boyut):
            yeni_ajan = SuruAjani(baslangic_x, baslangic_y, i)
            
            # İlk doğan ajan Liderdir
            if i == 0:
                yeni_ajan.lider_mi = True
                self.liderler.append(yeni_ajan)
            else:
                # Arkadan gelenleri birbirine bağla (Linked List)
                yeni_ajan.onumdeki_ajan = onceki_ajan
                onceki_ajan.arkamdaki_ajan = yeni_ajan
            
            self.ajanlar.append(yeni_ajan)
            onceki_ajan = yeni_ajan
            
        print(f"{boyut} kişilik sürü yaratıldı ve zincirlendi!")

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
            self.liderler.append(kopan_ajan)
            print(f"Zincir koptu! Ajan {kopan_ajan.id} YENİ LİDER oldu.")
        else:
            kopan_ajan.duygular["korku"] += 80  # Lidersiz kaldılar, panik!
            print(f"Zincir koptu ama liderlik kontenjanı dolu. Ajan {kopan_ajan.id} panikte!")

    def guncelle(self):
        """Bu fonksiyon main.py içindeki oyun döngüsünde sürekli çağrılacak."""
        self.tick_sayaci += 1
        
        # Ölü ajanları kaldır
        self.ajanlar = [ajan for ajan in self.ajanlar if ajan.hayatta]
        self.liderler = [lider for lider in self.liderler if lider.hayatta]
        
        # Öğrenme: Hayatta kalan ajanlar zamanla beceri kazanır
        for ajan in self.ajanlar:
            if ajan.hayatta:
                # Küçük rastgele beceri artışı
                import random
                beceri_adi = random.choice(list(ajan.beceriler.keys()))
                ajan.beceri_ogren(beceri_adi, 0.1)
        
        # Yapay zeka her karede (frame) düşünmez. Saniyede örneğin 5 kez karar verir.
        # Bu da hem oyunu satranç gibi oynanabilir kılar hem işlemciyi rahatlatır.
        if self.tick_sayaci >= (FPS // 5): 
            self.tick_sayaci = 0
            
            # 1. Aşama: Tüm ajanların mevcut konumunu hafızaya al
            for ajan in self.ajanlar:
                ajan.eski_x = ajan.x
                ajan.eski_y = ajan.y

            # 2. Aşama: Liderler karar verir ve hareket eder
            for lider in self.liderler:
                self.lider_yapay_zeka(lider)

            # 3. Aşama: Takipçiler sadece önündekinin "eski" konumuna geçer
            for ajan in self.ajanlar:
                if not ajan.lider_mi and ajan.onumdeki_ajan:
                    ajan.x = ajan.onumdeki_ajan.eski_x
                    ajan.y = ajan.onumdeki_ajan.eski_y

    def lider_yapay_zeka(self, lider):
        """Gelişmiş AI: Duygular, engeller ve tuzaklar dikkate alınarak karar verir."""
        import random
        
        # Kolektif zeka: Diğer liderlerin duygularını kontrol et
        toplam_korku = sum(l.korku for l in self.liderler)
        ortalama_korku = toplam_korku / len(self.liderler) if self.liderler else 0
        
        # Eğer ortalama korku yüksekse, tüm liderler daha temkinli olur
        if ortalama_korku > 60:
            lider.duygular["korku"] = min(100, lider.duygular["korku"] + 20)
        
        # 1. Duygulara göre temel karar
        korku = lider.duygular["korku"]
        merak = lider.duygular["merak"]
        suphe = lider.duygular["suphe"]
        
        # Korku yüksekse geri dön
        if korku > 70:
            hedef_x = lider.x - 1
            hedef_y = lider.y
        # Merak yüksekse rastgele yön
        elif merak > 50:
            yonler = [(1, 0), (-1, 0), (0, 1), (0, -1)]
            dx, dy = random.choice(yonler)
            hedef_x = lider.x + dx
            hedef_y = lider.y + dy
        # Şüphe yüksekse dur (hareket etme)
        elif suphe > 60:
            return  # Hareket etme
        # Normal: Sağa git
        else:
            hedef_x = lider.x + 1
            hedef_y = lider.y

        # 2. Harita sınırlarını kontrol et
        if not (0 <= hedef_x < HARITA_GENISLIK_PARSEL and 0 <= hedef_y < HARITA_YUKSEKLIK_PARSEL):
            return  # Sınır dışı, hareket etme

        # 3. Hedef parselleri kontrol et
        hedef_parsel = self.harita.map_grid[lider.z][hedef_y][hedef_x]
        
        # Duvar veya tehlikeli zemin varsa dönme
        if not hedef_parsel.yurunebilir or hedef_parsel.hasar_verir:
            # Alternatif yön dene: Aşağı
            hedef_y_alt = lider.y + 1
            if 0 <= hedef_y_alt < HARITA_YUKSEKLIK_PARSEL:
                alt_parsel = self.harita.map_grid[lider.z][hedef_y_alt][lider.x]
                if alt_parsel.yurunebilir and not alt_parsel.hasar_verir:
                    lider.x = lider.x
                    lider.y = hedef_y_alt
                    return
            # Yukarı dene
            hedef_y_ust = lider.y - 1
            if 0 <= hedef_y_ust < HARITA_YUKSEKLIK_PARSEL:
                ust_parsel = self.harita.map_grid[lider.z][hedef_y_ust][lider.x]
                if ust_parsel.yurunebilir and not ust_parsel.hasar_verir:
                    lider.x = lider.x
                    lider.y = hedef_y_ust
                    return
            return  # Hareket edemiyor

        # 4. Tuzak kontrolü: Üzerinde araç varsa kaç
        if hedef_parsel.uzerindeki_alet:
            lider.duygular["korku"] += 20  # Korku artır
            return  # Kaç, hareket etme

        # 5. Hareket et
        lider.x = hedef_x
        lider.y = hedef_y

    def render(self, surface, font, aktif_katman):
        """Ajanları ekrana karakter olarak çizer."""
        for ajan in self.ajanlar:
            if not ajan.hayatta or ajan.z != aktif_katman:
                continue # Ölü ajan veya başka kattaysa çizme

            # Ajanın durumuna göre emojiyi belirle
            if ajan.lider_mi:
                sembol = SURU_DUYUMLAR['LIDER']
            elif ajan.duygular["korku"] > 50:
                sembol = SURU_DUYUMLAR['KORKU']
            elif ajan.duygular["merak"] > 50:
                sembol = SURU_DUYUMLAR['MERAK']
            else:
                sembol = SURU_DUYUMLAR['SAKIN']

            px_x = ajan.x * PARSEK_BOYUTU
            px_y = ajan.y * PARSEK_BOYUTU
            
            # Yazıyı oluştur ve ekrana bas
            text_surf = font.render(sembol, True, BEYAZ)
            rect = pygame.Rect(px_x, px_y, PARSEK_BOYUTU, PARSEK_BOYUTU)
            text_rect = text_surf.get_rect(center=rect.center)
            surface.blit(text_surf, text_rect)