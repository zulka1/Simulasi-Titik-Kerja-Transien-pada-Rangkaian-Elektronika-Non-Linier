## Simulasi Titik Kerja Transien pada Rangkaian Elektronika Non-Linier

===



Number of team : 3

Member :

1. Ubaidullah Zulkarnain   			105224024
2. Muhammad Rafly 				105224040
3. Yusuf Rizky Nugroho 				105224012



&#x20;



Metode numerik digunakan untuk menyelesaikan masalah matematika yang sulit diselesaikan secara analitik. Dalam bidang elektronika, salah satu contoh permasalahan tersebut adalah analisis rangkaian non-linier. Rangkaian non-linier dapat menghasilkan persamaan yang kompleks karena hubungan antara arus dan tegangannya tidak selalu sebanding.

Pada proyek ini, komponen non-linier yang digunakan adalah dioda. Dioda memiliki karakteristik arus-tegangan yang berbentuk eksponensial, sehingga analisis titik kerja DC rangkaian dapat menghasilkan sistem persamaan non-linier. Untuk menyelesaikan sistem tersebut digunakan metode Newton-Raphson multivariabel dengan bantuan matriks Jacobian.

Selain titik kerja DC, proyek ini juga membahas respons transien pada rangkaian RC-dioda. Karena terdapat kapasitor, perubahan tegangan terhadap waktu dimodelkan sebagai persamaan diferensial biasa. Persamaan tersebut diselesaikan menggunakan metode Euler Implisit, dan persamaan non-linier pada setiap langkah waktunya diselesaikan kembali menggunakan Newton-Raphson.







## TEST \& RESULT



1. &#x20;



Pilih menu \[0-3]: 1



◆ Input Parameter Rangkaian (tekan Enter untuk default)

&#x20;   Resistor R \[1000.0 Ω]: 2200          ← ganti R jadi 2200 ohm

&#x20;   Arus saturasi Is \[1e-12 A]:          ← tekan Enter (pakai default 1e-12)

&#x20;   Tegangan termal VT \[0.026 V]:        ← tekan Enter (pakai default 0.026)



◆ Input Daftar Tegangan Vin (pisahkan dengan koma)

&#x20;   Daftar Vin \[0.5, 1.0, 2.0, 3.0, 5.0, 10.0]: 1, 3, 5, 7, 12

&#x20;                                                  ↑ custom 5 nilai Vin

&#x20;◆ Parameter yang Digunakan

&#x20; ──────────────────────────────────────────────────────────────────

&#x20;   Resistor R                    : 2200.0 Ω

&#x20;   Arus saturasi Is              : 1.00e-12 A

&#x20;   Tegangan termal VT            : 0.026 V

&#x20;   Persamaan dioda               : I = Is·(e^(V/VT) - 1)

&#x20;   KCL                           : (Vin-V)/R = Is·(e^(V/VT)-1)



&#x20; ◆ Hasil DC Bias Point

&#x20; ──────────────────────────────────────────────────────────────────

&#x20;      Vin (V) │  V\_diode (V) │    I\_diode (A) │        I\_R (A) │ Iterasi

&#x20;   ───────────┼──────────────┼────────────────┼────────────────┼────────

&#x20;         1.00 │     0.500269 │   2.271504e-04 │   2.271504e-04 │      18

&#x20;         3.00 │     0.541691 │   1.117413e-03 │   1.117413e-03 │      16

&#x20;         5.00 │     0.557079 │   2.019509e-03 │   2.019509e-03 │      16

&#x20;         7.00 │     0.566704 │   2.924226e-03 │   2.924226e-03 │      15

&#x20;        12.00 │     0.581621 │   5.190172e-03 │   5.190172e-03 │      15



&#x20;   ✓ Tegangan dioda konvergen ke \~0.5-0.6 V (sesuai karakteristik dioda silikon)

&#x20;   ✓ Arus resistor ≈ arus dioda (konfirmasi KCL terpenuhi)



&#x20; ◆ Grafik Analisis DC Bias

&#x20; ──────────────────────────────────────────────────────────────────

&#x20;   ✓ Grafik berhasil ditampilkan!



&#x20; Tekan \[Enter] untuk kembali ke menu...



2\.



Pilih menu \[0-3]: 2



◆ Input Parameter Rangkaian (tekan Enter untuk default)

&#x20;   Resistor R1 \[1000.0 Ω]: 1500         ← ganti R1

&#x20;   Resistor R2 \[2000.0 Ω]: 3300         ← ganti R2

&#x20;   Arus saturasi Is \[1e-12 A]: 1e-14    ← ganti Is (notasi ilmiah)

&#x20;   Tegangan termal VT \[0.026 V]:        ← tekan Enter (default)



