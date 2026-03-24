# TersLemm
Bu oyun, bir sahaya insanın yapay zekaya karşı tuzaklar hazırlayarak düşmanı engellemek üzerine kurulmuştur.

## Tuzaklar ve İşlevleri

Oyunda kullanılan tuzaklar ve ne işe yaradıkları (harita üzerinde harf olarak gösterilir):

- **M: Mancınık**: Yakındaki ajanları fırlatır. Ajanların yönünü değiştirir ve hızını artırır. Korku duygusunu yükseltir.
- **A: Ayna**: Ajanların yönünü ters çevirir. Korku duygusunu yükseltir.
- **B: Bariyer**: Engel koyar, ajanları yavaşlatır. Şüphe duygusunu yükseltir.
- **F: Ateş**: Ajanları yakar, hasar verir ve hızlandırır. Korku duygusunu yükseltir.
- **C: Çıkış Oku**: Çıkış işaretler. Oyun başlayınca kapıya dönüşür.
- **S: Sahte Yol**: Lemler yolları tercih eder.
- **T: Sendeletme Taşı**: Ajanları sendeletir. Yönünü değiştirir ve hızını azaltır. Şüphe duygusunu yükseltir.
- **G: Gizli Çukur**: Ajanları öldürür. Üzerine basan ajanı anında öldürür.
- **K: Kıyma Makinesi**: Ajanları öldürür. Üzerine basan ajanı anında öldürür.
- **Y: Yönlendirici**: Ajanların yönünü değiştirir. Belirli bir yöne yönlendirir, örneğin sağa.

## Kurulum ve Çalıştırma

1. Python 3.12+ kurulu olduğundan emin olun.
2. Gerekli paketleri yükleyin: `pip install pygame`
3. Oyunu çalıştırın: `python main.py`

### Oyun Başlatma Kodu

Oyunu başlatmak için terminalde şu komutu çalıştırın:

```bash
cd ters_lemmings
python main.py
```

## Oyun Akışı

1. Harita yer şekilleri ile renkli olarak rastgele üretilir.
2. Oyuncu düzenleme modunda tuzakları fare ile yerleştirir.
3. Oyuncu ESC ile oyunu başlatır.
4. Sürü girişten girer, AI sistemleri çalışır (duygu, öğrenme, yol bulma).
5. Kazanma: %90 ölüm veya sahte çıkışa yönlendirme.
6. Kaybetme: %10'dan fazla doğru çıkışa ulaşma.

**Düzenleme Modu Kontrolleri:**
- Fare sol tıklama: Araç yerleştir
- Fare sağ tıklama: Araç kaldır
- 1-0: Araç seç (1: M, ..., 0: Y)
- Yukarı/Aşağı ok: Katman değiştir
- S: Kaydet
- ESC: Oyunu başlat

## Özellikler

- AI kontrollü sürü ajanları (Lemler: 50 adet, yavaş hareket - hız 0.5)
- Duygu matrisi ve öğrenme sistemi
- Çok katmanlı harita sistemi (5 katman, rastgele doğal ortamlar)
- Rastgele harita oluşturma (dağ, göl, deniz, orman, yollar, vb.)
- Gerçek zamanlı tuzak yerleştirme (sınırlı sayılarda, geniş etki alanı)
- Yol bulma algoritması (lemler hedefe doğru yol bulur)
- Ses efektleri ve arka plan müziği (.sid uzantılı müzikler için sidplayfp.exe)
- Düzenleme modu: Oyun başlamadan harita ve tuzakları düzenleme
- Renkli harita: Yer şekillerine göre renkler, su derinliği gradyanı
- Hareket cezaları: Orman ve diğer türlerde yavaşlama
- Çıkış sistemi: Rastgele katmanlarda giriş/çıkış, oku kapıya çevirme
- Sahte yollar aracı: Lemler yolları tercih eder

## Test Durumu ✅

- **Düzenleme Modu:** Çalışıyor, harita render ediliyor, araç yerleştirme hazır
- **Araç Limitleri:** Kodda uygulandı (Mancınık 20, Ayna 20, Bariyer 30, Ateş 20, Çıkış Oku 1, Sahte Yol 15)
- **Lem Sistemi:** 50 ajan, yavaş hız (0.5) ayarlandı
- **Çıkış Sistemi:** Rastgele katmanlarda, oku kapıya çevirme kodu eklendi
- **Ses:** SID müzik çalışıyor, basit ses efektleri üretiliyor
- **Harita:** Rastgele doğal ortamlar, yollar
- **Yol Bulma:** Lemler hedefe doğru yaklaşık yol buluyor
- **Sonraki:** Tam oyun döngüsü testi ve dengeler

## Araç Sayıları (Artırıldı)

- **Mancınık**: 20 adet
- **Ayna**: 20 adet
- **Bariyer**: 30 adet
- **Ateş**: 20 adet
- **Çıkış Oku**: 1 adet
- **Sahte Yol**: 15 adet

## Ses Dosyaları

sesler/ klasörüne aşağıdaki dosyaları ekleyin:
- arka_plan.sid (veya .wav/.mp3): Arka plan müziği
- arac_yerlestir.wav: Araç yerleştirme sesi
- ajan_ol.wav: Ajan ölme sesi

## 21 Mart 2026 Güncel Durum

- Doğru çalıştırma komutu (venv):
	- `cd c:\Users\mete\Zotero\lemm`
	- `.venv\Scripts\python.exe ters_lemmings/main.py`
- Harita artık düzenleme modunda ZeminDuz ile ezilmiyor; doğal katman üretimi korunuyor.
- Etki alanı görselleştirmesi ve araç etkisi ±2 (5x5x5) olarak güncellendi.
- Giriş ve çıkış farklı katman zorunluluğu eklendi.
- Her katmanda en az bir yürünebilir yol garanti edildi.
- Oyun başladıktan sonra da 1-0 ile araç seçimi, sol tık ile yerleştirme, sağ tık ile kaldırma ve tekrar kullanım aktif.
- Alt bilgi satırı açık gri ve kalın font ile okunur hale getirildi.

## 22 Mart 2026 Yol Haritası Özeti

Gemini tasarım bağlantısı incelendi ve mevcut oyun kodu ile karşılaştırıldı. Bu turda kod değil, uygulama sırası netleştirildi.

Planlanan ana fazlar:

1. Harita oluşturulurken girişten çıkışa tüm katmanları bağlayan kesintisiz ana yol ve merdiven sistemi.
2. Sürü davranışında lider takibinden önce yol takibinin merkez alınması.
3. Nesneleri iyi, kötü, çirkin, kullanılabilir gibi yorumlayacak anlamsal üst akıl katmanı.
4. Mevcut duygu yapısını bozmadan kalp-beyin-hormon katmanının genişletilmesi.
5. Oyuncu araçlarının fiziksel etkilerinin yanında duygusal etki alanlarının eklenmesi.
6. Gazi modu, kriz anında liderlik devri ve kaçan ajanları toplama davranışları.
7. Evrimsel hafıza, benzersiz genom arşivi ve reset sonrası başlangıç genomuna dönüş sistemi.
8. Ajan üstü emoji balonları ve oyuncu okunabilirliğini artıran geri bildirimler.
