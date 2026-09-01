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

## 🗂️ Kategori dağılımı

Menü altı bölüm. Üç formatta da aynı ikiye ayrılır (`olustur.py` içinde `GRUP_A` / `GRUP_B`):

| Grup | Bölümler | Nerede |
| --- | --- | --- |
| **A** | Kahve Çeşitleri · Çaylar · Çekirdek Kahve | sol sütun / 1. sayfa |
| **B** | Soğuk Kahve ve İçecekler · Yiyecekler · Pastalar | sağ sütun / 2. sayfa |

19 + 20 kalem — dengeli. Bölüm eklenince bu dağılımı da gözden geçir, yoksa bir taraf şişer.

## ⚖️ A4 iki sütunda sütun dengesi — dikkat

Sağ sütunda beş varyant satırı var (Ice Tea, Milkshake, Frozen, iki tost), solda bir tane.
Bu yüzden sol sütun doğal olarak kısa kalıyordu. Denge, **sol sütunun satır aralığı bir tık
açılarak** kuruldu:

```css
.col-sol .item{padding:5.2px 0}   /* sağ sütun: 3.7px */
```

> **Menüye kalem eklenip çıkarıldığında bu denge bozulur.** PDF'e bakıp iki sütunun aynı hizada
> bittiğini kontrol et; değilse `.col-sol .item` padding değerini büyüt/küçült (her 1px ≈ 40px
> sütun boyu farkı). 2026-09-01 ölçümü: sol 728px, sağ 733px.

## 🔍 Taşma kontrolü — göz yerine ölçü

Sayfa yükseklikleri sabit, taşan satır **sessizce kesilir**. Gözle aramak yerine ölç:

```bash
# 1) sayfa sayısı doğru mu (1 / 2 / 2)
for f in menu-a4-2sutun menu-a5-cift-tarafli menu-a4-tek-sutun; do
  python3 -c "import re;d=open('print/$f.pdf','rb').read();print('$f',len(re.findall(rb'/Type\s*/Page[^s]',d)))"
done
# 2) bütün fiyatlar basıldı mı (fiyatlı kalem sayısı kadar ₺ olmalı — şu an 37)
pdftotext print/menu-a5-cift-tarafli.pdf - | grep -o "₺" | wc -l
```

Kesilen satır PDF'e hiç girmediği için ₺ sayısı düşer — en hızlı alarm bu.

## 📐 Sayfa marjları

| Format | Marj | Neden |
| --- | --- | --- |
| A4 iki sütun | 15mm | Fiyatların sağda nefes payı |
| A5 | 12mm | 9mm'de fiyatlar kenara dayanıyordu; matbaada kesim riski de var |
| A4 tek sütun | 18mm | Ferah düzen |

`.page` yüksekliği marjla **birlikte** ayarlanmalı: `yükseklik = kağıt − 2×marj − pay`.
Marjı büyütüp yüksekliği küçültmezsen sayfa taşar (A4 iki sütun bir kez böyle 2 sayfaya çıktı).

## Teknik notlar

- **Logo PDF'e gömülü** (base64 data URI) — dosyalar tek başına taşınabilir, matbaaya
  giderken yanında resim götürmeye gerek yok.
- Yazı tipi **Jost** (Google Fonts). Üretim sırasında internet gerekiyor; yoksa sistem
  sans-serif'e düşer ve görünüm değişir. PDF üretildikten sonra font gömülü olur.
- **İngilizce başlıklarda `lang="en"` şart.** Sayfa `lang="tr"` olduğu için
  `text-transform:uppercase` Türkçe kurala göre çeviriyordu: "Cold Drinks" → **"COLD DRİNKS"**
  (noktalı İ). `.cat-en` span'ine `lang="en"` eklenerek düzeltildi (2026-09-01). Yeni bir
  İngilizce büyük harf alanı eklersen aynısını yap.
- Tasarım siyah-beyaz — tek renk baskıda da sorunsuz.
- Sayfa yükseklikleri sabit (`height` + `overflow:hidden`). **Menüye çok sayıda kalem
  eklenirse taşan satır sessizce kesilir** — ekleme yaptıktan sonra PDF'i gözle kontrol et.
