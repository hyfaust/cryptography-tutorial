#!/usr/bin/env python3
"""
RSA Algorithm Demo for Cryptography Learning
Demonstrates complete RSA workflow: key generation, encryption, decryption,
digital signatures, and mathematical verification.

Usage: python scripts/rsa_demo.py
Dependencies: pip install cryptography
"""

import time
import hashlib
from sympy import isprime, nextprime, mod_inverse, gcd, totient
import random


# ============================================================
# Small Number RSA (Educational)
# ============================================================

def small_rsa_demo():
    """Demonstrate RSA with small numbers for clarity."""
    print("--- Small Number RSA ---")

    # Key Generation
    p, q = 61, 53
    n = p * q
    phi_n = (p - 1) * (q - 1)
    e = 17
    d = mod_inverse(e, phi_n)

    print(f"p = {p}, q = {q}")
    print(f"n = {n}")
    print(f"phi(n) = {phi_n}")
    print(f"e = {e}, d = {d}")
    print(f"Public key:  ({n}, {e})")
    print(f"Private key: ({n}, {d})")
    print()

    # Verify key correctness
    print(f"Verify: e * d mod phi(n) = {(e * d) % phi_n}")

    # Encryption
    M = 65
    C = pow(M, e, n)
    print(f"\nEncrypt M={M}:  C = {M}^{e} mod {n} = {C}")

    # Decryption
    M_dec = pow(C, d, n)
    print(f"Decrypt C={C}: M = {C}^{d} mod {n} = {M_dec}")
    print(f"Correct: {M == M_dec}")

    # Verify M^(ed) ≡ M (mod n)
    print(f"\nVerify M^(ed) ≡ M (mod n):")
    ed = e * d
    for test_m in [1, 2, 65, 100, 3000]:
        if test_m < n:
            enc = pow(test_m, e, n)
            dec = pow(enc, d, n)
            status = "✓" if dec == test_m else "✗"
            print(f"  M={test_m:4d} -> C={enc:4d} -> M'={dec:4d}  {status}")
    print()


# ============================================================
# Full RSA Implementation
# ============================================================

def generate_prime(bits):
    """Generate a random prime number of specified bit length."""
    while True:
        n = random.getrandbits(bits)
        n |= (1 << (bits - 1)) | 1  # Set MSB and LSB
        if isprime(n):
            return n


def rsa_keygen(bits=2048):
    """Generate RSA key pair."""
    print(f"Generating {bits}-bit RSA key pair...")
    start = time.time()

    half_bits = bits // 2
    p = generate_prime(half_bits)
    q = generate_prime(half_bits)

    # Ensure p != q
    while p == q:
        q = generate_prime(half_bits)

    n = p * q
    phi_n = (p - 1) * (q - 1)
    e = 65537

    # Ensure gcd(e, phi_n) = 1
    while gcd(e, phi_n) != 1:
        p = generate_prime(half_bits)
        q = generate_prime(half_bits)
        n = p * q
        phi_n = (p - 1) * (q - 1)

    d = mod_inverse(e, phi_n)

    elapsed = time.time() - start
    print(f"Key generation time: {elapsed:.2f} seconds")
    print(f"Public exponent e = {e}")
    print(f"Key size: {bits} bits")
    print()

    return (n, e), (n, d), p, q


def rsa_encrypt(M, public_key):
    """Encrypt message M using public key (n, e)."""
    n, e = public_key
    return pow(M, e, n)


def rsa_decrypt(C, private_key):
    """Decrypt ciphertext C using private key (n, d)."""
    n, d = private_key
    return pow(C, d, n)


def text_to_int(text):
    """Convert text to integer."""
    return int.from_bytes(text.encode('utf-8'), 'big')


def int_to_text(number):
    """Convert integer to text."""
    byte_length = (number.bit_length() + 7) // 8
    return number.to_bytes(byte_length, 'big').decode('utf-8')


