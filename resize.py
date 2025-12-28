import os
from PIL import Image

# AYARLAR
INPUT_FOLDER = 'images'       # Senin fotoğraflarının olduğu klasör
OUTPUT_FOLDER = 'optimized'   # Küçülenlerin konacağı yer
MAX_WIDTH = 1920              # Full HD genişlik (Yeterli)
QUALITY = 80                  # Kalite (%80 idealdir)

def batch_resize():
    # Çıktı klasörü yoksa oluştur
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)

    print(f"🚀 {INPUT_FOLDER} klasöründeki resimler optimize ediliyor...")

    count = 0
    # Klasördeki dosyaları tara
    for filename in os.listdir(INPUT_FOLDER):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
            filepath = os.path.join(INPUT_FOLDER, filename)
            
            with Image.open(filepath) as img:
                # Orijinal formatı koru (JPEG, PNG vs.)
                img_format = img.format 
                
                # Boyutlandırma (Sadece büyükse küçült)
                if img.width > MAX_WIDTH:
                    ratio = MAX_WIDTH / float(img.width)
                    new_height = int((float(img.height) * float(ratio)))
                    img = img.resize((MAX_WIDTH, new_height), Image.Resampling.LANCZOS)
                
                # Kaydet (Aynı isimle, yeni klasöre)
                output_path = os.path.join(OUTPUT_FOLDER, filename)
                img.save(output_path, format=img_format, quality=QUALITY, optimize=True)
                
                print(f"✅ Küçültüldü: {filename}")
                count += 1

    print(f"\n🎉 İşlem Tamam! Toplam {count} fotoğraf optimize edildi.")
    print(f"📂 Yeni dosyalar '{OUTPUT_FOLDER}' klasöründe duruyor.")

if __name__ == "__main__":
    batch_resize()