◆ Input Daftar Tegangan Vin (pisahkan dengan koma)

&#x20;   Daftar Vin \[0.5, 1.0, 2.0, 3.0, 5.0, 10.0]: 2 4 6 8 10

&#x20;                                                  ↑ bisa pakai spasi

◆ Parameter yang Digunakan

&#x20; ──────────────────────────────────────────────────────────────────

&#x20;   Resistor R1                   : 1500.0 Ω

&#x20;   Resistor R2                   : 3300.0 Ω

&#x20;   Arus saturasi Is              : 1.00e-14 A

&#x20;   Tegangan termal VT            : 0.026 V



&#x20; ◆ Persamaan KCL (Sistem Non-Linier 2 Variabel)

&#x20; ──────────────────────────────────────────────────────────────────

&#x20;   f1(V1,V2) = (Vin-V1)/R1 - (V1-V2)/R2 - Is·(e^(V1/VT)-1) = 0

&#x20;   f2(V1,V2) = (V1-V2)/R2  - Is·(e^(V2/VT)-1) = 0



&#x20; ◆ Matriks Jacobian (Diturunkan Secara Analitik)

&#x20; ──────────────────────────────────────────────────────────────────

&#x20;   ┌                                                        ┐

&#x20;   │ -1/R1 - 1/R2 - (Is/VT)·e^(V1/VT)         1/R2        │

&#x20;   │                                                        │

&#x20;   │           1/R2                -1/R2 - (Is/VT)·e^(V2/VT)│

&#x20;   └                                                        ┘



&#x20; ◆ Hasil DC Bias Point

&#x20; ──────────────────────────────────────────────────────────────────

&#x20;      Vin (V) │     V1 (V) │     V2 (V) │       I\_D1 (A) │       I\_D2 (A) │  Iter

&#x20;   ───────────┼────────────┼────────────┼────────────────┼────────────────┼──────

&#x20;         2.00 │   0.654902 │   0.564893 │   8.694564e-04 │   2.727543e-05 │    11

&#x20;         4.00 │   0.678815 │   0.569860 │   2.181107e-03 │   3.301666e-05 │    16

&#x20;         6.00 │   0.691135 │   0.572150 │   3.503187e-03 │   3.605611e-05 │    15

&#x20;         8.00 │   0.699479 │   0.573612 │   4.828872e-03 │   3.814169e-05 │    15

&#x20;        10.00 │   0.705794 │   0.574675 │   6.156404e-03 │   3.973321e-05 │    15



&#x20; ◆ Detail Konvergensi (Vin = 6.0 V)

&#x20; ──────────────────────────────────────────────────────────────────



&#x20; iter 1: V1=0.600000, V2=0.600000

&#x20; iter 2: V1=0.900000, V2=0.624427

&#x20; iter 3: V1=0.874008, V2=0.606261

&#x20; iter 4: V1=0.848030, V2=0.595142

&#x20; iter 5: V1=0.822090, V2=0.590080

&#x20; iter 6: V1=0.796254, V2=0.587021

&#x20; iter 7: V1=0.770701, V2=0.584042

&#x20; iter 8: V1=0.745902, V2=0.580867

&#x20; iter 9: V1=0.723039, V2=0.577595

&#x20; iter 10: V1=0.704634, V2=0.574634

&#x20; iter 11: V1=0.694092, V2=0.572736

&#x20; iter 12: V1=0.691296, V2=0.572183

&#x20; iter 13: V1=0.691135, V2=0.572150

&#x20; iter 14: V1=0.691135, V2=0.572150

&#x20; iter 15: V1=0.691135, V2=0.572150



&#x20; ◆ Grafik Analisis DC Bias 2 Node

&#x20; ──────────────────────────────────────────────────────────────────

&#x20;   ✓ Grafik berhasil ditampilkan!



&#x20; Tekan \[Enter] untuk kembali ke menu...



3\.



Pilih menu \[0-3]: 3



◆ Input Parameter Rangkaian (tekan Enter untuk default)

&#x20;   Resistor R \[1000.0 Ω]:               ← Enter (default 1000)

&#x20;   Kapasitor C \[1e-06 F]: 4.7e-6        ← ganti C jadi 4.7 µF

&#x20;   Arus saturasi Is \[1e-12 A]:          ← Enter (default)

&#x20;   Tegangan termal VT \[0.026 V]:        ← Enter (default)



◆ Input Parameter Sumber Sinus (tekan Enter untuk default)

&#x20;   Amplitudo Vm \[5.0 V]: 3.3            ← ganti amplitudo jadi 3.3V

&#x20;   Frekuensi \[50.0 Hz]: 1000            ← ganti frekuensi jadi 1 kHz



