# Veri Etiketleme İş Akışı (Workflow)

![Workflow Şeması](./workflow_labeling_system.png)

---

> **Not:** Bu dokümanda yer alan süreçlerde hata almanız durumunda, aksaklığı gidermek için lütfen bu kılavuzu güncel tutmaya özen gösterin.

## Süreç Rehberi

Projemizdeki veri setini hazırlamak ve ekibin kullanımına sunmak için aşağıdaki adımları sırasıyla takip etmelisin:

### 1. Ham Veri / Kareler
*   **Ne yapılmalı?** PTZ kamera kayıtlarını al, ilgili maç kesitlerini belirle ve videoyu karelere (frame) ayır.
*   **Araç:** Kullanılacak script'e [`YT-FrameExtractor`](https://github.com/emirhanuludogan/analiz_analytics/tree/main/src/YT-FrameExtractor) üzerinden ulaşabilirsin.
*   **İşlem:** Gereksiz sahneleri ayıkla ve optimize et.

### 2. Ön-etiketleme
*   **Ne yapılmalı?** Hazırlanan kareleri Kaggle GPU ortamına yükle.
*   **Araç:** [`oto-etiketle-kaggle`](https://github.com/emirhanuludogan/analiz_analytics/tree/main/src/oto-etiketlemekaggle) içerisindeki "Locate Anything" modelini kullanarak otomatik tespit (auto-labeling) işlemini gerçekleştir.

> **GitHub Erişim Notu:**
> Proje "private" (özel) içerikte olduğu için erişim sorunu yaşayabilirsiniz. Notebook hücresinin takılı kalması gibi yaygın hatalar için şu adımları kontrol edin:
> 1. Ayarlar kısmında erişim iznini **"Both"** veya **"Write and Read"** olarak seçtiğinizden emin olun (sadece read-only seçmeyin).
> 2. GitHub tarafından sağlanan API anahtarını kopyalayıp ilgili alana yapıştırdığınızdan emin olun.
> 3. GitHub clone hatası alıyorsanız, **Uludoğan** ile iletişime geçerek yetki talebinde bulunun.

### 3. Manuel Doğrulama
*   **Ne yapılmalı?** Otomatik oluşturulan etiketleri Label Studio üzerinden incele.
*   **İşlem:** Label Studio uygulamasını `PowerShell` üzerinden çalıştırarak kendi yerel ortamında doğrulama sürecini yürütebilirsin.
*   **Eylem:** Yanlış etiketleri düzelt veya sil. Hedefimiz **%100 doğruluktur.**

### 4. İsimlendirme ve Versiyonlama
*   **Kural:** Dosya ve veri seti isimlendirmesinde `takımAdi_takımAdi_yüklemeTarihi` formatını kullan.
    *   *Örnek:* `Kaplanoglu-Dostlarspor_27haziran2026`
*   **Versiyonlama:** Yapılan güncellemeler için mutlaka bir sürüm numarası (örneğin: `v1.0`, `v2.1`) ekle.

### 5. Hugging Face Hub
*   **Ne yapılmalı?** Doğrulanmış ve temizlenmiş "Gold" veri setini Hugging Face ortamına yükle.
*   **Eylem:** [https://huggingface.co/datasets/uldng-e/labeledball](https://huggingface.co/datasets/uldng-e/labeledball) adresine yükleme yaparken mutlaka şu formatı kullan: `YükleyenKişiAdı/TAKIMADI_tarih_frameSayisi.zip` (Örn: `Emirhan/BEKKAYA İNŞ GÖKBÖRÜ FK_25 Tem 2026_476.zip`).
*   **Önemli Not:** Lütfen anlaşılmayan kısımları sorun, boşu boşuna zaman kaybetmeyelim. Yükleme alanı ile ilgili sorun yaşarsanız **uludogan** ile iletişime geçin.

### 6. Takım Kullanımı
*   **Kullanım:** Yükleme süreci tamamlandığında, veri seti ekip arkadaşlarınız tarafından `load_dataset` fonksiyonu ile projeye entegre edilebilecektir.
*   **Durum:** Bu alan şu an demo aşamasındadır, altyapı tamamlandığında bilgilendirme yapılacaktır. Süreç tamamlandığında burası, tüm ekibin en güncel ve doğrulanmış verilere eriştiği "tek gerçek kaynak" (source of truth) noktası olacaktır.

### 7. Mimari
*   Bu model, **Medallion Architecture** mimarisinden esinlenerek yapılmıştır.
