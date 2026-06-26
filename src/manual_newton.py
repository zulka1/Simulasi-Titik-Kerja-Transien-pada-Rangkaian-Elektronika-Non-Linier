"""
manual_newton.py
Newton-Raphson MANUAL: versi 1 variabel dan versi multi-variabel generik
(menggunakan gauss_eliminasi manual untuk solve J*delta = -F).
"""

import numpy as np
from .manual_linalg import gauss_eliminasi


def newton_raphson_1var(f, f_prime, x0, tol=1e-10, max_iter=100, verbose=False):
    """
    Newton-Raphson untuk 1 variabel:  x_(n+1) = x_n - f(x_n)/f'(x_n)
    """
    x = x0
    for i in range(1, max_iter + 1):
        fx = f(x)
        fpx = f_prime(x)
        if abs(fpx) < 1e-14:
            raise ZeroDivisionError("Turunan mendekati nol, iterasi gagal.")
        x_baru = x - fx / fpx
        if verbose:
            print(f"  iter {i}: x = {x_baru:.10f}, f(x) = {f(x_baru):.3e}")
        if abs(x_baru - x) < tol:
            return x_baru, i
        x = x_baru
    raise RuntimeError("Newton-Raphson 1 variabel tidak konvergen.")


def newton_raphson_multivar(F_func, J_func, x0, tol=1e-10, max_iter=100, verbose=False):
    """
    Newton-Raphson untuk sistem n variabel:
        J(x_n) * delta = -F(x_n)
        x_(n+1) = x_n + delta

    F_func : fungsi -> array F(x) (n,)
    J_func : fungsi -> array Jacobian J(x) (n,n)
    Solve sistem linier pakai gauss_eliminasi MANUAL (bukan np.linalg.solve).
    """
    x = np.array(x0, dtype=float)
    for i in range(1, max_iter + 1):
        Fx = F_func(x)
        Jx = J_func(x)
        minus_F = [-val for val in Fx]

        delta = gauss_eliminasi(Jx, minus_F)
        x_baru = x + delta

        if verbose:
            print(f"  iter {i}: x = {x_baru}")

        norma_delta = 0.0
        for d in delta:
            norma_delta += d * d
        norma_delta = norma_delta ** 0.5  # akar pangkat 2 manual (bukan np.linalg.norm)

        if norma_delta < tol:
            return x_baru, i
        x = x_baru
    raise RuntimeError("Newton-Raphson multi-variabel tidak konvergen.")


if __name__ == "__main__":
    print("=== Validasi Newton-Raphson 1 variabel ===")
    print("f(x) = x^2 - 2, akar eksak = sqrt(2)")

    def f(x):
        return x**2 - 2

    def f_prime(x):
        return 2 * x

    akar, n_iter = newton_raphson_1var(f, f_prime, x0=1.0, verbose=True)
    print(f"Akar ditemukan: {akar:.10f} dalam {n_iter} iterasi")
    print(f"Akar eksak    : {2**0.5:.10f}\n")

    print("=== Validasi Newton-Raphson multi-variabel ===")
    print("Sistem: x^2+y^2=4, x-y=0 -> akar eksak x=y=sqrt(2)")

    def F(v):
        x, y = v
        return np.array([x**2 + y**2 - 4, x - y])

    def J(v):
        x, y = v
        return np.array([[2*x, 2*y], [1.0, -1.0]])

    akar2, n_iter2 = newton_raphson_multivar(F, J, x0=[1.0, 0.5], verbose=True)
    print(f"Akar ditemukan: {akar2} dalam {n_iter2} iterasi")
    print(f"Akar eksak    : x=y={2**0.5:.10f}")
