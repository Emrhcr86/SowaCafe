# SOWA — Baskı Menüsü

Broşür/baskı için üç format. Hepsi **tek kaynaktan** (`olustur.py` içindeki `MENU`) üretilir.

| Dosya | Ne | Baskı |
| --- | --- | --- |
| `menu-a4-2sutun.pdf` | **Ana format.** A4, tek sayfa, iki sütun | Tek yüz — en ucuz |
| `menu-a5-cift-tarafli.pdf` | A5, iki sayfa (ön/arka) | El menüsü boyutu, çift taraflı |
| `menu-a4-tek-sutun.pdf` | A4, iki sayfa, tek sütun | Ferah, çift yüz |

## Menü değişince

1. `../index.html` içindeki web menüsünü güncelle
2. `olustur.py` içindeki `MENU` listesini **aynı şekilde** güncelle
3. Çalıştır:

```bash
python3 print/olustur.py   # HTML üretir
./print/pdf-yap.sh         # PDF'e çevirir (headless Chrome)
```

> ⚠️ **Menü iki yerde duruyor** — web (`index.html`) ve baskı (`olustur.py`). Biri
> değişince diğeri de değişmeli, yoksa QR menü ile broşür birbirini tutmaz. Sık
> değişecekse ikisini tek JSON'dan besleyen bir yapıya geçmek gerekir; şu anki
> güncelleme sıklığında bu iki dosyayı elde tutmak yeterli.

## Teknik notlar

- **Logo PDF'e gömülü** (base64 data URI) — dosyalar tek başına taşınabilir, matbaaya
  giderken yanında resim götürmeye gerek yok.
- Yazı tipi **Jost** (Google Fonts). Üretim sırasında internet gerekiyor; yoksa sistem
  sans-serif'e düşer ve görünüm değişir. PDF üretildikten sonra font gömülü olur.
- Tasarım siyah-beyaz — tek renk baskıda da sorunsuz.
- Sayfa yükseklikleri sabit (`height` + `overflow:hidden`). **Menüye çok sayıda kalem
  eklenirse taşan satır sessizce kesilir** — ekleme yaptıktan sonra PDF'i gözle kontrol et.
