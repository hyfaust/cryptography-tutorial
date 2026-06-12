#!/usr/bin/env python3
"""
Lattice-Based Cryptography Demonstration
==========================================
This script demonstrates fundamental concepts of lattice-based cryptography:
- Lattice basics (basis, vectors)
- Learning With Errors (LWE) problem
- Simple LWE encryption/decryption
- Lattice reduction (simulated)

Dependencies: pip install numpy
"""

import numpy as np
import random


def print_separator(title):
    """Print a formatted section separator."""
    print(f"\n{'=' * 60}")
    print(f"  {title}")
    print(f"{'=' * 60}")


# ============================================================
# Part 1: Lattice Basics
# ============================================================

def demonstrate_lattice_basics():
    """Show fundamental lattice concepts."""
    print_separator("Part 1: Lattice Basics")

    print("""
    A lattice is a set of all integer linear combinations of
    linearly independent vectors (a basis).

    L = { c1*b1 + c2*b2 + ... + cn*bn | c1,...,cn in Z }

    where b1, b2, ..., bn are the basis vectors.
    """)

    # 2D lattice example
    b1 = np.array([3, 0])
    b2 = np.array([0, 4])

    print(f"    Basis vectors: b1 = {b1}, b2 = {b2}")
    print(f"\n    Lattice points (small examples):")
    for c1 in range(-2, 3):
        for c2 in range(-2, 3):
            point = c1 * b1 + c2 * b2
            if c1 >= 0 and c2 >= 0:
                print(f"      {c1}*{b1} + {c2}*{b2} = {point}")

    # Show alternative basis (shorter vectors)
    print(f"\n    Same lattice with different basis:")
    b1_alt = np.array([3, 4])
    b2_alt = np.array([3, -4])
    print(f"    b1' = {b1_alt}, b2' = {b2_alt}")
    print(f"    (Same lattice points, different representation)")

    # Shortest Vector Problem (SVP)
    print(f"\n    Shortest Vector Problem (SVP):")
    print(f"    Find the shortest non-zero vector in the lattice.")
    print(f"    For our basis: ||b1|| = {np.linalg.norm(b1):.1f}, ||b2|| = {np.linalg.norm(b2):.1f}")
    print(f"    Shortest vector: b1 with length {np.linalg.norm(b1):.1f}")


# ============================================================
# Part 2: Learning With Errors (LWE)
# ============================================================

class SimpleLWE:
    """
    A simple LWE-based encryption scheme for demonstration.

    Parameters:
    - n: dimension (security parameter)
    - q: modulus
    - e: error bound (noise)

    Key Generation:
    - Secret key: random vector s in Z_q^n
    - Public key: (A, b = A*s + e) where A is random matrix

    Encryption of bit m:
    - Choose random r, compute (u, v) = (A^T*r, b^T*r + m*floor(q/2))

    Decryption:
    - m' = v - s^T*u, check if m' is closer to 0 or floor(q/2)
    """

    def __init__(self, n=64, q=97, error_bound=1):
        self.n = n
        self.q = q
        self.error_bound = error_bound

    def keygen(self):
        """Generate LWE key pair."""
        n, q = self.n, self.q

        # Secret key: random vector
        s = np.array([random.randint(0, q - 1) for _ in range(n)])

        # Public key: (A, b = A*s + e)
        A = np.array([[random.randint(0, q - 1) for _ in range(n)] for _ in range(n)])
        e = np.array([random.randint(-self.error_bound, self.error_bound) for _ in range(n)])
        b = (A @ s + e) % q

        return (A, b), s

    def encrypt(self, public_key, bit):
        """Encrypt a single bit (0 or 1)."""
        A, b = public_key
        n, q = self.n, self.q

        # Random binary vector
        r = np.array([random.randint(0, 1) for _ in range(n)])

        # Ciphertext
        u = (A.T @ r) % q
        half_q = q // 2
        v = (b @ r + bit * half_q) % q

        return u, v

    def decrypt(self, secret_key, ciphertext):
        """Decrypt a ciphertext to recover the bit."""
        u, v = ciphertext
        n, q = self.n, self.q
        half_q = q // 2

        # Compute v - s^T * u
        result = (v - secret_key @ u) % q

        # Decide: closer to 0 or to q/2?
        if result > q // 2:
            result = result - q

        # If |result| < q/4, it's 0; otherwise it's 1
        return 0 if abs(result) < half_q / 2 else 1