def full_rsa_demo():
    """Demonstrate RSA with realistic key sizes."""
    print("--- Full RSA with Real Keys (2048-bit) ---")

    # Generate keys
    public_key, private_key, p, q = rsa_keygen(2048)
    n, e = public_key
    _, d = private_key

    # Encrypt a message
    message = "Hello RSA!"
    print(f"Original message: '{message}'")

    M = text_to_int(message)
    print(f"Message as integer: {M}")
    print(f"Message bit length: {M.bit_length()}")

    if M >= n:
        print("ERROR: Message too large for key size!")
        return

    print(f"\nEncrypting '{message}' ...")
    start = time.time()
    C = rsa_encrypt(M, public_key)
    enc_time = time.time() - start
    print(f"Ciphertext (hex): {hex(C)[:60]}...")
    print(f"Encryption time: {enc_time:.4f}s")

    print(f"\nDecrypting ...")
    start = time.time()
    M_dec = rsa_decrypt(C, private_key)
    dec_time = time.time() - start
    decrypted = int_to_text(M_dec)
    print(f"Decrypted: {decrypted}")
    print(f"Decryption time: {dec_time:.4f}s")
    print(f"Correct: {message == decrypted}")
    print()


# ============================================================
# RSA Digital Signature
# ============================================================

def rsa_sign_demo():
    """Demonstrate RSA digital signature."""
    print("--- RSA Digital Signature ---")

    # Generate keys
    public_key, private_key, _, _ = rsa_keygen(2048)
    n, e = public_key
    _, d = private_key

    # Sign a message
    message = "Important document"
    print(f"Message: '{message}'")

    # Hash the message (simulated)
    msg_hash = int(hashlib.sha256(message.encode()).hexdigest(), 16)
    msg_hash_reduced = msg_hash % n  # Ensure hash < n
    print(f"Message hash (reduced): {hex(msg_hash_reduced)[:40]}...")

    # Sign: S = H(m)^d mod n
    print(f"\nSigning message ...")
    start = time.time()
    signature = pow(msg_hash_reduced, d, n)
    sign_time = time.time() - start
    print(f"Signature (hex): {hex(signature)[:60]}...")
    print(f"Signing time: {sign_time:.4f}s")

    # Verify: S^e mod n == H(m)
    print(f"\nVerifying signature ...")
    start = time.time()
    verified_hash = pow(signature, e, n)
    verify_time = time.time() - start
    is_valid = verified_hash == msg_hash_reduced
    print(f"Signature valid: {is_valid}")
    print(f"Verification time: {verify_time:.4f}s")

    # Demonstrate tampering
    print(f"\n--- Tampering Detection ---")
    tampered_msg = "Tampered document"
    tampered_hash = int(hashlib.sha256(tampered_msg.encode()).hexdigest(), 16) % n
    tampered_valid = (verified_hash == tampered_hash)
    print(f"Tampered message: '{tampered_msg}'")
    print(f"Signature valid for tampered message: {tampered_valid}")
    print()


# ============================================================
# RSA Performance Benchmark
# ============================================================

def performance_demo():
    """Benchmark RSA operations."""
    print("--- RSA Performance ---")

    for key_size in [1024, 2048, 3072]:
        print(f"\nKey size: {key_size} bits")

        start = time.time()
        public_key, private_key, _, _ = rsa_keygen(key_size)
        gen_time = time.time() - start

        M = 42
        start = time.time()
        for _ in range(100):
            C = rsa_encrypt(M, public_key)
        enc_time = (time.time() - start) / 100

        start = time.time()
        for _ in range(100):
            rsa_decrypt(C, private_key)
        dec_time = (time.time() - start) / 100

        print(f"  Key generation: {gen_time:.3f}s")
        print(f"  Encryption:     {enc_time:.6f}s")
        print(f"  Decryption:     {dec_time:.6f}s")
    print()


# ============================================================
# Main
# ============================================================

def main():
    print("=" * 55)
    print("  RSA Algorithm Demo for Cryptography")
    print("=" * 55)
    print()

    small_rsa_demo()
    full_rsa_demo()
    rsa_sign_demo()
    performance_demo()

    print("=" * 55)
    print("  All RSA demos completed successfully!")
    print("=" * 55)


if __name__ == "__main__":
    main()
