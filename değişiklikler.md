# Değişiklikler Logu

Bu dosya programdaki tüm değişiklikleri kaydeder.

## [Tarih: Güncel]

- Araç gösterimi harflere çevrildi: OyuncuAleti render() metodu harf dictionary'si ile güncellendi, araçlar M, A, B, F, C, S, T, G, K, Y harfleri olarak gösterilir.
- cikis_oklarini_kapiya_cevir metodundaki yanlış kod kaldırıldı, NameError giderildi.
- Dokümantasyon güncellendi: plan.md, programcı el kitabı.md, README.md, değişiklikler.md araç harf gösterimi ile güncellendi.

## [Tarih: 21 Mart 2026]

- Araç etkileşimleri implement edildi: Mancinik, SendeletmeTasi, GizliCukur, KiymaMakinesi, Yonlendirici sınıflarına etki_uygula() metotları eklendi.
- HaritaYoneticisi'ne arac_etkilerini_uygula() metodu eklendi.
- main.py oyun döngüsüne araç etkileri uygulaması eklendi.
- SuruAjani'ya hayatta özelliği eklendi, ol() metodu güncellendi.
- SuruYoneticisi guncelle() ve render() metotları ölü ajanları kaldırmak/çizmemek için güncellendi.
- .copilot/plan.md oluşturuldu.
- instructions.md'ye plan takip kuralı eklendi.
- programcınınelkıtabı.md yeni sınıflar ve metotlarla güncellendi.

## [Tarih: 21 Mart 2026 - AI Geliştirmesi]

- AI kararları geliştirildi: Duygu matrisi ve öğrenme algoritmaları implement edildi. Lider AI engelleri algılıyor, duygulara göre karar veriyor, hayatta kalan ajanlar beceri kazanıyor.
- programcınınelkıtabı.md yeni metotlarla güncellendi.

## [Tarih: 21 Mart 2026 - AI ve Seviye Geliştirmesi]

- AI derinliği artırıldı: Kolektif zeka eklendi, liderler ortalama korkuya göre karar veriyor.
- Seviye editörü eklendi: seviye_editörü.py ile harita düzenleme aracı.
- Tuzaklar belirlenip Readme.md'ye eklendi: Mancınık, Sendeletme Taşı, Gizli Çukur, Kıyma Makinesi, Yönlendirici işlevleri tanımlandı.

## [Tarih: 21 Mart 2026 - Ses Sistemi]

- Ses efektleri ve müzik eklendi: Pygame mixer ile ses sistemi implement edildi.
- .sid uzantılı müzikler için destek (dönüştürme gerekli, pygame .sid desteklemez).
- Araç yerleştirme ve ajan ölme sesleri eklendi.
- Readme.md ses dosyaları bilgisi ile güncellendi.