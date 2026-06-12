#!/usr/bin/env python3
"""
Elliptic Curve Cryptography Demo for Cryptography Learning
Demonstrates elliptic curve point operations, scalar multiplication,
discrete logarithm problem, and key size comparison.

Usage: python scripts/ecc_demo.py
Dependencies: pip install sympy
"""

from sympy import mod_inverse, isprime


# ============================================================
# Elliptic Curve Point Operations
# ============================================================

class EllipticCurve:
    """Elliptic curve y^2 = x^3 + ax + b over GF(p)."""

    def __init__(self, a, b, p):
        self.a = a
        self.b = b
        self.p = p
        # Verify non-singular condition
        disc = (4 * a**3 + 27 * b**2) % p
        if disc == 0:
            raise ValueError("Curve is singular (discriminant = 0)")
        self.discriminant = disc

    def is_on_curve(self, point):
        """Check if a point is on the curve."""
        if point is None:  # Point at infinity
            return True
        x, y = point
        return (y * y - x * x * x - self.a * x - self.b) % self.p == 0

    def point_add(self, P, Q):
        """Add two points on the curve."""
        if P is None:
            return Q
        if Q is None:
            return P

        x1, y1 = P
        x2, y2 = Q

        if x1 == x2:
            if y1 != y2:
                return None  # P + (-P) = O
            # Point doubling
            if y1 == 0:
                return None
            lam = (3 * x1 * x1 + self.a) * mod_inverse(2 * y1, self.p) % self.p
        else:
            # Point addition
            lam = (y2 - y1) * mod_inverse(x2 - x1, self.p) % self.p

        x3 = (lam * lam - x1 - x2) % self.p
        y3 = (lam * (x1 - x3) - y1) % self.p
        return (x3, y3)

    def scalar_mult(self, k, P):
        """Compute kP using double-and-add algorithm."""
        if k == 0:
            return None
        if k < 0:
            k = -k
            P = (P[0], (-P[1]) % self.p)

        result = None  # Point at infinity
        addend = P

        while k:
            if k & 1:
                result = self.point_add(result, addend)
            addend = self.point_add(addend, addend)
            k >>= 1

        return result

    def point_order(self, P):
        """Compute the order of a point P."""
        Q = P
        n = 1
        while Q is not None:
            Q = self.point_add(Q, P)
            n += 1
            if n > self.p + 1:
                return None  # Safety check
        return n

    def point_neg(self, P):
        """Return the negation of a point."""
        if P is None:
            return None
        return (P[0], (-P[1]) % self.p)


# ============================================================
# Demo Functions
# ============================================================

def demo_curve_definition():
    """Demonstrate elliptic curve definition and verification."""
    print("--- Elliptic Curve Definition ---")

    a, b, p = 2, 3, 97
    curve = EllipticCurve(a, b, p)
    print(f"Curve: y^2 = x^3 + {a}x + {b} (mod {p})")
    print(f"Discriminant: {curve.discriminant} (non-zero, curve is non-singular)")

    # Count points on curve
    count = 1  # Include point at infinity
    for x in range(p):
        rhs = (x * x * x + a * x + b) % p
        for y in range(p):
            if (y * y) % p == rhs:
                count += 1
    print(f"Number of points on curve: {count}")
    print()


def demo_point_operations():
    """Demonstrate basic point operations."""
    print("--- Point Operations ---")

    a, b, p = 2, 3, 97
    curve = EllipticCurve(a, b, p)

    P = (3, 6)
    assert curve.is_on_curve(P), f"P = {P} is not on the curve!"
    print(f"P = {P} on curve")

    # Point doubling
    Q = curve.scalar_mult(2, P)
    print(f"Q = 2P = {Q}")

    # Point tripling
    R = curve.scalar_mult(3, P)
    print(f"R = 3P = {R}")

    # 5P
    S = curve.scalar_mult(5, P)
    print(f"5P = {S}")

    # Point negation
    neg_P = curve.point_neg(P)
    print(f"-P = {neg_P}")

    # P + (-P) should be point at infinity
    result = curve.point_add(P, neg_P)
    print(f"P + (-P) = {result}  (should be None = point at infinity)")
    print()


def demo_point_addition_verification():
    """Verify commutativity and associativity of point addition."""
    print("--- Point Addition Verification ---")

    a, b, p = 2, 3, 97
    curve = EllipticCurve(a, b, p)

    P = (3, 6)
    Q = (80, 10)
    S = (10, 21)

    # Verify all points are on the curve
    assert curve.is_on_curve(P)
    assert curve.is_on_curve(Q)
    assert curve.is_on_curve(S)

    # Commutativity: P + Q = Q + P
    pq = curve.point_add(P, Q)
    qp = curve.point_add(Q, P)
    print(f"P = {P}, Q = {Q}")
    print(f"P + Q = {pq}")
    print(f"Q + P = {qp}")
    print(f"Commutative: {pq == qp}")

    # Associativity: (P + Q) + S = P + (Q + S)
    pq_s = curve.point_add(pq, S)
    q_s = curve.point_add(Q, S)
    p_qs = curve.point_add(P, q_s)
    print(f"\n(P + Q) + S = {pq_s}")
    print(f"P + (Q + S) = {p_qs}")
    print(f"Associative: {pq_s == p_qs}")
    print()