◆ Input Parameter Simulasi (tekan Enter untuk default)

&#x20;   Waktu simulasi (t\_end) \[0.06 s]: 0.005   ← 5 ms (karena freq tinggi)

&#x20;   Langkah waktu (dt) \[1e-05 s]: 1e-6       ← dt lebih kecil



&#x20;◆ Parameter yang Digunakan

&#x20; ──────────────────────────────────────────────────────────────────

&#x20;   Resistor R                    : 1000.0 Ω

&#x20;   Kapasitor C                   : 4.70e-06 F

&#x20;   Arus saturasi Is              : 1.00e-12 A

&#x20;   Tegangan termal VT            : 0.026 V

&#x20;   Amplitudo Vm                  : 3.3 V

&#x20;   Frekuensi                     : 1000.0 Hz

&#x20;   Omega (ω)                     : 6283.1853 rad/s



&#x20; ◆ Persamaan ODE

&#x20; ──────────────────────────────────────────────────────────────────

&#x20;   dV/dt = (1/C) · \[ (Vin(t)-V)/R - Is·(e^(V/VT)-1) ]



&#x20;   Diskritisasi Euler Implisit:

&#x20;   g(V\_{n+1}) = V\_{n+1} - V\_n - Δt·f(t\_{n+1}, V\_{n+1}) = 0

&#x20;   → Diselesaikan dengan Newton-Raphson di setiap time-step



&#x20; ◆ Menjalankan Simulasi...

&#x20; ──────────────────────────────────────────────────────────────────

&#x20;   Waktu simulasi  : 0.0 ms → 5.0 ms

&#x20;   Langkah waktu Δt: 1.0 µs

&#x20;   Jumlah step     : 5000

&#x20;   Jumlah periode  : 5.0 periode



&#x20;   Menghitung ✓ Selesai!



&#x20; ◆ Tabel Hasil Simulasi (Sampling 20 Titik)

&#x20; ──────────────────────────────────────────────────────────────────

&#x20;     No │    t (ms) │    Vin (V) │   V\_node (V) │    I\_diode (A)

&#x20;   ─────┼───────────┼────────────┼──────────────┼───────────────

&#x20;      1 │     0.000 │     0.0000 │     0.000000 │   0.000000e+00

&#x20;      2 │     0.263 │     3.2890 │     0.118743 │   9.526021e-11

&#x20;      3 │     0.526 │    -0.5367 │     0.209218 │   3.122936e-09

&#x20;      4 │     0.789 │    -3.2014 │     0.063272 │   1.039907e-11

&#x20;      5 │     1.052 │     1.0591 │    -0.015149 │  -4.415929e-13

&#x20;      6 │     1.315 │     3.0286 │     0.132472 │   1.622142e-10

&#x20;      7 │     1.578 │    -1.5533 │     0.176287 │   8.793031e-10

&#x20;      8 │     1.842 │    -2.7638 │     0.010981 │   5.255433e-13

&#x20;      9 │     2.105 │     2.0226 │    -0.014335 │  -4.238359e-13

&#x20;     10 │     2.368 │     2.4338 │     0.145840 │   2.719329e-10

&#x20;     11 │     2.631 │    -2.4197 │     0.136613 │   1.903938e-10

&#x20;     12 │     2.894 │    -2.0389 │    -0.030006 │  -6.846472e-13

&#x20;     13 │     3.157 │     2.7525 │    -0.001106 │  -4.163399e-14

&#x20;     14 │     3.421 │     1.5716 │     0.153991 │   3.724322e-10

&#x20;     15 │     3.684 │    -3.0203 │     0.092147 │   3.360932e-11

&#x20;     16 │     3.947 │    -1.0787 │    -0.058623 │  -8.950986e-13

&#x20;     17 │     4.210 │     3.1963 │     0.021816 │   1.314234e-12

&#x20;     18 │     4.473 │     0.5572 │     0.153779 │   3.694033e-10

&#x20;     19 │     4.736 │    -3.2872 │     0.046435 │   4.965237e-12

&#x20;     20 │     5.000 │     0.0000 │    -0.073076 │  -9.398317e-13



&#x20; ◆ Statistik Hasil

&#x20; ──────────────────────────────────────────────────────────────────

&#x20;   V\_node minimum                : -0.073112 V

&#x20;   V\_node maksimum               : 0.212183 V

&#x20;   Vin minimum                   : -3.300000 V

&#x20;   Vin maksimum                  : 3.300000 V



&#x20; ◆ Grafik Respons Transien

&#x20; ──────────────────────────────────────────────────────────────────

&#x20;   ✓ Grafik berhasil ditampilkan!



&#x20; Tekan \[Enter] untuk kembali ke menu...

