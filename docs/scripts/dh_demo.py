#!/usr/bin/env python3
"""
Diffie-Hellman Key Exchange Demo for Cryptography Learning
Demonstrates DH protocol, MITM attack, ECDH, and forward secrecy concepts.

Usage: python scripts/dh_demo.py
Dependencies: pip install sympy
"""

import random
import hashlib
import time
from sympy import isprime, nextprime, mod_inverse


# ============================================================
# Helper: Elliptic Curve (reused from ecc_demo)
# ============================================================

class EllipticCurve:
    """Elliptic curve y^2 = x^3 + ax + b over GF(p)."""

    def __init__(self, a, b, p):
        self.a = a
        self.b = b
        self.p = p

    def is_on_curve(self, point):
        if point is None:
            return True
        x, y = point
        return (y * y - x * x * x - self.a * x - self.b) % self.p == 0

    def point_add(self, P, Q):
        if P is None:
            return Q
        if Q is None:
            return P
        x1, y1 = P
        x2, y2 = Q
        if x1 == x2:
            if y1 != y2:
                return None
            if y1 == 0:
                return None
            lam = (3 * x1 * x1 + self.a) * mod_inverse(2 * y1, self.p) % self.p
        else:
            lam = (y2 - y1) * mod_inverse(x2 - x1, self.p) % self.p
        x3 = (lam * lam - x1 - x2) % self.p
        y3 = (lam * (x1 - x3) - y1) % self.p
        return (x3, y3)

    def scalar_mult(self, k, P):
        if k == 0:
            return None
        result = None
        addend = P
        while k:
            if k & 1:
                result = self.point_add(result, addend)
            addend = self.point_add(addend, addend)
            k >>= 1
        return result


# ============================================================
# DH with Small Numbers
# ============================================================

def dh_small_demo():
    """Demonstrate DH key exchange with small numbers."""
    print("--- Basic DH with Small Numbers ---")

    # Public parameters
    p = 23
    g = 5
    print(f"Public parameters: p = {p}, g = {g}")

    # Alice
    a = 6
    A = pow(g, a, p)
    print(f"\nAlice:")
    print(f"  Private key a = {a}")
    print(f"  Public key A = g^a mod p = {g}^{a} mod {p} = {A}")

    # Bob
    b = 15
    B = pow(g, b, p)
    print(f"\nBob:")
    print(f"  Private key b = {b}")
    print(f"  Public key B = g^b mod p = {g}^{b} mod {p} = {B}")

    # Key exchange
    print(f"\nKey Exchange:")
    print(f"  Alice sends A = {A} to Bob")
    print(f"  Bob sends B = {B} to Alice")

    # Shared secret
    s_alice = pow(B, a, p)
    s_bob = pow(A, b, p)
    print(f"\nShared Secret Computation:")
    print(f"  Alice: s = B^a mod p = {B}^{a} mod {p} = {s_alice}")
    print(f"  Bob:   s = A^b mod p = {A}^{b} mod {p} = {s_bob}")
    print(f"\n  Shared secret matches: {s_alice == s_bob}")
    print(f"  Shared secret = {s_alice}")
    print()


# ============================================================
# DH with Larger Parameters
# ============================================================

def generate_safe_prime(bits):
    """Generate a safe prime p where (p-1)/2 is also prime."""
    while True:
        q = nextprime(random.getrandbits(bits - 1))
        p = 2 * q + 1
        if isprime(p) and p.bit_length() == bits:
            return p, q


def dh_large_demo():
    """Demonstrate DH with realistic parameter sizes."""
    print("--- DH with Larger Parameters ---")

    # Generate a 512-bit safe prime (for demo speed; use 2048+ in production)
    print("Generating safe prime (512-bit for demo)...")
    start = time.time()
    p, q = generate_safe_prime(512)
    gen_time = time.time() - start
    print(f"  p generated in {gen_time:.2f}s")
    print(f"  p has {p.bit_length()} bits")

    # Find a generator of the subgroup of order q
    g = 2
    while pow(g, 2, p) == 1 or pow(g, q, p) != 1:
        g += 1
    print(f"  g = {g}")

    # Alice
    a = random.randrange(2, p - 1)
    start = time.time()
    A = pow(g, a, p)
    print(f"\nAlice:")
    print(f"  Private key a: {a.bit_length()}-bit number")
    print(f"  Public key A computed in {time.time() - start:.4f}s")

    # Bob
    b = random.randrange(2, p - 1)
    start = time.time()
    B = pow(g, b, p)
    print(f"\nBob:")
    print(f"  Private key b: {b.bit_length()}-bit number")
    print(f"  Public key B computed in {time.time() - start:.4f}s")

    # Shared secret
    start = time.time()
    s_alice = pow(B, a, p)
    s_bob = pow(A, b, p)
    compute_time = time.time() - start
    print(f"\nShared secret computed in {compute_time:.4f}s")
    print(f"  Shared secrets match: {s_alice == s_bob}")
    print(f"  Shared secret: {hex(s_alice)[:40]}...")
    print()


# ============================================================
# MITM Attack Demo
# ============================================================

