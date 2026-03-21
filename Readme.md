# TersLemm
Bu oyun, bir sahaya insanın yapay zekaya karşı tuzaklar hazırlayarak düşmanı engellemek üzerine kurulmuştur.

## Tuzaklar ve İşlevleri

Oyunda kullanılan tuzaklar ve ne işe yaradıkları:

- **Mancınık**: Yakındaki ajanları fırlatır. Ajanların yönünü değiştirir ve hızını artırır. Korku duygusunu yükseltir.
- **Sendeletme Taşı**: Ajanları sendeletir. Yönünü değiştirir ve hızını azaltır. Şüphe duygusunu yükseltir.
- **Gizli Çukur**: Ajanları öldürür. Üzerine basan ajanı anında öldürür.
- **Kıyma Makinesi**: Ajanları öldürür. Üzerine basan ajanı anında öldürür.
- **Yönlendirici**: Ajanların yönünü değiştirir. Belirli bir yöne yönlendirir, örneğin sağa.
- **Ayna**: Ajanların yönünü ters çevirir. Korku duygusunu yükseltir.
- **Bariyer**: Engel koyar, ajanları yavaşlatır. Şüphe duygusunu yükseltir.
- **Ateş**: Ajanları yakar, hasar verir ve hızlandırır. Korku duygusunu yükseltir.

## Kurulum ve Çalıştırma

1. Python 3.12+ kurulu olduğundan emin olun.
2. Gerekli paketleri yükleyin: `pip install pygame`
3. Oyunu çalıştırın: `python main.py`

Oyun düzenleme modu ile başlar. Haritayı ve tuzakları düzenleyin, sonra ESC ile oyunu başlatın.

**Düzenleme Modu Kontrolleri:**
- Fare sol tıklama: Araç yerleştir
- 1-5: Araç seç (1: Mancınık, 2: Ayna, 3: Bariyer, 4: Ateş, 5: Çıkış Oku)
- Yukarı/Aşağı ok: Katman değiştir
- S: Kaydet
- ESC: Oyunu başlat

## Özellikler

- AI kontrollü sürü ajanları (Lemler: 50 adet, yavaş hareket)
- Duygu matrisi ve öğrenme sistemi
- Çok katmanlı harita sistemi
- Gerçek zamanlı tuzak yerleştirme (sınırlı sayılarda)
- Ses efektleri ve arka plan müziği (.sid uzantılı müzikler için .wav/.mp3'ye dönüştürün)

## Araç Sayıları

- **Mancınık**: 5 adet
- **Ayna**: 5 adet
- **Bariyer**: 10 adet
- **Ateş**: 5 adet
- **Çıkış Oku**: 1 adet (kenarlarda yerleştirilir, oyun başlayınca kapıya dönüşür)

## Ses Dosyaları

sesler/ klasörüne aşağıdaki dosyaları ekleyin:
- arka_plan.sid (veya .wav/.mp3): Arka plan müziği
- arac_yerlestir.wav: Araç yerleştirme sesi
- ajan_ol.wav: Ajan ölme sesi
