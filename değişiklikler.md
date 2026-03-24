# Değişiklikler Logu

Bu dosya programdaki tüm değişiklikleri kaydeder.

## [Tarih: Güncel]

- Araç gösterimi harflere çevrildi: OyuncuAleti render() metodu harf dictionary'si ile güncellendi, araçlar M, A, B, F, C, S, T, G, K, Y harfleri olarak gösterilir.
- cikis_oklarini_kapiya_cevir metodundaki yanlış kod kaldırıldı, NameError giderildi.
- Dokümantasyon güncellendi: plan.md, programcı el kitabı.md, README.md, değişiklikler.md araç harf gösterimi ile güncellendi.

## [Tarih: 21 Mart 2026 - Kural ve Plan Uygulaması]

- `.copilot/Kurallar.md` dosyasına "Mutlak Uyum Protokolü" ve "Sapma Yönetimi" eklendi.
- `main.py` içinde düzenleme modunda doğal haritayı ezen ZeminDuz reset döngüsü kaldırıldı.
- Etki alanı görselleştirme ve araç etki kontrolü ±2 (5x5x5) seviyesine güncellendi.
- Oyun içi (düzenleme sonrası) araç seçme/yerleştirme/kaldırma/yeniden kullanım akışı eklendi.
- Giriş ve çıkışın farklı katmanlarda olması zorunlu hale getirildi.
- Her katmanda en az bir yürünebilir yol üretimi eklendi.
- Su/deniz derinliği için kenardan merkeze artan derinlik yaklaşımı eklendi.
- Alt bilgi metni açık gri + kalın font ile okunur hale getirildi.
- `suru_yoneticisi.py` içinde lider korku ortalaması hatası düzeltildi ve yol bulma maliyetine zemin etkisi eklendi.
- `.copilot/plan.md` append-only olarak güncellendi ve yeni plan maddeleri için uygulama durumu işlendi.

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

## [Tarih: 22 Mart 2026 - Gemini İnceleme ve Planlama]

- Gemini bağlantısı `91b14b296dd1` incelendi ve konuşmadaki geliştirme başlıkları çıkarıldı.
- `.copilot/Kurallar.md`, `.copilot/istekler.md`, `.copilot/plan.md`, `.copilot/programcı el kitabı.md` okundu ve planlama turu bu kurallara göre yürütüldü.
- `.copilot/istekler.md` dosyasına yeni istek kaydı eklendi.
- `.copilot/plan.md` dosyasına append-only biçimde yeni entegrasyon yol haritası eklendi.
- `.copilot/programcı el kitabı.md` dosyasına 22 Mart 2026 mimari yön notu eklendi.
- Bu turda kod değişikliği yapılmadı; yalnızca mevcut kod ile tasarım farkı analiz edilip uygulama sırası netleştirildi.
## [Tarih: 22 Mart 2026 - Faz 1 ve Faz 2 Uygulamasi]

### harita_yoneticisi.py
- _omurga_rota_segment() yardimci metod eklendi: L-sekilli iki nokta arasinin (x,y,z) listesini dondurur.
- _yol_oyu() metod eklendi: Iki nokta arasini YOL dokusuyla L-seklinde kaplar; merdiven/giris/cikis hucreleri koruma alti.
- uc_boyutlu_yol_ve_merdiven_yarat(): Harita olusumunda giristen cikisa tum katmanlari YOL dokusuyla baglayan omurga yol yazar ve omurga_rota listesini hesaplar.
- HaritaYoneticisi.__init__: self.omurga_rota = [] eklendi. Harita olusturma sonunda uc_boyutlu_yol_ve_merdiven_yarat() cagrisi eklendi.

### suru_yoneticisi.py
- yol_bul(): Omurga_rota tabanli yol izleme birincil (0.1ms); A* yedek; greedy en son yedek.
- _greedy_yedek() eklendi: Eski greedy kodu ayri yedek metod olarak korundu.
- lider_yapay_zeka(): Faz 2 rol tabanli davranis - kolektif zeka -> korku/suphe override -> yol takibi birincil -> kesif yuruyusu ikincil.
- zinciri_kopar(): Yeni lider terfi etince aninda yol_bul() cagrisi eklendi; kopan suru parcasi otomatik yol takibine gecer.
- SURU_BASLANGIC_BEKLEME_TIK -> SURU_BASLANGIC_BEKLEME_TIK_TEMEL sabit ismi uyumsuzlugu duzeltildi.

### .copilot/plan.md
- Uygulama Prensipleri madde 3 mantik hatasina gore duzeltildi.
- Faz 2 yeniden yazildi: Rol Tabanli Suru Davranisi (Lider/Takipci/Kopan) basligi ile madde 1-2 duzeltildi.

### Dogrulama
- Tum py dosyalari: py_compile ile syntax temiz.
- omurga_rota: tum katmanlari kapsayan 50-100 adimlik yol, hedef mesafesi 0.
- yol_bul() suresi: 0.1ms (omurga listesi okuma).
- Oyun 4 saniye sorunsuz calisti.
