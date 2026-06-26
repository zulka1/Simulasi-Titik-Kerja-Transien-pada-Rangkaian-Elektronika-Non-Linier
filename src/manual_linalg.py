"""
manual_linalg.py
Solver sistem linier A*x = b menggunakan Gauss Elimination MANUAL
dengan partial pivoting. TIDAK menggunakan np.linalg.solve atau solver
library lain. numpy hanya dipakai sebagai struktur array (bukan fungsi
matematika/solver siap pakai).
"""

import numpy as np

def gauss_eliminasi(A, b):
    """
    Selesaikan sistem A*x = b secara manual.

    Parameter:
        A : array 2D (n x n) - matriks koefisien
        b : array 1D (n)     - vektor ruas kanan

    Return:
        x : array 1D (n) - solusi sistem

    Algoritma:
        1. Forward elimination dengan partial pivoting
           (tukar baris agar elemen pivot adalah yang terbesar
           magnitudonya di kolom tersebut -> stabilitas numerik)
        2. Back substitution
    """
    n = len(b)
    # Buat copy agar matriks input asli tidak berubah (augmented matrix)
    M = np.array(A, dtype=float).copy()
    v = np.array(b, dtype=float).copy()

    # --- 1. FORWARD ELIMINATION dengan PARTIAL PIVOTING ---
    for k in range(n - 1):
        # Cari baris dengan |elemen| terbesar di kolom k, mulai dari baris k ke bawah
        baris_pivot = k
        nilai_maks = abs(M[k][k])
        for i in range(k + 1, n):
            if abs(M[i][k]) > nilai_maks:
                nilai_maks = abs(M[i][k])
                baris_pivot = i

        if nilai_maks < 1e-14:
            raise ValueError("Matriks singular atau hampir singular, tidak ada solusi unik.")

        # Tukar baris k dengan baris_pivot jika perlu
        if baris_pivot != k:
            M[[k, baris_pivot]] = M[[baris_pivot, k]]
            v[k], v[baris_pivot] = v[baris_pivot], v[k]

        # Eliminasi elemen di bawah pivot pada kolom k
        for i in range(k + 1, n):
            faktor = M[i][k] / M[k][k]
            for j in range(k, n):
                M[i][j] -= faktor * M[k][j]
            v[i] -= faktor * v[k]

    # --- 2. BACK SUBSTITUTION ---
    x = np.zeros(n)
    for i in range(n - 1, -1, -1):
        sigma = 0.0
        for j in range(i + 1, n):
            sigma += M[i][j] * x[j]
        if abs(M[i][i]) < 1e-14:
            raise ValueError("Pivot mendekati nol pada back substitution.")
        x[i] = (v[i] - sigma) / M[i][i]

    return x

if __name__ == "__main__":
    print("=== Validasi gauss_eliminasi() ===\n")

    # Kasus uji sama dengan Tahap 3: hasil J*delta = -F untuk sistem
    # x^2+y^2=4, x-y=0 pada titik (1.0, 0.5)
    # J = [[2x, 2y], [1, -1]] = [[2.0, 1.0], [1, -1]]
    # F = [1^2+0.5^2-4, 1-0.5] = [-2.75, 0.5]
    J = [[2.0, 1.0],
         [1.0, -1.0]]
    F = [-2.75, 0.5]
    minus_F = [-f for f in F]

    delta = gauss_eliminasi(J, minus_F)
    print(f"J = {J}")
    print(f"-F = {minus_F}")
    print(f"Solusi delta (manual)   : {delta}")

    # Bandingkan dengan numpy.linalg.solve (HANYA untuk validasi, bukan dipakai di program utama)
    delta_ref = np.linalg.solve(np.array(J), np.array(minus_F))
    print(f"Solusi delta (referensi): {delta_ref}")
    print(f"Selisih max             : {np.max(np.abs(delta - delta_ref)):.2e}")

    print("\n--- Uji sistem 3x3 ---")
    A3 = [[2, 1, -1],
          [-3, -1, 2],
          [-2, 1, 2]]
    b3 = [8, -11, -3]
    x3 = gauss_eliminasi(A3, b3)
    x3_ref = np.linalg.solve(np.array(A3, dtype=float), np.array(b3, dtype=float))
    print(f"Solusi manual    : {x3}")
    print(f"Solusi referensi : {x3_ref}")
    print(f"Selisih max      : {np.max(np.abs(x3 - x3_ref)):.2e}")
