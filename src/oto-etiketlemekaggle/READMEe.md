# LocateAnything-3B ile Halı Saha Oyuncu Tespiti ve YOLO Formatına Dönüştürme

Bu betik, Kaggle ortamında NVIDIA'nın **LocateAnything-3B** Çok Modlu (VLM) modelini iki GPU (`device_map="auto"`) üzerinde çalıştırarak halı saha test görselleri üzerinde insan/oyuncu tespiti (`person`) yapar. Model çıktısını görselleştirir ve sonuçları doğrudan **YOLO formatında (`.txt`)** kaydeder.

---

## 📌 Proje ve Klasör Yapısı

Kod dosyası Kaggle Notebook ortamında çalışacak şekilde yapılandırılmıştır. Dosya girdi ve çıktı yolları şu şekildedir:

### 📥 Girdi Yolu (Input Directory)
* **Görsellerin Alındığı Konum:**
  `/kaggle/input/datasets/enesketenci/player/halisahaplayer/images/test`
* **İçerik:** Klasör içerisinde `.jpg`, `.jpeg` veya `.png` uzantılı halı saha maç görselleri yer almalıdır.

### 📤 Çıktı Yolları (Output Directories)
* **YOLO Etiket Dosyaları (`.txt`):**
  `/kaggle/working/halisahaplayer/labels/test/`
  * *Açıklama:* İşlenen görselin ismiyle aynı adda (örn. `image1.jpg` -> `image1.txt`) bir etiket dosyası oluşturulur.
* **Görsel Çıktısı:**
  Modelin çizdiği kırmızı bounding box (sınırlayıcı kutu) alanları `IPython.display` ile notebook hücre çıktısında anlık olarak görüntülenir.

---

## ⚙️ Kurulum ve Bağımlılıklar

Betik ilk çalıştırıldığında gerekli Python kütüphanelerini otomatik olarak doğru sürümleriyle yükler/günceller:

* `transformers==4.57.1`
* `huggingface-hub<1.0,>=0.34.0`
* `accelerate`
* `PIL (Pillow)`, `torch`, `IPython`

> **Not:** `decord` ve `lmdb` kütüphanelerinin eksikliğinden kaynaklı yükleme hatalarını önlemek için kod içinde `sys.modules` seviyesinde mock edilmiştir.

---

## 🚀 Çalıştırma Adımları

1. **Kaggle GPU Ortamını Açın:** Notebook'u çalıştırırken **Dual T4 GPU** veya **P100 GPU** seçeneğinin aktif olduğundan emin olun.
2. **Dataset Bağlantısını Sağlayın:** `/kaggle/input/datasets/enesketenci/player/halisahaplayer/images/test` dizininde test görsellerinizin yüklü olduğundan emin olun.
3. **Kodu Çalıştırın:** Betik sırasıyla paketleri kuracak, modeli dual-GPU dağıtımıyla yükleyecek, ilk test görselini işleyip YOLO formatındaki etiket dosyasını `/kaggle/working/` dizinine kaydedecektir.

---

## ⚠️ Dikkat Edilmesi Gereken Önemli Hususlar

1. **Kaggle Input Dizini Salt Okunurdur (Read-Only):**
   Kaggle'da `/kaggle/input/` klasörü sadece okunabilir. Bu nedenle oluşturulan `.txt` etiket dosyaları ve çıktılar mutlaka **`/kaggle/working/`** dizinine kaydedilmelidir.
2. **BBox Koordinat Normalizasyonu:**
   LocateAnything-3B modeli koordinatları `[0, 1000]` aralığında döndürür. Kod içerisindeki işlem adımları:
   * **Çizim için:** `(x / 1000) * görsel_genişliği` şeklinde piksel koordinatlarına çevrilir.
   * **YOLO Formatı için:** `[0, 1]` aralığında `Sınıf_ID x_center y_center width height` formatına dönüştürülür.
3. **Tekrar Eden Kutuların Engellenmesi (Deduplication):**
   Model aynı nesne için birden fazla çakışan koordinat üretebilir. Kod içerisindeki `list(dict.fromkeys(boxes_raw))` yapısı tekrar eden tespitleri temizler.
4. **Bellek (GPU RAM) Yönetimi:**
   Model `torch.bfloat16` hassasiyetinde yüklenmektedir. Bellek taşmasını (OOM) önlemek için çalıştırma öncesinde `gc.collect()` ve `torch.cuda.empty_cache()` çağrıları dahil edilmiştir.
