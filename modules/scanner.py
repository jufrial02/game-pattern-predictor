import cv2
import numpy as np
from PIL import ImageGrab

def capture_screen_area(x, y, width, height):
    """
    Mengambil tangkapan layar (screenshot) pada koordinat area tertentu.
    """
    # Mengambil screenshot area tertentu (X, Y, X+Width, Y+Height)
    bbox = (x, y, x + width, y + height)
    screenshot = ImageGrab.grab(bbox)
    
    # Konversi dari format PIL Image ke NumPy Array (agar bisa dibaca OpenCV)
    img_np = np.array(screenshot)
    
    # Konversi warna dari RGB (PIL) ke BGR (OpenCV)
    frame = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)
    return frame

def detect_color_pattren(frame, target_colors):
    """
    Mendeteksi warna dominan di tengah area yang di-scan 
    dan mencocokkannya dengan target_colors (misal: Merah atau Hijau).
    
    :param frame: Hasil tangkapan layar dari OpenCV
    :param target_colors: Dictionary berisi range warna BGR atau nama warna
    :return: String nama warna yang terdeteksi
    """
    # Ambil pixel di bagian paling tengah dari area yang di-scan
    height, width, _ = frame.shape
    mid_x, mid_y = width // 2, height // 2
    pixel_color = frame[mid_y, mid_x] # Mendapatkan format BGR
    
    b, g, r = pixel_color[0], pixel_color[1], pixel_color[2]
    
    # Logika deteksi warna sederhana berdasarkan dominasi nilai RGB
    if r > g and r > b and r > 100:
        return "Merah"
    elif g > r and g > b and g > 100:
        return "Hijau"
    
    return "Tidak Diketahui"

# =====================================================================
# BAGIAN PENGUJIAN (Hanya berjalan jika file ini dieksekusi langsung)
# =====================================================================
if __name__ == "__main__":
    print("--- Memulai Tes Scanner Layar ---")
    print("Mencoba mengambil area layar di koordinat (100, 100) dengan ukuran 50x50 pixel...")
    
    try:
        # Simulasi scan area kecil di layar
        test_frame = capture_screen_area(x=100, y=100, width=50, height=50)
        warna_terdeteksi = detect_color_pattren(test_frame, None)
        
        print(f"✅ Scanner Berhasil!")
        print(f"Warna dominan di tengah area tersebut: {warna_terdeteksi}")
    except Exception as e:
        print(f"❌ Gagal melakukan scan: {e}")
        print("Catatan: Jika dijalankan di Termux Android tanpa GUI, ImageGrab memerlukan akses display/VNC.")
      
