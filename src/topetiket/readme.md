# Otomatik Top Etiketleme Modülü

Bu modül, verilen bir ham görsel klasöründeki fotoğrafları önceden eğitilmiş YOLOv8x modelini kullanarak tarar ve **sadece top (class 0: ball)** içeren görselleri filtreleyip etiketlerini (YOLO txt formatında) oluşturur.

## Kullanım

```bash
python top_etiketle.py --input <HAM_GÖRSEL_KLASÖRÜ> --output <ÇIKTI_KLASÖRÜ>