def mitm_attack_demo():
    """Demonstrate a man-in-the-middle attack on DH."""
    print("--- MITM Attack Demonstration ---")

    p, g = 23, 5
    print(f"Public parameters: p = {p}, g = {g}")

    # Alice's side
    a = 6
    A = pow(g, a, p)
    print(f"\n[Legitimate] Alice: a = {a}, A = {A}")

    # Bob's side
    b = 15
    B = pow(g, b, p)
    print(f"[Legitimate] Bob:   b = {b}, B = {B}")

    # Mallory (attacker)
    m1 = 13  # Mallory's key for Alice
    m2 = 17  # Mallory's key for Bob
    M1 = pow(g, m1, p)  # What Mallory sends to Alice (pretending to be Bob)
    M2 = pow(g, m2, p)  # What Mallory sends to Bob (pretending to be Alice)

    print(f"\n[Attack] Mallory intercepts communication!")
    print(f"  Mallory's keys: m1 = {m1}, m2 = {m2}")
    print(f"  Mallory sends M1 = {M1} to Alice (pretending to be Bob)")
    print(f"  Mallory sends M2 = {M2} to Bob (pretending to be Alice)")

    # Alice thinks she's talking to Bob
    s_alice = pow(M1, a, p)
    print(f"\n  Alice computes shared key with 'Bob': {s_alice}")

    # Mallory computes shared key with Alice
    s_mallory_alice = pow(A, m1, p)
    print(f"  Mallory computes shared key with Alice: {s_mallory_alice}")
    print(f"  Keys match (Alice-Mallory): {s_alice == s_mallory_alice}")

    # Bob thinks he's talking to Alice
    s_bob = pow(M2, b, p)
    print(f"\n  Bob computes shared key with 'Alice': {s_bob}")

    # Mallory computes shared key with Bob
    s_mallory_bob = pow(B, m2, p)
    print(f"  Mallory computes shared key with Bob: {s_mallory_bob}")
    print(f"  Keys match (Bob-Mallory): {s_bob == s_mallory_bob}")

    print(f"\n  Alice and Bob's real shared keys are DIFFERENT!")
    print(f"  Mallory can decrypt and re-encrypt all messages!")
    print()


# ============================================================
# ECDH Demo
# ============================================================

def ecdh_demo():
    """Demonstrate Elliptic Curve Diffie-Hellman."""
    print("--- ECDH Demonstration ---")

    # Define curve
    a, b, p = 2, 3, 97
    curve = EllipticCurve(a, b, p)
    G = (3, 6)  # Base point
    assert curve.is_on_curve(G)
    print(f"Curve: y^2 = x^3 + {a}x + {b} (mod {p})")
    print(f"Base point G = {G}")

    # Alice
    alice_priv = 7
    alice_pub = curve.scalar_mult(alice_priv, G)
    print(f"\nAlice:")
    print(f"  Private key a = {alice_priv}")
    print(f"  Public key A = {alice_priv}G = {alice_pub}")

    # Bob
    bob_priv = 11
    bob_pub = curve.scalar_mult(bob_priv, G)
    print(f"\nBob:")
    print(f"  Private key b = {bob_priv}")
    print(f"  Public key B = {bob_priv}G = {bob_pub}")

    # Shared secret
    s_alice = curve.scalar_mult(alice_priv, bob_pub)
    s_bob = curve.scalar_mult(bob_priv, alice_pub)
    print(f"\nShared Secret:")
    print(f"  Alice: S = aB = {alice_priv} * {bob_pub} = {s_alice}")
    print(f"  Bob:   S = bA = {bob_priv} * {alice_pub} = {s_bob}")
    print(f"  Shared point matches: {s_alice == s_bob}")

    # Verify: abG = baG
    abG = curve.scalar_mult(alice_priv * bob_priv, G)
    print(f"\n  Verification: (ab)G = {abG}")
    print(f"  Matches shared secret: {abG == s_alice}")
    print()


# ============================================================
# Forward Secrecy Comparison
# ============================================================

def forward_secrecy_demo():
    """Compare RSA key exchange vs DH key exchange for forward secrecy."""
    print("--- Forward Secrecy Comparison ---")

    print("Scenario: Alice and Bob communicate over multiple sessions.")
    print("Later, Bob's long-term private key is compromised.\n")

    print("--- RSA Key Exchange (NO Forward Secrecy) ---")
    print("  Session 1: Alice encrypts key K1 with Bob's RSA public key")
    print("  Session 2: Alice encrypts key K2 with Bob's RSA public key")
    print("  Session 3: Alice encrypts key K3 with Bob's RSA public key")
    print("  ...")
    print("  Attacker records all encrypted key exchanges.")
    print("  Later: Bob's RSA private key is STOLEN!")
    print("  Result: Attacker can decrypt K1, K2, K3 ... ALL sessions compromised!")

    print("\n--- ECDHE Key Exchange (Forward Secrecy) ---")
    print("  Session 1: Alice and Bob generate ephemeral keys (a1, b1)")
    print("             Shared key K1 = ephemeral DH")
    print("             Ephemeral keys DESTROYED after session")
    print("  Session 2: Alice and Bob generate NEW ephemeral keys (a2, b2)")
    print("             Shared key K2 = ephemeral DH")
    print("             Ephemeral keys DESTROYED after session")
    print("  ...")
    print("  Later: Bob's long-term key is STOLEN!")
    print("  Result: Attacker CANNOT recover K1, K2, K3 ... past sessions safe!")

    print("\n  Key insight: Ephemeral keys are destroyed, so they cannot")
    print("  be used to compute past shared secrets even with long-term key compromise.")
    print()


# ============================================================
# Main
# ============================================================

def main():
    print("=" * 55)
    print("  Diffie-Hellman Key Exchange Demo")
    print("=" * 55)
    print()

    dh_small_demo()
    dh_large_demo()
    mitm_attack_demo()
    ecdh_demo()
    forward_secrecy_demo()

    print("=" * 55)
    print("  All DH demos completed successfully!")
    print("=" * 55)


if __name__ == "__main__":
    main()
