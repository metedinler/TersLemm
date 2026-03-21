## Plan: Ters Lemmings Oyun Geliştirme

Yeni nesil sistemik puzzle oyunu geliştirmek. Oyuncu tuzaklar kurar, AI sürü karar verir ve zincirleme takip eder. Çok katmanlı harita, duygu matrisi, öğrenme sistemi ile özgün bir deneyim.

**Adımlar**
1. Kod yapısını analiz et: Gemini konuşmasındaki Python sınıflarını incele, OOP mimarisini anla. (Tamamlandı)
2. Proje yapısını oluştur: ters_lemmings klasörü, main.py, ayarlar.py, harita_yoneticisi.py, suru_yoneticisi.py dosyalarını oluştur. (Tamamlandı)
3. Harita sistemini implement et: Çok boyutlu dizi, pasif nesneler, .txt'den yükleme. (Tamamlandı)
4. Sürü ajanlarını implement et: SuruAjani sınıfı, duygular, beceriler, öğrenme. (Tamamlandı)
5. Sürü yöneticisini implement et: Zincirleme hareket, lider AI, kopma mantığı. (Tamamlandı)
6. Oyuncu araçlarını ekle: Mancınık, taş, çukur, kıyma makinesi, ayna, bariyer sınıfları, eskime formülleri. (Tamamlandı)
7. Oyun döngüsünü tamamla: Güncelleme, render, kazanma/kaybetme koşulları. (Tamamlandı)
8. Araç etkileşimlerini implement et: Mancınık fırlatma, taş sendeletme, çukur düşürme kodlarını ekle. (Tamamlandı)
9. AI kararlarını geliştir: Duygu matrisi ve öğrenme algoritmalarını implement et. (Tamamlandı)
10. Test et ve geliştir: Hareketi test et, AI kararlarını geliştir, seviye tasarımı ekle. (Tamamlandı)
11. Harita tasarımını güncelle: Araçları harflerle göster, grafik değil. (Tamamlandı)
12. Oyun başlangıç sırasını doğrula: Harita renklerle üretilir, oyuncu tuzaklar koyar, oyun başlar, sürü girer, sistemler çalışır. (Tamamlandı)

**İlgili Dosyalar**
- `main.py` — Ana oyun döngüsü ve motor.
- `ayarlar.py` — Sabitler, renkler, emojiler.
- `harita_yoneticisi.py` — Harita OOP sınıfları, yükleme.
- `suru_yoneticisi.py` — Sürü sınıfları, hareket matematiği.

**Doğrulama**
1. Haritayı .txt'den yükle ve ekranda göster. (Tamamlandı)
2. Sürüyü yarat ve zincirleme hareket ettir. (Tamamlandı)
3. Fare ile araç yerleştir ve etkilerini test et. (Tamamlandı)
4. AI kararlarını test et, öğrenmeyi doğrula. (Tamamlandı)
5. Kazanma/kaybetme koşullarını test et. (Tamamlandı)
6. Araçları harflerle göster. (Tamamlandı)
7. Oyun başlangıç sırasını test et. (Tamamlandı)

**Kararlar**
- Tema: Evrimsel Laboratuvar / Sentetik Test Odası.
- Kazanma: %90 ölüm veya sahte kapıya yönlendirme.
- Kaybetme: %10'dan fazla doğru kapıya ulaşma.
- Sürü evrimi: %30 hayatta kalma ile deneyim kazanma.
- Kod dili: Python + Pygame.
- Görsel: Text-mode, emoji tabanlı, araçlar harf.

**Gelecek Adımlar**
1. AI derinliğini artır: Daha karmaşık karar ağacı, kolektif zeka. (Tamamlandı)
2. Seviye editörü ekle: Harita oluşturma aracı. (Tamamlandı)
3. Ses efektleri ve müzik: Atmosfer güçlendirme. (Tamamlandı)
4. Araç gösterimini harflere çevir. (Tamamlandı)
5. Oyun akışını doğrula. (Tamamlandı)

## Ek Plan Güncellemesi (Append-Only) - 21 Mart 2026

Bu bölüm, .copilot belgeleri (istekler/kurallar/bilgiler/programcı el kitabı) ile gerçek kod arasındaki fark analizi sonrası eklenmiştir.

