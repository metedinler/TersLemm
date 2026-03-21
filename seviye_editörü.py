# seviye_editörü.py
# Basit harita düzenleme aracı

import os

def seviye_duzenle(dosya_yolu):
    """Harita dosyasını düzenlemeye izin verir."""
    if not os.path.exists(dosya_yolu):
        print(f"Dosya bulunamadı: {dosya_yolu}")
        return
    
    with open(dosya_yolu, 'r') as f:
        satirlar = f.readlines()
    
    print("Mevcut harita:")
    for i, satir in enumerate(satirlar):
        print(f"{i}: {satir.strip()}")
    
    while True:
        print("\nDüzenleme seçenekleri:")
        print("1. Satır değiştir")
        print("2. Karakter değiştir")
        print("3. Kaydet ve çık")
        secim = input("Seçiminiz: ")
        
        if secim == '1':
            satir_no = int(input("Satır numarası: "))
            yeni_satir = input("Yeni satır: ")
            if 0 <= satir_no < len(satirlar):
                satirlar[satir_no] = yeni_satir + '\n'
        elif secim == '2':
            satir_no = int(input("Satır numarası: "))
            sutun_no = int(input("Sütun numarası: "))
            yeni_karakter = input("Yeni karakter: ")
            if 0 <= satir_no < len(satirlar) and 0 <= sutun_no < len(satirlar[satir_no].strip()):
                satir_list = list(satirlar[satir_no])
                satir_list[sutun_no] = yeni_karakter
                satirlar[satir_no] = ''.join(satir_list)
        elif secim == '3':
            with open(dosya_yolu, 'w') as f:
                f.writelines(satirlar)
            print("Kaydedildi.")
            break
        else:
            print("Geçersiz seçim.")

if __name__ == "__main__":
    seviye_duzenle("haritalar/bolum_1_kat_0.txt")