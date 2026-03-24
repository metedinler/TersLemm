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

## Gemini 91b14b296dd1 Entegrasyon Yol Haritasi (Append-Only) - 22 Mart 2026

Bu bolum, Gemini baglantisindaki tum gelistirme fikirlerinin mevcut kod tabani ile karsilastirilmasi sonrasinda eklenmistir. Bu planin amaci mevcut sistemi silmeden, mevcut davranislari koruyarak yeni katmanlari asamali sekilde entegre etmektir. Onceki ve simdiki ve bundan sonraki baglantilarin tum icerigi bilgiler.md dosyasinda bulunur.

### Gercek Kod Durumu Tespiti
1. Mevcut sistemde temel duygu matrisi var: korku, merak, suphe. (Tamamlandi)
2. Mevcut sistemde linked-list suru zinciri ve lider mantigi var. (Tamamlandi)
3. Mevcut sistemde greedy tabanli yol bulma var. (Tamamlandi)
4. Mevcut sistemde 10 araclik oyuncu sistemi var. (Tamamlandi)
5. Mevcut sistemde merdiven dokulari icin katman gecis kurali var ancak harita olusumunda giristen cikisa tum katmanlari baglayan aktif 3B rota sistemi yok. (Yapilmadi)
6. Mevcut sistemde anlamsal ust akil / kavramsal motor yok. (Yapilmadi)
7. Mevcut sistemde genis hormonal katman (dopamin, adrenalin, oksitosin, endorfin, serotonin, husran, kortizol) yok. (Yapilmadi)
8. Mevcut sistemde genetik hafiza / evrimsel secim / benzersiz genom kaydi yok. (Yapilmadi)
9. Mevcut sistemde gazi modu, liderlik darbesi ve kacanlari toplama davranisi yok. (Yapilmadi)
10. Mevcut sistemde ajan ustu emoji balonlari ve zihinsel durum gosterimi yok. (Yapilmadi)
11. Mevcut sistemde tasarimda gecen 20+ araclik psiko-biyolojik genisleme yok. (Yapilmadi)

### Uygulama Prensipleri
1. Mevcut siniflar korunacak; yeni sistemler ek siniflar ve yeni metodlarla entegre edilecek. (Basladi)
2. Var olan 10 arac kaldirilmayacak; yeni araclar ikinci fazdan sonra eklenecek. (Yapilacak)
3. Lider ajanlar icin yol takibi birincil davranis; takipci ajanlar icin lider izleme birincil davranis. Suru parcalandiginda yeni lider statusune gecen ajan otomatik olarak yol takibi moduna gecer. Hormonal sistem parcalanmayi kolaylastirarak yeni yol izleme modlarinin ortaya cikmasi saglaniyor — bu yuzden yol takibi tum ajanlar icin degil, yalnizca liderler ve yeni lider haline gelen ajanlar icin birincil davranistir. (Duzeltildi - 22 Mart 2026)
4. Harita, oyuncu ve suru etkilesimi siniflar arasi metod cagrilari ve veri nesneleri ile kurulacak. (Yapilacak)
5. Her buyuk faz ayri test ve belge guncellemesi ile dogrulanacak. (Yapilacak)

### Faz 1: Harita Omurgasi ve 3B Yol Surekliligi
0. Giris ve Cikis oklari ile giric ve cikis kapilari haritaya konacak. ayrica katmanlarin birbirine baglanmasi icin asonsor yada merdiven ile olacak. merdiver her katmanda olacak, asansor rastgele her katmanda ya bir yada hic olmayacak. asansor, merdiven, giris, cikis kapilarinin yerleri her oyun basinda rastgele olusturulacak.
1. Harita olusurken giristen cikisa kadar tum katmanlari baglayan kesintisiz ana yol algoritmasi ekle. (Yapilacak)
2. Ara katman hedef noktalarina merdiven baglanti noktalarini zorunlu kil. (Yapilacak)
3. Son katmanda ana cikisa ulasan yolun kesinligini dogrula. (Yapilacak)
4. Yol disi dogal doku dagilimini ana yolu bozmayacak sekilde koru. (Yapilacak)
5. Katman gecisinin sadece merdiven kullanarak yapildigini kod ve test ile kanitla. (Yapilacak)

