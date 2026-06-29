import numpy as np
from collections import Counter

def calculate_probability(history, pattern_length=2):
    """
    Menghitung probabilitas hasil berikutnya berdasarkan kecenderungan pola historis.
    
    :param history: list data riwayat (contoh: ['Merah', 'Merah', 'Hijau', 'Merah'])
    :param pattern_length: panjang pola yang dijadikan acuan untuk menebak (default: 2)
    :return: dict berisi persentase peluang untuk setiap kemungkinan hasil berikutnya
    """
    # Jika data riwayat terlalu sedikit, berikan peluang acak/rata (50:50 jika ada 2 pilihan)
    if len(history) <= pattern_length:
        unique_elements = list(set(history)) if history else ["Merah", "Hijau"]
        return {item: round(100 / len(unique_elements), 2) for item in unique_elements}
    
    # 1. Ambil pola terakhir yang saat ini sedang terjadi di game
    current_pattern = history[-pattern_length:]
    
    # 2. Cari di riwayat terdahulu, setiap kali pola ini muncul, apa hasil berikutnya?
    next_elements = []
    for i in range(len(history) - pattern_length):
        # Ambil potongan riwayat sepanjang pattern_length untuk dicocokkan
        match_segment = history[i : i + pattern_length]
        
        if match_segment == current_pattern:
            # Jika cocok, catat elemen tepat setelah potongan ini
            next_element = history[i + pattern_length]
            next_elements.append(next_element)
            
    # 3. Hitung persentase jika pola tersebut pernah terjadi sebelumnya
    if next_elements:
        counts = Counter(next_elements)
        total_matches = len(next_elements)
        
        # Konversi jumlah kemunculan menjadi persentase %
        probabilities = {item: round((count / total_matches) * 100, 2) for item, count in counts.items()}
        return probabilities
    
    # 4. Jika pola terakhir ini BARU PERTAMA KALI muncul di riwayat, gunakan data global
    counts = Counter(history)
    total_elements = len(history)
    return {item: round((count / total_elements) * 100, 2) for item, count in counts.items()}


# =====================================================================
# BAGIAN PENGUJIAN (Hanya berjalan jika file ini dieksekusi langsung)
# =====================================================================
if __name__ == "__main__":
    # Simulasi data riwayat game (contoh: hasil 15 putaran terakhir)
    # Katakanlah polanya seringkali setelah 2 Merah, hasilnya adalah Hijau
    sample_history = [
        'Merah', 'Merah', 'Hijau', 
        'Merah', 'Merah', 'Hijau', 
        'Hijau', 'Merah', 'Merah', 
        'Merah', 'Hijau', 'Hijau',
        'Merah', 'Merah' # Ini kondisi saat ini (2 Merah berturut-turut)
    ]
    
    print("--- Simulasi Analisis Pola ---")
    print(f"Riwayat Game saat ini: {sample_history}")
    print(f"Pola terakhir yang dianalisis: {sample_history[-2:]}\n")
    
    hasil_prediksi = calculate_probability(sample_history, pattern_length=2)
    
    print("🔮 Prediksi Peluang Hasil Berikutnya:")
    for hasil, persentase in hasil_prediksi.items():
        print(f"👉 {hasil}: {persentase}%")
      