def demonstrate_lwe():
    """Demonstrate the LWE problem and encryption."""
    print_separator("Part 2: Learning With Errors (LWE)")

    print("""
    The Learning With Errors (LWE) problem:

    Given: (A, b = A*s + e) where e is small noise
    Find:  secret vector s

    This is believed to be hard even for quantum computers!

    LWE is the foundation of many post-quantum schemes:
    - CRYSTALS-Kyber (NIST standard for KEM)
    - CRYSTALS-Dilithium (NIST standard for signatures)
    - FALCON (NIST standard for signatures)
    """)

    # Small example to show the concept
    print("    --- Small Example ---")
    n, q = 4, 23
    print(f"    Dimension n = {n}, Modulus q = {q}")

    s = np.array([3, 7, 2, 5])
    print(f"    Secret s = {s}")

    A = np.array([
        [1, 4, 6, 2],
        [8, 3, 1, 7],
        [5, 9, 2, 4],
        [3, 6, 8, 1],
    ])
    print(f"    Random matrix A:")
    for row in A:
        print(f"      {row}")

    e = np.array([0, -1, 1, 0])
    print(f"    Error e = {e}")

    b = (A @ s + e) % q
    print(f"    b = A*s + e mod q = {b}")

    print(f"\n    Given (A, b), finding s is the LWE problem.")
    print(f"    The small error e makes this hard!")
    print(f"    Without error: Gaussian elimination solves it instantly.")
    print(f"    With error: No efficient algorithm known (even quantum).")

    # LWE Encryption demo
    print(f"\n    --- LWE Encryption Demo ---")
    lwe = SimpleLWE(n=64, q=97, error_bound=1)

    print(f"    Parameters: n={lwe.n}, q={lwe.q}, error_bound={lwe.error_bound}")

    # Key generation
    public_key, secret_key = lwe.keygen()
    A, b = public_key
    print(f"\n    Key generated.")
    print(f"    Public key A shape: {A.shape}")
    print(f"    Secret key length: {len(secret_key)}")

    # Encrypt and decrypt bits
    print(f"\n    Encrypting and decrypting bits:")
    all_correct = True
    for bit in [0, 1, 0, 1, 1, 0, 1, 0]:
        u, v = lwe.encrypt(public_key, bit)
        decrypted = lwe.decrypt(secret_key, (u, v))
        status = "OK" if decrypted == bit else "FAIL"
        if decrypted != bit:
            all_correct = False
        print(f"      Plaintext: {bit} -> Ciphertext: (u[0..2]={u[:3]}..., v={v}) -> Decrypted: {decrypted} [{status}]")

    print(f"\n    All decryptions correct: {all_correct}")


# ============================================================
# Part 3: Lattice Reduction (Conceptual)
# ============================================================

def demonstrate_lattice_reduction():
    """Demonstrate lattice basis reduction concept."""
    print_separator("Part 3: Lattice Basis Reduction")

    print("""
    Lattice reduction finds a "better" basis with shorter,
    more orthogonal vectors.

    The LLL algorithm (Lenstra-Lenstra-Lovasz, 1982):
    - Polynomial time: O(n^5 * n * log(B))
    - Finds vectors within factor 2^((n-1)/2) of shortest
    - Critical tool in cryptanalysis

    Gauss's algorithm (2D case):
    - Exact shortest vector in 2D
    - Simple iterative reduction
    """)

    # 2D Gauss reduction
    print("    --- 2D Gauss Reduction ---")
    b1 = np.array([7.0, 3.0])
    b2 = np.array([4.0, 2.0])
    print(f"    Original basis: b1 = {b1}, b2 = {b2}")
    print(f"    ||b1|| = {np.linalg.norm(b1):.2f}, ||b2|| = {np.linalg.norm(b2):.2f}")

    # Gauss reduction: repeatedly subtract multiples
    print(f"\n    Applying Gauss reduction:")
    step = 0
    while np.linalg.norm(b2) < np.linalg.norm(b1):
        b1, b2 = b2.copy(), b1.copy()
        step += 1
        print(f"    Step {step}: swap -> b1={b1}, b2={b2} (||b1||={np.linalg.norm(b1):.2f})")

    while True:
        # Project b2 onto b1
        mu = round(np.dot(b2, b1) / np.dot(b1, b1))
        if mu == 0:
            break
        b2 = b2 - mu * b1
        step += 1
        print(f"    Step {step}: reduce -> b1={b1}, b2={b2} (||b2||={np.linalg.norm(b2):.2f})")

    print(f"\n    Reduced basis: b1 = {b1}, b2 = {b2}")
    print(f"    ||b1|| = {np.linalg.norm(b1):.2f}, ||b2|| = {np.linalg.norm(b2):.2f}")

    # CVP example
    print(f"\n    --- Closest Vector Problem (CVP) ---")
    print(f"    Given a target point, find the closest lattice point.")
    target = np.array([5.5, 3.7])
    print(f"    Target point: {target}")

    # Search nearby lattice points
    best_dist = float('inf')
    best_point = None
    for c1 in range(-5, 6):
        for c2 in range(-5, 6):
            point = c1 * b1 + c2 * b2
            dist = np.linalg.norm(target - point)
            if dist < best_dist:
                best_dist = dist
                best_point = point

    print(f"    Closest lattice point: {best_point}")
    print(f"    Distance: {best_dist:.4f}")