### Faz 2: Rol Tabanli Suru Davranisi (Lider/Takipci/Kopan)
--- NOT (22 Mart 2026 duzeltmesi): Bu faz daha once "Yol Takibi Merkezli" olarak tanimlanmisti; ancak bu tanimlama tum ajanlar icin yol takibini ust sirada gosterdigi icin mantik hatasidir. Asagidaki maddeler duzeltilmis sekliyle yeniden yazilmistir. ---
1. Lider ajanlar icin yol takibini birincil hamle yap. Takipci ajanlar icin lider izlemeyi birincil hamle olarak koru; takipci ajanlarda yol takibi devreye girmez. (Yapilacak)
2. Suru parcalandiginda yeni lider statusune gecen ajani otomatik olarak yol takibi moduna al. Aktif suru zincir baglantisi kopugunda lider izleme kaldirilir, yol takibi baslar. (Yapilacak)
3. Yoldan sapma kararlarini duygu ve nesne etkisi uzerinden kurgula. (Yapilacak)
4. Engel, kenar ve tuzak durumlarinda yol yeniden planlama akisini bozmadan koru. (Yapilacak)

### Faz 3: Anlamsal Ust Akil ve Kavramsal Motor
1. Haritadaki arazi ve aletleri IYI, KOTU, CIRKIN, KULLANILABILIR, KULLANILAMAZ gibi kavramsal etiketlerle degerlendiren ayri bir motor tasarla. (Yapilacak)
2. Bu kavramsal motoru sayisal duygu matrisinin ustune ek yorum katmani olarak kur. (Yapilacak)
3. Ajanin yakin nesne algisini sadece mesafe degil, anlamsal deger ile de beyne girdi yapan yapıya donustur. (Yapilacak)
4. Evrimsel hafiza icin bu anlamsal etiketleri ileride aktarilabilir veri yapisina bagla. (Yapilacak)

### Faz 4: Genisletilmis Kalp-Beyin Katmani
1. BiyolojikSistem veya esit bir kalp sinifi ekle: dopamin, adrenalin, oksitosin, endorfin, serotonin, husran, kortizol. (Yapilacak)
2. Mevcut duygular ile yeni hormon katmanini uyumlu hale getir; eski duygulari tamamen kaldirma. (Yapilacak)
3. SinirAgi veya esit karar motoru icin giris setini kademeli buyut; once sabit karar matrisini kur, sonra hafif sinir agi katmanina gec. (Yapilacak)
4. Beceri etkilerini hormon filtresi ile birlestir; ogrenilmis sogukkanlilik mantigini ekle. (Yapilacak)

### Faz 5: Oyuncu Aletleri ve Duygusal Etki Alani
1. Mevcut 10 arac icin duygu ve hormon etkisi tablosu olustur. (Yapilacak)
2. Alet etkilerini yalnizca fiziksel degil, etki alaninda psikolojik etki uretecek sekilde genislet. (Yapilacak)
3. Tasarimdaki yeni psiko-biyolojik araclari ikinci dalga olarak ekle; ilk 10 araci bozmadan ilerle. (Yapilacak)
4. Arac etkilerinin haritadaki nesne anlamina da veri beslemesini sagla. (Yapilacak)
5. mevcut 10 ve yeni 10 arac suru uzerine etkileri net sekilde olusturulacak, hepsinin suruyu kparma, duygu degerleri olusacak bir birleri ile etkilesimi hesaplanacak.
### Faz 6: Gazi Modu ve Suru Ic Dinamigi
1. Hasar, engel asma ve krizden sag cikma uzerinden gazi puani biriktiren sistem ekle. (Yapilacak)
2. Gazi ajanlarin lider degilken de gerekirse suruyu devralma davranisini tanimla. (Yapilacak)
3. Kacan ajanlari toplama, parca suruleri birlestirme ve fedakarlik omru mantigini ekle. (Yapilacak)
4. Gazi varliginin ogrenme cezasini ve gecici karakterini dengele. (Yapilacak)

### Faz 7: Evrimsel Hafiza ve Dosya Tabanli Miras
1. Baslangic genomu ve egitimli genom arsivi dosya yapisini tanimla. (Yapilacak)
2. Oyun bir kez oynandiktan sonra secilim baslat; ilk oyun tabula rasa olsun. (Yapilacak)
3. Reset durumunda baslangic genomuna don, ama egitimli veri benzersiz isimle arsivlensin. (Yapilacak)
4. En iyi ajan secim kriterini yalnizca can ile degil: hayatta kalma, hedefe yakinlik, beceri, anlamsal dogruluk ve suruye katkı ile tanimla. (Yapilacak)

