import cv2
import os

# Klasör Yolları
img_dir = r"C:\Users\enesk\Desktop\halisahaplayer\halisahaplayer\images\test"
lbl_dir = r"C:\Users\enesk\Desktop\halisahaplayer\halisahaplayer\labels\test"

# Desteklenen resim formatları
valid_exts = ('.jpg', '.jpeg', '.png', '.bmp', '.webp')

# Resim dosyalarını listele ve sırala
images = sorted([f for f in os.listdir(img_dir) if f.lower().endswith(valid_exts)])

if not images:
    print("HATA: Belirtilen klasörde hiç resim bulunamadı!")
    exit()

current_idx = 0
total_images = len(images)

print("=== YÖNERGELER ===")
print("[D] veya [Sağ Yön Tuşu] : Sonraki Fotoğraf")
print("[A] veya [Sol Yön Tuşu] : Önceki Fotoğraf")
print("[Q] veya [ESC]          : Çıkış\n")

while True:
    # Sınırları kontrol et
    if current_idx < 0:
        current_idx = 0
    elif current_idx >= total_images:
        current_idx = total_images - 1

    img_name = images[current_idx]
    base_name, _ = os.path.splitext(img_name)
    txt_name = f"{base_name}.txt"
    
    img_path = os.path.join(img_dir, img_name)
    txt_path = os.path.join(lbl_dir, txt_name)
    
    # Resmi Oku
    img = cv2.imread(img_path)
    if img is None:
        print(f"Resim okunamadı: {img_path}")
        current_idx += 1
        continue
        
    h, w, _ = img.shape
    
    # Etiket dosyası varsa oku ve kutuları çiz
    if os.path.exists(txt_path):
        with open(txt_path, "r") as f:
            lines = f.readlines()
            
        for line in lines:
            parts = line.strip().split()
            if len(parts) >= 5:
                class_id = int(parts[0])
                x_center = float(parts[1])
                y_center = float(parts[2])
                width = float(parts[3])
                height = float(parts[4])
                
                # YOLO formatını (0-1 arası) piksel koordinatlarına çevir
                x = int(x_center * w)
                y = int(y_center * h)
                box_w = int(width * w)
                box_h = int(height * h)
                
                # Dikdörtgenin sol üst ve sağ alt köşelerini hesapla
                x1 = int(x - box_w / 2)
                y1 = int(y - box_h / 2)
                x2 = int(x + box_w / 2)
                y2 = int(y + box_h / 2)
                
                # Kutu çizimi (Yeşil renk, 2 piksel kalınlık)
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                
                # Sınıf ID'sini kutunun üzerine yazdır
                cv2.putText(img, f"ID: {class_id}", (x1, y1 - 10), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    else:
        # Etiketi olmayan resimler için uyarı yazısı
        cv2.putText(img, "ETIKET BULUNAMADI", (20, 40), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    # Resmi ekranda göster (Pencere adına indeks bilgisini de ekle)
    window_title = f"Goruntuleyici - {img_name} ({current_idx + 1}/{total_images})"
    cv2.imshow("YOLO Label Viewer", img)
    cv2.setWindowTitle("YOLO Label Viewer", window_title)
    
    # Klavye tuşlarını dinle
    key = cv2.waitKey(0) & 0xFF
    
    if key == ord('d') or key == ord('D') or key == 83:  # D tuşu veya Sağ Yön
        current_idx += 1
    elif key == ord('a') or key == ord('A') or key == 81:  # A tuşu veya Sol Yön
        current_idx -= 1
    elif key == ord('q') or key == ord('Q') or key == 27:  # Q veya ESC
        break

cv2.destroyAllWindows()