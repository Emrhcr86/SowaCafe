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
 ("PASTALAR", "Cakes", [
   ("Devil's","Devil's Cake","₺200",None),
   ("Limonlu Cheesecake","Lemon Cheesecake","₺200",None),
   ("Frambuazlı Cheesecake","Raspberry Cheesecake","₺200",None),
 ]),
 ("ÇEKİRDEK KAHVE", "Coffee Beans", [
   ("Covim Çekirdek Kahve 1 kg","Covim Coffee Beans 1 kg","₺1300",None),
   ("Covim Çekirdek Kahve 500 gr","Covim Coffee Beans 500 g","₺650",None),
   ("Covim Filtre Kahve 250 gr","Covim Filter Coffee 250 g","₺350",None),
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
            f'<span class="cat-tr">{tr}</span><span class="cat-en" lang="en">{en}</span></div>'
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
  .page{min-height:250mm}
  .logo{width:62px;height:62px;background-size:368px auto;background-position:-90px -91px}
  .brand{font-size:20px;margin-top:6px}
  .tag{font-size:8px;margin-top:2px}
  .cols{display:flex;gap:10mm;margin-top:6mm}
  .col{flex:1;min-width:0}
  .cat{margin-top:5mm}
  .col > .cat:first-child{margin-top:0}
  .cat-tr{font-size:10.5px}
  .cat-en{font-size:7px}
  .item{padding:3.7px 0}
  .col-sol .item{padding:5.2px 0}
  .item .tr{font-size:9.4px;line-height:1.2}
  .item .en{font-size:7px;line-height:1.15}
  .item .var{font-size:6.6px;line-height:1.15;margin-top:.5px}
  .item .price{font-size:9.4px}
  .foot{margin-top:auto;padding-top:7px}
  .ig{font-size:9px}
  .info{font-size:7.6px;line-height:1.75;margin-top:4px}
"""
# Dağılım: sol/1. sayfa = kahve + çaylar + çekirdek | sağ/2. sayfa = soğuk + yiyecek + pasta
GRUP_A = bolum(*MENU[0]) + bolum(*MENU[1]) + bolum(*MENU[5])
GRUP_B = bolum(*MENU[2]) + bolum(*MENU[3]) + bolum(*MENU[4])
sol, sag = GRUP_A, GRUP_B
a4_2col = iskelet("SOWA · Menü (A4)", a4_2col_css,
    f'<div class="page">{basisim("a4")}'
    f'<div class="cols"><div class="col col-sol">{sol}</div><div class="col">{sag}</div></div>'
    f'{altbilgi()}</div>')

# ---------- 2) A5 çift taraflı ----------
a5_css = """
  @page{size:A5;margin:12mm}
  .page{height:186mm;overflow:hidden}
  .logo{width:48px;height:48px;background-size:285px auto;background-position:-69px -70px}
  .brand{font-size:16px;margin-top:4px}
  .tag{font-size:6.8px;margin-top:2px}
  .cat{margin-top:3.4mm}
  .cat-tr{font-size:9px}
  .cat-en{font-size:6.5px}
  .item{padding:1.9px 0}
  .item .tr{font-size:8.6px;line-height:1.15}
  .item .en{font-size:6.5px;line-height:1.1}
  .item .var{font-size:6.1px;line-height:1.1;margin-top:.3px}
  .item .price{font-size:8.6px}
  .foot{margin-top:3mm;padding-top:5px}
  .ig{font-size:8px}
  .info{font-size:6.6px;line-height:1.7;margin-top:3px}
  .sayfa2-bas{text-align:center;letter-spacing:.22em;font-size:13px;font-weight:500;
              margin-bottom:3mm}
"""
a5 = iskelet("SOWA · Menü (A5)", a5_css,
    f'<div class="page">{basisim("a5")}{GRUP_A}</div>'
    f'<div class="page"><div class="sayfa2-bas">SOWA</div>'
    f'{GRUP_B}{altbilgi()}</div>')

# ---------- 3) A4 çift yüz, tek sütun ----------
a4_1col_css = """
  @page{size:A4;margin:18mm}
  .page{height:261mm;overflow:hidden}
  .logo{width:78px;height:78px;background-size:463px auto;background-position:-113px -114px}
  .brand{font-size:23px;margin-top:8px}
  .tag{font-size:9px;margin-top:3px}
  .cat{margin-top:5mm}
  .cat-tr{font-size:12.5px}
  .cat-en{font-size:8.6px}
  .item{padding:3.8px 0}
  .item .tr{font-size:11.4px;line-height:1.18}
  .item .en{font-size:8.4px;line-height:1.14}
  .item .var{font-size:8px;line-height:1.14;margin-top:.5px}
  .item .price{font-size:11.4px}
  .foot{margin-top:6mm;padding-top:9px}
  .ig{font-size:10.5px}
  .info{font-size:8.8px;line-height:1.85;margin-top:5px}
  .sayfa2-bas{text-align:center;letter-spacing:.22em;font-size:19px;font-weight:500}
"""
a4_1col = iskelet("SOWA · Menü (A4 tek sütun)", a4_1col_css,
    f'<div class="page">{basisim("a4")}{GRUP_A}</div>'
    f'<div class="page"><div class="sayfa2-bas">SOWA</div>'
    f'{GRUP_B}{altbilgi()}</div>')

for ad, icerik in [("menu-a4-2sutun.html", a4_2col),
                   ("menu-a5-cift-tarafli.html", a5),
                   ("menu-a4-tek-sutun.html", a4_1col)]:
    (BURASI / ad).write_text(icerik, encoding="utf-8")
    print("yazıldı:", ad)