### Faz 8: Gorsel Geri Bildirim ve Oyuncu Okunabilirligi
1. Ajan ustu emoji balonlari ekle. (Yapilacak)
2. Baskin hormon, mod ve anlamsal karar durumlarini gorsel olarak ayriştir. (Yapilacak)
3. Oyuncu arayuzunde daha buyuk arac havuzu icin kategori veya hizli secim paneli planla. (Yapilacak)

### Faz 9: Dengeleme ve Dogrulama
1. Her faz sonunda terminalden calistirma ve oyun ici dogrulama yap. (Yapilacak)
2. Konsol spamlarini log dosyasina tasi. (Yapilacak)
3. Harita-yol-katman-ai-arac etkilesimini kayit sisteminde izlenebilir hale getir. (Yapilacak)

### Bu Turun Sonucu
1. Bu turda yalnizca inceleme, fark analizi ve uygulama plani hazirlandi. (Tamamlandi)
2. Kod yazimi icin onerilen ilk uygulama fazi: Faz 1 + Faz 2. (Hazir)
## Faz Ilerleme Notu - 22 Mart 2026 (Aksam)
- Faz 1 baslandi ve ilk calisir surum uygulandi.
- Harita tarafinda 3B omurga yol ve omurga_rota listesi kodlandi.
- Faz 2 baslandi ve lider/takipci/kopan rol modeline gore lider AI davranisi guncellendi.
- Yeni lider terfisinde otomatik yol takibi aktif edildi.
- Faz 1/Faz 2 su an erken calisir prototip asamasinda; bir sonraki adim oyunda uzun sureli denge testi ve follower tarafi sapma kurallarinin detaylandirilmasi.

## Faz 2-3 Ilerleme Notu - 22 Mart 2026 (Gece)
- Faz 2 davranis cekirdegi genisletildi: takipci lider izleme birincil; duygu + nesne baskisi altinda kontrollu kopma tetikleniyor.
- Kopan ajanlar yeni lider oldugunda otomatik yol takibi (omurga rota) aktif kalacak sekilde dogrulandi.
- Engel/tehlike semantigi lider yol kararina baglandi: KOTU/KULLANILAMAZ hedefte yeniden planlama ve sapma davranisi calisiyor.
- Faz 3 baslatildi: KavramsalMotor sinifi eklendi; parsel ve aletler IYI/KULLANILABILIR/CIRKIN/KOTU/KULLANILAMAZ etiketlerine cevriliyor.
- Kavramsal etiketler lider ve takipci duygularina yansitiliyor (korku/suphe/merak guncellemesi).
- Faz 3 sonraki adim: kavramsal etiketleri evrimsel hafiza veri formatina baglayacak kalici kayit katmani.

## Faz 3 Tamamlama ve Faz 4 Otomatik Gecis - 22 Mart 2026 (Gece)
- Faz 3 maddeleri uygulandi: KavramsalMotor aktif; parsel/alet etiketleme karar dongusune baglandi.
- Ajan semantik iz kaydi ve aktarilabilir_semantik_hafiza veri yapisi eklendi (JSON-benzeri aktarim formati).
- Lider ve takipcide kavramsal etiketlerin duygu etkisi ve riskte yoldan sapma davranisi dogrulandi.
- Plan geregi otomatik gecisle Faz 4 baslatildi: BiyolojikSistem eklendi (dopamin, adrenalin, oksitosin, endorfin, serotonin, husran, kortizol).
- Hormonlar cevre uyaranina gore guncellenip duygulara yansitiliyor; ajan modu (TEHDIT/KESIF/DENGELI) karar katmanina baglandi.
- Faz 4 ilerletildi: BiyolojikSistem.karar_matrisi ile hormon+duygu birlesik karar puanlari eklendi ve lider kararina baglandi.
- Faz 4 ilerletildi: ogrenme miktari hormon filtresine baglandi (dopamin/serotonin artisi, kortizol/husran azalimi).
- Faz 5 ilerletildi: mevcut 10 arac için psikobiyolojik etki tablosu eklendi, araclarin birlesik etkisi icin etkilesim matrisi calisir hale getirildi.
- Faz 6 baslatildi: gazi puani birikimi, gecici gazi mod, liderlik devri ve kacan ajan toplama davranislari eklendi.
- Faz 7 baslatildi: dosya tabanli evrimsel_hafiza katmani eklendi; en iyi ajan ozeti periyodik JSON arsive yaziliyor.
- Faz 7 ilerletildi: tabula rasa baslangic_genom/genom_v1.json otomatik olusturma ve yukleme mekanizmasi eklendi.

