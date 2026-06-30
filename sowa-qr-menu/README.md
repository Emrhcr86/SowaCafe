# SOWA QR Menü

## Proje Hakkında

SOWA için hazırlanmış ücretsiz, statik ve GitHub Pages uyumlu QR menü sitesidir.

Proje yalnızca HTML, CSS ve JavaScript kullanır. Backend, database veya ücretli servis gerektirmez. Menü içerikleri `menu.json` dosyasından dinamik olarak yüklenir.

## Dosya Yapısı

```text
sowa-qr-menu/
├─ index.html
├─ style.css
├─ script.js
├─ menu.json
├─ README.md
└─ assets/
   ├─ logo.jpeg
   └─ menu-reference.jpeg
```

Tüm dosya yolları relative olarak tanımlanmıştır. `index.html` proje root dizininde çalışır.

## Menü Güncelleme

Menü ürünlerini güncellemek için `menu.json` dosyasını düzenleyin.

Her ürün şu formatı kullanır:

```json
{
  "name": "Espresso",
  "description": "",
  "price": "₺75"
}
```

Yeni kategori eklemek için `categories` listesine yeni bir kategori objesi ekleyebilirsiniz. Fiyat göstermek istemiyorsanız `price` alanını boş bırakın.

## GitHub Pages Yayına Alma

1. Bu klasörü bir GitHub repository içine yükleyin.
2. Repository içinde `index.html` dosyasının root dizinde olduğundan emin olun.
3. GitHub üzerinde repository sayfasına gidin.
4. Şu yolu izleyin: `Settings > Pages > Deploy from branch > main > root`
5. Kaydettikten sonra GitHub Pages yayın linki oluşacaktır.

## QR Kod Oluşturma

GitHub Pages yayın linkini aldıktan sonra bu link için bir QR kod oluşturun.

QR oluşturmak için kullanılacak URL alanı:

```text
https://KULLANICI_ADI.github.io/sowa-qr-menu/
```

QR kodu bu URL'ye yönlendirilmelidir. Menüde değişiklik yaptığınızda aynı link çalışmaya devam eder; yeni QR kod oluşturmanız gerekmez.

## Test Checklist

- iPhone Safari'de açılıyor mu?
- Android Chrome'da açılıyor mu?
- Menü 2 saniyeden kısa sürede yükleniyor mu?
- Logo net görünüyor mu?
- Yazılar okunaklı mı?
- QR kod farklı ışık koşullarında okunuyor mu?
- Menü linki HTTPS olarak açılıyor mu?