### Belge-Kod Tutarlılık Denetimi
1. Rastgele doğal ortam üretimi mevcut. (Yapıldı)
2. 5 katmanlı harita yapısı mevcut. (Yapıldı)
3. Sahte Yol aracı mevcut. (Yapıldı)
4. Greedy tabanlı yaklaşık yol bulma mevcut. (Yapıldı)
5. Düzenleme modunda sol tık sürükleyerek yerleştirme ve sağ tık kaldırma mevcut. (Yapıldı)
6. Araçların harf ile gösterimi mevcut (M, A, B, F, C, S, T, G, K, Y). (Yapıldı)
7. Düzenleme modunda rastgele üretilen doğal harita korunmuyor; tüm katmanlar sonradan ZeminDuz ile eziliyor. (Yapılmadı)(once zemin duz calissin, sonra diger zemin ozelliklerini kontrollu sekilde rastgele ama mantikli ve dogaya uygun bir tasarimi ile uretilsin.)
8. Etki alanı görselleştirmesi ve araç etkileri ±1 düzeyinde; 5 katmanı kapsayan hedefe göre güncellenmemiş. (Yapılmadı)
9. Araç sayıları, toplam etki alanının haritanın %55'ini kapsaması hedefiyle uyumlu hesaplanmamış. (Yapılmadı)
10. Giriş ve çıkış katmanları tam rastgele olsa da farklı katman garantisi yok. (Yapılmadı)
11. Her katmanda yol garantisi yok; yalnız giriş/çıkış katmanlarında yol çizimi var. (Yapılmadı)
12. Su/deniz derinlik dağılımı kıyı-orta-çok derin morfolojiye göre değil, tekil rastgele atanıyor. (Yapılmadı)
13. Alt bilgi satırı rengi beyaza alınmış olsa da kalın font zorunluluğu uygulanmamış. (Kısmi)
14. Oyun başladıktan sonra oyuncunun tüm araçları seçip yeniden kurma/kaldırma akışı tam değil; ana döngüde sadece Mancinik yerleştirme var. (Yapılmadı)
15. Belgelerdeki bazı "tamamlandı" iddiaları kodla uyuşmuyor; istekler.md eksik kapsamlı. (Yapılmadı)

### Yeni Planlar (Kullanıcı Son Talebine Göre)
1. Plan/istek/bilgiler belgeleri ile kod arasındaki farkları resmi izleme listesi olarak bu planda tut. (Başladı)
2. Düzenleme modunda doğal harita ezme adımını kaldır; katmanları üretilen doğal doku ile başlat. (Yapılacak)
3. Etki alanını 5 katman düşüncesine göre yeniden tasarla; kapsam hesabını harita parsel toplamına göre formülle doğrula. (Yapılacak)
4. Araç adetlerini, toplam etkin kapsama oranı hedefi %55 olacak şekilde yeniden hesapla ve sabitlere bağla. (Yapılacak)
5. Giriş ve çıkışın farklı katmanlarda olmasını zorunlu kıl; giriş/çıkış konumları tam rastgele kalsın. (Yapılacak)
6. Her katman için en az bir yürünebilir rota üretimini garanti eden yol üretim adımı ekle. (Yapılacak)
7. Su derinlik modelini kıyıdan merkeze artan derinlik ve renk geçişi ile üret. (Yapılacak)
8. Yüzey türlerinin hareket etkilerini (özellikle sık orman ve derin su) dengeleyip belgeye işle. (Yapılacak)
9. Oyun başladıktan sonra da araç seçimi, kaldırma ve tekrar kullanma akışını tek bir tutarlı kontrol şemasına bağla. (Yapılacak)
10. Alt bilgi metnini açık gri/beyaz ve kalın font ile tüm çözünürlüklerde okunur hale getir. (Yapılacak)
11. Giriş oku (kalın beyaz, içeri bakan) ve çıkış oku (koyu yeşil, dışarı bakan) görünürlüğünü katman bazında doğrula. (Yapılacak)
12. Belgelerdeki (istekler/programcı el kitabı/README/değişiklikler) durumları gerçek uygulama seviyesine göre yeniden senkronize et. (Yapılacak)

### Not
- Bu güncelleme append-only olarak eklenmiştir; önceki plan maddeleri değiştirilmemiştir.

## Ek Uygulama Durumu (Append-Only) - 21 Mart 2026

