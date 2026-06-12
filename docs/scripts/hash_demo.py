#!/usr/bin/env python3
"""
Hash Algorithm Comparison Demo
Demonstrates MD5, SHA-1, SHA-256, SHA-512, SHA3-256:
- Output length comparison
- Avalanche effect (1-bit input change)
- Speed benchmarking

Usage:
    python hash_demo.py              # Basic comparison
    python hash_demo.py --avalanche  # Avalanche effect detail
    python hash_demo.py --speed      # Speed benchmark
"""

import hashlib
import time
import sys


def compute_hash(algorithm: str, data: bytes) -> str:
    """Compute hash using the specified algorithm."""
    if algorithm == "sha3_256":
        h = hashlib.sha3_256(data)
    else:
        h = hashlib.new(algorithm, data)
    return h.hexdigest()


def bit_diff(hex1: str, hex2: str) -> tuple:
    """Count the number of differing bits between two hex strings."""
    b1 = bytes.fromhex(hex1)
    b2 = bytes.fromhex(hex2)
    total_bits = len(b1) * 8
    diff_bits = 0
    for byte1, byte2 in zip(b1, b2):
        xor = byte1 ^ byte2
        diff_bits += bin(xor).count("1")
    return diff_bits, total_bits


def show_basic_info():
    """Display basic information about each hash algorithm."""
    algorithms = [
        ("md5", "MD5", "128 bit (32 hex)", "Broken"),
        ("sha1", "SHA-1", "160 bit (40 hex)", "Insecure"),
        ("sha256", "SHA-256", "256 bit (64 hex)", "Secure"),
        ("sha512", "SHA-512", "512 bit (128 hex)", "Secure"),
        ("sha3_256", "SHA3-256", "256 bit (64 hex)", "Secure"),
    ]

    print("=" * 56)
    print("  Hash Algorithm Comparison")
    print("=" * 56)
    print()
    print("--- Algorithm Info ---")
    print(f"{'Algorithm':<10} {'Output Length':<22} {'Status'}")
    print("-" * 50)
    for algo_id, name, length, status in algorithms:
        print(f"{name:<10} {length:<22} [{status}]")

    test_input = "Hello"
    print(f"\n--- Hash Outputs for '{test_input}' ---")
    print()
    for algo_id, name, _, _ in algorithms:
        digest = compute_hash(algo_id, test_input.encode())
        print(f"{name:<10}: {digest}")


def show_avalanche_effect():
    """Demonstrate the avalanche effect."""
    print("=" * 56)
    print("  Avalanche Effect Demo")
    print("=" * 56)
    print()

    pairs = [
        ("Hello", "Iello", "Change 1 char (H->I)"),
        ("Hello", "hello", "Change case (H->h)"),
        ("Hello", "Hellp", "Change last char (o->p)"),
        ("Hello", "HellO", "Change case (o->O)"),
    ]

    algorithms = [
        ("md5", "MD5"),
        ("sha1", "SHA-1"),
        ("sha256", "SHA-256"),
        ("sha512", "SHA-512"),
        ("sha3_256", "SHA3-256"),
    ]

    for input1, input2, desc in pairs:
        print(f"Input: '{input1}' -> '{input2}' ({desc})")
        print(f"  {'Algorithm':<10} {'Bits Changed':<16} {'Ratio'}")
        print(f"  {'-'*42}")
        for algo_id, name in algorithms:
            h1 = compute_hash(algo_id, input1.encode())
            h2 = compute_hash(algo_id, input2.encode())
            diff, total = bit_diff(h1, h2)
            ratio = diff / total * 100
            print(f"  {name:<10} {diff:>3}/{total:<4} bits  {ratio:5.1f}%")
        print()


def show_speed_benchmark(iterations: int = 100000):
    """Benchmark hash algorithm speed."""
    print("=" * 56)
    print(f"  Speed Benchmark ({iterations:,} iterations)")
    print("=" * 56)
    print()

    algorithms = [
        ("md5", "MD5"),
        ("sha1", "SHA-1"),
        ("sha256", "SHA-256"),
        ("sha512", "SHA-512"),
        ("sha3_256", "SHA3-256"),
    ]

    data = b"Hello World! This is a benchmark test message."
    results = []

    for algo_id, name in algorithms:
        start = time.perf_counter()
        for _ in range(iterations):
            compute_hash(algo_id, data)
        elapsed = time.perf_counter() - start
        results.append((name, elapsed))

    print(f"{'Algorithm':<10} {'Time (s)':<12} {'Hashes/sec':<15} {'Relative'}")
    print("-" * 52)

    min_time = min(t for _, t in results)
    for name, elapsed in results:
        rate = iterations / elapsed
        relative = elapsed / min_time
        print(f"{name:<10} {elapsed:<12.4f} {rate:<15,.0f} {relative:<6.2f}x")


def show_password_hash_demo():
    """Demonstrate bcrypt password hashing."""
    try:
        import bcrypt
    except ImportError:
        print("bcrypt is not installed. Install with: pip install bcrypt")
        return

    print("=" * 56)
    print("  Password Hashing Demo (bcrypt)")
    print("=" * 56)
    print()

    password = b"password123"

    print(f"Password: {password.decode()}")
    print()

    # Demonstrate different cost factors
    print("--- Cost Factor Comparison ---")
    for cost in [4, 8, 10, 12]:
        start = time.perf_counter()
        hashed = bcrypt.hashpw(password, bcrypt.gensalt(rounds=cost))
        elapsed = time.perf_counter() - start
        print(f"cost={cost}: {elapsed:.4f}s  hash={hashed.decode()[:40]}...")

    print()

    # Demonstrate salt uniqueness
    print("--- Salt Uniqueness (same password) ---")
    for i in range(3):
        hashed = bcrypt.hashpw(password, bcrypt.gensalt(rounds=10))
        print(f"Hash {i+1}: {hashed.decode()}")

    print()

    # Verify passwords
    hashed = bcrypt.hashpw(password, bcrypt.gensalt(rounds=10))
    print("--- Password Verification ---")
    print(f"Correct password:   {bcrypt.checkpw(password, hashed)}")
    print(f"Wrong password:     {bcrypt.checkpw(b'wrong_password', hashed)}")


def main():
    if "--avalanche" in sys.argv:
        show_avalanche_effect()
    elif "--speed" in sys.argv:
        show_speed_benchmark()
    elif "--bcrypt" in sys.argv:
        show_password_hash_demo()
    elif "--compare" in sys.argv:
        show_speed_benchmark()
    else:
        show_basic_info()
        print()
        show_avalanche_effect()
        print()
        show_speed_benchmark()


if __name__ == "__main__":
    main()
