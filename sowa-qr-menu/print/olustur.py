#!/usr/bin/env python3
"""SOWA Cafe — baskı menüsü üretici.
Menü verisi burada tek yerde; üç format da bundan çıkar.
Web menüsü (../index.html) değişince buradaki MENU'yü de güncelle.
Çalıştır:  python3 print/olustur.py   →  HTML üretir
Sonra:     bash print/pdf-yap.sh      →  PDF'e çevirir
"""
import base64, io, os, pathlib

BURASI = pathlib.Path(__file__).parent
KOK = BURASI.parent

MENU = [
 ("KAHVE ÇEŞİTLERİ", "Coffee", [
   ("Espresso","Espresso","₺90",None),
   ("Double Espresso","Double Espresso","₺110",None),
   ("Americano","Americano","₺140",None),
   ("Filtre Kahve","Filter Coffee","₺140",None),
   ("Cappuccino","Cappuccino","₺160",None),
   ("Latte","Latte","₺160",None),
   ("Flat White","Flat White","₺170",None),
   ("Cortado","Cortado","₺150",None),
   ("Mocha","Mocha","₺170",None),
   ("White Mocha","White Mocha","₺170",None),
   ("Caramel Latte","Caramel Latte","₺170",None),
   ("Türk Kahvesi","Turkish Coffee","₺80",None),
   ("Chai Tea Latte","Chai Tea Latte","₺160",None),
   ("Sıcak Çikolata","Hot Chocolate","₺160",None),
 ]),
 ("ÇAYLAR", "Tea", [
   ("Çay","Tea","₺30",None),
   ("Bitki Çayları","Herbal Teas","","Ihlamur, Nane Limon, Hibiskus"),
 ]),
 ("SOĞUK KAHVE VE İÇECEKLER", "Cold Drinks", [
   ("Ev Yapımı Limonata","Homemade Lemonade","₺140",None),
   ("Sowa Ice Tea","Sowa Iced Tea","₺150","Şeftali, Mango, Ananas vb."),
   ("Portakal Suyu","Orange Juice","",None),
   ("Ice Americano","Ice Americano","₺150",None),
   ("Ice Latte","Ice Latte","₺170",None),
   ("Ice Cappuccino","Ice Cappuccino","₺170",None),
   ("Ice Mocha","Ice Mocha","₺180",None),
   ("Ice White Chocolate Mocha","Ice W. Chocolate Mocha","₺180",None),
   ("Ice Caramel Latte","Ice Caramel Latte","₺180",None),
   ("Milkshake","Milkshake","₺180","Çikolata, Çilek"),
   ("Frozen","Frozen","₺180","Ananas, Mango, Karadut, Yaban Mersini vb."),
   ("Soda","Soda","₺35",None),
   ("Meyveli Soda","Fruit Soda","₺50",None),
   ("Su","Water","₺20",None),
 ]),
 ("YİYECEKLER", "Food", [
   ("Kaşarlı Tost","Cheese Toastie","₺120",None),
   ("Karışık Tost","Combination Toast","₺140","Sucuk, Kaşar"),
   ("Sowa Tost","Special Sowa Toast","₺150","Özel Sowa Sosu, Sucuk, Kaşar"),
 ]),
]

IG = "@sowacafesoke"
SAAT = "Her gün 08:00 – 20:00"
ADRES = "Basmacılar Çarşısı, Üçüncü Hasırcılar Sk. No:12 Söke/Aydın"

logo_b64 = base64.b64encode((KOK / "sowa.jpeg").read_bytes()).decode()
LOGO_URI = f"data:image/jpeg;base64,{logo_b64}"


def kalem(tr, en, fiyat, var):
    v = f'<span class="var">({var})</span>' if var else ""
    return (f'<div class="item"><div class="names"><span class="tr">{tr}</span>'
            f'<span class="en">{en}</span>{v}</div>'
            f'<span class="sp"></span><span class="price">{fiyat}</span></div>')


