# Değişiklikler Logu

Bu dosya programdaki tüm değişiklikleri kaydeder.

## [Tarih: Güncel]

- Araç gösterimi harflere çevrildi: OyuncuAleti render() metodu str(self.arac_turu) kullanacak şekilde güncellendi, araçlar 0-9 sayı olarak gösterilir.
- Tüm araç sınıflarına arac_turu parametresi eklendi: Mancinik, Ayna, Bariyer, Ates, CikisOku, SahteYol, SendeletmeTasi, GizliCukur, KiymaMakinesi, Yonlendirici init'lerine arac_turu eklendi.
- main.py yerlestir_arac fonksiyonu arac_turu parametresi ile güncellendi.
- .copilot/programcı el kitabı.md oluşturuldu: Kod yapısı, sınıflar, oyun akışı, araçlar, renk sistemi, AI sistemi, geliştirme notları.
- README.md güncellendi: Yeni araçlar (0-9), oyun akışı, düzenleme modu kontrolleri, özellikler eklendi.
- .copilot/plan.md güncellendi: Araç harf gösterimi ve oyun akışı doğrulama adımları eklendi.

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