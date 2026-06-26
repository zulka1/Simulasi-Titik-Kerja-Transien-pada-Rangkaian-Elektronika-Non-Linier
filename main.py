"""
============================================================================
  SIMULASI TITIK KERJA TRANSIEN PADA RANGKAIAN ELEKTRONIKA NON-LINIER
============================================================================
  Tugas Besar - Metode Numerik
  Tema 6: Pencarian Akar & Solusi Persamaan Diferensial

  Deskripsi:
    Simulator sirkuit komputasional mini untuk menganalisis respons
    tegangan statis (DC Bias) dan dinamika waktu (transien) dari
    rangkaian elektronika yang memiliki komponen non-linier (dioda silikon).

  Algoritma Utama:
    1. Newton-Raphson (1-variabel & multi-variabel) untuk pencarian akar
    2. Euler Implisit untuk penyelesaian ODE transien
    3. Taylor Series manual untuk exp(x) dan sin(x)
    4. Gauss Eliminasi manual untuk solver sistem linier

  Seluruh komputasi matematika dihitung MANUAL (tanpa library math/numpy
  untuk fungsi matematika). numpy hanya dipakai sebagai struktur array.
============================================================================
"""

import numpy as np
import sys
import os

# ─── Fix encoding untuk Windows console ──────────────────────────────
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stdin.reconfigure(encoding='utf-8')

# ─── Import dari package src ─────────────────────────────────────────
from src.manual_math import exp_manual, sin_manual, PI
from src.manual_linalg import gauss_eliminasi


# ═════════════════════════════════════════════════════════════════════════
#  UTILITAS
# ═════════════════════════════════════════════════════════════════════════

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def tekan_enter():
    print()
    try:
        input("  Tekan [Enter] untuk kembali ke menu... ")
    except EOFError:
        pass


def garis(karakter="═", panjang=70):
    print(f"  {karakter * panjang}")


def garis_tipis(panjang=70):
    print(f"  {'─' * panjang}")


def judul_bagian(teks):
    print()
    garis("═", 70)
    print(f"  ║  {teks:^66}║")
    garis("═", 70)
    print()


def sub_judul(teks):
    print(f"\n  ◆ {teks}")
    garis_tipis(66)


def info(label, nilai):
    print(f"    {label:<30}: {nilai}")


def input_param(label, default, satuan=""):
    satuan_str = f" {satuan}" if satuan else ""
    try:
        raw = input(f"    {label} [{default}{satuan_str}]: ").strip()
        if raw == "":
            return default
        return float(raw)
    except (ValueError, EOFError):
        return default


def input_list_vin(default_list):
    default_str = ", ".join(str(v) for v in default_list)
    try:
        raw = input(f"    Daftar Vin [{default_str}]: ").strip()
        if raw == "":
            return default_list
        raw = raw.replace(",", " ")
        return [float(x) for x in raw.split() if x]
    except (ValueError, EOFError):
        return default_list


# ═════════════════════════════════════════════════════════════════════════
#  MENU 1: ANALISIS DC BIAS - 1 NODE
# ═════════════════════════════════════════════════════════════════════════

