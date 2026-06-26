"""
manual_dc_bias.py
DC Bias Point rangkaian dioda - SEPENUHNYA MANUAL
(exp_manual untuk fungsi dioda, Newton-Raphson manual untuk solve).

Rangkaian: Vin --[R]-- V --[Diode]-- GND  (kapasitor diabaikan, statis)
KCL: (Vin - V)/R = Is*(exp(V/VT) - 1)
"""

from .manual_math import exp_manual

# Parameter rangkaian & dioda
R  = 1000.0
Is = 1e-12
VT = 0.026


def f(V, Vin):
    return (Vin - V) / R - Is * (exp_manual(V / VT) - 1)


def f_prime(V):
    # d/dV [ -Is*(exp(V/VT)-1) - V/R ] = -1/R - (Is/VT)*exp(V/VT)
    return -1.0 / R - (Is / VT) * exp_manual(V / VT)


def newton_raphson_dc_manual(Vin, V0=0.3, tol=1e-10, max_iter=100):
    V = V0
    for i in range(1, max_iter + 1):
        fV  = f(V, Vin)
        fpV = f_prime(V)
        V_baru = V - fV / fpV

        # Damping: batasi langkah Newton agar exp_manual tidak diberi
        # input yang melonjak terlalu jauh antar-iterasi
        langkah = V_baru - V
        langkah_maks = 0.5
        if abs(langkah) > langkah_maks:
            V_baru = V + langkah_maks * (1 if langkah > 0 else -1)

        if abs(V_baru - V) < tol:
            return V_baru, i
        V = V_baru
    raise RuntimeError(f"Tidak konvergen untuk Vin={Vin}")


if __name__ == "__main__":
    print(f"{'Vin (V)':>10} | {'V_diode (V)':>12} | {'I_diode (A)':>14} | {'Iterasi':>7}")
    print("-" * 52)
    for Vin in [0.5, 1.0, 2.0, 3.0, 5.0]:
        V_sol, n_iter = newton_raphson_dc_manual(Vin)
        I_sol = Is * (exp_manual(V_sol / VT) - 1)
        print(f"{Vin:>10.2f} | {V_sol:>12.6f} | {I_sol:>14.6e} | {n_iter:>7}")

    print("\n(Bandingkan dengan hasil Tahap 4 sebelumnya yang pakai np.exp -- harus identik)")
