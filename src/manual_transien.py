"""
manual_transien.py
Simulasi Transien Rangkaian RC + Dioda - SEPENUHNYA MANUAL
(exp_manual, sin_manual, Newton-Raphson manual; numpy hanya untuk array storage).

Rangkaian:
    Vin(t) --[R]--+--[Diode]-- GND
                   |
                 [C]
                   |
                  GND

Vin(t) = Vm * sin(omega*t)
ODE:  dV/dt = (1/C) * [ (Vin(t)-V)/R - Is*(exp(V/VT)-1) ] = f(t, V)

Diselesaikan dengan Euler Implisit; persamaan non-linier di tiap step
diselesaikan dengan Newton-Raphson 1 variabel manual.
"""

import numpy as np
from .manual_math import exp_manual, sin_manual

# ---------------------------------------------------------
# Parameter rangkaian & dioda
# ---------------------------------------------------------
R  = 1000.0
C  = 1e-6
Is = 1e-12
VT = 0.026

# Parameter sumber sinus
Vm    = 5.0
freq  = 50.0
omega = 2 * 3.14159265358979323846 * freq   # 2*pi*f, pi ditulis manual (bukan np.pi)


def Vin(t):
    return Vm * sin_manual(omega * t)


def f(t, V):
    """dV/dt = f(t, V)"""
    return (1.0 / C) * ((Vin(t) - V) / R - Is * (exp_manual(V / VT) - 1.0))


def df_dV(t, V):
    """Turunan parsial f terhadap V"""
    return (1.0 / C) * (-1.0 / R - (Is / VT) * exp_manual(V / VT))


def newton_solve_step_manual(V_n, t_np1, dt, V_guess, tol=1e-10, max_iter=50):
    """
    Selesaikan g(V_new) = V_new - V_n - dt*f(t_np1, V_new) = 0
    dengan Newton-Raphson manual, termasuk damping.
    """
    V_baru = V_guess
    for _ in range(max_iter):
        g  = V_baru - V_n - dt * f(t_np1, V_baru)
        gp = 1.0 - dt * df_dV(t_np1, V_baru)
        delta = -g / gp

        langkah_maks = 0.5
        if abs(delta) > langkah_maks:
            delta = langkah_maks * (1 if delta > 0 else -1)

        V_baru += delta
        if abs(delta) < tol:
            return V_baru
    raise RuntimeError(f"Newton-Raphson tidak konvergen pada t={t_np1}")


def simulasi_transien_manual(t0, t_end, dt, V0=0.0):
    n_steps = int((t_end - t0) / dt)
    t_arr   = np.zeros(n_steps + 1)
    V_arr   = np.zeros(n_steps + 1)
    Vin_arr = np.zeros(n_steps + 1)

    t_arr[0]   = t0
    V_arr[0]   = V0
    Vin_arr[0] = Vin(t0)

    for n in range(n_steps):
        t_np1 = t_arr[n] + dt
        V_np1 = newton_solve_step_manual(V_arr[n], t_np1, dt, V_guess=V_arr[n])

        t_arr[n+1]   = t_np1
        V_arr[n+1]   = V_np1
        Vin_arr[n+1] = Vin(t_np1)

    return t_arr, V_arr, Vin_arr


if __name__ == "__main__":
    t0, t_end = 0.0, 0.06
    dt = 1e-5

    t_arr, V_arr, Vin_arr = simulasi_transien_manual(t0, t_end, dt, V0=0.0)

    print(f"Jumlah step: {len(t_arr)-1}")
    print(f"\n{'t (ms)':>10} | {'Vin (V)':>10} | {'V_node (V)':>12}")
    print("-" * 38)
    idx_sample = np.linspace(0, len(t_arr)-1, 15, dtype=int)
    for i in idx_sample:
        print(f"{t_arr[i]*1000:>10.3f} | {Vin_arr[i]:>10.4f} | {V_arr[i]:>12.6f}")

    print("\n(Bandingkan dengan hasil Tahap 7 sebelumnya yang pakai np.exp/np.sin -- harus identik/sangat dekat)")
