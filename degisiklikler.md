
## [Tarih: 22 Mart 2026 - Faz 1 ve Faz 2 Uygulamasi]

### harita_yoneticisi.py
- _omurga_rota_segment() yardimci metod eklendi: L-sekilli iki nokta arasinin (x,y,z) listesini dondurur.
- _yol_oyu() metod eklendi: Iki nokta arasini YOL dokusuyla L-seklinde kaplar.
- uc_boyutlu_yol_ve_merdiven_yarat(): Harita olusumunda giristen cikisa tum katmanlari YOL dokusuyla baglayan omurga yol cizer; omurga_rota listesini hesaplar.
- HaritaYoneticisi init'e self.omurga_rota = [] eklendi.

### suru_yoneticisi.py
- yol_bul(): Omurga_rota tabanli yol izleme birincil; A* yedek; greedy en son yedek. Sure: 0.1ms.
- _greedy_yedek() eklendi: Eski greedy kodu ayri metod olarak korundu.
- lider_yapay_zeka(): Faz 2 - Rol tabanli: korku/suphe override → yol takibi birincil → kesif yuruyusu ikincil.
- zinciri_kopar(): Yeni lider terfi etince aninda yol_bul() cagrisi eklendi.
- SURU_BASLANGIC_BEKLEME_TIK sabit ismi duzeltildi (_TEMEL suffix).

### .copilot/plan.md
- Faz 2 basligi ve ilk iki madde mantik hatasina gore duzeltildi: yol takibi tum ajanlar icin degil, yalnizca liderler icin birincil davranistir.

### Dogrulama
- Tum py dosyalari: syntax temiz (py_compile).
- omurga_rota: tum katmanlari kapsayan 50-100 adimlik yol.
- yol_bul() suresi: 0.1ms. Hedefe mesafe: 0 (tam cikisa ulasiyor).
- Oyun 4 saniye sorunsuz calisti.
