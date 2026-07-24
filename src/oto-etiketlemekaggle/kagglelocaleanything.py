# --- 1. KÜTÜPHANE KURULUMU ---
import subprocess, sys

subprocess.run([sys.executable, "-m", "pip", "install", "-q", "-U",
                "transformers==4.57.1", "--force-reinstall", "--no-deps"])
subprocess.run([sys.executable, "-m", "pip", "install", "-q",
                "huggingface-hub<1.0,>=0.34.0", "--force-reinstall", "--no-deps"])
subprocess.run([sys.executable, "-m", "pip", "install", "-q", "-U", "accelerate"])

import transformers, huggingface_hub
print(f"transformers: {transformers.__version__}")
print(f"huggingface_hub: {huggingface_hub.__version__}")

# --- 2. MODELİ 2 GPU'YA DAĞITARAK YÜKLE ---
import sys, os, gc, torch
from unittest.mock import MagicMock
from transformers import AutoModel, AutoTokenizer, AutoProcessor

sys.modules['decord'] = MagicMock()
sys.modules['lmdb'] = MagicMock()

if 'model' in globals():
    del model
    gc.collect()
    torch.cuda.empty_cache()

model_path = "nvidia/LocateAnything-3B"
tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
processor = AutoProcessor.from_pretrained(model_path, trust_remote_code=True)
model = AutoModel.from_pretrained(
    model_path,
    torch_dtype=torch.bfloat16,
    trust_remote_code=True,
    device_map="auto"
).eval()

print("✅ Model başarıyla yüklendi ve GPU'lara dağıtıldı!")
print(model.hf_device_map)  # hangi katman hangi GPU'da, buradan doğrula


import os
import re
from PIL import Image, ImageDraw
from IPython.display import display

# --- GÖRSEL İŞLEME VE ÇİZİM ---
input_dir = "/kaggle/input/datasets/enesketenci/player/halisahaplayer/images/test"
output_base_dir = "/kaggle/working/halisahaplayer/labels/test"
os.makedirs(output_base_dir, exist_ok=True)

images_list = [f for f in os.listdir(input_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]

if not images_list:
    print(f"❌ {input_dir} klasöründe fotoğraf bulunamadı! Yolu kontrol et.")
else:
    test_image_name = images_list[0]
    image_path = os.path.join(input_dir, test_image_name)
    image = Image.open(image_path).convert("RGB")
    image.thumbnail((1280, 1280))

    draw_image = image.copy()
    draw = ImageDraw.Draw(draw_image)
    img_width, img_height = image.size

    print(f"📸 İşleniyor: {test_image_name}...")

    prompt = "Locate all the instances that matches the following description: person."
    messages = [
        {"role": "user", "content": [
            {"type": "image"},
            {"type": "text", "text": prompt}
        ]}
    ]

    text = processor.apply_chat_template(messages, add_generation_prompt=True)
    inputs = processor(text=[text], images=[image], return_tensors="pt").to(model.device)

    print("🧠 Model nesneleri arıyor...")
    with torch.no_grad():
        generated_ids = model.generate(
            pixel_values=inputs["pixel_values"].to(torch.bfloat16),
            input_ids=inputs["input_ids"],
            attention_mask=inputs["attention_mask"],
            image_grid_hws=inputs.get("image_grid_hws", None),
            tokenizer=tokenizer,
            max_new_tokens=256,
            use_cache=True,
            generation_mode="hybrid",
            do_sample=True,
            temperature=0.7,
            top_p=0.9,
            repetition_penalty=1.1,
        )

    output_text = generated_ids[0] if isinstance(generated_ids, tuple) else generated_ids

    print("\n📝 MODELİN HAM ÇIKTISI:")
    print(output_text)
    print("-" * 50)

    # --- KOORDİNATLARI AYIKLA (dedupe ile tekrar eden kutuları at) VE ÇİZ ---
    boxes_raw = re.findall(r'<box><(\d+)><(\d+)><(\d+)><(\d+)></box>', output_text)
    boxes = list(dict.fromkeys(boxes_raw))

    if not boxes:
        print("⚠️ Model çıktı üretti ancak formatında koordinat bulunamadı.")
    else:
        for idx, box in enumerate(boxes):
            x1, y1, x2, y2 = [int(v) / 1000 for v in box]
            x1, x2 = x1 * img_width, x2 * img_width
            y1, y2 = y1 * img_height, y2 * img_height

            draw.rectangle([x1, y1, x2, y2], outline="red", width=3)
            draw.text((x1, max(0, y1 - 15)), f"Player {idx+1}", fill="red")

        print(f"✅ {len(boxes)} kişi tespit edildi.")

    print("🎨 Çizilmiş Fotoğraf:")
    display(draw_image)

    # --- YOLO FORMATINDA KAYDET ---
    txt_filename = os.path.splitext(test_image_name)[0] + ".txt"
    txt_path = os.path.join(output_base_dir, txt_filename)
    with open(txt_path, "w", encoding="utf-8") as f:
        for box in boxes:
            x1, y1, x2, y2 = [int(v) / 1000 for v in box]
            xc = (x1 + x2) / 2
            yc = (y1 + y2) / 2
            bw = x2 - x1
            bh = y2 - y1
            f.write(f"0 {xc:.6f} {yc:.6f} {bw:.6f} {bh:.6f}\n")

    print(f"\n📁 YOLO formatında kaydedildi: {txt_path}")