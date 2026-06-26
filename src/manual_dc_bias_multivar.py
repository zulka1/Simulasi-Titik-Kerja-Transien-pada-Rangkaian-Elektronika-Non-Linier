"""
manual_dc_bias_multivar.py
DC Bias Point rangkaian dioda DUA NODE - SEPENUHNYA MANUAL
(exp_manual untuk fungsi dioda, gauss_eliminasi manual untuk solve JΔ=-F,
newton_raphson_multivar untuk iterasi Newton-Raphson beneran multivariabel).

Rangkaian (DC statis, tanpa kapasitor):

    Vin --[R1]--+-- V1 --[R2]--+-- V2
                 |               |
               [D1]            [D2]
                 |               |
                GND             GND

KCL di V1: (Vin-V1)/R1 = (V1-V2)/R2 + Is*(exp(V1/VT)-1)
KCL di V2: (V1-V2)/R2  = Is*(exp(V2/VT)-1)

Ditulis sebagai f1=0, f2=0:
    f1(V1,V2) = (Vin-V1)/R1 - (V1-V2)/R2 - Is*(exp(V1/VT)-1)
    f2(V1,V2) = (V1-V2)/R2  - Is*(exp(V2/VT)-1)

Jacobian (diturunkan manual di atas kertas, lihat laporan untuk detail):
    df1/dV1 = -1/R1 - 1/R2 - (Is/VT)*exp(V1/VT)
    df1/dV2 =  1/R2
    df2/dV1 =  1/R2
    df2/dV2 = -1/R2 - (Is/VT)*exp(V2/VT)

Catatan penting: off-diagonal Jacobian (df1/dV2 dan df2/dV1) TIDAK NOL.
Ini bukti bahwa kedua node benar-benar saling kopel -- Jacobian di sini
2x2 beneran (bukan dua persamaan independen yang dipaksa digabung).
"""

import numpy as np
from .manual_math import exp_manual
from .manual_newton import newton_raphson_multivar

# Parameter rangkaian & dioda
R1 = 1000.0
R2 = 2000.0
Is = 1e-12
VT = 0.026


def buat_F_func(Vin):
    """
    Mengembalikan fungsi F(V) = [f1, f2] untuk nilai Vin tertentu.
    Dipakai jika ingin memanggil newton_raphson_multivar() generik
    dari manual_newton.py secara langsung (lihat blok __main__ di bawah).
    """
    def F(V):
        V1, V2 = V[0], V[1]
        f1 = (Vin - V1) / R1 - (V1 - V2) / R2 - Is * (exp_manual(V1 / VT) - 1.0)
        f2 = (V1 - V2) / R2 - Is * (exp_manual(V2 / VT) - 1.0)
        return np.array([f1, f2])
    return F


def J_func(V):
    """Matriks Jacobian 2x2 di titik V=[V1,V2]."""
    V1, V2 = V[0], V[1]
    df1_dV1 = -1.0 / R1 - 1.0 / R2 - (Is / VT) * exp_manual(V1 / VT)
    df1_dV2 = 1.0 / R2
    df2_dV1 = 1.0 / R2
    df2_dV2 = -1.0 / R2 - (Is / VT) * exp_manual(V2 / VT)
    return np.array([[df1_dV1, df1_dV2],
                      [df2_dV1, df2_dV2]])


def newton_raphson_dc_multivar_manual(Vin, V0=(0.3, 0.3), tol=1e-10, max_iter=100, verbose=False):
    """
    Newton-Raphson multivariabel UNTUK rangkaian dua node, dengan damping
    (step-limiting) per komponen -- diperlukan karena fungsi dioda
    sangat curam (eksponensial), persis seperti versi 1-variabel sebelumnya.
    """
    V = np.array(V0, dtype=float)
    langkah_maks = 0.3

    for i in range(1, max_iter + 1):
        f1 = (Vin - V[0]) / R1 - (V[0] - V[1]) / R2 - Is * (exp_manual(V[0] / VT) - 1.0)
        f2 = (V[0] - V[1]) / R2 - Is * (exp_manual(V[1] / VT) - 1.0)
        Fx = np.array([f1, f2])
        Jx = J_func(V)

        from .manual_linalg import gauss_eliminasi
        minus_F = [-val for val in Fx]
        delta = gauss_eliminasi(Jx, minus_F)

        # Damping per komponen: batasi tiap elemen delta agar tidak
        # melonjak terlalu jauh antar-iterasi (sama alasannya dengan
        # versi 1-variabel: exp_manual akan diberi input ekstrem kalau
        # langkah Newton dibiarkan mentah).
        delta_clamped = np.array([
            max(min(d, langkah_maks), -langkah_maks) for d in delta
        ])

        V_baru = V + delta_clamped

        if verbose:
            print(f"  iter {i}: V1={V_baru[0]:.6f}, V2={V_baru[1]:.6f}, "
                  f"delta_raw={delta}, delta_clamped={delta_clamped}")

        norma_delta = (delta_clamped[0]**2 + delta_clamped[1]**2) ** 0.5
        if norma_delta < tol:
            return V_baru, i
        V = V_baru

    raise RuntimeError(f"Tidak konvergen untuk Vin={Vin}")


if __name__ == "__main__":
    print("=== DC Bias Point - Rangkaian Dua Node (Multivariabel) ===")
    print(f"R1={R1} ohm, R2={R2} ohm, Is={Is} A, VT={VT} V\n")

    print(f"{'Vin (V)':>10} | {'V1 (V)':>10} | {'V2 (V)':>10} | {'Iterasi':>7}")
    print("-" * 48)
    for Vin in [0.5, 1.0, 2.0, 3.0, 5.0]:
        (V1_sol, V2_sol), n_iter = newton_raphson_dc_multivar_manual(Vin)
        print(f"{Vin:>10.2f} | {V1_sol:>10.6f} | {V2_sol:>10.6f} | {n_iter:>7}")

    print("\n=== Detail iterasi untuk Vin = 2.0 V (verbose) ===")
    newton_raphson_dc_multivar_manual(2.0, verbose=True)

    print("\n--- Validasi Jacobian (cek manual vs hasil program) ---")
    V_test = np.array([0.5, 0.4])
    J_test = J_func(V_test)
    print(f"Di titik V1={V_test[0]}, V2={V_test[1]}:")
    print(f"J = \n{J_test}")
    print(f"Catatan: off-diagonal J[0][1]=J[1][0]={J_test[0][1]:.6e} (=1/R2={1/R2:.6e}) -- "
          f"konfirmasi kedua node saling kopel.")

    print("\n=== Validasi silang: pakai newton_raphson_multivar() generik dari manual_newton.py ===")
    print("(Fungsi ini sama persis dengan yang dipakai di Tahap 3 untuk sistem lingkaran-garis;")
    print(" dipakai ulang di sini tanpa modifikasi untuk membuktikan kode generik reusable)")
    Vin_uji = 2.0
    F_uji = buat_F_func(Vin_uji)
    (V_hasil, n_iter_uji) = newton_raphson_multivar(F_uji, J_func, x0=[0.3, 0.3])
    print(f"Vin={Vin_uji}: V1={V_hasil[0]:.6f}, V2={V_hasil[1]:.6f}, iterasi={n_iter_uji}")
    print("(Catatan: hasil bisa sedikit beda jumlah iterasi dari versi dengan damping di atas,")
    print(" karena newton_raphson_multivar() generik TIDAK punya damping -- ini risikonya")
    print(" untuk Vin besar/tebakan awal jauh, seperti dijelaskan di Tahap 4 sebelumnya.)")