def bolum(tr, en, kalemler):
    items = "".join(kalem(*k) for k in kalemler)
    return (f'<section class="cat"><div class="cat-head">'
            f'<span class="cat-tr">{tr}</span><span class="cat-en">{en}</span></div>'
            f'{items}</section>')


def basisim(boyut):
    return (f'<div class="head"><div class="logo"></div>'
            f'<div class="brand">SOWA</div>'
            f'<div class="tag">Coffee &amp; Pause</div></div>')


def altbilgi():
    return (f'<footer class="foot"><div class="ig">{IG}</div>'
            f'<div class="info">{SAAT}<br>{ADRES}</div></footer>')


ORTAK_CSS = """
  *{box-sizing:border-box;margin:0;padding:0}
  html,body{background:#fff}
  body{font-family:"Jost","Helvetica Neue",Arial,sans-serif;color:#1a1a1a;
       -webkit-print-color-adjust:exact;print-color-adjust:exact}
  .page{page-break-after:always;display:flex;flex-direction:column}
  .page:last-child{page-break-after:auto}
  .head{display:flex;flex-direction:column;align-items:center;text-align:center}
  .logo{border-radius:50%;border:1.2px solid #1a1a1a;background-image:url("LOGO");
        background-repeat:no-repeat;background-color:#fff;background-blend-mode:multiply}
  .brand{font-weight:500;letter-spacing:.22em}
  .tag{font-weight:300;letter-spacing:.44em;text-transform:uppercase}
  .cat{break-inside:avoid-column}
  .cat-head{display:flex;align-items:baseline;justify-content:space-between;
            border-bottom:1px solid #1a1a1a;padding-bottom:5px}
  .cat-tr{font-weight:400;letter-spacing:.28em;text-transform:uppercase}
  .cat-en{font-weight:300;letter-spacing:.18em;color:#9a9a9a;text-transform:uppercase;
          white-space:nowrap;padding-left:10px}
  .item{display:flex;align-items:baseline;gap:8px;border-bottom:.6px solid #ececec;
        break-inside:avoid}
  .item .names{display:flex;flex-direction:column;gap:0}
  .item .tr{font-weight:400}
  .item .en{font-weight:300;color:#a8a8a8}
  .item .var{font-weight:300;color:#b8b8b8}
  .item .sp{flex:1}
  .item .price{font-weight:400;white-space:nowrap}
  .foot{margin-top:auto;padding-top:12px;border-top:1px solid #1a1a1a;text-align:center}
  .ig{font-weight:400;letter-spacing:.14em;text-transform:uppercase}
  .info{font-weight:300;color:#6e6e6e;letter-spacing:.1em;text-transform:uppercase}
"""


def iskelet(baslik, sayfa_css, govde):
    css = ORTAK_CSS.replace("LOGO", LOGO_URI)
    return f"""<!doctype html>
<html lang="tr"><head><meta charset="utf-8"><title>{baslik}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Jost:wght@300;400;500&display=swap" rel="stylesheet">
<style>{css}{sayfa_css}</style></head><body>{govde}</body></html>"""


# ---------- 1) A4 tek yüz, 2 sütun ----------
a4_2col_css = """
  @page{size:A4;margin:15mm}
  .page{min-height:255mm}
  .logo{width:74px;height:74px;background-size:439px auto;background-position:-107px -108px}
  .brand{font-size:23px;margin-top:8px}
  .tag{font-size:8.5px;margin-top:3px}
  .cols{display:flex;gap:11mm;margin-top:9mm}
  .col{flex:1;min-width:0}
  .cat{margin-top:7mm}
  .col > .cat:first-child{margin-top:0}
  .cat-tr{font-size:11.5px}
  .cat-en{font-size:7.5px}
  .item{padding:5.2px 0}
  .col-sol .item{padding:7.4px 0}
  .item .tr{font-size:10px}
  .item .en{font-size:7.4px}
  .item .var{font-size:7px;margin-top:1px}
  .item .price{font-size:10px}
  .foot{margin-top:auto;padding-top:9px}
  .ig{font-size:9.5px}
  .info{font-size:8px;line-height:1.9;margin-top:5px}
"""
sol = bolum(*MENU[0]) + bolum(*MENU[1])
sag = bolum(*MENU[2]) + bolum(*MENU[3])
a4_2col = iskelet("SOWA · Menü (A4)", a4_2col_css,
    f'<div class="page">{basisim("a4")}'
    f'<div class="cols"><div class="col col-sol">{sol}</div><div class="col">{sag}</div></div>'
    f'{altbilgi()}</div>')

