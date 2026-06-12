"""
PRNG vs CSPRNG comparison demo.

Demonstrates the difference between Python's random (Mersenne Twister, not
cryptographically secure) and secrets (CSPRNG backed by the OS).

Usage:
    python random_demo.py                # Run all demos
    python random_demo.py --predict      # Show PRNG predictability
    python random_demo.py --compare      # Compare random vs secrets
    python random_demo.py --entropy      # Entropy concepts
"""

import argparse
import math
import secrets
import struct
import time
import random as insecure_random


def demo_predict():
    """Show that Python random module output is predictable."""
    print("=" * 60)
    print("PRNG (random module) Predictability Demo")
    print("=" * 60)

    # Demonstrate that same seed produces same sequence
    insecure_random.seed(42)
    seq1 = [insecure_random.random() for _ in range(10)]

    insecure_random.seed(42)
    seq2 = [insecure_random.random() for _ in range(10)]

    print("\n[1] Same seed => same sequence:")
    print(f"  Seed 42, run 1: {seq1[:5]}")
    print(f"  Seed 42, run 2: {seq2[:5]}")
    print(f"  Identical: {seq1 == seq2}")

    print("\n[2] Mersenne Twister state recovery:")
    print("  The MT19937 generator has 624 internal 32-bit state words.")
    print("  Given 624 consecutive outputs, the full internal state")
    print("  can be recovered, and all future outputs predicted.")

    # Simplified demo: show that time-based seed is trivially brute-forceable
    print("\n[3] Time-based seed brute force:")
    current_time = int(time.time())
    insecure_random.seed(current_time)
    target = [insecure_random.random() for _ in range(3)]
    print(f"  Seeded with current epoch: {current_time}")
    print(f"  First 3 outputs: {[f'{v:.10f}' for v in target]}")
    print("  An attacker who knows the approximate time can try")
    print("  all seeds in a small window to recover the sequence.")

    # Actually brute-force a small window
    print("\n  Brute-forcing seed (checking +/- 10 seconds)...")
    for t in range(current_time - 10, current_time + 11):
        insecure_random.seed(t)
        trial = [insecure_random.random() for _ in range(3)]
        if trial == target:
            print(f"  [+] FOUND! Seed = {t}")
            print(f"  All future outputs are now predictable.")
            break

    print()


def demo_compare():
    """Compare random (PRNG) vs secrets (CSPRNG) statistical properties."""
    print("=" * 60)
    print("random vs secrets Statistical Comparison")
    print("=" * 60)

    n = 10000

    # Generate samples
    random_samples = [insecure_random.random() for _ in range(n)]
    secure_samples = [secrets.randbelow(10**9) / 10**9 for _ in range(n)]

    # Compute statistics
    for name, samples in [("random (PRNG)", random_samples),
                           ("secrets (CSPRNG)", secure_samples)]:
        mean = sum(samples) / len(samples)
        var = sum((x - mean) ** 2 for x in samples) / len(samples)
        std = math.sqrt(var)
        print(f"\n  {name} ({n} samples in [0,1)):")
        print(f"    Mean:     {mean:.6f}  (ideal: 0.500000)")
        print(f"    Std Dev:  {std:.6f}  (ideal: 0.288675)")
        print(f"    Min:      {min(samples):.10f}")
        print(f"    Max:      {max(samples):.10f}")

    print("\n[!] Both have similar statistics, but random is PREDICTABLE.")
    print("    secrets uses the OS CSPRNG and is safe for cryptography.\n")

    # Demonstrate secrets API
    print("CSPRNG (secrets) API examples:")
    print(f"  Token (URL-safe, 32 bytes): {secrets.token_urlsafe(32)[:40]}...")
    print(f"  Token (hex, 16 bytes):      {secrets.token_hex(16)}")
    print(f"  Token (bytes, 8 bytes):      {secrets.token_hex(8)}")
    print(f"  Random integer [1, 100]:     {secrets.randbelow(100) + 1}")
    print(f"  Random choice from list:     {secrets.choice(['A', 'B', 'C', 'D'])}")
    print()


def demo_entropy():
    """Demonstrate the concept of information entropy."""
    print("=" * 60)
    print("Entropy (Information Theory) Demo")
    print("=" * 60)

    def shannon_entropy(probs):
        """Calculate Shannon entropy H = -sum(p * log2(p))."""
        h = 0.0
        for p in probs:
            if p > 0:
                h -= p * math.log2(p)
        return h

    # Fair coin
    print("\n[1] Fair coin (50/50):")
    h = shannon_entropy([0.5, 0.5])
    print(f"  H = -0.5*log2(0.5) - 0.5*log2(0.5) = {h:.4f} bits")

    # Fair dice
    print("\n[2] Fair dice (6 sides):")
    h = shannon_entropy([1 / 6] * 6)
    print(f"  H = {h:.4f} bits")

    # Biased coin (90% heads)
    print("\n[3] Biased coin (90% heads, 10% tails):")
    h = shannon_entropy([0.9, 0.1])
    print(f"  H = {h:.4f} bits  (much less than fair coin)")

    # Fully predictable
    print("\n[4] Fully predictable (100% heads):")
    h = shannon_entropy([1.0])
    print(f"  H = {h:.4f} bits  (zero uncertainty)")

    # Practical: password entropy
    print("\n[5] Password entropy:")
    charset_lower = 26
    charset_alnum = 62
    charset_printable = 95

    for length in [8, 12, 16, 32]:
        h_lower = length * math.log2(charset_lower)
        h_alnum = length * math.log2(charset_alnum)
        h_print = length * math.log2(charset_printable)
        print(f"  {length}-char password:")
        print(f"    lowercase only:   {h_lower:.1f} bits")
        print(f"    alphanumeric:     {h_alnum:.1f} bits")
        print(f"    printable ASCII:  {h_print:.1f} bits")

    print("\n[!] AES-256 requires 256 bits of entropy for its key.")
    print("    A 32-char random printable ASCII password provides ~211 bits.")
    print("    Use a CSPRNG (secrets.token_hex(32)) to generate keys directly.\n")


def main():
    parser = argparse.ArgumentParser(description="PRNG vs CSPRNG demo")
    parser.add_argument("--predict", action="store_true",
                        help="Show PRNG predictability")
    parser.add_argument("--compare", action="store_true",
                        help="Compare random vs secrets")
    parser.add_argument("--entropy", action="store_true",
                        help="Entropy concepts demo")
    args = parser.parse_args()

    run_all = not any([args.predict, args.compare, args.entropy])

    if run_all or args.predict:
        demo_predict()
    if run_all or args.compare:
        demo_compare()
    if run_all or args.entropy:
        demo_entropy()


if __name__ == "__main__":
    main()
