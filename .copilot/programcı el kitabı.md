# Programcı El Kitabı: Ters Lemmings

## Genel Bakış
Ters Lemmings, klasik Lemmings oyununu tersine çeviren bir puzzle oyunu. Oyuncu tuzaklar kurar, AI sürü karar verir ve zincirleme takip eder. Çok katmanlı harita, duygu matrisi, öğrenme sistemi ile özgün bir deneyim.

## Kod Yapısı
- **main.py**: Ana oyun döngüsü, düzenleme modu, olay yönetimi.
- **ayarlar.py**: Sabitler, renkler, emojiler, araç limitleri.
- **harita_yoneticisi.py**: Parsel sınıfları, araç sınıfları, harita oluşturma.
- **suru_yoneticisi.py**: SuruAjani ve SuruYoneticisi sınıfları, hareket ve AI.
- **sid_player.py**: Müzik sistemi.

## Sınıflar
### Parsel
Temel harita hücresi. Özellikler: yurunebilir, yavaslatma_katsayisi, kazilabilir, bogulma_riski, hasar_verir, derinlik.

Alt sınıflar: ZeminDuz, DuvarKaya, SuGol, Deniz, Dag, vb.

### OyuncuAleti
Oyuncu araçları için temel sınıf. Özellikler: maks_kapasite, mevcut_kapasite, gizlilik_carpani, zemin_katsayisi.

Alt sınıflar: Mancinik, Ayna, Bariyer, Ates, CikisOku, SahteYol, SendeletmeTasi, GizliCukur, KiymaMakinesi, Yonlendirici.

### SuruAjani
Sürü ajanları. Özellikler: can, hiz, yon, duygular, beceriler, deneyim.

### SuruYoneticisi
Sürü yönetimi. Zincirleme hareket, lider AI, kopma mantığı.

## Oyun Akışı
1. Harita renklerle rastgele üretilir.
2. Oyuncu düzenleme modunda tuzaklar koyar (fare ile).
3. Oyuncu oyunu başlatır.
4. Sürü girer, AI sistemleri çalışır.
5. Kazanma/kaybetme koşulları kontrol edilir.

## Araçlar
0: Mancinik - Yakındaki ajanları fırlatır.
1: Ayna - Yönü ters çevirir.
2: Bariyer - Engel koyar, yavaşlatır.
3: Ateş - Hasar verir, hızlandırır.
4: Çıkış Oku - Çıkış işaretler.
5: Sahte Yol - Lemler tercih eder.
6: Sendeletme Tası - Yön değiştirir, yavaşlatır.
7: Gizli Çukur - Sahte çıkış.
8: Kıyma Makinesi - Öldürür.
9: Yönlendirici - Yön değiştirir.

Araçlar harita üzerinde sayı olarak gösterilir (0-9).

## Renk Sistemi
RENKLER sözlüğü ile harita türlerine renk atanır. Su türleri derinliğe göre gradyan.

## AI Sistemi
- Duygu matrisi: sakin, lider, korku, merak, şüphe.
- Öğrenme: Deneyim kazanma, kolektif zeka.
- Hareket: Pathfinding ile yol bulma, zincirleme takip.

## Geliştirme Notları
- Kod Türkçe yazılır, no pseudo-code.
- Her adımda git commit.
- Dokümantasyon: Bu dosya, README.md, değişiklikler.md.
- Görsel: Text-mode, emoji tabanlı, araçlar sayı.

## Hata Ayıklama
- Pygame olayları kontrol et.
- Harita grid sınırları.
- AI kararları test et.
- Ses sistemi fallback kullan.