# ---------- 2) A5 çift taraflı ----------
a5_css = """
  @page{size:A5;margin:12mm}
  .page{height:186mm;overflow:hidden}
  .logo{width:56px;height:56px;background-size:332px auto;background-position:-81px -82px}
  .brand{font-size:18px;margin-top:5px}
  .tag{font-size:7.2px;margin-top:2px}
  .cat{margin-top:5mm}
  .cat-tr{font-size:9.6px}
  .cat-en{font-size:6.9px}
  .item{padding:2.9px 0}
  .item .tr{font-size:9.1px;line-height:1.25}
  .item .en{font-size:6.9px;line-height:1.2}
  .item .var{font-size:6.5px;line-height:1.2;margin-top:.5px}
  .item .price{font-size:9.1px}
  .foot{margin-top:5mm;padding-top:7px}
  .ig{font-size:8.4px}
  .info{font-size:6.9px;line-height:1.8;margin-top:4px}
  .sayfa2-bas{text-align:center;letter-spacing:.22em;font-size:13px;font-weight:500;
              margin-bottom:3mm}
"""
a5 = iskelet("SOWA · Menü (A5)", a5_css,
    f'<div class="page">{basisim("a5")}{bolum(*MENU[0])}{bolum(*MENU[1])}</div>'
    f'<div class="page"><div class="sayfa2-bas">SOWA</div>'
    f'{bolum(*MENU[2])}{bolum(*MENU[3])}{altbilgi()}</div>')

# ---------- 3) A4 çift yüz, tek sütun ----------
a4_1col_css = """
  @page{size:A4;margin:18mm}
  .page{height:261mm;overflow:hidden}
  .logo{width:96px;height:96px;background-size:570px auto;background-position:-138px -141px}
  .brand{font-size:27px;margin-top:10px}
  .tag{font-size:10px;margin-top:4px}
  .cat{margin-top:8mm}
  .cat-tr{font-size:14px}
  .cat-en{font-size:9.5px}
  .item{padding:5.6px 0}
  .item .tr{font-size:12.5px;line-height:1.3}
  .item .en{font-size:9.2px;line-height:1.25}
  .item .var{font-size:8.8px;line-height:1.25;margin-top:1px}
  .item .price{font-size:12.5px}
  .foot{margin-top:11mm;padding-top:12px}
  .ig{font-size:11.5px}
  .info{font-size:9.5px;line-height:2;margin-top:6px}
  .sayfa2-bas{text-align:center;letter-spacing:.22em;font-size:19px;font-weight:500}
"""
a4_1col = iskelet("SOWA · Menü (A4 tek sütun)", a4_1col_css,
    f'<div class="page">{basisim("a4")}{bolum(*MENU[0])}{bolum(*MENU[1])}</div>'
    f'<div class="page"><div class="sayfa2-bas">SOWA</div>'
    f'{bolum(*MENU[2])}{bolum(*MENU[3])}{altbilgi()}</div>')

for ad, icerik in [("menu-a4-2sutun.html", a4_2col),
                   ("menu-a5-cift-tarafli.html", a5),
                   ("menu-a4-tek-sutun.html", a4_1col)]:
    (BURASI / ad).write_text(icerik, encoding="utf-8")
    print("yazıldı:", ad)
