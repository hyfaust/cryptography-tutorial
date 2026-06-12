#!/usr/bin/env python3
"""
Number Theory Demo for Cryptography Learning
Demonstrates modular arithmetic, GCD, modular inverse, Euler's totient,
Fermat's Little Theorem, Euler's theorem, and Miller-Rabin primality test.

Usage: python scripts/number_theory_demo.py
Dependencies: pip install sympy
"""

import random
from sympy import gcd, mod_inverse, totient, isprime, nextprime


# ============================================================
# Helper Functions
# ============================================================

def extended_gcd(a, b):
    """Extended Euclidean Algorithm. Returns (gcd, x, y) such that a*x + b*y = gcd."""
    if a == 0:
        return b, 0, 1
    g, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return g, x, y


def mod_inverse_manual(a, n):
    """Compute modular inverse of a mod n using extended GCD."""
    g, x, _ = extended_gcd(a % n, n)
    if g != 1:
        return None
    return x % n


def euler_totient(n):
    """Compute Euler's totient function phi(n)."""
    result = n
    p = 2
    temp = n
    while p * p <= temp:
        if temp % p == 0:
            while temp % p == 0:
                temp //= p
            result -= result // p
        p += 1
    if temp > 1:
        result -= result // temp
    return result


def miller_rabin(n, k=20):
    """Miller-Rabin primality test. Returns True if n is probably prime."""
    if n < 2:
        return False
    if n == 2 or n == 3:
        return True
    if n % 2 == 0:
        return False

    # Write n-1 as 2^s * d
    s, d = 0, n - 1
    while d % 2 == 0:
        s += 1
        d //= 2

    # Perform k rounds
    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, d, n)

        if x == 1 or x == n - 1:
            continue

        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False

    return True


# ============================================================
# Demo Functions
# ============================================================

def demo_modular_arithmetic():
    """Demonstrate basic modular arithmetic."""
    print("--- Modular Arithmetic ---")
    a, n = 17, 5
    print(f"{a} mod {n} = {a % n}")

    a, b, n = 13, 17, 5
    print(f"({a} + {b}) mod {n} = {(a + b) % n}")
    print(f"({a} * {b}) mod {n} = {(a * b) % n}")

    # Large modular exponentiation
    base, exp, mod = 2, 100, 1000
    result = pow(base, exp, mod)
    print(f"{base}^{exp} mod {mod} = {result}")
    print()


def demo_gcd():
    """Demonstrate GCD using Euclidean algorithm."""
    print("--- GCD (Euclidean Algorithm) ---")
    pairs = [(48, 18), (1071, 462), (270, 192)]
    for a, b in pairs:
        result = gcd(a, b)
        print(f"gcd({a}, {b}) = {result}")
    print()


def demo_extended_gcd():
    """Demonstrate extended GCD and Bezout's identity."""
    print("--- Extended GCD (Bezout's Identity) ---")
    a, b = 48, 18
    g, x, y = extended_gcd(a, b)
    print(f"gcd({a}, {b}) = {g}")
    print(f"{a} * ({x}) + {b} * ({y}) = {g}")
    print(f"Verification: {a}*{x} + {b}*{y} = {a*x + b*y}")
    print()


def demo_modular_inverse():
    """Demonstrate modular inverse computation."""
    print("--- Modular Inverse ---")
    test_cases = [(3, 11), (7, 26), (17, 43)]
    for a, n in test_cases:
        inv = mod_inverse_manual(a, n)
        if inv is not None:
            print(f"{a}^(-1) mod {n} = {inv}")
            print(f"  Verification: {a} * {inv} mod {n} = {(a * inv) % n}")
        else:
            print(f"{a}^(-1) mod {n} does not exist (gcd != 1)")

    # Case where inverse does not exist
    a, n = 2, 4
    inv = mod_inverse_manual(a, n)
    print(f"\n{a}^(-1) mod {n} = {inv}  (does not exist, gcd({a},{n}) = {gcd(a, n)})")
    print()


def demo_euler_totient():
    """Demonstrate Euler's totient function."""
    print("--- Euler's Totient Function ---")
    for n in [1, 7, 12, 15, 30, 100]:
        phi = euler_totient(n)
        phi_sympy = totient(n)
        print(f"φ({n}) = {phi}  (sympy: {phi_sympy})")
    print()


def demo_fermat_little_theorem():
    """Verify Fermat's Little Theorem."""
    print("--- Fermat's Little Theorem Verification ---")
    p = 97  # Prime
    print(f"p = {p}")
    for a in [2, 3, 5, 7, 11]:
        result = pow(a, p - 1, p)
        status = "✓" if result == 1 else "✗"
        print(f"{a}^({p-1}) mod {p} = {result}  {status}")
    print()


def demo_euler_theorem():
    """Verify Euler's theorem."""
    print("--- Euler's Theorem Verification ---")
    n = 15
    phi_n = euler_totient(n)
    print(f"n = {n}, φ({n}) = {phi_n}")
    for a in [2, 4, 7, 11, 13]:
        if gcd(a, n) == 1:
            result = pow(a, phi_n, n)
            status = "✓" if result == 1 else "✗"
            print(f"{a}^{phi_n} mod {n} = {result}  {status}")
    print()


def demo_miller_rabin():
    """Demonstrate Miller-Rabin primality test."""
    print("--- Miller-Rabin Primality Test ---")
    test_numbers = [97, 100, 561, 104729, 104730]
    for n in test_numbers:
        mr_result = miller_rabin(n)
        sympy_result = isprime(n)
        label = "Prime" if mr_result else "Composite"
        print(f"Is {n} prime? {mr_result} ({label})  [sympy: {sympy_result}]")

    # Carmichael number explanation
    print(f"\nNote: 561 = 3 * 11 * 17 is a Carmichael number")
    print(f"  It passes Fermat's test but is detected by Miller-Rabin")

    # Generate a large prime
    print("\n--- Large Prime Generation ---")
    large_prime = nextprime(2**512)
    print(f"A 513-bit prime: {large_prime}")
    print(f"Verified prime: {isprime(large_prime)}")
    print()


# ============================================================
# Main
# ============================================================

def main():
    print("=" * 50)
    print("  Number Theory Demo for Cryptography")
    print("=" * 50)
    print()

    demo_modular_arithmetic()
    demo_gcd()
    demo_extended_gcd()
    demo_modular_inverse()
    demo_euler_totient()
    demo_fermat_little_theorem()
    demo_euler_theorem()
    demo_miller_rabin()

    print("=" * 50)
    print("  All demos completed successfully!")
    print("=" * 50)


if __name__ == "__main__":
    main()
