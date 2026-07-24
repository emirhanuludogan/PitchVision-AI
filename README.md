# analiz_analytics

# Proje Adı: Analiz Analytics

## Proje Yapısı
- `/src`: Ana Python kaynak kodları ve model dosyaları.
- `/notebooks`: Kaggle çalışmaları ve deneme kodları.
- `/data`: Veri setleri (Git tarafından takip edilmez, yerel tutulmalıdır).

## Çalışma Kuralları
- Asla 'main' dalına doğrudan commit atma.
- Kendi 'feature/isim-gorev' dalını aç ve oradan çalış.
- Veri setlerini Git'e yükleme, yerel klasörlerde tut.



# Analiz Analytics - Çalışma Kılavuzu

Ekip olarak düzenli ve çakışmasız çalışabilmemiz için aşağıdaki kuralları lütfen dikkatle okuyun ve uygulayın.

## 1. Altın Kural: `main` Dalı Dokunulmazdır
*   **Asla** `main` dalına doğrudan kod göndermeyin (push). 
*   `main` dalı her zaman çalışır durumda kalmalıdır.

## 2. Çalışma Düzeni (Branching Strategy)
Her yeni özellik veya görev için mutlaka kendi dalınızı (branch) oluşturun.

1.  **Güncel kalın:** Çalışmaya başlamadan önce mutlaka en güncel kodları alın:
    `git checkout main`
    `git pull origin main`

2.  **Yeni dal oluşturun:** İsimlendirme formatı: `feature/isim-gorev`
    *Örnek:* `git checkout -b feature/ahmet-model-egitimi`

3.  **Çalışmanızı kaydedin:** Değişikliklerinizi yapın, commit atın ve uzak sunucuya gönderin:
    `git add .`
    `git commit -m "Mesajınız"`
    `git push origin feature/isim-gorev`

4.  **Birleştirme (Merge):** İşiniz bittiğinde GitHub üzerinden `main` dalına **Pull Request (PR)** açın. Bizim onayımızdan sonra `main` dalına birleştirilecektir.

## 3. Veri Seti (Data) Politikası
*   **Verileri Git'e yüklemeyin!**
*   Tüm veri setleri (`dataset_attached`, `top_dataset` veya resimler) kendi bilgisayarınızdaki yerel `data/` klasöründe kalmalıdır.
*   `.gitignore` dosyamız bu klasörleri otomatik olarak yoksayar. Git sadece `.py`, `.ipynb`, `.md` gibi kaynak kodlarını takip eder.

## 4. İlk Kurulum (Sadece bir kez yapın)
Projeyi ilk defa bilgisayarınıza indiriyorsanız:

1.  **Clone edin:** `git clone <repo-linki>`
2.  **Sanal ortam oluşturun (Önerilen):** 
    `python -m venv venv`
    `source venv/bin/activate` (Windows için: `venv\Scripts\activate`)
3.  **Kütüphaneleri yükleyin:**
    `pip install -r requirements.txt`
4.  **Verileri yerleştirin:** `data/` klasörünü oluşturun ve ilgili veri dosyalarını bu klasörün içine (kendi bilgisayarınızda) kopyalayın.

---
*Sorun yaşarsanız veya bir dalı birleştirmeden önce yardıma ihtiyacınız olursa mutlaka haberleşelim.*