## Faz 7-8-9 Tamamlama Notu (22 Mart 2026)
- Faz 7 madde 2: ilk_oyun_mu / ilk_oyun_bitti_isaretle flag mekanizmasi eklendi; arsive_yaz sonunda otomatik isaretleniyor.
- Faz 7 madde 3: reset_ve_arsivle metodu eklendi; egitimli arsiv dosyalari benzersiz zaman damgali alt klasore tasiniyor, flag sifirlaniyor.
- Faz 7 madde 2 (secilim): en_iyi_arsivi_yukle metodu eklendi; ikinci oyunda lider ajanin beceri ve hormonlari arsiv verisinden seed ediliyor.
- Faz 7: Tamam (tum maddeler uygulandı).
- Faz 8 madde 1: render metodunda ajanlarin ustune emoji balon gosterimi (GAZI sembol eklendi).
- Faz 8 madde 2: mod renk arkaplan (TEHDIT=koyu kirmizi, KESIF=koyu mavi, DENGELI=koyu yesil, GAZI=altin), kavramsal_durum renk kodlu kucuk nokta (sag ust kose), gazi altin cerceve. Tamam.
- Faz 8 madde 3: Oyun ici durum barinda tum 10 aracin kisayol/miktar ozeti mini satiri eklendi. Tamam.
- Faz 8: Tamam (tum maddeler uygulandı).
- Faz 9 madde 2: SuruAjani.beceri_ogren ve ol metodlarindaki tek-satir print spam kaldirildi; zinciri_kopar print'leri kaldirildi.
- Faz 9 madde 3: anlik_durum_yaz log kaydina hormonlar, kavramsal_durum, mod, gazi, yol_index alanlari eklendi. Tamam.
- Faz 9: Maddeler 2 ve 3 tamamlandi; madde 1 (faz sonu terminal test) surekli yapiliyor.

## 23 Mart 2026 Dokumantasyon ve Paylasim Paketi (Append-Only)

Bu bolum, Faz 1-9 sonrasinda kodun modulasyona alinmasi ve dis paylasim icin gerekli dosyalarin netlestirilmesi amaciyla eklenmistir.

### Yapilanlar
1. Oyun akisinin modullere bolunmesi: main.py icindeki yardimci siniflar oyun_bilesenleri.py dosyasina tasindi. (Tamamlandi)
2. Harita kaliciligi: HaritaYoneticisi icine haritayi_kaydet, dosyadan_yukle ve kayitli_haritalari_listele eklendi. (Tamamlandi)
3. Baslangicta kayitli harita secimi: Baslangic menusune kayitli harita secim modu eklendi. (Tamamlandi)
4. Oyun basinda otomatik harita kaydi: Duzenleme cikisinda aktif harita haritalar klasorune yaziliyor. (Tamamlandi)
5. Ajan durum penceresi acilis davranisi: Otomatik acik/odakli baslama kaldirildi, F2 ile ac-kapat eklendi. (Tamamlandi)
6. Ajan durum penceresi yerlesimi: Dar genislik + alt alta hizali duygu/hormon gosterimi eklendi. (Tamamlandi)
7. Alt durum cubugu okunabilirligi: Iki satir metin gorunecek yukseklik ayari yapildi. (Tamamlandi)
8. Dagitim kapsami netlestirme: Oyun icin gerekli moduller ve evrimsel_hafiza dosyalari repoya eklendi. (Tamamlandi)

### Bu Tur Belge Senkronu
1. Programci el kitabi: Faz 1-9 ozeti ve git sonrasi degisiklikler eklendi. (Tamamlandi)
2. Istekler dosyasi: bu tur istek kaydi ve uygulama notu eklendi. (Tamamlandi)
3. Bilgiler dosyasi: faz/sonrasi teknik ozet duzenlendi. (Tamamlandi)
