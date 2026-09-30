# 🚀 Label Studio Lokal Veri Seti Etiketleme Rehberi

Bu depo, 1000+ görselden oluşan büyük yerel (lokal) veri setlerini **Label Studio** üzerinde kasmadan, donmadan ve kırık görsel hatası almadan etiketlemek için gerekli klasör yapısını ve içe aktarma (import) adımlarını içerir.

Özellikle bilgisayarınızdaki yerel dosyaları bulut depolama kullanmadan Label Studio'ya bağlamak ve YOLO formatındaki mevcut etiketlerinizi kaybetmeden düzenlemek için bu rehberi takip edebilirsiniz.

---

## 📂 1. Klasör Yapısı

Projeye başlamadan önce çalışma dizininiz (`yeni_veriseti`) aşağıdaki gibi olmalıdır:

```text
yeni_veriseti/
├── images/                           # Etiketlenecek tüm fotoğraflar (.jpg, .png)
├── labels/                           # (Varsa) Fotoğraflarla aynı isimdeki YOLO .txt dosyaları
├── classes.txt                       # Sınıf listesi (Her satıra bir sınıf, örn: player)
├── proje_girdisi.label_config.xml    # Label Studio arayüz konfigürasyonu
└── olustur.py                        # (Opsiyonel) Görselleri Label Studio formatına çeviren betik
```

### `classes.txt` Dosyası
Sadece sınıflarınızı içermelidir. Örnek:
```text
player
```

### `proje_girdisi.label_config.xml` Neye Göre Oluşturulur?
Bu XML dosyası, Label Studio'nun etiketleme ekranını çizer. `<Label value="..." />` kısımları, `classes.txt` dosyanızla **birebir aynı isimde** olmak zorundadır.

Örnek (Tek sınıflı yapı):
```xml
<View>
  <Image name="image" value="$image"/>
  <Header value="RectangleLabels"/>
  <RectangleLabels name="label" toName="image">
    <!-- classes.txt içindeki sınıf isimlerini buraya value olarak ekliyoruz -->
    <Label value="player" background="rgba(218, 1, 238, 1)"/>
  </RectangleLabels>
</View>
```

---

## 🛠️ 2. Kurulum ve Gereksinimler

Python yüklü sisteminizde terminali/komut satırını açın ve Label Studio'yu kurun:

```bash
pip install label-studio label-studio-converter
```

---

## 🔄 3. Görselleri Label Studio (JSON) Formatına Çevirme

1000'den fazla fotoğrafı Label Studio'ya tek tek yüklemek tarayıcıyı donduracaktır. Bunun yerine görsellerin dosya yollarını (path) içeren bir JSON haritası oluşturmalıyız. 

Bunu yapmanın en kolay yolu resmi dönüştürücüyü kullanmaktır. Terminalde `yeni_veriseti` klasörünün içindeyken şu komutu çalıştırın:

```bash
label-studio-converter import yolo -i . -o proje_girdisi.json --image-root-url /data/local-files/?d=images/
```

*Not: Bu komut, klasördeki `images`, `labels` ve `classes.txt` dosyalarını okuyarak bir `proje_girdisi.json` dosyası oluşturur.*

---

## 🚀 4. Label Studio'yu Başlatma (Kritik Adım)

Label Studio'nun yerel bilgisayarınızdaki (C:/ veya D:/ diskindeki) fotoğrafları okuyabilmesi için **Lokal Dosya Servisi** izniyle başlatılması şarttır. Terminalinize göre aşağıdaki komutlardan birini kullanın:

**Windows CMD için (Boşluklara dikkat edin):**
```cmd
set LABEL_STUDIO_LOCAL_FILES_SERVING_ENABLED=true& label-studio start
```

**Windows PowerShell için:**
```powershell
$env:LABEL_STUDIO_LOCAL_FILES_SERVING_ENABLED="true"; label-studio start
```

**Mac/Linux için:**
```bash
LABEL_STUDIO_LOCAL_FILES_SERVING_ENABLED=true label-studio start
```

Tarayıcınızda `http://localhost:8080` adresi otomatik açılacaktır.

---

## ⚙️ 5. Label Studio Proje Ayarları ve İçe Aktarma

Label Studio arayüzüne girdikten sonra:

### Adım 5.1: Proje Oluşturma ve Arayüzü Ayarlama
1. **Create Project** diyerek yeni bir proje açın. İsmini verin ve **Save**'e basın.
2. Sağ üstten **Settings -> Labeling Interface** menüsüne gidin.
3. Sağ üstteki **Code** (XML) butonuna tıklayın.
4. Klasörünüzdeki `proje_girdisi.label_config.xml` içeriğini buraya kopyalayıp yapıştırın ve **Save** deyin.

### Adım 5.2: Lokal Dosya Bağlantısı (Cloud Storage)
1. Sol menüden **Cloud Storage**'a tıklayın.
2. **Add Source Storage** butonuna tıklayın.
3. Ayarları şu şekilde doldurun:
   * **Storage Type:** `Local files`
   * **Storage Title:** `yerel_veriseti`
   * **Absolute local path:** `C:/Users/KULLANICI_ADINIZ/Desktop/yeni_veriseti` *(Kendi tam klasör yolunuzu yazın. Slaşların `/` yönüne dikkat edin)*
   * **Treat every bucket object as a source file:** `KAPALI (Unchecked) Bırakın!`
4. **Test Connection** diyerek yeşil uyarıyı görün ve **Save**'e basın.
5. *Önemli: "Sync Storage" butonuna BASMAYIN.*

### Adım 5.3: Verileri İçeri Alma
1. Sol üstten projenizin adına tıklayarak ana tabloya dönün.
2. Sağ üstteki mor **Import** butonuna tıklayın.
3. Oluşturduğumuz **`proje_girdisi.json`** dosyasını buraya sürükleyip bırakın.

Tebrikler! Tüm fotoğraflarınız (varsa kutuları ve etiketleriyle birlikte) anında panele yüklendi. Görsellere tıklayarak etiketlemeye başlayabilirsiniz!

---

## 💾 6. Dışa Aktarma (Export) ve YOLO Model Eğitimi

Etiketlemeleriniz bittiğinde verilerinizi modeli eğitmek üzere YOLO formatında geri almak için:

1. Label Studio ana ekranında sağ üstteki **Export** butonuna tıklayın.
2. Açılan listeden **YOLO** formatını seçin.
3. İnen ZIP dosyasının içerisinde `classes.txt`, `images` ve `labels` klasörleri hazır bir şekilde bulunacaktır. Bu klasörleri doğrudan YOLO model eğitiminize (Örn: Ultralytics YOLOv8) verebilirsiniz.
