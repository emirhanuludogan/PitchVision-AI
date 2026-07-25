import argparse
import glob
import os
import shutil
from ultralytics import YOLO


def auto_label(input_dir: str, output_dir: str, conf: float = 0.25, device: str = "cpu"):
    """YOLOv8 kullanarak futbol topu (class 32) için otomatik etiketleme yapar."""
    images_out = os.path.join(output_dir, "images")
    labels_out = os.path.join(output_dir, "labels")

    os.makedirs(images_out, exist_ok=True)
    os.makedirs(labels_out, exist_ok=True)

    print("🚀 YOLOv8x modeli yükleniyor...")
    model = YOLO("yolov8x.pt")

    # COCO Veri Seti: 32 = sports ball
    TARGET_CLASS = 32

    # Görselleri tara
    extensions = ("**/*.jpg", "**/*.png", "**/*.jpeg")
    image_files = []
    for ext in extensions:
        image_files.extend(glob.glob(os.path.join(input_dir, ext), recursive=True))

    print(f"📸 Toplam {len(image_files)} adet görsel taranıyor...")

    labeled_count = 0

    for img_path in image_files:
        filename = os.path.basename(img_path)
        txt_filename = os.path.splitext(filename)[0] + ".txt"

        results = model(img_path, conf=conf, device=device, verbose=False)[0]

        ball_boxes = []
        for box in results.boxes:
            cls_id = int(box.cls[0])

            if cls_id == TARGET_CLASS:
                x, y, w, h = box.xywhn[0].tolist()
                ball_boxes.append(f"0 {x:.6f} {y:.6f} {w:.6f} {h:.6f}\n")

        if ball_boxes:
            shutil.copy(img_path, os.path.join(images_out, filename))

            with open(os.path.join(labels_out, txt_filename), "w", encoding="utf-8") as f:
                f.writelines(ball_boxes)

            labeled_count += 1

    print("\n🎉 İşlem Tamamlandı!")
    print(f"✅ Toplam {len(image_files)} görselden {labeled_count} tanesinde FUTBOL TOPU tespit edildi.")

    # Model Eğitimi İçin Yapılandırma Dosyası (data.yaml)
    yaml_content = f"""path: {os.path.abspath(output_dir)}
train: images
val: images

names:
  0: ball
"""

    with open(os.path.join(output_dir, "data.yaml"), "w", encoding="utf-8") as f:
        f.write(yaml_content.strip())

    print("📄 'ball' sınıfını içeren 'data.yaml' başarıyla oluşturuldu.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Auto Labeling Script using YOLOv8")
    parser.add_argument("--input", type=str, default="data/raw_images", help="Girdi görsellerinin klasör yolu")
    parser.add_argument("--output", type=str, default="data/labeled_dataset", help="Çıktı klasör yolu")
    parser.add_argument("--conf", type=float, default=0.25, help="Confidence threshold")
    parser.add_argument("--device", type=str, default="cpu", help="Çalıştırma cihazı (cpu veya 0, 1 vs.)")

    args = parser.parse_args()
    auto_label(args.input, args.output, args.conf, args.device)