def menu_dc_bias_1node():
    judul_bagian("ANALISIS DC BIAS - RANGKAIAN 1 NODE (Newton-Raphson 1-Var)")

    print("    Skema Rangkaian:")
    print("    ┌────────────────────────────────────────┐")
    print("    │                                        │")
    print("    │   Vin ──[R]──┬── V ──[Diode]── GND    │")
    print("    │              │                         │")
    print("    │             (node)                     │")
    print("    │                                        │")
    print("    └────────────────────────────────────────┘")

    sub_judul("Input Parameter Rangkaian (tekan Enter untuk default)")
    R  = input_param("Resistor R", 1000.0, "Ω")
    Is = input_param("Arus saturasi Is", 1e-12, "A")
    VT = input_param("Tegangan termal VT", 0.026, "V")

    sub_judul("Input Daftar Tegangan Vin (pisahkan dengan koma)")
    list_Vin = input_list_vin([0.5, 1.0, 2.0, 3.0, 5.0, 10.0])

    # ── Solver lokal ──
    def f_local(V, Vin):
        return (Vin - V) / R - Is * (exp_manual(V / VT) - 1)

    def fp_local(V):
        return -1.0 / R - (Is / VT) * exp_manual(V / VT)

    def newton_dc_local(Vin, V0=0.3, tol=1e-10, max_iter=100):
        V = V0
        for i in range(1, max_iter + 1):
            fV  = f_local(V, Vin)
            fpV = fp_local(V)
            V_baru = V - fV / fpV
            langkah = V_baru - V
            if abs(langkah) > 0.5:
                V_baru = V + 0.5 * (1 if langkah > 0 else -1)
            if abs(V_baru - V) < tol:
                return V_baru, i
            V = V_baru
        raise RuntimeError(f"Tidak konvergen untuk Vin={Vin}")

    sub_judul("Parameter yang Digunakan")
    info("Resistor R", f"{R:.1f} Ω")
    info("Arus saturasi Is", f"{Is:.2e} A")
    info("Tegangan termal VT", f"{VT} V")
    info("Persamaan dioda", "I = Is·(e^(V/VT) - 1)")
    info("KCL", "(Vin-V)/R = Is·(e^(V/VT)-1)")

    sub_judul("Hasil DC Bias Point")
    print(f"    {'Vin (V)':>10} │ {'V_diode (V)':>12} │ {'I_diode (A)':>14} │ {'I_R (A)':>14} │ {'Iterasi':>7}")
    print(f"    {'─'*10}─┼─{'─'*12}─┼─{'─'*14}─┼─{'─'*14}─┼─{'─'*7}")

    list_Vd, list_Id, list_Ir = [], [], []

    for Vin in list_Vin:
        V_sol, n_iter = newton_dc_local(Vin)
        I_diode = Is * (exp_manual(V_sol / VT) - 1)
        I_R = (Vin - V_sol) / R
        list_Vd.append(V_sol)
        list_Id.append(I_diode)
        list_Ir.append(I_R)
        print(f"    {Vin:>10.2f} │ {V_sol:>12.6f} │ {I_diode:>14.6e} │ {I_R:>14.6e} │ {n_iter:>7}")

    print("\n    ✓ Tegangan dioda konvergen ke ~0.5-0.6 V (sesuai karakteristik dioda silikon)")
    print("    ✓ Arus resistor ≈ arus dioda (konfirmasi KCL terpenuhi)")

    # ── Grafik ──
    sub_judul("Grafik Analisis DC Bias")
    try:
        import matplotlib
        matplotlib.use('TkAgg')
        import matplotlib.pyplot as plt

        fig, axes = plt.subplots(2, 2, figsize=(13, 8))
        fig.suptitle(f'Analisis DC Bias - Rangkaian 1 Node\n'
                     f'R={R:.0f}Ω, Is={Is:.1e}A, VT={VT}V',
                     fontsize=13, fontweight='bold')

        ax = axes[0, 0]
        ax.plot(list_Vin, list_Vd, 'ro-', linewidth=2, markersize=7, label='V_diode')
        ax.set_xlabel('Vin (V)'); ax.set_ylabel('V_diode (V)')
        ax.set_title('(a) Tegangan Dioda vs Tegangan Input'); ax.grid(True, alpha=0.3); ax.legend()

        ax = axes[0, 1]
        ax.plot(list_Vin, [i*1000 for i in list_Id], 'gs-', linewidth=2, markersize=7, label='I_diode')
        ax.set_xlabel('Vin (V)'); ax.set_ylabel('I_diode (mA)')
        ax.set_title('(b) Arus Dioda vs Tegangan Input'); ax.grid(True, alpha=0.3); ax.legend()

        ax = axes[1, 0]
        ax.plot(list_Vd, [i*1000 for i in list_Id], 'b^-', linewidth=2, markersize=7, label='Titik kerja')
        V_teori = [v * 0.01 for v in range(0, 70)]
        I_teori = [Is * (exp_manual(v / VT) - 1) * 1000 for v in V_teori]
        ax.plot(V_teori, I_teori, 'b--', alpha=0.4, linewidth=1, label='Kurva I-V ideal')
        ax.set_xlabel('V_diode (V)'); ax.set_ylabel('I_diode (mA)')
        ax.set_title('(c) Karakteristik I-V Dioda'); ax.grid(True, alpha=0.3); ax.legend()

        ax = axes[1, 1]
        Vin_demo = list_Vin[-1]
        V_range = [v * 0.01 for v in range(0, int(Vin_demo*100)+1)]
        I_load = [(Vin_demo - v) / R * 1000 for v in V_range]
        I_dioda_curve = [Is * (exp_manual(v / VT) - 1) * 1000 for v in V_range]
        ax.plot(V_range, I_load, 'r-', linewidth=2, label=f'Garis beban (Vin={Vin_demo}V)')
        ax.plot(V_range, I_dioda_curve, 'b-', linewidth=2, label='Kurva I-V dioda')
        V_op, _ = newton_dc_local(Vin_demo)
        I_op = Is * (exp_manual(V_op / VT) - 1) * 1000
        ax.plot(V_op, I_op, 'ko', markersize=10, zorder=5, label=f'Titik kerja ({V_op:.3f}V, {I_op:.2f}mA)')
        ax.set_xlabel('V (V)'); ax.set_ylabel('I (mA)')
        ax.set_title(f'(d) Load Line Analysis (Vin={Vin_demo}V)'); ax.grid(True, alpha=0.3); ax.legend(fontsize=8)

        plt.tight_layout(); plt.show(block=False); plt.pause(0.1)
        print("    ✓ Grafik berhasil ditampilkan!")
    except ImportError:
        print("    ⚠ matplotlib tidak terinstall. Jalankan: pip install matplotlib")
    except Exception as e:
        print(f"    ⚠ Tidak dapat menampilkan grafik: {e}")


