#!/usr/bin/env python3
"""
Birthday Attack Simulation Demo
Demonstrates the birthday paradox and birthday attack on shortened hashes.

This script uses short hash outputs (8-16 bits) to make collision search
feasible. In real-world scenarios, hash outputs are 128-512 bits.

Usage:
    python birthday_attack.py                # Full demo
    python birthday_attack.py --paradox      # Birthday paradox only
    python birthday_attack.py --attack       # Collision attack only
"""

import hashlib
import random
import math
import time
import sys
from collections import defaultdict


def short_hash(data: str, bits: int = 16) -> str:
    """
    Compute a shortened hash of the given data.

    Uses SHA-256 internally and truncates to the specified number of bits.
    This is for educational purposes only -- real hashes are not truncated.
    """
    full_hash = hashlib.sha256(data.encode()).digest()
    # Truncate to the desired number of bits
    num_bytes = max(1, bits // 8)
    truncated = full_hash[:num_bytes]
    # Mask extra bits if bits is not a multiple of 8
    if bits % 8 != 0:
        mask = (1 << (bits % 8)) - 1
        truncated = bytes([truncated[0] & mask]) + truncated[1:]
    return truncated.hex()


def birthday_paradox_simulation(num_people: int, num_trials: int = 100000) -> float:
    """
    Simulate the birthday paradox.

    Returns the probability that at least two people share a birthday
    in a group of `num_people` people (out of 365 possible birthdays).
    """
    collisions = 0
    for _ in range(num_trials):
        birthdays = [random.randint(1, 365) for _ in range(num_people)]
        if len(birthdays) != len(set(birthdays)):
            collisions += 1
    return collisions / num_trials


def birthday_theoretical(n: int, k: int) -> float:
    """
    Calculate the theoretical probability of at least one collision.

    Args:
        n: Size of the output space (e.g., 365 for birthdays)
        k: Number of samples (e.g., number of people)

    Returns:
        Probability of at least one collision (0.0 to 1.0)
    """
    # P(no collision) = n/n * (n-1)/n * (n-2)/n * ... * (n-k+1)/n
    p_no_collision = 1.0
    for i in range(k):
        p_no_collision *= (n - i) / n
    return 1.0 - p_no_collision


def birthday_theoretical_approx(n: int) -> int:
    """
    Calculate the approximate number of samples needed for 50% collision probability.

    Uses the formula: k ≈ sqrt(pi/2 * n) ≈ 1.177 * sqrt(n)
    """
    return int(math.sqrt(math.pi / 2 * n))


def find_collision(bits: int = 16, max_attempts: int = None) -> tuple:
    """
    Find a collision using a birthday attack on shortened hashes.

    Args:
        bits: Number of bits in the shortened hash
        max_attempts: Maximum number of attempts before giving up

    Returns:
        Tuple of (attempts, msg1, msg2, hash_value) or None if no collision found
    """
    hash_space = 2 ** bits
    if max_attempts is None:
        max_attempts = hash_space * 2  # Should be more than enough

    seen = {}  # hash_value -> message

    for i in range(max_attempts):
        msg = f"msg_{i}"
        h = short_hash(msg, bits)

        if h in seen:
            return (i + 1, seen[h], msg, h)

        seen[h] = msg

    return None


def demonstrate_paradox():
    """Demonstrate the birthday paradox with simulations."""
    print("=" * 56)
    print("  Birthday Paradox Demonstration")
    print("=" * 56)
    print()
    print("In a group of N people, what is the probability that")
    print("at least two people share the same birthday (out of 365)?")
    print()

    print(f"{'N people':<10} {'Theoretical':<14} {'Simulated':<14}")
    print("-" * 38)

    test_sizes = [5, 10, 15, 20, 23, 25, 30, 40, 50, 60, 70]
    for k in test_sizes:
        theoretical = birthday_theoretical(365, k)
        simulated = birthday_paradox_simulation(k, num_trials=200000)
        print(f"{k:<10} {theoretical:<14.2%} {simulated:<14.2%}")

    print()
    print(f"The 'surprising' answer: with just 23 people, the probability")
    print(f"exceeds 50%! This is because we compare all PAIRS, not just")
    print(f"one person against everyone else.")
    print(f"  Pairs with 23 people: C(23,2) = {23*22//2}")


def demonstrate_collision_attack():
    """Demonstrate a birthday attack on shortened hashes."""
    print("=" * 56)
    print("  Birthday Attack Simulation")
    print("=" * 56)
    print()

    bit_sizes = [8, 12, 16, 20]

    print("--- Finding Collisions on Shortened Hashes ---")
    print()
    print(f"{'Bits':<6} {'Space Size':<14} {'Theory':<10} {'Actual':<10} {'Hash'}")
    print("-" * 56)

    for bits in bit_sizes:
        hash_space = 2 ** bits
        theoretical = birthday_theoretical_approx(hash_space)

        result = find_collision(bits)
        if result:
            attempts, msg1, msg2, h = result
            print(
                f"{bits:<6} {hash_space:<14,} {theoretical:<10,} {attempts:<10,} {h}"
            )
            if bits <= 12:
                print(f"       Collision: '{msg1}' == '{msg2}' -> {h}")
        else:
            print(f"{bits:<6} {hash_space:<14,} {theoretical:<10,} {'N/A':<10}")

    print()
    print("--- Scaling Analysis ---")
    print()
    print("How the required attempts scale with hash bit length:")
    print()
    print(f"{'Bits':<6} {'Hash Space':<14} {'Expected Attempts':<20} {'Security'}")
    print("-" * 54)

    for bits in [16, 32, 64, 128, 256]:
        hash_space = 2 ** bits
        expected = birthday_theoretical_approx(hash_space)
        if expected < 1_000_000:
            security = "Trivially breakable"
        elif expected < 1_000_000_000:
            security = "Breakable with CPU"
        elif expected < 2**64:
            security = "Breakable with GPU/farm"
        else:
            security = "Computationally infeasible"
        print(f"{bits:<6} 2^{bits:<10} {expected:<20,} {security}")


def demonstrate_collision_statistics():
    """Run multiple collision searches and show statistics."""
    print()
    print("=" * 56)
    print("  Collision Statistics (16-bit hash, 100 trials)")
    print("=" * 56)
    print()

    bits = 16
    hash_space = 2 ** bits
    expected = birthday_theoretical_approx(hash_space)
    num_trials = 100
    attempts_list = []

    for _ in range(num_trials):
        result = find_collision(bits)
        if result:
            attempts_list.append(result[0])

    if attempts_list:
        avg_attempts = sum(attempts_list) / len(attempts_list)
        min_attempts = min(attempts_list)
        max_attempts = max(attempts_list)

        print(f"Hash space:       {hash_space:,}")
        print(f"Theoretical:      ~{expected:,} attempts")
        print(f"Trials:           {num_trials}")
        print(f"Average attempts: {avg_attempts:,.0f}")
        print(f"Min attempts:     {min_attempts:,}")
        print(f"Max attempts:     {max_attempts:,}")
        print(f"Std deviation:    {(sum((x - avg_attempts)**2 for x in attempts_list) / len(attempts_list))**0.5:,.0f}")


def main():
    if "--paradox" in sys.argv:
        demonstrate_paradox()
    elif "--attack" in sys.argv:
        demonstrate_collision_attack()
    else:
        demonstrate_paradox()
        print()
        demonstrate_collision_attack()
        print()
        demonstrate_collision_statistics()


if __name__ == "__main__":
    main()