# ============================================================
# Part 4: NTRU-like Encryption (Simplified)
# ============================================================

def demonstrate_ntru_concept():
    """Demonstrate NTRU-like polynomial encryption concept."""
    print_separator("Part 4: NTRU Concept (Polynomial Ring)")

    print("""
    NTRU operates in the polynomial ring R = Z[x]/(x^n - 1).

    Key idea: multiplication in a lattice-based polynomial ring
    where finding the inverse with small coefficients is hard.

    Simplified demo with small parameters:
    """)

    n = 7
    q = 41
    p = 3

    print(f"    n = {n} (polynomial degree)")
    print(f"    q = {q} (large modulus)")
    print(f"    p = {p} (small modulus)")

    # Polynomial multiplication mod (x^n - 1)
    def poly_mul(a, b, n, mod):
        """Multiply two polynomials in Z[x]/(x^n - 1)."""
        result = [0] * (2 * n - 1)
        for i in range(len(a)):
            for j in range(len(b)):
                result[i + j] += a[i] * b[j]
        # Reduce mod (x^n - 1): x^n = 1, x^(n+1) = x, etc.
        reduced = [0] * n
        for i in range(len(result)):
            reduced[i % n] += result[i]
        return [x % mod for x in reduced]

    # Simple key generation
    # f = 1 + x - x^2 + x^4 (small polynomial)
    f = [1, 1, -1, 0, 1, 0, 0]
    # g = -1 + x^2 - x^3 + x^5
    g = [-1, 0, 1, -1, 0, 1, 0]

    print(f"\n    Private key f = {f}")
    print(f"    Small polynomial g = {g}")
    print(f"    (In real NTRU, finding inverse of f mod q is the trapdoor)")

    # Simple demonstration of polynomial arithmetic
    h = poly_mul(f, g, n, q)
    print(f"\n    f * g mod q = {h}")
    print(f"    (Public key involves f^(-1) * g mod q)")

    print(f"\n    NTRU Security:")
    print(f"    - Based on hardness of finding short vectors in lattices")
    print(f"    - Resistant to quantum attacks")
    print(f"    - Very fast encryption/decryption")
    print(f"    - NTRU is a finalist in NIST PQC competition")


# ============================================================
# Main
# ============================================================

def main():
    print("=" * 60)
    print("  Lattice-Based Cryptography Demonstration")
    print("=" * 60)

    demonstrate_lattice_basics()
    demonstrate_lwe()
    demonstrate_lattice_reduction()
    demonstrate_ntru_concept()

    # Summary
    print_separator("Summary")
    print("""
    Key Takeaways:

    1. LATTICES are discrete subgroups of R^n, defined by
       basis vectors. Hard problems: SVP, CVP.

    2. LWE (Learning With Errors) is the foundation of
       modern lattice cryptography. Adding small noise to
       linear equations makes them computationally hard to solve.

    3. LATTICE REDUCTION (LLL algorithm) is the main
       cryptanalytic tool against lattice-based schemes.

    4. POST-QUANTUM SECURITY: Lattice problems are believed
       hard even for quantum computers (no known quantum
       speedup beyond generic approaches).

    NIST Post-Quantum Standards (2024):
    - ML-KEM (Kyber): Lattice-based key encapsulation
    - ML-DSA (Dilithium): Lattice-based digital signatures
    - SLH-DSA (SPHINCS+): Hash-based signatures
    - FN-DSA (FALCON): Lattice-based signatures (NTRU lattices)
    """)


if __name__ == "__main__":
    main()