def demo_scalar_multiplication():
    """Demonstrate scalar multiplication and double-and-add."""
    print("--- Scalar Multiplication ---")

    a, b, p = 2, 3, 97
    curve = EllipticCurve(a, b, p)

    P = (3, 6)
    print(f"P = {P}")

    # Compute kP for k = 1 to 10
    print("\nScalar multiples:")
    for k in range(1, 11):
        kp = curve.scalar_mult(k, P)
        print(f"  {k}P = {kp}")

    # Verify double-and-add vs naive addition
    print("\nDouble-and-add verification:")
    k = 7
    # Double-and-add
    result_da = curve.scalar_mult(k, P)
    # Naive addition
    result_naive = None
    for _ in range(k):
        result_naive = curve.point_add(result_naive, P)
    print(f"  {k}P (double-and-add) = {result_da}")
    print(f"  {k}P (naive addition) = {result_naive}")
    print(f"  Match: {result_da == result_naive}")
    print()


def demo_discrete_log():
    """Demonstrate the discrete logarithm problem on elliptic curves."""
    print("--- Discrete Logarithm Problem ---")

    a, b, p = 2, 3, 97
    curve = EllipticCurve(a, b, p)

    P = (3, 6)

    # Given k, compute Q = kP (easy)
    k_secret = 15
    Q = curve.scalar_mult(k_secret, P)
    print(f"P = {P}")
    print(f"Secret k = {k_secret}")
    print(f"Q = kP = {Q}")

    # Given P and Q, find k by brute force (feasible for small curves)
    print(f"\nSearching for k such that Q = kP...")
    for k_try in range(1, curve.p + 1):
        if curve.scalar_mult(k_try, P) == Q:
            print(f"Found k = {k_try}")
            print(f"Verification: {k_try}P = {curve.scalar_mult(k_try, P)}")
            print(f"Correct: {k_try == k_secret}")
            break
    print()


def demo_point_order():
    """Demonstrate computing the order of a point."""
    print("--- Point Order ---")

    a, b, p = 2, 3, 97
    curve = EllipticCurve(a, b, p)

    P = (3, 6)
    order = curve.point_order(P)
    print(f"P = {P}")
    print(f"Order of P: {order}")

    # Verify: order * P should be point at infinity
    result = curve.scalar_mult(order, P)
    print(f"{order} * P = {result}  (should be None = point at infinity)")

    # Compute order of another point
    Q = (80, 10)
    order_q = curve.point_order(Q)
    print(f"\nQ = {Q}")
    print(f"Order of Q: {order_q}")
    print()


def demo_key_size_comparison():
    """Compare RSA and ECC key sizes for equivalent security."""
    print("--- Key Size Comparison ---")

    comparisons = [
        (80, 1024, 160),
        (112, 2048, 224),
        (128, 3072, 256),
        (192, 7680, 384),
        (256, 15360, 512),
    ]

    print(f"{'Security':<10} | {'RSA Size':<12} | {'ECC Size':<12} | {'Ratio':<8}")
    print("-" * 50)
    for security, rsa_size, ecc_size in comparisons:
        ratio = rsa_size / ecc_size
        print(f"{security:<10} | {rsa_size:<12} | {ecc_size:<12} | {ratio:<8.1f}x")
    print()


def demo_real_world_ecc():
    """Demonstrate ECC parameters used in real-world applications."""
    print("--- Real-World ECC Curves ---")

    # secp256k1 (Bitcoin)
    print("secp256k1 (used in Bitcoin/Ethereum):")
    print(f"  Equation: y^2 = x^3 + 7")
    print(f"  a = 0, b = 7")
    print(f"  p = 2^256 - 2^32 - 977")
    p_secp256k1 = 2**256 - 2**32 - 977
    print(f"  p (hex): {hex(p_secp256k1)}")
    print(f"  p is prime: {isprime(p_secp256k1)}")
    print()

    # P-256 (NIST)
    print("P-256 / prime256v1 / secp256r1 (used in TLS, SSH):")
    print(f"  Standard: NIST FIPS 186-4")
    print(f"  Security level: 128 bits")
    print()


# ============================================================
# Main
# ============================================================

def main():
    print("=" * 50)
    print("  Elliptic Curve Cryptography Demo")
    print("=" * 50)
    print()

    demo_curve_definition()
    demo_point_operations()
    demo_point_addition_verification()
    demo_scalar_multiplication()
    demo_discrete_log()
    demo_point_order()
    demo_key_size_comparison()
    demo_real_world_ecc()

    print("=" * 50)
    print("  All ECC demos completed successfully!")
    print("=" * 50)


if __name__ == "__main__":
    main()
