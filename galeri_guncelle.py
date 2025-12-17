import os

# --- AYARLAR ---
resim_klasoru = "images"
html_dosyasi = "index.html"

# Desteklenen formatlar
uzantilar = ('.jpg', '.jpeg', '.png', '.webp')

# --- HTML ŞABLONU (Üst Kısım) ---
html_baslangic = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Oytun Can Altay | Photography</title>
    <style>
        body { background-color: #000000; color: #ffffff; font-family: sans-serif; margin: 0; padding: 20px; }
        h1 { text-align: center; font-weight: 300; letter-spacing: 2px; margin-bottom: 40px; }
        
        .gallery-container {
            column-count: 3; column-gap: 15px; max-width: 1200px; margin: 0 auto;
        }
        .photo-item { break-inside: avoid; margin-bottom: 15px; transition: transform 0.3s ease; }
        .photo-item img { width: 100%; display: block; border-radius: 4px; }
        .photo-item:hover { transform: scale(1.02); cursor: pointer; }

        @media (max-width: 900px) { .gallery-container { column-count: 2; } }
        @media (max-width: 600px) { .gallery-container { column-count: 1; } }
    </style>
</head>
<body>

    <h1>OYTUN CAN ALTAY <br> <span style="font-size: 0.6em; color: #888;">PHOTOGRAPHY PORTFOLIO</span></h1>
    
    <div class="gallery-container">
"""

# --- HTML ŞABLONU (Alt Kısım) ---
html_bitis = """
    </div>
</body>
</html>
"""

def guncelle():
    print("📸 Fotoğraflar taranıyor...")
    
    # 1. Klasördeki resimleri bul
    try:
        dosyalar = os.listdir(resim_klasoru)
    except FileNotFoundError:
        print(f"HATA: '{resim_klasoru}' klasörü bulunamadı!")
        return

    # Sadece resim dosyalarını al ve sırala
    resimler = [f for f in dosyalar if f.lower().endswith(uzantilar)]
    resimler.sort() # İstersen burayı değiştirebiliriz

    print(f"Toplam {len(resimler)} fotoğraf bulundu.")

    # 2. HTML içeriğini oluştur
    yeni_icerik = html_baslangic

    for resim in resimler:
        blok = f"""
        <div class="photo-item">
            <img src="{resim_klasoru}/{resim}" loading="lazy" alt="{resim}">
        </div>
        """
        yeni_icerik += blok

    yeni_icerik += html_bitis

    # 3. Dosyayı kaydet
    with open(html_dosyasi, "w", encoding="utf-8") as f:
        f.write(yeni_icerik)
    
    print(f"✅ {html_dosyasi} başarıyla güncellendi! Siteye yüklemeye hazır.")

if __name__ == "__main__":
    guncelle()