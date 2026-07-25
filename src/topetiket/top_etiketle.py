import os
import glob
import shutil
import argparse
import subprocess
import sys

def check_dependencies():
    try:
        import ultralytics
    except ImportError:
        print("📦 Ultralytics (YOLO) kütüphanesi yükleniyor...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "ultralytics", "-q"])

check_dependencies()
from ultralytics import YOLO

def auto_label_ball(input_dir, output_dir, model_name="yolov8x.pt", conf_thresh=0.25, device="cpu"):
    """
    Görsellerdeki futbol/spor topu (COCO class 32) nesnelerini tespit eder 
    ve YOLO formatında otomatik etiketler.
    """
    images_out = os.path.join(output_dir, "images")
    labels_out = os.path.join(output_dir, "labels")

    os.makedirs(images_out, exist_ok=True)
    os.makedirs(labels_out, exist_ok=True)

    print(f"🚀 {model_name} modeli yükleniyor...")
    model = YOLO(model_name)

    TARGET_CLASS = 32  # COCO Class ID: sports ball

    valid_extensions = ("*.jpg", "*.png", "*.jpeg", "*.JPG", "*.PNG", "*.JPEG")
    image_files = []
    for ext in valid_extensions:
        image_files.extend(glob.glob(os.path.join(input_dir, "**", ext), recursive=True))

    print(f"📸 Toplam {len(image_files)} adet görsel taranıyor...")

    labeled_count = 0

    for img_path in image_files:
        filename = os.path.basename(img_path)
        txt_filename = os.path.splitext(filename)[0] + ".txt"

        results = model(img_path, conf=conf_thresh, device=device, verbose=False)[0]

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

    print(f"\n🎉 İşlem Tamamlandı!")
    print(f"✅ {len(image_files)} görselden {labeled_count} tanesinde TOP tespit edildi.")

    yaml_content = f"""path: {os.path.abspath(output_dir)}
train: images
val: images

names:
  0: ball
"""
    with open(os.path.join(output_dir, "data.yaml"), "w", encoding="utf-8") as f:
        f.write(yaml_content)

    print("📄 Sadece 'ball' sınıfını içeren 'data.yaml' oluşturuldu.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Otomatik Top Etiketleme Modülü")
    
    parser.add_argument("--input", type=str, default="./raw_dataset", help="Etiketlenecek ham görsellerin yolu")
    parser.add_argument("--output", type=str, default="./labeled_dataset", help="Çıktı klasör yolu")
    parser.add_argument("--model", type=str, default="yolov8x.pt", help="Kullanılacak YOLOv8 modeli")
    parser.add_argument("--conf", type=float, default=0.25, help="Güven eşiği")
    parser.add_argument("--device", type=str, default="cpu", help="Çalıştırma cihazı (cpu / 0)")

    args = parser.parse_args()

    auto_label_ball(
        input_dir=args.input,
        output_dir=args.output,
        model_name=args.model,
        conf_thresh=args.conf,
        device=args.device
    )