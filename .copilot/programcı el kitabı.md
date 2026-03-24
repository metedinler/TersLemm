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

Araçlar harita üzerinde harf olarak gösterilir (M, A, B, F, C, S, T, G, K, Y).

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

## 21 Mart 2026 Teknik Güncelleme

- `ayarlar.py`:
	- `ETKI_YARICAPI = 2` eklendi (5x5x5 etki alanı).
	- `%55 kapsama` hedefi için `HARITA_TOPLAM_PARSEL`, `HEDEF_ETKI_PARSEL`, `TEK_ARAC_NOMINAL_ETKI`, `NOMINAL_TOPLAM_ETKI` hesapları eklendi.
	- Araç adetleri güncellendi (Mancınık 50, Ayna 60, Bariyer 100, Ateş 45, Sahte Yol 50).

- `harita_yoneticisi.py`:
	- Çift `Parsel` tanımı tekilleştirildi.
	- Giriş/çıkış için farklı katman zorunluluğu eklendi.
	- Su/deniz derinliği kenardan merkeze artan modele geçirildi.
	- Her katmanda en az bir yatay yol garanti edildi.
	- Araç etki kontrol yarıçapı tüm ilgili araçlarda `ETKI_YARICAPI` ile genişletildi.

- `main.py`:
	- Düzenleme modunda doğal haritayı ezen ZeminDuz döngüsü kaldırıldı.
	- `kaldir_arac` eklendi; sol sürükleme yerleştir, sağ tık kaldır akışı tamamlandı.
	- Oyun başladıktan sonra da araç seçme/yerleştirme/kaldırma/yeniden kullanım akışı eklendi.
	- Alt bilgi metni için kalın font ve açık gri renk kullanıldı.

- `suru_yoneticisi.py`:
	- Lider korku ortalaması hesabındaki `l.korku` hatası `l.duygular["korku"]` olarak düzeltildi.
	- Yol bulmada yüzey maliyeti dikkate alınarak en az efor yaklaşımı güçlendirildi.

## 22 Mart 2026 Planlama ve Mimari Yön Notu

- Bu turda Gemini 91b14b296dd1 bağlantısı incelenmiş ve mevcut kod ile tasarım farkı çıkarılmıştır.
- Uygulama stratejisi, mevcut sistemi silip baştan yazmak değil; mevcut sınıf yapısını koruyup katmanlı entegrasyon yapmaktır.
- Öncelik sırası şu şekilde belirlenmiştir:
	1. Harita omurgası: girişten çıkışa tüm katmanları bağlayan kesintisiz yol ve merdiven sistemi
	2. Yol takibi merkezli sürü davranışı
	3. Anlamsal üst akıl / kavramsal motor
	4. Genişletilmiş kalp-beyin-hormon sistemi
	5. Araçların fiziksel + duygusal etki alanı
	6. Gazi modu ve sürü iç liderlik devri
	7. Evrimsel kayıt ve benzersiz genom arşivi
	8. Emoji balonları ve oyuncu okunabilirliği
- Bu sıralama, mevcut oyunun çalışan parçalarını koruyarak risk kontrollü ilerlemek için seçilmiştir.

## 23 Mart 2026 Faz 1-9 Uygulama Ozeti

Bu bolum, oyundaki 9 fazli gelistirme setinin kod tarafinda neye karsilik geldigini kisa ama operasyonel bir dille ozetler.

1. Faz 1 (Harita Omurgasi): Giristen cikisa katman gecisli omurga rota uretilir, lider yol bulma once bu rotayi kullanir.
2. Faz 2 (Rol Tabanli Suru): Lider yol takibi birincil, takipci lider izleme birincil; kopanlar yeni lider olup yol takibine gecer.
3. Faz 3 (Kavramsal Motor): Zemin/alet algisi IYI-KOTU-CIRKIN-KULLANILABILIR-KULLANILAMAZ etiketiyle yorumlanir.
4. Faz 4 (Biyolojik Sistem): Hormonlar cevreye tepki verir, duygular hedef degerlere kontrollu yaklasir.
5. Faz 5 (Arac Psiko-Biyoloji): 10 arac yalniz fiziksel degil duygusal/hormonal etki de olusturur.
6. Faz 6 (Gazi Dinamigi): Krizde gazi puani birikir, gecici gazi mod ve liderlik devri mekanigi devreye girer.
7. Faz 7 (Evrimsel Hafiza): En iyi ajan periyodik JSON arsive yazilir, ilk oyun flag ve reset/arsivleme akisi calisir.
8. Faz 8 (Gorsel Geri Bildirim): Ajan kutularinda mod/gazi/kavramsal durum okunur sekilde gorsellestirilir.
9. Faz 9 (Denge ve Log): Olaylar, hormonlar, kavramsal durumlar loglanir; spam azaltimi ve izlenebilirlik guclenir.

## 23 Mart 2026 Son Git Sonrasi Degisiklikler

Bu bolum, bir onceki git turundan sonra oyuna eklenen ve paylasimda kritik olan degisiklikleri yazar.

1. Kod modulasyonu:
	- Ana akis hafifletildi ve yardimci siniflar oyun_bilesenleri.py dosyasina ayrildi.
	- Tasinanlar: SesAyarMenusu, AjanIzlemePenceresi, OyunKayitYonetici, OyunYoneticisi, oyun ici menu yardimcilari.

2. Harita kaliciligi:
	- HaritaYoneticisi icine JSON tabanli kaydet/yukle eklendi.
	- haritalar klasorune yazma, oyun basinda kayitli harita secme ve otomatik kayit akisina gecildi.

3. Arayuz okunabilirligi:
	- Alt durum cubugu ikinci satiri net gosterecek yukseklige cikarildi.
	- Arac kisa ozet satiri tasmadan gorunur hale getirildi.

4. Ajan durum penceresi ergonomisi:
	- Pencere artik oyun acilisinda otomatik secili/acik gelmez.
	- F2 ile ac/kapat kontrolu eklendi.
	- Genislik daraltildi; duygu ve hormon alanlari alt alta, sayilar hizali formatta gosterilir.

5. Dagitim kapsami:
	- Oyunun calismasi icin gerekli suru_yoneticisi.py ve evrimsel_hafiza icerigi depoya eklendi.
	- Gecici dosyalar (pycache, debug, log) dagitim kapsamina dahil edilmedi.