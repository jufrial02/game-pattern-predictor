import time
import threading
from modules.scanner import capture_screen_area, detect_color_pattren
from modules.analyzer import calculate_probability
from modules.overlay import PredictorOverlay

# =====================================================================
# KONFIGURASI KOORDINAT SCANNER (Sesuaikan dengan posisi game di layar)
# =====================================================================
SCAN_X = 100       # Posisi koordinat X kotak riwayat game
SCAN_Y = 100       # Posisi koordinat Y kotak riwayat game
SCAN_WIDTH = 50    # Lebar area scan (pixel)
SCAN_HEIGHT = 50   # Tinggi area scan (pixel)
LOOP_DELAY = 2     # Jeda waktu pengecekan layar (detik)

# List global untuk menampung riwayat game yang terkumpul selama tools berjalan
game_history = []

def core_loop(overlay_app):
    """
    Fungsi utama yang berjalan di background untuk memantau layar
    dan memperbarui hasil prediksi pada overlay.
    """
    print("[+] Tools Predictor aktif. Memulai pemantauan layar...")
    last_detected_color = None
    
    while True:
        try:
            # 1. Ambil gambar di area koordinat yang diatur
            frame = capture_screen_area(SCAN_X, SCAN_Y, SCAN_WIDTH, SCAN_HEIGHT)
            
            # 2. Deteksi warna apa yang muncul di area tersebut
            current_color = detect_color_pattren(frame, None)
            
            # 3. Jika mendeteksi warna valid (Merah/Hijau) DAN warnanya baru (berubah dari sebelumnya)
            if current_color in ["Merah", "Hijau"] and current_color != last_detected_color:
                print(f"[!] Data Baru Terdeteksi: {current_color}")
                game_history.append(current_color)
                last_detected_color = current_color
                
                # Batasi riwayat agar tidak terlalu penuh (ambil 50 data terakhir saja)
                if len(game_history) > 50:
                    game_history.pop(0)
            
            # 4. Hitung probabilitas berdasarkan riwayat yang terkumpul saat ini
            if len(game_history) >= 2:
                predictions = calculate_probability(game_history, pattern_length=2)
                # Kirim hasil hitungan ke tampilan overlay
                overlay_app.update_prediction(predictions)
                
        except Exception as e:
            print(f"[-] Terjadi kesalahan pada core loop: {e}")
            
        # Jeda waktu sebelum melakukan scan ulang agar HP/PC tidak berat
        time.sleep(LOOP_DELAY)

def main():
    # 1. Inisialisasi jendela overlay melayang
    overlay = PredictorOverlay()
    
    # 2. Jalankan fungsi core_loop di dalam Thread terpisah (Background)
    # Supaya pencatatan data tidak mengganggu kelancaran pergerakan jendela overlay
    logic_thread = threading.Thread(target=core_loop, args=(overlay,), daemon=True)
    logic_thread.start()
    
    # 3. Mulai jalankan tampilan overlay di layar utama
    overlay.start()

if __name__ == "__main__":
    main()
  