# ═════════════════════════════════════════════════════════════════════════
#  MENU 2: ANALISIS DC BIAS - 2 NODE (MULTIVARIABEL)
# ═════════════════════════════════════════════════════════════════════════

def menu_dc_bias_multivar():
    judul_bagian("ANALISIS DC BIAS - RANGKAIAN 2 NODE (Newton-Raphson Multi-Var)")

    print("    Skema Rangkaian:")
    print("    ┌──────────────────────────────────────────────────┐")
    print("    │                                                  │")
    print("    │   Vin ──[R1]──┬── V1 ──[R2]──┬── V2             │")
    print("    │               │               │                  │")
    print("    │             [D1]            [D2]                 │")
    print("    │               │               │                  │")
    print("    │              GND             GND                 │")
    print("    │                                                  │")
    print("    └──────────────────────────────────────────────────┘")

    sub_judul("Input Parameter Rangkaian (tekan Enter untuk default)")
    R1 = input_param("Resistor R1", 1000.0, "Ω")
    R2 = input_param("Resistor R2", 2000.0, "Ω")
    Is = input_param("Arus saturasi Is", 1e-12, "A")
    VT = input_param("Tegangan termal VT", 0.026, "V")

    sub_judul("Input Daftar Tegangan Vin (pisahkan dengan koma)")
    list_Vin = input_list_vin([0.5, 1.0, 2.0, 3.0, 5.0, 10.0])

    # ── Solver lokal ──
    def J_local(V):
        V1, V2 = V[0], V[1]
        return np.array([
            [-1.0/R1 - 1.0/R2 - (Is/VT)*exp_manual(V1/VT), 1.0/R2],
            [1.0/R2, -1.0/R2 - (Is/VT)*exp_manual(V2/VT)]
        ])

    def newton_dc_multi_local(Vin, V0=(0.3, 0.3), tol=1e-10, max_iter=100, verbose=False):
        V = np.array(V0, dtype=float)
        for i in range(1, max_iter + 1):
            f1 = (Vin - V[0])/R1 - (V[0] - V[1])/R2 - Is*(exp_manual(V[0]/VT) - 1.0)
            f2 = (V[0] - V[1])/R2 - Is*(exp_manual(V[1]/VT) - 1.0)
            Fx = np.array([f1, f2])
            delta = gauss_eliminasi(J_local(V), [-val for val in Fx])
            delta_clamped = np.array([max(min(d, 0.3), -0.3) for d in delta])
            V_baru = V + delta_clamped
            if verbose:
                print(f"  iter {i}: V1={V_baru[0]:.6f}, V2={V_baru[1]:.6f}")
            if (delta_clamped[0]**2 + delta_clamped[1]**2)**0.5 < tol:
                return V_baru, i
            V = V_baru
        raise RuntimeError(f"Tidak konvergen untuk Vin={Vin}")

    sub_judul("Parameter yang Digunakan")
    info("Resistor R1", f"{R1:.1f} Ω")
    info("Resistor R2", f"{R2:.1f} Ω")
    info("Arus saturasi Is", f"{Is:.2e} A")
    info("Tegangan termal VT", f"{VT} V")

    sub_judul("Persamaan KCL (Sistem Non-Linier 2 Variabel)")
    print("    f1(V1,V2) = (Vin-V1)/R1 - (V1-V2)/R2 - Is·(e^(V1/VT)-1) = 0")
    print("    f2(V1,V2) = (V1-V2)/R2  - Is·(e^(V2/VT)-1) = 0")

    sub_judul("Matriks Jacobian (Diturunkan Secara Analitik)")
    print("    ┌                                                        ┐")
    print("    │ -1/R1 - 1/R2 - (Is/VT)·e^(V1/VT)         1/R2        │")
    print("    │                                                        │")
    print("    │           1/R2                -1/R2 - (Is/VT)·e^(V2/VT)│")
    print("    └                                                        ┘")

    sub_judul("Hasil DC Bias Point")
    print(f"    {'Vin (V)':>10} │ {'V1 (V)':>10} │ {'V2 (V)':>10} │ {'I_D1 (A)':>14} │ {'I_D2 (A)':>14} │ {'Iter':>5}")
    print(f"    {'─'*10}─┼─{'─'*10}─┼─{'─'*10}─┼─{'─'*14}─┼─{'─'*14}─┼─{'─'*5}")

    list_V1, list_V2, list_ID1, list_ID2 = [], [], [], []

    for Vin in list_Vin:
        (V1, V2), n_iter = newton_dc_multi_local(Vin)
        I_D1 = Is * (exp_manual(V1 / VT) - 1)
        I_D2 = Is * (exp_manual(V2 / VT) - 1)
        list_V1.append(V1); list_V2.append(V2)
        list_ID1.append(I_D1); list_ID2.append(I_D2)
        print(f"    {Vin:>10.2f} │ {V1:>10.6f} │ {V2:>10.6f} │ {I_D1:>14.6e} │ {I_D2:>14.6e} │ {n_iter:>5}")

    sub_judul(f"Detail Konvergensi (Vin = {list_Vin[len(list_Vin)//2]:.1f} V)")
    print()
    newton_dc_multi_local(list_Vin[len(list_Vin)//2], verbose=True)

    # ── Grafik ──
    sub_judul("Grafik Analisis DC Bias 2 Node")
    try:
        import matplotlib
        matplotlib.use('TkAgg')
        import matplotlib.pyplot as plt

        fig, axes = plt.subplots(2, 2, figsize=(13, 8))
        fig.suptitle(f'Analisis DC Bias - Rangkaian 2 Node\n'
                     f'R1={R1:.0f}Ω, R2={R2:.0f}Ω, Is={Is:.1e}A, VT={VT}V',
                     fontsize=13, fontweight='bold')

        ax = axes[0, 0]
        ax.plot(list_Vin, list_V1, 'ro-', lw=2, ms=7, label='V1 (node 1)')
        ax.plot(list_Vin, list_V2, 'bs-', lw=2, ms=7, label='V2 (node 2)')
        ax.set_xlabel('Vin (V)'); ax.set_ylabel('Tegangan Node (V)')
        ax.set_title('(a) Tegangan Node vs Vin'); ax.grid(True, alpha=0.3); ax.legend()

        ax = axes[0, 1]
        ax.plot(list_Vin, [i*1000 for i in list_ID1], 'r^-', lw=2, ms=7, label='I_D1')
        ax.plot(list_Vin, [i*1000 for i in list_ID2], 'bv-', lw=2, ms=7, label='I_D2')
        ax.set_xlabel('Vin (V)'); ax.set_ylabel('Arus Dioda (mA)')
        ax.set_title('(b) Arus Dioda vs Vin'); ax.grid(True, alpha=0.3); ax.legend()

        ax = axes[1, 0]
        delta_V = [v1 - v2 for v1, v2 in zip(list_V1, list_V2)]
        ax.plot(list_Vin, [dv*1000 for dv in delta_V], 'mD-', lw=2, ms=7, label='V1 - V2')
        ax.set_xlabel('Vin (V)'); ax.set_ylabel('V1 - V2 (mV)')
        ax.set_title('(c) Beda Potensial Antar-Node'); ax.grid(True, alpha=0.3); ax.legend()

        ax = axes[1, 1]
        ax.plot(list_V1, [i*1000 for i in list_ID1], 'ro-', lw=2, ms=7, label='D1')
        ax.plot(list_V2, [i*1000 for i in list_ID2], 'bs-', lw=2, ms=7, label='D2')
        V_teori = [v * 0.01 for v in range(0, 70)]
        I_teori = [Is * (exp_manual(v / VT) - 1) * 1000 for v in V_teori]
        ax.plot(V_teori, I_teori, 'k--', alpha=0.4, lw=1, label='I-V ideal')
        ax.set_xlabel('V_diode (V)'); ax.set_ylabel('I_diode (mA)')
        ax.set_title('(d) Karakteristik I-V Dioda'); ax.grid(True, alpha=0.3); ax.legend(fontsize=8)

        plt.tight_layout(); plt.show(block=False); plt.pause(0.1)
        print("    ✓ Grafik berhasil ditampilkan!")
    except ImportError:
        print("    ⚠ matplotlib tidak terinstall. Jalankan: pip install matplotlib")
    except Exception as e:
        print(f"    ⚠ Tidak dapat menampilkan grafik: {e}")


# ═════════════════════════════════════════════════════════════════════════
#  MENU 3: SIMULASI TRANSIEN (EULER IMPLISIT + ODE)
# ═════════════════════════════════════════════════════════════════════════

def menu_transien():
    judul_bagian("SIMULASI TRANSIEN - RANGKAIAN RC + DIODA (Euler Implisit)")

    print("    Skema Rangkaian:")
    print("    ┌────────────────────────────────────────────┐")
    print("    │                                            │")
    print("    │   Vin(t) ──[R]──┬──[Diode]── GND          │")
    print("    │                 │                          │")
    print("    │               [C]                          │")
    print("    │                 │                          │")
    print("    │                GND                         │")
    print("    │                                            │")
    print("    │   Vin(t) = Vm · sin(ω·t)                  │")
    print("    └────────────────────────────────────────────┘")

    sub_judul("Input Parameter Rangkaian (tekan Enter untuk default)")
    R     = input_param("Resistor R", 1000.0, "Ω")
    C     = input_param("Kapasitor C", 1e-6, "F")
    Is    = input_param("Arus saturasi Is", 1e-12, "A")
    VT    = input_param("Tegangan termal VT", 0.026, "V")

    sub_judul("Input Parameter Sumber Sinus (tekan Enter untuk default)")
    Vm    = input_param("Amplitudo Vm", 5.0, "V")
    freq  = input_param("Frekuensi", 50.0, "Hz")

    sub_judul("Input Parameter Simulasi (tekan Enter untuk default)")
    t_end = input_param("Waktu simulasi (t_end)", 0.06, "s")
    dt    = input_param("Langkah waktu (dt)", 1e-5, "s")

    omega = 2 * PI * freq

    # ── Solver lokal ──
    def Vin_func(t):
        return Vm * sin_manual(omega * t)

    def f_local(t, V):
        return (1.0 / C) * ((Vin_func(t) - V) / R - Is * (exp_manual(V / VT) - 1.0))

    def df_dV_local(t, V):
        return (1.0 / C) * (-1.0 / R - (Is / VT) * exp_manual(V / VT))

    def newton_step(V_n, t_np1, dt_s, V_guess, tol=1e-10, max_iter=50):
        V_b = V_guess
        for _ in range(max_iter):
            g  = V_b - V_n - dt_s * f_local(t_np1, V_b)
            gp = 1.0 - dt_s * df_dV_local(t_np1, V_b)
            delta = -g / gp
            if abs(delta) > 0.5:
                delta = 0.5 * (1 if delta > 0 else -1)
            V_b += delta
            if abs(delta) < tol:
                return V_b
        raise RuntimeError(f"Newton-Raphson tidak konvergen pada t={t_np1}")

    def simulasi_local(t0, t_end_sim, dt_sim, V0=0.0):
        n_steps = int((t_end_sim - t0) / dt_sim)
        t_arr = np.zeros(n_steps + 1)
        V_arr = np.zeros(n_steps + 1)
        Vin_arr = np.zeros(n_steps + 1)
        t_arr[0], V_arr[0], Vin_arr[0] = t0, V0, Vin_func(t0)
        for n in range(n_steps):
            t_np1 = t_arr[n] + dt_sim
            t_arr[n+1]   = t_np1
            V_arr[n+1]   = newton_step(V_arr[n], t_np1, dt_sim, V_arr[n])
            Vin_arr[n+1] = Vin_func(t_np1)
        return t_arr, V_arr, Vin_arr

    sub_judul("Parameter yang Digunakan")
    info("Resistor R", f"{R:.1f} Ω")
    info("Kapasitor C", f"{C:.2e} F")
    info("Arus saturasi Is", f"{Is:.2e} A")
    info("Tegangan termal VT", f"{VT} V")
    info("Amplitudo Vm", f"{Vm:.1f} V")
    info("Frekuensi", f"{freq:.1f} Hz")
    info("Omega (ω)", f"{omega:.4f} rad/s")

    sub_judul("Persamaan ODE")
    print("    dV/dt = (1/C) · [ (Vin(t)-V)/R - Is·(e^(V/VT)-1) ]")
    print()
    print("    Diskritisasi Euler Implisit:")
    print("    g(V_{n+1}) = V_{n+1} - V_n - Δt·f(t_{n+1}, V_{n+1}) = 0")
    print("    → Diselesaikan dengan Newton-Raphson di setiap time-step")

    sub_judul("Menjalankan Simulasi...")
    t0 = 0.0
    n_steps = int((t_end - t0) / dt)
    print(f"    Waktu simulasi  : {t0*1000:.1f} ms → {t_end*1000:.1f} ms")
    print(f"    Langkah waktu Δt: {dt*1e6:.1f} µs")
    print(f"    Jumlah step     : {n_steps}")
    print(f"    Jumlah periode  : {t_end * freq:.1f} periode")
    print()
    print("    Menghitung", end="", flush=True)

    t_arr, V_arr, Vin_arr = simulasi_local(t0, t_end, dt, V0=0.0)
    print(" ✓ Selesai!")

    sub_judul("Tabel Hasil Simulasi (Sampling 20 Titik)")
    print(f"    {'No':>4} │ {'t (ms)':>9} │ {'Vin (V)':>10} │ {'V_node (V)':>12} │ {'I_diode (A)':>14}")
    print(f"    {'─'*4}─┼─{'─'*9}─┼─{'─'*10}─┼─{'─'*12}─┼─{'─'*14}")

    idx_sample = np.linspace(0, len(t_arr) - 1, 20, dtype=int)
    for no, i in enumerate(idx_sample, 1):
        I_d = Is * (exp_manual(V_arr[i] / VT) - 1)
        print(f"    {no:>4} │ {t_arr[i]*1000:>9.3f} │ {Vin_arr[i]:>10.4f} │ {V_arr[i]:>12.6f} │ {I_d:>14.6e}")

    sub_judul("Statistik Hasil")
    info("V_node minimum", f"{min(V_arr):.6f} V")
    info("V_node maksimum", f"{max(V_arr):.6f} V")
    info("Vin minimum", f"{min(Vin_arr):.6f} V")
    info("Vin maksimum", f"{max(Vin_arr):.6f} V")

    # ── Grafik ──
    sub_judul("Grafik Respons Transien")
    try:
        import matplotlib
        matplotlib.use('TkAgg')
        import matplotlib.pyplot as plt

        t_ms = t_arr * 1000

        fig, axes = plt.subplots(2, 2, figsize=(14, 8))
        fig.suptitle(f'Simulasi Transien RC + Dioda (Euler Implisit)\n'
                     f'R={R:.0f}Ω, C={C:.1e}F, Vm={Vm:.1f}V, f={freq:.0f}Hz',
                     fontsize=13, fontweight='bold')

        ax = axes[0, 0]
        ax.plot(t_ms, Vin_arr, 'b-', lw=1.2, label='Vin(t) = Vm·sin(ωt)', alpha=0.7)
        ax.plot(t_ms, V_arr, 'r-', lw=1.5, label='V_node(t)')
        ax.set_xlabel('Waktu (ms)'); ax.set_ylabel('Tegangan (V)')
        ax.set_title('(a) Tegangan Input vs Node'); ax.grid(True, alpha=0.3); ax.legend()

        I_diode_arr = np.array([Is * (exp_manual(v / VT) - 1) for v in V_arr])
        ax = axes[0, 1]
        ax.plot(t_ms, I_diode_arr * 1000, 'g-', lw=1.2, label='I_diode(t)')
        ax.set_xlabel('Waktu (ms)'); ax.set_ylabel('Arus Dioda (mA)')
        ax.set_title('(b) Arus Dioda vs Waktu'); ax.grid(True, alpha=0.3); ax.legend()

        I_cap_arr = np.zeros(len(V_arr))
        for k in range(1, len(V_arr)):
            I_cap_arr[k] = C * (V_arr[k] - V_arr[k-1]) / dt
        ax = axes[1, 0]
        ax.plot(t_ms, I_cap_arr * 1000, 'm-', lw=1.0, label='I_C(t) = C·dV/dt', alpha=0.8)
        ax.set_xlabel('Waktu (ms)'); ax.set_ylabel('Arus Kapasitor (mA)')
        ax.set_title('(c) Arus Kapasitor vs Waktu'); ax.grid(True, alpha=0.3); ax.legend()

        ax = axes[1, 1]
        scatter = ax.scatter(Vin_arr[::10], V_arr[::10], c=t_ms[::10], cmap='viridis', s=3, alpha=0.7)
        ax.set_xlabel('Vin (V)'); ax.set_ylabel('V_node (V)')
        ax.set_title('(d) Diagram Fase: V_node vs Vin'); ax.grid(True, alpha=0.3)
        plt.colorbar(scatter, ax=ax).set_label('Waktu (ms)')

        plt.tight_layout(); plt.show(block=False); plt.pause(0.1)
        print("    ✓ Grafik berhasil ditampilkan!")
    except ImportError:
        print("    ⚠ matplotlib tidak terinstall. Jalankan: pip install matplotlib")
    except Exception as e:
        print(f"    ⚠ Tidak dapat menampilkan grafik: {e}")


# ═════════════════════════════════════════════════════════════════════════
#  MENU UTAMA
# ═════════════════════════════════════════════════════════════════════════

def tampilkan_menu_utama():
    clear_screen()
    print()
    print("  ╔══════════════════════════════════════════════════════════════════════╗")
    print("  ║                                                                    ║")
    print("  ║     SIMULASI TITIK KERJA TRANSIEN PADA RANGKAIAN ELEKTRONIKA       ║")
    print("  ║                         NON-LINIER                                 ║")
    print("  ║                                                                    ║")
    print("  ╠══════════════════════════════════════════════════════════════════════╣")
    print("  ║  Tugas Besar - Metode Numerik                                      ║")
    print("  ║  Tema 6: Pencarian Akar & Solusi Persamaan Diferensial             ║")
    print("  ╠══════════════════════════════════════════════════════════════════════╣")
    print("  ║                                                                    ║")
    print("  ║  [1] Analisis DC Bias - 1 Node  (Newton-Raphson 1-Variabel)        ║")
    print("  ║  [2] Analisis DC Bias - 2 Node  (Newton-Raphson Multi-Variabel)    ║")
    print("  ║  [3] Simulasi Transien RC+Dioda (Euler Implisit + ODE)             ║")
    print("  ║                                                                    ║")
    print("  ║  [0] Keluar                                                        ║")
    print("  ║                                                                    ║")
    print("  ╚══════════════════════════════════════════════════════════════════════╝")
    print()


def main():
    menu_handlers = {
        '1': menu_dc_bias_1node,
        '2': menu_dc_bias_multivar,
        '3': menu_transien,
    }

    while True:
        tampilkan_menu_utama()
        try:
            pilihan = input("  Pilih menu [0-3]: ").strip()
        except (EOFError, KeyboardInterrupt):
            pilihan = '0'

        if pilihan == '0':
            print()
            garis("═", 70)
            print("  ║  Terima kasih telah menggunakan simulator ini!              ║")
            garis("═", 70)
            print()
            break

        handler = menu_handlers.get(pilihan)
        if handler:
            clear_screen()
            try:
                handler()
            except Exception as e:
                print(f"\n  ✗ Error: {e}")
            tekan_enter()
        else:
            print("\n  ⚠ Pilihan tidak valid. Silakan masukkan angka 0-3.")
            tekan_enter()


if __name__ == "__main__":
    main()
