# Programcının El Kitabı

Bu dosya programın çalışma ilkeleri, tasarım artefactları ve her modülün, sınıfın, metodun ve bağımsız fonksiyonun görevlerini içerir.

## Genel Çalışma İlkeleri

- Oyun Python + Pygame ile geliştirilir.
- OOP (Nesne Yönelimli Programlama) kullanılır.
- Türkçe değişken ve sınıf adları kullanılır.
- Modüller silinmez, sadece eklenir veya güncellenir.

## Modüller

### ayarlar.py
Sabit değerler, renkler, emojiler ve oyun parametreleri.

### harita_yoneticisi.py
Harita sınıfları ve yönetim.

### suru_yoneticisi.py
Sürü ajanları ve hareket mantığı.

### seviye_editörü.py
Harita düzenleme aracı.

### main.py
Ana oyun döngüsü.

## Sınıflar ve Metotlar

### harita_yoneticisi.py

#### Parsel
Temel harita hücresi sınıfı.
- Özellikler: x, y, z, doku_id, yurunebilir, yavaslatma_katsayisi, kazilabilir, bogulma_riski, hasar_verir, uzerindeki_alet, suru_ajanlari
- Metotlar: render(surface, font) - Hücreyi ekrana çizer.

#### ZeminDuz, DuvarKaya, Dag, SuGol
Parsel alt sınıfları, belirli özelliklerle özelleştirilmiş.

#### OyuncuAleti
Oyuncu araçlarının temel sınıfı.
- Özellikler: x, y, z, doku_id, maks_kapasite, mevcut_kapasite, gizlilik_carpani, zemin_katsayisi
- Metotlar: kullan() - Kapasiteyi azaltır, render(surface, font) - Araç sembolünü çizer.

#### Mancinik(OyuncuAleti)
Mancınık aracı.
- __init__(x, y, z, zemin_tipi) - Zemin tipine göre kapasite ayarlar.
- etki_uygula(ajanlar) - Yakındaki ajanları fırlatır, yön değiştirir ve hızlandırır.

#### SendeletmeTasi(OyuncuAleti)
Sendeletme taşı aracı.
- etki_uygula(ajanlar) - Yakındaki ajanları sendeletir, yön değiştirir ve yavaşlatır.

#### GizliCukur(OyuncuAleti)
Gizli çukur aracı.
- etki_uygula(ajanlar) - Üzerindeki ajanı öldürür.

#### KiymaMakinesi(OyuncuAleti)
Kıyma makinesi aracı.
- etki_uygula(ajanlar) - Üzerindeki ajanı öldürür.

#### Yonlendirici(OyuncuAleti)
Yönlendirici aracı.
- etki_uygula(ajanlar) - Yakındaki ajanların yönünü değiştirir.

#### HaritaYoneticisi
Harita yönetim sınıfı.
- Özellikler: max_katman, map_grid, aktif_katman
- Metotlar: txt_den_yukle(klasor_yolu) - Haritayı dosyadan yükler, aktif_katmani_degistir(yeni_kat), render(surface, font), arac_etkilerini_uygula(ajanlar) - Tüm araçların etkilerini ajanlara uygular.

### suru_yoneticisi.py

#### SuruAjani
Sürü ajanı sınıfı.
- Özellikler: id, x, y, z, hayatta, onumdeki_ajan, arkamdaki_ajan, lider_mi, can, hiz, duygular (korku, merak, şüphe), beceriler (yuzme, tirmanma, tuzak_fark_etme, engelden_kacma)
- Metotlar: beceri_ogren(beceri_adi, miktar) - Beceriyi artırır, suya_gir(zemin_zorlugu) - Suda yüzme, can azaltır, korku artırır, hayatta kalırsa merak artırır, arkaya_bilgi_ilet(beceri_adi, ogretme_miktari) - Bilgiyi zincir boyunca iletir, ol() - Ajani öldürür, hayatta=False yapar, zinciri koparır.

#### SuruYoneticisi
Sürü yönetim sınıfı.
- Özellikler: harita, ajanlar, liderler, maks_lider, tick_sayaci
- Metotlar: suru_yarat(baslangic_x, baslangic_y, boyut), zinciri_kopar(kopan_ajan), guncelle() - Ölü ajanları kaldırır, öğrenme verir, AI kararlarını çalıştırır, lider_yapay_zeka(lider) - Duygulara göre yön seçer, engelleri algılar, tuzaklardan kaçar, render(surface, font, aktif_katman) - Duygulara göre emoji gösterir.

### main.py

#### OyunYoneticisi
Oyun kazanma/kaybetme yönetim sınıfı.
- Özellikler: suru_yon, baslangic_nufusu, olenler, dogru_cikis, sahte_cikis, kazanma_kosulu, kaybetme_kosulu
- Metotlar: guncelle() - Ajan durumlarını kontrol eder ve kazanma/kaybetme koşullarını belirler, render(surface, font) - UI'yi çizer.