## Plan: Ters Lemmings Oyun Geliştirme

Yeni nesil sistemik puzzle oyunu geliştirmek. Oyuncu tuzaklar kurar, AI sürü karar verir ve zincirleme takip eder. Çok katmanlı harita, duygu matrisi, öğrenme sistemi ile özgün bir deneyim.

**Adımlar**
1. Kod yapısını analiz et: Gemini konuşmasındaki Python sınıflarını incele, OOP mimarisini anla.
2. Proje yapısını oluştur: ters_lemmings klasörü, main.py, ayarlar.py, harita_yoneticisi.py, suru_yoneticisi.py dosyalarını oluştur.
3. Harita sistemini implement et: Çok boyutlu dizi, pasif nesneler, .txt'den yükleme.
4. Sürü ajanlarını implement et: SuruAjani sınıfı, duygular, beceriler, öğrenme.
5. Sürü yöneticisini implement et: Zincirleme hareket, lider AI, kopma mantığı.
6. Oyuncu araçlarını ekle: Mancınık, taş, çukur, kıyma makinesi, ayna, bariyer sınıfları, eskime formülleri.
7. Oyun döngüsünü tamamla: Güncelleme, render, kazanma/kaybetme koşulları. (Tamamlandı: OyunYoneticisi eklendi, harita çıkışları güncellendi.)
8. Araç etkileşimlerini implement et: Mancınık fırlatma, taş sendeletme, çukur düşürme kodlarını ekle. (Tamamlandı: etki_uygula() metotları eklendi, oyun döngüsüne entegre edildi.)
9. AI kararlarını geliştir: Duygu matrisi ve öğrenme algoritmalarını implement et. (Tamamlandı: Lider AI duygulara göre karar veriyor, öğrenme sistemi eklendi.)
10. Test et ve geliştir: Hareketi test et, AI kararlarını geliştir, seviye tasarımı ekle.

**İlgili Dosyalar**
- `main.py` — Ana oyun döngüsü ve motor.
- `ayarlar.py` — Sabitler, renkler, emojiler.
- `harita_yoneticisi.py` — Harita OOP sınıfları, yükleme.
- `suru_yoneticisi.py` — Sürü sınıfları, hareket matematiği.

**Doğrulama**
1. Haritayı .txt'den yükle ve ekranda göster.
2. Sürüyü yarat ve zincirleme hareket ettir.
3. Fare ile araç yerleştir ve etkilerini test et.
4. AI kararlarını test et, öğrenmeyi doğrula.
5. Kazanma/kaybetme koşullarını test et.

**Kararlar**
- Tema: Evrimsel Laboratuvar / Sentetik Test Odası.
- Kazanma: %90 ölüm veya sahte kapıya yönlendirme.
- Kaybetme: %10'dan fazla doğru kapıya ulaşma.
- Sürü evrimi: %30 hayatta kalma ile deneyim kazanma.
- Kod dili: Python + Pygame.
- Görsel: Text-mode, emoji tabanlı.

**Gelecek Adımlar**
1. AI derinliğini artır: Daha karmaşık karar ağacı, kolektif zeka. (Tamamlandı: Kolektif zeka eklendi.)
2. Seviye editörü ekle: Harita oluşturma aracı. (Tamamlandı: seviye_editörü.py eklendi.)
3. Ses efektleri ve müzik: Atmosfer güçlendirme. (Tamamlandı: Pygame mixer ile ses sistemi eklendi.)