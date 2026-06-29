import tkinter as tk

class PredictorOverlay:
    def __init__(self):
        # 1. Inisialisasi jendela utama Tkinter
        self.root = tk.Tk()
        self.root.title("Predictor Overlay")
        
        # 2. Atur agar jendela selalu berada di paling depan (Always on Top)
        self.root.attributes("-topmost", True)
        
        # 3. Membuat latar belakang jendela menjadi transparan
        # Menggunakan warna hitam sebagai kunci transparansi (Chroma Key)
        self.root.config(bg='black')
        self.root.wm_attributes("-transparentcolor", 'black')
        
        # 4. Hilangkan border/tombol close bawaan windows agar terlihat bersih
        self.root.overrideredirect(True)
        
        # 5. Atur posisi jendela (Lebar x Tinggi + Koordinat X + Koordinat Y)
        # Kamu bisa menggeser angka +100+100 ini sesuai posisi ideal di layarmu
        self.root.geometry("250x80+100+100")
        
        # 6. Membuat label teks untuk menampilkan hasil prediksi
        self.label = tk.Label(
            self.root, 
            text="🔮 Menunggu Data...", 
            font=("Helvetica", 12, "bold"), 
            fg="#00FF00", # Warna teks Hijau Neon agar kontras
            bg="black"
        )
        self.label.pack(expand=True, fill='both')
        
        # Mengizinkan jendela untuk bisa digeser manual dengan mouse (drag)
        self.label.bind("<Button-1>", self.start_drag)
        self.label.bind("<B1-Motion>", self.drag)

    def start_drag(self, event):
        self.x = event.x
        self.y = event.y

    def drag(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.root.winfo_x() + deltax
        y = self.root.winfo_y() + deltay
        self.root.geometry(f"+{x}+{y}")

    def update_prediction(self, predictions):
        """
        Mengupdate teks di overlay berdasarkan hasil analisis probabilitas.
        :param predictions: dict dari analyzer.py (contoh: {'Hijau': 75.0, 'Merah': 25.0})
        """
        if not predictions:
            self.label.config(text="🔮 Membaca Pola...")
            return
            
        # Cari hasil yang persentasenya paling tinggi
        best_pick = max(predictions, key=predictions.get)
        percentage = predictions[best_pick]
        
        # Update teks tampilan
        text_display = f"👉 PREDIKSI: {best_pick.upper()}\n🎯 Peluang: {percentage}%"
        self.label.config(text=text_display)
        
    def start(self):
        # Jalankan loop GUI
        self.root.mainloop()

# =====================================================================
# BAGIAN PENGUJIAN (Hanya berjalan jika file ini dieksekusi langsung)
# =====================================================================
if __name__ == "__main__":
    print("--- Memulai Tes Jendela Overlay ---")
    print("Memunculkan jendela melayang transparan di layar...")
    
    overlay = PredictorOverlay()
    
    # Simulasi data prediksi uji coba setelah 2 detik
    overlay.root.after(2000, lambda: overlay.update_prediction({'Hijau': 78.4, 'Merah': 21.6}))
    
    overlay.start()
  
