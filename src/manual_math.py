"""
manual_math.py
Fungsi matematika dasar dihitung MANUAL menggunakan Taylor series.
TIDAK menggunakan np.exp, np.sin, math.exp, math.sin, dll.
numpy hanya dipakai untuk array/storage (np.zeros, dll), bukan fungsi matematika.
"""

def faktorial(n):
    """Hitung n! secara manual (iteratif)."""
    hasil = 1
    for i in range(2, n + 1):
        hasil *= i
    return hasil

def _taylor_exp_kecil(x, n_term=20):
    """
    Taylor series murni e^x = sum x^n/n!, HANYA dipakai untuk |x| kecil
    (setelah range reduction), di mana deret konvergen cepat dan stabil
    secara numerik (tanpa catastrophic cancellation).
    """
    hasil = 0.0
    suku = 1.0  # suku ke-0 = x^0/0! = 1
    for n in range(n_term):
        if n > 0:
            suku *= x / n  # suku_n = suku_(n-1) * x/n  -> hindari hitung pangkat & faktorial besar terpisah
        hasil += suku
    return hasil

def exp_manual(x, k=256):
    """
    Hitung e^x secara manual dengan TEKNIK RANGE REDUCTION:

        e^x = (e^(x/k))^k

    Alasan: Taylor series e^x = sum x^n/n! akurat dan stabil HANYA untuk
    |x| kecil (suku-suku deret kecil, tidak ada catastrophic cancellation).
    Untuk |x| besar (misal x=23, kasus tegangan dioda V/VT), Taylor series
    polos GAGAL karena melibatkan penjumlahan angka sangat besar yang saling
    membatalkan, menghancurkan presisi floating-point.

    Solusi: pecah x menjadi x/k (sangat kecil, |x/k| << 1), hitung Taylor
    series di sana (akurat), lalu pangkatkan k kali. Ini sama persis dengan
    teknik "scaling and squaring" yang dipakai library matematika profesional.

    k=256 dipilih agar x/k selalu << 1 untuk rentang x yang dipakai di
    proyek ini (x hingga ~40), sehingga Taylor series suku kecil konvergen
    sangat cepat dan akurat.
    """
    x_kecil = x / k
    hasil_kecil = _taylor_exp_kecil(x_kecil)
    # (e^(x/k))^k dihitung dengan perkalian berulang manual (bukan ** library pangkat besar)
    hasil = 1.0
    basis = hasil_kecil
    sisa = k
    while sisa > 0:
        if sisa % 2 == 1:
            hasil *= basis
        basis *= basis
        sisa //= 2
    return hasil

PI = 3.14159265358979323846
DUA_PI = 2 * PI

def _taylor_sin_kecil(x, n_term=15):
    """
    Taylor series murni sin(x) = x - x^3/3! + x^5/5! - ...
    HANYA dipakai untuk |x| kecil (setelah range reduction ke [-pi, pi]),
    di mana deret konvergen cepat dan akurat.
    """
    hasil = 0.0
    tanda = 1
    for n in range(n_term):
        pangkat = 2 * n + 1
        hasil += tanda * (x ** pangkat) / faktorial(pangkat)
        tanda *= -1
    return hasil

def sin_manual(x, n_term=15):
    """
    Hitung sin(x) secara manual dengan RANGE REDUCTION mod 2*pi:

        sin(x) = sin(x - 2*pi*k)   untuk k bulat sembarang

    Alasan: Taylor series sin(x) akurat HANYA untuk |x| kecil (mendekati 0).
    Untuk |x| besar (misal x=omega*t pada simulasi panjang, bisa mencapai
    puluhan radian), Taylor series polos GAGAL TOTAL -- hasilnya bisa jauh
    di luar rentang [-1, 1] yang valid untuk sin(x).

    Solusi: kurangi x dengan kelipatan 2*pi terdekat sampai hasilnya masuk
    rentang [-pi, pi], BARU hitung Taylor series di rentang kecil itu.
    k dihitung manual dengan pembagian bulat (bukan np.mod atau math.fmod).
    """
    # Reduksi x ke rentang [-pi, pi] dengan mengurangi kelipatan 2*pi
    k = int(x / DUA_PI)          # perkiraan jumlah periode penuh (pembagian bulat manual)
    x_reduksi = x - k * DUA_PI   # sisa setelah dikurangi k*2*pi, masih bisa sedikit > pi

    # Penyesuaian akhir agar x_reduksi pasti di [-pi, pi]
    while x_reduksi > PI:
        x_reduksi -= DUA_PI
    while x_reduksi < -PI:
        x_reduksi += DUA_PI

    return _taylor_sin_kecil(x_reduksi, n_term)

if __name__ == "__main__":
    import math  # HANYA untuk pembanding/validasi, TIDAK dipakai di program utama

    print("=== Validasi exp_manual() vs math.exp() ===")
    print(f"{'x':>8} | {'exp_manual':>16} | {'math.exp (ref)':>16} | {'selisih':>12}")
    print("-" * 60)
    for x in [-30, -10, -1, 0, 0.026, 1, 5, 10, 23, 30]:
        hasil_manual = exp_manual(x)
        hasil_ref = math.exp(x)
        selisih = abs(hasil_manual - hasil_ref)
        print(f"{x:>8} | {hasil_manual:>16.8e} | {hasil_ref:>16.8e} | {selisih:>12.2e}")

    print("\n=== Validasi sin_manual() vs math.sin() ===")
    print(f"{'x (rad)':>8} | {'sin_manual':>14} | {'math.sin (ref)':>14} | {'selisih':>12}")
    print("-" * 56)
    for x in [0, 0.1, 0.5, 1.0, math.pi/2, math.pi, 2*math.pi, 3.0, 6.0]:
        hasil_manual = sin_manual(x)
        hasil_ref = math.sin(x)
        selisih = abs(hasil_manual - hasil_ref)
        print(f"{x:>8.4f} | {hasil_manual:>14.8f} | {hasil_ref:>14.8f} | {selisih:>12.2e}")