Bu bölümde "Yeni Planlar (Kullanıcı Son Talebine Göre)" maddelerinin uygulama durumu işaretlenmiştir.

1. Plan/istek/bilgiler belgeleri ile kod farklarının izlenmesi: plan içinde tutuluyor. (Tamamlandı)
2. Düzenleme modunda doğal harita ezme adımının kaldırılması: ZeminDuz ile toplu ezme kaldırıldı. (Tamamlandı)
3. Etki alanı 5 katman düşüncesiyle güncellendi: ±2 (5x5x5) uygulandı. (Tamamlandı)
4. Araç adetleri ve %55 kapsama hedefi: ayarlara hedef oran ve nominal etki hesabı eklendi, adetler güncellendi. (Tamamlandı)
5. Giriş-çıkış farklı katman zorunluluğu: while kontrolü ile sağlandı. (Tamamlandı)
6. Her katmanda en az bir yürünebilir yol: katman başına yatay yol garanti edildi. (Tamamlandı)
7. Su derinlik modeli: kenardan merkeze artan derinlik yaklaşımı eklendi. (Tamamlandı)
8. Yüzey etkilerinin dengeleme ayarı: temel etkiler var, ileri dengeleme/test kalemi devam ediyor. (Kısmi)
9. Oyun başladıktan sonra araç seçimi/kaldırma/tekrar kullanım: ana oyun döngüsüne eklendi. (Tamamlandı)
10. Alt bilgi metninin okunurluğu: açık gri + kalın font uygulandı. (Tamamlandı)
11. Giriş/çıkış oku görünürlüğü: düzenleme modunda katman bazlı gösterim korunup doğrulandı. (Tamamlandı)
12. Belgelerin gerçek uygulama ile senkronu: Kurallar ve plan güncellendi; diğer belgeler bir sonraki döngüde tamamlanacak. (Kısmi)

## Ek Uygulama Durumu 2 (Append-Only) - 21 Mart 2026

1. Belgelerin gerçek uygulama ile senkronu tamamlandı:
	- `.copilot/istekler.md` güncellendi.
	- `.copilot/programcı el kitabı.md` güncellendi.
	- `README.md` güncellendi.
	- `değişiklikler.md` güncellendi.
	(Tamamlandı)

## Plan Duzeltme ve Tamamlama Kaydi (Append-Only) - 21 Mart 2026

Bu bolum, onceki satirlardaki durum celiskilerini duzeltmek ve planin guncel net durumunu vermek icin eklendi.

### Durum Duzeltmeleri
1. "Belge-Kod Tutarlilik Denetimi" altindaki 7, 8, 9, 10, 11, 12, 13, 14, 15 maddeleri sonraki uygulama bolumlerinde ilerletildigi icin eski "Yapilmadi/Kismi" kayitlari tarihsel kayit olarak kalir; guncel durum asagidaki gibidir.
2. Guncel durum:
	- Madde 7: Tamamlandi
	- Madde 8: Tamamlandi
	- Madde 9: Tamamlandi
	- Madde 10: Tamamlandi
	- Madde 11: Tamamlandi
	- Madde 12: Tamamlandi
	- Madde 13: Tamamlandi
	- Madde 14: Tamamlandi
	- Madde 15: Tamamlandi
3. Acik kalan teknik kalem: yuzey etkilerinin ileri dengeleme ve oyun ici test tuning calismasi. (Devam ediyor)

### Operasyonel Zorunluluklar (Yeni)
1. Her onemli degisiklikte once yerel yedek alinacak (backup branch/tag veya yedek kopya), sonra uygulama yapilacak. (Zorunlu)
2. Degisiklik tamamlandiginda gerekli goruldugunde yerel git commit yapilacak. (Zorunlu)
3. Onemli adimlarda uzak depoya push yapilacak. (Zorunlu)
4. Backup alinmadan riskli refactor veya cok dosyali degisiklik yapilmayacak. (Zorunlu)

### Plan Hazirlik Kontrolu
1. Ana plan maddeleri: Hazir
2. Uygulanan yeni planlar: Buyuk oranda tamam
3. Kalan eksik: ileri dengeleme/tuning ve genis oyun testi raporu
4. Sonuc: Plan kullanima hazir, acik maddeler net sekilde isaretli