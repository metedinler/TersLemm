# Belge vs Kod Karşılaştırması ve Güncelleme Planı
## Tarih: 23 Mart 2026

---

## 1. NEDEN BU BELGE YAZILDI

Kullanıcı haklı olarak şunu talep etti:
- Önce tasarım belgelerini oku
- Belgede ne var, kodda ne var karşılaştır
- Bir plan yaz
- Beni onaylatmadan kod yazma

Bu belge tam olarak bu amaca hizmet etmektedir.

---

## 2. TASARIM BELGESIN DE OLAN AMA KODDA OLMAYAN ÖZELLİKLER

### 2.1 SinirAgi (Yapay Sinir Ağı) — KRİTİK EKSİK

**Belgede ne var (bılgıler.md, satır ~5021):**
- Her ajanda `self.beyin = SinirAgi()` nesnesi olacak
- Mimari: **11 girdi → 5 gizli → 3 çıktı**
- Girdi nöronları (11 adet):
  1. korku (0-100, normalize edilmiş)
  2. merak (0-100, normalize edilmiş)
  3. suphe (0-100, normalize edilmiş)
  4. adrenalin (hormon)
  5. kortizol (hormon)
  6. dopamin (hormon)
  7. serotonin (hormon)
  8. oksitosin (hormon)
  9. husran (hormon)
  10. cesaret_skoru (mizac'tan)
  11. lider_mesafe (zincirdeki pozisyon, 0-1)
- Gizli katman: 5 nöron, sigmoid aktivasyon
- Çıktı katmanı (3 nöron):
  1. hiz_carpani — hareketi hızlandır/yavaşlat
  2. yon_sapmasi — liderden sap/sapma
  3. kacis_egilimi — zinciri kop/kopyalarsa panoik
- **Kütüphane YOK** — saf Python, matris çarpımı
- Her ajan doğuşta `random.uniform(-0.1, 0.1)` ile unique ağırlık alır
- Evrim: Başarılı ajan ağırlıkları `EvrimselHafiza` ile sonraki nesle aktarılır

**Kodda ne var:**
- `SinirAgi` sınıfı: **YOK**
- `self.beyin`: **YOK**
- Var olan en yakın şey: `durum_matrisi_karari()` — bu kural tabanlı (if-else + skor matrisi), gerçek ağırlıklı hesap değil

---

### 2.2 Asansör (Elevator) — EKSİK

**Belgede ne var (bılgıler.md, satır ~6974):**
```python
class Asansor:
    # Konforludur, dopamini artırır, hüsranı azaltır
    # Kapasite var (kaç kişi sığar)
    # Bekleme sırası var (kuyruk mekanizması)
    # Farklı kat hızı (merdivenin 2 katı hızlı)
```
- Harita üzerinde `ASANSOR_YUKARI` ve `ASANSOR_ASAGI` parsel tipi
- Ajan asansöre gelince bekler, dolarsa BORCUKLA bayiyortır
- Bekleme süresinde sabır/bekleyiş duygusu

**Kodda ne var:**
- Sadece `MERDIVEN_YUKARI` / `MERDIVEN_ASAGI` mevcut
- `Asansor` sınıfı: **YOK**
- `katman_gecisi_izinli_mi()` sadece merdiveni tanıyor

---

### 2.3 10 Ek Araç (Araç 11–20) — EKSİK

**Kodda olan (10 araç):**
1. Mancinik
2. Ayna
3. Bariyer
4. Ates
5. CikisOku
6. SahteYol
7. SendeletmeTasi
8. GizliCukur
9. KiymaMakinesi
10. Yonlendirici

**Belgede olan ama olmayan (araç 11-20):**
| No | İsim | Belge İsmi | Etki |
|----|------|-----------|------|
| 11 | Feromon İstasyonu | Koloni Sinyali | Oksitosin↑ (sürüyü kümeler) |
| 12 | Öfori Gazı | Kimyasal | Dopamin↑↑ (sürü hedefe kör koşar) |
| 13 | Korku Gazı / Sis Bombası | Kimyasal | Adrenalin↑↑ (ani panik dağılma) |
| 14 | Donma Alanı | Biyolojik | Kortizol↑ (zincir donup kalır) |
| 15 | Depresif Alan | Biyolojik | Serotonin↓ (liderlik krizi) |
| 16 | Sosyal Ayna | Sosyal | Şüphe↑ (sürü kendini sorgulatır) |
| 17 | Engel Yansıtıcı | Fiziksel | Mevcut engelleri kopyalar |
| 18 | Ses Yayıcı | Psikolojik | Belirtilen duyguyu tetikler |
| 19 | Gölge Rehber | Sosyal Mühendislik | Sahte lider yaratır, sürüyü peşine takar |
| 20 | Kaos Çekirdeği | Sistemik | SinirAgi ağırlıklarını sıfırlar, karakter değişimi |

---

### 2.4 %30 Evrim Tetikleyicisi — EKSİK

**Belgede:**
- Eğer doğru kapıdan %30 geçerse → tüm sürü büyük evrim bonusu alır
- Liderler özellikle çok deneyim kazanır
- EvrimselHafiza'ya güçlendirilmiş ağırlıklarla kayıt yapılır

**Kodda (oyun_bilesenleri.py, ~satır 483):**
```python
if self.dogru_cikis / self.baslangic_nufusu <= 0.1:
    kazanma_kosulu = True
```
- Sadece %10 kontrolü var, %30 evrimi YOK

---

## 3. KODDA OLAN VE BELGEYE UYGUN OLAN ÖZELLİKLER ✅

| Özellik | Belge | Kod | Durum |
|---------|-------|-----|-------|
| BiyolojikSistem (7 hormon) | ✅ | ✅ | TAM |
| Duygu matrisi (korku/merak/suphe) | ✅ | ✅ | TAM |
| Zincir (linked list) yapısı | ✅ | ✅ | TAM |
| En fazla 4 lider kuralı | ✅ | ✅ | TAM |
| Gazi modu | ✅ | ✅ | TAM |
| Alt-grup ayrışma | ✅ | ✅ | TAM |
| KavramsalMotor | ✅ | ✅ | TAM |
| EvrimselHafiza (JSON) | ✅ | ✅ | TAM |
| A* pathfinding + omurga | ✅ | ✅ | TAM |
| Merdiven (katman geçişi) | ✅ | ✅ | TAM |
| Beceri sistemi (yüzme, tırmanma vs.) | ✅ | ✅ | TAM |
| mizac (cesaret/sadakat/zeka) | ✅ | ✅ | Son oturumda eklendi |
| durum_modu matrisi | ✅ | ✅ | Son oturumda eklendi |
| duygu bulaşma (sosyal) | ✅ | ✅ | Son oturumda eklendi |
| kopma_egilimi | ✅ | ✅ | Son oturumda eklendi |
| **SinirAgi** | ✅ | ❌ | **EKSİK** |
| Asansör | ✅ | ❌ | **EKSİK** |
| Araç 11-20 | ✅ | ❌ | **EKSİK** |
| %30 evrim tetikleyici | ✅ | ❌ | **EKSİK** |

---

## 4. SİNİR AĞI HAKKINDA SORU: "NE OLACAK, NASIL ÇALIŞACAK?"

### 4.1 Şu An Nasıl Çalışıyor (Kural-Tabanlı Hibrit)

```
Her tick:
  1. cevre_ozeti hesapla (KavramsalMotor)
  2. BiyolojikSistem.cevre_uyarimina_tepki(ozet)
  3. BiyolojikSistem.duygulara_yansit(duygular)
  4. durum_matrisi_karari(cevre_ozeti)  ← KURAL TABANLI (if-else + skor)
     → panik_skoru = korku*0.75 + adrenalin*0.55 - cesaret*18
     → hangi skor kazanırsa o mod
  5. lider_yapay_zeka() → hedef seç, yürü
```

Bu sistema şu anlama geliyor: Ajanın kararı HER ZAMAN aynı formülden çıkar. Ajan A ve Ajan B aynı çevrede aynı kararı verir (sadece hormon farkları var, ama formül aynı). Bu belge açıklar: "Bu bir sinir ağı değil, kural tabanlı uzman sistemdir."

### 4.2 SinirAgi Eklenirsene Nasıl Çalışacak

```
Her tick:
  1. (aynı) cevre_ozeti hesapla
  2. (aynı) BiyolojikSistem güncelle
  3. (aynı) durum_matrisi_karari() çalış → kural-tabanlı mod
  4. [YENİ] sinir_karari(ceyre_ozeti) çalış:
       girdiler = [korku/100, merak/100, suphe/100,
                   adrenalin/100, kortizol/100, dopamin/100,
                   serotonin/100, oksitosin/100, husran/100,
                   cesaret, zincir_pozisyon]
       [hiz, yon, kacis] = beyin.dusun(girdiler)  ← matris çarpımı
  5. lider_yapay_zeka() hareket kararında:
       - kural_modu = durum_modu  (PANIK, KESIF vs.)
       - nn_kacis = beyin_cikti[2]
       - FINAL = blend(kural_modu, nn_kacis, kacis_agirlik=0.3)
```

**Fark:**
- Ajan A: weights = [-0.08, 0.12, -0.04, ...] → cesur
- Ajan B: weights = [0.09, -0.11, 0.06, ...] → korkak
- Aynı çevrede, Ajan A geçer, Ajan B kaçar → gerçek bireysel karakter

### 4.3 Neden Uyum Sorunu OLMAYACAK

Mevcut `BiyolojikSistem` tam 7 hormon üretiyor: dopamin, adrenalin, oksitosin, serotonin, kortizol, endorfin, husran — bunlar tam olarak sinir ağının girdi nöronları. `mizac.cesaret` de zaten var. Tek hesaplanacak yeni şey `zincir_pozisyon` (kaçıncı ajan olduğu, 0-1 normalize).

Uyum sorunu yok. Altyapı hazır. Sinir ağı bu altyapının üstüne oturuyor.

---

## 5. SİLMEDEN vs SİLEREK: İKİ YAKLAŞIM

### Yaklaşım A: Kod Silinmeden (Ekleyerek)

**Ne yapılır:**
1. `SinirAgi` sınıfı `BiyolojikSistem`'den önce eklenir (yeni sınıf)
2. `SuruAjani.__init__`'e `self.beyin = SinirAgi()` satırı eklenir
3. `SuruAjani`'ye yeni metot: `sinir_karari(cevre_ozeti)` eklenir
4. `lider_yapay_zeka()` içinde var olan mantığın yanına NN çıktısı blend edilir
5. `EvrimselHafiza.arsive_yaz()` fonksiyonu ağırlıkları da kaydedecek şekilde genişletilir
6. `suru_yarat()` archive'dan ağırlıkları seed olarak yükler

**Avantajlar:**
- Mevcut kod çalışmaya devam eder
- Kural sistemi güvenlik ağı olarak kalır
- Eğer NN tuhaf davranırsa kural sistemi düzeltirir
- Hiçbir özellik kaybolmaz

**Dezavantajlar:**
- İki karar sistemi birlikte çalışır → bazen çakışabilir
- Blend katsayısı ayarlamak gerekir (`kural 70% + NN 30%` gibi)
- Daha fazla kod = daha fazla test

### Yaklaşım B: Silerek (Değiştirerek)

**Ne yapılır:**
1. `durum_matrisi_karari()` metodu kaldırılır
2. Yerine `sinir_karari()` tam yetkiyle girer
3. `lider_yapay_zeka()` içindeki `durum_modu == "PANIK"` gibi kontroller kaldırılır
4. Kararın tamamı NN çıktısından gelir

**Avantajlar:**
- Temiz, minimal kod
- Çift karar sistemi çakışması yok
- Daha az satır

**Dezavantajlar:**
- İlk aşamada random ağırlıklar tuhaf davranışlar çıkarabilir
- `durum_modu` değişkeni (PANIK, KESIF vs.) boşa düşer
- Mevcut `mizac.cesaret` sistemi etkisizleşir (NN ağırlıkları onun yerini alır)
- Son oturumda eklenen 4 özellik anlamsız hale gelebilir
- Geri dönmek zor

### ÖNERİ

**Yaklaşım A** ile başlamak daha güvenli. Nedeni:
- `durum_matrisi_karari()` içindeki `panik/kesif/itaat/savunma` modları hâlâ yararlı
- Bu modlar NN'in birer **girdisi** olabilir (bool değer olarak)
- Evrim mekanizması oturduğunda, NN güçlenince Yaklaşım B'ye geçilebilir

---

## 6. UYGULAMA SIRASI (ONAY BEKLENİYOR)

Aşağıdaki 4 iş için **senin onayını bekliyorum**. Hangisinden başlayacağımı söyle:

| # | Görev | Değiştirilecek Dosya | Yaklaşık Yeni Satır |
|---|-------|---------------------|---------------------|
| A | SinirAgi sınıfı + self.beyin entegrasyonu | suru_yoneticisi.py | ~80 satır ekleme |
| B | Asansör sınıfı | harita_yoneticisi.py + ayarlar.py | ~60 satır ekleme |
| C | 10 ek araç (Feromon, Gölge Rehber, Kaos Çekirdeği dahil) | harita_yoneticisi.py + ayarlar.py + main.py | ~200 satır ekleme |
| D | %30 evrim tetikleyicisi | oyun_bilesenleri.py | ~20 satır ekleme |

**Tüm işlemler additive (ekleyerek) yapılacak. Hiçbir mevcut kod silinmeyecek.**

---

## 7. SİLİNEN METİN / KOD DURUMU

Geçmiş oturumlarda bazı kodların silindiğinden şikayetçisin.
Bu belgede kayıt altına aldım:

- Mevcut `suru_yoneticisi.py`: KavramsalMotor + BiyolojikSistem + EvrimselHafiza + SuruAjani + SuruYoneticisi hepsi MEVCUT
- Son oturumda eklenenler: mizac, durum_modu, kopma_egilimi, durum_matrisi_karari(), _duygu_bulastir() — MEVCUT
- Silinmiş herhangi bir şey tespit edilmedi

Eğer silinen özellik varsa, git log ile en son commiti gösterebilirim veya belirli bir satırın mevcut olup olmadığını kontrol edebilirim.

---

*Bu belge onay almadan kod yazmama taahhüdü altında hazırlanmıştır.*
*Onay ver → kodlama başlar. Onay yok → bekler.*

---

## 8. HIBRIT MODEL A-D UYGULAMA DURUMU (23 Mart 2026)

Bu turda kullanicinin istegiyle A-D adimlari kodlanmaya baslandi.

### A) SinirAgi hibrit entegrasyonu
- Eklendi: `SinirAgi` sinifi (11-5-3)
- Eklendi: `SuruAjani.beyin`, `SuruAjani.sinir_karari()`
- Hibrit karar: `durum_matrisi_karari()` + `nn_karar.kopma_bias`
- Lider davranisinda NN hiz/yon sapmasi kullaniliyor

### B) Asansor altyapisi
- Eklendi: `AsansorYukari`, `AsansorAsagi` parsel siniflari
- Eklendi: asansor doku/renk/sembol tanimlari
- Eklendi: katman gecisinde asansor cifti kabul kurali

### C) 20 arac UI/akisi
- Eklendi: class tabanli `AracPaneli` (2x10 = 20 grafik dugme)
- Eklendi: `1-0` (ilk satir) + `Shift+1-0` (ikinci satir) secim
- Eklendi: oyun ve duzenleme modunda panelden mouse secimi
- Not: ilk 10 arac islevsel, 11-20 butonlari secilebilir/izlenebilir ama etki siniflari henuz yazim asamasinda

### D) %30 evrim tetikleyicisi
- Eklendi: `OyunYoneticisi` icinde %30 dogru cikis esiginde tek-seferlik evrimsel sicrama
- Etki: beceri/hormon bonusu + arsive yazma tetigi

